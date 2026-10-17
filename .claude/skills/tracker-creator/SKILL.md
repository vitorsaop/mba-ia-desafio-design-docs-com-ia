---
name: tracker-creator
description: Gera docs/TRACKER.md, a tabela de rastreabilidade que liga cada item do PRD, do RFC, do FDD e dos ADRs de webhooks à fala da TRANSCRICAO.md (com [hh:mm] Nome) ou ao arquivo do código de origem, e confere a cobertura de 80%. Use esta skill sempre que o usuário pedir para criar, gerar, atualizar, refazer ou validar o tracker, a rastreabilidade, a referência cruzada entre documentos e fontes, ou para checar se algo nos documentos foi inventado, mesmo que ele não cite o nome da skill. Rode depois que PRD, RFC, FDD e ADRs existirem.
---

# tracker-creator

Gera `docs/TRACKER.md`: uma linha por item identificável dos documentos, com a origem na transcrição ou no código. O Tracker existe para pegar invenção da IA. Se uma linha não tem Localização verdadeira, o item não tem origem e precisa ser corrigido ou removido do documento, e não "justificado" no Tracker.

## Por que existe um enumerador

O README exige que 80% dos itens identificáveis dos documentos tenham linha. Contar "a olho" não prova isso. O script `scripts/enumerar_itens.py` lista os itens de forma determinística (requisitos, objetivos, decisões, alternativas, contratos, erros, riscos, critérios de aceite, linhas de integração etc.) com IDs fixos. O validador compara essa lista com a tabela e calcula a cobertura. A regra de cada ID está em `references/regras.md`.

## Entradas obrigatórias

1. Os documentos prontos: `docs/PRD.md`, `docs/RFC.md`, `docs/FDD.md`, `docs/adrs/ADR-*.md`. Se algum faltar, pare e peça a skill correspondente.
2. `.claude/plano/PLANO-WEBHOOKS.md`: cada item do plano já traz a Localização (coluna "Localização" das seções S2 a S6 e S1 para código).
3. `TRANSCRICAO.md`, para conferir que cada `[hh:mm] Nome` existe.
4. `assets/template-tracker.md` e `references/regras.md`.

## Passo a passo

1. Liste os itens: `python3 .claude/skills/tracker-creator/scripts/enumerar_itens.py --tabela`. Cada linha já traz ID, Documento, Tipo sugerido e um resumo curto; faltam Fonte e Localização.
2. Para cada item, leia o texto no documento e ache a origem no plano ou na transcrição. Escolha uma só Fonte:
   - `TRANSCRICAO` quando a origem é uma fala. Localização: `[hh:mm] Nome`; para mais de uma fala, separe com `; `.
   - `CODIGO` quando a origem é um arquivo. Localização: `caminho` ou `caminho:linha`.
3. Itens de classe B apontam para o item A que os obriga (fala) ou para o arquivo. Itens "Hipótese:" e lacunas levam Tipo `Hipótese` e apontam para a fala que originou a lacuna. Alternativas de ADR que são plausíveis mas não foram discutidas também levam Tipo `Hipótese`.
4. Se um item não tem origem verificável, não escreva uma origem aproximada: corrija o documento (com a skill dele) ou remova o item.
5. Registre a origem de cada item em `.claude/plano/FONTES-TRACKER.tsv`, arquivo de trabalho local que não é versionado (uma linha por ID, quatro colunas separadas por tabulação: ID, Tipo ou vazio, Fonte, Localização) e monte o arquivo com o script, que usa o template, a legenda e o resumo do enumerador e se recusa a continuar se faltar ou sobrar um ID:

```bash
python3 .claude/skills/tracker-creator/scripts/montar_tracker.py
```

6. Execute o validador e corrija até `RESULTADO: PASS`:

```bash
python3 .claude/skills/tracker-creator/scripts/validar_tracker.py
```

7. Rode a conferência entre documentos e corrija até `RESULTADO: PASS`. Ela falha se uma frase já corrigida voltar ou se um fato que a reunião não decidiu aparecer sem "Hipótese:":

```bash
python3 .claude/skills/tracker-creator/scripts/conferir_consistencia.py
```

8. Informe ao usuário: linhas, cobertura, proporção TRANSCRICAO e CODIGO, e itens que ficaram sem linha.

## Regras que não podem ser quebradas

- Cabeçalho da tabela exatamente `| ID | Documento | Tipo | Conteúdo (resumo) | Fonte | Localização |`.
- Mínimo de 80% dos itens enumerados com linha; a meta deste projeto é 100%.
- Mínimo de 70% das linhas com Fonte `TRANSCRICAO` e `[hh:mm] Nome` existente na transcrição; mínimo de 5 linhas `CODIGO` com arquivo existente.
- Uma linha por ID, uma única Fonte por linha, resumo em uma linha, sem o caractere `|` dentro das células.
- Sem emoji e sem travessão.
- A `TRANSCRICAO.md` é a fonte da verdade. Se o plano, um documento ou o código divergir dela, vale a transcrição e o plano é corrigido. Uma correção vale para todos os documentos: depois de mudar um fato, procure o termo em `docs/` e rode `python3 .claude/skills/tracker-creator/scripts/conferir_consistencia.py`. Um fato que a reunião não decidiu leva "Hipótese:" em todo documento em que aparece.
