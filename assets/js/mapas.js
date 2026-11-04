/*
 * Mapas de sistemas de atividades (Aula 4). Só leitura: nada aqui é salvo.
 *   - clicar (ou Enter) em um nó destaca as ligações dele e lista os vizinhos no painel abaixo do mapa;
 *   - os botões "Destacar" realçam uma categoria (renúncias, pessoas, cliente, núcleo, genéricas);
 *   - as abas do Bloco 4 alternam entre os três mapas de Porter.
 * Os SVG vêm prontos do gerador (ferramentas/mapas_atividades.py) ou são desenhados pelo construtor
 * do estudante (widget "sistema", em parte.js), que usa MAPAS.ligar e MAPAS.desenhar.
 * Todo texto vindo do estudante passa por VD.esc antes de entrar em innerHTML.
 */
(function () {
  'use strict';
  var esc = function (s) { return VD.esc(s); };
  var DICA = {};

  function rotulo(fig, id) {
    var n = fig.querySelector('.msa-no[data-no="' + id + '"]');
    return n ? n.getAttribute('data-rot') : id;
  }

  function limpar(fig) {
    var svg = fig.querySelector('.msa-svg');
    svg.classList.remove('foco');
    svg.querySelectorAll('.on, .sel').forEach(function (e) { e.classList.remove('on', 'sel'); });
  }

  function mostrarDica(fig) {
    var p = fig.querySelector('.msa-painel');
    if (p && p.dataset.dica) p.innerHTML = '<p class="msa-dica">' + p.dataset.dica + '</p>';
  }

  function selecionar(fig, g) {
    var id = g.getAttribute('data-no');
    if (g.classList.contains('sel')) { limpar(fig); mostrarDica(fig); return; }
    fig.querySelectorAll('.msa-cat[aria-pressed="true"]').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
    limpar(fig);
    var svg = fig.querySelector('.msa-svg');
    svg.classList.add('foco');
    g.classList.add('on', 'sel');
    var viz = [], frases = [];
    svg.querySelectorAll('.msa-l').forEach(function (l) {
      var a = l.getAttribute('data-a'), b = l.getAttribute('data-b');
      if (a !== id && b !== id) return;
      l.classList.add('on');
      var outro = a === id ? b : a;
      var no = svg.querySelector('.msa-no[data-no="' + outro + '"]');
      if (no) no.classList.add('on');
      if (l.getAttribute('data-frase') !== null) {
        var seta = l.getAttribute('data-seta') ? (a === id ? ' → ' : ' ← ') : ' — ';
        frases.push('<li><b class="tp tp-' + esc(l.getAttribute('data-tipo')) + '">' + esc(l.getAttribute('data-tipo')) + '</b>' + seta + '<strong>' + esc(rotulo(fig, outro)) + '</strong>' +
          (l.getAttribute('data-frase') ? ': ' + esc(l.getAttribute('data-frase')) : '') + '</li>');
      } else {
        viz.push('<li>' + esc(rotulo(fig, outro)) + '</li>');
      }
    });
    svg.querySelectorAll('.msa-sinal').forEach(function (s) {
      if (s.getAttribute('data-a') === id || s.getAttribute('data-b') === id) s.classList.add('on');
    });
    var total = viz.length + frases.length;
    var p = fig.querySelector('.msa-painel');
    p.innerHTML = '<p class="msa-sel-tit">' + esc(g.getAttribute('data-rot')) + ' · ' + total + (total === 1 ? ' ligação' : ' ligações') + '</p>' +
      (frases.length ? '<ul class="msa-frases">' + frases.join('') + '</ul>' : '') +
      (viz.length ? '<ul>' + viz.join('') + '</ul>' : '') +
      (total ? '' : '<p>Nenhuma ligação: este nó está solto no sistema.</p>');
  }

  function destacar(fig, botao) {
    var ligado = botao.getAttribute('aria-pressed') === 'true', cat = botao.getAttribute('data-cat');
    fig.querySelectorAll('.msa-cat').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
    limpar(fig);
    if (ligado) { mostrarDica(fig); return; }
    botao.setAttribute('aria-pressed', 'true');
    var svg = fig.querySelector('.msa-svg'), nomes = [];
    svg.classList.add('foco');
    svg.querySelectorAll('.msa-no').forEach(function (n) {
      if ((' ' + n.getAttribute('data-cats') + ' ').indexOf(' ' + cat + ' ') >= 0) { n.classList.add('on'); nomes.push(n.getAttribute('data-rot')); }
    });
    var p = fig.querySelector('.msa-painel');
    p.innerHTML = '<p class="msa-sel-tit">' + esc(botao.textContent) + ' · ' + nomes.length + '</p><p>' + esc(botao.title) + '</p>' +
      '<ul>' + nomes.map(function (n) { return '<li>' + esc(n) + '</li>'; }).join('') + '</ul>';
  }

  /* mapa em tela cheia: em telas pequenas e na coluna do texto, as letras ficam maiores */
  function ampliar(fig, ligar) {
    fig.classList.toggle('msa-cheia', ligar);
    document.documentElement.classList.toggle('msa-sem-rolagem', ligar);
    var b = fig.querySelector('.msa-ampliar');
    if (b) { b.textContent = ligar ? 'Fechar' : 'Ampliar o mapa'; b.setAttribute('aria-pressed', String(ligar)); }
    if (ligar) { fig.scrollTop = 0; if (b) b.focus(); }
  }
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var f = document.querySelector('.msa.msa-cheia');
    if (f) ampliar(f, false);
  });

  /* liga um mapa (estático ou recém-desenhado) aos cliques e ao teclado */
  function ligar(fig) {
    if (fig.dataset.ligado) return;
    fig.dataset.ligado = '1';
    var p = fig.querySelector('.msa-painel');
    if (p && !p.dataset.dica) { var d = p.querySelector('.msa-dica'); p.dataset.dica = d ? d.textContent : ''; }
    fig.addEventListener('click', function (e) {
      var amp = e.target.closest('.msa-ampliar');
      if (amp) { ampliar(fig, !fig.classList.contains('msa-cheia')); return; }
      var cat = e.target.closest('.msa-cat');
      if (cat) { destacar(fig, cat); return; }
      var g = e.target.closest('.msa-no');
      if (g) selecionar(fig, g);
      else if (e.target.closest('.msa-svg') && fig.querySelector('.msa-svg.foco')) { limpar(fig); fig.querySelectorAll('.msa-cat').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); }); mostrarDica(fig); }
    });
    fig.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      var g = e.target.closest ? e.target.closest('.msa-no') : null;
      if (g) { e.preventDefault(); selecionar(fig, g); }
    });
  }

  function ligarAbas(box) {
    var botoes = box.querySelectorAll('.msa-aba');
    botoes.forEach(function (b, i) {
      b.addEventListener('click', function () {
        botoes.forEach(function (x, k) {
          x.setAttribute('aria-selected', String(k === i));
          box.querySelectorAll('.msa')[k].hidden = k !== i;
        });
      });
    });
  }

  /* ---------------------------------------------------------------- desenho do mapa do estudante */
  var NS = 13, W_T = 8.7, W_A = 7.9;

  function quebrar(txt, max, maxLin) {
    var pal = String(txt || '').trim().split(/\s+/), lin = [], at = '';
    pal.forEach(function (p) {
      if (at && (at + ' ' + p).length > max) { lin.push(at); at = p; } else at = at ? at + ' ' + p : p;
    });
    if (at) lin.push(at);
    if (lin.length > maxLin) { lin = lin.slice(0, maxLin); lin[maxLin - 1] = lin[maxLin - 1].slice(0, max - 1).replace(/\s+$/, '') + '…'; }
    return lin.map(function (l) { return l.length > max + 6 ? l.slice(0, max + 5) + '…' : l; });
  }

  function caixa(tipo, lin) {
    var m = 0; lin.forEach(function (l) { if (l.length > m) m = l.length; });
    return tipo === 'T' ? { w: m * W_T + 40, h: lin.length * 21 + 26 } : { w: m * (W_A + 0.15) + 28, h: lin.length * 19.5 + 16 };
  }

  /*
   * Posições: temas em elipse larga; cada atividade começa junto ao(s) seu(s) tema(s), em leque para fora do mapa,
   * e as de mais de um tema ficam entre eles. Depois, relaxação: separa as caixas sobrepostas e afasta as caixas
   * das linhas que não são delas. É determinístico: os mesmos dados sempre dão o mesmo desenho.
   */
  function posicionar(temas, ativs, arestas, W, H) {
    var cx = W / 2, cy = H / 2, nT = temas.length;
    var rx = nT <= 1 ? 0 : W * 0.3, ry = nT <= 1 ? 0 : H * 0.3;
    var ini = nT === 2 ? Math.PI : nT === 4 ? -3 * Math.PI / 4 : -Math.PI / 2;
    temas.forEach(function (t, i) {
      var ang = ini + i * 2 * Math.PI / Math.max(nT, 1);
      t.x = cx + rx * Math.cos(ang); t.y = cy + ry * Math.sin(ang); t.ang = ang;
    });
    var indice = {}; temas.forEach(function (t) { indice[t.id] = t; });
    var porTema = {}, soltas = 0;
    ativs.forEach(function (a, k) {
      var ts = a.temas.map(function (id) { return indice[id]; }).filter(Boolean);
      var chave = ts.map(function (t) { return t.id; }).join('+');
      var n = (porTema[chave] = (porTema[chave] || 0) + 1);
      if (ts.length >= 2) {
        var sx = 0, sy = 0; ts.forEach(function (t) { sx += t.x; sy += t.y; });
        sx /= ts.length; sy /= ts.length;
        var ox = sx - cx, oy = sy - cy, L = Math.sqrt(ox * ox + oy * oy);
        if (L < 1) { ox = Math.cos(k * 2.4); oy = Math.sin(k * 2.4); L = 1; }
        a.x = sx + (ox / L) * (n * 30); a.y = sy + (oy / L) * (n * 26);
      } else if (ts.length === 1) {
        var t = ts[0], base = nT <= 1 ? (k / Math.max(ativs.length, 1)) * 2 * Math.PI : t.ang;
        var ab = (n % 2 ? 1 : -1) * Math.floor(n / 2) * 0.68;
        a.x = t.x + (250 + (n % 3) * 26) * Math.cos(base + ab); a.y = t.y + (155 + (n % 3) * 22) * Math.sin(base + ab);
      } else {
        // sem tema: em fila embaixo, à vista, para o estudante notar que está solta
        soltas++;
        a.x = 130 + ((soltas - 1) % 5) * (W - 260) / 4; a.y = H * 0.9 + Math.floor((soltas - 1) / 5) * 70;
      }
    });
    var todos = temas.concat(ativs), MIN_X = -200, MAX_X = W + 200, MIN_Y = -200, MAX_Y = H + 400;
    function separar() {
      for (var i = 0; i < todos.length; i++) {
        for (var j = i + 1; j < todos.length; j++) {
          var p = todos[i], q = todos[j];
          var dx = q.x - p.x, dy = q.y - p.y;
          var sx2 = (p.w + q.w) / 2 + 22 - Math.abs(dx), sy2 = (p.h + q.h) / 2 + 22 - Math.abs(dy);
          if (sx2 > 0 && sy2 > 0) {
            var fp = p.tema ? 0.08 : 0.5, fq = q.tema ? 0.08 : 0.5;
            if (sx2 < sy2) { var ex = (dx >= 0 ? 1 : -1) * sx2; p.x -= ex * fp; q.x += ex * fq; }
            else { var ey = (dy >= 0 ? 1 : -1) * sy2; p.y -= ey * fp; q.y += ey * fq; }
          }
        }
      }
    }
    function afastarDasLinhas() {
      arestas.forEach(function (e) {
        var vx = e.b.x - e.a.x, vy = e.b.y - e.a.y, L2 = vx * vx + vy * vy || 1, L = Math.sqrt(L2);
        todos.forEach(function (n, k) {
          if (n === e.a || n === e.b) return;
          var t = Math.max(0, Math.min(1, ((n.x - e.a.x) * vx + (n.y - e.a.y) * vy) / L2));
          var px = e.a.x + vx * t, py = e.a.y + vy * t;
          if (Math.abs(px - n.x) < n.w / 2 + 10 && Math.abs(py - n.y) < n.h / 2 + 10) {
            var nx = -vy / L, ny = vx / L, lado = (n.x - e.a.x) * nx + (n.y - e.a.y) * ny;
            var sinal = lado === 0 ? (k % 2 ? 1 : -1) : (lado > 0 ? 1 : -1), passo = n.tema ? 1 : 7;
            n.x += nx * sinal * passo; n.y += ny * sinal * passo;
          }
        });
      });
    }
    function limitar() {
      todos.forEach(function (n) {
        n.x = Math.max(MIN_X, Math.min(MAX_X, n.x));
        n.y = Math.max(MIN_Y, Math.min(MAX_Y, n.y));
      });
    }
    for (var it = 0; it < 260; it++) { separar(); afastarDasLinhas(); limitar(); }
    for (var fim = 0; fim < 80; fim++) separar();   // a última palavra é não haver caixa sobre caixa
  }

  /* onde pôr a letra do tipo: no meio da linha, ou no ponto livre mais próximo do meio */
  function posSinal(ini, fim, nos, usados) {
    var ts = [0.5, 0.38, 0.62, 0.28, 0.72, 0.18, 0.82], melhor = null;
    for (var i = 0; i < ts.length && !melhor; i++) {
      var x = ini.x + (fim.x - ini.x) * ts[i], y = ini.y + (fim.y - ini.y) * ts[i];
      var livre = nos.every(function (n) { return Math.abs(n.x - x) > n.w / 2 + 12 || Math.abs(n.y - y) > n.h / 2 + 12; }) &&
        usados.every(function (u) { return Math.abs(u.x - x) > 24 || Math.abs(u.y - y) > 24; });
      if (livre) melhor = { x: x, y: y };
    }
    melhor = melhor || { x: (ini.x + fim.x) / 2, y: (ini.y + fim.y) / 2 };
    usados.push(melhor);
    return melhor;
  }

  function textoNo(lin, n, lh) {
    var y0 = n.y - (lin.length - 1) * lh / 2;
    return '<text class="msa-t" text-anchor="middle" dominant-baseline="central">' + lin.map(function (l, i) {
      return '<tspan x="' + n.x.toFixed(1) + '" y="' + (y0 + i * lh).toFixed(1) + '">' + esc(l) + '</tspan>';
    }).join('') + '</text>';
  }

  function borda(n, de) {
    var dx = de.x - n.x, dy = de.y - n.y;
    if (!dx && !dy) return { x: n.x, y: n.y };
    var t = Math.min((n.w / 2 + 3) / (Math.abs(dx) || 1e-6), (n.h / 2 + 3) / (Math.abs(dy) || 1e-6));
    return { x: n.x + dx * t, y: n.y + dy * t };
  }

  /* dados = { temas:[{id,nome}], atividades:[{id,nome,ge,ren,temas:[id]}], ligacoes:[{de,para,tipo,frase}] } (só itens com nome) */
  function desenhar(alvo, dados) {
    if (alvo.querySelector('.msa.msa-cheia')) document.documentElement.classList.remove('msa-sem-rolagem');
    var temas = dados.temas.map(function (t) {
      var lin = quebrar(t.nome, 20, 4), c = caixa('T', lin);
      return { id: t.id, nome: t.nome, lin: lin, w: c.w, h: c.h, tema: true };
    });
    var ativs = dados.atividades.map(function (a) {
      var lin = quebrar(a.id + ' ' + a.nome, 20, 4), c = caixa('A', lin);
      return { id: a.id, nome: a.nome, lin: lin, w: c.w, h: c.h, ge: a.ge, ren: a.ren, temas: a.temas || [] };
    });
    var n = temas.length + ativs.length;
    var W = 1180, H = Math.max(620, Math.min(1300, 340 + n * 34));
    var idx = {}; temas.concat(ativs).forEach(function (x) { idx[x.id] = x; });
    var arestas = [];
    ativs.forEach(function (a) { a.temas.forEach(function (t) { if (idx[t]) arestas.push({ a: a, b: idx[t] }); }); });
    dados.ligacoes.forEach(function (l) { if (idx[l.de] && idx[l.para] && l.de !== l.para) arestas.push({ a: idx[l.de], b: idx[l.para] }); });
    posicionar(temas, ativs, arestas, W, H);
    // recorta a área vazia: o desenho usa toda a largura do quadro
    var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    temas.concat(ativs).forEach(function (n) {
      x0 = Math.min(x0, n.x - n.w / 2); x1 = Math.max(x1, n.x + n.w / 2);
      y0 = Math.min(y0, n.y - n.h / 2); y1 = Math.max(y1, n.y + n.h / 2);
    });
    var folga = 16, vbW = Math.max(x1 - x0 + 2 * folga, 820), vbH = y1 - y0 + 2 * folga;
    var vbX = (x0 + x1) / 2 - vbW / 2, vbY = y0 - folga, usados = [];

    var lin = [], sinais = [];
    ativs.forEach(function (a) {
      a.temas.forEach(function (tid) {
        if (idx[tid]) lin.push('<g class="msa-l msa-l-fina" data-a="' + esc(a.id) + '" data-b="' + esc(tid) + '"><path class="msa-casca" d="M' + a.x.toFixed(1) + ' ' + a.y.toFixed(1) + ' L' + idx[tid].x.toFixed(1) + ' ' + idx[tid].y.toFixed(1) + '"/><path class="msa-traco" d="M' + a.x.toFixed(1) + ' ' + a.y.toFixed(1) + ' L' + idx[tid].x.toFixed(1) + ' ' + idx[tid].y.toFixed(1) + '"/></g>');
      });
    });
    dados.ligacoes.forEach(function (l) {
      var p = idx[l.de], q = idx[l.para]; if (!p || !q || p === q) return;
      var tp = (l.tipo === 'C' || l.tipo === 'R' || l.tipo === 'O') ? l.tipo : 'R';
      var fim = borda(q, p), ini = borda(p, q);
      var d = 'M' + p.x.toFixed(1) + ' ' + p.y.toFixed(1) + ' L' + fim.x.toFixed(1) + ' ' + fim.y.toFixed(1);
      lin.push('<g class="msa-l msa-l-tipada msa-l-' + tp + '" data-a="' + esc(l.de) + '" data-b="' + esc(l.para) + '" data-tipo="' + tp + '" data-frase="' + esc(l.frase || '') + '" data-seta="1"><path class="msa-casca" d="' + d + '"/><path class="msa-traco" d="' + d + '" marker-end="url(#seta-aluno-' + tp + ')"/></g>');
      var ps = posSinal(ini, fim, temas.concat(ativs), usados), mx = ps.x, my = ps.y;
      sinais.push('<g class="msa-sinal msa-sinal-' + tp + '" data-a="' + esc(l.de) + '" data-b="' + esc(l.para) + '"><circle cx="' + mx.toFixed(1) + '" cy="' + my.toFixed(1) + '" r="10.5"/><text x="' + mx.toFixed(1) + '" y="' + my.toFixed(1) + '" text-anchor="middle" dominant-baseline="central">' + tp + '</text></g>');
    });
    var nos = ativs.map(function (a) {
      var cats = []; if (a.ren) cats.push('ren'); if (a.temas.length >= 2) cats.push('nuc'); if (a.ge === 'G') cats.push('gen');
      var cl = 'msa-no msa-ativ' + cats.map(function (c) { return ' msa-c-' + c; }).join('');
      return '<g class="' + cl + '" data-no="' + esc(a.id) + '" data-rot="' + esc(a.id + ' ' + a.nome) + '" data-cats="' + cats.join(' ') + '" tabindex="0" role="button" aria-label="' + esc(a.id + ' ' + a.nome) + '">' +
        '<rect x="' + (a.x - a.w / 2).toFixed(1) + '" y="' + (a.y - a.h / 2).toFixed(1) + '" width="' + a.w.toFixed(1) + '" height="' + a.h.toFixed(1) + '" rx="' + NS + '"/>' + textoNo(a.lin, a, 19.5) + '</g>';
    }).concat(temas.map(function (t) {
      return '<g class="msa-no msa-tema" data-no="' + esc(t.id) + '" data-rot="' + esc(t.nome) + '" data-cats="" tabindex="0" role="button" aria-label="' + esc(t.nome) + '">' +
        '<rect x="' + (t.x - t.w / 2).toFixed(1) + '" y="' + (t.y - t.h / 2).toFixed(1) + '" width="' + t.w.toFixed(1) + '" height="' + t.h.toFixed(1) + '" rx="' + (t.h / 2).toFixed(1) + '"/>' + textoNo(t.lin, t, 21) + '</g>';
    }));
    var defs = '<defs>' + ['C', 'R', 'O'].map(function (t) {
      return '<marker id="seta-aluno-' + t + '" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" orient="auto-start-reverse"><path class="msa-ponta msa-ponta-' + t + '" d="M0 0 L10 5 L0 10 z"/></marker>';
    }).join('') + '</defs>';
    var cats = [['ren', 'Renúncias', 'O que a empresa deliberadamente não faz.'], ['nuc', 'Núcleo', 'Atividades ligadas a dois ou mais temas.'], ['gen', 'Genéricas', 'Marcadas como G: qualquer concorrente pode fazer.']];
    alvo.innerHTML = '<figure class="msa" data-mapa="aluno">' +
      '<div class="msa-legenda"><span class="msa-leg msa-leg-tema"><i></i>Tema</span><span class="msa-leg msa-leg-ativ"><i></i>Atividade</span>' +
      '<span class="msa-leg msa-leg-fina"><i></i>Atividade sustenta o tema</span><span class="msa-leg msa-leg-C"><i></i>C: Consistência</span><span class="msa-leg msa-leg-R"><i></i>R: Reforço</span><span class="msa-leg msa-leg-O"><i></i>O: Otimização</span>' +
      '<button type="button" class="msa-ampliar" aria-pressed="false">Ampliar o mapa</button></div>' +
      '<div class="msa-cats" role="group" aria-label="Destacar no mapa"><span class="msa-cats-rot">Destacar:</span>' + cats.map(function (c) {
        return '<button type="button" class="msa-cat msa-c-' + c[0] + '" data-cat="' + c[0] + '" aria-pressed="false" title="' + c[2] + '"><i></i>' + c[1] + '</button>';
      }).join('') + '</div>' +
      '<div class="msa-palco" tabindex="0"><svg class="msa-svg" viewBox="' + vbX.toFixed(1) + ' ' + vbY.toFixed(1) + ' ' + vbW.toFixed(1) + ' ' + vbH.toFixed(1) + '" role="group" aria-label="Mapa do sistema de atividades da empresa analisada">' + defs +
      '<g class="msa-ligacoes">' + lin.join('') + '</g><g class="msa-nos">' + nos.join('') + '</g><g class="msa-sinais">' + sinais.join('') + '</g></svg></div>' +
      '<p class="msa-arraste">Arraste o mapa para os lados para vê-lo inteiro.</p>' +
      '<div class="msa-painel" aria-live="polite"><p class="msa-dica">Clique em um nó para acompanhar as ligações dele.</p></div></figure>';
    ligar(alvo.querySelector('.msa'));
  }

  function iniciar() {
    document.querySelectorAll('.msa[data-mapa]').forEach(ligar);
    document.querySelectorAll('.msa-abas').forEach(ligarAbas);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar();

  window.MAPAS = { ligar: ligar, desenhar: desenhar };
})();
