---
name: rfc-creator
description: Gera docs/RFC.md, a proposta técnica de arquitetura da feature de webhooks de pedidos, submetida à equipe para revisão, com metadados, alternativas descartadas, questões em aberto e links para os ADRs, a partir de .claude/plano/PLANO-WEBHOOKS.md, TRANSCRICAO.md e do código. Use esta skill sempre que o usuário pedir para criar, gerar, refazer, corrigir ou validar o RFC, a proposta técnica ou o documento de revisão da solução de webhooks, mesmo que ele não cite o nome da skill. Gere os ADRs antes, porque o RFC aponta para eles.
---

# rfc-creator

Gera `docs/RFC.md` com a estrutura de `assets/template-rfc.md`. O RFC responde "o que propomos e por quê" e abre os pontos pendentes para revisão. Ele não responde "como construir": isso é do FDD.

## Por que a estrutura é essa

O material do curso não traz um template de RFC. A única estrutura oficial é a lista do README do desafio (requisito 2): Metadados, Resumo executivo (TL;DR), Contexto e problema, Proposta técnica, Alternativas consideradas, Questões em aberto, Impacto e riscos, Decisões relacionadas. O template reproduz essa lista na mesma ordem, com o mesmo estilo de títulos (`###`) do PRD e do FDD do curso. Alterar nomes ou ordem quebra a validação.

## Entradas obrigatórias

1. `.claude/plano/PLANO-WEBHOOKS.md`: seção S7.2 (insumos do RFC), S5 (descartados e adiados), S6 (lacunas), S7.5 (riscos), S1 (código).
2. `docs/adrs/ADR-*.md`: o RFC precisa linkar os ADRs que já existem. Se não existirem, pare e peça a execução da skill `adr-creator`.
3. `TRANSCRICAO.md` para conferir cada fala citada.
4. `assets/template-rfc.md` e `references/regras.md`.

## Passo a passo

1. Leia as entradas, incluindo os títulos reais dos ADRs gerados.
2. Crie `docs/RFC.md` a partir de `assets/template-rfc.md`, substituindo todos os campos entre colchetes.
3. Use o nível de detalhe de arquitetura. Se uma frase só serve a quem vai programar (nome de tabela, assinatura de função, formato de header, SQL), ela pertence ao FDD: remova.
4. Em cada alternativa, escreva o trade-off que motivou o descarte e a fala da reunião (`[hh:mm] Nome`).
5. Em Questões em aberto, separe o que foi adiado na reunião do que foi identificado na análise do código, com o rótulo exato do template.
6. Execute o validador e corrija até `RESULTADO: PASS`:

```bash
python3 .claude/skills/rfc-creator/scripts/validar_rfc.py
```

7. Informe ao usuário o resultado e as questões em aberto.

## Regras que não podem ser quebradas

- Mesmos títulos, mesma ordem e mesmos rótulos de `assets/template-rfc.md`.
- Tamanho de 2 a 4 páginas: de 700 a 2300 palavras.
- Revisores são os cinco participantes da reunião, com os papéis do cabeçalho de `TRANSCRICAO.md`.
- Pelo menos 2 alternativas descartadas na reunião, cada uma com o trade-off do descarte.
- Pelo menos 2 questões em aberto que a reunião adiou ou deixou sem decisão.
- Pelo menos 2 links para ADRs existentes, no formato `[ADR-001: título](adrs/ADR-001-arquivo.md)`. O ideal é linkar todos.
- Nada descartado na reunião aparece como proposta. Nada sem origem na transcrição ou no código entra como fato.
- Sem emoji e sem travessão.
- A `TRANSCRICAO.md` é a fonte da verdade. Se o plano, um documento ou o código divergir dela, vale a transcrição e o plano é corrigido. Uma correção vale para todos os documentos: depois de mudar um fato, procure o termo em `docs/` e rode `python3 .claude/skills/tracker-creator/scripts/conferir_consistencia.py`. Um fato que a reunião não decidiu leva "Hipótese:" em todo documento em que aparece.
