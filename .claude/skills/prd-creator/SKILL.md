---
name: prd-creator
description: Gera docs/PRD.md, o Product Requirements Document da feature de webhooks de notificação de pedidos (problema, público, objetivos com métricas, escopo, requisitos funcionais e não funcionais, decisões, dependências, riscos, critérios de aceitação e testes), exatamente no esqueleto de PRD do curso, a partir de .claude/plano/PLANO-WEBHOOKS.md, TRANSCRICAO.md e do código. Use esta skill sempre que o usuário pedir para criar, gerar, refazer, corrigir ou validar o PRD, o documento de produto ou os requisitos de negócio da feature de webhooks, mesmo que ele não cite o nome da skill.
---

# prd-creator

Gera `docs/PRD.md` com a estrutura de `assets/template-prd.md`, que é o "Esqueleto de PRD (modelo de saída)" do curso. O PRD responde "por que e o quê?" em linguagem de produto. Ele consolida o que já está nos ADRs, no RFC e no FDD sem repetir o nível de detalhe deles.

## Por que o formato é rígido

O prompt do curso manda entregar o PRD "exatamente neste formato Markdown" e "seguir exatamente a estrutura de títulos, subtítulos, negrito e listas do esqueleto". O README do desafio lista 12 seções mínimas com nomes um pouco diferentes. A conciliação já está feita em `references/regras.md`: os títulos do template valem, e cada seção do README cabe numa seção do template. O validador confere os títulos, os rótulos internos, as contagens do README e a ausência de placeholders.

## Entradas obrigatórias

1. `.claude/plano/PLANO-WEBHOOKS.md`: seção S7.4 (insumos do PRD), S2 (requisitos funcionais e agrupamento em FR), S3 (não funcionais), S4 (decisões), S5 (descartados e adiados), S7.5 (riscos), S8 (critérios de aceitação).
2. `TRANSCRICAO.md`: confirme cada número e cada fala usados.
3. `docs/adrs/ADR-*.md`, `docs/RFC.md` e `docs/FDD.md`, se já existirem, para manter as decisões idênticas. Se não existirem, siga o plano.
4. `assets/template-prd.md` e `references/regras.md`.

## Passo a passo

1. Leia as entradas e `references/regras.md`.
2. Crie `docs/PRD.md` copiando a estrutura de `assets/template-prd.md`, repetindo os blocos que o template mostra duas vezes (requisitos, decisões, dependências, riscos) quantas vezes forem necessárias.
3. Escreva em linguagem de produto: o que o cliente e o operador veem, não como o código faz. Nomes de tabela, função e arquivo não entram no PRD.
4. Em cada requisito funcional, use o id `FR-NN` (dois dígitos, a partir de `FR-01`) e preencha os quatro blocos do template.
5. Para tudo que a reunião não definiu, escreva "Hipótese:" seguido da proposta. Isso vale para a meta de disponibilidade (não existe número na transcrição).
6. Execute o validador e corrija até `RESULTADO: PASS`:

```bash
python3 .claude/skills/prd-creator/scripts/validar_prd.py
```

7. Informe ao usuário o resultado e as hipóteses que dependem de confirmação.

## Regras que não podem ser quebradas

- Mesmos títulos `###`, mesma ordem, mesmos rótulos e mesmos separadores `---` do template.
- Mínimo de 8 requisitos funcionais (o plano define 12), de 1 objetivo com métrica e meta numérica (o plano define 4), de 2 itens descartados ou adiados em "Fora de escopo" e de 2 riscos com probabilidade, impacto, mitigação e plano de contingência.
- Prioridade apenas `alta`, `media` ou `baixa` (sem acento), como no template.
- Nada descartado na reunião aparece como requisito ou como item incluso.
- Português simples e direto. Sem emoji, sem travessão, sem termos vagos ("etc.", "entre outros", "adequado").
- Cada afirmação tem origem na transcrição ou no código. O PRD não carrega as citações; o Tracker as registra.
- A `TRANSCRICAO.md` é a fonte da verdade. Se o plano, um documento ou o código divergir dela, vale a transcrição e o plano é corrigido. Uma correção vale para todos os documentos: depois de mudar um fato, procure o termo em `docs/` e rode `python3 .claude/skills/tracker-creator/scripts/conferir_consistencia.py`. Um fato que a reunião não decidiu leva "Hipótese:" em todo documento em que aparece.
