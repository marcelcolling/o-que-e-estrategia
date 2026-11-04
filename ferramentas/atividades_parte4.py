"""
Atividades da Parte IV (Aula 4), onde cada uma entra no material, os módulos e o modelo da página.
Os componentes (campo, escolha, caixa, pausa, mapa) e o modelo da página vêm de atividades_parte1;
o espelho vem de atividades_parte2 e sub() de atividades_parte3. Os mapas de sistemas de atividades vêm de
mapas_atividades.py; o widget "sistema" (o mapa do estudante) está em assets/js/parte.js e o desenho em assets/js/mapas.js.

ATENÇÃO: as chaves usadas em data-campo são gravadas na planilha, na atividade "aula4".
Não renomeie uma chave depois que a turma começar a responder: as respostas salvas
ficariam órfãs. Para tirar uma pergunta, apague a caixa; para acrescentar, use uma chave nova.
"""
import atividades_parte1 as P1
from atividades_parte1 import E, campo, escolha, caixa, pausa, mapa  # noqa: F401  (pausa e mapa são usados pelo gerador)
from atividades_parte2 import espelho
from atividades_parte3 import sub
import mapas_atividades as MA

ANTES = "Escreva a sua resposta <strong>antes</strong> de abrir o comentário. Depois compare: o que você acertou, o que faltou?"
ORDENS = [("1", "1ª ordem"), ("2", "2ª ordem"), ("3", "3ª ordem")]
TIPOS_FIT = [("C", "C: consistência"), ("R", "R: reforço"), ("O", "O: otimização")]

NOTA_MAPA = ('<p class="msa-nota" data-atividade>Mapa redesenhado a partir do original, com os rótulos traduzidos. Os temas (cinza-escuro no original) '
             'aparecem em azul-escuro; as atividades (cinza-claro), em branco. A posição dos nós foi refeita para evitar cruzamentos, mas as ligações '
             'são as de Porter. As cores das renúncias, das pessoas e do cliente são uma leitura nossa, para destacar as lições do Bloco 4.</p>')

B = {}

B["prep"] = caixa(
    "Antes de ler", "As atividades de uma empresa que você conhece",
    "Responda antes de ler o texto de Porter. Use a empresa que você vem acompanhando desde a Aula 1. "
    "Não se preocupe ainda com as ligações entre as atividades: a lista é a matéria-prima do mapa que você vai construir no Bloco 5.",
    campo("prep_empresa", "Empresa e principal concorrente", 1, "Ex.: Vivelar × líder do setor")
    + campo("prep_lista", "Liste de 10 a 15 atividades que ela executa de forma diferente do principal concorrente, incluindo as renúncias da Aula 3 (uma por linha)", 10,
            "Ex.: visita semanal a cada loja\nNão faz promoção de preço\nPedido mínimo baixo"),
    tipo="Antes de ler")

B["abertura"] = caixa(
    "Abertura", "A sua resposta", "Responda antes de abrir o comentário: não existe resposta única, e a sua volta à discussão no Bloco 6.",
    campo("abertura_resposta", "Qual é a competência essencial da Southwest? E qual seria a da empresa que você acompanha?", 3))

B["b1_resultado"] = caixa(
    "Bloco 1 · Atividades combinadas", "O “giro de 15 minutos” da sua empresa",
    "Repita o raciocínio da Southwest com um resultado de que a sua empresa se orgulha.",
    campo("b1_resultado", "Qual é o resultado? (Ex.: entrega em 24 horas, baixa rotatividade, atendimento sem fila)", 2)
    + campo("b1_depende", "De que outras atividades ele depende? Um concorrente conseguiria copiá-lo sem copiar essas atividades?", 4))

B["b1_generico"] = caixa(
    "Bloco 1 · Atividades combinadas", "Genérico ou específico?", "",
    campo("b1_combinacao", "Descreva uma combinação de atividades da sua empresa que funciona bem", 2)
    + escolha("b1_comb_tipo", "Esse fit é…", [("generico", "Genérico: funcionaria em muitas empresas"), ("especifico", "Específico: só faz sentido nessa posição"), ("naosei", "Ainda não sei")]))

CASOS_FIT = [
    (1, "A Vanguard vincula os bônus dos funcionários à economia de custos"),
    (2, "O hóspede experimenta a Neutrogena no hotel e depois a compra na farmácia"),
    (3, "A Gap repõe quase diariamente e, por isso, precisa de menos estoque nas lojas"),
    (4, "A Bic projeta as canetas para facilitar a fabricação"),
    (5, "Na Bic, ponto de venda, propaganda e trocas de embalagem juntos geram mais compra por impulso"),
    (6, "O projeto do produto elimina a necessidade de assistência pós-venda"),
]
B["b2_classifica"] = caixa(
    "Bloco 2 · Os três tipos de fit", "Que tipo de fit é este?", ANTES,
    "".join(escolha(f"b2_c{k}", f"Caso {k}: {t}", ORDENS) for k, t in CASOS_FIT))

B["b2_sua"] = caixa(
    "Bloco 2 · Os três tipos de fit", "Um exemplo de cada tipo na sua empresa", "Se não encontrar um dos tipos, escreva isso: a ausência também é um diagnóstico.",
    campo("b2_sua1", "1ª ordem: uma atividade coerente com a posição", 2)
    + campo("b2_sua2", "2ª ordem: uma atividade que fica melhor ou mais barata por causa de outra", 2)
    + campo("b2_sua3", "3ª ordem: algo que a empresa elimina, ou faz com menos esforço, por causa de outra atividade", 2))

B["b3_copia"] = caixa(
    "Bloco 3 · Fit e sustentabilidade", "O que o concorrente conseguiria copiar?", "",
    campo("b3_copia", "Na empresa que você acompanha, qual atividade é a mais fácil de copiar? O que o concorrente ainda não teria depois de copiá-la?", 3))

B["b3_toys"] = caixa(
    "Bloco 3 · Fit e sustentabilidade", "Para debater", "",
    campo("b3_toys", "O que acontece com um sistema de atividades muito integrado quando a estrutura do setor muda? O caso Toys R Us invalida o argumento de Porter?", 3))

B["b3_definicao"] = caixa(
    "Bloco 3 · A definição final", "A sua definição", "",
    campo("b3_definicao", "Escreva, em uma frase, uma definição de estratégia que integre as quatro camadas", 3))

B["b4_leitura"] = caixa(
    "Bloco 4 · Ler um mapa", "Acompanhe as ligações da rotação", ANTES,
    campo("b4_ligacoes", "Siga todas as ligações do nó e escreva uma frase para cada uma: “a rotação é possível porque…” ou “a rotação permite que…”", 5)
    + campo("b4_renuncias", "Quais dessas ligações levam, diretamente ou por um tema, às renúncias da Aula 3?", 2)
    + campo("b4_refeicoes", "Se a Southwest passasse a servir refeições, que ligações seriam afetadas? Clique no nó “Sem refeições” e siga o caminho.", 3))

B["b5_t4"] = caixa(
    "Bloco 5 · O diagnóstico da Vivelar", "Reforce o tema mais frágil", "",
    campo("b5_t4", "Que atividade reforçaria o tema T4 (custo de servir)? Com que outra atividade ela se ligaria, e com que tipo de fit?", 3))

B["b5_construtor"] = caixa(
    "Bloco 5 · O mapa da sua empresa", "Construa o seu sistema de atividades",
    "Preencha na ordem: atividades, temas e ligações. Tudo é salvo com as suas respostas, e o desenho e o diagnóstico se atualizam sozinhos. "
    "Comece pela tabela; o desenho é consequência dela.",
    campo("b5_posicao", "Passo 1: a posição em uma frase (origem e combinação de valor). Ela passa no teste do slogan?", 3)
    + '<div class="sistema-widget" data-widget="sistema"></div>'
    + sub("Passo 6: o que o diagnóstico automático não vê")
    + campo("b5_conflito", "Conflito: há alguma atividade que contradiz um tema ou viola uma renúncia?", 2)
    + campo("b5_perg1", "Pergunta 1 de Porter (consistência): que atividade não serve à posição? Como as outras atividades ajudam ou atrapalham a mais importante?", 2)
    + campo("b5_perg2", "Pergunta 2 de Porter (reforço): que par de atividades poderia se ajudar e hoje não se ajuda?", 2)
    + campo("b5_perg3", "Pergunta 3 de Porter (otimização): que atividade poderia ser eliminada por causa de outra?", 2)
    + sub("Passo 7: o teste da imitação")
    + campo("b5_imitacao", "Para o principal concorrente, o que é copiável com investimento? Que renúncia ele dificilmente faria? Qual é, em ordem de grandeza, a chance de ele igualar o sistema?", 3))

for n in range(1, 6):
    B[f"b6_duvida{n}"] = caixa(
        "Bloco 6 · Dúvidas comuns", f"Dúvida {n}: sua resposta",
        "Antes de abrir o comentário, responda com o que você entendeu da Parte IV.",
        campo(f"b6_duvida{n}", f"Dúvida {n}: minha resposta antes de ler", 3, mostrar_rotulo=False))

B["b7_dono"] = caixa(
    "Bloco 7 · Execução e BSC", "Quem cuida da ligação?", "",
    campo("b7_dono", "Na sua empresa, quem é o responsável por uma ligação entre duas áreas? Por exemplo, entre a visita do vendedor e a entrega da logística.", 3))

FILTRO = [(1, "Roteirização com IA"), (2, "Visita quinzenal"), (3, "Campanha nacional"), (4, "Incentivo só a treinados"), (5, "Pedido pelo aplicativo")]
DECISOES = [("aprovar", "Aprovar"), ("recusar", "Recusar"), ("testar", "Testar ou repensar")]
B["b7_filtro"] = caixa(
    "Bloco 7 · Execução e BSC", "Avalie as iniciativas pelo mapa", ANTES,
    "".join(
        sub(f"Iniciativa {k} · {E(t)}")
        + escolha(f"b7_f{k}", f"Iniciativa {k} ({t}): decisão", DECISOES)
        + campo(f"b7_f{k}_porque", f"Iniciativa {k}: que nós e ligações ela toca?", 2)
        for k, t in FILTRO))

B["b7_aplicar"] = caixa(
    "Bloco 7 · Execução e BSC", "Do mapa para a execução", "",
    campo("b7_meta", "No mapa da sua empresa, qual meta funcional atual pode estar quebrando uma ligação? Qual seria a alternativa alinhada ao sistema?", 3)
    + campo("b7_indicador", "Escolha um objetivo do BSC (ou das metas) da sua empresa e proponha um indicador de elo para ele. Quem seria o dono?", 3)
    + sub("Avalie uma iniciativa real")
    + campo("b7_inic_nome", "Uma iniciativa em discussão na sua empresa", 1)
    + campo("b7_inic_nos", "Que nós e ligações ela toca?", 2)
    + escolha("b7_inic_efeito", "No sistema, ela…", [("cria", "Cria uma ligação"), ("fortalece", "Fortalece"), ("enfraquece", "Enfraquece"), ("quebra", "Quebra")])
    + escolha("b7_inic_renuncia", "Viola alguma renúncia?", [("sim", "Sim"), ("nao", "Não")])
    + campo("b7_inic_decisao", "Qual é a sua decisão, e por quê?", 2)
    + sub("Mudar de posição custa caro")
    + campo("b7_18meses", "Se a diretoria da Vivelar mudasse de posição a cada 18 meses, que atividades do mapa “nunca alcançariam” a estratégia, nas palavras de Porter?", 3))

SINTESE = [
    "EO é excelência em atividades isoladas; estratégia é combinar atividades.",
    "Tudo importa: a vantagem vem do sistema, não de uma competência ou de um fator crítico.",
    "Há três tipos de fit: consistência, reforço e otimização do esforço.",
    "O fit mais valioso é específico da estratégia.",
    "Sistemas protegem mais que atividades isoladas.",
    "O fit exige organização, incentivos e horizonte específicos da estratégia.",
    "Estratégia é criar fit entre as atividades da empresa.",
]
B["sintese"] = caixa(
    "Fechamento", "Consigo explicar com minhas palavras?",
    "Marque as ideias que você seria capaz de explicar a um colega sem consultar o texto. As que ficarem sem marca indicam o que reler.",
    '<div class="checks">' + "".join(
        f'<label class="check"><input type="checkbox" data-campo="sintese_{k}" data-rotulo="{E(t)}"><span>{k}. {E(t)}</span></label>'
        for k, t in enumerate(SINTESE, 1)) + "</div>")

B["exit"] = caixa(
    "Fechamento · Exit ticket", "Exit ticket", "Escolha a ligação no mapa que você construiu no Bloco 5.",
    campo("exit_ligacao", "A ligação mais difícil de copiar (de qual atividade para qual)", 2)
    + campo("exit_frase", "A frase que a justifica", 2)
    + escolha("exit_tipo", "Tipo de fit", TIPOS_FIT)
    + campo("exit_indicador", "Um indicador de elo que mostraria se ela está funcionando", 2)
    + campo("exit_mudou", "O que mudou na sua leitura da empresa entre a lista do início da aula e o mapa?", 3))

B["mapa_volta"] = P1.B["mapa_volta"]


def bloco(chave):
    return B[chave]


def mapa_sistema(nome):
    """Mapa dentro do texto de Porter (diretiva ?MAPA da tradução)."""
    return MA.figura(nome) + NOTA_MAPA


def visual(nome):
    if nome == "mapa_vivelar":
        return MA.figura("vivelar")
    if nome == "mapas_abas":
        ordem = [("ikea", "Ikea"), ("vanguard", "Vanguard"), ("southwest", "Southwest")]
        botoes = "".join(f'<button type="button" class="msa-aba" role="tab" aria-selected="{"true" if i == 2 else "false"}">{E(t)}</button>' for i, (_, t) in enumerate(ordem))
        figs = [MA.figura(n) for n, _ in ordem]
        figs = [f.replace('<figure class="msa"', '<figure class="msa" hidden', 1) if i != 2 else f for i, f in enumerate(figs)]
        return f'<div class="msa-abas" data-atividade><div class="msa-abas-botoes" role="tablist" aria-label="Os três mapas de Porter">{botoes}</div>{"".join(figs)}{NOTA_MAPA}</div>'
    return ""


MODULOS = [
    ("Mapa de aprendizagem", "Diagnóstico", "Mapa de aprendizagem", "Marque o que você já domina e volte aqui no fim da aula."),
    ("Texto de Porter", "Leitura", "Texto de Porter (Parte IV)", "Tradução da Parte IV, com os três mapas redesenhados, destaques, anotações e pausas para responder."),
    ("Abertura", "Abertura", "Da Parte III à Parte IV", "A pergunta de Porter sobre a Southwest: qual é a competência essencial?"),
    ("Bloco 1", "Bloco 1", "Atividades combinadas", "O giro de 15 minutos, “tudo importa” e a corrente do elo mais forte."),
    ("Bloco 2", "Bloco 2", "Os três tipos de fit", "Consistência, reforço e otimização do esforço, com os exemplos de Porter."),
    ("Bloco 3", "Bloco 3", "Fit e sustentabilidade", "Por que sistemas protegem mais que atividades e a definição final de estratégia."),
    ("Bloco 4", "Bloco 4", "Como ler um mapa", "Os mapas de Ikea, Vanguard e Southwest: temas, atividades, ligações e renúncias."),
    ("Bloco 5", "Bloco 5", "Como construir um mapa", "O método passo a passo, o exemplo da Vivelar e o mapa da sua empresa."),
    ("Bloco 6", "Bloco 6", "Dúvidas comuns", "Cinco dúvidas frequentes: responda antes de ler o comentário."),
    ("Bloco 7", "Bloco 7", "Execução e BSC", "Medir elos, metas que quebram o fit e a nova camada do BSC da Vivelar."),
    ("Fechamento", "Fechamento", "Síntese e exit ticket", "Sete ideias, as duas visões de estratégia, exit ticket e revisão do mapa."),
    ("Para consulta", "Consulta", "Para consulta", "Os casos em um quadro, armadilhas comuns e referências."),
]


def info_modulo(titulo):
    for prefixo, tipo, curto, desc in MODULOS:
        if titulo.startswith(prefixo):
            return {"tipo": tipo, "curto": curto, "desc": desc}
    return {"tipo": "Módulo", "curto": titulo, "desc": ""}


REGRAS = [
    ("Mapa de aprendizagem", {"mapa": True}),
    ("A pergunta de Porter sobre a Southwest", {"antes_revelar": ["abertura"]}),
    ("1.2 O giro de 15 minutos", {"fim": ["b1_resultado"]}),
    ("1.6 Fit genérico", {"fim": ["b1_generico"]}),
    ("2.5 Treine a classificação", {"antes_revelar": ["b2_classifica"], "fim": ["b2_sua"]}),
    ("3.4 Imitar parte", {"fim": ["b3_copia"]}),
    ("3.6 Competição", {"fim": ["b3_toys"]}),
    ("3.8 A definição final", {"fim": ["b3_definicao"]}),
    ("4.6 Exercício de leitura", {"antes_revelar": ["b4_leitura"]}),
    ("Passo 6: o diagnóstico", {"fim": ["b5_t4"]}),
    ("5.5 Construa o mapa", {"fim": ["b5_construtor"]}),
    ("Dúvida 1:", {"apos_titulo": ["b6_duvida1"], "recolher": True}),
    ("Dúvida 2:", {"apos_titulo": ["b6_duvida2"], "recolher": True}),
    ("Dúvida 3:", {"apos_titulo": ["b6_duvida3"], "recolher": True}),
    ("Dúvida 4:", {"apos_titulo": ["b6_duvida4"], "recolher": True}),
    ("Dúvida 5:", {"apos_titulo": ["b6_duvida5"], "recolher": True}),
    ("7.1 Por que o fit", {"fim": ["b7_dono"]}),
    ("7.7 Avaliar iniciativas", {"antes_revelar": ["b7_filtro"]}),
    ("7.9 Aplique", {"fim": ["b7_aplicar"]}),
    ("Síntese em sete ideias", {"fim": ["sintese"]}),
    ("Exit ticket", {"fim": ["exit", "mapa_volta"]}),
]


def _modelo():
    m = P1.MODELO
    trocas = [
        ('<div class="sidebar-badge"><span class="dot"></span><span>Aula {{n}} · Parte I</span></div>',
         '<div class="sidebar-badge"><span class="dot"></span><span>Aula {{n}} · Parte IV</span></div>'),
        ('<div class="sidebar-title">Eficácia operacional não é estratégia</div>',
         '<div class="sidebar-title">O fit gera vantagem e sustentabilidade</div>'),
        ("Aula {{n}} · Parte I do artigo · pp. 37–40", "Aula {{n}} · Parte IV do artigo · pp. 45–50"),
        ("titulo: 'Aula {{n}} · Parte I: Eficácia operacional não é estratégia', crumb: 'Aula {{n}} · Parte I'",
         "titulo: 'Aula {{n}} · Parte IV: O fit gera vantagem e sustentabilidade', crumb: 'Aula {{n}} · Parte IV'"),
        ('<script src="../assets/js/parte.js"></script>',
         '<script src="../assets/js/mapas.js"></script>\n<script src="../assets/js/parte.js"></script>'),
    ]
    for a, b in trocas:
        assert m.count(a) == 1, a
        m = m.replace(a, b)
    return m


MODELO = _modelo()
