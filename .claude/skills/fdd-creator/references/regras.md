# Regras do fdd-creator

## Fontes do formato

1. Curso (Notion), página "Prompt para geração de um FDD", bloco "Esqueleto de FDD (modelo de saída)". Cabeçalho `### FDD: [nome da feature]` com Versão, Data e Responsável; 10 seções `### N. Título`; separadores `---` entre seções.
2. README do desafio, requisito 3: seções mínimas, matriz `WEBHOOK_*`, estratégias de resiliência e a seção "Integração com o sistema existente".

## Conciliação entre as duas fontes

| README | Onde fica no template |
| --- | --- |
| Contexto e motivação técnica | 1 |
| Objetivos técnicos | 2 |
| Escopo e exclusões | 3 |
| Fluxos detalhados (outbox, worker, retry, DLQ) | 4, "Fluxo principal" e "Fluxos alternativos e exceções" |
| Contratos públicos | 5 |
| Matriz de erros previstos com códigos `WEBHOOK_*` | 6, tabela depois do bullet "Matriz de erros previstos e tratamentos" |
| Estratégias de resiliência (timeouts, retries, backoff, fallback) | 6, bullets "Estratégias de resiliência" e "Política de fallback" |
| Observabilidade (métricas, logs, tracing) | 7 |
| Dependências e compatibilidade | 8 |
| Critérios de aceite técnicos | 9 |
| Riscos e mitigação | 10 |
| Integração com o sistema existente | 11 (única adição, exigida pelo README) |

## Adaptações ao projeto

- O template diz "encaixe no HLD". Este projeto não tem HLD: descreva o encaixe no código existente.
- O template lista "circuit breaker" entre as estratégias. A reunião não o discutiu: escreva "circuit breaker: não previsto nesta fase (não discutido na reunião)".
- O template tem `[status/header 1 — significado]` com travessão. A regra de estilo do próprio prompt proíbe travessão, então o separador é dois-pontos.

## Formatos

- Cabeçalho: `Versão: 1.0`, `Data: 2026-10-17`, `Responsável: Vitor Oliveira`.
- Contrato: `**Contrato N: nome**`, depois os quatro bullets do template, depois `**Exemplo de requisição**` e `**Exemplo de resposta**`, cada um com um bloco de código. Bloco `json` precisa ser JSON válido (sem `...`). Requisição sem corpo usa bloco `http`.
- Tipos de contrato permitidos: function, method, endpoint, queue, stream, sdk.
- Envelope de erro do código (`src/middlewares/error.middleware.ts:15`): `{ "error": { "code", "message", "details" } }`. Listas seguem `{ "data": [], "pagination": { "page", "pageSize", "total", "totalPages" } }` (`src/shared/http/response.ts:13`).
- Campos da API de configuração em camelCase (padrão de `src/modules/orders/order.schemas.ts`); payload e headers do evento exatamente como decididos em `[09:43] Diego` e `[09:44] Sofia`.
- Matriz de erros: colunas `Código | Condição | Status HTTP | Tratamento | Notas`. Códigos internos do worker usam "interno" em Status HTTP.
- Dependências: colunas `Versão mínima | Componente | Observações`.
- Risco (seção 10): `### Nome`, `- Probabilidade: baixa|média|alta`, `- Impacto:`, `- Mitigação:` com sub-bullets, `- Plano de contingência:`.
- Seção 11: colunas `Caminho | Situação atual | Integração do módulo de webhooks`; o caminho vai entre crases, com `:linha` quando fizer sentido.

## Como tratar hipóteses

Tudo que o plano marca como classe C, ou como "Hipótese", começa com "Hipótese:" no texto. O leitor deve saber, sem consultar o plano, o que foi decidido na reunião e o que é proposta do FDD. Nunca escreva uma hipótese como se fosse decisão.

## Diagramas

Dois blocos Mermaid na seção 4, dentro do bullet de Diagramas ou logo depois dele: sequência (API, banco, worker, cliente) e estados da linha da outbox. Use apenas os estados e transições descritos no plano.

## Estilo

Português simples e direto. Sem emoji, sem travessão. Cada número tem unidade. Cada fato tem origem.
