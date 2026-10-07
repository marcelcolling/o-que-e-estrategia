/*
 * Página de uma parte do artigo: liga as caixas de atividade, os destaques e as anotações
 * nos parágrafos e os widgets (fronteira, portfólio, troca de logo, simulador) ao portal.js.
 *
 * Formato salvo (uma atividade por aula: aula1, aula2...):
 *   { v: 1, campos: { chave: texto | opção | true }, notas: { "3": texto }, destaques: [3, 8],
 *     fronteira: {...}, portfolio: [...], logo: [...], simulador: { p, exp } }
 * As chaves de "campos" vêm do atributo data-campo do HTML. Não renomeie chaves em uso.
 */
(function () {
  'use strict';
  var esc = function (s) { return VD.esc(s); };
  var CORES = ['#2a78d6', '#eb6834', '#1baf7a', '#8C8A80'];

  /* ================================================================ widgets */
  var W = {};

  /* ----- Bloco 3: três empresas na fronteira ----- */
  function fronteiraY(x) { return 88 * Math.sqrt(Math.max(0, 1 - Math.pow(x / 100, 3))); }
  W.fronteira = function (el) {
    var d = [];
    // posições iniciais diferentes, para os pontos não começarem sobrepostos
    var INICIO = [{ custo: 25, valor: 35 }, { custo: 55, valor: 55 }, { custo: 80, valor: 25 }];
    function vazio() { return INICIO.map(function (p) { return { nome: '', custo: p.custo, valor: p.valor, just: '' }; }); }
    el.innerHTML = '<div class="fr-grade"><div class="fr-cartoes"></div><div class="fr-graf"><svg viewBox="0 0 400 300" role="img" aria-label="Posição das três empresas em relação à fronteira de produtividade"></svg></div></div>';
    var cartoes = el.querySelector('.fr-cartoes'), svg = el.querySelector('svg');
    function status(e) {
      var f = fronteiraY(e.custo);
      if (e.valor > f + 0.5) return { t: 'Acima da fronteira não existe: a fronteira é o máximo possível hoje.', c: 'fora' };
      if (f - e.valor <= 6) return { t: 'Na fronteira: a escolha é de posição.', c: 'na' };
      return { t: 'Abaixo da fronteira: há espaço para EO.', c: 'abaixo' };
    }
    function montarCartoes() {
      cartoes.innerHTML = d.map(function (e, i) {
        return '<div class="fr-cartao" data-i="' + i + '"><div class="fr-cab"><i style="background:' + CORES[i] + '"></i>' +
          '<input type="text" class="fr-nome" maxlength="60" placeholder="Empresa ' + (i + 1) + '" aria-label="Nome da empresa ' + (i + 1) + '"></div>' +
          '<label class="fr-sl"><span>Custo relativo <em>alto → baixo</em></span><input type="range" class="fr-custo" min="0" max="100"></label>' +
          '<label class="fr-sl"><span>Valor além do preço <em>baixo → alto</em></span><input type="range" class="fr-valor" min="0" max="100"></label>' +
          '<p class="fr-status"></p>' +
          '<textarea class="fr-just" rows="2" placeholder="Por que ela está nesse ponto? Cite atividades."></textarea></div>';
      }).join('');
      cartoes.querySelectorAll('.fr-cartao').forEach(function (c, i) {
        c.querySelector('.fr-nome').value = d[i].nome;
        c.querySelector('.fr-custo').value = d[i].custo;
        c.querySelector('.fr-valor').value = d[i].valor;
        c.querySelector('.fr-just').value = d[i].just;
      });
    }
    function desenhar() {
      var X = function (v) { return 40 + v * 3.4; }, Y = function (v) { return 270 - v * 2.5; };
      var curva = [];
      for (var x = 0; x <= 100; x += 2) curva.push((x ? 'L' : 'M') + X(x).toFixed(1) + ' ' + Y(fronteiraY(x)).toFixed(1));
      var h = '<rect x="40" y="20" width="340" height="250" rx="6" fill="#EFEEE7"/>' +
        '<path d="' + curva.join(' ') + '" fill="none" stroke="#1F3A5F" stroke-width="3"/>' +
        '<text x="44" y="292" class="fr-ax">custo alto</text><text x="376" y="292" text-anchor="end" class="fr-ax">custo baixo</text>' +
        '<text x="14" y="150" class="fr-ax" transform="rotate(-90 14 150)" text-anchor="middle">valor além do preço</text>' +
        '<text x="200" y="36" class="fr-ax fr-ax-f">fronteira de produtividade</text>';
      d.forEach(function (e, i) {
        var v = Math.min(e.valor, fronteiraY(e.custo));
        h += '<circle cx="' + X(e.custo) + '" cy="' + Y(v) + '" r="9" fill="' + CORES[i] + '" stroke="#fff" stroke-width="2"/>' +
          // perto da borda direita, o rótulo vai para a esquerda do ponto
          '<text x="' + (e.custo > 62 ? X(e.custo) - 13 : X(e.custo) + 13) + '" y="' + (Y(v) + 4) + '"' + (e.custo > 62 ? ' text-anchor="end"' : '') + ' class="fr-pt">' + esc(e.nome || 'Empresa ' + (i + 1)) + '</text>';
      });
      svg.innerHTML = h;
      cartoes.querySelectorAll('.fr-cartao').forEach(function (c, i) {
        var s = status(d[i]), p = c.querySelector('.fr-status');
        p.textContent = s.t; p.className = 'fr-status ' + s.c;
      });
    }
    el.addEventListener('input', function (e) {
      var c = e.target.closest('.fr-cartao'); if (!c) return;
      var i = Number(c.dataset.i);
      d[i] = { nome: c.querySelector('.fr-nome').value, custo: Number(c.querySelector('.fr-custo').value), valor: Number(c.querySelector('.fr-valor').value), just: c.querySelector('.fr-just').value };
      desenhar();
    });
    return {
      coletar: function () { return d.some(function (e, i) { return e.nome || e.just || e.custo !== INICIO[i].custo || e.valor !== INICIO[i].valor; }) ? d : null; },
      aplicar: function (v) {
        d = vazio();
        if (Array.isArray(v)) v.slice(0, 3).forEach(function (e, i) { d[i] = { nome: String(e.nome || ''), custo: Number(e.custo) || 0, valor: Number(e.valor) || 0, just: String(e.just || '') }; });
        montarCartoes(); desenhar();
      },
      resumo: function (v) {
        return (v || []).map(function (e, i) {
          var s = status(e);
          return ['Bloco 3 · Fronteira de produtividade', 'Empresa ' + (i + 1) + ': ' + (e.nome || '—'),
            'Custo ' + e.custo + '/100 (0 = alto), valor ' + e.valor + '/100. ' + s.t + ' Justificativa: ' + (e.just || '—')];
        });
      },
      respondido: function (v) { return !!(v && v.some(function (e) { return e.nome && e.just; })); }
    };
  };

  /* ----- Bloco 6: portfólio de iniciativas ----- */
  var CATS = [['paridade', 'EO de paridade'], ['lideranca', 'EO de liderança temporária'], ['posicao', 'Reforço de posição'], ['naosei', 'Não sei']];
  W.portfolio = function (el) {
    var d = [];
    el.innerHTML = '<div class="pf-linhas"></div><button type="button" class="btn-add pf-add">+ Iniciativa</button><div class="pf-barra" aria-live="polite"></div>';
    var linhas = el.querySelector('.pf-linhas');
    function montar() {
      linhas.innerHTML = d.map(function (r, i) {
        return '<div class="pf-linha" data-i="' + i + '"><input type="text" class="pf-nome" maxlength="140" placeholder="Iniciativa ' + (i + 1) + '" aria-label="Iniciativa ' + (i + 1) + '">' +
          '<select class="pf-cat" aria-label="Categoria da iniciativa ' + (i + 1) + '"><option value="">Classifique…</option>' +
          CATS.map(function (c) { return '<option value="' + c[0] + '">' + c[1] + '</option>'; }).join('') + '</select>' +
          '<button type="button" class="pf-x" aria-label="Remover iniciativa ' + (i + 1) + '">✕</button></div>';
      }).join('');
      linhas.querySelectorAll('.pf-linha').forEach(function (l, i) { l.querySelector('.pf-nome').value = d[i].nome; l.querySelector('.pf-cat').value = d[i].cat; });
      barra();
    }
    function barra() {
      var n = {}, tot = 0;
      d.forEach(function (r) { if (r.cat) { n[r.cat] = (n[r.cat] || 0) + 1; tot++; } });
      var b = el.querySelector('.pf-barra');
      if (!tot) { b.innerHTML = '<p class="pf-vazio">Classifique as iniciativas para ver a proporção.</p>'; return; }
      b.innerHTML = '<div class="pf-stack">' + CATS.map(function (c, i) {
        return n[c[0]] ? '<span style="flex:' + n[c[0]] + ';background:' + CORES[i] + '" title="' + c[1] + ': ' + n[c[0]] + '"></span>' : '';
      }).join('') + '</div><ul class="pf-leg">' + CATS.map(function (c, i) {
        return n[c[0]] ? '<li><i style="background:' + CORES[i] + '"></i>' + c[1] + ' <b>' + n[c[0]] + '</b> (' + Math.round(n[c[0]] / tot * 100) + '%)</li>' : '';
      }).join('') + '</ul>';
    }
    el.addEventListener('input', function (e) {
      var l = e.target.closest('.pf-linha'); if (!l) return;
      var i = Number(l.dataset.i);
      d[i] = { nome: l.querySelector('.pf-nome').value, cat: l.querySelector('.pf-cat').value };
      barra();
    });
    el.addEventListener('change', function (e) { if (e.target.classList.contains('pf-cat')) e.target.dispatchEvent(new Event('input', { bubbles: true })); });
    el.addEventListener('click', function (e) {
      if (e.target.closest('.pf-add')) { d.push({ nome: '', cat: '' }); montar(); var ins = linhas.querySelectorAll('.pf-nome'); ins[ins.length - 1].focus(); }
      var x = e.target.closest('.pf-x');
      if (x) { d.splice(Number(x.closest('.pf-linha').dataset.i), 1); if (!d.length) d.push({ nome: '', cat: '' }); montar(); }
    });
    return {
      coletar: function () { var v = d.filter(function (r) { return r.nome || r.cat; }); return v.length ? v : null; },
      aplicar: function (v) {
        d = Array.isArray(v) && v.length ? v.map(function (r) { return { nome: String(r.nome || ''), cat: String(r.cat || '') }; }) : [{ nome: '', cat: '' }, { nome: '', cat: '' }, { nome: '', cat: '' }];
        montar();
      },
      resumo: function (v) {
        return (v || []).map(function (r, i) {
          var c = CATS.filter(function (c) { return c[0] === r.cat; })[0];
          return ['Bloco 6 · Portfólio de iniciativas', 'Iniciativa ' + (i + 1) + ': ' + (r.nome || '—'), c ? c[1] : '—'];
        });
      },
      respondido: function (v) { return !!(v && v.some(function (r) { return r.nome && r.cat; })); }
    };
  };

  /* ----- Bloco 6: teste da troca de logo ----- */
  var PERSP = ['Financeira', 'Clientes', 'Processos internos', 'Aprendizado e crescimento'];
  W.logo = function (el) {
    var d = [];
    el.innerHTML = '<div class="lg-linhas">' + PERSP.map(function (p, i) {
      return '<div class="lg-linha" data-i="' + i + '"><span class="lg-persp">' + p + '</span>' +
        '<textarea class="lg-obj" rows="2" placeholder="Objetivo da sua empresa nesta perspectiva"></textarea>' +
        '<div class="lg-sob" role="group" aria-label="Sobrevive à troca de logo? (' + p + ')"><span>Sobrevive à troca?</span>' +
        '<label class="pilula"><input type="radio" name="lg-' + i + '" value="sim"><span>Sim</span></label>' +
        '<label class="pilula"><input type="radio" name="lg-' + i + '" value="nao"><span>Não</span></label></div></div>';
    }).join('') + '</div><p class="lg-veredito" aria-live="polite"></p>';
    function ler() {
      d = PERSP.map(function (p, i) {
        var l = el.querySelector('.lg-linha[data-i="' + i + '"]'), r = l.querySelector('input:checked');
        return { obj: l.querySelector('.lg-obj').value, sobrevive: r ? r.value : '' };
      });
      veredito();
    }
    function veredito() {
      var sim = d.filter(function (x) { return x.sobrevive === 'sim'; }).length, marc = d.filter(function (x) { return x.sobrevive; }).length;
      el.querySelector('.lg-veredito').textContent = marc ? sim + ' de ' + marc + ' objetivos continuam fazendo sentido para o concorrente. ' +
        (sim === marc ? 'O painel sobrevive à troca: ele mede EO, não a sua diferença.' : sim === 0 ? 'Nenhum sobrevive: o painel descreve uma forma específica de competir.' : 'Veja quais são específicos: é neles que mora a escolha.') : '';
    }
    el.addEventListener('input', ler);
    el.addEventListener('change', ler);
    return {
      coletar: function () { return d.some(function (x) { return x.obj || x.sobrevive; }) ? d : null; },
      aplicar: function (v) {
        PERSP.forEach(function (p, i) {
          var x = (Array.isArray(v) && v[i]) || {}, l = el.querySelector('.lg-linha[data-i="' + i + '"]');
          l.querySelector('.lg-obj').value = String(x.obj || '');
          l.querySelectorAll('input').forEach(function (r) { r.checked = r.value === x.sobrevive; });
        });
        ler();
      },
      resumo: function (v) {
        return (v || []).map(function (x, i) {
          return ['Bloco 6 · Teste da troca de logo', PERSP[i], (x.obj || '—') + ' · Sobrevive à troca: ' + (x.sobrevive === 'sim' ? 'sim' : x.sobrevive === 'nao' ? 'não' : '—')];
        });
      },
      respondido: function (v) { return !!(v && v.some(function (x) { return x.obj; })); }
    };
  };

  /* ----- Bloco 7: simulador ----- */
  W.simulador = function (el) {
    var s = VIVELAR.montar(el, function () { VD.alterado(); });
    return {
      coletar: function () {
        var v = s.coletar();
        var mudou = Object.keys(VIVELAR.PADRAO).some(function (k) { return v.p[k] !== VIVELAR.PADRAO[k]; });
        return (mudou || v.exp.length) ? v : null;
      },
      aplicar: s.aplicar, resumo: s.resumo,
      respondido: function (v) { return !!(v && v.exp && v.exp.length); }
    };
  };

  /* ================================================================ campos simples */
  function campos() { return Array.prototype.slice.call(document.querySelectorAll('[data-campo]')); }

  function coletarCampos() {
    var o = {};
    campos().forEach(function (c) {
      var k = c.dataset.campo;
      if (c.type === 'radio') { if (c.checked) o[k] = c.value; }
      else if (c.type === 'checkbox') { if (c.checked) o[k] = true; }
      else if (c.value.trim()) o[k] = c.value;
    });
    return o;
  }
  function aplicarCampos(o) {
    o = o || {};
    campos().forEach(function (c) {
      var v = o[c.dataset.campo];
      if (c.type === 'radio') c.checked = v != null && String(v) === c.value;
      else if (c.type === 'checkbox') c.checked = v === true;
      else c.value = v == null ? '' : String(v);
    });
  }

  /* ================================================================ parágrafos: destacar e anotar */
  function pars() { return Array.prototype.slice.call(document.querySelectorAll('.par')); }
  function ligarParagrafos() {
    document.addEventListener('click', function (e) {
      var b = e.target.closest('.par-ferr button'); if (!b) return;
      var par = b.closest('.par');
      if (b.classList.contains('b-dest')) {
        var on = !par.classList.contains('destacado');
        par.classList.toggle('destacado', on);
        b.setAttribute('aria-pressed', String(on));
        b.lastChild.textContent = on ? 'Destacado' : 'Destacar';
      } else {
        var box = par.querySelector('.par-nota'), ta = box.querySelector('textarea');
        // abre; se já estiver aberta e vazia, fecha; com texto, só leva o foco à anotação
        if (box.hidden) box.hidden = false;
        else if (!ta.value.trim()) box.hidden = true;
        if (!box.hidden) ta.focus();
        b.classList.toggle('ativo', !box.hidden);
      }
      atualizarProgresso();
    });
  }
  function coletarParagrafos(o) {
    var notas = {}, dest = [];
    pars().forEach(function (p) {
      var n = p.dataset.par, t = p.querySelector('textarea[data-nota]').value;
      if (t.trim()) notas[n] = t;
      if (p.classList.contains('destacado')) dest.push(Number(n));
    });
    if (Object.keys(notas).length) o.notas = notas;
    if (dest.length) o.destaques = dest;
  }
  function aplicarParagrafos(d) {
    var notas = (d && d.notas) || {}, dest = (d && d.destaques) || [];
    pars().forEach(function (p) {
      var n = p.dataset.par, t = notas[n] || '';
      var ta = p.querySelector('textarea[data-nota]');
      ta.value = t;
      p.querySelector('.par-nota').hidden = !t;
      p.querySelector('.b-nota').classList.toggle('ativo', !!t);
      var on = dest.indexOf(Number(n)) >= 0;
      p.classList.toggle('destacado', on);
      var b = p.querySelector('.b-dest');
      b.setAttribute('aria-pressed', String(on));
      b.lastChild.textContent = on ? 'Destacado' : 'Destacar';
    });
  }

  /* ================================================================ resumo legível (planilha) */
  function rotuloOpcao(k, v) {
    var r = document.querySelector('input[type=radio][data-campo="' + k + '"][value="' + (window.CSS && CSS.escape ? CSS.escape(v) : v) + '"]');
    return r ? r.parentNode.textContent.trim() : String(v);
  }
  function resumo(d) {
    d = d || {};
    var c = d.campos || {}, linhas = [], vistos = {};
    var els = document.querySelectorAll('[data-campo], [data-widget], .par');
    Array.prototype.forEach.call(els, function (el) {
      var secaoEl = el.closest('[data-secao]');
      var secao = secaoEl ? secaoEl.dataset.secao : '';
      if (el.classList.contains('par')) {
        var n = el.dataset.par, nota = d.notas && d.notas[n], dest = (d.destaques || []).indexOf(Number(n)) >= 0;
        if (!nota && !dest) return;
        var trecho = el.querySelector('.par-texto p').textContent.trim().slice(0, 90);
        linhas.push(['Texto de Porter · leitura ativa', el.dataset.rotulo + ' · ' + trecho + '…', (dest ? '[destacado] ' : '') + (nota || '')]);
        return;
      }
      if (el.dataset.widget) {
        var w = INST[el.dataset.widget];
        if (w && d[el.dataset.widget]) linhas = linhas.concat(w.resumo(d[el.dataset.widget]));
        return;
      }
      var k = el.dataset.campo;
      if (vistos[k]) return;
      vistos[k] = true;
      var v = c[k], txt;
      if (el.type === 'radio') txt = v != null ? rotuloOpcao(k, v) : '—';
      else if (el.type === 'checkbox') txt = v === true ? '✓ consigo explicar' : '—';
      else txt = v ? String(v) : '—';
      linhas.push([secao, el.dataset.rotulo || k, txt]);
    });
    return linhas;
  }

  /* ================================================================ progresso */
  var INST = {};
  function perguntas(raiz) {
    // uma "pergunta" = um campo de texto ou um grupo de opções. Não contam: caixas de seleção da síntese
    // e campos opcionais (data-opcional, ex.: anotações do mapa)
    var grupos = {}, lista = [];
    (raiz || document).querySelectorAll('[data-campo]').forEach(function (c) {
      if (c.type === 'checkbox' || c.hasAttribute('data-opcional') || grupos[c.dataset.campo]) return;
      grupos[c.dataset.campo] = true;
      lista.push(c);
    });
    return lista;
  }
  function respondida(c) {
    if (c.type === 'radio') return !!document.querySelector('input[data-campo="' + c.dataset.campo + '"]:checked');
    return !!c.value.trim();
  }
  function contar(raiz) {
    var ps = perguntas(raiz), ok = ps.filter(respondida).length, total = ps.length;
    (raiz || document).querySelectorAll('[data-widget]').forEach(function (el) {
      var w = INST[el.dataset.widget];
      if (!w || !w.respondido) return;
      total++;
      if (w.respondido(w.coletar())) ok++;
    });
    return { ok: ok, total: total };
  }
  var tProg = null;
  function atualizarProgresso() { clearTimeout(tProg); tProg = setTimeout(progresso, 250); }
  function barra(el, ok, total) { if (el) el.style.width = (total ? ok / total * 100 : 0) + '%'; }
  function progresso() {
    var g = contar();
    var sp = document.querySelector('.sidebar-progresso');
    if (sp) { sp.querySelector('.sp-txt').textContent = g.ok + ' de ' + g.total + ' respostas'; barra(sp.querySelector('.sp-barra i'), g.ok, g.total); }
    var ig = document.querySelector('.ind-geral');
    if (ig) { ig.querySelector('.ig-num').textContent = g.ok; ig.querySelector('.ig-txt').textContent = 'de ' + g.total + ' respostas'; barra(ig.querySelector('.sp-barra i'), g.ok, g.total); }
    // por módulo: cartões do índice e itens do sumário
    var proximo = null, algum = g.ok > 0;
    MODS.forEach(function (m, i) {
      var c = contar(m), feito = c.total > 0 && c.ok === c.total;
      var card = document.querySelector('.mod-card[data-mod="' + m.id + '"]');
      var nav = document.querySelector('.nav-mod[data-mod="' + m.id + '"]');
      if (card) {
        card.querySelector('.mc-prog').textContent = c.total ? (feito ? '✓ ' : '') + c.ok + '/' + c.total + ' respostas' : 'Leitura';
        barra(card.querySelector('.mc-barra i'), c.ok, c.total);
        card.classList.toggle('feito', feito);
        card.classList.toggle('sem-atividade', !c.total);
      }
      if (nav) { nav.querySelector('.nm-p').textContent = c.total ? (feito ? '✓' : c.ok + '/' + c.total) : ''; nav.classList.toggle('feito', feito); }
      if (!proximo && c.total && !feito) proximo = { m: m, i: i };
    });
    var cont = document.querySelector('.btn-continuar');
    if (cont && MODS.length) {
      var alvo = proximo || { m: MODS[0], i: 0 };
      cont.href = '#' + alvo.m.id;
      cont.textContent = algum ? 'Continuar: módulo ' + (alvo.i + 1) + ' · ' + alvo.m.dataset.titulo : 'Começar pelo módulo 1';
    }
    resumirMapa();
    compararExit();
  }

  /* ----- Mapa de aprendizagem: resumo dos níveis ----- */
  var NIVEIS = [['domino', 'Domino'], ['parcial', 'Domino parcialmente'], ['nao', 'Ainda não domino']];
  function resumirMapa() {
    var box = document.querySelector('.mapa-resumo'); if (!box) return;
    var itens = document.querySelectorAll('.mapa-item'), n = { domino: 0, parcial: 0, nao: 0 }, marcados = 0;
    itens.forEach(function (li, i) {
      var r = li.querySelector('input[type=radio]:checked');
      if (r) { n[r.value]++; marcados++; }
    });
    if (!marcados) { box.innerHTML = '<p class="mr-vazio">Marque cada objetivo para ver o seu mapa.</p>'; return; }
    box.innerHTML = '<div class="mr-barra">' + NIVEIS.map(function (v) {
      return n[v[0]] ? '<span class="mr-' + v[0] + '" style="flex:' + n[v[0]] + '"></span>' : '';
    }).join('') + (itens.length - marcados ? '<span class="mr-sem" style="flex:' + (itens.length - marcados) + '"></span>' : '') + '</div>' +
      '<ul class="mr-leg">' + NIVEIS.map(function (v) { return '<li><i class="mr-' + v[0] + '"></i>' + v[1] + ' <b>' + n[v[0]] + '</b></li>'; }).join('') +
      (itens.length - marcados ? '<li><i class="mr-sem"></i>Sem marcação <b>' + (itens.length - marcados) + '</b></li>' : '') + '</ul>';
  }

  /* ================================================================ navegação por módulos */
  var MODS = [];
  function semAnimacao(f) {
    var h = document.documentElement, antes = h.style.scrollBehavior;
    h.style.scrollBehavior = 'auto'; f(); h.style.scrollBehavior = antes;
  }
  function fecharSumario() {
    document.getElementById('sidebar').classList.remove('open');
    var t = document.getElementById('sidebar-toggle'); if (t) t.classList.remove('active');
    var o = document.getElementById('overlay'); if (o) o.style.display = 'none';
  }
  function marcarSumario(mod) {
    document.querySelectorAll('.nav-mod').forEach(function (a) { a.classList.toggle('ativo', !!mod && a.dataset.mod === mod.id); });
    document.querySelectorAll('.nav-subs').forEach(function (s) { s.classList.toggle('aberto', !!mod && s.dataset.subs === mod.id); });
    var ind = document.querySelector('.nav-indice'); if (ind) ind.classList.toggle('ativo', !mod);
  }
  function mostrarModulo(mod, el) {
    MODS.forEach(function (m) { m.hidden = m !== mod; });
    document.getElementById('indice').hidden = true;
    document.body.classList.add('em-modulo');
    marcarSumario(mod);
    if (el) { var d = el.closest('details'); while (d) { d.open = true; d = d.parentElement && d.parentElement.closest('details'); } }
    window.dispatchEvent(new Event('resize'));   // recalcula caixas de texto e o gráfico do simulador
    semAnimacao(function () {
      if (el && el !== mod) el.scrollIntoView({ block: 'start' });
      else window.scrollTo(0, 0);
    });
    fecharSumario();
  }
  function mostrarIndice() {
    MODS.forEach(function (m) { m.hidden = true; });
    document.getElementById('indice').hidden = false;
    document.body.classList.remove('em-modulo');
    marcarSumario(null);
    semAnimacao(function () { window.scrollTo(0, 0); });
    fecharSumario();
    progresso();
  }
  function rota() {
    var h = decodeURIComponent(location.hash.slice(1));
    var el = h ? document.getElementById(h) : null;
    var mod = el ? (el.classList.contains('modulo') ? el : el.closest('.modulo')) : null;
    if (mod) mostrarModulo(mod, el); else mostrarIndice();
  }
  function abrir(id) {
    var el = document.getElementById(id); if (!el) return;
    if (history.replaceState) history.replaceState(null, '', '#' + id);
    rota();
  }
  function ligarNavegacao() {
    MODS = Array.prototype.slice.call(document.querySelectorAll('.modulo'));
    window.addEventListener('hashchange', rota);
    // um link para o hash atual não dispara "hashchange": trata o clique na mão
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="#"]'); if (!a) return;
      if (a.getAttribute('href') === location.hash) { e.preventDefault(); rota(); }
    });
    // sumário no celular
    var toggle = document.getElementById('sidebar-toggle'), sidebar = document.getElementById('sidebar'), overlay = document.getElementById('overlay');
    toggle.addEventListener('click', function () {
      var aberto = sidebar.classList.toggle('open');
      toggle.classList.toggle('active', aberto);
      overlay.style.display = aberto ? 'block' : 'none';
    });
    overlay.addEventListener('click', fecharSumario);
    // barra de progresso de leitura, item ativo do sumário e voltar ao topo
    var barraLeitura = document.getElementById('progress-bar'), topo = document.getElementById('back-to-top'), agendado = false;
    function aoRolar() {
      agendado = false;
      var total = document.documentElement.scrollHeight - window.innerHeight;
      barraLeitura.style.width = (total > 0 ? window.scrollY / total * 100 : 0) + '%';
      topo.style.display = window.scrollY > 600 ? 'flex' : 'none';
      var subs = document.querySelectorAll('.nav-subs.aberto .nav-sub'), atual = null;
      subs.forEach(function (a) {
        var alvo = document.getElementById(a.getAttribute('href').slice(1));
        if (alvo && alvo.getBoundingClientRect().top <= 140) atual = a;
      });
      subs.forEach(function (a) { a.classList.toggle('ativo', a === atual); });
    }
    window.addEventListener('scroll', function () { if (!agendado) { agendado = true; requestAnimationFrame(aoRolar); } }, { passive: true });
    topo.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }

  /* ----- exit ticket: compara com a preparação ----- */
  var EFEITO = { melhor: 'melhor', diferente: 'mais diferente', 'as duas': 'melhor e mais diferente', 'não sei': '(você ainda não sabia)' };
  var CLASSE = { a: '(a) EO de paridade', b: '(b) EO de liderança temporária', c: '(c) reforço de posição' };
  function compararExit() {
    var el = document.querySelector('.exit-compara'); if (!el) return;
    var c = coletarCampos();
    if (!c.prep_efeito || !c.exit_classe) { el.innerHTML = ''; return; }
    var coerente = (c.prep_efeito === 'melhor' && c.exit_classe !== 'c') || (c.prep_efeito === 'diferente' && c.exit_classe === 'c');
    el.innerHTML = '<p>No início, você disse que a iniciativa deixou a empresa <strong>' + esc(EFEITO[c.prep_efeito] || c.prep_efeito) +
      '</strong>. Agora você a classificou como <strong>' + esc(CLASSE[c.exit_classe] || c.exit_classe) + '</strong>. ' +
      (coerente ? 'As duas leituras combinam.' : 'As duas leituras não combinam totalmente: vale explicar abaixo o que mudou.') + '</p>';
  }

  /* ================================================================ início */
  function iniciar(cfg) {
    document.querySelectorAll('[data-widget]').forEach(function (el) {
      var f = W[el.dataset.widget];
      if (f) INST[el.dataset.widget] = f(el);
    });
    ligarParagrafos();
    ligarNavegacao();
    // anotação opcional de cada objetivo do mapa
    document.addEventListener('click', function (e) {
      var b = e.target.closest('.b-mapa-nota'); if (!b) return;
      var lab = b.parentNode.querySelector('.mapa-nota'), ta = lab.querySelector('textarea');
      if (lab.hidden) lab.hidden = false; else if (!ta.value.trim()) lab.hidden = true;
      b.setAttribute('aria-expanded', String(!lab.hidden));
      if (!lab.hidden) ta.focus();
    });
    document.addEventListener('click', function (e) {
      var b = e.target.closest('[data-trazer]'); if (!b) return;
      var par = b.dataset.trazer.split(':');
      var de = document.querySelector('[data-campo="' + par[0] + '"]'), para = document.querySelector('[data-campo="' + par[1] + '"]');
      if (!de || !para) return;
      if (!de.value.trim()) { VD.toast('Você ainda não respondeu à pergunta "Antes de ler", no início do módulo Texto de Porter.'); return; }
      if (para.value.trim() && para.value !== de.value && !window.confirm('Substituir o que você já escreveu?')) return;
      para.value = de.value;
      para.dispatchEvent(new Event('input', { bubbles: true }));
    });
    ['input', 'change'].forEach(function (ev) { document.addEventListener(ev, atualizarProgresso); });

    VD.ferramenta({
      id: cfg.id, titulo: cfg.titulo, crumb: cfg.crumb,
      coletar: function () {
        var o = { v: 1, campos: coletarCampos() };
        coletarParagrafos(o);
        Object.keys(INST).forEach(function (k) { var v = INST[k].coletar(); if (v) o[k] = v; });
        return o;
      },
      aplicar: function (d) {
        aplicarCampos(d && d.campos);
        aplicarParagrafos(d);
        Object.keys(INST).forEach(function (k) { INST[k].aplicar(d ? d[k] : null); });
        document.querySelectorAll('.mapa-nota').forEach(function (lab) {
          var tem = !!lab.querySelector('textarea').value.trim();
          lab.hidden = !tem;
          lab.parentNode.querySelector('.b-mapa-nota').setAttribute('aria-expanded', String(tem));
        });
        progresso();
      },
      resumo: resumo,
      infoImpressao: function () { return cfg.crumb; }
    });
    rota();
    // na impressão, mostra todos os módulos e abre as respostas recolhidas
    var abertos = [];
    window.addEventListener('beforeprint', function () {
      document.body.classList.add('imprimindo');
      var ds = document.querySelectorAll('details');
      abertos = Array.prototype.map.call(ds, function (d) { return d.open; });
      Array.prototype.forEach.call(ds, function (d) { d.open = true; });
    });
    window.addEventListener('afterprint', function () {
      document.body.classList.remove('imprimindo');
      Array.prototype.forEach.call(document.querySelectorAll('details'), function (d, i) { d.open = abertos[i]; });
    });
  }

  window.PARTE = { iniciar: iniciar, resumo: resumo, instancias: INST, abrir: abrir };
})();
