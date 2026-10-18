---
name: adr-creator
description: Gera os ADRs (Architecture Decision Records) da feature de webhooks de pedidos em docs/adrs/ADR-NNN-titulo-em-kebab-case.md, no formato MADR estrito do curso traduzido para pt-BR, a partir de .claude/plano/PLANO-WEBHOOKS.md, TRANSCRICAO.md e do código. Use esta skill sempre que o usuário pedir para criar, gerar, refazer, corrigir ou validar ADRs, registros de decisão arquitetural ou as decisões da reunião de webhooks, mesmo que ele não cite o nome da skill.
---

# adr-creator

Gera de 5 a 8 ADRs, um arquivo por decisão, seguindo o template em `assets/template-adr.md`. O plano diz quais decisões existem e de onde veio cada uma; esta skill só transforma esse plano em arquivos no formato exato.

## Por que o formato é rígido

O desafio avalia os ADRs por estrutura (seções, contagens, nomes de arquivo) e por rastreabilidade. O formato vem de duas fontes que precisam valer ao mesmo tempo: o MADR estrito do plugin `adrs-management` do professor e a lista de seções do README do desafio. A conciliação já está feita em `references/regras.md`. Mudar um cabeçalho ou acrescentar uma seção quebra a validação e a leitura cruzada com o Tracker.

## Entradas obrigatórias

1. `.claude/plano/PLANO-WEBHOOKS.md`: seção S7.1 (especificação de cada ADR), S4 (decisões), S5 (descartados), S6 (lacunas), S1 (código).
2. `TRANSCRICAO.md`: confirme cada fala citada antes de usá-la no texto.
3. Cada arquivo de código listado em Referências: abra o arquivo e confirme que a linha existe e mostra o que o ADR afirma.
4. `assets/template-adr.md` e `references/regras.md`.

## Passo a passo

1. Leia as entradas. Não escreva nada antes de ler `references/regras.md`.
2. Para cada linha da tabela S7.1, crie `docs/adrs/<Arquivo>` copiando a estrutura de `assets/template-adr.md` e substituindo todos os campos entre colchetes. Nenhum colchete do template pode sobrar.
3. Escreva em português simples e direto. Fatos da reunião entram como decisão; lacunas entram como `[PRECISA DE INFORMAÇÃO: ...]`, dentro dos limites do plano. Nada fora do plano e da transcrição vira decisão.
4. Preencha Consequências com exatamente 3 parágrafos: `**Positivas:**`, `**Negativas:**`, `**Trade-off:**`.
5. Se `docs/adrs/` tiver qualquer arquivo fora do padrão `ADR-NNN-*.md` (por exemplo o `README.md` do boilerplate), avise o usuário e remova somente com a aprovação dele.
6. Escreva cada parágrafo e cada item de lista em uma linha só e rode o quebrador de linhas. O professor limita o ADR a 100–250 linhas físicas, e texto corrido em linha única nunca chega a 100; o script quebra em 88 colunas sem mudar o conteúdo:

```bash
python3 .claude/skills/adr-creator/scripts/quebrar_linhas.py
```

7. Execute o validador (passo obrigatório) e corrija até aparecer `RESULTADO: PASS`:

```bash
python3 .claude/skills/adr-creator/scripts/validar_adr.py
```

8. Informe ao usuário: arquivos criados, resultado do validador e as lacunas marcadas.

## Regras que não podem ser quebradas

- Cabeçalho só com Status, Data e ADRs Relacionados. Qualquer outro campo foi proibido pelo professor.
- Exatamente 7 seções `##`, com os nomes e a ordem de `assets/template-adr.md`.
- Zero blocos de código. Zero nomes de classe, método, tabela, coluna ou endpoint no texto. Esses nomes ficam no FDD. Nomes de headers do protocolo (`X-Event-Id`, `X-Signature`) e `HMAC-SHA256` são permitidos porque são a própria decisão.
- Caminhos de arquivo só na seção Referências, no formato `` `caminho:linha` ``, de 3 a 5 por ADR, todos existentes.
- De 2 a 3 alternativas; a primeira é a escolhida. Cada alternativa tem uma subseção em Prós e Contras.
- Sem sugestões futuras ("considere", "avalie", "se o volume crescer"). Perguntas abertas vão para o RFC.
- Sem emoji e sem travessão.
- Cada afirmação tem origem na transcrição ou no código. Se não tem, ela não entra.
- A `TRANSCRICAO.md` é a fonte da verdade. Se o plano, um documento ou o código divergir dela, vale a transcrição e o plano é corrigido. Uma correção vale para todos os documentos: depois de mudar um fato, procure o termo em `docs/` e rode `python3 .claude/skills/tracker-creator/scripts/conferir_consistencia.py`. Um fato que a reunião não decidiu leva "Hipótese:" em todo documento em que aparece.

## Saída

`docs/adrs/ADR-001-...md` até `ADR-007-...md`, com os nomes definidos no plano. O Tracker é gerado depois, pela skill `tracker-creator`.
