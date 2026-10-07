"""
Roda o teste de ponta a ponta (teste_ponta_a_ponta.html) num Edge headless, em tempo real,
controlado pelo protocolo de depuração (CDP), contra o Apps Script simulado (servidor_simulado.py).
Não toca na planilha real. Saída: uma linha PASS/FAIL por verificação; código de saída 1 se houver falha.

Uso (na raiz do repositório):  python ferramentas/testes/rodar_testes.py
(ou .\\ferramentas\\testes\\rodar_testes.ps1, que chama este script)

Por que não --dump-dom com --virtual-time-budget: o Edge headless às vezes trava o carregamento
da página (o parser para depois das folhas de estilo). Em tempo real dá para detectar a trava:
se nenhuma verificação aparecer em 30 s, o teste recomeça do zero (servidor e navegador novos).
"""
import json
import pathlib
import subprocess
import sys
import tempfile
import time
import urllib.request

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
from capturar_telas import WS, EDGE  # noqa: E402

PORTA_SITE, PORTA_CDP, LIMITE, ARRANQUE, TENTATIVAS = 8766, 9337, 300, 30, 3


def rodar():
    """Uma tentativa. Devolve (linhas, terminou, travou_no_inicio)."""
    srv = subprocess.Popen([sys.executable, str(AQUI / "servidor_simulado.py"), str(PORTA_SITE)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    edge = subprocess.Popen([EDGE, "--headless=new", "--disable-gpu", "--no-first-run", f"--remote-debugging-port={PORTA_CDP}",
                             f"--user-data-dir={tempfile.mkdtemp(prefix='pe-teste-')}", "about:blank"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    linhas, fim = [], False
    try:
        time.sleep(1.5)
        alvo = None
        for _ in range(40):
            try:
                alvo = next(t for t in json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORTA_CDP}/json")) if t["type"] == "page")
                break
            except Exception:
                time.sleep(0.5)
        ws = WS(alvo["webSocketDebuggerUrl"])
        ws.cmd("Page.enable")
        ws.cmd("Runtime.enable")
        ws.cmd("Page.navigate", url=f"http://127.0.0.1:{PORTA_SITE}/__teste.html")
        inicio = time.time()
        while time.time() - inicio < LIMITE and not fim:
            time.sleep(3)
            r = ws.cmd("Runtime.evaluate", returnByValue=True,
                       expression="document.getElementById('log').textContent + '\\n@' + document.title")
            todas = r["result"]["value"].split("\n")
            fim = todas[-1] == "@FIM"
            for l in todas[:-1]:
                if l.startswith(("PASS", "FAIL", "ERRO")) and l not in linhas:
                    linhas.append(l)
                    print(l, flush=True)
            if not linhas and time.time() - inicio > ARRANQUE:
                return linhas, False, True
        return linhas, fim, False
    finally:
        edge.kill()
        srv.kill()
        time.sleep(1)


for tentativa in range(1, TENTATIVAS + 1):
    linhas, fim, travou = rodar()
    if not travou:
        break
    print(f"(o Edge headless travou ao carregar a página; recomeçando, tentativa {tentativa + 1} de {TENTATIVAS})", flush=True)

falhas = sum(1 for l in linhas if not l.startswith("PASS"))
if not fim:
    print("TIMEOUT: o teste não terminou")
    falhas += 1
print("---")
print(f"PASS: {sum(1 for l in linhas if l.startswith('PASS'))}  FAIL/ERRO: {falhas}")
sys.exit(1 if falhas else 0)
