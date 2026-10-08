"""
Protege as respostas já salvas pela turma: tira uma "fotografia" das chaves de cada página de aula
e depois confere se nada mudou.

Uso (na raiz do repositório):
    python ferramentas/fotografar_chaves.py antes      # ANTES de mexer em qualquer coisa
    python ferramentas/fotografar_chaves.py comparar   # depois de gerar as páginas de novo

O que entra na fotografia de cada partes/parte-N.html:
  - as chaves de resposta (data-campo) e os pares opção/chave dos botões de escolha;
  - os parágrafos da tradução (data-par e o rótulo §N/QN), aos quais as anotações e destaques estão ligados;
  - os widgets (data-widget) e o id da atividade em PARTE.iniciar (aula1, aula2...).
Se algo disso mudar numa aula que a turma já usa, as respostas salvas podem ficar órfãs.
Páginas novas (sem fotografia anterior) são apenas listadas.

A fotografia fica em conteudo/.chaves-antes.json (fora do git). Sai com código 1 se houver diferença.
"""
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ARQ = RAIZ / "conteudo" / ".chaves-antes.json"


def chaves(html):
    return {
        "campos": sorted(set(re.findall(r'data-campo="([^"]+)"', html))),
        "opcoes": sorted({f"{c}={v}" for v, c in re.findall(r'value="([^"]+)" data-campo="([^"]+)"', html)}),
        "paragrafos": [f"{n}:{r}" for n, r in re.findall(r'data-par="(\d+)" data-rotulo="([^"]+)"', html)],
        "widgets": re.findall(r'data-widget="([^"]+)"', html),
        "atividade": re.findall(r"PARTE\.iniciar\(\{ id: '([^']+)'", html),
    }


def todas():
    return {p.name: chaves(p.read_text(encoding="utf-8")) for p in sorted((RAIZ / "partes").glob("parte-*.html"))}


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else ""
    if modo == "antes":
        foto = todas()
        ARQ.parent.mkdir(exist_ok=True)
        ARQ.write_text(json.dumps(foto, ensure_ascii=False, indent=1), encoding="utf-8")
        for nome, c in foto.items():
            print(f"{nome}: {len(c['campos'])} chaves, {len(c['opcoes'])} opções, {len(c['paragrafos'])} parágrafos, "
                  f"widgets {c['widgets']}, atividade {c['atividade']}")
        print(f"Fotografia salva em {ARQ.relative_to(RAIZ)}")
    elif modo == "comparar":
        if not ARQ.exists():
            sys.exit("Não há fotografia anterior. Rode primeiro: python ferramentas/fotografar_chaves.py antes")
        antes, agora = json.loads(ARQ.read_text(encoding="utf-8")), todas()
        problemas = 0
        for nome, c in antes.items():
            if nome not in agora:
                print(f"FALHA {nome}: a página sumiu")
                problemas += 1
                continue
            difs = [k for k in c if c[k] != agora[nome][k]]
            if difs:
                problemas += 1
                print(f"FALHA {nome}: mudou {', '.join(difs)}")
                for k in difs:
                    a, b = set(map(str, c[k])), set(map(str, agora[nome][k]))
                    if a - b:
                        print(f"   saiu de {k}: {sorted(a - b)[:10]}")
                    if b - a:
                        print(f"   entrou em {k}: {sorted(b - a)[:10]}")
                    if a == b:
                        print(f"   {k}: mesma coleção, ordem diferente")
            else:
                print(f"OK    {nome}: chaves, opções, parágrafos, widgets e atividade idênticos")
        for nome in agora:
            if nome not in antes:
                print(f"NOVA  {nome}: {len(agora[nome]['campos'])} chaves, atividade {agora[nome]['atividade']}")
        sys.exit(1 if problemas else 0)
    else:
        sys.exit(__doc__)
