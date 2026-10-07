"""
Confere a integridade dos textos publicados em partes/parte-1.html.

Uso (na raiz do repositório, depois de rodar o gerador):
    python ferramentas/conferir_integridade.py

1. MATERIAL DA AULA: compara, palavra por palavra (tokens \\w+), o Markdown original
   (conteudo/aula-1-material.md) com o texto visível da página, ignorando o que é
   atividade ou interface (elementos marcados com data-atividade). Tem de dar 100%.
2. TRADUÇÃO: confere a tradução contra o texto em inglês extraído do PDF
   (conteudo/referencia-parte-1-en.txt): mesmo número de parágrafos, proporção de palavras
   coerente em cada par (nenhum trecho pulado ou resumido), todos os números e nomes próprios.

Sai com código 1 se algo falhar.
"""
import difflib
import html.parser
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RAIZ / "partes" / "parte-1.html"
MATERIAL = RAIZ / "conteudo" / "aula-1-material.md"
REF_EN = RAIZ / "conteudo" / "referencia-parte-1-en.txt"
VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


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


def conferir_material(pagina):
    p = Texto(["material-cab", "material"])
    p.feed(pagina)
    visivel = tokens(" ".join(p.saida["material-cab"] + p.saida["material"]))
    original = tokens(MATERIAL.read_text(encoding="utf-8"))
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


NOMES = ["Donnelley", "Quebecor", "World Color Press", "Big Flower Press", "Lotus Notes", "TQM",
         "Sony", "Canon", "Sega", "Hirotaka Takeuchi", "Mariko Sakakibara", "Competitive Advantage", "Free Press"]


def numeros_en(s):
    out = []
    for n in re.findall(r"\$?\d[\d.,]*%?", s):
        n = n.rstrip(".,").lstrip("$")
        if n == "1":   # chamada da nota de rodapé colada ao texto ("a few.1")
            continue
        out.append(n.replace(".", ","))
    return out


def conferir_traducao(pagina):
    ref = REF_EN.read_text(encoding="utf-8").splitlines()
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
    en_pars = en["CORPO"] + en["QUADRO"][:4]
    ok = True
    print(f"TRADUÇÃO  parágrafos em inglês (corpo + quadro): {len(en_pars)} · na tradução: {len(pt_pars)}")
    if len(en_pars) != len(pt_pars):
        print("   FALHA: número de parágrafos diferente")
        ok = False
    # o subtítulo "Operational Effectiveness: Necessary but Not Sufficient." está colado ao §5 no inglês
    sub = "Eficácia operacional: necessária, mas não suficiente"
    razoes = []
    for k, (e, t) in enumerate(zip(en_pars, pt_pars), 1):
        we, wt = len(tokens(e)), len(tokens(t)) + (len(tokens(sub)) if k == 5 else 0)
        r = wt / we
        razoes.append(r)
        marca = "" if 0.95 <= r <= 1.45 else "   <-- FORA DA FAIXA"
        if marca:
            ok = False
        print(f"   {'§' + str(k) if k <= 18 else 'Quadro ' + str(k):>9}: {we:4d} palavras EN → {wt:4d} PT  (×{r:.2f}){marca}")
    print(f"   proporção PT/EN: mínima ×{min(razoes):.2f}, máxima ×{max(razoes):.2f} (faixa aceita: 0,95 a 1,45)")
    # notas: quadro e rodapé
    for rotulo, e in (("nota do quadro", en["QUADRO"][4]), ("nota de rodapé", en["NOTA"][0])):
        print(f"   {rotulo}: {'presente' if ('Takeuchi' in pt_todo if 'Japan' in e else 'The Free Press, 1985' in pt_todo) else 'AUSENTE'}")
    # números
    todos_en = " ".join(en["CORPO"] + en["QUADRO"] + en["NOTA"])
    faltam = sorted({n for n in numeros_en(todos_en) if n.rstrip("s") not in pt_todo})
    print("   números do original: " + ("todos presentes" if not faltam else "FALTAM " + ", ".join(faltam)))
    ok &= not faltam
    nomes = [n for n in NOMES if n not in pt_todo]
    print("   nomes próprios: " + ("todos presentes" if not nomes else "FALTAM " + ", ".join(nomes)))
    ok &= not nomes
    print("   " + ("OK: tradução completa em relação ao original." if ok else "FALHA"))
    return ok


if __name__ == "__main__":
    pagina = PAGINA.read_text(encoding="utf-8")
    r1 = conferir_material(pagina)
    print()
    r2 = conferir_traducao(pagina)
    sys.exit(0 if r1 and r2 else 1)
