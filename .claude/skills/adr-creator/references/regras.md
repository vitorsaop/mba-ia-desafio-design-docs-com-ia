# Regras do adr-creator

## Fontes do formato

1. Professor: `plugins/adrs-management/agents/adr-generator.md`, seção "STRICT MADR FORMAT", repositório `devfullcycle/claude-mkt-place`.
2. README do desafio, requisito 4 e critérios de aceite dos ADRs.

Quando as duas fontes divergem, vale a regra de maior alcance do README (nomes de arquivo, localização e seções mínimas). Em todo o resto vale o professor.

## Tradução dos cabeçalhos (o professor permite traduzir)

| Professor (inglês) | Este projeto (pt-BR) | Por que esse nome |
| --- | --- | --- |
| Status (campo do cabeçalho) | Status | Nome exigido pelo README |
| Date | Data | Tradução |
| Related ADRs | ADRs Relacionados | Tradução |
| Context and Problem Statement | Contexto e Declaração do Problema | Contém "Contexto", exigido pelo README |
| Decision Drivers | Fatores de Decisão | Tradução |
| Considered Options | Alternativas Consideradas | Nome exigido pelo README |
| Decision Outcome | Decisão | Nome exigido pelo README |
| Pros and Cons of the Options | Prós e Contras das Alternativas | Tradução |
| Consequences | Consequências | Nome exigido pelo README |
| References | Referências | Tradução |
| [NEEDS INPUT: ...] | [PRECISA DE INFORMAÇÃO: ...] | Tradução |
| Accepted, Proposed, Deprecated, Superseded | Aceito, Proposto, Obsoleto, Substituído | Tradução |

Formato de data em pt-BR: DD-MM-AAAA.

## Onde o README manda mais que o professor

- Local dos arquivos: `docs/adrs/ADR-NNN-titulo-em-kebab-case.md`. Não usar `generated/<MÓDULO>/` nem `needs-input/`.
- Consequências: o README exige "positivas e negativas, com trade-off explícito". O professor limita Consequências a 3 parágrafos. Solução: 3 parágrafos, um para cada rótulo (`**Positivas:**`, `**Negativas:**`, `**Trade-off:**`).
- Referência ao código: o README exige que ao menos 1 ADR referencie arquivos, módulos ou classes. O professor proíbe nomes de classe no texto. Solução: caminhos reais na seção Referências (`caminho:linha`) e conceitos de módulo no texto ("módulo de pedidos", "middleware de erro centralizado").
- Número de arquivos: de 5 a 8 em `docs/adrs/`. Qualquer outro arquivo nessa pasta quebra a contagem.

## Limites do professor

- Contexto: 2 a 3 parágrafos, no máximo 300 palavras.
- Fatores de Decisão: 4 a 6 itens, uma frase cada.
- Alternativas: 2 a 3, nunca mais de 3. Se existirem mais de 3 na reunião, junte as parecidas (como o plano faz no ADR-003).
- Prós e Contras: até 4 itens por alternativa.
- Consequências: 3 parágrafos.
- Referências: de 3 a 5, no formato `caminho:linha`.
- Marcadores `[PRECISA DE INFORMAÇÃO: ...]`: no máximo 4 por ADR, cada um específico.
- Tamanho total: de 100 a 250 linhas.

## Conteúdo proibido

Código; nomes de classe, método, função, tabela ou coluna; endpoints; detalhes de implementação (cron, credenciais, caminhos de configuração); sugestões futuras; seções extras (Validação, Mais Informações, Questões em Aberto); campos extras no cabeçalho (Decision Makers, Technical Story).

## Conteúdo permitido

Conceitos de arquitetura (padrão, estratégia), tecnologias de alto nível (MySQL, Redis, HMAC-SHA256), trade-offs, razões de negócio e os nomes de headers do protocolo que são a própria decisão (`X-Event-Id`, `X-Signature`).

## Exemplo de transformação (código para conceito)

Ruim: "O método changeStatus chama publishWebhookEvent com o tx e insere em webhook_outbox."
Bom: "A mudança de status registra o evento de notificação na mesma transação do banco que atualiza o pedido."

## Como escrever Consequências

- Positivas: o que a decisão garante, com o requisito que ela atende (RNF ou RF do plano).
- Negativas: o que ela custa, incluindo lacunas assumidas (LAC) e itens adiados (ADIA).
- Trade-off: uma frase "ganha-se X em troca de Y". Nunca repita as duas listas anteriores.

## Cobertura das 6 decisões obrigatórias do README

Outbox no MySQL; retry com backoff e DLQ; HMAC-SHA256 com secret por endpoint; at-least-once com `X-Event-Id`; worker em processo separado em polling; reuso dos padrões do projeto. O validador reconhece cada uma por palavras no nome do arquivo.
