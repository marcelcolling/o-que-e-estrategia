"""
Atividades da Parte III (Aula 3), onde cada uma entra no material, os módulos e o modelo da página.
Os componentes (campo, escolha, caixa, pausa, mapa) e o modelo da página vêm de atividades_parte1;
o espelho vem de atividades_parte2. A Aula 3 não tem widget próprio.

ATENÇÃO: as chaves usadas em data-campo são gravadas na planilha, na atividade "aula3".
Não renomeie uma chave depois que a turma começar a responder: as respostas salvas
ficariam órfãs. Para tirar uma pergunta, apague a caixa; para acrescentar, use uma chave nova.
"""
import atividades_parte1 as P1
from atividades_parte1 import E, campo, escolha, caixa, pausa, mapa  # noqa: F401  (pausa e mapa são usados pelo gerador)
from atividades_parte2 import espelho

ANTES = "Escreva a sua resposta <strong>antes</strong> de abrir o comentário. Depois compare: o que você acertou, o que faltou?"
ORIGENS = [("imagem", "Imagem ou reputação"), ("atividades", "Atividades"), ("coordenacao", "Coordenação e controle")]
SIM_NAO = [("sim", "Sim"), ("nao", "Não")]


def sub(texto):
    """Subtítulo dentro de uma caixa (separa os itens de uma mesma atividade)."""
    return f'<p class="ativ-sub">{texto}</p>'


def vazio_renuncia(i):
    return f"Você ainda não escreveu a renúncia {i}. A lista fica no início do módulo Texto de Porter."


B = {}

B["prep"] = caixa(
    "Antes de ler", "A lista do “não” de uma empresa que você conhece",
    "Responda antes de ler o texto de Porter. Liste três coisas que a sua empresa (ou uma empresa que você conhece bem) "
    "decidiu deliberadamente <strong>não</strong> fazer, mesmo que algum cliente tenha pedido, e o que ela perde por não fazê-las. "
    "A segunda pergunta é a mais difícil, e a mais importante. A lista volta na abertura, no Bloco 3 e no exit ticket.",
    "".join(
        '<div class="colunas2">'
        + campo(f"prep_nao{i}", f"Renúncia {i}: o que a empresa decidiu não fazer", 2)
        + campo(f"prep_perde{i}", f"Renúncia {i}: o que a empresa perde por não fazer", 2)
        + "</div>"
        for i in (1, 2, 3)),
    tipo="Antes de ler")

B["abertura_lista"] = caixa(
    "Abertura", "Uma primeira leitura da sua lista", "As três renúncias que você listou antes de ler:",
    "".join(espelho(f"prep_nao{i}", vazio_renuncia(i)) for i in (1, 2, 3))
    + campo("abertura_leitura", "Pela leitura provisória da tabela, qual delas parece custar mais à empresa? Alguma é algo que ela simplesmente nunca quis fazer?", 3))

B["b1_palpite"] = caixa(
    "Bloco 1 · Por que a posição não basta", "Seu palpite", "Ele volta no Bloco 4, onde a pergunta é respondida.",
    campo("b1_palpite", "Se tudo pode ser comprado, por que a Southwest não foi copiada?", 3))

B["b2_renuncia"] = caixa(
    "Bloco 2 · Neutrogena", "Quem a renúncia afasta", "",
    campo("b2_renuncia", "Escolha uma das renúncias da Neutrogena. Que tipo de concorrente ela afasta, e o que esse concorrente teria de abandonar para copiá-la?", 3))


def _lista():
    itens = []
    for i in (1, 2, 3):
        itens.append(
            sub(f"Renúncia {i}")
            + espelho(f"prep_nao{i}", vazio_renuncia(i))
            + escolha(f"b3_cls_{i}", f"Renúncia {i}: há incompatibilidade com a posição? Qual origem predomina?",
                      ORIGENS + [("nenhuma", "Nenhuma: não é trade-off")])
            + campo(f"b3_cls_{i}_just", f"Renúncia {i}: um concorrente conseguiria fazer as duas coisas ao mesmo tempo? Por quê?", 2))
    return "".join(itens)


B["b3_lista"] = caixa(
    "Bloco 3 · As três origens", "Classifique a sua lista do “não”",
    "Se não houver incompatibilidade, marque “Nenhuma”: a renúncia não é trade-off.", _lista())

B["b4_origens"] = caixa(
    "Bloco 4 · Continental Lite", "As três origens no caso", ANTES,
    campo("b4_atividades", "Atividades: o que, na Continental Lite, era incompatível com a posição copiada?", 2)
    + campo("b4_imagem", "Imagem ou reputação: o que mudou para os clientes e os agentes do serviço completo?", 2)
    + campo("b4_coordenacao", "Coordenação e controle: por que a empresa recorreu a “soluções” que valiam para todos?", 2))

B["b4_retomada"] = caixa(
    "Bloco 4 · Continental Lite", "O seu palpite do Bloco 1", "Compare com a resposta abaixo:",
    espelho("b1_palpite", "Você ainda não registrou o palpite. Ele fica no Bloco 1, em 1.2."),
    tipo="Retomada")

B["b4_caso"] = caixa(
    "Bloco 4 · Continental Lite", "Analise um caso", "Escolha um dos casos (ou outro que você conheça bem) e aplique o método.",
    escolha("b4_caso_escolha", "Caso escolhido",
            [("subsidiarias", "Subsidiárias de baixo custo"), ("tarifas", "Tarifas básicas"),
             ("bancos", "Marcas digitais de bancos"), ("outro", "Outro")])
    + campo("b4_caso_outro", "Se escolheu outro, qual?", 1)
    + campo("b4_caso_analise", "O que foi copiado, o que foi mantido e onde está a incompatibilidade? O padrão lembra a Continental Lite?", 4))

B["b5_falso_real"] = caixa(
    "Bloco 5 · Qualidade nem sempre é grátis", "Falso ou real na sua empresa", "",
    '<div class="colunas2">'
    + campo("b5_falso", "Um trade-off que era falso (e que a melhoria operacional eliminou)", 3)
    + campo("b5_real", "Um trade-off que é real (e que obriga a escolher)", 3)
    + "</div>")

for n in range(1, 6):
    B[f"b6_duvida{n}"] = caixa(
        "Bloco 6 · Dúvidas comuns", f"Dúvida {n}: sua resposta",
        "Antes de abrir o comentário, responda com o que você entendeu da Parte III.",
        campo(f"b6_duvida{n}", f"Dúvida {n}: minha resposta antes de ler", 3, mostrar_rotulo=False))

B["b7_documento"] = caixa(
    "Bloco 7 · Execução e BSC", "Onde estão as renúncias?", "",
    campo("b7_documento", "Em que documento da sua empresa estão escritas as renúncias estratégicas? Quem é cobrado por elas?", 3))

B["b7_concorrente"] = caixa(
    "Bloco 7 · Execução e BSC", "O teste do concorrente", "",
    campo("b7_concorrente", "O que o principal concorrente da sua empresa teria de abandonar para fazer o que vocês fazem? Se a resposta for “nada”, o que isso indica?", 3))

B["b7_palpite"] = caixa(
    "Bloco 7 · Execução e BSC", "Antes de ler a análise", "Aposte primeiro e depois compare com a tabela abaixo.",
    escolha("b7_palpite", "O líder conseguiria copiar a posição por acesso da Vivelar?",
            [("sim", "Sim, sem abrir mão de nada"), ("custo", "Sim, mas abrindo mão de algo"), ("nao", "Na prática, não")])
    + campo("b7_palpite_origem", "Que origem de trade-off você acha que mais protege a Vivelar? Por quê?", 2))

SITUACOES = [(1, "Mês 10: tabloide de fim de ano"), (2, "Mês 14: promoção-relâmpago"),
             (3, "Mês 16: distribuidor com grandes lotes"), (4, "Mês 20: campanha nacional")]
DECISOES = [("aprovar", "Aprovar"), ("recusar", "Recusar"), ("diretoria", "Levar à diretoria")]
B["b7_filtro"] = caixa(
    "Bloco 7 · Execução e BSC", "O filtro de straddling", ANTES,
    "".join(
        sub(f"Situação {k} · {E(t)}")
        + escolha(f"b7_f{k}", f"Situação {k} ({t}): decisão", DECISOES)
        + campo(f"b7_f{k}_porque", f"Situação {k}: que origem de trade-off está em jogo? Por quê?", 2)
        for k, t in SITUACOES))

SINTESE = [
    "Uma posição única e valiosa atrai imitação, por reposicionamento ou, mais comumente, por straddling.",
    "Trade-off é incompatibilidade entre atividades, não qualquer “não”.",
    "Os trade-offs criam a necessidade de escolher e protegem a posição.",
    "Os trade-offs têm três origens: imagem ou reputação, atividades e coordenação e controle.",
    "Straddling cobra uma penalidade: degrada a posição original.",
    "Longe da fronteira, os trade-offs costumam ser falsos; na fronteira, são reais.",
    "Estratégia é fazer trade-offs: o centro dela está em escolher o que não fazer.",
]
B["sintese"] = caixa(
    "Fechamento", "Consigo explicar com minhas palavras?",
    "Marque as ideias que você seria capaz de explicar a um colega sem consultar o texto. As que ficarem sem marca indicam o que reler.",
    '<div class="checks">' + "".join(
        f'<label class="check"><input type="checkbox" data-campo="sintese_{k}" data-rotulo="{E(t)}"><span>{k}. {E(t)}</span></label>'
        for k, t in enumerate(SINTESE, 1)) + "</div>")

B["exit"] = caixa(
    "Fechamento · Exit ticket", "Exit ticket",
    'Escolha uma renúncia da lista do início: '
    + " ".join(f'<button type="button" class="b-trazer" data-trazer="prep_nao{i}:exit_renuncia">Usar a renúncia {i}</button>' for i in (1, 2, 3)),
    campo("exit_renuncia", "Renúncia escolhida", 2)
    + '<div class="colunas3">'
    + escolha("exit_custo", "Custo: a empresa perde algo de valor com ela?", SIM_NAO)
    + escolha("exit_incompat", "Incompatibilidade: fazer o contrário prejudicaria a posição?", SIM_NAO)
    + escolha("exit_protecao", "Proteção: o concorrente teria de abrir mão de algo parecido?", SIM_NAO)
    + "</div>"
    + escolha("exit_origem", "Origem do trade-off", ORIGENS + [("nenhuma", "Não passa nos testes")])
    + campo("exit_indicador", "Que indicador mostraria, no BSC (ou nas metas) da sua empresa, que ela está sendo respeitada? Qual seria a meta?", 3)
    + campo("exit_mudou", "O que mudou na sua leitura da lista entre o início da aula e agora?", 3))

B["mapa_volta"] = P1.B["mapa_volta"]


def bloco(chave):
    return B[chave]


def visual(nome):
    return ""


MODULOS = [
    ("Mapa de aprendizagem", "Diagnóstico", "Mapa de aprendizagem", "Marque o que você já domina e volte aqui no fim da aula."),
    ("Texto de Porter", "Leitura", "Texto de Porter (Parte III)", "Tradução da Parte III, com destaques, anotações e pausas para responder."),
    ("Abertura", "Abertura", "Da Parte II à Parte III", "A pergunta que ficou em aberto e a sua lista do “não”."),
    ("Bloco 1", "Bloco 1", "Por que a posição não basta", "As duas formas de imitação e a definição de trade-off."),
    ("Bloco 2", "Bloco 2", "Neutrogena", "Uma posição construída com renúncias."),
    ("Bloco 3", "Bloco 3", "As três origens dos trade-offs", "Imagem, atividades e coordenação, aplicadas à sua lista."),
    ("Bloco 4", "Bloco 4", "Continental Lite", "O straddling e a penalidade que ele cobra."),
    ("Bloco 5", "Bloco 5", "Qualidade nem sempre é grátis", "Trade-offs falsos e reais, Honda e Toyota e a nova definição."),
    ("Bloco 6", "Bloco 6", "Dúvidas comuns", "Cinco dúvidas frequentes: responda antes de ler o comentário."),
    ("Bloco 7", "Bloco 7", "Execução e BSC", "A lista do “não”, indicadores de disciplina e o caso Vivelar."),
    ("Fechamento", "Fechamento", "Síntese e exit ticket", "Sete ideias, exit ticket e revisão do mapa."),
    ("Para consulta", "Consulta", "Para consulta", "Os casos em um quadro, armadilhas comuns e referências."),
]


def info_modulo(titulo):
    for prefixo, tipo, curto, desc in MODULOS:
        if titulo.startswith(prefixo):
            return {"tipo": tipo, "curto": curto, "desc": desc}
    return {"tipo": "Módulo", "curto": titulo, "desc": ""}


REGRAS = [
    ("Mapa de aprendizagem", {"mapa": True}),
    ("A sua lista do", {"fim": ["abertura_lista"]}),
    ("1.2 O teste mais duro", {"fim": ["b1_palpite"]}),
    ("2.3 O que o caso ensina", {"fim": ["b2_renuncia"]}),
    ("3.6 Exercício", {"fim": ["b3_lista"]}),
    ("4.4 As três origens no caso", {"antes_revelar": ["b4_origens"]}),
    ("4.5 Resposta à pergunta", {"apos_titulo": ["b4_retomada"]}),
    ("4.6 O padrão se repetiu", {"fim": ["b4_caso"]}),
    ("5.1 Trade-offs falsos e reais", {"fim": ["b5_falso_real"]}),
    ("Dúvida 1:", {"apos_titulo": ["b6_duvida1"], "recolher": True}),
    ("Dúvida 2:", {"apos_titulo": ["b6_duvida2"], "recolher": True}),
    ("Dúvida 3:", {"apos_titulo": ["b6_duvida3"], "recolher": True}),
    ("Dúvida 4:", {"apos_titulo": ["b6_duvida4"], "recolher": True}),
    ("Dúvida 5:", {"apos_titulo": ["b6_duvida5"], "recolher": True}),
    ("7.1 Por que trade-off", {"fim": ["b7_documento"]}),
    ("7.3 Quatro práticas", {"fim": ["b7_concorrente"]}),
    ("7.5 O caso Vivelar", {"apos_bloco": [("**A pergunta que ficou da Aula 2:**", ["b7_palpite"])]}),
    ("7.8 Treine o filtro", {"antes_revelar": ["b7_filtro"]}),
    ("Síntese em sete ideias", {"fim": ["sintese"]}),
    ("Exit ticket", {"fim": ["exit", "mapa_volta"]}),
]


def _modelo():
    m = P1.MODELO
    trocas = [
        ('<div class="sidebar-badge"><span class="dot"></span><span>Aula {{n}} · Parte I</span></div>',
         '<div class="sidebar-badge"><span class="dot"></span><span>Aula {{n}} · Parte III</span></div>'),
        ('<div class="sidebar-title">Eficácia operacional não é estratégia</div>',
         '<div class="sidebar-title">Uma posição sustentável exige trade-offs</div>'),
        ("Aula {{n}} · Parte I do artigo · pp. 37–40", "Aula {{n}} · Parte III do artigo · pp. 43–45"),
        ("titulo: 'Aula {{n}} · Parte I: Eficácia operacional não é estratégia', crumb: 'Aula {{n}} · Parte I'",
         "titulo: 'Aula {{n}} · Parte III: Uma posição sustentável exige trade-offs', crumb: 'Aula {{n}} · Parte III'"),
    ]
    for a, b in trocas:
        assert m.count(a) == 1, a
        m = m.replace(a, b)
    return m


MODELO = _modelo()
