"""
Capturas de tela do portal no Edge headless, controlado pelo protocolo de depuração (CDP).
Sem dependências: tem um cliente WebSocket mínimo embutido.

Uso (na raiz do repositório):
    python ferramentas/capturar_telas.py <pasta-de-saída> [nomes das capturas...]

Sobe um servidor local na porta 8765, abre cada página com uma sessão local de exemplo
("Ana Souza", sem planilha), rola até o seletor indicado e salva PNGs em 1366px e 520px.
Por que não usar só --screenshot: com âncoras e rolagem suave, o headless captura a página
no meio da rolagem; aqui a rolagem é instantânea e a captura espera os scripts.
"""
import base64
import json
import os
import pathlib
import random
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORTA_SITE, PORTA_CDP = 8765, 9333

# (nome, página, alvo, largura, altura). O alvo é um id: na página da parte ele vai no endereço (#id),
# e o próprio portal abre o módulo certo e rola até o ponto, como acontece com o estudante.
CAPTURAS = [
    ("home", "/index.html", "", 1366, 1500),
    ("home-porter", "/index.html", "porter", 1366, 1300),
    ("p1-indice", "/partes/parte-1.html", "", 1366, 1500),
    ("p1-mapa", "/partes/parte-1.html", "m-mapa-de-aprendizagem", 1366, 1300),
    ("p1-texto", "/partes/parte-1.html", "p5", 1366, 1200),
    ("p1-figura", "/partes/parte-1.html", "figura-fronteira", 1366, 1300),
    ("p1-bloco1", "/partes/parte-1.html", "m-bloco-1-definicoes", 1366, 1200),
    ("p1-duvida", "/partes/parte-1.html", "duvida-1-para-fazer-melhor-eu-nao-preciso-fazer-diferent", 1366, 1200),
    ("p1-esquema", "/partes/parte-1.html", "3-2-a-fronteira-em-um-esquema", 1366, 1300),
    ("p1-fronteira", "/partes/parte-1.html", "3-5-exercicio-posicione-tres-empresas", 1366, 1300),
    ("p1-bsc", "/partes/parte-1.html", "bsc-do-cenario-a-eficacia-operacional", 1366, 1200),
    ("p1-simulador", "/partes/parte-1.html", "simulador", 1366, 1500),
    ("p1-exit", "/partes/parte-1.html", "exit-ticket", 1366, 1300),
    ("p1-fim-modulo", "/partes/parte-1.html", "referencias", 1366, 1100),
    ("m-home", "/index.html", "", 520, 2000),
    ("m-p1-indice", "/partes/parte-1.html", "", 520, 2400),
    ("m-p1-mapa", "/partes/parte-1.html", "m-mapa-de-aprendizagem", 520, 2000),
    ("m-p1-texto", "/partes/parte-1.html", "p5", 520, 1600),
    ("m-p1-esquema", "/partes/parte-1.html", "3-2-a-fronteira-em-um-esquema", 520, 1400),
    ("m-p1-simulador", "/partes/parte-1.html", "simulador", 520, 2600),
    ("p2-indice", "/partes/parte-2.html", "", 1366, 1500),
    ("p2-texto", "/partes/parte-2.html", "p8", 1366, 1200),
    ("p2-quadro", "/partes/parte-2.html", "quadro-novas-posicoes", 1366, 1200),
    ("p2-abertura", "/partes/parte-2.html", "a-sua-frase-de-estrategia", 1366, 1300),
    ("p2-cadeia", "/partes/parte-2.html", "2-4-exercicio-a-cadeia-comparada", 1366, 1400),
    ("p2-classificacao", "/partes/parte-2.html", "3-6-exercicio-de-classificacao", 1366, 1300),
    ("p2-rastreio", "/partes/parte-2.html", "7-4-quatro-praticas-de-execucao", 1366, 1500),
    ("m-p2-cadeia", "/partes/parte-2.html", "2-4-exercicio-a-cadeia-comparada", 520, 2200),
    ("m-p2-classificacao", "/partes/parte-2.html", "3-6-exercicio-de-classificacao", 520, 2000),
]


def encerrar(proc):
    """Encerra o processo e todos os filhos (no Windows, edge.kill() deixa os processos filhos do Edge vivos)."""
    subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)


class WS:
    """Cliente WebSocket mínimo (só texto, sem extensões) para o CDP."""

    def __init__(self, url):
        host, resto = url[len("ws://"):].split("/", 1)
        h, p = host.split(":")
        self.s = socket.create_connection((h, int(p)))
        chave = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall((f"GET /{resto} HTTP/1.1\r\nHost: {host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                        f"Sec-WebSocket-Key: {chave}\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += self.s.recv(4096)
        self.buf = resp.split(b"\r\n\r\n", 1)[1]
        self.n = 0

    def _ler(self, n):
        while len(self.buf) < n:
            self.buf += self.s.recv(1 << 20)
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def enviar(self, obj):
        dados = json.dumps(obj).encode()
        cab = bytearray([0x81])
        n = len(dados)
        if n < 126:
            cab.append(0x80 | n)
        elif n < 65536:
            cab += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            cab += bytes([0x80 | 127]) + struct.pack(">Q", n)
        mask = os.urandom(4)
        self.s.sendall(bytes(cab) + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(dados)))

    def receber(self):
        partes = b""
        while True:
            b1, b2 = self._ler(2)
            n = b2 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._ler(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._ler(8))[0]
            partes += self._ler(n)
            if b1 & 0x80:
                return json.loads(partes)

    def cmd(self, metodo, **params):
        self.n += 1
        self.enviar({"id": self.n, "method": metodo, "params": params})
        while True:
            m = self.receber()
            if m.get("id") == self.n:
                if "error" in m:
                    raise RuntimeError(m["error"])
                return m.get("result", {})


def main(saida):
    saida = pathlib.Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    site = subprocess.Popen([sys.executable, "-m", "http.server", str(PORTA_SITE), "--bind", "127.0.0.1"],
                            cwd=RAIZ, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    perfil = tempfile.mkdtemp(prefix="pe-cdp-")
    edge = subprocess.Popen([EDGE, "--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars",
                             f"--remote-debugging-port={PORTA_CDP}", f"--user-data-dir={perfil}", "about:blank"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        alvo = None
        for _ in range(40):
            try:
                lista = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORTA_CDP}/json"))
                alvo = next(t for t in lista if t["type"] == "page")
                break
            except Exception:
                time.sleep(0.5)
        ws = WS(alvo["webSocketDebuggerUrl"])
        ws.cmd("Page.enable")
        ws.cmd("Runtime.enable")   # sem isto, o headless às vezes não executa os scripts da página a tempo
        ws.cmd("Page.bringToFront")
        ws.cmd("Emulation.setFocusEmulationEnabled", enabled=True)
        base = f"http://127.0.0.1:{PORTA_SITE}"
        ws.cmd("Page.navigate", url=base + "/index.html")
        time.sleep(1.5)
        sessao = json.dumps({"id": "ana souza", "nome": "Ana Souza", "turma": "Turma 2026", "chave": "", "modo": "local"})
        ws.cmd("Runtime.evaluate", expression=f"localStorage.clear(); localStorage.setItem('pe_sessao_v1', {json.dumps(sessao)})")
        filtro = sys.argv[2:] 
        for nome, pagina, sel, w, h in CAPTURAS:
            if filtro and nome not in filtro:
                continue
            ws.cmd("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=1, mobile=w < 700)
            marca = str(random.randint(1, 10**9))
            ws.cmd("Page.navigate", url=base + pagina + "?x=" + marca)
            # espera a página e o portal.js terminarem (barra superior montada)
            for k in range(80):
                pronto = ws.cmd("Runtime.evaluate", returnByValue=True, expression="JSON.stringify([location.search.indexOf('" + marca + "')>=0, document.readyState, !!document.querySelector('.vd-topbar'), document.fonts.status])")
                v = json.loads(pronto.get("result", {}).get("value") or "[false]")
                if v[0] and v[1] == "complete" and v[2] and v[3] == "loaded":
                    break
                if k in (20, 40, 60):   # o headless às vezes para no meio do carregamento: recarrega
                    ws.cmd("Page.reload", ignoreCache=True)
                time.sleep(0.25)
            else:
                print("  aviso: página não ficou pronta:", v)
                rec = ws.cmd("Runtime.evaluate", returnByValue=True, expression="JSON.stringify(performance.getEntriesByType('resource').map(function(e){return e.name.split('/').slice(-1)[0].slice(0,40)+' '+Math.round(e.duration)}))")
                print("  recursos carregados:", rec.get("result", {}).get("value"))
            time.sleep(0.6)
            if sel:
                # na página da parte, quem abre o módulo e rola é o próprio portal (PARTE.abrir);
                # nas demais, rola até o id sem animação
                r = ws.cmd("Runtime.evaluate", returnByValue=True, expression=(
                    "(function(){document.documentElement.style.scrollBehavior='auto';"
                    f"var id={json.dumps(sel)}, el=document.getElementById(id); if(!el) return 'sem alvo';"
                    "if (window.PARTE) { PARTE.abrir(id); return 'ok'; }"
                    "window.scrollTo({top: el.getBoundingClientRect().top + scrollY - 70, behavior:'instant'}); return 'ok';})()"))
                if r.get("result", {}).get("value") != "ok":
                    print(f"  aviso: {nome}: alvo {sel} não encontrado ({r})")
                time.sleep(0.9)
            png = ws.cmd("Page.captureScreenshot", format="png")["data"]
            (saida / f"{nome}.png").write_bytes(base64.b64decode(png))
            print("OK ", nome)
        erros = ws.cmd("Runtime.evaluate", returnByValue=True, expression="document.documentElement.scrollWidth > innerWidth ? 'rolagem horizontal!' : 'sem rolagem horizontal'")
        print("última página (520px):", erros["result"]["value"])
    finally:
        encerrar(edge)
        encerrar(site)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "capturas")
