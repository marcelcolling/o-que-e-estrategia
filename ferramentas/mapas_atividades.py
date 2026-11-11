"""
Mapas de sistemas de atividades da Aula 4: os três de Porter (Ikea, Vanguard, Southwest), redesenhados
com os rótulos traduzidos, e o da Vivelar (construção didática da aula). Da Aula 5: a Neutrogena antes e depois
dos movimentos de crescimento da Parte V (construção didática com os fatos de Porter; "conflitos" são ligações X).

Os nós e as ligações dos mapas de Porter foram traçados um a um a partir das figuras das pp. 47–49. A posição
dos nós foi refeita para evitar cruzamentos; a topologia (quem se liga a quem) é a do original.

Uso:
    python ferramentas/mapas_atividades.py     confere os mapas: nós sobrepostos, linha passando por cima de um
                                               nó que não é o dela, nó solto e número de cruzamentos.

Texto do nó: "|" separa as linhas. Categorias (cores e botões de destaque, leitura nossa, não de Porter):
    ren = renúncias e limites · pes = pessoas e incentivos · cli = o cliente executa ou é educado
    nuc = núcleo (ligada a dois ou mais temas) · gen = genérica na técnica (só no mapa da Vivelar)
    mov = movimento de crescimento da Parte V (só no mapa da Neutrogena depois)
"""
import html
import math

E = lambda s: html.escape(s, quote=True)  # noqa: E731

CATEGORIAS = {
    "ren": ("Renúncias e limites", "O que a empresa deliberadamente não faz ou limita."),
    "pes": ("Pessoas e incentivos", "Gestão de pessoas dentro do sistema."),
    "cli": ("Atividades do cliente", "O cliente executa a atividade ou é educado para agir de certo jeito."),
    "nuc": ("Núcleo", "Atividades ligadas a dois ou mais temas: as mais difíceis de copiar."),
    "gen": ("Genéricas na técnica", "Ferramentas e práticas que qualquer concorrente pode adotar."),
    "mov": ("Movimentos de crescimento", "O que a Neutrogena fez no início dos anos 1990, segundo a Parte V."),
}

TIPOS = {"C": "Consistência", "R": "Reforço", "O": "Otimização"}

# nó: id -> (tipo, texto, x, y, categorias). tipo: "T" = tema, "A" = atividade
IKEA = {
    "titulo": "Sistema de atividades da Ikea",
    "W": 1180, "H": 760,
    "nos": {
        "LS": ("T", "Serviço limitado|ao cliente", 400, 300, ""),
        "SS": ("T", "Autosseleção|pelo cliente", 830, 300, ""),
        "MD": ("T", "Projeto modular|dos móveis", 400, 595, ""),
        "LC": ("T", "Custo baixo|de fabricação", 830, 595, ""),
        "EX": ("A", "Catálogos explicativos,|expositores e etiquetas|informativos", 430, 170, "cli"),
        "ST": ("A", "Transporte feito|pelo cliente", 185, 60, "cli"),
        "SU": ("A", "Lojas em subúrbios,|com amplo|estacionamento", 640, 65, ""),
        "HT": ("A", "Layout de loja com|grande circulação", 860, 65, ""),
        "IB": ("A", "Mais compras|por impulso", 1085, 65, ""),
        "EA": ("A", "Facilidade de|transporte|e montagem", 85, 405, ""),
        "LE": ("A", "Equipe de vendas|reduzida", 620, 385, "ren"),
        "SA": ("A", "Montagem feita|pelo cliente", 400, 450, "cli"),
        "AI": ("A", "Amplo estoque|no local", 830, 450, ""),
        "MI": ("A", "Maioria dos itens|em estoque", 1085, 300, ""),
        "KD": ("A", "Embalagem em|kit desmontado", 90, 570, ""),
        "IL": ("A", "Maior probabilidade|de compra futura", 620, 495, ""),
        "YR": ("A", "Estoque|o ano inteiro", 1085, 485, ""),
        "WV": ("A", "Grande variedade|com fabricação fácil", 180, 705, ""),
        "IH": ("A", "Projeto interno voltado|ao custo de fabricação", 620, 705, ""),
        "SO": ("A", "100% do fornecimento|por fornecedores|de longo prazo", 1075, 690, ""),
    },
    "grossas": ["LS-SS", "MD-LC"],
    "finas": ["EX-LS", "ST-LS", "ST-SU", "ST-EA", "SU-HT", "SU-SS", "HT-IB", "IB-MI", "LS-LE", "LE-SS", "LS-SA", "SA-MD",
              "EA-SA", "EA-MD", "EA-KD", "KD-MD", "KD-WV", "WV-MD", "MD-IL", "IL-SS", "MD-IH", "IH-LC", "SS-AI", "AI-LC",
              "SS-MI", "MI-AI", "AI-YR", "MI-YR", "YR-SO", "LC-SO"],
}

VANGUARD = {
    "titulo": "Sistema de atividades da Vanguard",
    "W": 1285, "H": 1040,
    "nos": {
        "BA": ("T", "Ampla gama de fundos|mútuos, excluindo|algumas categorias", 627, 330, ""),
        "VL": ("T", "Despesas muito baixas|repassadas ao cliente", 240, 360, ""),
        "EI": ("T", "Gestão eficiente dos|investimentos, com|desempenho bom|e consistente", 1015, 360, ""),
        "SC": ("T", "Controle rigoroso|de custos", 627, 640, ""),
        "DD": ("T", "Distribuição|direta", 240, 860, ""),
        "CC": ("T", "Comunicação e educação|simples do cliente", 1015, 860, ""),
        "WS": ("A", "Cautela com fundos|de pequenas empresas|de crescimento", 435, 225, "ren"),
        "LI": ("A", "Poucos fundos|internacionais, por|volatilidade e|custo alto", 815, 225, "ren"),
        "RF": ("A", "Taxas de resgate|para desestimular|negociações", 1140, 200, "cli"),
        "EB": ("A", "Bônus dos|funcionários ligados|à economia de custos", 432, 625, "pes"),
        "NL": ("A", "Sem taxa|de entrada|(no-load)", 433, 500, "ren"),
        "IH": ("A", "Gestão interna|dos fundos-padrão", 750, 460, ""),
        "EM": ("A", "Ênfase em renda|fixa e fundos|de índice", 1205, 395, ""),
        "LR": ("A", "Taxa muito|baixa de|negociação", 895, 535, ""),
        "SE": ("A", "Educação do|cotista, com alerta|sobre riscos", 1175, 565, "cli"),
        "LT": ("A", "Incentivo ao|investimento de|longo prazo", 935, 705, "cli"),
        "NB": ("A", "Sem relações|com corretoras", 85, 690, "ren"),
        "MC": ("A", "Sem mudanças|de marketing", 335, 725, "ren"),
        "FC": ("A", "Executivos não|viajam de|primeira classe", 745, 810, "ren"),
        "NC": ("A", "Sem comissões|a corretores ou|distribuidores", 84, 880, "ren"),
        "OL": ("A", "Acesso a|informações|on-line", 1190, 735, ""),
        "TR": ("A", "Só três pontos|de venda físicos", 540, 775, "ren"),
        "AD": ("A", "Verba de|propaganda limitada", 627, 945, "ren"),
        "WM": ("A", "Apoio na recomendação|boca a boca", 835, 1000, ""),
        "VP": ("A", "A Vanguard divulga|ativamente sua filosofia", 1125, 1000, ""),
    },
    # VL-EI passa por cima do tema da ampla gama, num arco: assim as ligações entre temas não se cruzam
    "curvas": {"VL-EI": ("arco", -25)},
    "grossas": ["BA-VL", "BA-EI", "BA-SC", "VL-EI", "VL-DD", "EI-SC", "EI-CC", "SC-DD", "SC-CC", "VL-NL", "NL-SC"],
    "finas": ["WS-BA", "BA-LI", "LI-EI", "RF-EI", "EI-EM", "EI-SE", "EI-LT", "EI-LR", "EI-IH", "IH-SC", "LR-SC", "EB-VL", "EB-SC",
              "VL-MC", "NB-MC", "NB-DD", "NB-NC", "NC-DD", "MC-AD", "SC-FC", "SC-AD", "SC-TR", "DD-AD", "DD-TR", "AD-CC", "CC-LT",
              "CC-SE", "CC-OL", "CC-WM", "CC-VP", "WM-VP"],
}

SOUTHWEST = {
    "titulo": "Sistema de atividades da Southwest Airlines",
    "W": 1190, "H": 820,
    "nos": {
        "LP": ("T", "Serviço limitado|ao passageiro", 590, 185, ""),
        "FD": ("T", "Partidas frequentes|e confiáveis", 130, 345, ""),
        "LE": ("T", "Equipes de solo e de|portão enxutas e|muito produtivas", 300, 570, ""),
        "VT": ("T", "Tarifas|muito baixas", 880, 570, ""),
        "HU": ("T", "Alta utilização|dos aviões", 590, 760, ""),
        "SH": ("T", "Rotas curtas, ponto|a ponto, entre cidades|médias e aeroportos|secundários", 1062, 380, ""),
        "NM": ("A", "Sem refeições", 390, 60, "ren"),
        "NS": ("A", "Sem marcação|de assentos", 225, 175, "ren"),
        "NB": ("A", "Sem transferência|de bagagem", 790, 60, "ren"),
        "NO": ("A", "Sem conexões com|outras companhias", 975, 165, "ren"),
        "T1": ("A", "Rotação de|15 minutos|no portão", 345, 375, ""),
        "LU": ("A", "Uso limitado de|agentes de viagem", 590, 325, "ren"),
        "SF": ("A", "Frota padronizada|de Boeing 737", 845, 375, ""),
        "AT": ("A", "Máquinas|automáticas de|emissão de|passagens", 590, 450, "cli"),
        "HC": ("A", "Alta remuneração|dos funcionários", 90, 525, "pes"),
        "FU": ("A", "Contratos sindicais|flexíveis", 100, 685, "pes"),
        "ES": ("A", "Alta participação|acionária dos|funcionários", 300, 760, "pes"),
        "SB": ("A", "“Southwest,|a companhia de|tarifas baixas”", 1050, 760, ""),
    },
    "grossas": ["LP-FD", "LP-LE", "LP-VT", "LP-SH", "FD-LE", "LE-VT", "LE-HU", "VT-HU", "VT-SH"],
    "finas": ["NM-LP", "NS-LP", "LP-NB", "LP-NO", "NB-NO", "NO-SH", "LP-T1", "FD-T1", "T1-LE", "T1-SF", "LP-LU", "LU-AT", "AT-HU", "AT-LE",
              "LU-VT", "SF-SH", "SF-VT", "HC-LE", "FU-LE", "ES-LE", "SH-SB", "VT-SB"],
}

# Vivelar: construção didática. As ligações tipadas têm frase e, quando faz sentido, direção (a -> b).
VIVELAR = {
    "titulo": "Sistema de atividades da Vivelar",
    "W": 1272, "H": 950,
    "nos": {
        "T1": ("T", "T1|Reposição frequente|em lote pequeno", 620, 520, ""),
        "T2": ("T", "T2|Preço estável e margem|protegida ao lojista", 945, 205, ""),
        "T3": ("T", "T3|Venda puxada pela|recomendação no balcão", 290, 205, ""),
        "T4": ("T", "T4|Custo de servir controlado|em clientes pequenos|e dispersos", 620, 870, ""),
        "A1": ("A", "A1 Equipe dedicada,|com visita semanal", 125, 470, "nuc"),
        "A2": ("A", "A2 Pedido mínimo|baixo", 1045, 705, ""),
        "A3": ("A", "A3 Rotas agrupadas|por microrregião", 180, 705, "gen"),
        "A4": ("A", "A4 Entrega semanal|consolidada", 430, 695, "nuc"),
        "A5": ("A", "A5 Pedido sugerido|pelo giro do PDV", 1160, 575, "gen"),
        "A6": ("A", "A6 Sortimento enxuto,|ajustado a cada PDV", 790, 705, "nuc"),
        "A7": ("A", "A7 Preço sugerido|estável e comunicado", 1165, 210, ""),
        "A8": ("A", "A8 Não financiar tabloides|nem pagar espaço nas redes", 890, 60, "ren"),
        "A9": ("A", "A9 Não fazer promoção-|relâmpago nos|independentes", 1120, 335, "ren"),
        "A10": ("A", "A10 Não vender grandes|lotes a distribuidores", 1155, 75, "ren"),
        "A11": ("A", "A11 Treinamento|do balcão, na|visita", 345, 420, "gen"),
        "A12": ("A", "A12 Expositor de|balcão, com guia|de orientação", 85, 58, "gen"),
        "A13": ("A", "A13 Incentivo ao|atendente por|sell-out", 480, 62, "pes"),
        "A14": ("A", "A14 Relatório de giro|ao lojista", 862, 420, "nuc"),
        "A15": ("A", "A15 Variável do|representante por|sell-out e ruptura", 720, 285, "nuc pes"),
        "A16": ("A", "A16 Certificação|em gestão de|categoria", 530, 310, "pes"),
        "A17": ("A", "A17 Aplicativo do|representante", 1095, 440, "gen"),
    },
    # membros: atividade <-> tema (linha clara, sem frase)
    "finas": ["A1-T1", "A1-T3", "A2-T1", "A3-T4", "A4-T1", "A4-T4", "A5-T1", "A6-T1", "A6-T4", "A7-T2", "A8-T2", "A9-T2", "A10-T2",
              "A14-T1", "A14-T2", "A15-T1", "A15-T2", "A15-T3", "A16-T3", "A17-T1"],
    "grossas": [],
    "sinais": {"T1-T3": 0.72, "T3-T2": 0.74, "A13-A15": 0.3, "T2-T1": 0.62, "A16-A14": 0.55, "A8-A7": 0.72},
    # ligações tipadas: (de, para, tipo, frase, seta?)
    "tipadas": [
        ("A1", "A11", "O", "A mesma visita semanal faz o pedido e o treinamento, sem deslocamento dedicado ao treinamento.", True),
        ("A17", "A5", "R", "Os dados de giro registrados tornam o pedido sugerido preciso.", True),
        ("A17", "A14", "O", "Os mesmos dados alimentam o relatório da categoria, sem coleta duplicada.", True),
        ("A5", "A2", "R", "O pedido sugerido preciso torna o lote pequeno viável sem ruptura.", True),
        ("A6", "A2", "R", "O sortimento enxuto concentra o pedido pequeno nos itens que giram.", True),
        ("A14", "A6", "R", "O relatório de giro justifica ao lojista o sortimento enxuto.", True),
        ("A3", "A4", "O", "A densidade por microrregião reduz o custo de cada entrega semanal.", True),
        ("A1", "A3", "C", "Visita e entrega seguem a mesma lógica de microrregião.", False),
        ("A8", "A7", "R", "Não financiar promoções nas redes torna crível a promessa de preço estável.", True),
        ("A9", "A7", "C", "Sem promoção-relâmpago, a promessa de preço estável se mantém.", True),
        ("A10", "A7", "R", "Sem lotes com desconto a distribuidores, não surge um preço paralelo que mine a promessa.", True),
        ("A11", "T3", "R", "Treinamento, expositor e incentivo juntos geram mais recomendação do que cada um sozinho.", True),
        ("A12", "T3", "R", "Treinamento, expositor e incentivo juntos geram mais recomendação do que cada um sozinho.", True),
        ("A13", "T3", "R", "Treinamento, expositor e incentivo juntos geram mais recomendação do que cada um sozinho.", True),
        ("A13", "A15", "C", "Atendente e representante são remunerados pela mesma coisa: venda ao consumidor.", False),
        ("A16", "A11", "R", "O representante certificado treina melhor.", True),
        ("A16", "A14", "R", "O representante certificado faz uma gestão de categoria melhor.", True),
        ("T3", "T2", "R", "Se a venda é puxada pela recomendação, a empresa não precisa empurrar volume com desconto.", True),
        ("T2", "T1", "R", "Sem promoções, o lojista não precisa estocar para aproveitar descontos, e o lote pequeno faz sentido.", True),
        ("T4", "T1", "C", "O custo de servir controlado é o que torna viável a reposição frequente em lote pequeno.", True),
        ("T1", "T3", "R", "A visita frequente cria a oportunidade de treinar o balcão.", True),
    ],
}

# ---------------------------------------------------------------- Aula 5: a Neutrogena antes e depois (fatos das Partes III, IV e V)
_NEUTRO_BASE = {
    "N1": ("T", "N1|Credibilidade médica", 560, 290, ""),
    "N2": ("T", "N2|Produto suave,|fiel ao conceito", 230, 470, ""),
    "N3": ("T", "N3|Canal farmácia com|preço sustentado", 890, 470, ""),
    "PR": ("A", "Propagandistas|visitando|dermatologistas", 380, 90, ""),
    "AN": ("A", "Revistas médicas,|mala direta e|congressos", 740, 90, ""),
    "HO": ("A", "Hotéis sofisticados,|com a embalagem|da marca", 1000, 220, ""),
    "SI": ("A", "Pesquisa no|próprio instituto", 250, 290, ""),
    "FL": ("A", "Fabricação lenta|e mais cara", 110, 610, "ren"),
    "ND": ("A", "Não acrescentar|desodorantes e|hidratantes", 380, 610, "ren"),
}
_NEUTRO_FINAS = ["PR-N1", "AN-N1", "HO-N1", "HO-AN", "SI-N1", "SI-N2", "FL-N2", "ND-N2"]

NEUTROGENA = {
    "titulo": "Neutrogena: a posição original",
    "W": 1120, "H": 680,
    "nos": dict(_NEUTRO_BASE, **{
        "FA": ("A", "Distribuição|concentrada|em farmácias", 760, 610, "ren"),
        "NP": ("A", "Sem promoções|de preço", 1010, 610, "ren"),
    }),
    "grossas": ["N1-N2", "N1-N3"],
    "finas": _NEUTRO_FINAS + ["FA-N3", "NP-N3"],
}

NEUTROGENA_DEPOIS = {
    "titulo": "Neutrogena: depois dos movimentos de crescimento",
    "W": 1120, "H": 680,
    "nos": dict(_NEUTRO_BASE, **{
        "VM": ("A", "Varejistas de massa|(como o Wal-Mart)", 760, 610, "mov"),
        "PP": ("A", "Promoções|de preço", 1030, 340, "mov"),
        "DX": ("A", "Demaquilante, xampu|e outros produtos em|que não era única", 560, 545, "mov"),
    }),
    "grossas": ["N1-N2", "N1-N3"],
    "finas": _NEUTRO_FINAS,
    # ligações de conflito: (de, para, frase)
    "conflitos": [
        ("VM", "N3", "O canal de massa contradiz a distribuição concentrada em farmácias."),
        ("PP", "N3", "As promoções desfazem a renúncia que sustentava o preço."),
        ("PP", "N1", "Promoção de preço não combina com a imagem de produto recomendado por médicos."),
        ("DX", "N1", "Produtos em que a marca não era única diluem a credibilidade."),
    ],
}

MAPAS = {"ikea": IKEA, "vanguard": VANGUARD, "southwest": SOUTHWEST, "vivelar": VIVELAR,
         "neutrogena": NEUTROGENA, "neutrogena_depois": NEUTROGENA_DEPOIS}


# ---------------------------------------------------------------- geometria
def tam_no(tipo, texto):
    """(largura, altura) estimadas a partir do texto. As fontes são Inter (15,5px) e Inter negrito (16px)."""
    linhas = texto.split("|")
    if tipo == "T":
        return max(len(x) for x in linhas) * 8.7 + 40, len(linhas) * 21 + 26
    return max(len(x) for x in linhas) * 8.05 + 28, len(linhas) * 19.5 + 16


def _caixas(m):
    return {k: (n[2], n[3], *tam_no(n[0], n[1])) for k, n in m["nos"].items()}


def _pares(m):
    """Lista de arestas [(a, b, classe, tipo, frase, seta)]."""
    out = []
    for a in m.get("finas", []):
        x, y = a.split("-")
        out.append((x, y, "fina", "", "", False))
    for a in m.get("grossas", []):
        x, y = a.split("-")
        out.append((x, y, "grossa", "", "", False))
    for de, para, tipo, frase, seta in m.get("tipadas", []):
        out.append((de, para, "tipada", tipo, frase, seta))
    for de, para, frase in m.get("conflitos", []):
        out.append((de, para, "conflito", "X", frase, False))
    return out


def _curva(m, a, b):
    return m.get("curvas", {}).get(f"{a}-{b}", m.get("curvas", {}).get(f"{b}-{a}"))


def _ctrl(m, a, b):
    """Ponto de controle de uma ligação com curva simples, ou None."""
    cv = _curva(m, a, b)
    if cv is None or isinstance(cv, tuple):
        return None
    (x1, y1), (x2, y2) = m["nos"][a][2:4], m["nos"][b][2:4]
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    return (x1 + x2) / 2 + (-dy / L) * cv, (y1 + y2) / 2 + (dx / L) * cv


def _bordas(c, de_fora):
    """Ponto em que a reta de de_fora até o centro de c entra na caixa c (para a ponta da seta)."""
    x, y, w, h = c
    dx, dy = de_fora[0] - x, de_fora[1] - y
    if dx == 0 and dy == 0:
        return x, y
    t = min((w / 2 + 3) / abs(dx) if dx else 9e9, (h / 2 + 3) / abs(dy) if dy else 9e9)
    return x + dx * t, y + dy * t


def _pontos(m, a, b, n=24):
    (x1, y1), (x2, y2) = m["nos"][a][2:4], m["nos"][b][2:4]
    cv = _curva(m, a, b)
    if isinstance(cv, tuple):
        out = []
        for i in range(n + 1):
            t = i / n
            f0, f1, f2, f3 = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
            out.append((f0 * x1 + f1 * x1 + f2 * x2 + f3 * x2, f0 * y1 + f1 * cv[1] + f2 * cv[1] + f3 * y2))
        return out
    c = _ctrl(m, a, b)
    if c is None:
        return [(x1, y1), (x2, y2)]
    out = []
    for i in range(n + 1):
        t = i / n
        out.append(((1 - t) ** 2 * x1 + 2 * (1 - t) * t * c[0] + t * t * x2, (1 - t) ** 2 * y1 + 2 * (1 - t) * t * c[1] + t * t * y2))
    return out


def _cruza(p, q, r, s):
    def o(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return o(p, q, r) * o(p, q, s) < 0 and o(r, s, p) * o(r, s, q) < 0


def _seg_caixa(p, q, c, folga=4):
    x, y, w, h = c
    a, b = x - w / 2 - folga, x + w / 2 + folga
    d, e = y - h / 2 - folga, y + h / 2 + folga
    for i in range(41):
        t = i / 40
        u, v = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        if a <= u <= b and d <= v <= e:
            return True
    return False


def conferir(nome, m):
    """Devolve (problemas, cruzamentos). Problema = nó sobre nó, linha sobre nó alheio, nó sem ligação, nó fora da tela."""
    cx = _caixas(m)
    prob, ids = [], list(cx)
    for i, a in enumerate(ids):
        xa, ya, wa, ha = cx[a]
        if xa - wa / 2 < 0 or xa + wa / 2 > m["W"] or ya - ha / 2 < 0 or ya + ha / 2 > m["H"]:
            prob.append(f"{a} fora da tela")
        for b in ids[i + 1:]:
            xb, yb, wb, hb = cx[b]
            if abs(xa - xb) < (wa + wb) / 2 + 6 and abs(ya - yb) < (ha + hb) / 2 + 6:
                prob.append(f"nó {a} sobre nó {b}")
    ars = _pares(m)
    tocados = {x for a in ars for x in a[:2]}
    prob += [f"nó {a} sem ligação" for a in ids if a not in tocados]
    for (a, b, *_) in ars:
        if a not in cx or b not in cx:
            prob.append(f"ligação {a}-{b}: nó inexistente")
            continue
        pts = _pontos(m, a, b)
        for k in ids:
            if k in (a, b):
                continue
            if any(_seg_caixa(pts[i], pts[i + 1], cx[k]) for i in range(len(pts) - 1)):
                prob.append(f"ligação {a}-{b} passa sobre {k}")
    cruz = []
    for i, x in enumerate(ars):
        for y in ars[i + 1:]:
            if {x[0], x[1]} & {y[0], y[1]}:
                continue
            p1, p2 = _pontos(m, x[0], x[1]), _pontos(m, y[0], y[1])
            if any(_cruza(p1[u], p1[u + 1], p2[v], p2[v + 1]) for u in range(len(p1) - 1) for v in range(len(p2) - 1)):
                cruz.append(f"{x[0]}-{x[1]} × {y[0]}-{y[1]}")
    return prob, cruz


# ---------------------------------------------------------------- desenho
def _texto(tipo, texto, x, y):
    linhas = texto.split("|")
    lh = 21 if tipo == "T" else 19.5
    y0 = y - (len(linhas) - 1) * lh / 2
    # rótulos "T1", "A1" etc. do mapa da Vivelar ganham destaque
    out = []
    for i, l in enumerate(linhas):
        out.append(f'<tspan x="{x}" y="{y0 + i * lh:.1f}">{E(l)}</tspan>')
    return f'<text class="msa-t" text-anchor="middle" dominant-baseline="central">{"".join(out)}</text>'


def _rotulo_puro(texto):
    return texto.replace("-|", "-").replace("|", " ")


def svg(nome):
    m = MAPAS[nome]
    cx = _caixas(m)
    corpo_lin, setas = [], []
    temseta = False
    for a, b, classe, tipo, frase, seta in _pares(m):
        c = _ctrl(m, a, b)
        (x1, y1), (x2, y2) = m["nos"][a][2:4], m["nos"][b][2:4]
        if seta:
            ref = c if c else (x1, y1)
            x2, y2 = _bordas(cx[b], ref)
            temseta = True
        cv = _curva(m, a, b)
        if isinstance(cv, tuple):
            d = f"M{x1} {y1} C{x1} {cv[1]} {x2} {cv[1]} {x2} {y2}"
        elif c is None:
            d = f"M{x1} {y1} L{x2:.1f} {y2:.1f}"
        else:
            d = f"M{x1} {y1} Q{c[0]:.1f} {c[1]:.1f} {x2:.1f} {y2:.1f}"
        extra = (f' data-tipo="{tipo}" data-frase="{E(frase)}"' if tipo else "") + (' data-seta="1"' if seta else "")
        cl = f"msa-l msa-l-{classe}" + (f" msa-l-{tipo}" if tipo else "")
        marca = f' marker-end="url(#seta-{nome}-{tipo})"' if seta else ""
        corpo_lin.append(f'<g class="{cl}" data-a="{a}" data-b="{b}"{extra}><path class="msa-casca" d="{d}"/><path class="msa-traco" d="{d}"{marca}/></g>')
        if tipo:
            mx, my = _meio(m, a, b, c, (x2, y2))
            setas.append(f'<g class="msa-sinal msa-sinal-{tipo}" data-a="{a}" data-b="{b}"><circle cx="{mx:.1f}" cy="{my:.1f}" r="10.5"/>'
                         f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" dominant-baseline="central">{tipo}</text></g>')
    nos = []
    # atividades primeiro e temas por cima
    for k, n in sorted(m["nos"].items(), key=lambda kv: kv[1][0] == "T"):
        tipo, texto, x, y, cats = n
        w, h = tam_no(tipo, texto)
        rx = h / 2 if tipo == "T" else 13
        cl = "msa-no " + ("msa-tema" if tipo == "T" else "msa-ativ") + "".join(f" msa-c-{c}" for c in cats.split())
        rot = _rotulo_puro(texto)
        nos.append(f'<g class="{cl}" data-no="{k}" data-rot="{E(rot)}" data-cats="{E(cats)}" tabindex="0" role="button" aria-label="{E(rot)}">'
                   f'<rect x="{x - w / 2:.1f}" y="{y - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}"/>{_texto(tipo, texto, x, y)}</g>')
    defs = ""
    if temseta:
        defs = "<defs>" + "".join(
            f'<marker id="seta-{nome}-{t}" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" orient="auto-start-reverse">'
            f'<path class="msa-ponta msa-ponta-{t}" d="M0 0 L10 5 L0 10 z"/></marker>' for t in TIPOS) + "</defs>"
    return (f'<svg class="msa-svg" viewBox="0 0 {m["W"]} {m["H"]}" role="group" aria-label="{E(m["titulo"])}">{defs}'
            f'<g class="msa-ligacoes">{"".join(corpo_lin)}</g><g class="msa-nos">{"".join(nos)}</g><g class="msa-sinais">{"".join(setas)}</g></svg>')


def _meio(m, a, b, c, fim):
    (x1, y1) = m["nos"][a][2:4]
    if c is None:
        ini = _bordas(_caixas(m)[a], fim)
        t = m.get("sinais", {}).get(f"{a}-{b}", 0.5)
        return ini[0] + (fim[0] - ini[0]) * t, ini[1] + (fim[1] - ini[1]) * t
    return 0.25 * x1 + 0.5 * c[0] + 0.25 * fim[0], 0.25 * y1 + 0.5 * c[1] + 0.25 * fim[1]


def lista(nome):
    """Versão em lista do mapa: legível em qualquer largura e sem depender de JavaScript."""
    m = MAPAS[nome]
    rot = {k: _rotulo_puro(n[1]) for k, n in m["nos"].items()}
    viz = {k: [] for k in rot}
    for a, b, classe, *_ in _pares(m):
        if classe == "conflito":
            continue
        viz[a].append(b)
        viz[b].append(a)
    temas = [k for k, n in m["nos"].items() if n[0] == "T"]
    itens = []
    for t in temas:
        ativ = [rot[v] for v in viz[t] if m["nos"][v][0] == "A"]
        tt = [rot[v] for v in viz[t] if m["nos"][v][0] == "T"]
        itens.append(f'<li><strong>{E(rot[t])}.</strong>' + (f' Atividades ligadas: {E("; ".join(ativ))}.' if ativ else "")
                     + (f' Temas ligados: {E("; ".join(tt))}.' if tt else "") + "</li>")
    entre = sorted({" — ".join(sorted((rot[a], rot[b]))) for a, b, classe, *_ in _pares(m)
                    if m["nos"][a][0] == "A" and m["nos"][b][0] == "A" and classe != "conflito"})
    h = f'<ul class="msa-lista-temas">{"".join(itens)}</ul>'
    if entre:
        h += '<p class="msa-lista-sub">Ligações entre atividades:</p><ul class="msa-lista-pares">' + "".join(f"<li>{E(x)}</li>" for x in entre) + "</ul>"
    if m.get("conflitos"):
        h += ('<p class="msa-lista-sub">Conflitos com os temas:</p><ul class="msa-lista-pares">'
              + "".join(f"<li>{E(rot[a])} × {E(rot[b])}: {E(f)}</li>" for a, b, f in m["conflitos"]) + "</ul>")
    return h


def figura(nome, sufixo=""):
    """Mapa completo: legenda com botões de destaque, SVG, painel de leitura e versão em lista."""
    m = MAPAS[nome]
    cats = sorted({c for n in m["nos"].values() for c in n[4].split()}, key=list(CATEGORIAS).index)
    botoes = "".join(
        f'<button type="button" class="msa-cat msa-c-{c}" data-cat="{c}" aria-pressed="false" title="{E(CATEGORIAS[c][1])}"><i></i>{E(CATEGORIAS[c][0])}</button>'
        for c in cats)
    tipos = ""
    if m.get("tipadas"):
        tipos = "".join(f'<span class="msa-leg msa-leg-{t}"><i></i>{t}: {E(TIPOS[t])}</span>' for t in TIPOS)
    linhas_leg = ('<span class="msa-leg msa-leg-tema"><i></i>Tema de ordem superior</span>'
                  '<span class="msa-leg msa-leg-ativ"><i></i>Atividade</span>')
    if m.get("grossas"):
        linhas_leg += '<span class="msa-leg msa-leg-grossa"><i></i>Ligação entre temas</span><span class="msa-leg msa-leg-fina"><i></i>Ligação com atividade</span>'
    else:
        linhas_leg += '<span class="msa-leg msa-leg-fina"><i></i>Atividade sustenta o tema</span>'
    if m.get("conflitos"):
        tipos += '<span class="msa-leg msa-leg-X"><i></i>X: conflito com o tema</span>'
    total = len(_pares(m))
    n_nos = len(m["nos"])
    return (
        f'<figure class="msa" data-mapa="{nome}" data-atividade>'
        f'<div class="msa-legenda">{linhas_leg}{tipos}<button type="button" class="msa-ampliar" aria-pressed="false">Ampliar o mapa</button></div>'
        + (f'<div class="msa-cats" role="group" aria-label="Destacar no mapa"><span class="msa-cats-rot">Destacar:</span>{botoes}</div>' if botoes else "")
        + f'<div class="msa-palco" tabindex="0" role="region" aria-label="{E(m["titulo"])}: role para os lados em telas estreitas">{svg(nome)}</div>'
        f'<p class="msa-arraste">Arraste o mapa para os lados para vê-lo inteiro.</p>'
        f'<div class="msa-painel" aria-live="polite"><p class="msa-dica">Clique em um nó para acompanhar as ligações dele. {n_nos} nós e {total} ligações neste mapa.</p></div>'
        f'<details class="msa-lista"><summary>Ler este mapa em forma de lista</summary>{lista(nome)}</details>'
        f'</figure>')


if __name__ == "__main__":
    tudo_ok = True
    for nome, m in MAPAS.items():
        p, c = conferir(nome, m)
        temas = sum(1 for n in m["nos"].values() if n[0] == "T")
        print(f"{nome}: {temas} temas, {len(m['nos']) - temas} atividades, {len(_pares(m))} ligações, {len(c)} cruzamentos")
        for x in c:
            print("   cruzamento:", x)
        for x in p:
            print("   PROBLEMA:", x)
        tudo_ok &= not p
    raise SystemExit(0 if tudo_ok else 1)
