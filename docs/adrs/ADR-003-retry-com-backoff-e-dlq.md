# ADR-003: Retry com backoff exponencial e DLQ em tabela separada

**Status:** Aceito
**Data:** 17-10-2026
**ADRs Relacionados:** ADR-001, ADR-002, ADR-005

## Contexto e Declaração do Problema

Os clientes podem ficar fora do ar. A reunião citou um cliente que já teve
indisponibilidade de duas horas em manutenção planejada. Quando um envio falha ou não
recebe resposta em 10 segundos, o sistema precisa tentar de novo sem sobrecarregar o
cliente e sem manter o evento pendente para sempre.

Tentar de novo indefinidamente deixaria eventos pendurados quando o cliente desaparece.
Poucas tentativas, como três, encerrariam o evento em cerca de 30 minutos, antes de uma
manutenção de duas horas terminar. Também era preciso decidir onde guardar os eventos
que esgotam as tentativas e quem os reprocessa. O aviso por e-mail ao cliente ficou fora
desta fase.

A decisão precisa fixar três coisas: quantas vezes o sistema tenta de novo, quanto
espera entre as tentativas e para onde vai o evento quando todas falham.

## Fatores de Decisão

- Cobrir indisponibilidades do cliente de várias horas.
- Não manter eventos pendurados indefinidamente.
- Não sobrecarregar um cliente que está se recuperando com tentativas em sequência
  rápida.
- Conservar o conteúdo e o motivo da falha como evidência para depuração e
  reprocessamento.
- Manter simples a leitura da outbox principal.
- Permitir o reprocessamento manual somente por quem tem papel de administrador.

## Alternativas Consideradas

1. Cinco retentativas com espera crescente e DLQ em tabela separada
2. Outro número de tentativas, como três tentativas ou retry indefinido
3. Marcar o evento como falho na própria outbox, sem tabela separada

## Decisão

Opção escolhida: "Cinco retentativas com espera crescente e DLQ em tabela separada",
porque cobre cerca de 14,6 horas de indisponibilidade, deixa nenhum evento pendurado e
guarda a evidência fora da leitura principal.

Depois da primeira falha, o sistema repete o envio após 1 minuto, 5 minutos, 30 minutos,
2 horas e 12 horas. Interpretação adotada: as 5 tentativas decididas são 5 retentativas
depois do envio inicial, no máximo 6 requisições por ciclo de entrega, porque a soma das
esperas é de 876 minutos, o que corresponde às "quase 15 horas" citadas na reunião.
[PRECISA DE INFORMAÇÃO: "5 tentativas" significa 5 retentativas depois do envio inicial,
ou 5 envios no total?] O PM considerou aceitável essa janela: um cliente que fica fora
do ar por esse tempo já tem um problema sério do lado dele.

Esgotadas as retentativas, o evento vai para a DLQ com o conteúdo, o motivo da falha e a
data, e só volta para a fila por reprocessamento manual de um administrador.

## Prós e Contras das Alternativas

### Cinco retentativas com espera crescente e DLQ em tabela separada

- Bom, porque cobre cerca de 14,6 horas, bem mais que a manutenção de 2 horas citada.
- Bom, porque as esperas crescentes evitam sobrecarregar um cliente que está se
  recuperando.
- Bom, porque a tabela separada mantém simples a leitura da outbox e serve de evidência.
- Ruim, porque um cliente fora do ar por mais de 14,6 horas só volta a receber o evento
  por reprocessamento manual.

### Outro número de tentativas, como três tentativas ou retry indefinido

- Bom, porque três tentativas liberam o evento mais cedo.
- Bom, porque o retry indefinido nunca descarta um evento.
- Ruim, porque três tentativas encerram o evento antes de uma manutenção de 2 horas
  acabar.
- Ruim, porque o retry indefinido deixa o evento pendurado para sempre se o cliente
  desaparecer.

### Marcar o evento como falho na própria outbox, sem tabela separada

- Bom, porque não cria uma tabela adicional.
- Bom, porque o reprocessamento seria apenas uma mudança de situação da mesma linha.
- Ruim, porque mistura eventos encerrados com eventos ativos na leitura principal.
- Ruim, porque enfraquece a evidência disponível para depuração e reprocessamento.

## Consequências

**Positivas:** A janela de cerca de 14,6 horas cobre manutenções planejadas, nenhum
evento fica pendurado e a DLQ preserva o conteúdo, o motivo e a data de cada falha
permanente. O reprocessamento fica restrito a administradores e registra em log quem o
executou.

**Negativas:** Um cliente fora do ar por mais de 14,6 horas só recebe o evento depois de
um reprocessamento manual, e como o aviso por e-mail ficou fora desta fase, o cliente
não é avisado da falha. [PRECISA DE INFORMAÇÃO: o que acontece com a linha da DLQ depois
do reprocessamento?]

**Trade-off:** Ganha-se um tempo máximo de espera previsível e uma evidência separada
das falhas. Em troca, os eventos de clientes fora do ar por muito tempo passam a
depender de ação humana.

## Referências

- `src/middlewares/auth.middleware.ts:49`
- `src/shared/logger/index.ts:13`
- `prisma/schema.prisma:116`
