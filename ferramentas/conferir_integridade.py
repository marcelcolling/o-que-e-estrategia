"""
Confere a integridade dos textos publicados nas páginas das partes (partes/parte-N.html).

Uso (na raiz do repositório, depois de rodar o gerador):
    python ferramentas/conferir_integridade.py          # todas as partes
    python ferramentas/conferir_integridade.py 2        # só a Parte II

1. MATERIAL DA AULA: compara, palavra por palavra (tokens \\w+), o Markdown do estudante
   (conteudo/aula-N-material-estudante.md) com o texto visível da página, ignorando o que é
   atividade ou interface (elementos marcados com data-atividade). Tem de dar 100%.
   (O original do professor, conteudo/aula-N-material.md, fica só como referência.)
2. TRADUÇÃO: confere a tradução contra o texto em inglês extraído do PDF
   (conteudo/referencia-parte-N-en.txt): mesmo número de parágrafos, proporção de palavras
   coerente em cada par (nenhum trecho pulado ou resumido), todos os números e nomes próprios.

Sai com código 1 se algo falhar.
"""
import difflib
import html.parser
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
C = RAIZ / "conteudo"
VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

PARTES = {
    1: {
        "pagina": RAIZ / "partes" / "parte-1.html",
        "material": C / "aula-1-material-estudante.md",
        "ref": C / "referencia-parte-1-en.txt",
        # subtítulo em linha própria na tradução, mas colado ao parágrafo no inglês: (número do parágrafo, texto)
        "subtitulos": [(5, "Eficácia operacional: necessária, mas não suficiente")],
        "n_quadro": 4,                                   # parágrafos de quadro numerados como .par
        "extras": [("nota do quadro", "Takeuchi"), ("nota de rodapé", "The Free Press, 1985")],
        "nomes": ["Donnelley", "Quebecor", "World Color Press", "Big Flower Press", "Lotus Notes", "TQM",
                  "Sony", "Canon", "Sega", "Hirotaka Takeuchi", "Mariko Sakakibara", "Competitive Advantage", "Free Press"],
    },
    2: {
        "pagina": RAIZ / "partes" / "parte-2.html",
        "material": C / "aula-2-material-estudante.md",
        "ref": C / "referencia-parte-2-en.txt",
        "subtitulos": [(11, "As origens das posições estratégicas")],
        "n_quadro": 6,
        "extras": [],
        "nomes": ["Southwest", "Ikea", "Jiffy Lube", "Vanguard", "Bessemer Trust", "Citibank", "Carmike", "Delta Air Lines",
                  "Circuit City", "CarMax", "Neutrogena", "Continental Lite", "Competitive Strategy", "Free Press", "NC-17", "737"],
    },
}


class Texto(html.parser.HTMLParser):
    """Junta o texto visível dos elementos com data-integro=<alvo>, pulando data-atividade."""

    def __init__(self, alvos):
        super().__init__(convert_charrefs=True)
        self.alvos = alvos
        self.pilha = []  # (tag, dentro_do_alvo, pular)
        self.saida = {a: [] for a in alvos}
        self.pars = []    # parágrafos da tradução (div.par)
        self.par_atual = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        pai_alvo = self.pilha[-1][1] if self.pilha else None
        pai_pula = self.pilha[-1][2] if self.pilha else False
        alvo = a.get("data-integro") if a.get("data-integro") in self.alvos else pai_alvo
        pula = pai_pula or ("data-atividade" in a) or tag in ("script", "style", "template", "svg")
        if tag in VAZIOS:
            return
        if alvo == "traducao" and "par" in (a.get("class") or "").split():
            self.par_atual = []
            self.pars.append(self.par_atual)
            tag = "div-par"
        self.pilha.append((tag, alvo, pula))

    def handle_endtag(self, tag):
        if tag in VAZIOS:
            return
        while self.pilha:
            t, _, _ = self.pilha.pop()
            if t == "div-par":
                self.par_atual = None
            if t == tag or (t == "div-par" and tag == "div"):
                break

    def handle_data(self, data):
        if not self.pilha:
            return
        _, alvo, pula = self.pilha[-1]
        if alvo and not pula:
            self.saida[alvo].append(data)
            if alvo == "traducao" and self.par_atual is not None:
                self.par_atual.append(data)


def tokens(s):
    return re.findall(r"\w+", s)


def conferir_material(cfg, pagina):
    p = Texto(["material-cab", "material"])
    p.feed(pagina)
    visivel = tokens(" ".join(p.saida["material-cab"] + p.saida["material"]))
    md = "\n".join(l for l in cfg["material"].read_text(encoding="utf-8").splitlines() if not l.strip().startswith(":::"))
    original = tokens(md)
    sm = difflib.SequenceMatcher(None, original, visivel, autojunk=False)
    faltam, sobram = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op in ("delete", "replace"):
            faltam.append(" ".join(original[i1:i2]))
        if op in ("insert", "replace"):
            sobram.append(" ".join(visivel[j1:j2]))
    print(f"MATERIAL  palavras no .md: {len(original)} · na página: {len(visivel)} · semelhança: {sm.ratio():.4f}")
    for f in faltam[:15]:
        print("   faltando na página:", f[:120])
    for s in sobram[:15]:
        print("   sobrando na página:", s[:120])
    ok = not faltam and not sobram
    print("   " + ("OK: texto íntegro, mesma sequência de palavras." if ok else "FALHA"))
    return ok


def numeros(s):
    """Grupos de dígitos (sem o "000" dos milhares e sem a chamada de nota "1")."""
    return {n for n in re.findall(r"\d+", s) if n not in ("000", "1")}


def conferir_traducao(cfg, pagina):
    ref = cfg["ref"].read_text(encoding="utf-8").splitlines()
    sec, en = None, {"CORPO": [], "QUADRO": [], "NOTA": []}
    for l in ref:
        m = re.fullmatch(r"\[(CORPO|QUADRO|NOTA)\]", l.strip())
        if m:
            sec = m.group(1)
            continue
        if sec and l.strip():
            en[sec].append(l.strip())
    p = Texto(["traducao"])
    p.feed(pagina)
    pt_pars = [" ".join(x).strip() for x in p.pars]
    pt_todo = " ".join(p.saida["traducao"])
    n_corpo = len(en["CORPO"])
    en_pars = en["CORPO"] + en["QUADRO"][:cfg["n_quadro"]]
    ok = True
    print(f"TRADUÇÃO  parágrafos em inglês (corpo + quadros): {len(en_pars)} · na tradução: {len(pt_pars)}")
    if len(en_pars) != len(pt_pars):
        print("   FALHA: número de parágrafos diferente")
        ok = False
    subs = dict(cfg["subtitulos"])
    razoes = []
    for k, (e, t) in enumerate(zip(en_pars, pt_pars), 1):
        we, wt = len(tokens(e)), len(tokens(t)) + (len(tokens(subs[k])) if k in subs else 0)
        r = wt / we
        razoes.append(r)
        marca = "" if 0.95 <= r <= 1.45 else "   <-- FORA DA FAIXA"
        if marca:
            ok = False
        rot = f"§{k}" if k <= n_corpo else f"Q{k - n_corpo}"
        print(f"   {rot:>5}: {we:4d} palavras EN → {wt:4d} PT  (×{r:.2f}){marca}")
    print(f"   proporção PT/EN: mínima ×{min(razoes):.2f}, máxima ×{max(razoes):.2f} (faixa aceita: 0,95 a 1,45)")
    for rotulo, trecho in cfg["extras"]:
        presente = trecho in pt_todo
        print(f"   {rotulo}: {'presente' if presente else 'AUSENTE'}")
        ok &= presente
    faltam = sorted(numeros(" ".join(en["CORPO"] + en["QUADRO"] + en["NOTA"])) - numeros(pt_todo), key=int)
    print("   números do original: " + ("todos presentes" if not faltam else "FALTAM " + ", ".join(faltam)))
    ok &= not faltam
    nomes = [n for n in cfg["nomes"] if n not in pt_todo]
    print("   nomes próprios: " + ("todos presentes" if not nomes else "FALTAM " + ", ".join(nomes)))
    ok &= not nomes
    print("   " + ("OK: tradução completa em relação ao original." if ok else "FALHA"))
    return ok


if __name__ == "__main__":
    escolhidas = [int(a) for a in sys.argv[1:]] or sorted(PARTES)
    tudo_ok = True
    for n in escolhidas:
        cfg = PARTES[n]
        print(f"===== PARTE {n} · {cfg['pagina'].name}")
        pagina = cfg["pagina"].read_text(encoding="utf-8")
        tudo_ok &= conferir_material(cfg, pagina)
        print()
        tudo_ok &= conferir_traducao(cfg, pagina)
        print()
    sys.exit(0 if tudo_ok else 1)
