"""
Gera a página de uma parte do artigo (ex.: partes/parte-1.html) a partir de:
  - conteudo/porter-parte-N-traducao.md        tradução do texto de Porter (formato abaixo)
  - conteudo/aula-N-material-estudante.md      material da aula na versão para o estudante (Markdown)
  - ferramentas/atividades_parteN.py            caixas de atividade, onde entram, módulos e o modelo da página

Uso (na raiz do repositório):
    python ferramentas/gerar_parte.py

A página é organizada em MÓDULOS: o Mapa de aprendizagem, o Texto de Porter e cada seção "##"
do material (Abertura, Bloco 1...7, Fechamento, Para consulta). O estudante abre um módulo por vez
a partir do índice. Os .md ficam em conteudo/, que NÃO vai para o GitHub (.gitignore).
O texto do material é mantido na íntegra (em relação ao .md do estudante): o script só converte a
marcação e encaixa as atividades. Para conferir, rode ferramentas/conferir_integridade.py.

Formato da tradução (uma linha por parágrafo):
    # Título / autor: / fonte: / nota:      cabeçalho
    ## Título  |  ### Subtítulo            títulos do artigo
    [p37] texto                            parágrafo que começa na página 37
    ?PAUSA chave | pergunta                pausa para responder (caixa de atividade)
    ?FIGURA p39 | título | eixo y | eixo x | rótulo da curva | alto | baixo
    ?QUADRO p40 | título   ...   ?NOTAQUADRO texto   ?FIMQUADRO
    [^1]  /  [^1]: texto                   nota de rodapé
Marcações extras no material:
    ::: visual nome                        esquema visual gerado por atividades_parteN.visual(nome)
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
        "material": RAIZ / "conteudo" / "aula-1-material-estudante.md",
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
    meta, corpo, subs = {}, [], []
    usados = set()
    par = 0
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
            subs.append((sid, puro(s[3:])))
            corpo.append(f'<h2 class="t-h2" id="{sid}">{inline(s[3:])}</h2>')
            continue
        if s.startswith("### "):
            sid = slug(s[4:], usados)
            subs.append((sid, puro(s[4:])))
            corpo.append(f'<h3 class="t-h3" id="{sid}">{inline(s[4:])}</h3>')
            continue
        if s.startswith("?PAUSA"):
            chave, perg = [x.strip() for x in s[len("?PAUSA"):].split("|", 1)]
            corpo.append(at.pausa(chave, perg))
            continue
        if s.startswith("?FIGURA"):
            pag, titulo, eixo_y, eixo_x, curva, alto, baixo = [x.strip() for x in s[len("?FIGURA"):].split("|")]
            subs.append(("figura-fronteira", "Figura: a fronteira"))
            corpo.append(figura_fronteira(pag[1:], titulo, eixo_y, eixo_x, curva, alto, baixo))
            continue
        if s.startswith("?QUADRO"):
            pag, titulo = [x.strip() for x in s[len("?QUADRO"):].split("|", 1)]
            subs.append(("quadro-japao", "Quadro: as empresas japonesas"))
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
        m = re.match(r"^\[p(\d+)\]\s*(.+)$", s)
        texto, nova_pag = s, None
        if m:
            nova_pag, texto = m.group(1), m.group(2)
        par += 1
        total_pal += palavras(texto)
        if no_quadro:
            n_quadro += 1
        rot = f"Q{n_quadro}" if no_quadro else f"§{par}"
        pag_html = f'<span class="par-pag">p. {nova_pag}</span>' if nova_pag else ""
        corpo.append(
            f'<div class="par{" par-quadro" if no_quadro else ""}" id="p{par}" data-par="{par}" data-rotulo="{rot}">'
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
    return meta, "\n".join(corpo), subs, total_pal, par


def figura_fronteira(pag, titulo, eixo_y, eixo_x, curva, alto, baixo):
    # recriação da figura da p. 39: curva côncava (a fronteira); o eixo x vai de custo alto a baixo
    principal, _, resto = curva.partition(" (")
    sub = "(" + resto if resto else ""
    return f"""<figure class="figura" id="figura-fronteira">
<figcaption><span class="quadro-eyebrow">Figura · p. {pag}</span><strong>{html.escape(titulo)}</strong></figcaption>
<svg viewBox="0 0 520 380" role="img" aria-label="{html.escape(titulo)}: {html.escape(eixo_y)} no eixo vertical, {html.escape(eixo_x)} no eixo horizontal, e a curva da {html.escape(curva)}.">
  <rect x="70" y="20" width="420" height="300" rx="6" fill="#EFEEE7"/>
  <path d="M110 58 C 330 52, 432 90, 452 300" fill="none" stroke="#1F3A5F" stroke-width="4" stroke-linecap="round"/>
  <text x="128" y="96" class="fig-rot"><tspan x="128">{html.escape(principal)}</tspan><tspan x="128" dy="16" class="fig-rot-sub">{html.escape(sub)}</tspan></text>
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
INICIO = re.compile(r"^(#{1,6}\s|\||\s*[-*] |\s*\d+\.\s|>|```|:::|-{3,}\s*$)")


def blocos(linhas):
    i, n = 0, len(linhas)
    while i < n:
        s = linhas[i].strip()
        if not s:
            i += 1
            continue
        if s.startswith(":::"):
            partes = s[3:].split()
            yield ("visual", partes[1] if len(partes) > 1 else "")
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
            yield ("quote", [x for x in q if x.strip()])
            continue
        if re.match(r"^[-*] ", s) or re.match(r"^\d+\.\s", s):
            ordenada = bool(re.match(r"^\d+\.\s", s))
            itens = []  # (nível, número|None, texto)
            while i < n:
                l = linhas[i]
                if not l.strip():
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
    return [c.strip() for c in linha.strip().strip("|").split("|")]


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
    for nivel, num, txt in itens:
        if nivel == 1 and not aberto_sub:
            if out[-1].endswith("</li>"):
                out[-1] = out[-1][:-5]
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


ROTULOS_CHAVE = ("Implicação para execução", "Em uma frase")
ROTULOS_NOTA = ("Cuidado prático", "Sobre o horizonte", "Antecipações", "Como estudar", "Texto-base")
ROTULOS_REVELAR = {"Comentário": "Ver o comentário", "Resposta esperada": "Ver a resposta esperada",
                   "Pistas de resposta": "Ver as pistas de resposta"}


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


def render_bloco(b, at):
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
    if t == "visual":
        return at.visual(b[1])
    return ""


def eh_revelar(b):
    if b[0] != "p":
        return None
    m = re.match(r"^\*\*(.+?):\*\*", b[1])
    return ROTULOS_REVELAR.get(m.group(1)) if m else None


def render_unidade(blocos_u, regra, at):
    """Renderiza o conteúdo de uma subseção aplicando a regra de atividades."""
    out = []
    regra = regra or {}
    out += [at.bloco(x) for x in regra.get("apos_titulo", [])]
    resto = list(blocos_u)
    if regra.get("recolher"):
        corpo = "".join(render_bloco(b, at) for b in resto)
        out.append(f'<details class="revelar revelar-longo"><summary data-atividade><span class="rev-ico" aria-hidden="true">+</span>'
                   f'{regra.get("rotulo_recolher", "Ler o comentário")}</summary><div class="revelar-corpo">{corpo}</div></details>')
        resto = []
    k = 0
    while k < len(resto):
        b = resto[k]
        rot = eh_revelar(b)
        if rot:
            out += [at.bloco(x) for x in regra.get("antes_revelar", [])]
            corpo = "".join(render_bloco(x, at) for x in resto[k:])
            out.append(f'<details class="revelar"><summary data-atividade><span class="rev-ico" aria-hidden="true">+</span>{rot}</summary>'
                       f'<div class="revelar-corpo">{corpo}</div></details>')
            break
        if regra.get("mapa") and b[0] == "ol":
            out.append(at.mapa(b[1], inline))
        else:
            out.append(render_bloco(b, at))
        for depois_de, tpls in regra.get("apos_bloco", []):
            alvo = b[1] if b[0] == "p" else " ".join(b[1]) if b[0] == "quote" else ""
            if isinstance(alvo, str) and depois_de in alvo:
                out += [at.bloco(x) for x in tpls]
        k += 1
    out += [at.bloco(x) for x in regra.get("fim", [])]
    return "".join(out)


def regra_para(titulo, at):
    for prefixo, regra in at.REGRAS:
        if titulo.startswith(prefixo):
            return regra
    return None


def ler_material(md):
    """Separa cabeçalho (título, subtítulo, ficha) e seções (##) com suas subseções (### / ####)."""
    lista = list(blocos(md.splitlines()))
    titulo, subtitulo, ficha = "", "", []
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
    return titulo, subtitulo, ficha, secoes


def texto_blocos(bs):
    out = []
    for b in bs:
        if b[0] in ("p", "code"):
            out.append(b[1])
        elif b[0] == "quote":
            out += b[1]
        elif b[0] == "table":
            out += b[1]
        elif b[0] in ("ul", "ol"):
            out += [x[2] for x in b[1]]
    return " ".join(out)


def render_secao(s, at, usados):
    """Conteúdo de uma seção do material (o título vai no cabeçalho do módulo)."""
    out, subs = [], []
    regra_sec = regra_para(s["titulo"], at)
    if s["intro"] or regra_sec:
        out.append(render_unidade(s["intro"], regra_sec, at))
    for u in s["unidades"]:
        uid = slug(u["titulo"], usados)
        if u["nivel"] == 3:
            subs.append((uid, puro(u["titulo"])))
        h = "h3" if u["nivel"] == 3 else "h4"
        out.append(f'<div class="m-unidade" id="{uid}"><{h} class="m-{h}">{inline(u["titulo"])}</{h}>')
        out.append(render_unidade(u["blocos"], regra_para(u["titulo"], at), at))
        out.append("</div>")
    pal = palavras(s["titulo"] + " " + texto_blocos(s["intro"]) + " " +
                   " ".join(u["titulo"] + " " + texto_blocos(u["blocos"]) for u in s["unidades"]))
    return "".join(out), subs, pal


# ================================================================ PÁGINA
def gerar(cfg):
    at = cfg["atividades"]
    usados = set()
    meta, html_trad, subs_t, pal_t, n_par = render_traducao(cfg["traducao"].read_text(encoding="utf-8"), at)
    md_mat = cfg["material"].read_text(encoding="utf-8")
    titulo_m, sub_m, ficha, secoes = ler_material(md_mat)

    # ----- módulos: Mapa, Texto de Porter, demais seções do material
    mods = []
    for s in secoes:
        corpo, subs, pal = render_secao(s, at, usados)
        mods.append({"id": "m-" + slug(s["titulo"], usados), "titulo": s["titulo"], "corpo": corpo,
                     "subs": subs, "palavras": pal, "material": True})
    mods.insert(1, {
        "id": "m-texto-de-porter", "titulo": "Texto de Porter", "subs": subs_t, "palavras": pal_t, "material": False,
        "corpo": (f'<p class="t-nota" data-atividade>{inline(meta.get("nota", ""))}</p>'
                  f'<div id="antes-de-ler">{at.bloco("prep")}</div>'
                  '<div class="ferr-ajuda" data-atividade><strong>Leitura ativa:</strong> passe o mouse (ou toque) em um parágrafo para usar '
                  '<span class="kbd">▍ Destacar</span> e <span class="kbd">✎ Anotar</span>. Tudo é salvo com suas respostas.</div>'
                  f'<article class="traducao" data-integro="traducao">{html_trad}</article>')})
    total = len(mods)

    cards, navs, secs = [], [], []
    for k, m in enumerate(mods, 1):
        info = at.info_modulo(m["titulo"])
        minutos = max(1, math.ceil(m["palavras"] / 200))
        ant = mods[k - 2] if k > 1 else None
        prox = mods[k] if k < total else None
        if m["material"]:
            titulo_html = f'<h2 class="mod-titulo">{inline(m["titulo"])}</h2>'
            integro = ' data-integro="material"'
            sub_t = ""
        else:
            titulo_html = f'<h2 class="mod-titulo" data-atividade>{html.escape(meta.get("titulo", "Texto de Porter"))}</h2>'
            integro = ""
            sub_t = f'<p class="mod-sub" data-atividade>{html.escape(meta.get("autor", ""))} · {html.escape(meta.get("fonte", ""))}</p>'
        nav_mod = (
            '<nav class="mod-nav" data-atividade aria-label="Navegação entre módulos">'
            + (f'<a class="mn-ant" href="#{ant["id"]}"><span>← Anterior</span><strong>{html.escape(at.info_modulo(ant["titulo"])["curto"])}</strong></a>' if ant else "<span></span>")
            + '<a class="mn-ind" href="#indice">Índice da aula</a>'
            + (f'<a class="mn-prox" href="#{prox["id"]}"><span>Próximo →</span><strong>{html.escape(at.info_modulo(prox["titulo"])["curto"])}</strong></a>' if prox else "<span></span>")
            + "</nav>")
        secs.append(
            f'<section class="modulo secao m-sec" id="{m["id"]}" data-titulo="{html.escape(info["curto"], quote=True)}" hidden{integro}>'
            f'<header class="mod-cab"><span class="mod-n" data-atividade>{k}</span><div>'
            f'<span class="mod-eyebrow" data-atividade>Módulo {k} de {total} · {html.escape(info["tipo"])} · ~{minutos} min</span>'
            f'{titulo_html}{sub_t}<p class="mod-desc" data-atividade>{html.escape(info["desc"])}</p></div></header>'
            f'{m["corpo"]}{nav_mod}</section>')
        cards.append(
            f'<li><a class="mod-card{" mod-card-texto" if not m["material"] else ""}" href="#{m["id"]}" data-mod="{m["id"]}">'
            f'<span class="mc-topo"><span class="mc-n">{k}</span><span class="mc-tipo">{html.escape(info["tipo"])}</span></span>'
            f'<span class="mc-titulo">{html.escape(info["curto"])}</span>'
            f'<span class="mc-desc">{html.escape(info["desc"])}</span>'
            f'<span class="mc-pe"><span class="mc-min">~{minutos} min</span><span class="mc-prog"></span></span>'
            f'<span class="mc-barra"><i></i></span></a></li>')
        subs_html = "".join(f'<a class="nav-sub" href="#{sid}">{html.escape(r)}</a>' for sid, r in m["subs"])
        navs.append(
            f'<a class="nav-mod" href="#{m["id"]}" data-mod="{m["id"]}"><span class="nm-n">{k}</span>'
            f'<span class="nm-t">{html.escape(info["curto"])}</span><span class="nm-p"></span></a>'
            + (f'<div class="nav-subs" data-subs="{m["id"]}">{subs_html}</div>' if subs_html else ""))

    valores = dict(
        n=cfg["n"],
        titulo_pagina=html.escape(f"Parte I · {puro(titulo_m)}"),
        titulo_m=inline(titulo_m),
        sub_m=inline(sub_m),
        ficha="".join(render_paragrafo(p) for p in ficha),
        nav="\n  ".join(navs),
        cards="\n".join(cards),
        modulos="\n".join(secs),
        total=total,
    )
    pagina = at.MODELO
    for k, v in valores.items():
        pagina = pagina.replace("{{" + k + "}}", str(v))
    resto = re.findall(r"\{\{\w+\}\}", pagina)
    if resto:
        sys.exit(f"Marcadores sem valor no modelo: {resto}")
    cfg["destino"].parent.mkdir(parents=True, exist_ok=True)
    cfg["destino"].write_text(pagina, encoding="utf-8")
    print(f"OK  {cfg['destino'].relative_to(RAIZ)}  ({total} módulos · tradução: {pal_t} palavras, {n_par} parágrafos · material: {palavras(md_mat)} palavras)")


if __name__ == "__main__":
    for cfg in PARTES:
        gerar(cfg)
