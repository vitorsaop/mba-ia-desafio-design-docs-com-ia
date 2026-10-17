# ADR-001: Outbox no MySQL para publicar eventos de webhook

**Status:** Aceito
**Data:** 17-10-2026
**ADRs Relacionados:** ADR-002, ADR-003, ADR-005, ADR-007

## Contexto e Declaração do Problema

Três clientes B2B querem ser notificados quando o status dos pedidos muda e hoje
consultam a listagem de pedidos de tempos em tempos, o que deixa a integração lenta e
cara para eles. Para esses clientes, qualquer atraso abaixo de 10 segundos já é "tempo
real". A aplicação não tem nenhum mecanismo de notificação externa, de evento ou de
fila, e o banco MySQL é a única infraestrutura de dados em uso.

A mudança de status de um pedido já acontece dentro de uma transação pesada: atualiza o
pedido, grava o histórico de status e movimenta o estoque dos produtos. Chamar o
endereço de um cliente dentro dessa transação faria um cliente lento travar a mudança de
status de outros pedidos. Se o cliente estivesse fora do ar, a única saída seria
desfazer a mudança de status, o que não é aceitável.

O problema a resolver é como registrar o evento de notificação de modo que ele exista
se, e somente se, a mudança de status for confirmada, sem acoplar a mudança de status à
disponibilidade do cliente e sem exigir infraestrutura nova de um time pequeno.

## Fatores de Decisão

- O evento só pode existir se a mudança de status for confirmada, e a mudança de status
  não pode ser confirmada sem o evento.
- Um cliente lento ou indisponível não pode atrasar nem desfazer a mudança de status de
  outros pedidos.
- O time é pequeno e não deve operar infraestrutura nova para esta funcionalidade.
- A leitura dos eventos pendentes precisa ser eficiente por situação do evento e por
  data de criação.
- O conteúdo enviado ao cliente deve refletir o estado do pedido no instante da mudança,
  e os identificadores seguem o padrão UUID do projeto.

## Alternativas Consideradas

1. Outbox no MySQL existente
2. Chamada HTTP síncrona dentro do serviço de pedidos
3. Redis Streams ou outra fila externa

## Decisão

Opção escolhida: "Outbox no MySQL existente", porque grava o evento na mesma transação
SQL que atualiza o pedido e o histórico, o que garante consistência entre status e
evento sem infraestrutura nova.

A tabela de outbox usa identificadores UUID, tem índices na situação do evento e na data
de criação e guarda o conteúdo já renderizado, isto é, um retrato do estado do pedido no
instante da inserção. Um processo separado lê essa tabela e faz as chamadas HTTP
(ADR-002). O arquivamento das linhas entregues, depois de cerca de 30 dias, ficou fora
desta funcionalidade.

## Prós e Contras das Alternativas

### Outbox no MySQL existente

- Bom, porque o evento e a mudança de status são confirmados ou desfeitos juntos, sem
  inconsistência possível.
- Bom, porque reaproveita o banco, o acesso ao banco e a operação que o time já mantém.
- Ruim, porque aumenta a carga do banco transacional com escritas e leituras periódicas.
- Ruim, porque a vazão de um banco usado como fila é menor que a de um serviço de
  mensageria dedicado.

### Chamada HTTP síncrona dentro do serviço de pedidos

- Bom, porque é a solução mais simples de escrever, sem tabela nem processo adicional.
- Ruim, porque um cliente lento trava a mudança de status de outros pedidos.
- Ruim, porque um cliente fora do ar obriga a escolher entre desfazer a mudança de
  status e perder o evento.

### Redis Streams ou outra fila externa

- Bom, porque separa a entrega de eventos do banco transacional.
- Ruim, porque exige subir e operar infraestrutura nova para um time pequeno.
- Ruim, porque o registro do evento deixa de ser atômico com o banco, já que passam a
  ser dois sistemas.

## Consequências

**Positivas:** Se a transação for confirmada, o evento está registrado; se for desfeita,
o evento desaparece junto. Nenhuma infraestrutura nova é necessária, e o conteúdo
enviado ao cliente não muda se o pedido for alterado depois, porque foi gravado como
retrato no momento da mudança.

**Negativas:** O banco transacional recebe escrita adicional dentro da transação mais
pesada do sistema. A tabela cresce sem limite nesta fase, porque o arquivamento das
linhas entregues ficou fora do escopo. Uma falha ao gravar o evento desfaz a mudança de
status do pedido.

**Trade-off:** Ganha-se simplicidade operacional e consistência forte entre status e
evento. Em troca, o banco relacional passa a servir de fila, com menos vazão que um
serviço dedicado, e a latência de entrega fica ligada à leitura periódica do processo de
envio.

## Referências

- `prisma/schema.prisma:74`
- `src/modules/orders/order.service.ts:131`
- `src/modules/orders/order.service.ts:159`
- `docker-compose.yml:2`
