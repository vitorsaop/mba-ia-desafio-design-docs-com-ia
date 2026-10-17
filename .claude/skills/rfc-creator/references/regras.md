# Regras do rfc-creator

## Fonte do formato

README do desafio, requisito 2 e critérios de aceite do RFC. Não existe template de RFC no material do curso (páginas "Design Docs", "Design e Arquitetura" e "Classificação geral de documentos" do Notion). O título, o estilo de separadores (`---`) e o nível de título (`###`) acompanham o PRD e o FDD do curso para o pacote ter um aspecto único.

## Papel do RFC e fronteira com os outros documentos

| Documento | Pergunta | O que fica fora do RFC |
| --- | --- | --- |
| RFC | Como pretendemos resolver e o que ainda está em aberto? | Nada de tabela, coluna, assinatura de função, formato de header ou código |
| ADR | Por que decidimos exatamente assim? | O RFC resume em uma linha e linka |
| FDD | Como construir, em detalhe? | O RFC não repete fluxos, contratos nem matriz de erros |
| PRD | Por que e o quê? | O RFC não repete métricas de negócio nem cenários de uso |

Teste prático: se a frase só ajuda quem vai escrever código, ela é do FDD.

## Metadados

- Autor: Vitor Oliveira.
- Status: Em revisão (o RFC é submetido à equipe).
- Data: 2026-10-17 (a transcrição não informa a data da reunião).
- Revisores (papéis do cabeçalho de `TRANSCRICAO.md`): Larissa (Tech Lead), Marcos (Product Manager), Bruno (Engenheiro Pleno, time de Pedidos), Diego (Engenheiro Sênior, time de Plataforma), Sofia (Engenheira de Segurança).

## Como preencher cada seção

- Resumo executivo (TL;DR): 3 a 5 frases. Inclua a decisão central (outbox no MySQL com worker separado), a garantia (at-least-once) e o pedido de revisão.
- Contexto e problema: pedido dos 3 clientes B2B, polling do `GET /orders`, risco comercial da Atlas, e o vácuo no código (sem eventos, filas ou webhooks). Use a latência de 10 segundos como requisito.
- Proposta técnica: um bullet por decisão do plano S7.2 (PROP-1 a PROP-6), cada um com link para o ADR. Sem nomes de tabela.
- Alternativas consideradas: as alternativas listadas em S7.2. Para DESC-04 e DESC-05, escreva um único bullet ("outro número de tentativas").
- Questões em aberto: as listas de S7.2. As adiadas na reunião levam a fala; as da análise levam o rótulo "Lacuna identificada na análise." e dizem de onde vêm (LAC no plano, fala ou arquivo).
- Impacto e riscos: impactos de S7.2 e riscos RISK-01 a RISK-05 em uma frase cada, com probabilidade, impacto e mitigação.
- Decisões relacionadas: um link por ADR existente.

## Estilo

Português simples e direto. Sem emoji, sem travessão. Cada fato tem origem. Termos técnicos usados na reunião (outbox, DLQ, at-least-once, HMAC) são definidos na primeira ocorrência, em uma frase.
