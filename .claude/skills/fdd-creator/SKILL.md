---
name: fdd-creator
description: Gera docs/FDD.md, o Feature Design Document da feature de webhooks de pedidos (como implementar em detalhe, com fluxos, contratos HTTP com exemplos, matriz de erros WEBHOOK_*, resiliência, observabilidade, critérios de aceite, riscos e integração com o código existente), no template do curso, a partir de .claude/plano/PLANO-WEBHOOKS.md, TRANSCRICAO.md e do código. Use esta skill sempre que o usuário pedir para criar, gerar, refazer, corrigir ou validar o FDD, o design de implementação, os contratos de API ou a integração com o código da feature de webhooks, mesmo que ele não cite o nome da skill.
---

# fdd-creator

Gera `docs/FDD.md` com a estrutura de `assets/template-fdd.md`: as 10 seções numeradas do template do curso mais a seção 11, "Integração com o sistema existente", exigida pelo README do desafio. O FDD é o documento mais técnico do pacote: um desenvolvedor deve conseguir começar a programar só com ele.

## Por que o formato é rígido

O template vem do bloco "Esqueleto de FDD (modelo de saída)" da página "Prompt para geração de um FDD" do curso, que manda renderizar "exatamente" aquele Markdown. A seção 11 é a única adição e fica depois da 10 para não renumerar nada. O validador confere títulos, ordem, rótulos e os exemplos JSON, porque é aí que um FDD gerado por IA costuma se desviar.

## Entradas obrigatórias

1. `.claude/plano/PLANO-WEBHOOKS.md`: seção S7.3 (insumos do FDD), S1 (código), S2 a S4 (requisitos e decisões), S6 (lacunas), S7.5 (riscos), S8 (critérios de aceite).
2. `TRANSCRICAO.md`: confirme os valores decididos (tempos, limites, headers, nomes de tabela).
3. Os arquivos de código da tabela S1. Abra cada um e confirme caminho, linha e comportamento antes de citá-lo.
4. `docs/adrs/ADR-*.md`: o FDD detalha o que os ADRs decidiram e não pode contradizê-los.
5. `assets/template-fdd.md` e `references/regras.md`.

## Passo a passo

1. Leia as entradas. Confirme no código os formatos que o FDD vai reproduzir (envelope de erro, paginação, nomes de campo).
2. Crie `docs/FDD.md` copiando a estrutura de `assets/template-fdd.md` e substituindo todos os campos entre colchetes.
3. Seção 4: cubra os quatro fluxos exigidos (criação do evento na outbox, processamento pelo worker, retry, DLQ) e inclua dois diagramas Mermaid.
4. Seção 5: um bloco por contrato, com exemplo de requisição e de resposta em JSON válido. Para requisição sem corpo, use um bloco `http` com a linha da requisição e os headers.
5. Seção 6: a matriz de erros vai logo depois do primeiro bullet, como tabela; os outros três bullets levam sub-bullets.
6. Marque com "Hipótese:" tudo que o plano classifica como lacuna (classe C) ou como proposta (LAC-03, LAC-04, LAC-10, LAC-13, LAC-15, LAC-16, LAC-17, LAC-19). Não transforme hipótese em decisão.
7. Seção 11: uma linha por arquivo do código que o módulo toca; arquivos que ainda não existem levam o sufixo "(arquivo novo)" ou, para vários na mesma linha, "(arquivos novos)".
8. Execute o validador e corrija até `RESULTADO: PASS`:

```bash
python3 .claude/skills/fdd-creator/scripts/validar_fdd.py
```

9. Informe ao usuário o resultado e a lista de hipóteses que a revisão de segurança ou o PM precisam confirmar.

## Regras que não podem ser quebradas

- Mesmos títulos, mesma numeração e mesmos rótulos do template. O título de risco da seção 10 também é `###`, como no template.
- Mínimo de 4 endpoints com exemplo de requisição, exemplo de resposta e status codes. Este projeto tem 7 endpoints, mais o contrato de saída e a função de publicação.
- Toda sigla `WEBHOOK_*` citada no documento existe na matriz de erros.
- Mínimo de 4 caminhos de arquivo reais na seção 11. Qualquer caminho no documento que não exista no repositório precisa do sufixo "(arquivo novo)" na mesma linha.
- A seção 7 cita métricas, logs e tracing.
- Nada descartado na reunião vira requisito. Nada sem origem na transcrição ou no código entra como fato.
- Sem emoji e sem travessão (o template original tem um travessão em um placeholder; ele foi trocado por dois-pontos).
- A `TRANSCRICAO.md` é a fonte da verdade. Se o plano, um documento ou o código divergir dela, vale a transcrição e o plano é corrigido. Uma correção vale para todos os documentos: depois de mudar um fato, procure o termo em `docs/` e rode `python3 .claude/skills/tracker-creator/scripts/conferir_consistencia.py`. Um fato que a reunião não decidiu leva "Hipótese:" em todo documento em que aparece.
