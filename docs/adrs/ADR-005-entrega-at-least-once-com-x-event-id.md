# ADR-005: Entrega at-least-once com identificador de evento no header

**Status:** Aceito
**Data:** 17-10-2026
**ADRs Relacionados:** ADR-001, ADR-003, ADR-004, ADR-007

## Contexto e Declaração do Problema

O sistema precisa definir qual garantia de entrega oferece ao cliente. Quando o cliente
recebe o evento mas a confirmação não chega ao sistema, por falha de rede ou por tempo
esgotado, o envio é repetido e o cliente recebe o mesmo evento duas vezes. Evitar
totalmente essa repetição exigiria coordenação entre o sistema e o cliente.

Provedores conhecidos de webhook, como Stripe e GitHub, entregam o evento ao menos uma
vez e enviam um identificador único para o cliente reconhecer repetições. A reunião
aceitou que essa escolha transfere ao cliente a responsabilidade de deduplicar e decidiu
que o PM documenta isso de forma destacada no portal do desenvolvedor.

Durante a discussão, a primeira pergunta foi como o cliente diferencia um evento
repetido de um evento novo. A resposta definiu a forma do identificador: um valor único,
gerado quando o evento entra na outbox e enviado em um header de todo envio.

## Fatores de Decisão

- Nenhum evento pode ser perdido por falha de confirmação.
- A solução deve ser simples para quem envia e não depender de coordenação com o
  cliente.
- O cliente precisa de um identificador estável para reconhecer repetições.
- O identificador deve ser único por evento e nascer quando o evento entra na outbox.
- A prática deve ser a mesma de provedores de webhook conhecidos pelos clientes.
- A responsabilidade do cliente precisa ser clara e documentável no portal do
  desenvolvedor.

## Alternativas Consideradas

1. Entrega ao menos uma vez (at-least-once) com identificador do evento no header
2. Entrega exatamente uma vez (exactly-once)
3. Entrega ao menos uma vez sem identificador, com o cliente comparando o conteúdo
   (plausível, não discutida como alternativa na reunião)

## Decisão

Opção escolhida: "Entrega ao menos uma vez com identificador do evento no header",
porque garante que nenhum evento se perde por falha de confirmação e resolve a repetição
com um mecanismo simples e conhecido.

Cada evento recebe um UUID quando entra na outbox, e esse valor viaja no header
X-Event-Id de todo envio daquele evento. Se o cliente receber o mesmo evento mais de uma
vez, ele descarta as repetições comparando o valor desse header. A repetição de entrega
é possível e faz parte do contrato com o cliente.

O reenvio acontece quando o cliente não confirma o recebimento, seja por tempo esgotado,
seja por erro de conexão ou por resposta de falha. Nessas repetições o sistema mantém o
mesmo identificador, de modo que o cliente reconhece a repetição pelo valor do header e
não pelo momento em que ela chegou. A reunião tratou a deduplicação do lado do cliente
como o padrão de mercado, e não como uma exceção desta integração.

## Prós e Contras das Alternativas

### Entrega ao menos uma vez (at-least-once) com identificador do evento no header

- Bom, porque garante que nenhum evento se perde por falha de confirmação.
- Bom, porque é a prática de provedores como Stripe e GitHub.
- Bom, porque o identificador é estável entre as tentativas de envio do mesmo evento.
- Ruim, porque o cliente pode receber repetições e precisa deduplicar.

### Entrega exatamente uma vez (exactly-once)

- Bom, porque o cliente nunca veria repetições.
- Ruim, porque exige coordenação entre o sistema e o cliente, muito mais complexa.
- Ruim, porque a complexidade recai sobre os dois lados da integração.
- Bom, porque eliminaria a necessidade de documentar a deduplicação para os clientes.

### Entrega ao menos uma vez sem identificador, com o cliente comparando o conteúdo

- Bom, porque não exige um header adicional.
- Ruim, porque o cliente não distingue com segurança uma repetição de dois eventos
  legítimos parecidos.
- Ruim, porque cada cliente teria de criar a sua própria regra de comparação.

## Consequências

**Positivas:** A entrega não perde eventos por falha de confirmação. A solução não
depende de coordenação com o cliente e usa um identificador que já nasce com o evento,
estável entre as tentativas de envio.

**Negativas:** O cliente precisa deduplicar pelo identificador do evento, e um cliente
que não o faça pode processar o mesmo pedido duas vezes. A documentação para os clientes
passa a ser parte da entrega, e a repetição pode ocorrer depois de qualquer falha entre
o envio e a confirmação.

**Trade-off:** Ganha-se simplicidade e ausência de perda de eventos para quem envia. Em
troca, a responsabilidade de deduplicar passa para o cliente, que a reunião tratou como
aceitável e como risco a ser mitigado por documentação.

## Referências

- `prisma/schema.prisma:26`
- `package.json:32`
- `src/middlewares/request-logger.middleware.ts:6`
- `src/middlewares/request-logger.middleware.ts:8`
- `src/modules/orders/order.service.ts:131`
