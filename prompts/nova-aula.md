# Prompt: publicar a próxima aula do portal "Entendendo Porter"

Como usar: abra uma conversa nova no Claude Code **na pasta do projeto**
(`C:\Users\LENOVO\OneDrive - Biopark Educação\Documentos\ESTRATÉGIA\PORTER - WHAT IS STRATEGY`),
anexe o material da aula (o `.md` que você escreveu) e cole o texto abaixo, preenchendo os campos entre colchetes.
Não é preciso anexar o PDF nem o artigo em inglês: eles já estão na pasta.

---

Quero publicar a **Aula [3 | 4 | 5]**, correspondente à **Parte [III | IV | V]** do artigo *What Is Strategy?* (Porter, 1996), no portal "Entendendo Porter: O que é estratégia?", que já está no ar com as Aulas 1 e 2.

**Material da aula (anexo):** [nome do arquivo, ex.: aula_porter_parte3_trade_offs.md]. Se não estiver anexado, procure em `C:\Users\LENOVO\Downloads`.

**Pedidos específicos para esta aula (opcional):** [ex.: "quero um simulador para o caso X", "o quadro Y deve virar uma atividade", ou "nenhum"]

## Antes de tudo

1. Leia o `CLAUDE.md` do projeto inteiro. Ele é a fonte da verdade: arquitetura, decisões que eu já tomei, como funciona o salvamento, armadilhas e como validar. Depois leia o `README.md` e os arquivos `ferramentas/gerar_parte.py`, `ferramentas/atividades_parte2.py`, `ferramentas/conferir_integridade.py` e `ferramentas/testes/teste_ponta_a_ponta.html`.
2. Rode `git status` e `git log --oneline -5` e confirme que está tudo limpo e sincronizado com o GitHub.
3. **A turma já está respondendo às aulas publicadas.** Antes de mexer em qualquer coisa, rode `python ferramentas/fotografar_chaves.py antes`. No fim, rode `python ferramentas/fotografar_chaves.py comparar`: as aulas existentes precisam sair **OK** (mesmas chaves, opções, parágrafos, widgets e atividade). Não altere `assets/js/portal.js` nem `apps-script/Codigo.gs`; o Painel da planilha já tem colunas para as Aulas 1 a 5. Em `assets/js/parte.js`, só **acrescente** código (widgets novos); não mude o que as aulas anteriores usam.
4. Me apresente um **plano curto** antes de construir: a lista dos 12 módulos (ou quantos forem), as atividades de cada bloco com as chaves que pretende usar, os widgets novos (se houver), o que será simplificado ou consolidado no material e como as figuras ou quadros da parte serão tratados. Pergunte só o que for decisão minha.

## O que fazer (mesmo padrão das Aulas 1 e 2)

Siga a receita "Nova parte" do `CLAUDE.md`. Em resumo:

1. **Referência em inglês** em `conteudo/referencia-parte-N-en.txt` (formato `[CORPO]`, `[QUADRO]`, `[NOTA]`, um parágrafo por linha), extraída do PDF `..\PORTER - WHAT IS STRATEGY.pdf` com `pdftotext` (Git Bash). A página impressa p. N é a página N−36 do arquivo PDF. Os parágrafos do corpo saem inteiros; junte a continuação de página (que começa em minúscula), mas cuidado com fragmentos de quadros que também começam em minúscula. Os quadros saem em colunas misturadas: copie o texto limpo deles. Nada em inglês vai para o site.
2. **Tradução** completa e fiel em `conteudo/porter-parte-N-traducao.md`, um parágrafo da tradução para cada parágrafo do original, com `[pNN]` só no início do parágrafo em que a página começa, subtítulos em `###`, quadros com `?QUADRO pNN | título | id-do-quadro`, notas de rodapé `[^n]` e **pausas para responder** (`?PAUSA t_qK | pergunta`) a cada trecho de sentido (6 a 8 pausas).
3. **Material para o estudante** em `conteudo/aula-N-material-estudante.md`, a partir do meu original (salve o original sem alterações em `conteudo/aula-N-material.md`, como referência):
   - fala direto com o estudante ("você"); sem roteiro de aula, tempos, "nota ao professor", "como conduzir", "peça aos alunos", "em grupos/duplas" (o trabalho é individual);
   - os objetivos viram a seção `## Mapa de aprendizagem` (lista numerada; o gerador cria os botões Domino / Domino parcialmente / Ainda não domino e a anotação);
   - cada seção `##` vira um módulo: Mapa, (o Texto de Porter entra como módulo 2), Abertura, Blocos, Fechamento, "Para consulta" (apêndices úteis: casos, armadilhas, referências);
   - respostas esperadas viram `**Comentário:**`, recolhidas até o estudante responder; as dúvidas do bloco de dúvidas ficam recolhidas com a caixa de resposta antes;
   - simplifique e elimine redundâncias (dúvidas que repetem blocos, perguntas que aparecem duas vezes, modelos de sala que podem virar atividade), **sem perder conceitos, casos, números ou referências**. Me diga quantas palavras tinha e quantas ficou.
4. **Atividades** em `ferramentas/atividades_parteN.py`, partindo de `atividades_parte2.py`: chaves novas e estáveis, `REGRAS` dizendo onde cada caixa entra, `MODULOS` (tipo, título curto, descrição), `MODELO` trocando apenas os títulos. Use as caixas de resposta, as escolhas em pílulas, o espelho (`espelho()`) para retomar uma resposta anterior da mesma aula e o botão "trazer" no exit ticket. Prefira atividades que façam o estudante **aplicar** o conceito à empresa dele e ao caso Vivelar, que é o fio condutor. Widgets novos vão no `parte.js` como acréscimo, com `coletar`, `aplicar`, `resumo` legível para a planilha e `respondido`; todo texto do estudante em `innerHTML` passa por `VD.esc` (ou use `.value`/`textContent`).
5. Registre a parte em `PARTES` no `gerar_parte.py` e no `conferir_integridade.py` (com `subtitulos`, `n_quadro`, `extras` e `nomes` próprios da parte). Se a parte tiver figuras que o gerador ainda não sabe desenhar, crie o suporte (SVG recriado, rótulos traduzidos) sem mudar a saída das partes já publicadas.
6. **Home** (`index.html`): troque o cartão "Em breve" da aula pelo botão único "Abrir a Aula N" com `data-ferramenta="aulaN"` e inclua a aula no array `ATIVIDADES`.
7. **Testes:** acrescente ao `teste_ponta_a_ponta.html` as verificações da nova aula (parágrafos, pausas, módulos, widgets, resumo na planilha simulada, volta dos dados em outro computador, escape de HTML, e que os dados das aulas anteriores continuam intactos), sem remover as existentes.

## Validação antes de publicar

1. `python ferramentas/gerar_parte.py` e `python ferramentas/conferir_integridade.py` (Git Bash: `PYTHONIOENCODING=utf-8`). Todas as partes precisam dar OK: material 100% íntegro e tradução completa (mesmo número de parágrafos, proporção PT/EN entre 0,95 e 1,45, números e nomes próprios). Se um parágrafo sair fora da faixa, verifique primeiro se a referência em inglês não foi contaminada por fragmento de quadro.
2. `python ferramentas/fotografar_chaves.py comparar`: aulas anteriores **OK**, a nova aparece como **NOVA**.
3. `.\ferramentas\testes\rodar_testes.ps1`: precisa terminar com `FAIL/ERRO: 0`. O executor recomeça sozinho se o Edge headless travar; isso é esperado de vez em quando.
4. `python ferramentas/capturar_telas.py <pasta-no-scratchpad> [nomes]` (acrescente as capturas da nova parte na lista `CAPTURAS`) e **olhe** as imagens em 1366px e 520px: sobreposições, cortes, rolagem horizontal.
5. Publique (`git add -A`, commit com a linha de coautoria, `git push`), espere o build do GitHub Pages e confira o site no ar: a página nova abre e as chaves das páginas publicadas continuam iguais. **Não grave dados de teste na planilha real** sem me perguntar: a turma está usando.
6. Atualize o `CLAUDE.md` (aulas publicadas, widgets e chaves novos, armadilhas que aparecerem, número de verificações do teste) e o `README.md`, e encerre processos do Edge headless que sobrarem (só os com `--headless` e perfil em `AppData\Local\Temp`).

## O que me entregar no fim

Um resumo curto: link da aula, o que foi construído, o que foi simplificado no material (palavras antes e depois), o resultado de cada verificação (integridade, chaves, teste, capturas, site no ar) e qualquer decisão que você tenha tomado por conta própria e que eu deva conferir.

---

## Referência rápida: o que existe em cada parte restante

| Aula | Parte | Páginas impressas (páginas do arquivo PDF) | O que tem além do corpo |
|---|---|---|---|
| 3 | III. Uma posição estratégica sustentável exige trade-offs | pp. 43–45 (arquivo 7–9) | Sem quadros. Frases em destaque nas margens ("The essence of strategy is choosing to perform activities differently than rivals do", "Strategic positions can be based on customers' needs...") são citações repetidas do texto, não parágrafos. Casos: J.C. Penney, Continental Lite, Neutrogena, Ivory, Ikea, Honda e Toyota. |
| 4 | IV. O encaixe gera vantagem competitiva e sustentabilidade | pp. 45–50 (arquivo 9–14) | Subtítulos em linha: "Types of Fit." e "Fit and sustainability.". Três figuras de mapas de sistemas de atividades (Ikea p. 47, Vanguard p. 48, Southwest p. 49), que precisam ser redesenhadas em SVG com rótulos traduzidos (de preferência interativas). Quadro "Alternative Views of Strategy" (p. 50), em duas colunas. Notas 2 (Milgrom e Roberts) e 3 (Rivkin, Siggelkow), na p. 54. Frase em destaque "Trade-offs are essential to strategy..." (p. 46) não é parágrafo. |
| 5 | V. Redescobrindo a estratégia | pp. 50–54 (arquivo 14–18) | Subtítulos em linha: "The Failure to Choose.", "The Growth Trap.", "Profitable Growth.", "The Role of Leadership.". Quadros "Reconnecting with Strategy" (p. 51, com lista de perguntas) e "Emerging Industries and Technologies" (p. 52). A parte termina no alto da p. 54 ("...tary activities into a sustainable advantage."). |
