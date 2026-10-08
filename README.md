# Entendendo Porter: O que é estratégia?

Portal da disciplina Execução Estratégica. Cada aula corresponde a uma parte do artigo *What Is Strategy?* (Michael E. Porter, Harvard Business Review, 1996). A página da aula abre num índice de módulos, que o estudante percorre um de cada vez:

1. **Mapa de aprendizagem:** marca, em cada objetivo, se domina, domina parcialmente ou ainda não domina, com uma anotação opcional;
2. **Texto de Porter:** a tradução da parte, com botões para destacar e anotar cada parágrafo e pausas para responder;
3. **Abertura, Blocos 1 a 7 e Fechamento:** o material da aula, escrito para o estudante, com as atividades no próprio texto (os comentários ficam recolhidos até ele responder), o caso Vivelar com simulador e o exit ticket;
4. **Para consulta:** como a simulação funciona, armadilhas comuns e referências.

O material publicado é a versão revisada de cada aula (`conteudo/aula-N-material-estudante.md`). Os seus originais (`conteudo/aula-N-material.md`) ficam guardados como referência. Hoje estão publicadas as Aulas 1 e 2.

As respostas são salvas sozinhas: no navegador, na hora, e na sua planilha Google, alguns segundos depois.

- **Site:** https://marcelcolling.github.io/o-que-e-estrategia/
- **Repositório:** https://github.com/marcelcolling/o-que-e-estrategia
- **Planilha de respostas:** https://docs.google.com/spreadsheets/d/1u83Aw17rn3-g_iOtOhLEcx2WMXNI6hJHTPZUtlEH6lQ/edit

## O que vai e o que não vai para a internet

- Vai: a página inicial, as traduções das Partes I e II, os materiais das Aulas 1 e 2 e as atividades.
- **Não vai:** o PDF do artigo (não há link para ele em lugar nenhum), o texto original em inglês e os arquivos `.md` de origem. Eles ficam na pasta `conteudo/`, que só existe no seu computador (OneDrive) e é ignorada pelo git.

## Ligar a planilha (uma vez)

1. Abra a planilha de respostas.
2. Vá em **Extensões › Apps Script**. Apague o que estiver no editor e cole todo o conteúdo de `apps-script/Codigo.gs`. Salve (ícone de disquete).
3. No alto do editor, escolha a função **`configurar`** e clique em **Executar**. Autorize o acesso quando o Google pedir (Avançado › Acessar o projeto, se aparecer o aviso de app não verificado). Ela cria as abas `Painel`, `_alunos` e `_dados` e um gatilho que atualiza as abas a cada 5 minutos.
4. Clique em **Implantar › Nova implantação**. Em "Selecionar tipo", escolha **App da Web** e configure:
   - **Executar como:** Eu
   - **Quem pode acessar:** Qualquer pessoa
5. Clique em **Implantar** e copie a **URL do app da Web** (termina em `/exec`).
6. Envie essa URL ao Claude. Ele a coloca em `assets/js/config.js`, publica e faz um teste com um usuário "Teste (apagar)".

Enquanto a URL não estiver configurada, o portal funciona em "modo local": as respostas ficam só no navegador do estudante.

## Acompanhar a turma

- **Painel:** uma linha por estudante, com a data da última gravação e quantas respostas há em cada aula. Clique no nome para ir à aba do estudante.
- **Aba do estudante:** todas as respostas em formato legível (seção, pergunta, resposta), incluindo as anotações nos parágrafos do texto e os experimentos do simulador.
- O menu **Portal da disciplina** (aparece ao abrir a planilha) tem:
  - **Atualizar abas e painel agora**, sem esperar os 5 minutos;
  - **Remover um estudante…**, para apagar cadastros de teste ou duplicados.
- **Estudante esqueceu a palavra-chave:** na aba oculta `_alunos` (Ver › Mostrar abas ocultas), apague a célula `hash_chave` dele. A próxima palavra-chave que ele usar passa a valer.

## Atualizar o conteúdo

O conteúdo da página da Parte I é gerado a partir dos arquivos em `conteudo/`. Para corrigir o material ou a tradução, edite o `.md` correspondente e peça ao Claude para regenerar, conferir a integridade, testar e publicar. Ou faça você mesmo:

```
python ferramentas/gerar_parte.py
python ferramentas/conferir_integridade.py
.\ferramentas\testes\rodar_testes.ps1
git add -A; git commit -m "Atualiza material"; git push
```

**Cuidado depois que a turma começar:** não renomeie perguntas existentes nem junte ou divida parágrafos da tradução. As respostas já salvas estão ligadas a eles.

## Próximas aulas

As Partes III a V já aparecem na trilha como "Em breve". Para liberar uma, basta enviar o material da aula ao Claude. A tradução da parte e as atividades seguem o mesmo padrão das Aulas 1 e 2, sem mexer nas respostas já salvas das aulas anteriores.
