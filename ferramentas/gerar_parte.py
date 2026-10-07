"""
Gera a página de uma parte do artigo (ex.: partes/parte-1.html) a partir de:
  - conteudo/porter-parte-N-traducao.md   tradução do texto de Porter (formato descrito abaixo)
  - conteudo/aula-N-material.md            material da aula do professor (Markdown, texto íntegro)
  - ferramentas/atividades_parte1.py       as caixas de atividade e onde cada uma entra no material

Uso (na raiz do repositório):
    python ferramentas/gerar_parte.py

Os .md ficam em conteudo/, que NÃO vai para o GitHub (.gitignore): são fontes locais.
O texto do material é mantido na íntegra: o script só converte a marcação e encaixa
as atividades entre os blocos. Para conferir, rode ferramentas/conferir_integridade.py.

Formato da tradução (uma linha por parágrafo):
    # Título / autor: / fonte: / nota:      cabeçalho
    ## Título  |  ### Subtítulo            títulos do artigo
    [p37] texto                            parágrafo que começa na página 37
    ?PAUSA chave | pergunta                pausa para responder (caixa de atividade)
    ?FIGURA p39 | título | eixo y | eixo x | rótulo da curva | alto | baixo
    ?QUADRO p40 | título   ...   ?NOTAQUADRO texto   ?FIMQUADRO
    [^1]  /  [^1]: texto                   nota de rodapé
"""
import html
import math
import pathlib
import re
import sys
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "ferramentas"))
import atividades_parte1 as AT  # noqa: E402

PARTES = [
    {
        "n": 1,
        "traducao": RAIZ / "conteudo" / "porter-parte-1-traducao.md",
        "material": RAIZ / "conteudo" / "aula-1-material.md",
        "destino": RAIZ / "partes" / "parte-1.html",
        "atividades": AT,
    },
]


# ---------------------------------------------------------------- utilidades
def slug(texto, usados):
    s = unicodedata.normalize("NFD", texto)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:56] or "secao"
    base, n = s, 2
    while s in usados:
        s = f"{base}-{n}"
        n += 1
    usados.add(s)
    return s


def inline(texto):
    s = html.escape(texto, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\[\^(\d+)\]", r'<sup class="nota-ref"><a href="#nota-\1" id="ref-\1">\1</a></sup>', s)
    return s


def puro(texto):
    return re.sub(r"\*+", "", texto)


def palavras(texto):
    return len(re.findall(r"\w+", texto))


# ================================================================ TRADUÇÃO
def render_traducao(md, at):
    linhas = [l.rstrip() for l in md.splitlines()]
    meta, corpo, nav = {}, [], []
    usados = set()
    par = 0
    pagina = None
    no_quadro = False
    n_quadro = 0
    nota_rodape = {}
    total_pal = 0
    for l in linhas:
        s = l.strip()
        if not s:
            continue
        m = re.match(r"^(autor|fonte|nota):\s*(.+)$", s)
        if m:
            meta[m.group(1)] = m.group(2)
            continue
        if s.startswith("# "):
            meta["titulo"] = s[2:]
            continue
        m = re.match(r"^\[\^(\d+)\]:\s*(.+)$", s)
        if m:
            nota_rodape[m.group(1)] = m.group(2)
            continue
        if s.startswith("## "):
            sid = slug(s[3:], usados)
            nav.append((2, sid, puro(s[3:])))
            corpo.append(f'<h2 class="t-h2" id="{sid}">{inline(s[3:])}</h2>')
            continue
        if s.startswith("### "):
            sid = slug(s[4:], usados)
            nav.append((2, sid, puro(s[4:])))
            corpo.append(f'<h3 class="t-h3" id="{sid}">{inline(s[4:])}</h3>')
            continue
        if s.startswith("?PAUSA"):
            chave, perg = [x.strip() for x in s[len("?PAUSA"):].split("|", 1)]
            corpo.append(at.pausa(chave, perg))
            continue
        if s.startswith("?FIGURA"):
            partes = [x.strip() for x in s[len("?FIGURA"):].split("|")]
            pag, titulo, eixo_y, eixo_x, curva, alto, baixo = partes
            nav.append((2, "figura-fronteira", "Figura: " + titulo))
            corpo.append(figura_fronteira(pag[1:], titulo, eixo_y, eixo_x, curva, alto, baixo))
            continue
        if s.startswith("?QUADRO"):
            pag, titulo = [x.strip() for x in s[len("?QUADRO"):].split("|", 1)]
            nav.append((2, "quadro-japao", "Quadro: " + titulo))
            corpo.append(
                f'<aside class="quadro" id="quadro-japao"><div class="quadro-cab"><span class="quadro-eyebrow">'
                f'Quadro · p. {pag[1:]}</span><h3>{inline(titulo)}</h3></div><div class="quadro-corpo">'
            )
            no_quadro = True
            continue
        if s.startswith("?NOTAQUADRO"):
            corpo.append(f'<p class="quadro-nota">{inline(s[len("?NOTAQUADRO"):].strip())}</p>')
            continue
        if s.startswith("?FIMQUADRO"):
            corpo.append("</div></aside>")
            no_quadro = False
            continue
        # parágrafo
        m = re.match(r"^\[p(\d+)\]\s*(.+)$", s)
        texto = s
        nova_pag = None
        if m:
            nova_pag, texto = m.group(1), m.group(2)
            pagina = nova_pag
        par += 1
        total_pal += palavras(texto)
        pid = f"p{par}"
        if no_quadro:
            n_quadro += 1
        rot = f"Q{n_quadro}" if no_quadro else f"§{par}"
        pag_html = f'<span class="par-pag">p. {nova_pag}</span>' if nova_pag else ""
        corpo.append(
            f'<div class="par{" par-quadro" if no_quadro else ""}" id="{pid}" data-par="{par}" data-rotulo="{rot}">'
            f'<div class="par-margem"><span class="par-num">{rot}</span>{pag_html}</div>'
            f'<div class="par-texto"><p>{inline(texto)}</p>'
            f'<div class="par-nota" data-atividade hidden><label><span>Minha anotação sobre {rot}</span>'
            f'<textarea data-nota="{par}" rows="3" placeholder="O que este trecho diz para você? Concorda? Que exemplo do seu setor ilustra isso?"></textarea></label></div>'
            f"</div>"
            f'<div class="par-ferr" data-atividade><button type="button" class="b-dest" aria-pressed="false" title="Destacar este parágrafo">'
            f'<span aria-hidden="true">▍</span>Destacar</button><button type="button" class="b-nota" title="Escrever uma anotação">'
            f'<span aria-hidden="true">✎</span>Anotar</button></div>'
            f"</div>"
        )
    if nota_rodape:
        itens = "".join(
            f'<li id="nota-{k}"><span class="nota-n">{k}</span> {inline(v)} <a href="#ref-{k}" class="nota-volta" data-atividade aria-label="Voltar ao texto">↩</a></li>'
            for k, v in nota_rodape.items()
        )
        corpo.append(f'<div class="notas-rodape"><h4>Nota do autor</h4><ol>{itens}</ol></div>')
        total_pal += sum(palavras(v) for v in nota_rodape.values())
    return meta, "\n".join(corpo), nav, total_pal, par


def figura_fronteira(pag, titulo, eixo_y, eixo_x, curva, alto, baixo):
    # recriação da figura da p. 39: curva côncava (a fronteira) num quadrado; eixo x vai de custo alto a baixo
    return f"""<figure class="figura" id="figura-fronteira">
<figcaption><span class="quadro-eyebrow">Figura · p. {pag}</span><strong>{html.escape(titulo)}</strong></figcaption>
<svg viewBox="0 0 520 380" role="img" aria-label="{html.escape(titulo)}: {html.escape(eixo_y)} no eixo vertical, {html.escape(eixo_x)} no eixo horizontal, e a curva da {html.escape(curva)}.">
  <rect x="70" y="20" width="420" height="300" rx="6" fill="#EFEEE7"/>
  <path d="M110 58 C 330 52, 432 90, 452 300" fill="none" stroke="#1F3A5F" stroke-width="4" stroke-linecap="round"/>
  <text x="128" y="96" class="fig-rot"><tspan x="128">{html.escape(curva.split(" (")[0])}</tspan><tspan x="128" dy="16" class="fig-rot-sub">{html.escape("(" + curva.split(" (")[1]) if " (" in curva else ""}</tspan></text>
  <text x="58" y="34" text-anchor="end" class="fig-ax">{html.escape(alto)}</text>
  <text x="58" y="318" text-anchor="end" class="fig-ax">{html.escape(baixo)}</text>
  <text x="74" y="342" class="fig-ax">{html.escape(alto)}</text>
  <text x="488" y="342" text-anchor="end" class="fig-ax">{html.escape(baixo)}</text>
  <text x="280" y="370" text-anchor="middle" class="fig-eixo">{html.escape(eixo_x)}</text>
  <text x="22" y="170" text-anchor="middle" class="fig-eixo" transform="rotate(-90 22 170)">{html.escape(eixo_y)}</text>
</svg>
<p class="fig-nota" data-atividade>Figura redesenhada a partir do original. Mover-se <em>em direção</em> à curva é eficácia operacional; escolher <em>onde</em> ficar ao longo dela é posicionamento.</p>
</figure>"""


# ================================================================ MATERIAL (Markdown)
INICIO = re.compile(r"^(#{1,6}\s|\||\s*[-*] |\s*\d+\.\s|>|```|-{3,}\s*$)")


def blocos(linhas):
    i, n = 0, len(linhas)
    while i < n:
        bruto = linhas[i]
        s = bruto.strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):
            cod = []
            i += 1
            while i < n and not linhas[i].strip().startswith("```"):
                cod.append(linhas[i])
                i += 1
            i += 1
            yield ("code", "\n".join(cod))
            continue
        if re.fullmatch(r"-{3,}", s):
            yield ("hr",)
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            yield ("h", len(m.group(1)), m.group(2).strip())
            i += 1
            continue
        if s.startswith("|"):
            tab = []
            while i < n and linhas[i].strip().startswith("|"):
                tab.append(linhas[i].strip())
                i += 1
            yield ("table", tab)
            continue
        if s.startswith(">"):
            q = []
            while i < n and linhas[i].strip().startswith(">"):
                q.append(re.sub(r"^>\s?", "", linhas[i].strip()))
                i += 1
            # cada linha não vazia é um parágrafo (o material separa rótulos em linhas próprias)
            yield ("quote", [x for x in q if x.strip()])
            continue
        if re.match(r"^[-*] ", s) or re.match(r"^\d+\.\s", s):
            ordenada = bool(re.match(r"^\d+\.\s", s))
            itens = []  # (nível, número|None, texto)
            while i < n:
                l = linhas[i]
                if not l.strip():
                    # lista continua se a próxima linha não vazia for item
                    k = i + 1
                    while k < n and not linhas[k].strip():
                        k += 1
                    if k < n and re.match(r"^\s*([-*]|\d+\.)\s", linhas[k]) and (
                        bool(re.match(r"^\s*\d+\.\s", linhas[k])) == ordenada or linhas[k].startswith("  ")
                    ):
                        i = k
                        continue
                    break
                mm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", l)
                if not mm:
                    break
                nivel = 1 if len(mm.group(1)) >= 2 else 0
                num = mm.group(2)[:-1] if mm.group(2)[0].isdigit() else None
                itens.append((nivel, num, mm.group(3)))
                i += 1
            yield ("ol" if ordenada else "ul", itens)
            continue
        par = [s]
        i += 1
        while i < n and linhas[i].strip() and not INICIO.match(linhas[i]):
            par.append(linhas[i].strip())
            i += 1
        yield ("p", " ".join(par))


def celulas(linha):
    linha = linha.strip().strip("|")
    return [c.strip() for c in linha.split("|")]


def render_tabela(tab):
    cab = celulas(tab[0])
    corpo = [celulas(l) for l in tab[1:] if not re.fullmatch(r"\|?[\s:\-|]+\|?", l)]
    classes = "tabela" + (" tabela-cards" if len(cab) >= 3 else "")
    out = [f'<div class="tabela-wrap"><table class="{classes}"><thead><tr>']
    out += [f"<th>{inline(c)}</th>" for c in cab]
    out.append("</tr></thead><tbody>")
    for linha in corpo:
        out.append("<tr>" + "".join(
            f'<td data-label="{html.escape(puro(cab[j]) if j < len(cab) else "", quote=True)}">{inline(c)}</td>'
            for j, c in enumerate(linha)) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def render_lista(tipo, itens):
    out, aberto_sub = [], False
    tag = "ol" if tipo == "ol" else "ul"
    out.append(f'<{tag} class="{"numerada" if tag == "ol" else "lista"}">')
    for k, (nivel, num, txt) in enumerate(itens):
        if nivel == 1 and not aberto_sub:
            out[-1] = out[-1][:-5] if out[-1].endswith("</li>") else out[-1]
            out.append('<ul class="lista sub">')
            aberto_sub = True
        if nivel == 0 and aberto_sub:
            out.append("</ul></li>")
            aberto_sub = False
        n_html = f'<span class="n">{num}.</span> ' if num else ""
        out.append(f"<li>{n_html}{inline(txt)}</li>")
    if aberto_sub:
        out.append("</ul></li>")
    out.append(f"</{tag}>")
    return "".join(out)


ROTULOS_CHAVE = ("Implicação para execução", "Frase para o quadro", "Mensagem-chave", "Conclusão que Porter endossaria")
ROTULOS_NOTA = ("Nota ao professor", "Nota sobre o tempo", "Como conduzir", "Como tratar em sala",
                "Cuidado com o limite do gráfico", "Nuance para a turma", "Aviso de escopo", "Cuidado prático",
                "Para situar os alunos no debate da época")
ROTULOS_REVELAR = {"Resposta esperada": "Ver a resposta esperada", "Pistas de resposta": "Ver as pistas de resposta"}


def render_paragrafo(texto):
    m = re.match(r"^\*\*(.+?)[.:]?\*\*", texto)
    if m:
        rot = m.group(1).rstrip(".:")
        if rot in ROTULOS_CHAVE:
            return f'<div class="callout callout-chave"><p>{inline(texto)}</p></div>'
        if rot in ROTULOS_NOTA:
            return f'<div class="callout callout-nota"><p>{inline(texto)}</p></div>'
        return f'<p class="p-rotulo">{inline(texto)}</p>'
    return f"<p>{inline(texto)}</p>"


def render_bloco(b):
    t = b[0]
    if t == "p":
        return render_paragrafo(b[1])
    if t == "table":
        return render_tabela(b[1])
    if t in ("ul", "ol"):
        return render_lista(t, b[1])
    if t == "code":
        return f'<pre class="esboco">{html.escape(b[1])}</pre>'
    if t == "quote":
        return '<blockquote class="pergunta">' + "".join(f"<p>{inline(x)}</p>" for x in b[1]) + "</blockquote>"
    return ""


def eh_revelar(b):
    if b[0] != "p":
        return None
    m = re.match(r"^\*\*(.+?):\*\*", b[1])
    return ROTULOS_REVELAR.get(m.group(1)) if m else None


def render_unidade(titulo, blocos_u, regra, at):
    """Renderiza uma subseção (### ...) aplicando a regra de atividades."""
    out = []
    regra = regra or {}
    out += [at.bloco(x) for x in regra.get("apos_titulo", [])]
    resto = list(blocos_u)
    if regra.get("recolher"):
        corpo = "".join(render_bloco(b) for b in resto)
        out.append(f'<details class="revelar revelar-longo"><summary data-atividade><span class="rev-ico" aria-hidden="true">+</span>'
                   f'{regra.get("rotulo_recolher", "Ler a resposta do material")}</summary><div class="revelar-corpo">{corpo}</div></details>')
        resto = []
    k = 0
    while k < len(resto):
        b = resto[k]
        rot = eh_revelar(b)
        if rot:
            out += [at.bloco(x) for x in regra.get("antes_revelar", [])]
            corpo = "".join(render_bloco(x) for x in resto[k:])
            out.append(f'<details class="revelar"><summary data-atividade><span class="rev-ico" aria-hidden="true">+</span>{rot}</summary>'
                       f'<div class="revelar-corpo">{corpo}</div></details>')
            k = len(resto)
            break
        if b[0] == "quote" and any(x.startswith("**Resposta:**") for x in b[1]):
            perg = [x for x in b[1] if not x.startswith("**Resposta:**")]
            resp = [x for x in b[1] if x.startswith("**Resposta:**")]
            out.append('<blockquote class="pergunta">' + "".join(f"<p>{inline(x)}</p>" for x in perg) + "</blockquote>")
            out += [at.bloco(x) for x in regra.get("antes_revelar", [])]
            out.append('<details class="revelar"><summary data-atividade><span class="rev-ico" aria-hidden="true">+</span>Ver a resposta</summary>'
                       '<div class="revelar-corpo">' + "".join(f"<p>{inline(x)}</p>" for x in resp) + "</div></details>")
            k += 1
            continue
        out.append(render_bloco(b))
        for depois_de, tpls in regra.get("apos_bloco", []):
            if b[0] in ("p", "quote", "table") and depois_de in (b[1] if b[0] == "p" else " ".join(b[1]) if b[0] == "quote" else b[1][0]):
                out += [at.bloco(x) for x in tpls]
        k += 1
    out += [at.bloco(x) for x in regra.get("fim", [])]
    return "".join(out)


def regra_para(titulo, at):
    for prefixo, regra in at.REGRAS:
        if titulo.startswith(prefixo):
            return regra
    return None


def render_material(md, at):
    lista = list(blocos(md.splitlines()))
    usados = set()
    titulo, subtitulo, ficha = "", "", []
    nav = []
    # 1) separa cabeçalho (até o primeiro ##, sem contar o subtítulo)
    k = 0
    while k < len(lista):
        b = lista[k]
        if b[0] == "h" and b[1] == 1:
            titulo = b[2]
        elif b[0] == "h" and b[1] == 2 and not subtitulo:
            subtitulo = b[2]
        elif b[0] == "h":
            break
        elif b[0] == "p":
            ficha.append(b[1])
        k += 1
    # 2) agrupa em seções (##) e unidades (### / ####)
    secoes = []
    for b in lista[k:]:
        if b[0] == "hr":
            continue
        if b[0] == "h" and b[1] == 2:
            secoes.append({"titulo": b[2], "intro": [], "unidades": []})
        elif b[0] == "h" and b[1] >= 3:
            secoes[-1]["unidades"].append({"nivel": b[1], "titulo": b[2], "blocos": []})
        else:
            alvo = secoes[-1]["unidades"][-1]["blocos"] if secoes[-1]["unidades"] else secoes[-1]["intro"]
            alvo.append(b)
    out = []
    for s in secoes:
        sid = slug(s["titulo"], usados)
        m = re.match(r"^(Bloco \d+|Apêndice [A-Z]|\d+\.)\s*:?\s*(.*)$", s["titulo"])
        nav.append((2, sid, puro(s["titulo"])))
        classe = "secao m-sec" + (" m-apendice" if s["titulo"].startswith("Apêndice") else "")
        if m and m.group(1).startswith("Bloco"):
            cab = f'<h2 class="secao-titulo"><span class="secao-cod">{html.escape(m.group(1))}</span>{inline(s["titulo"][len(m.group(1)):].lstrip(": "))}</h2>'
            # o rótulo "Bloco N" precisa continuar no texto: fica no selo, e o ":" é só pontuação
        else:
            cab = f'<h2 class="secao-titulo">{inline(s["titulo"])}</h2>'
        out.append(f'<section class="{classe}" id="{sid}">{cab}')
        regra_sec = regra_para(s["titulo"], at)
        out.append(render_unidade(s["titulo"], s["intro"], regra_sec, at) if (s["intro"] or regra_sec) else "")
        for u in s["unidades"]:
            uid = slug(u["titulo"], usados)
            if s["titulo"].startswith("Bloco 7") and u["nivel"] == 3:
                nav.append((3, uid, puro(u["titulo"])))
            h = "h3" if u["nivel"] == 3 else "h4"
            out.append(f'<div class="m-unidade" id="{uid}"><{h} class="m-{h}">{inline(u["titulo"])}</{h}>')
            out.append(render_unidade(u["titulo"], u["blocos"], regra_para(u["titulo"], at), at))
            out.append("</div>")
        out.append("</section>")
    return titulo, subtitulo, ficha, "\n".join(out), nav


# ================================================================ PÁGINA
def gerar(cfg):
    at = cfg["atividades"]
    meta, html_trad, nav_t, pal_t, n_par = render_traducao(cfg["traducao"].read_text(encoding="utf-8"), at)
    md_mat = cfg["material"].read_text(encoding="utf-8")
    titulo_m, sub_m, ficha, html_mat, nav_m = render_material(md_mat, at)
    pal_m = palavras(md_mat)
    min_t = max(1, math.ceil(pal_t / 200))
    min_m = max(1, math.ceil(pal_m / 210))

    def navhtml(itens):
        return "\n  ".join(
            f'<a class="nav-item{" sub" if nv == 3 or (nv == 2 and grupo) else ""}" href="#{sid}">{html.escape(r)}</a>'
            for nv, sid, r, grupo in itens)

    nav = ['<a class="nav-grupo" href="#texto">A · Texto de Porter</a>']
    nav.append(navhtml([(nv, sid, r, True) for nv, sid, r in nav_t]))
    nav.append('<a class="nav-grupo" href="#material">B · Material da aula</a>')
    nav.append(navhtml([(nv, sid, r, nv == 3) for nv, sid, r in nav_m]))
    nav.append('<a class="nav-grupo nav-destaque" href="#simulador">★ Simulador Vivelar</a>')
    nav.append('<a class="nav-grupo" href="#minhas-respostas">✓ Minhas respostas</a>')

    ficha_html = "".join(f"<p>{inline(p)}</p>" for p in ficha)
    valores = dict(
        n=cfg["n"],
        titulo_pagina=html.escape(f"Parte I · {puro(titulo_m)}"),
        titulo_m=inline(titulo_m),
        sub_m=inline(sub_m),
        ficha=ficha_html,
        nav="\n  ".join(nav),
        traducao=html_trad,
        material=html_mat,
        t_titulo=html.escape(meta.get("titulo", "")),
        t_autor=html.escape(meta.get("autor", "")),
        t_fonte=html.escape(meta.get("fonte", "")),
        t_nota=inline(meta.get("nota", "")),
        min_t=min_t,
        min_m=min_m,
        n_par=n_par,
        pre=at.bloco("prep"),
    )
    pagina = at.MODELO
    for k, v in valores.items():
        pagina = pagina.replace("{{" + k + "}}", str(v))
    resto = re.findall(r"\{\{\w+\}\}", pagina)
    if resto:
        sys.exit(f"Marcadores sem valor no modelo: {resto}")
    cfg["destino"].parent.mkdir(parents=True, exist_ok=True)
    cfg["destino"].write_text(pagina, encoding="utf-8")
    print(f"OK  {cfg['destino'].relative_to(RAIZ)}  (tradução: {pal_t} palavras, {n_par} parágrafos · material: {pal_m} palavras)")


if __name__ == "__main__":
    for cfg in PARTES:
        gerar(cfg)
