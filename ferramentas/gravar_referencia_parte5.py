"""Grava conteudo/referencia-parte-5-en.txt a partir do PDF, sem imprimir o texto (só contagens).

Uso (na raiz): python ferramentas/gravar_referencia_parte5.py "../PORTER - WHAT IS STRATEGY.pdf" conteudo/referencia-parte-5-en.txt
Precisa do PyMuPDF (fitz). Os índices dos blocos foram conferidos pela posição na página (pp. 50–54 = páginas 14–18 do arquivo).
"""
import re
import sys
import warnings

warnings.filterwarnings("ignore")
import fitz  # noqa: E402

pdf, destino = sys.argv[1], sys.argv[2]
doc = fitz.open(pdf)
B = [None]
for pg in (14, 15, 16, 17, 18):
    for b in doc[pg - 1].get_text("blocks"):
        if b[1] < 50 or b[1] > 745:
            continue
        t = re.sub(r"-[ \t]*\n[ \t]*(?=[a-z])", "", b[4])   # hifenização no fim da linha
        t = " ".join(t.split())
        t = re.sub("[•�]", "•", t)
        B.append(t)


def junta(*ids):
    out = ""
    for i in ids:
        t = B[i]
        if out.endswith("-") and t[:1].islower():
            out = out[:-1] + t
        else:
            out = (out + " " + t).strip()
    return out


corpo_ids = [(8, 9), (10,), (11,), (12,), (13, 19), (20,), (21, 22), (23,), (24, 33), (34, 35), (36,), (37,), (38,), (39,),
             (46,), (47,), (48,), (49,), (50, 51), (52,), (53,), (54,), (55,), (56, 57)]
corpo = [junta(*ids) for ids in corpo_ids]
corpo[0] = re.sub(r"^V\.\s+\S+\s+\S+\s+", "", corpo[0])   # o bloco traz o título da parte antes do parágrafo

b30 = B[30]   # quadro da p. 51: a lista de perguntas e o começo do parágrafo seguinte
m = list(re.finditer(r"\?\s+(?=[A-Z])", b30))[-1]
lista, resto = b30[:m.end()].strip(), b30[m.end():].strip()
itens = [x.strip() for x in lista.split("•") if x.strip()]
q3 = B[29] + " • " + " • ".join(itens)
q4 = resto + " " + B[31]
quadro = [B[26], junta(27, 28), q3, q4, B[32], B[41], junta(42, 43), B[44], B[45]]

cab = ("# Referência em inglês da Parte V (extraída do PDF com PyMuPDF, pp. 50–54 = páginas 14–18 do arquivo; "
       "quadros da p. 51 e da p. 52; sem notas; uso só para conferência, não é publicado)")
with open(destino, "w", encoding="utf-8", newline="\n") as f:
    f.write(cab + "\n[CORPO]\n" + "\n".join(corpo) + "\n[QUADRO]\n" + "\n".join(quadro) + "\n[NOTA]\n")
for k, t in enumerate(corpo, 1):
    print(f"§{k}: {len(re.findall(r'[^\W_]+', t))} palavras")
for k, t in enumerate(quadro, 1):
    print(f"Q{k}: {len(re.findall(r'[^\W_]+', t))} palavras, itens de lista: {t.count('•')}")
