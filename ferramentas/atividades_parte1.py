"""
Atividades da Parte I (Aula 1) e onde cada uma entra no material.

ATENÇÃO: as chaves usadas em data-campo (ex.: "b1_checagem") são gravadas na planilha.
Não renomeie uma chave depois que a turma começar a responder: as respostas salvas
ficariam órfãs. Para tirar uma pergunta, apague a caixa; para acrescentar, use uma chave nova.

Tudo o que é marcado com data-atividade fica fora da conferência de integridade do material.
"""
import html

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


ANTES = "Escreva a sua resposta <strong>antes</strong> de abrir a do material. Depois compare: o que você acertou, o que faltou?"

B = {}

B["prep"] = caixa(
    "Antes de ler", "Uma iniciativa da sua empresa",
    "Esta é a pergunta da preparação da aula. Responda antes de ler o texto de Porter; você vai voltar a ela no exit ticket.",
    campo("prep_iniciativa", "Cite uma iniciativa da sua empresa (ou de uma empresa que você conhece bem) dos últimos dois anos", 3,
          "Ex.: implantação de um novo ERP, abertura de um canal digital, programa de redução de custos…")
    + escolha("prep_efeito", "Ela fez a empresa ficar…", [("melhor", "Melhor"), ("diferente", "Mais diferente"),
                                                         ("as duas", "As duas coisas"), ("não sei", "Ainda não sei")])
    + campo("prep_porque", "Por quê?", 3),
    tipo="Preparação")

B["prep_ref"] = ('<p class="ativ-ref" data-atividade>✎ Você respondeu a esta pergunta no início da página, '
                 '<a href="#antes-de-ler">antes de ler o texto de Porter</a>.</p>')

B["abertura_provocacao"] = caixa(
    "Abertura", "Pense na sua empresa", "",
    campo("abertura_projetos", "Quais foram os três últimos grandes projetos da sua empresa?", 3)
    + campo("abertura_provocacao", "Se o principal concorrente fizesse os mesmos três projetos, o que mudaria na posição relativa de vocês?", 4))

B["b1_checagem"] = caixa(
    "Bloco 1 · Definições", "Pergunta de checagem", ANTES,
    escolha("b1_checagem_tipo", "Reduzir pela metade o tempo de desenvolvimento de produtos é…",
            [("EO", "Eficácia operacional"), ("estratégia", "Estratégia"), ("depende", "Depende")])
    + campo("b1_checagem", "Justifique", 3))

for n in range(1, 8):
    B[f"b2_duvida{n}"] = caixa(
        "Bloco 2 · Pontos que geram dúvida", f"Dúvida {n}: sua resposta",
        "Antes de ler a resposta do material, responda à dúvida com o que você entendeu do texto de Porter.",
        campo(f"b2_duvida{n}", f"Dúvida {n}: minha resposta antes de ler", 3, mostrar_rotulo=False))

B["b2_colunas"] = caixa(
    "Bloco 2 · Pontos que geram dúvida", "Melhor, diferente ou não sei?",
    "Liste iniciativas reais (uma por linha) e classifique-as. A coluna <em>Não sei</em> costuma ser a mais rica: "
    "ali aparecem iniciativas que são EO, mas se vendem como estratégia.",
    '<div class="colunas3">'
    + campo("b2_col_melhor", "Melhor (EO)", 5, "Uma iniciativa por linha")
    + campo("b2_col_diferente", "Diferente (posição)", 5, "Uma iniciativa por linha")
    + campo("b2_col_naosei", "Não sei", 5, "Uma iniciativa por linha")
    + "</div>"
    + campo("b2_col_teste", "Aplique o teste da renúncia a uma iniciativa da coluna “Não sei”: um concorrente poderia adotá-la sem abrir mão de nada?", 3))

B["b2_convergencia"] = caixa(
    "Bloco 2 · Pontos que geram dúvida", "A convergência no seu setor", "",
    campo("b2_convergencia", "Quantas empresas do seu setor usam a mesma consultoria, o mesmo ERP, a mesma agência ou o mesmo operador logístico? O que isso faz com as diferenças entre elas?", 4))

B["b2_setor_br"] = caixa(
    "Bloco 2 · Pontos que geram dúvida", "O retrato japonês no Brasil", "",
    campo("b2_setor_br", "Que setor brasileiro se parece com o retrato das empresas japonesas de 1996? Justifique com atividades concretas, não com impressões.", 4))

B["b3_fronteira"] = caixa(
    "Bloco 3 · Fronteira de produtividade", "Exercício rápido: posicione três empresas",
    "Escolha um setor que você conhece. Para cada empresa, mova os controles: a posição de custo (da esquerda, custo alto, "
    "para a direita, custo baixo) e o valor entregue além do preço. O gráfico mostra se ela fica abaixo da fronteira ou sobre ela.",
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
    '<p class="ativ-enunciado">O simulador refaz, mês a mês, as contas do caso com o mesmo modelo do Apêndice A. Com as premissas '
    'do material, ele reproduz as tabelas 7.6 a 7.8. Mude <strong>uma premissa por vez</strong>, observe o que muda na conclusão e '
    'registre cada experimento.</p>'
    '<div class="sim-widget" data-widget="simulador"></div></div>')

B["b7_licao"] = caixa(
    "Bloco 7 · Caso Vivelar", "Qual lição mexeu com você?", "",
    campo("b7_licao", "Qual das sete lições contraria o que você pensava antes do caso? Por quê?", 3))

B["b7_perguntas"] = caixa(
    "Bloco 7 · Caso Vivelar", "Perguntas do caso (responda individualmente)", "",
    campo("b7_q1", "1. Quais premissas de B você considera mais frágeis? Como testá-las antes de investir?", 3)
    + campo("b7_q2", "2. O líder conseguiria replicar o modelo nos independentes? O que ele teria de abandonar para isso?", 3)
    + campo("b7_q3", "3. Se você fosse o conselho, com que horizonte e com quais indicadores avaliaria B? O que diria ao CFO no mês 18?", 3)
    + campo("b7_q4", "4. Onde está a EO no Cenário B? Seria possível fazer B sem fazer A?", 3)
    + campo("b7_q5", "5. Reescreva um objetivo do BSC A para que ele deixe de sobreviver à troca de logo (só faça sentido para a Vivelar)", 3)
    + campo("b7_q6", "6. Se a Vivelar precisar negociar com distribuidores, o que muda no Cenário B? Isso reforça ou enfraquece a posição?", 3))

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
    'Retome a iniciativa que você citou no início <button type="button" class="b-trazer" data-trazer="prep_iniciativa:exit_iniciativa">Usar a iniciativa da preparação</button>',
    campo("exit_iniciativa", "Iniciativa em curso", 2)
    + escolha("exit_classe", "Classificação", [("a", "(a) EO de paridade"), ("b", "(b) EO de liderança temporária"), ("c", "(c) Reforço de posição")])
    + campo("exit_justificativa", "Justificativa (em até três linhas)", 3)
    + campo("exit_quem", "Quem tende a capturar o ganho dela daqui a dois anos?", 2)
    + '<div class="exit-compara" data-atividade aria-live="polite"></div>'
    + campo("exit_mudou", "O que mudou na sua leitura entre a preparação e agora?", 3))

B["fechamento_final"] = ""

# ---------------------------------------------------------------- onde cada atividade entra
# (prefixo do título da seção/subseção, regra). Regras:
#   apos_titulo: caixas logo depois do título | fim: caixas no fim da subseção
#   antes_revelar: caixas antes da resposta esperada (que fica recolhida)
#   recolher: recolhe todo o conteúdo da subseção (as Dúvidas do Bloco 2)
#   apos_bloco: [(trecho do parágrafo, [caixas])]
REGRAS = [
    ("Preparação dos alunos", {"fim": ["prep_ref"]}),
    ("Provocação para abrir a discussão", {"fim": ["abertura_provocacao"]}),
    ("Pergunta de checagem", {"antes_revelar": ["b1_checagem"]}),
    ("Dúvida 1:", {"apos_titulo": ["b2_duvida1"], "recolher": True, "fim": ["b2_colunas"]}),
    ("Dúvida 2:", {"apos_titulo": ["b2_duvida2"], "recolher": True}),
    ("Dúvida 3:", {"apos_titulo": ["b2_duvida3"], "recolher": True, "fim": ["b2_convergencia"]}),
    ("Dúvida 4:", {"apos_titulo": ["b2_duvida4"], "recolher": True}),
    ("Dúvida 5:", {"apos_titulo": ["b2_duvida5"], "recolher": True}),
    ("Dúvida 6:", {"apos_titulo": ["b2_duvida6"], "recolher": True, "fim": ["b2_setor_br"]}),
    ("Dúvida 7:", {"apos_titulo": ["b2_duvida7"], "recolher": True}),
    ("3.5 Exercício rápido", {"fim": ["b3_fronteira"]}),
    ("4.5 Pergunta para debate", {"antes_revelar": ["b4_debate"]}),
    ("5.5 Pergunta de fixação", {"antes_revelar": ["b5_fixacao"]}),
    ("6.1 A provocação central", {"fim": ["b6_executar"]}),
    ("6.3 Quatro práticas", {"apos_bloco": [("Um diagnóstico útil para a turma", ["b6_portfolio"]),
                                            ("Aplique o teste ao **conjunto**", ["b6_logo"]),
                                            ("Adotar continua sendo, muitas vezes", ["b6_filtro"])]}),
    ("6.4 Uma tensão conceitual", {"fim": ["b6_excelencia"]}),
    ("7.2 Um esclarecimento", {"antes_revelar": ["b7_ansoff"]}),
    ("7.4 Os três cenários", {"fim": ["b7_palpite"]}),
    ("BSC do Cenário B", {"apos_bloco": [("**Sugestão para debate:**", ["b7_renuncia"])]}),
    ("7.8 Análise de sensibilidade", {"fim": ["simulador"]}),
    ("7.9 O que os números ensinam", {"fim": ["b7_licao"]}),
    ("7.10 Perguntas para os grupos", {"fim": ["b7_perguntas"]}),
    ("Síntese em seis ideias", {"fim": ["sintese"]}),
    ("Exit ticket", {"fim": ["exit"]}),
]


def bloco(chave):
    return B[chave]


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

<nav id="sidebar" aria-label="Sumário">
  <div class="sidebar-badge"><span class="dot"></span><span>Aula {{n}} · Parte I</span></div>
  <div class="sidebar-title">Eficácia operacional não é estratégia</div>
  <div class="sidebar-progresso" aria-live="polite"><span class="sp-txt">0 respostas</span><span class="sp-barra"><i></i></span></div>
  <a class="nav-item nav-voltar" href="../index.html">← Voltar ao portal</a>
  <a class="nav-item" href="#intro">Início</a>
  {{nav}}
</nav>

<main class="wrapper">

  <section class="hero" id="intro">
    <div class="hero-tag"><span class="dot"></span>Aula {{n}} · Parte I do artigo · pp. 37–40</div>
    <h1>{{titulo_m}}</h1>
    <p class="hero-sub">Porter, <em>What Is Strategy?</em> (1996): por que fazer melhor o que todos fazem não é o mesmo que ter uma estratégia.</p>
    <div class="hero-meta">
      <div class="meta-item"><span class="meta-label">Texto de Porter</span><span class="meta-value">{{n_par}} parágrafos · ~{{min_t}} min</span></div>
      <div class="meta-item"><span class="meta-label">Material da aula</span><span class="meta-value">~{{min_m}} min de leitura</span></div>
      <div class="meta-item"><span class="meta-label">Entrega</span><span class="meta-value">Atividades + exit ticket</span></div>
    </div>
    <ol class="passos" aria-label="Como estudar esta parte">
      <li><a href="#texto"><span class="passo-n">A</span><span><strong>Leia Porter</strong>Tradução da Parte I. Destaque, anote e responda às pausas.</span></a></li>
      <li><a href="#material"><span class="passo-n">B</span><span><strong>Estude o material</strong>Conceitos, dúvidas e exercícios, com as atividades no próprio texto.</span></a></li>
      <li><a href="#simulador"><span class="passo-n">C</span><span><strong>Pratique</strong>Caso Vivelar com simulador, e feche com o exit ticket.</span></a></li>
    </ol>
  </section>

  <section class="bloco-grande" id="texto">
    <header class="bloco-cab">
      <span class="bloco-letra">A</span>
      <div><span class="bloco-eyebrow">Leitura · texto de Porter</span><h2 class="bloco-titulo">{{t_titulo}}</h2>
      <p class="bloco-sub">{{t_autor}} · {{t_fonte}}</p></div>
    </header>
    <p class="t-nota">{{t_nota}}</p>
    <div id="antes-de-ler">{{pre}}</div>
    <div class="ferr-ajuda" data-atividade><strong>Leitura ativa:</strong> passe o mouse (ou toque) em um parágrafo para usar <span class="kbd">▍ Destacar</span> e <span class="kbd">✎ Anotar</span>. Tudo é salvo com suas respostas.</div>
    <article class="traducao" data-integro="traducao">
{{traducao}}
    </article>
  </section>

  <section class="bloco-grande" id="material">
    <header class="bloco-cab bloco-cab-b" data-integro="material-cab">
      <span class="bloco-letra" data-atividade>B</span>
      <div><span class="bloco-eyebrow" data-atividade>Material da aula</span><h2 class="bloco-titulo">{{titulo_m}}</h2>
      <p class="bloco-sub">{{sub_m}}</p></div>
    </header>
    <div class="material" data-integro="material">
      <div class="ficha">{{ficha}}</div>
{{material}}
    </div>
  </section>

  <section class="bloco-grande" id="minhas-respostas" data-atividade>
    <header class="bloco-cab bloco-cab-c">
      <span class="bloco-letra">✓</span>
      <div><span class="bloco-eyebrow">Fechamento</span><h2 class="bloco-titulo">Minhas respostas</h2>
      <p class="bloco-sub">Confira o que falta antes de encerrar a aula.</p></div>
    </header>
    <div class="resumo-respostas" aria-live="polite"></div>
    <div class="barra-acoes">
      <button type="button" class="vd-btn vd-btn-roxo btn-salvar" data-vd-salvar hidden>Salvar respostas</button>
      <button type="button" class="vd-btn vd-btn-ghost" onclick="window.print()">Imprimir / salvar em PDF</button>
      <a class="vd-btn vd-btn-ghost" href="../index.html">Voltar ao portal</a>
    </div>
    <div class="vd-print-id"></div>
  </section>

</main>

<button id="back-to-top" title="Voltar ao topo" aria-label="Voltar ao topo">&#8593;</button>
<script src="../assets/js/config.js"></script>
<script src="../assets/js/portal.js"></script>
<script src="../assets/js/leitura.js"></script>
<script src="../assets/js/vivelar.js"></script>
<script src="../assets/js/parte.js"></script>
<script>PARTE.iniciar({ id: 'aula{{n}}', titulo: 'Aula {{n}} · Parte I: Eficácia operacional não é estratégia', crumb: 'Aula {{n}} · Parte I' });</script>
</body>
</html>
"""
