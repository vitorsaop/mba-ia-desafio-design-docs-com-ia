# Regras do prd-creator

## Fontes do formato

1. Curso (Notion), página "Prompt de Entrevista para Gerar PRD para desenvolvimento de Feature", blocos "Esqueleto de PRD (modelo de saída)", "Checagens de Consistência antes de finalizar" e "Estilo".
2. README do desafio, requisito 1 e critérios de aceite do PRD.

## Conciliação entre as duas fontes

O template do curso manda nos títulos. O README manda no conteúdo mínimo. As 12 seções do README cabem no template assim:

| README | Onde fica no template |
| --- | --- |
| Resumo e contexto da feature | `### Resumo` e o bloco "Onde essa feature será implantada" |
| Problema e motivação | `### Contexto e problema`, bloco "Problemas priorizados" |
| Público-alvo e cenários de uso | `### Contexto e problema`, blocos "Público-alvo" e "Cenários de uso chave" |
| Objetivos e métricas de sucesso | `### Objetivos e métricas` |
| Escopo (incluso e fora de escopo) | `### Escopo` |
| Requisitos funcionais | `### Requisitos funcionais` |
| Requisitos não funcionais | `### Requisitos não funcionais` |
| Decisões e trade-offs principais | `### Decisões e trade-offs` |
| Dependências | `### Dependências` |
| Riscos e mitigação | `### Riscos e mitigação` |
| Critérios de aceitação | `### Critérios de aceitação` |
| Estratégia de testes e validação | `### Testes e validação`, bloco "Estratégia de validação" |

O template ainda tem `### Arquitetura e abordagem`, que o README não lista. Mantenha, em nível de produto.

## Regras de estilo do curso

- Português simples e direto.
- Sem travessão do tipo "—".
- Seguir exatamente títulos, subtítulos, negrito e listas do esqueleto.
- Marcar como "Hipótese:" o que o usuário não definiu.

## Checagens de consistência do curso (todas viram verificação do validador ou da leitura final)

- Cada objetivo tem métrica e meta alvo.
- Todo requisito funcional tem nome, descrição, fluxo principal e prioridade.
- Requisitos não funcionais incluem pelo menos performance e disponibilidade, mesmo que como hipótese.
- Fora de escopo não contradiz o que está incluso.
- Toda decisão relevante tem justificativa e trade-off.
- Cada dependência é clara e específica.
- Cada risco tem probabilidade, impacto, mitigação e plano de contingência.
- Os critérios de aceitação são objetivos e verificáveis.
- Os tipos de teste obrigatórios estão definidos.

## Formatos

- Cabeçalho: `### PRD: Order Management System (OMS) Sistema de Webhooks de Notificação de Pedidos`, `Versão: 1.0`, `Data: 2026-10-17`, `Responsável: Vitor Oliveira`.
- Requisito funcional: `#### FR-01 Nome` e a descrição na linha seguinte, depois os blocos `**Fluxo principal**`, `**Fluxos alternativos e exceções**`, `**Erros previstos**` e `**Prioridade:** alta`. Blocos separados por `---`.
- Prioridade (critério do autor, ver S2 do plano): `alta` para o que aparece no resumo final de `[09:48] Larissa`; `media` para o que o PM pediu e ficou fora do resumo.
- Dependência: `#### organizacional: título`, `#### técnica: título` ou `#### externa: título`.
- Risco: `#### frase`, `- **Probabilidade:** baixa|media|alta` (sem acento), `- **Impacto:**`, `- **Mitigação:**` com sub-bullets, `- **Plano de contingência:**`.
- Decisão: `#### Decisão: título`, `- **Justificativa:**`, `- **Trade-off:**`.
- Critérios: a linha "Checklist objetivo que define se a feature está pronta." e depois bullets objetivos (com número ou comportamento observável).

## Requisitos não funcionais: os 8 rótulos

Performance; Disponibilidade; Segurança e autorização; Observabilidade; Confiabilidade e integridade de dados; Compatibilidade e portabilidade; Compliance; Acessibilidade no frontend consumidor. Todos aparecem, mesmo quando o item for "não discutido na reunião" ou "não se aplica nesta fase". Em Disponibilidade, escreva "Hipótese:" e não invente porcentagem de uptime.

## Fronteira com os outros documentos

O PRD não traz nome de tabela, de classe, de função nem de endpoint administrativo com corpo e headers. Isso é do FDD. Ele pode citar os ADRs pelo número ("ver ADR-001") para quem quiser o detalhe.
