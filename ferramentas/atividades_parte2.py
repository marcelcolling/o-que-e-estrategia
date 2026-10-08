"""
Atividades da Parte II (Aula 2), onde cada uma entra no material, os módulos e o modelo da página.
Os componentes (campo, escolha, caixa, pausa, mapa) e o modelo da página vêm de atividades_parte1.

ATENÇÃO: as chaves usadas em data-campo são gravadas na planilha, na atividade "aula2".
Não renomeie uma chave depois que a turma começar a responder: as respostas salvas
ficariam órfãs. Para tirar uma pergunta, apague a caixa; para acrescentar, use uma chave nova.
"""
import atividades_parte1 as P1
from atividades_parte1 import E, campo, escolha, caixa, pausa, mapa  # noqa: F401  (pausa e mapa são usados pelo gerador)

ANTES = "Escreva a sua resposta <strong>antes</strong> de abrir o comentário. Depois compare: o que você acertou, o que faltou?"
ORIGENS = [("variedade", "Variedade"), ("necessidades", "Necessidades"), ("acesso", "Acesso")]


def espelho(chave, vazio):
    """Mostra, só para leitura, o que o estudante escreveu em outro campo (preenchido por parte.js, com escape)."""
    return f'<blockquote class="espelho" data-atividade data-espelho="{chave}" data-vazio="{E(vazio)}"></blockquote>'


B = {}

B["prep"] = caixa(
    "Antes de ler", "A estratégia de uma empresa que você conhece",
    "Responda antes de ler o texto de Porter. Esta resposta volta na abertura, no Bloco 1 e no exit ticket.",
    campo("prep_frase", "Descreva em uma frase a estratégia da sua empresa (ou de uma empresa que você conhece bem)", 2,
          "Ex.: Somos a escolha de quem quer…")
    + campo("prep_atividades", "Liste três atividades que ela executa de forma diferente do principal concorrente (uma por linha)", 3,
            "1.\n2.\n3."),
    tipo="Antes de ler")

B["abertura_frase"] = caixa(
    "Abertura", "Em que coluna cai a sua frase?", "A frase que você escreveu antes de ler:",
    espelho("prep_frase", "Você ainda não escreveu a sua frase. Ela fica no início do módulo Texto de Porter.")
    + escolha("abertura_tipo", "A sua frase fala sobretudo de…",
              [("clientes", "Clientes e atributos"), ("atividades", "Atividades"), ("mistura", "Um pouco de cada")])
    + campo("abertura_porque", "Foi fácil ou difícil listar as três atividades diferentes? O que isso indica?", 3))

B["b1_slogan"] = caixa(
    "Bloco 1 · A ideia central", "Aplique o teste do slogan à sua frase", "",
    espelho("prep_frase", "Escreva a sua frase no início do módulo Texto de Porter.")
    + escolha("b1_slogan_passa", "Se você trocar o nome da empresa pelo do concorrente, a frase continua verdadeira?",
              [("sim", "Sim: é slogan"), ("em parte", "Em parte"), ("não", "Não: descreve atividades próprias")])
    + campo("b1_slogan_reescrita", "Reescreva a frase usando atividades que o concorrente não executa", 3))

B["b1_checagem"] = caixa(
    "Bloco 1 · A ideia central", "Pergunta de checagem", ANTES,
    campo("b1_checagem", "O que a Parte II responderia à consultoria?", 3))

B["b2_cadeia"] = caixa(
    "Bloco 2 · Southwest e Ikea", "A cadeia comparada",
    "Edite os nomes das atividades se quiser, compare as duas empresas e marque cada linha. O resumo mostra quantas são de fato diferentes.",
    campo("b2_empresas", "Empresa analisada e o concorrente tradicional dela", 1, "Ex.: Nubank × banco tradicional")
    + '<div class="cadeia-widget" data-widget="cadeia"></div>'
    + campo("b2_acrescenta", "Alguma atividade é acrescentada, como o espaço infantil da Ikea, e não apenas cortada? Qual?", 2)
    + campo("b2_frase", "Escreva a frase de posição dessa empresa usando as atividades diferentes. Ela passa no teste do slogan?", 3))

B["b3_filtro"] = caixa(
    "Bloco 3 · As três origens", "O filtro das necessidades", "",
    campo("b3_filtro_nec", "Uma necessidade de um grupo de clientes que a sua empresa diz atender", 2)
    + campo("b3_filtro_ativ", "Que atividade vocês fazem diferente para atendê-la? Se a resposta for “nenhuma, só fazemos melhor”, o que isso revela?", 3))

CASOS = [("jiffy", "Jiffy Lube"), ("ikea", "Ikea"), ("carmike", "Carmike"), ("southwest", "Southwest"),
         ("bessemer", "Bessemer"), ("vanguard", "Vanguard")]


def _classificacao():
    linhas = []
    for k, nome in CASOS:
        radios = "".join(
            f'<label class="pilula"><input type="radio" name="b3_cls_{k}" value="{v}" data-campo="b3_cls_{k}" '
            f'data-rotulo="{E(nome)}: origem principal"><span>{t}</span></label>' for v, t in ORIGENS)
        linhas.append(
            f'<div class="cls-linha"><span class="cls-nome">{E(nome)}</span>'
            f'<div class="pilulas" role="group" aria-label="Origem da posição: {E(nome)}">{radios}</div>'
            f'<label class="ativ-campo cls-just"><span class="ativ-rot">Atividade que sustenta a classificação</span>'
            f'<textarea data-campo="b3_cls_{k}_ativ" data-rotulo="{E(nome)}: atividade que sustenta" rows="1"></textarea></label></div>')
    return '<div class="cls-grade">' + "".join(linhas) + "</div>"


B["b3_classificacao"] = caixa("Bloco 3 · As três origens", "Classifique os seis casos", ANTES, _classificacao())

B["b4_focados"] = caixa(
    "Bloco 4 · Foco, alvo amplo e genéricas", "Além ou aquém do necessário", "",
    '<div class="colunas2">'
    + campo("b4_alem", "No seu setor, quem está pagando por algo que não usa?", 3)
    + campo("b4_aquem", "E quem gostaria de pagar mais por algo que ninguém oferece?", 3)
    + "</div>")

B["b4_camadas"] = caixa(
    "Bloco 4 · Foco, alvo amplo e genéricas", "As três camadas na sua empresa",
    "Use a mesma empresa da sua frase de estratégia e desça do nível mais genérico ao mais concreto.",
    escolha("b4_generica", "1. Estratégia genérica",
            [("custo", "Liderança em custo"), ("diferenciacao", "Diferenciação"), ("foco-custo", "Foco em custo"),
             ("foco-diferenciacao", "Foco com diferenciação"), ("indefinida", "Não está claro")])
    + escolha("b4_origem", "2. Origem da posição", ORIGENS + [("combinacao", "Combinação"), ("nenhuma", "Não há posição clara")])
    + campo("b4_atividades", "3. Que atividades sob medida materializam essa posição?", 3))

for n in range(1, 7):
    B[f"b5_duvida{n}"] = caixa(
        "Bloco 5 · Dúvidas comuns", f"Dúvida {n}: sua resposta",
        "Antes de abrir o comentário, responda com o que você entendeu da Parte II.",
        campo(f"b5_duvida{n}", f"Dúvida {n}: minha resposta antes de ler", 3, mostrar_rotulo=False))

B["b6_ia"] = caixa(
    "Bloco 6 · Novas posições", "A mesma tecnologia, dois usos", "",
    campo("b6_ia", "Pense numa tecnologia recente no seu setor. Como ela seria usada só como EO, e como poderia abrir uma posição nova, com atividades diferentes?", 4))

B["b6_caso"] = caixa(
    "Bloco 6 · Novas posições", "Analise um caso",
    "Escolha um dos casos (ou outro que você conheça bem) e aplique o método.",
    escolha("b6_caso_escolha", "Caso escolhido",
            [("nubank", "Nubank"), ("azul", "Azul"), ("academias", "Academias de baixo custo"), ("outro", "Outro")])
    + campo("b6_caso_outro", "Se escolheu outro, qual?", 1)
    + escolha("b6_caso_origem", "Origem principal da posição", ORIGENS + [("combinacao", "Combinação")])
    + campo("b6_caso_mudanca", "Que mudança abriu a posição?", 2)
    + campo("b6_caso_atividades", "Que atividades diferem das dos estabelecidos? O estabelecido conseguiria replicá-las sem mexer no que já faz?", 3))

B["b7_processo"] = caixa(
    "Bloco 7 · Execução e BSC", "Um processo que só faz sentido para vocês", "",
    campo("b7_processo", "No BSC (ou nas metas) da sua empresa, que objetivo de processos só faria sentido para vocês? Se não houver nenhum, o que isso indica?", 3))

B["b7_rastreio"] = caixa(
    "Bloco 7 · Execução e BSC", "Matriz de rastreabilidade",
    "Para cada objetivo de clientes do mapa estratégico (ou das metas) da sua empresa, aponte o objetivo de processos que o sustenta e marque se o principal concorrente executa esse processo.",
    '<div class="rastreio-widget" data-widget="rastreio"></div>'
    + campo("b7_rastreio_conclusao", "O que a matriz revela sobre o seu mapa: posição ou slogan?", 3))

B["b7_palpite"] = caixa(
    "Bloco 7 · Execução e BSC", "Antes de ler a tabela",
    "Aposte primeiro e depois compare com a tabela abaixo.",
    escolha("b7_palpite_origem", "Qual origem de posição você acha que passa no teste das atividades, dentro dos limites da diretoria?", ORIGENS)
    + campo("b7_palpite_porque", "Por quê?", 2))

B["b7_perguntas"] = caixa(
    "Bloco 7 · Execução e BSC", "Perguntas sobre o caso", "",
    campo("b7_q1", "1. Na matriz de rastreabilidade do BSC da Vivelar por acesso, qual linha é a mais frágil? Que processo o líder conseguiria copiar com mais facilidade?", 3)
    + campo("b7_q2", "2. Reescreva o BSC-slogan para que a posição por necessidades passe no teste das atividades. Que atividade nova seria necessária, e ela cabe nos limites da diretoria?", 3)
    + campo("b7_q3", "3. Se a Vivelar considerasse o lojista (e não a consumidora) como cliente principal, a posição seria por acesso ou por necessidades? Isso muda o BSC?", 3)
    + campo("b7_q4", "4. Pense no BSC (ou nas metas) de uma empresa real que você conhece. Há indicadores que puniriam a própria posição, como a Bessemer num benchmarking de custo de pessoal?", 3))

SINTESE = [
    "Estratégia competitiva é escolher deliberadamente um conjunto diferente de atividades.",
    "A posição se materializa nas atividades, não na descrição dos clientes.",
    "Estratégia é criar uma posição única e valiosa, e só existe porque não há uma posição ideal única.",
    "Posições nascem de variedade, necessidades ou acesso, que se combinam.",
    "Uma necessidade diferente só vira posição se as atividades também forem diferentes.",
    "Posição não é nicho: pode ser ampla ou focada.",
    "Novas posições surgem sobretudo de mudanças, e os entrantes costumam enxergá-las primeiro.",
]
B["sintese"] = caixa(
    "Fechamento", "Consigo explicar com minhas palavras?",
    "Marque as ideias que você seria capaz de explicar a um colega sem consultar o texto. As que ficarem sem marca indicam o que reler.",
    '<div class="checks">' + "".join(
        f'<label class="check"><input type="checkbox" data-campo="sintese_{k}" data-rotulo="{E(t)}"><span>{k}. {E(t)}</span></label>'
        for k, t in enumerate(SINTESE, 1)) + "</div>")

B["exit"] = caixa(
    "Fechamento · Exit ticket", "Exit ticket",
    'Retome a frase que você escreveu no início <button type="button" class="b-trazer" data-trazer="prep_frase:exit_frase">Usar a frase do início</button>',
    campo("exit_frase", "Frase de estratégia reescrita", 3,
          "Atendemos [variedade / grupo de clientes / contexto de acesso], oferecendo [combinação de valor]. Para isso, [atividade 1] e [atividade 2], que o [concorrente] não executa.")
    + escolha("exit_origem", "Origem da posição", ORIGENS + [("combinacao", "Combinação")])
    + '<div class="colunas2">'
    + campo("exit_ativ1", "Atividade 1 que o principal concorrente não executa", 2)
    + campo("exit_ativ2", "Atividade 2 que o principal concorrente não executa", 2)
    + "</div>"
    + campo("exit_revela", "Se não conseguiu citar nenhuma, o que isso revela? Se conseguiu, o que mudou em relação à frase do início?", 3))

B["mapa_volta"] = P1.B["mapa_volta"]


def bloco(chave):
    return B[chave]


def visual(nome):
    return ""


MODULOS = [
    ("Mapa de aprendizagem", "Diagnóstico", "Mapa de aprendizagem", "Marque o que você já domina e volte aqui no fim da aula."),
    ("Texto de Porter", "Leitura", "Texto de Porter (Parte II)", "Tradução da Parte II e de dois quadros, com destaques, anotações e pausas para responder."),
    ("Abertura", "Abertura", "Da Parte I à Parte II", "O que ficou em aberto na Parte I e a sua frase de estratégia."),
    ("Bloco 1", "Bloco 1", "A ideia central", "Clientes ou atividades, o teste do slogan e a definição de estratégia."),
    ("Bloco 2", "Bloco 2", "Southwest e Ikea", "Dois casos-âncora e o método da cadeia comparada."),
    ("Bloco 3", "Bloco 3", "As três origens das posições", "Variedade, necessidades e acesso, com exercício de classificação."),
    ("Bloco 4", "Bloco 4", "Foco, alvo amplo e genéricas", "Posição não é nicho, e onde entram as estratégias genéricas."),
    ("Bloco 5", "Bloco 5", "Dúvidas comuns", "Seis dúvidas frequentes: responda antes de ler o comentário."),
    ("Bloco 6", "Bloco 6", "Novas posições", "Por que os entrantes enxergam primeiro, com casos atuais."),
    ("Bloco 7", "Bloco 7", "Execução e BSC", "Da posição ao mapa estratégico, com o caso Vivelar."),
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
    ("A sua frase de estratégia", {"fim": ["abertura_frase"]}),
    ("1.2 Clientes ou atividades", {"fim": ["b1_slogan"]}),
    ("Pergunta de checagem", {"antes_revelar": ["b1_checagem"]}),
    ("2.4 Exercício", {"fim": ["b2_cadeia"]}),
    ("3.2 Posicionamento por necessidades", {"apos_bloco": [("Use isso como filtro", ["b3_filtro"])]}),
    ("3.6 Exercício de classificação", {"antes_revelar": ["b3_classificacao"]}),
    ("4.2 Onde os focados", {"fim": ["b4_focados"]}),
    ("4.3 A conexão", {"fim": ["b4_camadas"]}),
    ("Dúvida 1:", {"apos_titulo": ["b5_duvida1"], "recolher": True}),
    ("Dúvida 2:", {"apos_titulo": ["b5_duvida2"], "recolher": True}),
    ("Dúvida 3:", {"apos_titulo": ["b5_duvida3"], "recolher": True}),
    ("Dúvida 4:", {"apos_titulo": ["b5_duvida4"], "recolher": True}),
    ("Dúvida 5:", {"apos_titulo": ["b5_duvida5"], "recolher": True}),
    ("Dúvida 6:", {"apos_titulo": ["b5_duvida6"], "recolher": True}),
    ("6.3 Quando a mudança", {"fim": ["b6_ia"]}),
    ("6.4 Casos atuais", {"fim": ["b6_caso"]}),
    ("7.1 Por que a Parte II", {"fim": ["b7_processo"]}),
    ("7.4 Quatro práticas", {"apos_bloco": [("**Prática 1: a matriz de rastreabilidade.**", ["b7_rastreio"])]}),
    ("7.5 O caso Vivelar", {"apos_bloco": [("**A pergunta da Parte II:**", ["b7_palpite"])]}),
    ("7.7 Perguntas sobre o caso", {"fim": ["b7_perguntas"]}),
    ("Síntese em sete ideias", {"fim": ["sintese"]}),
    ("Exit ticket", {"fim": ["exit", "mapa_volta"]}),
]


def _modelo():
    m = P1.MODELO
    trocas = [
        ('<div class="sidebar-badge"><span class="dot"></span><span>Aula {{n}} · Parte I</span></div>',
         '<div class="sidebar-badge"><span class="dot"></span><span>Aula {{n}} · Parte II</span></div>'),
        ('<div class="sidebar-title">Eficácia operacional não é estratégia</div>',
         '<div class="sidebar-title">A estratégia se apoia em atividades únicas</div>'),
        ("Aula {{n}} · Parte I do artigo · pp. 37–40", "Aula {{n}} · Parte II do artigo · pp. 39–43"),
        ("titulo: 'Aula {{n}} · Parte I: Eficácia operacional não é estratégia', crumb: 'Aula {{n}} · Parte I'",
         "titulo: 'Aula {{n}} · Parte II: A estratégia se apoia em atividades únicas', crumb: 'Aula {{n}} · Parte II'"),
    ]
    for a, b in trocas:
        assert m.count(a) == 1, a
        m = m.replace(a, b)
    return m


MODELO = _modelo()
