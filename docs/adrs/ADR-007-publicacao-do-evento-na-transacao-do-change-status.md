# ADR-007: Publicação do evento dentro da transação de mudança de status

**Status:** Aceito
**Data:** 17-10-2026
**ADRs Relacionados:** ADR-001, ADR-005, ADR-006

## Contexto e Declaração do Problema

A mudança de status de um pedido roda em uma única transação que valida a transição,
movimenta o estoque, atualiza o pedido e grava o histórico. A reunião decidiu que o
evento de webhook precisa nascer dentro dessa mesma transação: se a gravação do evento
falhar, a mudança de status é desfeita, e não pode existir caso em que o status muda e o
evento não sai.

Havia duas formas de entregar o evento ao módulo de webhooks: injetar no serviço de
pedidos o repositório completo de webhooks, ou chamar uma função de publicação que
recebe o cliente da transação corrente. Também ficou decidido que o filtro por status do
webhook é aplicado na gravação do evento: se nenhum webhook do cliente do pedido quer
aquele status, nada é gravado, o que poupa linhas na tabela.

A função de publicação recebe o pedido e os dois status da transição, o de origem e o de
destino, porque o evento informa de qual status para qual status o pedido passou.

## Fatores de Decisão

- O evento deve ser confirmado ou desfeito junto com a mudança de status.
- O serviço de pedidos deve ficar pouco acoplado ao módulo de webhooks.
- Linhas desnecessárias não devem ser gravadas quando nenhum webhook quer o status.
- A alteração no código existente deve ser mínima e localizada.
- O conteúdo do evento deve refletir o pedido no instante da mudança.
- O evento deve informar o status de origem e o status de destino da transição.

## Alternativas Consideradas

1. Função de publicação que recebe o cliente da transação corrente
2. Injetar o repositório de webhooks no serviço de pedidos
3. Publicar o evento depois da confirmação da transação

## Decisão

Opção escolhida: "Função de publicação que recebe o cliente da transação corrente",
porque garante a atomicidade entre status e evento sem acoplar o serviço de pedidos ao
repositório inteiro de webhooks.

A função é chamada pela mudança de status logo depois do registro do histórico e antes
da releitura do pedido. Ela consulta os webhooks ativos do cliente do pedido que assinam
o novo status, monta o conteúdo do evento a partir do pedido e grava uma linha na outbox
para cada webhook interessado, tudo na transação em andamento.

A reunião integrou a função apenas na mudança de status. Se a criação de pedido também
deve gerar evento, a reunião não decidiu; o status inicial pendente não é destino de
nenhuma transição.

O conteúdo do evento é montado com os dados do pedido que não mudam com a transição
(identificador, número, cliente e total) e com os dois status da transição. Os itens do
pedido não entram no evento: o cliente que precisar deles consulta o pedido depois.

## Prós e Contras das Alternativas

### Função de publicação que recebe o cliente da transação corrente

- Bom, porque o evento e a mudança de status compartilham a mesma transação.
- Bom, porque o serviço de pedidos só conhece uma função, e não o repositório de
  webhooks.
- Bom, porque a montagem do serviço de pedidos não precisa mudar.
- Ruim, porque o módulo de pedidos passa a depender do módulo de webhooks.

### Injetar o repositório de webhooks no serviço de pedidos

- Bom, porque a dependência fica explícita no construtor do serviço.
- Ruim, porque acopla o serviço de pedidos a todo o repositório de webhooks.
- Ruim, porque exige alterar a montagem do serviço de pedidos.

### Publicar o evento depois da confirmação da transação

- Bom, porque mantém a transação de status curta.
- Bom, porque uma falha na gravação do evento não desfaria a mudança de status.
- Ruim, porque perde toda a garantia de atomicidade: o status pode mudar sem que o
  evento seja gravado.

## Consequências

**Positivas:** Não existe status alterado sem evento, nem evento sem status alterado. O
serviço de pedidos muda pouco: ganha uma chamada dentro da transação existente, sem
alteração na montagem do serviço. O filtro na gravação evita linhas para webhooks que
não querem o status.

**Negativas:** A transação de mudança de status fica mais longa, porque inclui a
consulta dos webhooks e as gravações na outbox. Uma falha na gravação do evento desfaz a
mudança de status, por decisão da reunião. [PRECISA DE INFORMAÇÃO: a criação de pedido
deve gerar evento, ou só a mudança de status?]

**Trade-off:** Ganha-se atomicidade forte entre status e evento. Em troca, a transação
mais sensível do sistema passa a fazer mais trabalho, e o módulo de pedidos passa a
depender do módulo de webhooks.

## Referências

- `src/modules/orders/order.service.ts:126`
- `src/modules/orders/order.service.ts:159`
- `src/modules/orders/order.status.ts:3`
- `src/modules/orders/order.service.ts:24`
- `prisma/schema.prisma:116`
