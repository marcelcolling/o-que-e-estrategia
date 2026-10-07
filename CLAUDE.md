# Portal "Entendendo Porter: O que é estratégia?": guia para sessões do Claude

Portal da disciplina Execução Estratégica. Cada aula é uma parte do artigo *What Is Strategy?* (Porter, HBR, 1996): o estudante lê a tradução da parte, estuda o material da aula e responde às atividades na mesma página. As respostas vão para uma planilha Google do professor. Trabalho **individual**. Depois que a turma começar a usar, **não quebre o salvamento nem os dados já gravados**.

O núcleo (sessão, salvamento, planilha, testes) veio do portal "Vieses e Decisão" (`C:\Users\LENOVO\vieses-e-decisao`). Os dois projetos são independentes: não altere nada lá a partir daqui.

## Onde está cada coisa

| Item | Local |
|---|---|
| Repositório local | `C:\Users\LENOVO\OneDrive - Biopark Educação\Documentos\ESTRATÉGIA\PORTER - WHAT IS STRATEGY` (git, branch `main`) |
| GitHub | https://github.com/marcelcolling/o-que-e-estrategia (público) |
| Site (GitHub Pages) | https://marcelcolling.github.io/o-que-e-estrategia/ (publica sozinho a cada `git push`, cerca de 1 min) |
| Planilha de respostas | id `1u83Aw17rn3-g_iOtOhLEcx2WMXNI6hJHTPZUtlEH6lQ` (dá para ler pelo conector do Google Drive) |
| URL do Apps Script | em `assets/js/config.js` (implantação de 07/10/2026, testada contra a planilha real) |
| PDF original do artigo | `...\Documentos\ESTRATÉGIA\PORTER - WHAT IS STRATEGY.pdf` (pasta acima). **Nunca publicar nem linkar** (decisão do professor; copyright da HBR) |

## Decisões do professor (não reverter sem perguntar)

- Só a **tradução** vai para o site. Nenhum link para o PDF, em lugar nenhum. O texto em inglês também não é publicado.
- Os `.md` de origem (material da aula, texto original) **não vão para o GitHub**: `conteudo/` está no `.gitignore` e fica só na pasta local (OneDrive). O que é publicado é o HTML gerado.
- Uma parte do artigo por aula. Por enquanto só a Parte I tem conteúdo; Partes II a V aparecem como "Em breve" na home.
- Identidade do "Vieses e Decisão" com azul-escuro no lugar do roxo.
- **Material e atividades são uma coisa só:** na home, um único botão por aula.
- **O material fala direto com o estudante** ("você"), sem roteiro de aula, tempos, notas ao professor nem "os alunos devem…". O original do professor (`conteudo/aula-1-material.md`) é só referência; a página é gerada da versão revisada `conteudo/aula-1-material-estudante.md` (enxuta, sem redundâncias). A integridade é conferida contra essa versão.
- **Um módulo por vez:** a página da aula abre num índice de cartões; cada módulo (Mapa, Texto de Porter, Abertura, Blocos 1–7, Fechamento, Para consulta) é aberto separadamente, com "Anterior / Índice / Próximo".
- **Mapa de aprendizagem** no lugar dos objetivos: cada objetivo com Domino / Domino parcialmente / Ainda não domino e uma anotação opcional.

## Arquitetura (site estático, sem build de JS)

```
index.html                     home: hero + sessão, trilha das 5 partes, "Quem é Michael Porter" (bio + obras por fase)
partes/parte-1.html            GERADO por ferramentas/gerar_parte.py (não editar à mão): índice + 12 módulos
conteudo/  (fora do git)       porter-parte-1-traducao.md, aula-1-material-estudante.md (fonte), aula-1-material.md (original do professor),
                               referencia-parte-1-en.txt, referencia-porter-original.md
ferramentas/gerar_parte.py     tradução + material (Markdown) + atividades -> página da parte (cada "##" do material vira um módulo;
                               o Texto de Porter entra como módulo 2; "::: visual nome" insere um esquema)
ferramentas/atividades_parte1.py  caixas de atividade (chaves data-campo), mapa(), visual(), MODULOS (tipo/título curto/descrição),
                                  REGRAS de onde cada caixa entra e o MODELO da página
ferramentas/conferir_integridade.py  confere material (palavra por palavra) e tradução (contra o PDF)
ferramentas/capturar_telas.py  capturas no Edge headless via CDP (1366px e 520px)
ferramentas/testes/            teste de ponta a ponta com Apps Script simulado (rodar_testes.ps1)
assets/js/portal.js            núcleo: sessão, login, salvamento automático, sincronização, conflito, barra superior, guia de uso
assets/js/parte.js             página da parte: campos, destacar/anotar parágrafos, widgets, resumo, progresso por módulo,
                               navegação por hash (#m-… abre um módulo; #id interno abre o módulo dele e rola até o ponto)
assets/js/vivelar.js           modelo mensal do caso Vivelar (Apêndice A) + simulador
assets/js/leitura.js           (não é usado na página da parte; sobrou do núcleo de referência)
assets/css/portal.css · leitura.css · parte.css
apps-script/Codigo.gs          back-end na planilha (doPost entrar/salvar, abas legíveis, Painel, menu)
```

## Como funciona o salvamento (não alterar sem necessidade)

- Igual ao portal de referência: `VD.entrar` (nome + palavra-chave), `VD.ferramenta({ id, titulo, crumb, coletar, aplicar, resumo })`, `localStorage` na hora e Apps Script alguns segundos depois, conflito por timestamp, `[data-vd-salvar]` = botão "Salvar respostas".
- **Prefixos próprios no navegador:** `pe_sessao_v1`, `pe_dados_v1::`, `pe_leitura_`. Os portais do professor ficam no mesmo domínio (`marcelcolling.github.io`) e compartilham o `localStorage`; com os prefixos do outro portal, a sessão e o `aula1` vazariam entre eles. Há um teste para isso.
- **Uma atividade por aula:** ids `aula1` a `aula5`. Formato salvo (ver `parte.js`):
  `{ v:1, campos:{ chave: texto|opção|true }, notas:{ "8": texto }, destaques:[3,8], fronteira, portfolio, logo, simulador:{ p, exp } }`.
- Módulos escondidos usam o atributo `hidden`, mas continuam no DOM: coleta, aplicação e resumo funcionam com todos eles. Ao abrir um módulo, `parte.js` dispara `resize` para recalcular a altura das caixas de texto e o gráfico do simulador.
- O progresso conta perguntas (campo de texto ou grupo de opções) e widgets; não contam as caixas da síntese nem campos `data-opcional` (anotações do mapa).
- As chaves de `campos` vêm do atributo `data-campo` em `atividades_parte1.py`. **Não renomeie chaves em uso** (as respostas ficariam órfãs). O mapa usa `mapa_1`…`mapa_7` e `mapa_N_nota`. A chave `b2_duvida7` deixou de existir na revisão (a Dúvida 7 foi incorporada ao Bloco 5). Para tirar uma pergunta, apague a caixa; para acrescentar, use chave nova. Os parágrafos da tradução são identificados pelo número (`notas`/`destaques`): **não junte nem divida parágrafos** depois que a turma começar.
- `resumo` percorre a página em ordem (`[data-campo]`, `[data-widget]`, `.par`) e gera `[seção, pergunta, resposta]` para a aba do estudante. A seção vem de `data-secao` da caixa; a pergunta, de `data-rotulo`.
- Todo texto do estudante que entra em `innerHTML` passa por `VD.esc`. Valores em campos são atribuídos por `.value`.

## Receitas

### Gerar e conferir a página de uma parte
1. `python ferramentas/gerar_parte.py`
2. `python ferramentas/conferir_integridade.py` (com `PYTHONIOENCODING=utf-8` no Git Bash). Precisa dar **OK** nas duas partes: material com 100% de semelhança e tradução com o mesmo número de parágrafos do original, proporção PT/EN entre 0,95 e 1,45 em cada parágrafo e todos os números e nomes próprios.

### Nova parte (ex.: Aula 2 = Parte II, pp. 39–43)
1. Extraia o inglês da parte do PDF (`pdftotext`, do Git Bash) para `conteudo/referencia-parte-2-en.txt` no mesmo formato (`[CORPO]`, `[QUADRO]`, `[NOTA]`, um parágrafo por linha). A Parte II tem os quadros "Finding New Positions" e "The Connection with Generic Strategies"; em pdftotext eles saem em colunas misturadas, então copie-os limpos.
2. Traduza em `conteudo/porter-parte-2-traducao.md` (formato descrito no topo de `gerar_parte.py`: `[p40]` marca página, `?PAUSA chave | pergunta`, `?QUADRO`, `?FIGURA`, `[^n]`). Mantenha um parágrafo da tradução por parágrafo do original.
3. Copie o material do professor para `conteudo/aula-2-material.md`.
4. Crie `ferramentas/atividades_parte2.py` (partindo do da Parte I) e acrescente a parte em `PARTES` no gerador. Generalize `conferir_integridade.py` para a nova parte.
5. Na home, troque o cartão "Em breve" da Aula 2 pelos recursos (leitura/atividade, `data-ferramenta="aula2"`) e inclua a aula no array `ATIVIDADES`.
6. O Painel do `Codigo.gs` já tem colunas para as Aulas 1 a 5.
7. Acrescente verificações da nova parte em `ferramentas/testes/teste_ponta_a_ponta.html`.

### Caso Vivelar
`vivelar.js` reproduz exatamente as tabelas 7.6 a 7.8 do material com estas regras (deduzidas e conferidas contra todos os números): perda da inércia 0,5%/mês dos meses 7 a 24; janela de A de +5% nos meses 4–12, sumindo linearmente até o 18 (`(18−m)/6`); a janela vale para os dois canais de B; perda nas redes linear dos meses 4 a 9 (`(m−3)/6`); rampa nos independentes `(m−6)/18`; custo de servir de R$ 2,30 desde o mês 4; desconto mensal arredondado a 4 casas (15% a.a. → 1,17%, como diz o texto; com a taxa exata, o VP de 48 meses de B daria 38,3 em vez de 38,4). O teste confere 18 acumulados, mensais, participações, VP, cruzamentos e as duas sensibilidades.

### Mudanças no Apps Script
O professor cola o `Codigo.gs` novo no editor (Extensões › Apps Script), salva e vai em **Implantar › Gerenciar implantações › lápis › Versão: Nova versão** (a URL se mantém). Funções do gatilho de 5 minutos (abas e Painel) usam o código salvo mesmo sem nova versão; `doPost` só muda com nova versão.

## Armadilhas já encontradas

- **Planilha em pt-BR:** não gravar fórmulas (separador `;`); links por `RichTextValue`; todo texto passa por `texto()` (prefixa `'` em `= + - @`).
- **Capturas:** `--screenshot` do Edge headless captura no meio da rolagem suave (âncoras e `scroll-behavior:smooth`) e às vezes antes dos scripts terminarem. Use `python ferramentas/capturar_telas.py <pasta> [nomes]`, que controla o Edge pelo CDP, abre o módulo pelo id (`PARTE.abrir`), espera a URL nova e a barra superior, e recarrega se a página travar.
- **Headless travando no carregamento:** às vezes o Edge headless para o parser logo depois das folhas de estilo (`readyState` fica em `loading`, nenhum script é pedido), mesmo com o servidor entregando o HTML em 0,2 s. Não é defeito da página (no navegador normal e no site publicado ela carrega). Por isso: o teste roda em tempo real via CDP com `Runtime.enable` (`rodar_testes.py`; o antigo `--dump-dom` com tempo virtual não chegava a iniciar), e a captura recarrega a página quando ela não fica pronta.
- **Edge headless** (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`): largura mínima real ≈ 500px. Não há Node na máquina.
- **CSS:** `leitura.css` tem `.secao p { font-size; color }` com especificidade (0,1,1): estilos de `<p>` dentro do material precisam de seletor mais forte (ex.: `.secao p.fr-status`).
- **Ids que começam com número** (`7-6-…`) funcionam nas âncoras, mas não com `querySelector('#7-6…')`. Use `getElementById` ou `[id="…"]`.
- **PowerShell 5.1:** recarregue o PATH após instalar algo; grave arquivos sem BOM (`New-Object Text.UTF8Encoding $false`). O Git Bash tem `pdftotext`.
- Logo depois de uma implantação nova, o Apps Script pode devolver 404 por alguns minutos. O portal guarda no navegador e tenta de novo.
- A pasta do projeto está no OneDrive: se o git reclamar de arquivo bloqueado, espere a sincronização terminar.

## Como validar antes de publicar

1. Gerar + conferir integridade (acima).
2. `.\ferramentas\testes\rodar_testes.ps1`: precisa terminar com `FAIL/ERRO: 0` (45 verificações hoje). O servidor simulado (`servidor_simulado.py`) segue as mesmas regras do `Codigo.gs`.
3. `python ferramentas/capturar_telas.py <pasta>` e olhar as capturas (1366px e 520px; o script também avisa se houver rolagem horizontal).
4. Se mexeu no back-end ou na URL: teste contra o Apps Script real com um usuário "Teste (apagar)" e leia a planilha pelo conector do Drive. Depois peça ao professor para removê-lo pelo menu **Portal da disciplina › Remover um estudante…**.
5. `git add -A; git commit; git push` e confira o site (cache: `?x=aleatório`).

## Identidade visual

Azul-escuro `#1F3A5F` / profundo `#152A45` / noite `#0E1D31` (no CSS, as variáveis ainda se chamam `--roxo`, `--vd-roxo`, `--purple`: nome herdado, cor nova), azul-ardósia `#455066`, papel `#FCFCFA` / `#EFEEE7`, amarelo `#EFB93C` (tinta `#5B4212`), texto `#1E2733`. Títulos em **Fraunces**, corpo em **Inter**; o texto de Porter usa Fraunces, para se distinguir do material. Leitura = cartão claro; atividade = moldura azul-escura com faixa sólida e ícone ✎; pausas do texto com moldura amarela. Gráficos: três primeiras cores da paleta de referência da skill de dataviz (azul `#2a78d6`, laranja `#eb6834`, verde-água `#1baf7a`), validadas para daltonismo, sempre com legenda, rótulo direto e tabela. O professor quer texto aproveitando a largura da tela e caixas de texto grandes.

## Pendências conhecidas

- Partes II a V: material e atividades ainda não existem ("Em breve").
- Erros de digitação do original em inglês tratados na tradução: "in race to stay ahead" (traduzido como "na corrida"), "anothers'".
