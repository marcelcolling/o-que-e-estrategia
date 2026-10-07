"""
Atividades da Parte I (Aula 1), onde cada uma entra no material, os módulos e o modelo da página.

ATENÇÃO: as chaves usadas em data-campo (ex.: "b1_checagem") são gravadas na planilha.
Não renomeie uma chave depois que a turma começar a responder: as respostas salvas
ficariam órfãs. Para tirar uma pergunta, apague a caixa; para acrescentar, use uma chave nova.

Tudo o que é marcado com data-atividade fica fora da conferência de integridade do material.
Campos com data-opcional não entram na contagem de progresso (ex.: anotações do mapa).
"""
import html
import math
import re

E = lambda s: html.escape(s, quote=True)  # noqa: E731


# ---------------------------------------------------------------- componentes
def campo(chave, rotulo, linhas=4, dica="", mostrar_rotulo=True):
    r = f'<span class="ativ-rot">{E(rotulo)}</span>' if mostrar_rotulo else ""
    return (f'<label class="ativ-campo">{r}<textarea data-campo="{chave}" data-rotulo="{E(rotulo)}" rows="{linhas}"'
            f' placeholder="{E(dica)}"></textarea></label>')


def escolha(chave, rotulo, opcoes):
    itens = "".join(
        f'<label class="pilula"><input type="radio" name="{chave}" value="{E(v)}" data-campo="{chave}" data-rotulo="{E(rotulo)}"><span>{E(t)}</span></label>'
        for v, t in opcoes)
    return f'<fieldset class="ativ-escolha"><legend class="ativ-rot">{E(rotulo)}</legend><div class="pilulas">{itens}</div></fieldset>'


def caixa(secao, titulo, enunciado, conteudo, tipo="Atividade", classe=""):
    return (f'<div class="ativ {classe}" data-atividade data-secao="{E(secao)}">'
            f'<div class="ativ-cab"><span class="ativ-ico" aria-hidden="true">✎</span><span class="ativ-tipo">{E(tipo)}</span>'
            f'<span class="ativ-titulo">{E(titulo)}</span></div>'
            + (f'<p class="ativ-enunciado">{enunciado}</p>' if enunciado else "")
            + conteudo + "</div>")


def pausa(chave, pergunta):
    return caixa("Texto de Porter · pausas para responder", "Responda ao texto", E(pergunta),
                 campo(chave, pergunta, 4, "Escreva com suas palavras, sem copiar o texto.", False),
                 tipo="Pausa para responder", classe="ativ-pausa")


ANTES = "Escreva a sua resposta <strong>antes</strong> de abrir o comentário. Depois compare: o que você acertou, o que faltou?"

B = {}

B["prep"] = caixa(
    "Antes de ler", "Uma iniciativa da sua empresa",
    "Responda antes de ler o texto de Porter. Você vai voltar a esta resposta no exit ticket.",
    campo("prep_iniciativa", "Cite uma iniciativa da sua empresa (ou de uma empresa que você conhece bem) dos últimos dois anos", 3,
          "Ex.: implantação de um novo ERP, abertura de um canal digital, programa de redução de custos…")
    + escolha("prep_efeito", "Ela fez a empresa ficar…", [("melhor", "Melhor"), ("diferente", "Mais diferente"),
                                                         ("as duas", "As duas coisas"), ("não sei", "Ainda não sei")])
    + campo("prep_porque", "Por quê?", 3),
    tipo="Antes de ler")

B["abertura_provocacao"] = caixa(
    "Abertura", "Pense na sua empresa", "",
    campo("abertura_projetos", "Quais foram os três últimos grandes projetos da sua empresa?", 3)
    + campo("abertura_provocacao", "Se o principal concorrente fizesse os mesmos três projetos, o que mudaria na posição relativa de vocês?", 4))

B["b1_checagem"] = caixa(
    "Bloco 1 · Definições", "Pergunta de checagem", ANTES,
    escolha("b1_checagem_tipo", "Reduzir pela metade o tempo de desenvolvimento de produtos é…",
            [("EO", "Eficácia operacional"), ("estratégia", "Estratégia"), ("depende", "Depende")])
    + campo("b1_checagem", "Justifique", 3))

for n in range(1, 7):
    B[f"b2_duvida{n}"] = caixa(
        "Bloco 2 · Dúvidas comuns", f"Dúvida {n}: sua resposta",
        "Antes de abrir o comentário, responda com o que você entendeu do texto de Porter.",
        campo(f"b2_duvida{n}", f"Dúvida {n}: minha resposta antes de ler", 3, mostrar_rotulo=False))

B["b2_colunas"] = caixa(
    "Bloco 2 · Dúvidas comuns", "Melhor, diferente ou não sei?",
    "Liste iniciativas reais (uma por linha) e classifique-as. A coluna <em>Não sei</em> costuma ser a mais rica: "
    "ali aparecem iniciativas que são EO, mas se vendem como estratégia.",
    '<div class="colunas3">'
    + campo("b2_col_melhor", "Melhor (EO)", 5, "Uma iniciativa por linha")
    + campo("b2_col_diferente", "Diferente (posição)", 5, "Uma iniciativa por linha")
    + campo("b2_col_naosei", "Não sei", 5, "Uma iniciativa por linha")
    + "</div>"
    + campo("b2_col_teste", "Aplique o teste da renúncia a uma iniciativa da coluna “Não sei”: um concorrente poderia adotá-la sem abrir mão de nada?", 3))

B["b2_convergencia"] = caixa(
    "Bloco 2 · Dúvidas comuns", "A convergência no seu setor", "",
    campo("b2_convergencia", "Quantas empresas do seu setor usam a mesma consultoria, o mesmo ERP, a mesma agência ou o mesmo operador logístico? O que isso faz com as diferenças entre elas?", 4))

B["b2_setor_br"] = caixa(
    "Bloco 2 · Dúvidas comuns", "O retrato japonês no Brasil", "",
    campo("b2_setor_br", "Que setor brasileiro se parece com o retrato das empresas japonesas de 1996? Justifique com atividades concretas, não com impressões.", 4))

B["b3_fronteira"] = caixa(
    "Bloco 3 · Fronteira de produtividade", "Posicione três empresas",
    "Para cada empresa, mova os controles: a posição de custo (da esquerda, custo alto, para a direita, custo baixo) "
    "e o valor entregue além do preço. O gráfico mostra se ela fica abaixo da fronteira ou sobre ela.",
    campo("b3_setor", "Setor escolhido", 1, "Ex.: companhias aéreas, bancos, academias, supermercados")
    + '<div class="fronteira-widget" data-widget="fronteira"></div>'
    + campo("b3_inovacao", "Uma inovação recente que empurrou a fronteira desse setor", 2)
    + campo("b3_ganhou", "Alguma dessas empresas ganhou posição com essa inovação, ou todas apenas acompanharam?", 3))

B["b4_debate"] = caixa(
    "Bloco 4 · EO como vantagem temporária", "Pergunta para debate", ANTES,
    '<div class="colunas2">'
    + campo("b4_vantagem", "Isso é vantagem competitiva?", 3)
    + campo("b4_tempo", "Por quanto tempo?", 3)
    + campo("b4_quem", "Quem vai capturar o ganho daqui a três anos?", 3)
    + campo("b4_durar", "O que faria essa vantagem durar mais?", 3)
    + "</div>")

B["b5_fixacao"] = caixa(
    "Bloco 5 · Trade-offs", "Pergunta de fixação", ANTES,
    campo("b5_fixacao", "O que isso indica sobre a posição da empresa em relação à fronteira? O que deve acontecer se ela tentar repetir o feito várias vezes?", 4))

B["b6_executar"] = caixa(
    "Bloco 6 · Execução estratégica", "Executar bem ou executar a estratégia?", "",
    campo("b6_executar", "Execução estratégica é executar bem, ou executar a estratégia? Qual a diferença, na prática da sua empresa?", 4))

B["b6_portfolio"] = caixa(
    "Bloco 6 · Execução estratégica", "Diagnóstico do seu portfólio de iniciativas",
    "Liste as iniciativas em curso na sua empresa (ou numa empresa que você conhece) e classifique cada uma. A barra mostra a proporção.",
    '<div class="portfolio-widget" data-widget="portfolio"></div>'
    + campo("b6_portfolio_leitura", "O que essa proporção diz sobre a agenda da empresa?", 3))

B["b6_logo"] = caixa(
    "Bloco 6 · Execução estratégica", "Teste da troca de logo",
    "Escreva um objetivo do mapa estratégico ou dos OKRs da sua empresa em cada perspectiva. Depois imagine o nome do principal "
    "concorrente no lugar do seu e marque se o objetivo continua fazendo sentido para ele.",
    '<div class="logo-widget" data-widget="logo"></div>'
    + campo("b6_logo_conclusao", "Olhando o conjunto: o seu painel sobrevive à troca? O que isso revela?", 3))

B["b6_filtro"] = caixa(
    "Bloco 6 · Execução estratégica", "Filtre uma prática de mercado", "Escolha uma prática que sua empresa adotou ou pensa em adotar e passe pelas três perguntas.",
    campo("b6_filtro_pratica", "Prática", 1)
    + campo("b6_filtro_1", "1. Ela nos deixa em dia com a fronteira ou nos diferencia?", 2)
    + campo("b6_filtro_2", "2. Se todos adotarem, quem fica com o ganho: nós, o cliente ou o fornecedor?", 2)
    + campo("b6_filtro_3", "3. Adotá-la nos torna mais parecidos com quem? Isso é desejado?", 2))

B["b6_excelencia"] = caixa(
    "Bloco 6 · Execução estratégica", "Excelência operacional: posição ou EO?", "",
    campo("b6_excelencia", "Se o BSC da sua empresa tem como proposta de valor “excelência operacional”, como saber se isso é uma posição ou apenas EO?", 4))

B["b7_ansoff"] = caixa(
    "Bloco 7 · Caso Vivelar", "A decisão da diretoria já é estratégia?", ANTES,
    escolha("b7_ansoff_tipo", "Minha resposta", [("sim", "Sim"), ("não", "Não"), ("em parte", "Em parte")])
    + campo("b7_ansoff", "Por quê?", 3))

B["b7_palpite"] = caixa(
    "Bloco 7 · Caso Vivelar", "Seu palpite antes dos números",
    "Antes de ler os resultados (7.6), aposte. Depois compare com o que a simulação mostra.",
    '<div class="colunas2">'
    + escolha("b7_palpite18", "Maior EBITDA acumulado em 18 meses", [("0", "Inércia"), ("A", "A · EO pura"), ("B", "B · EO + posição")])
    + escolha("b7_palpite36", "Maior EBITDA acumulado em 36 meses", [("0", "Inércia"), ("A", "A · EO pura"), ("B", "B · EO + posição")])
    + "</div>"
    + campo("b7_palpite_porque", "Por que você acha isso?", 2))

B["b7_renuncia"] = caixa(
    "Bloco 7 · Caso Vivelar", "O indicador da renúncia", "",
    campo("b7_renuncia", "Que indicador você colocaria no BSC B para medir a disciplina da renúncia? Qual seria a meta?", 3))

B["simulador"] = (
    '<div class="ativ ativ-simulador" data-atividade data-secao="Bloco 7 · Simulador Vivelar" id="simulador">'
    '<div class="ativ-cab"><span class="ativ-ico" aria-hidden="true">▦</span><span class="ativ-tipo">Laboratório</span>'
    '<span class="ativ-titulo">Simulador da Vivelar</span></div>'
    '<p class="ativ-enunciado">O simulador refaz, mês a mês, as contas do caso com o modelo descrito em "Para consulta". Com as premissas '
    'do material, ele reproduz as tabelas 7.6 a 7.8. Mude <strong>uma premissa por vez</strong>, observe o que muda na conclusão e '
    'registre cada experimento.</p>'
    '<div class="sim-widget" data-widget="simulador"></div></div>')

B["b7_licao"] = caixa(
    "Bloco 7 · Caso Vivelar", "Qual lição mexeu com você?", "",
    campo("b7_licao", "Qual das sete lições contraria o que você pensava antes do caso? Por quê?", 3))

B["b7_perguntas"] = caixa(
    "Bloco 7 · Caso Vivelar", "Perguntas sobre o caso", "",
    campo("b7_q1", "1. Quais premissas de B você considera mais frágeis? Como testá-las antes de investir?", 3)
    + campo("b7_q2", "2. O líder conseguiria replicar o modelo nos independentes? O que ele teria de abandonar para isso?", 3)
    + campo("b7_q3", "3. Se você fosse o conselho, com que horizonte e com quais indicadores avaliaria B? O que diria ao CFO no mês 18?", 3)
    + campo("b7_q4", "4. Onde está a EO no Cenário B? Seria possível fazer B sem fazer A?", 3)
    + campo("b7_q5", "5. Reescreva um objetivo do BSC A para que ele deixe de sobreviver à troca de logo (só faça sentido para a Vivelar)", 3)
    + campo("b7_q6", "6. Farmácias independentes costumam comprar via distribuidores. Se a Vivelar precisar negociar com eles, o que muda no Cenário B? Isso reforça ou enfraquece a posição?", 3))

SINTESE = [
    "Vantagem é uma diferença que se consegue preservar, no preço, no custo ou nos dois.",
    "As atividades são a unidade básica da vantagem.",
    "EO aproxima a empresa da fronteira; o posicionamento escolhe onde ficar nela.",
    "EO é necessária, mas raramente suficiente.",
    "Competir só em EO gera convergência.",
    "Longe da fronteira, os trade-offs costumam ser falsos; na fronteira, são reais.",
]
B["sintese"] = caixa(
    "Fechamento", "Consigo explicar com minhas palavras?",
    "Marque as ideias que você seria capaz de explicar a um colega sem consultar o texto. As que ficarem sem marca indicam o que reler.",
    '<div class="checks">' + "".join(
        f'<label class="check"><input type="checkbox" data-campo="sintese_{k}" data-rotulo="{E(t)}"><span>{k}. {E(t)}</span></label>'
        for k, t in enumerate(SINTESE, 1)) + "</div>")

B["exit"] = caixa(
    "Fechamento · Exit ticket", "Exit ticket",
    'Retome a iniciativa que você citou no início <button type="button" class="b-trazer" data-trazer="prep_iniciativa:exit_iniciativa">Usar a iniciativa do início</button>',
    campo("exit_iniciativa", "Iniciativa em curso", 2)
    + escolha("exit_classe", "Classificação", [("a", "(a) EO de paridade"), ("b", "(b) EO de liderança temporária"), ("c", "(c) Reforço de posição")])
    + campo("exit_justificativa", "Justificativa (em até três linhas)", 3)
    + campo("exit_quem", "Quem tende a capturar o ganho dela daqui a dois anos?", 2)
    + '<div class="exit-compara" data-atividade aria-live="polite"></div>'
    + campo("exit_mudou", "O que mudou na sua leitura entre o início da aula e agora?", 3))

B["mapa_volta"] = ('<p class="ativ-ref ativ-ref-mapa" data-atividade>↺ Para terminar, volte ao '
                   '<a href="#m-mapa-de-aprendizagem">Mapa de aprendizagem</a> e atualize como você está em cada objetivo.</p>')


def bloco(chave):
    return B[chave]


# ---------------------------------------------------------------- Mapa de aprendizagem
NIVEIS = [("domino", "Domino"), ("parcial", "Domino parcialmente"), ("nao", "Ainda não domino")]


def mapa(itens, inline):
    """Lista de objetivos do material virando o Mapa: cada objetivo com três níveis e uma anotação opcional."""
    linhas = []
    for k, (_, num, txt) in enumerate(itens, 1):
        rot = f"Objetivo {k}: {re.sub(r'[*]+', '', txt)}"
        radios = "".join(
            f'<label class="pilula pilula-{v}"><input type="radio" name="mapa_{k}" value="{v}" data-campo="mapa_{k}" data-rotulo="{E(rot)}"><span>{E(t)}</span></label>'
            for v, t in NIVEIS)
        linhas.append(
            f'<li class="mapa-item"><div class="mapa-obj"><span class="n">{num}.</span> {inline(txt)}</div>'
            f'<div class="mapa-resp" data-atividade><div class="pilulas" role="group" aria-label="Como você está no objetivo {k}">{radios}</div>'
            f'<button type="button" class="b-mapa-nota" aria-expanded="false">✎ Anotar</button>'
            f'<label class="mapa-nota" hidden><span>Anotação sobre o objetivo {k}</span>'
            f'<textarea data-campo="mapa_{k}_nota" data-opcional data-rotulo="Objetivo {k}: anotação" rows="2" '
            f'placeholder="O que ainda não está claro? O que você quer rever?"></textarea></label></div></li>')
    return ('<div class="mapa" data-secao="Mapa de aprendizagem">'
            '<div class="mapa-resumo" data-atividade aria-live="polite"></div>'
            f'<ol class="mapa-lista">{"".join(linhas)}</ol></div>')


# ---------------------------------------------------------------- esquema visual (3.2)
def _bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    u = 1 - t
    return (u**3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t**3 * x3,
            u**3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t**3 * y3)


def visual(nome):
    if nome != "fronteira":
        return ""
    F = [(110, 78), (380, 70), (520, 118), (556, 336)]       # fronteira atual
    N = [(110, 44), (420, 34), (572, 92), (604, 336)]        # fronteira deslocada
    d = lambda p: f"M{p[0][0]} {p[0][1]} C {p[1][0]} {p[1][1]}, {p[2][0]} {p[2][1]}, {p[3][0]} {p[3][1]}"  # noqa: E731
    A, Bp = (190, 262), (320, 292)
    C, D = _bez(F, 0.14), _bez(F, 0.66)
    alvo = _bez(F, 0.30)
    vx, vy = alvo[0] - A[0], alvo[1] - A[1]
    L = math.hypot(vx, vy)
    fim = (A[0] + vx * (L - 16) / L, A[1] + vy * (L - 16) / L)
    ini = (A[0] + vx * 14 / L, A[1] + vy * 14 / L)
    s1, s2 = _bez(F, 0.86), _bez(N, 0.86)
    arco_ini, arco_fim = (C[0] + 4, C[1] - 22), (D[0] - 14, D[1] - 18)
    ctrl = ((arco_ini[0] + arco_fim[0]) / 2 + 40, min(arco_ini[1], arco_fim[1]) - 40)
    f = lambda v: f"{v:.0f}"  # noqa: E731
    return f"""<figure class="esquema" data-atividade>
<svg viewBox="0 0 680 420" role="img" aria-label="Esquema da fronteira de produtividade: as empresas A e B estão abaixo da curva; a seta de A até a curva é melhoria de eficácia operacional; C e D estão sobre a curva em pontos diferentes, o que é posicionamento; uma curva tracejada mais acima mostra a fronteira depois de uma nova tecnologia.">
  <defs>
    <marker id="seta-eo" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#c4521f"/></marker>
    <marker id="seta-pos" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#2a78d6"/></marker>
    <marker id="seta-des" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#5E6878"/></marker>
  </defs>
  <rect x="80" y="24" width="540" height="312" rx="8" fill="#F6F5F0"/>
  <path d="{d(F)} L 110 336 Z" fill="rgba(235,104,52,0.08)"/>
  <text x="120" y="324" class="esq-zona">Abaixo da fronteira: espaço para EO</text>
  <path d="{d(N)}" fill="none" stroke="#5E6878" stroke-width="2" stroke-dasharray="6 6"/>
  <text x="612" y="58" text-anchor="end" class="esq-rot esq-cinza">nova fronteira</text>
  <path d="{d(F)}" fill="none" stroke="#1F3A5F" stroke-width="4" stroke-linecap="round"/>
  <text x="532" y="304" text-anchor="end" class="esq-rot">fronteira de produtividade</text>
  <line x1="{f(s1[0] + 4)}" y1="{f(s1[1] - 2)}" x2="{f(s2[0] - 5)}" y2="{f(s2[1] + 1)}" stroke="#5E6878" stroke-width="2" marker-end="url(#seta-des)"/>
  <line x1="{f(ini[0])}" y1="{f(ini[1])}" x2="{f(fim[0])}" y2="{f(fim[1])}" stroke="#c4521f" stroke-width="3" marker-end="url(#seta-eo)"/>
  <text x="{f((A[0] + alvo[0]) / 2 + 12)}" y="{f((A[1] + alvo[1]) / 2 + 8)}" class="esq-rot esq-laranja">EO: aproximar-se da fronteira</text>
  <path d="M{f(arco_ini[0])} {f(arco_ini[1])} Q {f(ctrl[0])} {f(ctrl[1])} {f(arco_fim[0])} {f(arco_fim[1])}" fill="none" stroke="#2a78d6" stroke-width="2.5" marker-start="url(#seta-pos)" marker-end="url(#seta-pos)"/>
  <text x="{f(ctrl[0] - 10)}" y="{f(ctrl[1] + 6)}" class="esq-rot esq-azul" text-anchor="middle">posicionamento: escolher onde ficar</text>
  <circle cx="{A[0]}" cy="{A[1]}" r="13" fill="#eb6834"/><text x="{A[0]}" y="{A[1] + 5}" class="esq-pt">A</text>
  <circle cx="{Bp[0]}" cy="{Bp[1]}" r="13" fill="#eb6834"/><text x="{Bp[0]}" y="{Bp[1] + 5}" class="esq-pt">B</text>
  <circle cx="{f(C[0])}" cy="{f(C[1])}" r="13" fill="#2a78d6"/><text x="{f(C[0])}" y="{f(C[1] + 5)}" class="esq-pt">C</text>
  <circle cx="{f(D[0])}" cy="{f(D[1])}" r="13" fill="#2a78d6"/><text x="{f(D[0])}" y="{f(D[1] + 5)}" class="esq-pt">D</text>
  <text x="84" y="356" class="esq-ax">custo alto</text>
  <text x="616" y="356" text-anchor="end" class="esq-ax">custo baixo</text>
  <text x="350" y="394" text-anchor="middle" class="esq-eixo">Posição relativa de custo</text>
  <text x="66" y="40" text-anchor="end" class="esq-ax">alto</text>
  <text x="66" y="334" text-anchor="end" class="esq-ax">baixo</text>
  <text x="26" y="180" text-anchor="middle" class="esq-eixo" transform="rotate(-90 26 180)">Valor entregue além do preço</text>
</svg>
<figcaption class="esq-legenda"><span><i class="lg-eo"></i>Empresas abaixo da fronteira e a melhoria de EO</span><span><i class="lg-pos"></i>Empresas na fronteira, em posições diferentes</span><span><i class="lg-des"></i>A fronteira depois de uma nova tecnologia</span></figcaption>
</figure>"""


# ---------------------------------------------------------------- módulos
# (prefixo do título no material, tipo, título curto, descrição)
MODULOS = [
    ("Mapa de aprendizagem", "Diagnóstico", "Mapa de aprendizagem", "Marque o que você já domina e volte aqui no fim da aula."),
    ("Texto de Porter", "Leitura", "Texto de Porter (Parte I)", "Tradução da Parte I, com destaques, anotações e pausas para responder."),
    ("Abertura", "Abertura", "O que Porter contesta", "As “novas regras” dos anos 1990 e a tese central da Parte I."),
    ("Bloco 1", "Bloco 1", "Definições", "Diferença preservável, atividades e as duas definições."),
    ("Bloco 2", "Bloco 2", "Dúvidas comuns", "Seis dúvidas frequentes: responda antes de ler o comentário."),
    ("Bloco 3", "Bloco 3", "A fronteira de produtividade", "O conceito central da Parte I, em um esquema e em um exercício."),
    ("Bloco 4", "Bloco 4", "EO como vantagem temporária", "Por que a vantagem baseada em EO se dissipa, com o caso da IA."),
    ("Bloco 5", "Bloco 5", "Trade-offs falsos e reais", "Quando o trade-off é ilusão e quando é escolha."),
    ("Bloco 6", "Bloco 6", "Da distinção à execução", "Duas agendas e quatro práticas para aplicar na sua empresa."),
    ("Bloco 7", "Bloco 7", "Caso Vivelar", "BSC, números e simulador: EO pura contra EO com posição."),
    ("Fechamento", "Fechamento", "Síntese e exit ticket", "Seis ideias, exit ticket e revisão do mapa."),
    ("Para consulta", "Consulta", "Para consulta", "Como a simulação funciona, armadilhas comuns e referências."),
]


def info_modulo(titulo):
    for prefixo, tipo, curto, desc in MODULOS:
        if titulo.startswith(prefixo):
            return {"tipo": tipo, "curto": curto, "desc": desc}
    return {"tipo": "Módulo", "curto": titulo, "desc": ""}


# ---------------------------------------------------------------- onde cada atividade entra
# (prefixo do título da seção/subseção, regra). Regras:
#   apos_titulo: caixas logo depois do título | fim: caixas no fim da subseção
#   antes_revelar: caixas antes do comentário (que fica recolhido)
#   recolher: recolhe todo o conteúdo da subseção (as Dúvidas do Bloco 2)
#   apos_bloco: [(trecho do parágrafo, [caixas])] | mapa: a lista numerada vira o Mapa de aprendizagem
REGRAS = [
    ("Mapa de aprendizagem", {"mapa": True}),
    ("Uma provocação para começar", {"fim": ["abertura_provocacao"]}),
    ("Pergunta de checagem", {"antes_revelar": ["b1_checagem"]}),
    ("Dúvida 1:", {"apos_titulo": ["b2_duvida1"], "recolher": True, "fim": ["b2_colunas"]}),
    ("Dúvida 2:", {"apos_titulo": ["b2_duvida2"], "recolher": True}),
    ("Dúvida 3:", {"apos_titulo": ["b2_duvida3"], "recolher": True, "fim": ["b2_convergencia"]}),
    ("Dúvida 4:", {"apos_titulo": ["b2_duvida4"], "recolher": True}),
    ("Dúvida 5:", {"apos_titulo": ["b2_duvida5"], "recolher": True}),
    ("Dúvida 6:", {"apos_titulo": ["b2_duvida6"], "recolher": True, "fim": ["b2_setor_br"]}),
    ("3.5 Exercício", {"fim": ["b3_fronteira"]}),
    ("4.5 Pergunta para debate", {"antes_revelar": ["b4_debate"]}),
    ("5.4 Pergunta de fixação", {"antes_revelar": ["b5_fixacao"]}),
    ("6.1 Executar bem", {"fim": ["b6_executar"]}),
    ("6.3 Quatro práticas", {"apos_bloco": [("Na maioria das empresas, quase todo", ["b6_portfolio"]),
                                            ("Aplique o teste ao **conjunto**", ["b6_logo"]),
                                            ("Adotar continua sendo, muitas vezes", ["b6_filtro"])]}),
    ("6.4 Excelência operacional", {"fim": ["b6_excelencia"]}),
    ("7.2 Ansoff não é Porter", {"antes_revelar": ["b7_ansoff"]}),
    ("7.4 Os três cenários", {"fim": ["b7_palpite"]}),
    ("BSC do Cenário B", {"apos_bloco": [("**Sugestão para debate:**", ["b7_renuncia"])]}),
    ("7.8 Análise de sensibilidade", {"fim": ["simulador"]}),
    ("7.9 O que os números ensinam", {"fim": ["b7_licao"]}),
    ("7.10 Perguntas sobre o caso", {"fim": ["b7_perguntas"]}),
    ("Síntese em seis ideias", {"fim": ["sintese"]}),
    ("Exit ticket", {"fim": ["exit", "mapa_volta"]}),
]


MODELO = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{titulo_pagina}} — O que é estratégia?</title>
<!-- Página gerada por ferramentas/gerar_parte.py. Não edite à mão: edite as fontes e rode o gerador. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,400;1,9..144,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/portal.css">
<link rel="stylesheet" href="../assets/css/leitura.css">
<link rel="stylesheet" href="../assets/css/parte.css">
</head>
<body data-chave="parte-{{n}}" class="pagina-parte">

<div id="progress-bar"></div>
<button id="sidebar-toggle" aria-label="Abrir sumário"><span></span><span></span><span></span></button>
<div id="overlay"></div>

<nav id="sidebar" aria-label="Módulos da aula">
  <div class="sidebar-badge"><span class="dot"></span><span>Aula {{n}} · Parte I</span></div>
  <div class="sidebar-title">Eficácia operacional não é estratégia</div>
  <div class="sidebar-progresso" aria-live="polite"><span class="sp-txt">0 respostas</span><span class="sp-barra"><i></i></span></div>
  <a class="nav-item nav-voltar" href="../index.html">← Voltar ao portal</a>
  <a class="nav-indice" href="#indice">☰ Índice da aula</a>
  {{nav}}
</nav>

<main class="wrapper">

  <section class="indice" id="indice">
    <div class="hero" id="intro" data-integro="material-cab">
      <div class="hero-tag" data-atividade><span class="dot"></span>Aula {{n}} · Parte I do artigo · pp. 37–40</div>
      <h1>{{titulo_m}}</h1>
      <p class="hero-sub">{{sub_m}}</p>
    </div>
    <div class="ficha" data-integro="material">{{ficha}}</div>
    <div class="ind-topo" data-atividade>
      <div><span class="bloco-eyebrow">Índice da aula</span><h2>{{total}} módulos, um de cada vez</h2>
      <p>Abra um módulo para estudar. Ao terminar, siga para o próximo pelo botão no fim da página.</p></div>
      <div class="ind-geral"><strong class="ig-num">0</strong><span class="ig-txt">de 0 respostas</span><span class="sp-barra"><i></i></span></div>
    </div>
    <ol class="mod-cards" data-atividade>
{{cards}}
    </ol>
    <div class="barra-acoes" data-atividade>
      <a class="vd-btn vd-btn-amarelo btn-continuar" href="#m-mapa-de-aprendizagem">Começar pelo módulo 1</a>
      <button type="button" class="vd-btn vd-btn-roxo btn-salvar" data-vd-salvar hidden>Salvar respostas</button>
      <button type="button" class="vd-btn vd-btn-ghost" onclick="window.print()">Imprimir / salvar em PDF</button>
      <a class="vd-btn vd-btn-ghost" href="../index.html">Voltar ao portal</a>
    </div>
    <div class="vd-print-id"></div>
  </section>

{{modulos}}

</main>

<button id="back-to-top" title="Voltar ao topo" aria-label="Voltar ao topo">&#8593;</button>
<script src="../assets/js/config.js"></script>
<script src="../assets/js/portal.js"></script>
<script src="../assets/js/vivelar.js"></script>
<script src="../assets/js/parte.js"></script>
<script>PARTE.iniciar({ id: 'aula{{n}}', titulo: 'Aula {{n}} · Parte I: Eficácia operacional não é estratégia', crumb: 'Aula {{n}} · Parte I' });</script>
</body>
</html>
"""
