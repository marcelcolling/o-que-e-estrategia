/*
 * Caso Vivelar (Aula 1, seção 7): modelo mensal do Apêndice A e o simulador da página.
 *
 * Com as premissas do material (PADRAO), o modelo reproduz as tabelas 7.6 a 7.8:
 * acumulados, cruzamentos (meses 19, 28 e 34), valores presentes e as duas sensibilidades.
 * O teste de ponta a ponta confere esses números. Se mudar o modelo, rode o teste.
 *
 * API: window.VIVELAR = { PADRAO, simular(p), montar(el, aoMudar) }
 */
(function () {
  'use strict';

  var PADRAO = { janelaFim: 12, perda: 14, precoIndep: 41, ganho: 60, fimRampa: 24, imitacao: 0, repasse: 39, taxa: 15 };
  var MERCADO = 1125000;

  var CONTROLES = [
    { k: 'janelaFim', rot: 'Fim da janela de liderança de A', un: 'mês', min: 6, max: 24, passo: 1, dica: 'Até quando A vende 5% a mais antes de os rivais alcançarem (depois, a vantagem some em 6 meses).' },
    { k: 'perda', rot: 'Perda de volume nas redes em B', un: '%', min: 0, max: 30, passo: 1, dica: 'Quanto B perde nas redes ao parar de financiar tabloides e espaço.' },
    { k: 'precoIndep', rot: 'Preço ao lojista independente em B', un: 'R$', min: 39, max: 44, passo: 0.5, dica: 'Preço que o independente paga a partir do mês 7.' },
    { k: 'ganho', rot: 'Ganho de volume nos independentes em B', un: '%', min: 0, max: 100, passo: 5, dica: 'Crescimento total do volume nos independentes ao fim da rampa.' },
    { k: 'fimRampa', rot: 'Mês em que o ganho de B se completa', un: 'mês', min: 12, max: 48, passo: 1, dica: 'A rampa começa no mês 7 e cresce em linha reta até este mês.' },
    { k: 'imitacao', rot: 'O líder replica B a partir do mês', un: '', min: 0, max: 0, passo: 1, opcoes: [[0, 'Não replica'], [13, 'Mês 13'], [19, 'Mês 19'], [25, 'Mês 25'], [31, 'Mês 31']], dica: 'Com imitação, em 12 meses o ganho nos independentes cai pela metade e o preço cai até o preço de repasse.' },
    { k: 'repasse', rot: 'Preço ao PDV depois do repasse (mês 13)', un: 'R$', min: 37, max: 40, passo: 0.5, dica: 'Quanto do ganho de produtividade do setor vai para o canal.' },
    { k: 'taxa', rot: 'Taxa de desconto para o valor presente', un: '% a.a.', min: 5, max: 30, passo: 1, dica: 'Usada só no valor presente.' }
  ];
  var PRESETS = [
    { nome: 'Premissas do material', p: {} },
    { nome: 'B com imitação (7.8)', p: { imitacao: 19 } },
    { nome: 'B com rampa lenta (7.8)', p: { fimRampa: 36 } }
  ];
  var CEN = [
    { k: 'Z', nome: 'Inércia', cor: '#2a78d6' },
    { k: 'A', nome: 'A · EO pura', cor: '#eb6834' },
    { k: 'B', nome: 'B · EO + posição', cor: '#1baf7a' }
  ];

  function completo(p) {
    var o = {};
    Object.keys(PADRAO).forEach(function (k) { o[k] = (p && p[k] != null && !isNaN(Number(p[k]))) ? Number(p[k]) : PADRAO[k]; });
    return o;
  }

  function simular(p0) {
    var p = completo(p0);
    var r = Math.round((Math.pow(1 + p.taxa / 100, 1 / 12) - 1) * 10000) / 10000; // "≈ 1,17% ao mês" para 15% a.a.
    var M = 48, Z = [], A = [], B = [], vZ = [], vA = [], vB = [];
    var perda = p.perda / 100, ganho = p.ganho / 100;
    function bonusA(m) {
      if (m >= 4 && m <= p.janelaFim) return 0.05;
      if (m > p.janelaFim && m <= p.janelaFim + 6) return 0.05 * (p.janelaFim + 6 - m) / 6;
      return 0;
    }
    for (var m = 1; m <= M; m++) {
      var preco = m >= 13 ? p.repasse : 40;
      var cpv = m >= 4 ? 15 : 16;
      // Cenário 0: não acompanha a fronteira
      var l = m >= 7 ? Math.min(0.09, 0.005 * (m - 6)) : 0;
      vZ.push(90000 * (1 - l));
      Z.push((90000 * (1 - l) * (preco - 16) - 1.1e6) / 1e6);
      // Cenário A: EO pura
      var b = bonusA(m);
      vA.push(90000 * (1 + b));
      A.push((90000 * (1 + b) * (preco - cpv) - 1.1e6 - (m <= 6 ? 0.5e6 : 0) - (m >= 4 ? 40e3 : 0)) / 1e6);
      // Cenário B: tudo de A + posição nos independentes
      var lr = m >= 4 ? Math.min(perda, perda * (m - 3) / 6) : 0;
      var g = m >= 7 ? Math.min(ganho, ganho * (m - 6) / Math.max(1, p.fimRampa - 6)) : 0;
      var pi = m >= 7 ? p.precoIndep : preco;
      if (p.imitacao && m >= p.imitacao) {
        var k = Math.min(1, (m - p.imitacao + 1) / 12);
        g = g * (1 - 0.5 * k);
        pi = p.precoIndep - (p.precoIndep - p.repasse) * k;
      }
      var vr = 49000 * (1 - lr) * (1 + b), vi = 41000 * (1 + g) * (1 + b);
      var cs = m >= 4 ? 2.3 : 0;
      vB.push(vr + vi);
      B.push((vr * (preco - cpv) + vi * (pi - cpv - cs) - 1.1e6 - (m <= 6 ? 0.5e6 : 0) - (m <= 9 ? 2.4e6 / 9 : 0) - (m >= 4 ? 140e3 : 0)) / 1e6);
    }
    function acum(x) { var s = 0; return x.map(function (v) { s += v; return s; }); }
    function vp(x, n) { var s = 0; for (var i = 0; i < n; i++) s += x[i] / Math.pow(1 + r, i + 1); return s; }
    function cruza(a, b) { // primeiro mês a partir do qual o acumulado de a fica acima do de b até o fim
      var ca = acum(a), cb = acum(b), achou = null;
      for (var i = ca.length - 1; i >= 0; i--) { if (ca[i] > cb[i]) achou = i + 1; else break; }
      return achou;
    }
    var serie = { Z: Z, A: A, B: B }, vol = { Z: vZ, A: vA, B: vB }, out = { p: p, taxaMes: r, mensal: serie, acum: {}, k: {} };
    CEN.forEach(function (c) {
      var ac = acum(serie[c.k]);
      out.acum[c.k] = ac;
      out.k[c.k] = {
        ac6: ac[5], ac12: ac[11], ac18: ac[17], ac24: ac[23], ac30: ac[29], ac36: ac[35],
        m36: serie[c.k][35], sh18: vol[c.k][17] / MERCADO, sh36: vol[c.k][35] / MERCADO,
        vp36: vp(serie[c.k], 36), vp48: vp(serie[c.k], 48)
      };
    });
    out.cruz = { AZ: cruza(A, Z), BZ: cruza(B, Z), BA: cruza(B, A) };
    return out;
  }

  /* ---------------------------------------------------------------- interface */
  var esc = function (s) { return window.VD ? VD.esc(s) : String(s); };
  function f1(x) { return x.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }); }
  function f2(x) { return x.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
  function pct(x) { return (x * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%'; }
  function valorTxt(c, v) {
    if (c.opcoes) { for (var i = 0; i < c.opcoes.length; i++) if (c.opcoes[i][0] === v) return c.opcoes[i][1]; return String(v); }
    if (c.un === 'R$') return 'R$ ' + v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    if (c.un === 'mês') return 'mês ' + v;
    return v.toLocaleString('pt-BR') + (c.un ? ' ' + c.un : '');
  }
  function mudancas(p) {
    return CONTROLES.filter(function (c) { return p[c.k] !== PADRAO[c.k]; });
  }
  function descreverMudancas(p) {
    var m = mudancas(p);
    if (!m.length) return 'Premissas do material';
    return m.map(function (c) { return c.rot + ': ' + valorTxt(c, p[c.k]) + ' (material: ' + valorTxt(c, PADRAO[c.k]) + ')'; }).join('; ');
  }
  function mesTxt(x) { return x ? 'mês ' + x : 'nunca, até o mês 48'; }

  function montar(el, aoMudar) {
    var estado = { p: completo({}), exp: [], modo: 'acum' };
    var base = simular({});
    el.innerHTML =
      '<div class="sim-presets" role="group" aria-label="Cenários prontos"></div>' +
      '<div class="sim-grade">' +
        '<div class="sim-controles"></div>' +
        '<div class="sim-saida">' +
          '<div class="sim-aviso" hidden></div>' +
          '<div class="sim-graf-cab"><div class="sim-legenda"></div><div class="sim-modo" role="group" aria-label="O que o gráfico mostra">' +
            '<button type="button" data-modo="acum" aria-pressed="true">Acumulado</button><button type="button" data-modo="mensal" aria-pressed="false">Mensal</button></div></div>' +
          '<div class="sim-graf"><svg class="sim-svg" viewBox="0 0 640 300" role="img"></svg><div class="sim-tip" hidden></div></div>' +
          '<p class="sim-cruz"></p>' +
          '<div class="tabela-wrap"><table class="tabela sim-tab"></table></div>' +
          '<details class="sim-mes"><summary>Tabela mês a mês</summary><div class="sim-mes-corpo"></div></details>' +
        '</div>' +
      '</div>' +
      '<div class="sim-registro">' +
        '<div class="sim-reg-cab"><div><strong>Registro de experimentos</strong><span>Mudou uma premissa? Registre o resultado e escreva o que mudou na conclusão.</span></div>' +
        '<button type="button" class="vd-btn vd-btn-roxo sim-reg-btn">+ Registrar este experimento</button></div>' +
        '<ol class="sim-exps"></ol>' +
      '</div>';

    var $ = function (s) { return el.querySelector(s); };
    $('.sim-presets').innerHTML = PRESETS.map(function (pr, i) { return '<button type="button" class="sim-preset" data-i="' + i + '">' + esc(pr.nome) + '</button>'; }).join('');
    $('.sim-controles').innerHTML = CONTROLES.map(function (c) {
      var entrada = c.opcoes
        ? '<select data-k="' + c.k + '">' + c.opcoes.map(function (o) { return '<option value="' + o[0] + '">' + esc(o[1]) + '</option>'; }).join('') + '</select>'
        : '<input type="range" data-k="' + c.k + '" min="' + c.min + '" max="' + c.max + '" step="' + c.passo + '">';
      return '<div class="sim-ctl" data-k="' + c.k + '"><div class="sim-ctl-top"><label>' + esc(c.rot) + '</label>' +
        '<output></output></div>' + entrada +
        '<div class="sim-ctl-pe"><span>Material: ' + esc(valorTxt(c, PADRAO[c.k])) + '</span><button type="button" class="sim-reset" data-k="' + c.k + '" title="Voltar ao valor do material">↺</button></div>' +
        '<p class="sim-dica">' + esc(c.dica) + '</p></div>';
    }).join('');
    $('.sim-legenda').innerHTML = CEN.map(function (c) { return '<span><i style="background:' + c.cor + '"></i>' + esc(c.nome) + '</span>'; }).join('');

    function setP(k, v) { estado.p[k] = Number(v); render(); avisar(); }
    function avisar() { if (aoMudar) aoMudar(); }

    el.addEventListener('input', function (e) {
      var k = e.target.dataset && e.target.dataset.k;
      if (k && (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT')) setP(k, e.target.value);
    });
    el.addEventListener('change', function (e) {
      var k = e.target.dataset && e.target.dataset.k;
      if (k && e.target.tagName === 'SELECT') setP(k, e.target.value);
    });
    el.addEventListener('click', function (e) {
      var t = e.target.closest('button');
      if (!t || !el.contains(t)) return;
      if (t.classList.contains('sim-preset')) { estado.p = completo(PRESETS[Number(t.dataset.i)].p); render(); avisar(); }
      else if (t.classList.contains('sim-reset')) { setP(t.dataset.k, PADRAO[t.dataset.k]); }
      else if (t.dataset.modo) { estado.modo = t.dataset.modo; render(); }
      else if (t.classList.contains('sim-reg-btn')) {
        var s = simular(estado.p);
        estado.exp.push({
          quando: Date.now(), p: JSON.parse(JSON.stringify(estado.p)), conclusao: '',
          r: { ac18: [s.k.Z.ac18, s.k.A.ac18, s.k.B.ac18], ac36: [s.k.Z.ac36, s.k.A.ac36, s.k.B.ac36], m36: [s.k.Z.m36, s.k.A.m36, s.k.B.m36], cruz: s.cruz }
        });
        renderExps(); avisar();
        var tas = el.querySelectorAll('.sim-exp textarea');
        if (tas.length) tas[tas.length - 1].focus();
      } else if (t.classList.contains('sim-exp-x')) {
        if (window.confirm('Remover este experimento do registro?')) { estado.exp.splice(Number(t.dataset.i), 1); renderExps(); avisar(); }
      }
    });
    el.addEventListener('input', function (e) {
      if (e.target.classList && e.target.classList.contains('sim-exp-txt')) { estado.exp[Number(e.target.dataset.i)].conclusao = e.target.value; }
    });

    /* ----- gráfico ----- */
    var svg = $('.sim-svg'), tip = $('.sim-tip');
    var G = { l: 46, r: 92, t: 14, b: 34, w: 640, h: 300 };
    var ultimo = null;
    function desenhar(s) {
      ultimo = s;
      // o gráfico é desenhado na largura real do contêiner, para o texto não encolher no celular
      var larg = Math.round(svg.parentNode.clientWidth - 10);
      if (larg > 200) G.w = Math.max(320, Math.min(900, larg));
      G.h = G.w < 500 ? 260 : 300;
      svg.setAttribute('viewBox', '0 0 ' + G.w + ' ' + G.h);
      var dados = estado.modo === 'acum' ? s.acum : s.mensal;
      var todos = [].concat(dados.Z, dados.A, dados.B);
      var lo = Math.min(0, Math.min.apply(null, todos)), hi = Math.max.apply(null, todos);
      var passo = estado.modo === 'acum' ? (hi - lo > 40 ? 10 : 5) : 0.25;
      lo = Math.floor(lo / passo) * passo; hi = Math.ceil(hi / passo) * passo;
      var W = G.w - G.l - G.r, H = G.h - G.t - G.b;
      var x = function (m) { return G.l + (m - 1) / 47 * W; };
      var y = function (v) { return G.t + (hi - v) / (hi - lo) * H; };
      var h = [];
      for (var v = lo; v <= hi + 1e-9; v += passo) {
        h.push('<line class="g-grade" x1="' + G.l + '" x2="' + (G.l + W) + '" y1="' + y(v) + '" y2="' + y(v) + '"/>');
        h.push('<text class="g-ax" x="' + (G.l - 6) + '" y="' + (y(v) + 4) + '" text-anchor="end">' + (estado.modo === 'acum' ? v.toLocaleString('pt-BR') : f2(v)) + '</text>');
      }
      if (lo < 0) h.push('<line class="g-zero" x1="' + G.l + '" x2="' + (G.l + W) + '" y1="' + y(0) + '" y2="' + y(0) + '"/>');
      [1, 6, 12, 18, 24, 30, 36, 42, 48].forEach(function (m) {
        h.push('<text class="g-ax" x="' + x(m) + '" y="' + (G.t + H + 18) + '" text-anchor="middle">' + m + '</text>');
      });
      h.push('<text class="g-ax" x="' + (G.l + W / 2) + '" y="' + (G.h - 2) + '" text-anchor="middle">mês</text>');
      [[18, 'horizonte de 18 meses'], [36, 'mês 36']].forEach(function (mk) {
        h.push('<line class="g-marco" x1="' + x(mk[0]) + '" x2="' + x(mk[0]) + '" y1="' + G.t + '" y2="' + (G.t + H) + '"/>');
        h.push('<text class="g-marco-txt" x="' + (x(mk[0]) + 4) + '" y="' + (G.t + 10) + '">' + mk[1] + '</text>');
      });
      // linhas + rótulos diretos no fim (com afastamento para não colidir)
      var fins = CEN.map(function (c) { return { c: c, y: y(dados[c.k][47]) }; }).sort(function (a, b) { return a.y - b.y; });
      for (var i = 1; i < fins.length; i++) if (fins[i].y - fins[i - 1].y < 14) fins[i].y = fins[i - 1].y + 14;
      CEN.forEach(function (c) {
        var d = dados[c.k].map(function (v, i) { return (i ? 'L' : 'M') + x(i + 1).toFixed(1) + ' ' + y(v).toFixed(1); }).join(' ');
        h.push('<path d="' + d + '" fill="none" stroke="' + c.cor + '" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>');
      });
      fins.forEach(function (f) {
        h.push('<text class="g-rot" x="' + (G.l + W + 6) + '" y="' + (f.y + 4) + '">' + esc(f.c.nome.split(' · ')[0]) + ' ' + f1(dados[f.c.k][47]) + '</text>');
      });
      h.push('<line class="g-cruz" x1="0" x2="0" y1="' + G.t + '" y2="' + (G.t + H) + '" visibility="hidden"/>');
      CEN.forEach(function (c) { h.push('<circle class="g-pt" data-k="' + c.k + '" r="4.5" fill="' + c.cor + '" stroke="#fff" stroke-width="2" visibility="hidden"/>'); });
      h.push('<rect class="g-hit" x="' + G.l + '" y="' + G.t + '" width="' + W + '" height="' + H + '" fill="transparent"/>');
      svg.innerHTML = h.join('');
      svg.setAttribute('aria-label', 'EBITDA ' + (estado.modo === 'acum' ? 'acumulado' : 'mensal') + ' em R$ milhões, meses 1 a 48, nos três cenários. Valores no mês 48: ' +
        CEN.map(function (c) { return c.nome + ' ' + f1(dados[c.k][47]); }).join(', ') + '.');
      var hit = svg.querySelector('.g-hit');
      function mover(ev) {
        var r = svg.getBoundingClientRect();
        var px = (ev.clientX - r.left) / r.width * G.w;
        var m = Math.max(1, Math.min(48, Math.round((px - G.l) / W * 47) + 1));
        var cz = svg.querySelector('.g-cruz');
        cz.setAttribute('x1', x(m)); cz.setAttribute('x2', x(m)); cz.setAttribute('visibility', 'visible');
        svg.querySelectorAll('.g-pt').forEach(function (pt) {
          pt.setAttribute('cx', x(m)); pt.setAttribute('cy', y(dados[pt.dataset.k][m - 1])); pt.setAttribute('visibility', 'visible');
        });
        tip.hidden = false;
        tip.innerHTML = '<strong>Mês ' + m + '</strong>' + CEN.map(function (c) {
          return '<span><i style="background:' + c.cor + '"></i>' + esc(c.nome) + '<b>' + f2(dados[c.k][m - 1]) + '</b></span>';
        }).join('') + '<em>R$ milhões, ' + (estado.modo === 'acum' ? 'acumulado' : 'no mês') + '</em>';
        var left = (x(m) / G.w) * r.width;
        tip.style.left = Math.min(Math.max(8, left + 12), r.width - tip.offsetWidth - 8) + 'px';
      }
      function sair() {
        tip.hidden = true;
        svg.querySelectorAll('.g-pt, .g-cruz').forEach(function (n) { n.setAttribute('visibility', 'hidden'); });
      }
      hit.addEventListener('pointermove', mover);
      hit.addEventListener('pointerdown', mover);
      hit.addEventListener('pointerleave', sair);
    }

    function tabela(s) {
      var linhas = [
        ['EBITDA acumulado em 18 meses (R$ mi)', 'ac18', f1],
        ['EBITDA acumulado em 36 meses (R$ mi)', 'ac36', f1],
        ['EBITDA mensal no mês 36 (R$ mi)', 'm36', f2],
        ['Participação de mercado no mês 18', 'sh18', pct],
        ['Participação de mercado no mês 36', 'sh36', pct],
        ['Valor presente do EBITDA em 36 meses (R$ mi)', 'vp36', f1],
        ['Valor presente do EBITDA em 48 meses (R$ mi)', 'vp48', f1]
      ];
      var mudou = mudancas(estado.p).length > 0;
      var h = '<thead><tr><th>Indicador</th>' + CEN.map(function (c) { return '<th><i class="sw" style="background:' + c.cor + '"></i>' + esc(c.nome) + '</th>'; }).join('') + '</tr></thead><tbody>';
      linhas.forEach(function (l) {
        var vals = CEN.map(function (c) { return s.k[c.k][l[1]]; });
        var max = Math.max.apply(null, vals);
        h += '<tr><td data-label="Indicador">' + esc(l[0]) + '</td>' + CEN.map(function (c, i) {
          var v = vals[i], b = base.k[c.k][l[1]];
          var dif = mudou && l[2](v) !== l[2](b) ? '<small>material: ' + l[2](b) + '</small>' : '';
          return '<td data-label="' + esc(c.nome) + '"' + (v === max ? ' class="melhor"' : '') + '>' + l[2](v) + dif + '</td>';
        }).join('') + '</tr>';
      });
      $('.sim-tab').innerHTML = h + '</tbody>';
      $('.sim-cruz').innerHTML = '<strong>Cruzamentos no acumulado:</strong> A supera a inércia: ' + mesTxt(s.cruz.AZ) +
        ' · B supera a inércia: ' + mesTxt(s.cruz.BZ) + ' · <strong>B supera A: ' + mesTxt(s.cruz.BA) + '</strong>';
      var det = $('.sim-mes');
      if (det.open) tabelaMes(s);
      det.ontoggle = function () { if (det.open) tabelaMes(simular(estado.p)); };
    }
    function tabelaMes(s) {
      var h = '<table class="tabela"><thead><tr><th>Mês</th>' + CEN.map(function (c) { return '<th>' + esc(c.nome) + ' (mensal)</th><th>acumulado</th>'; }).join('') + '</tr></thead><tbody>';
      for (var m = 0; m < 48; m++) {
        h += '<tr><td>' + (m + 1) + '</td>' + CEN.map(function (c) { return '<td>' + f2(s.mensal[c.k][m]) + '</td><td>' + f1(s.acum[c.k][m]) + '</td>'; }).join('') + '</tr>';
      }
      $('.sim-mes-corpo').innerHTML = h + '</tbody></table>';
    }

    function renderControles() {
      CONTROLES.forEach(function (c) {
        var box = el.querySelector('.sim-ctl[data-k="' + c.k + '"]');
        var inp = box.querySelector('[data-k]');
        if (String(inp.value) !== String(estado.p[c.k])) inp.value = estado.p[c.k];
        box.querySelector('output').textContent = valorTxt(c, estado.p[c.k]);
        box.classList.toggle('mudou', estado.p[c.k] !== PADRAO[c.k]);
      });
      var n = mudancas(estado.p).length, av = $('.sim-aviso');
      av.hidden = n < 2;
      av.textContent = 'Você mudou ' + n + ' premissas ao mesmo tempo. Para saber o efeito de cada uma, o Apêndice A sugere mudar uma por vez.';
      el.querySelectorAll('.sim-preset').forEach(function (b, i) {
        b.classList.toggle('ativo', JSON.stringify(completo(PRESETS[i].p)) === JSON.stringify(estado.p));
      });
      el.querySelectorAll('[data-modo]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.modo === estado.modo)); });
    }

    function renderExps() {
      var ol = $('.sim-exps');
      if (!estado.exp.length) { ol.innerHTML = '<li class="sim-vazio">Nenhum experimento registrado ainda.</li>'; return; }
      ol.innerHTML = estado.exp.map(function (x, i) {
        var r = x.r;
        return '<li class="sim-exp"><div class="sim-exp-cab"><span class="sim-exp-n">' + (i + 1) + '</span><span class="sim-exp-p">' + esc(descreverMudancas(completo(x.p))) + '</span>' +
          '<button type="button" class="sim-exp-x" data-i="' + i + '" aria-label="Remover experimento ' + (i + 1) + '">✕</button></div>' +
          '<p class="sim-exp-r">Acumulado em 36 meses: inércia ' + f1(r.ac36[0]) + ' · A ' + f1(r.ac36[1]) + ' · B ' + f1(r.ac36[2]) +
          ' &nbsp;|&nbsp; Mensal no mês 36: A ' + f2(r.m36[1]) + ' · B ' + f2(r.m36[2]) + ' &nbsp;|&nbsp; B supera A: ' + mesTxt(r.cruz.BA) + '</p>' +
          '<label><span>O que mudou na conclusão?</span><textarea class="sim-exp-txt" data-i="' + i + '" rows="2" placeholder="Ex.: com perda de 25% nas redes, B nunca supera A; a posição só se paga se…"></textarea></label></li>';
      }).join('');
      ol.querySelectorAll('.sim-exp-txt').forEach(function (ta) { ta.value = estado.exp[Number(ta.dataset.i)].conclusao || ''; });
    }

    function render() {
      var s = simular(estado.p);
      renderControles();
      desenhar(s);
      tabela(s);
    }
    render();
    renderExps();
    var tRes = null;
    window.addEventListener('resize', function () { clearTimeout(tRes); tRes = setTimeout(function () { if (ultimo) desenhar(ultimo); }, 150); });

    return {
      coletar: function () { return { p: estado.p, exp: estado.exp }; },
      aplicar: function (d) {
        estado.p = completo(d && d.p);
        estado.exp = (d && Array.isArray(d.exp)) ? d.exp.map(function (x) { return { quando: x.quando, p: x.p, r: x.r, conclusao: String(x.conclusao || '') }; }) : [];
        render(); renderExps();
      },
      resumo: function (d) {
        var linhas = [['Simulador Vivelar', 'Premissas na tela', descreverMudancas(completo(d && d.p))]];
        ((d && d.exp) || []).forEach(function (x, i) {
          var r = x.r || {}, ac = r.ac36 || [0, 0, 0];
          linhas.push(['Simulador Vivelar', 'Experimento ' + (i + 1) + ': ' + descreverMudancas(completo(x.p)),
            'Acumulado em 36 meses: inércia ' + f1(ac[0]) + ', A ' + f1(ac[1]) + ', B ' + f1(ac[2]) + '. B supera A: ' + mesTxt(r.cruz && r.cruz.BA) +
            '. O que mudou na conclusão: ' + (x.conclusao || '—')]);
        });
        return linhas;
      },
      contar: function () { return estado.exp.length; }
    };
  }

  window.VIVELAR = { PADRAO: PADRAO, simular: simular, montar: montar, descrever: descreverMudancas };
})();
