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

CAPTURAS = [  # (nome, página, seletor, largura, altura)
    ("home", "/index.html", "", 1366, 1500),
    ("home-porter", "/index.html", "#porter", 1366, 1300),
    ("p1-topo", "/partes/parte-1.html", "", 1366, 1100),
    ("p1-texto", "/partes/parte-1.html", "#p5", 1366, 1200),
    ("p1-figura", "/partes/parte-1.html", "#figura-fronteira", 1366, 1300),
    ("p1-quadro", "/partes/parte-1.html", "#quadro-japao", 1366, 1200),
    ("p1-material", "/partes/parte-1.html", "#material", 1366, 1200),
    ("p1-duvida", "/partes/parte-1.html", "#duvida-1-para-fazer-melhor-eu-nao-preciso-fazer-diferent", 1366, 1200),
    ("p1-fronteira", "/partes/parte-1.html", "[data-widget=fronteira]", 1366, 1100),
    ("p1-portfolio", "/partes/parte-1.html", "[data-widget=portfolio]", 1366, 1100),
    ("p1-bsc", "/partes/parte-1.html", "#bsc-do-cenario-a-eficacia-operacional", 1366, 1200),
    ("p1-simulador", "/partes/parte-1.html", "#simulador", 1366, 1500),
    ("p1-exit", "/partes/parte-1.html", "#exit-ticket-5-min-individual", 1366, 1200),
    ("p1-fim", "/partes/parte-1.html", "#minhas-respostas", 1366, 1000),
    ("m-home", "/index.html", "", 520, 2000),
    ("m-home-porter", "/index.html", "#porter", 520, 2000),
    ("m-p1-texto", "/partes/parte-1.html", "#p5", 520, 1600),
    ("m-p1-fronteira", "/partes/parte-1.html", "[data-widget=fronteira]", 520, 1800),
    ("m-p1-simulador", "/partes/parte-1.html", "#simulador", 520, 2600),
    ("m-p1-tabela", "/partes/parte-1.html", "[id=\"7-6-resultados-financeiros\"]", 520, 1600),
]


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
            for _ in range(40):
                pronto = ws.cmd("Runtime.evaluate", returnByValue=True, expression="location.search.indexOf('" + marca + "')>=0 && document.readyState==='complete' && !!document.querySelector('.vd-topbar') && document.fonts.status==='loaded'")
                if pronto.get("result", {}).get("value"):
                    break
                time.sleep(0.25)
            time.sleep(0.6)
            if sel:
                r = ws.cmd("Runtime.evaluate", returnByValue=True, expression=(
                    "(function(){document.documentElement.style.scrollBehavior='auto';"
                    f"var el=document.querySelector({json.dumps(sel)}); if(!el) return 'sem alvo';"
                    "var d=el.closest('details'); if(d) d.open=true;"
                    "window.scrollTo({top: el.getBoundingClientRect().top + scrollY - 70, behavior:'instant'}); return 'ok';})()"))
                if r.get("result", {}).get("value") != "ok":
                    print(f"  aviso: {nome}: seletor {sel} não encontrado ({r})")
                time.sleep(0.8)
            png = ws.cmd("Page.captureScreenshot", format="png")["data"]
            (saida / f"{nome}.png").write_bytes(base64.b64decode(png))
            print("OK ", nome)
        erros = ws.cmd("Runtime.evaluate", returnByValue=True, expression="document.documentElement.scrollWidth > innerWidth ? 'rolagem horizontal!' : 'sem rolagem horizontal'")
        print("última página (520px):", erros["result"]["value"])
    finally:
        edge.kill()
        site.kill()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "capturas")
