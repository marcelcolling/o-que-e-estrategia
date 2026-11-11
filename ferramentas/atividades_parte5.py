"""
Atividades da Parte V (Aula 5), onde cada uma entra no material, os módulos e o modelo da página.
Os componentes (campo, escolha, caixa, pausa, mapa) e o modelo da página vêm de atividades_parte1;
o espelho vem de atividades_parte2 e sub() de atividades_parte3. O mapa da Neutrogena (antes e depois)
vem de mapas_atividades.py e usa a interação de assets/js/mapas.js. A Aula 5 não tem widget próprio.

ATENÇÃO: as chaves usadas em data-campo são gravadas na planilha, na atividade "aula5".
Não renomeie uma chave depois que a turma começar a responder: as respostas salvas
ficariam órfãs. Para tirar uma pergunta, apague a caixa; para acrescentar, use uma chave nova.
"""
import math

import atividades_parte1 as P1
from atividades_parte1 import E, campo, escolha, caixa, pausa, mapa  # noqa: F401  (pausa e mapa são usados pelo gerador)
from atividades_parte2 import espelho
from atividades_parte3 import sub
import mapas_atividades as MA

ANTES = "Escreva a sua resposta <strong>antes</strong> de abrir o comentário. Depois compare: o que você acertou, o que faltou?"
PRESENTE = [("sim", "Sim"), ("parte", "Em parte"), ("nao", "Não")]
EFEITO = [("aprofunda", "Aprofunda"), ("neutro", "Neutro (EO)"), ("corroi", "Corrói")]
CLASSES = [("aprofundar", "Aprofundar"), ("estender", "Estender alavancando o sistema"), ("separar", "Ampliar com unidade separada"),
           ("comprometer", "Ampliar comprometendo")]

NOTA_NEUTRO = ('<p class="msa-nota" data-atividade>Mapa didático montado com os fatos que Porter dá nas Partes III, IV e V. Os temas e a maior parte '
               'das ligações são uma leitura nossa. Em amarelo, as renúncias; em vermelho, os movimentos de crescimento da Parte V e as ligações de conflito (X).</p>')

B = {}

B["prep"] = caixa(
    "Antes de ler", "O que a sua empresa acrescentou",
    "Responda antes de ler o texto de Porter. Use a empresa que você vem acompanhando desde a Aula 1 e tenha à mão o mapa que você construiu na Aula 4. "
    "A lista volta nos Blocos 3 e 5.",
    campo("prep_empresa", "Empresa que você acompanha", 1, "Ex.: Vivelar")
    + campo("prep_acrescimos", "Liste o que a empresa acrescentou nos últimos cinco anos: produtos ou serviços, tipos de cliente, canais, regiões, aquisições. "
            "Para cada item, diga quem pediu ou propôs e se ele se liga a algum tema do seu mapa (uma linha por item)", 8,
            "Ex.: linha infantil · proposta do comercial · não se liga a nenhum tema\nVenda pelo aplicativo · pedido dos clientes · liga-se a T1"),
    tipo="Antes de ler")

B["abertura"] = caixa(
    "Abertura", "A sua resposta", "Não existe resposta certa: o objetivo é registrar o ponto de partida.",
    escolha("abertura_hoje", "A estratégia da empresa que você acompanha passaria hoje nas quatro camadas?", PRESENTE)
    + escolha("abertura_antes", "E no passado, ela já passou?", PRESENTE + [("naosei", "Não sei")])
    + campo("abertura_porque", "Se a resposta mudou do passado para hoje, o que aconteceu no meio do caminho? Se não mudou, o que a manteve?", 3))

CAUSAS = [
    "Longe da fronteira, os trade-offs parecem desnecessários",
    "Fazer escolhas é visto como sinal de fraqueza",
    "Imitar tudo dos concorrentes, por medo da hipercompetição",
    "Perseguir toda tecnologia nova por ela mesma",
    "A EO seduz porque é concreta e mensurável",
    "A sabedoria convencional do setor homogeneíza a competição",
    "“Foco no cliente” como atender todos os pedidos",
    "Preservar a flexibilidade",
    "Medo de ser culpado por uma escolha ruim",
    "Comportamento de manada",
    "Funcionários empoderados sem visão do todo",
    "Relutância em desapontar gestores ou funcionários valorizados",
    "O desejo de crescer",
]
B["b1_causas"] = caixa(
    "Bloco 1 · A falha em escolher", "Diagnóstico da falha em escolher",
    "Para cada causa, marque se ela está presente na empresa que você acompanha.",
    '<div class="colunas2">' + "".join(escolha(f"b1_c{k}", f"{k}. {t}", PRESENTE) for k, t in enumerate(CAUSAS, 1)) + "</div>"
    + campo("b1_top3", "As três causas mais fortes, com uma evidência concreta de cada uma", 4)
    + escolha("b1_natureza", "Elas são mais de visão (o que os gestores acreditam) ou de organização (como a empresa decide)?",
              [("visao", "Visão"), ("organizacao", "Organização"), ("as duas", "As duas")]))

B["b2_maytag"] = caixa(
    "Bloco 2 · A armadilha do crescimento", "Faça a conta", ANTES,
    escolha("b2_maytag_lucro", "Entre o período de retorno de 8% a 12% e o pico de receita, o lucro da Maytag…",
            [("cresceu", "Cresceu"), ("parecido", "Ficou parecido"), ("caiu", "Caiu")])
    + campo("b2_maytag_conta", "Mostre a conta (uma ordem de grandeza basta)", 2))

B["b2_ciclo"] = caixa(
    "Bloco 2 · A armadilha do crescimento", "O ciclo numa empresa real", "",
    campo("b2_ciclo", "Você conhece uma empresa que passou, ou está passando, por esse ciclo? Em que etapa ela está, e o que mostra isso?", 3))

B["b3_neutrogena"] = caixa(
    "Bloco 3 · A erosão no mapa", "As renúncias da Neutrogena", ANTES,
    campo("b3_neutrogena", "Quantas das renúncias da Aula 3 sobreviveram aos três movimentos? O que isso diz sobre a proteção da posição?", 3))

B["b3_neutrogena_coment"] = (
    '<details class="revelar" data-atividade><summary><span class="rev-ico" aria-hidden="true">+</span>Ver o comentário</summary>'
    '<div class="revelar-corpo"><p>Pelos fatos de Porter, duas das renúncias da Aula 3 foram desfeitas diretamente: a distribuição concentrada em farmácias '
    'e a recusa a promoções. Com elas, o tema N3 perdeu tudo o que o sustentava. Porter não diz o que aconteceu com a fabricação lenta nem com o sabonete '
    'sem desodorantes e hidratantes, mas a extensão da marca a produtos em que ela não era única dilui a credibilidade médica (N1), que é justamente o que '
    'as renúncias protegiam. A lição: bastaram poucas decisões, cada uma defensável, para derrubar um tema inteiro. A proteção de uma posição dura '
    'enquanto as renúncias forem mantidas.</p></div></details>')

B["b3_acrescimos"] = caixa(
    "Bloco 3 · A erosão no mapa", "Os acréscimos da sua empresa no mapa",
    "A sua lista, escrita antes de ler o texto de Porter:",
    espelho("prep_acrescimos", "Você ainda não escreveu a lista. Ela fica no início do módulo Texto de Porter.")
    + "".join(
        sub(f"Acréscimo {i}")
        + campo(f"b3_a{i}", f"Acréscimo {i}: o item", 1)
        + escolha(f"b3_a{i}_cls", f"Acréscimo {i}: no mapa, ele…", EFEITO)
        + campo(f"b3_a{i}_liga", f"Acréscimo {i}: a que tema, atividade ou renúncia ele se liga, ou contradiz?", 1)
        for i in (1, 2, 3, 4))
    + sub("O que a lista revela")
    + escolha("b3_sinal", "Qual sinal de erosão (seção 3.4) aparece com mais força no mapa da sua empresa?",
              [("orfas", "Órfãs se acumulando"), ("renuncias", "Renúncias desfeitas"), ("tema", "Tema enfraquecido"),
               ("compartilhadas", "Atividades compartilhadas"), ("convergencia", "Convergência"), ("complexidade", "Complexidade sem fit")])
    + campo("b3_quem", "Quem propôs os itens que corroem? Que causas do Bloco 1 estão por trás deles?", 3))

B["b4_extensao"] = caixa(
    "Bloco 4 · Crescimento lucrativo", "A pergunta de Porter na sua empresa", "",
    campo("b4_extensao", "Que atividade, atributo ou forma de competir é viável, ou mais barata, para a sua empresa por causa das atividades que ela já executa? "
          "Um concorrente sem o mesmo sistema conseguiria oferecer o mesmo?", 3))

B["b4_teste"] = caixa(
    "Bloco 4 · Crescimento lucrativo", "Aplique o teste da extensão",
    "Escolha uma opção de crescimento real, em discussão ou possível, da empresa que você acompanha.",
    campo("b4_opcao", "A opção de crescimento", 2)
    + escolha("b4_t1", "1. Alavanca o sistema?", [("sim", "Sim, usa várias atividades do núcleo"), ("parte", "Em parte"), ("nao", "Não")])
    + escolha("b4_t2", "2. Exige atividades incompatíveis com algum tema ou renúncia?", [("sim", "Sim"), ("nao", "Não")])
    + escolha("b4_t3", "3. Um rival sem o nosso sistema conseguiria igualá-la?",
              [("facil", "Sim, ao mesmo custo"), ("caro", "Só a um custo bem maior"), ("nao", "Não")])
    + escolha("b4_t4", "4. Penetra onde a empresa é distinta?", PRESENTE)
    + escolha("b4_t5", "5. Se exige atividades incompatíveis, poderia ser uma unidade separada, com marca e atividades próprias?",
              [("sim", "Sim"), ("nao", "Não"), ("naoaplica", "Não se aplica")])
    + escolha("b4_classe", "Classificação", CLASSES)
    + campo("b4_justifica", "Justifique com o mapa: que nós e ligações a opção usa, reforça ou contradiz?", 3))

B["b5_auditoria"] = caixa(
    "Bloco 5 · Reconectar-se", "A auditoria do núcleo da sua empresa",
    "Onde não houver dados, registre a sua melhor estimativa e o dado que confirmaria a resposta.",
    sub("As cinco perguntas do quadro")
    + campo("b5_q1", "Variedades de produto ou serviço mais distintas", 2)
    + campo("b5_q2", "Variedades mais lucrativas", 2)
    + campo("b5_q3", "Clientes mais satisfeitos", 2)
    + campo("b5_q4", "Clientes, canais e ocasiões de compra mais lucrativos", 2)
    + campo("b5_q5", "Atividades da cadeia de valor mais diferentes e eficazes (e onde elas estão no seu mapa)", 2)
    + campo("b5_concentracao", "Que parcela das vendas e do lucro vem desse núcleo?", 2)
    + sub("A maior craca")
    + espelho("prep_acrescimos", "Você ainda não escreveu a lista de acréscimos. Ela fica no início do módulo Texto de Porter.")
    + campo("b5_craca", "A maior craca da empresa: o que é e por que não se liga ao núcleo", 2)
    + escolha("b5_decisao", "O que fazer com ela?",
              [("vender", "Vender"), ("desaparecer", "Deixar desaparecer"), ("separar", "Separar em unidade própria"), ("naosei", "Ainda não sei")])
    + campo("b5_decisao_porque", "Por quê? Se a craca sair, o que a empresa perde e o que ganha?", 2)
    + sub("A história")
    + campo("b5_historia", "Que produtos e clientes fizeram a empresa? A posição original pode ser executada de forma moderna? Como?", 3))

B["b6_emergentes"] = caixa(
    "Bloco 6 · Setores emergentes", "Treine o olhar", "",
    campo("b6_emergentes", "No seu setor, ou em negócios em torno da IA, que empresa já está definindo uma posição com trade-offs, e qual está apenas "
          "acrescentando todos os atributos possíveis? Que renúncia ou atividade mostra a diferença?", 4))

AGENDAS = [
    (1, "Adotar roteirização com IA nas entregas"),
    (2, "Decidir não atender as grandes redes com condições especiais"),
    (3, "Reduzir o prazo de fechamento contábil"),
    (4, "Manter a visita semanal aos independentes, mesmo que custe mais"),
    (5, "Fazer benchmarking do processo de cobrança"),
    (6, "Recusar uma linha corporal para supermercados"),
]
B["b7_agendas"] = caixa(
    "Bloco 7 · Liderança e duas agendas", "Qual agenda?", ANTES,
    "".join(escolha(f"b7_ag{k}", f"{k}. {t}", [("operacional", "Operacional"), ("estrategica", "Estratégica")]) for k, t in AGENDAS))

B["b7_agendas_coment"] = (
    '<details class="revelar" data-atividade><summary><span class="rev-ico" aria-hidden="true">+</span>Ver o comentário</summary>'
    '<div class="revelar-corpo"><p><strong>Operacionais:</strong> 1, 3 e 5. São melhorias onde não há trade-off: qualquer concorrente pode fazê-las, '
    'e deixar de fazê-las cria vulnerabilidade. A roteirização com IA reforça uma ligação do mapa da Vivelar (Aula 4), mas continua sendo EO a serviço do sistema.</p>'
    '<p><strong>Estratégicas:</strong> 2, 4 e 6. São escolhas sobre o que fazer e o que não fazer, que só se justificam pela posição. Repare que a 4 '
    'parece operacional (é sobre a frequência de visitas), mas é uma decisão de manter o sistema contra a pressão por custo: cabe à direção, '
    'não à melhoria contínua.</p></div></details>')

B["b7_lider"] = caixa(
    "Bloco 7 · Liderança e duas agendas", "A liderança na sua empresa", "",
    campo("b7_tempo", "Em que a liderança da empresa que você acompanha gasta mais tempo: orquestrar melhorias e fechar negócios, ou definir, comunicar e proteger a posição? Dê um exemplo.", 3)
    + campo("b7_nao", "Quando foi a última vez que um líder dessa empresa disse não a algo atraente em nome da estratégia? Como isso foi comunicado?", 3))

for n in range(1, 5):
    B[f"b8_duvida{n}"] = caixa(
        "Bloco 8 · Dúvidas comuns", f"Dúvida {n}: sua resposta",
        "Antes de abrir o comentário, responda com o que você entendeu da Parte V.",
        campo(f"b8_duvida{n}", f"Dúvida {n}: minha resposta antes de ler", 3, mostrar_rotulo=False))

B["b9_reuniao"] = caixa(
    "Bloco 9 · Execução e BSC", "Onde a estratégia é discutida?", "",
    campo("b9_reuniao", "Na empresa que você acompanha, a estratégia e o resultado do mês são discutidos na mesma reunião? O que você mudaria?", 3))

B["b9_maytag"] = caixa(
    "Bloco 9 · Execução e BSC", "Um alerta para a Maytag", "",
    campo("b9_maytag", "Qual indicador de deriva teria alertado a Maytag mais cedo? Por quê?", 3))

PROPOSTAS = [(1, "Novos independentes do Sudeste"), (2, "Item complementar da rotina facial"), (3, "A mesma posição no Sul"),
             (4, "Tabloides das grandes redes"), (5, "Linha corporal para supermercados"), (6, "Marca de massa com a mesma equipe"),
             (7, "Comércio eletrônico próprio")]
B["b9_vivelar"] = caixa(
    "Bloco 9 · Execução e BSC", "As sete propostas da Vivelar", ANTES,
    "".join(escolha(f"b9_p{k}", f"Proposta {k} ({t})", CLASSES + [("depende", "Depende do desenho")]) for k, t in PROPOSTAS)
    + campo("b9_primeira", "Qual proposta você recomendaria primeiro à diretoria? Justifique com o mapa da Vivelar (Aula 4)", 3)
    + campo("b9_p2_cond", "Que condições fariam a proposta 2 passar no teste da extensão? Como saber se o produto é distinto?", 3))

B["b9_aplicar"] = caixa(
    "Bloco 9 · Execução e BSC", "Leve a Parte V para a gestão",
    "As causas mais fortes que você apontou no Bloco 1:",
    espelho("b1_top3", "Você ainda não apontou as causas mais fortes. A pergunta fica no Bloco 1, em 1.4.")
    + campo("b9_mecanismo", "Para a causa mais forte, que mecanismo de execução da seção 9.2 você adotaria primeiro? Quem seria o dono?", 3)
    + sub("Um indicador de deriva por perspectiva")
    + '<div class="colunas2">'
    + campo("b9_der_fin", "Financeira", 2)
    + campo("b9_der_cli", "Clientes", 2)
    + campo("b9_der_proc", "Processos internos", 2)
    + campo("b9_der_apr", "Aprendizado e crescimento", 2)
    + "</div>")

SINTESE = [
    "A maior ameaça à estratégia costuma vir de dentro.",
    "A armadilha do crescimento é feita de passos sensatos que, somados, borram a posição.",
    "O sistema de atividades torna a erosão visível.",
    "Crescer com lucro é aprofundar, não ampliar.",
    "Reconectar-se é encontrar o núcleo de singularidade e remover as cracas.",
    "A estratégia depende da liderança e da separação entre as duas agendas.",
]
B["sintese"] = caixa(
    "Fechamento", "Consigo explicar com minhas palavras?",
    "Marque as ideias que você seria capaz de explicar a um colega sem consultar o texto. As que ficarem sem marca indicam o que reler.",
    '<div class="checks">' + "".join(
        f'<label class="check"><input type="checkbox" data-campo="sintese_{k}" data-rotulo="{E(t)}"><span>{k}. {E(t)}</span></label>'
        for k, t in enumerate(SINTESE, 1)) + "</div>")

B["exit"] = caixa(
    "Fechamento · Exit ticket", "Exit ticket", "A estratégia da empresa que você acompanhou ao longo do ciclo, em cinco respostas curtas.",
    campo("exit_posicao", "A posição, em uma frase", 2)
    + campo("exit_renuncias", "Duas renúncias", 2)
    + campo("exit_tema", "O tema mais importante do mapa", 1)
    + campo("exit_ameaca", "A principal ameaça interna", 2)
    + campo("exit_deriva", "O indicador de deriva que você colocaria no BSC", 2)
    + campo("exit_mudou", "O que mudou na sua leitura da empresa entre a Aula 1 e agora?", 3))

B["mapa_volta"] = P1.B["mapa_volta"]


def bloco(chave):
    return B[chave]


# ---------------------------------------------------------------- esquema: o ciclo da armadilha do crescimento
def _borda(c, alvo):
    """Ponto em que a reta do centro de c até alvo sai do retângulo c (x, y, largura, altura)."""
    x, y, w, h = c
    dx, dy = alvo[0] - x, alvo[1] - y
    t = min((w / 2 + 6) / abs(dx) if dx else 9e9, (h / 2 + 6) / abs(dy) if dy else 9e9)
    return x + dx * t, y + dy * t


def _ciclo():
    # caixas: id -> (x, y, largura, altura, linhas, classe)
    C = {
        "P": (112, 62, 176, 50, ["Pressão por crescer"], "cic-entrada"),
        "A": (352, 62, 214, 58, ["Passos incrementais que", "ultrapassam os limites"], "cic-no"),
        "B": (548, 182, 180, 58, ["Concessões e", "inconsistências"], "cic-no"),
        "C": (540, 330, 196, 58, ["A vantagem original", "se corrói"], "cic-no"),
        "D": (262, 412, 168, 50, ["Os lucros caem"], "cic-no"),
        "E": (122, 246, 190, 58, ["Mais receita vira", "a solução"], "cic-no"),
        "X": (522, 492, 252, 58, ["Fusão ou enxugamento de", "volta à posição original"], "cic-saida"),
    }
    setas = [("P", "A", "cic-s-entrada"), ("A", "B", "cic-s"), ("B", "C", "cic-s"), ("C", "D", "cic-s"),
             ("D", "E", "cic-s"), ("E", "A", "cic-s"), ("D", "X", "cic-s-saida")]
    f = lambda v: f"{v:.0f}"  # noqa: E731
    lin = []
    for a, b, cl in setas:
        ca, cb = C[a], C[b]
        p, q = _borda(ca[:4], cb[:2]), _borda(cb[:4], ca[:2])
        lin.append(f'<line class="{cl}" x1="{f(p[0])}" y1="{f(p[1])}" x2="{f(q[0])}" y2="{f(q[1])}" marker-end="url(#{cl}-ponta)"/>')
    nos = []
    for k, (x, y, w, h, linhas, cl) in C.items():
        y0 = y - (len(linhas) - 1) * 9
        tsp = "".join(f'<tspan x="{x}" y="{y0 + i * 18:.0f}">{E(t)}</tspan>' for i, t in enumerate(linhas))
        nos.append(f'<g class="{cl}"><rect x="{f(x - w / 2)}" y="{f(y - h / 2)}" width="{w}" height="{h}" rx="12"/>'
                   f'<text text-anchor="middle" dominant-baseline="central">{tsp}</text></g>')
    marcas = "".join(
        f'<marker id="{cl}-ponta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        f'<path class="{cl}-p" d="M0 0 L10 5 L0 10 z"/></marker>' for cl in ("cic-s", "cic-s-entrada", "cic-s-saida"))
    centro = math.floor((62 + 412) / 2)
    return f"""<figure class="esquema esquema-ciclo" data-atividade>
<svg viewBox="0 0 660 532" role="img" aria-label="O ciclo da armadilha do crescimento: a pressão por crescer leva a passos incrementais que ultrapassam os limites; eles geram concessões e inconsistências; a vantagem original se corrói; os lucros caem; mais receita vira a solução, o que leva a novos passos incrementais. O ciclo só costuma ser quebrado pelo desespero, com uma fusão ou um enxugamento de volta à posição original.">
  <defs>{marcas}</defs>
  <text x="340" y="{centro - 8}" text-anchor="middle" class="cic-centro">o ciclo se</text>
  <text x="340" y="{centro + 12}" text-anchor="middle" class="cic-centro">autoalimenta</text>
  {"".join(lin)}
  {"".join(nos)}
  <text x="410" y="430" class="cic-rot">o desespero quebra o ciclo</text>
</svg>
<figcaption class="esq-legenda"><span><i class="lg-cic"></i>O ciclo descrito por Porter (p. 52)</span><span><i class="lg-cic-saida"></i>A saída mais comum: fusão ou enxugamento</span></figcaption>
</figure>"""


def visual(nome):
    if nome == "ciclo":
        return _ciclo()
    if nome == "neutrogena":
        ordem = [("neutrogena", "Antes: a posição original"), ("neutrogena_depois", "Depois: os movimentos da Parte V")]
        botoes = "".join(f'<button type="button" class="msa-aba" role="tab" aria-selected="{"true" if i == 0 else "false"}">{E(t)}</button>'
                         for i, (_, t) in enumerate(ordem))
        figs = [MA.figura(n) for n, _ in ordem]
        figs = [f.replace('<figure class="msa"', '<figure class="msa" hidden', 1) if i else f for i, f in enumerate(figs)]
        return (f'<div class="msa-abas" data-atividade><div class="msa-abas-botoes" role="tablist" aria-label="A Neutrogena antes e depois">{botoes}</div>'
                f'{"".join(figs)}{NOTA_NEUTRO}</div>')
    return ""


MODULOS = [
    ("Mapa de aprendizagem", "Diagnóstico", "Mapa de aprendizagem", "Marque o que você já domina e volte aqui no fim da aula."),
    ("Texto de Porter", "Leitura", "Texto de Porter (Parte V)", "Tradução da Parte V e dos dois quadros, com destaques, anotações e pausas para responder."),
    ("Abertura", "Abertura", "Por que tão poucas têm estratégia?", "As quatro camadas da definição e a sua empresa, hoje e no passado."),
    ("Bloco 1", "Bloco 1", "A falha em escolher", "Por que a maior ameaça vem de dentro, e as causas na sua empresa."),
    ("Bloco 2", "Bloco 2", "A armadilha do crescimento", "Maytag, Neutrogena e o ciclo que se autoalimenta."),
    ("Bloco 3", "Bloco 3", "A erosão no mapa", "O que cada movimento de crescimento faz com o sistema de atividades."),
    ("Bloco 4", "Bloco 4", "Crescimento lucrativo", "Aprofundar, e não ampliar: Carmike, extensões e o teste da extensão."),
    ("Bloco 5", "Bloco 5", "Reconectar-se com a estratégia", "O núcleo de singularidade, as cracas e a auditoria da sua empresa."),
    ("Bloco 6", "Bloco 6", "Setores emergentes", "Incerteza, imitação e a vantagem de definir a posição cedo."),
    ("Bloco 7", "Bloco 7", "Liderança e duas agendas", "O papel do líder, a agenda operacional e a estratégica."),
    ("Bloco 8", "Bloco 8", "Dúvidas comuns", "Quatro dúvidas frequentes: responda antes de ler o comentário."),
    ("Bloco 9", "Bloco 9", "Execução e BSC", "Indicadores de deriva, governança do crescimento e a Vivelar 18 meses depois."),
    ("Fechamento", "Fechamento", "Síntese e exit ticket", "Seis ideias, o ciclo em uma tabela, exit ticket e revisão do mapa."),
    ("Para consulta", "Consulta", "Para consulta", "Os casos em um quadro, armadilhas comuns e referências."),
]


def info_modulo(titulo):
    for prefixo, tipo, curto, desc in MODULOS:
        if titulo.startswith(prefixo):
            return {"tipo": tipo, "curto": curto, "desc": desc}
    return {"tipo": "Módulo", "curto": titulo, "desc": ""}


REGRAS = [
    ("Mapa de aprendizagem", {"mapa": True}),
    ("Uma pergunta sobre a sua empresa", {"fim": ["abertura"]}),
    ("1.4 As causas na sua empresa", {"apos_bloco": [("Marque, na atividade abaixo", ["b1_causas"])]}),
    ("2.3 Caso Maytag", {"antes_revelar": ["b2_maytag"]}),
    ("2.5 O ciclo da armadilha", {"fim": ["b2_ciclo"]}),
    ("3.3 A Neutrogena antes e depois", {"fim": ["b3_neutrogena", "b3_neutrogena_coment"]}),
    ("3.5 Os acréscimos", {"fim": ["b3_acrescimos"]}),
    ("4.3 Extensões", {"fim": ["b4_extensao"]}),
    ("4.5 O teste da extensão", {"fim": ["b4_teste"]}),
    ("5.5 A auditoria do núcleo", {"fim": ["b5_auditoria"]}),
    ("6.3 Ponte com hoje", {"fim": ["b6_emergentes"]}),
    ("7.3 As duas agendas", {"fim": ["b7_agendas", "b7_agendas_coment"]}),
    ("7.2 O que o líder faz", {"fim": ["b7_lider"]}),
    ("Dúvida 1:", {"apos_titulo": ["b8_duvida1"], "recolher": True}),
    ("Dúvida 2:", {"apos_titulo": ["b8_duvida2"], "recolher": True}),
    ("Dúvida 3:", {"apos_titulo": ["b8_duvida3"], "recolher": True}),
    ("Dúvida 4:", {"apos_titulo": ["b8_duvida4"], "recolher": True}),
    ("9.3 Separar as duas agendas", {"fim": ["b9_reuniao"]}),
    ("9.4 Indicadores de deriva", {"fim": ["b9_maytag"]}),
    ("9.6 O caso Vivelar", {"antes_revelar": ["b9_vivelar"]}),
    ("9.9 Aplique", {"fim": ["b9_aplicar"]}),
    ("Síntese da Parte V", {"fim": ["sintese"]}),
    ("Exit ticket", {"fim": ["exit", "mapa_volta"]}),
]


def _modelo():
    m = P1.MODELO
    trocas = [
        ('<div class="sidebar-badge"><span class="dot"></span><span>Aula {{n}} · Parte I</span></div>',
         '<div class="sidebar-badge"><span class="dot"></span><span>Aula {{n}} · Parte V</span></div>'),
        ('<div class="sidebar-title">Eficácia operacional não é estratégia</div>',
         '<div class="sidebar-title">Redescobrindo a estratégia</div>'),
        ("Aula {{n}} · Parte I do artigo · pp. 37–40", "Aula {{n}} · Parte V do artigo · pp. 50–54"),
        ("titulo: 'Aula {{n}} · Parte I: Eficácia operacional não é estratégia', crumb: 'Aula {{n}} · Parte I'",
         "titulo: 'Aula {{n}} · Parte V: Redescobrindo a estratégia', crumb: 'Aula {{n}} · Parte V'"),
        ('<script src="../assets/js/parte.js"></script>',
         '<script src="../assets/js/mapas.js"></script>\n<script src="../assets/js/parte.js"></script>'),
    ]
    for a, b in trocas:
        assert m.count(a) == 1, a
        m = m.replace(a, b)
    return m


MODELO = _modelo()
