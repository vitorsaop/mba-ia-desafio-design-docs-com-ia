### RFC-001: Sistema de Webhooks de Notificação de Pedidos

### Metadados

| Campo | Valor |
| --- | --- |
| Autor | Vitor Oliveira |
| Status | Em revisão |
| Data | 2026-10-17 |
| Revisores | Larissa (Tech Lead), Marcos (Product Manager), Bruno (Engenheiro Pleno, time de Pedidos), Diego (Engenheiro Sênior, time de Plataforma), Sofia (Engenheira de Segurança) |

---

### Resumo executivo (TL;DR)

Propomos notificar os clientes B2B por webhooks de saída sempre que o status de um pedido mudar. O evento é gravado em uma tabela de outbox no MySQL, na mesma transação da mudança de status, e um worker em processo separado o envia ao cliente, assinado com HMAC-SHA256, com até 5 tentativas de envio e uma DLQ para as falhas permanentes. A garantia é at-least-once, com um identificador de evento para o cliente deduplicar. A meta é notificar em menos de 10 segundos e entregar em 3 sprints. Pedimos aos revisores que confirmem a proposta e se posicionem sobre as questões em aberto, em especial as de segurança, que a Sofia revisa antes do deploy.

---

### Contexto e problema

Três clientes B2B (Atlas Comercial, MaxDistribuição e Nova Cargo) pediram para ser notificados em tempo real quando o status dos pedidos muda. Hoje eles consultam a listagem de pedidos de tempos em tempos, o que deixa a integração lenta e cara. Para eles, "tempo real" é qualquer atraso abaixo de 10 segundos. A Atlas indicou que pode migrar para um concorrente se a entrega passar do fim do trimestre. O webhook é só de saída: os clientes recebem, não enviam.

A aplicação não tem nenhum mecanismo de notificação externa, de evento, de fila ou de webhook, e o banco MySQL é a única infraestrutura de dados em uso. A mudança de status já roda em uma transação pesada, que atualiza o pedido, grava o histórico e movimenta o estoque. Uma chamada HTTP dentro dela faria um cliente lento travar a mudança de status de outros pedidos e obrigaria a desfazer a mudança se o cliente estivesse fora do ar.

Neste documento, outbox é uma tabela no próprio banco onde o evento é gravado na mesma transação da mudança de status, e DLQ (dead letter queue) é a tabela dos eventos que esgotaram as tentativas.

---

### Proposta técnica

A solução registra o evento de forma atômica e o entrega de forma assíncrona. Seis elementos formam a proposta: o registro do evento dentro da transação do pedido, um processo de envio separado da API, uma política de repetição que isola as falhas permanentes, uma assinatura que prova a origem do evento, a garantia de entrega at-least-once e uma API de configuração. A configuração dos webhooks e o histórico de entregas ficam expostos por uma API REST no padrão dos módulos existentes.

- **Registro atômico do evento.** A mudança de status grava o evento na outbox, na mesma transação, com o conteúdo já renderizado e somente para os webhooks que assinam o novo status. Se a gravação falhar, a mudança de status é desfeita. Ver [ADR-001](adrs/ADR-001-outbox-no-mysql.md) e [ADR-007](adrs/ADR-007-publicacao-do-evento-na-transacao-do-change-status.md).
- **Envio por um worker separado.** Um processo próprio consulta a outbox a cada 2 segundos, com um único worker, e envia cada evento ao cliente com timeout de 10 segundos. Ver [ADR-002](adrs/ADR-002-worker-separado-em-polling.md).
- **Repetição e isolamento de falhas.** Falha ou timeout agenda nova tentativa depois de 1 minuto, 5 minutos, 30 minutos, 2 horas e 12 horas, o que cobre cerca de 14,6 horas. Depois da última retentativa, o evento vai para a DLQ e um administrador pode reprocessá-lo. Ver [ADR-003](adrs/ADR-003-retry-com-backoff-e-dlq.md).
- **Assinatura por endpoint.** Cada envio leva uma assinatura HMAC-SHA256 do corpo, com uma secret única por endpoint, que o cliente pode rotacionar com 24 horas de sobreposição. Ver [ADR-004](adrs/ADR-004-hmac-sha256-secret-por-endpoint.md).
- **Entrega at-least-once.** Cada evento leva um identificador único para o cliente deduplicar repetições. Ver [ADR-005](adrs/ADR-005-entrega-at-least-once-com-x-event-id.md).
- **API de configuração e histórico.** Cadastro, listagem, edição e remoção de webhooks, escolha dos status que cada webhook quer receber, rotação de secret e consulta do histórico de entregas, com autenticação normal. O reprocessamento da DLQ exige o papel de administrador. Ver [ADR-006](adrs/ADR-006-reuso-dos-padroes-do-projeto.md).

---

### Alternativas consideradas

- **Alternativa: chamada HTTP síncrona no serviço de pedidos.** O serviço de pedidos chamaria o cliente dentro da transação de mudança de status. **Trade-off do descarte:** seria a solução mais simples, mas um cliente lento travaria a mudança de status de outros pedidos, e um cliente fora do ar obrigaria a desfazer a mudança. ([09:04] Bruno)
- **Alternativa: Redis Streams ou outra fila externa.** A entrega sairia do banco para uma fila dedicada. **Trade-off do descarte:** separaria a entrega do banco transacional, mas exigiria subir e operar infraestrutura nova para um time pequeno, e o registro do evento deixaria de ser atômico com o banco. ([09:07] Diego)
- **Alternativa: gatilho do banco para avisar o worker.** O banco avisaria o processo de envio quando houvesse evento novo. **Trade-off do descarte:** reagiria sem esperar o intervalo de consulta, mas o MySQL não notifica processos externos e o gatilho só executa SQL, o que obrigaria a improvisos. ([09:09] Diego)
- **Alternativa: outro número de tentativas, com retry indefinido ou apenas 3 tentativas.** **Trade-off do descarte:** o retry indefinido deixa eventos pendurados se o cliente desaparecer, e 3 tentativas encerrariam o evento em cerca de 30 minutos, antes de uma manutenção de 2 horas terminar. ([09:15] Diego; [09:16] Bruno; [09:16] Diego)
- **Alternativa: entrega exatamente uma vez (exactly-once).** **Trade-off do descarte:** o cliente nunca veria repetições, mas isso exigiria coordenação entre o sistema e o cliente, muito mais complexa. ([09:25] Diego)
- **Alternativa: worker dentro do processo da API.** **Trade-off do descarte:** dispensaria um processo adicional, mas reiniciar a API perderia o worker. ([09:11] Diego)

---

### Questões em aberto

- **Adiada na reunião.** Limitar a taxa de envio por cliente: se um cliente tiver 50 pedidos mudando de status em um minuto, ele recebe 50 chamadas. A decisão é observar e decidir depois. ([09:39] Larissa)
- **Adiada na reunião.** Avisar o cliente por e-mail quando o webhook falha repetidamente. Ficou para a próxima fase, depois de medir o impacto. ([09:37] Larissa)
- **Adiada na reunião.** Usar mais de um worker, particionando por pedido ou com lock pessimista. Hoje a ordem de entrega vale só por pedido e com um único worker. ([09:13] Diego)
- **Adiada na reunião.** Endurecer as permissões do CRUD de configuração, hoje liberado a qualquer papel autenticado. ([09:37] Sofia)
- **Adiada na reunião.** Arquivar as linhas entregues da outbox depois de cerca de 30 dias. ([09:08] Diego)
- **Lacuna identificada na análise.** O que vai no header de assinatura durante as 24 horas de rotação, quando duas secrets são válidas, e onde a secret anterior fica guardada. A reunião decidiu o prazo, mas não o formato. ([09:21] Sofia)
- **Lacuna identificada na análise.** Como a secret é guardada em repouso, já que o HMAC exige a chave recuperável e a configuração atual da aplicação não tem chave de cifra. A Sofia pediu para revisar a geração de secret antes do deploy. ([09:46] Sofia)
- **Lacuna identificada na análise.** O header com o instante do envio não faz parte da assinatura, que cobre só o corpo, então a detecção de replay pelo cliente fica fraca. ([09:44] Diego)
- **Lacuna identificada na análise.** A reunião exigiu só HTTPS e não tratou de endereços que apontam para a rede interna ou que redirecionam para outro destino. ([09:23] Sofia)
- **Lacuna identificada na análise.** Um evento em espera de nova tentativa pode ser ultrapassado pelo evento seguinte do mesmo pedido, o que reduz a garantia de ordem. ([09:13] Larissa)
- **Lacuna identificada na análise.** A criação de pedido gera evento? A reunião integrou apenas a mudança de status. ([09:40] Bruno)
- **Lacuna identificada na análise.** O que acontece com os eventos pendentes quando o webhook é removido e com a linha da DLQ depois do reprocessamento. ([09:18] Diego)
- **Lacuna identificada na análise.** Métricas e tracing não foram discutidos; a reunião decidiu apenas reaproveitar o log existente. ([09:30] Larissa)
- **Lacuna identificada na análise.** O que significa "5 tentativas": 5 retentativas depois do envio inicial, como as 5 esperas e as "quase 15 horas" indicam, ou 5 envios no total. ([09:17] Diego; [09:17] Larissa)
- **Lacuna identificada na análise.** O worker trata os eventos de um lote um por vez e cada chamada pode levar até 10 segundos, então um cliente lento atrasa os eventos seguintes e pode quebrar a meta de 10 segundos para eles. ([09:12] Diego; [09:42] Diego)
- **Lacuna identificada na análise.** Qual código de erro recebe uma URL sem HTTPS: o erro de validação do schema, como [09:23] Sofia descreveu, ou um código próprio do módulo, como [09:28] Bruno listou. ([09:23] Sofia; [09:28] Bruno)

---

### Impacto e riscos

**Impacto no sistema existente**

- A mudança de status de pedidos ganha uma chamada dentro da transação existente. Os endpoints atuais não mudam, e a resposta de sucesso dessa operação também não. Hipótese: um erro novo só ocorre se o conteúdo do evento passar de 64 KB, o que os campos definidos na reunião tornam improvável.
- Um novo processo precisa ser implantado e operado ao lado da API.
- O banco recebe novas tabelas por uma migration aditiva. Nenhuma infraestrutura nova é necessária. Hipótese: também nenhuma biblioteca nova, porque os recursos nativos do Node 20 bastam.
- O módulo novo reaproveita o tratamento de erros, o log e o controle de acesso existentes.

**Riscos**

- Cliente fora do ar por mais de 14,6 horas. Probabilidade média, impacto alto para o cliente, que fica sem eventos até o reprocessamento. Mitigação: histórico de entregas e DLQ com reprocessamento por administrador.
- Ordem dos eventos fora de sequência, com evento em nova tentativa ou com mais de um worker. Probabilidade média, impacto médio. Mitigação: um único worker e um evento que informa o status de origem e o de destino.
- Vazamento de secret. Probabilidade média, impacto alto. Mitigação: secret por endpoint, rotação com 24 horas de sobreposição e, como hipótese, secret fora de logs e de respostas de leitura.
- Prazo de 3 sprints com revisão de segurança de pelo menos 2 dias úteis no fim. Probabilidade média, impacto alto, porque a Atlas pode migrar. Mitigação: agendar a revisão da Sofia com antecedência.
- Cliente que não deduplica os eventos. Probabilidade alta, impacto médio. Mitigação: identificador de evento em todo envio e documentação destacada no portal do desenvolvedor.
- Cliente lento atrasando os eventos seguintes do mesmo lote. Probabilidade média, impacto médio. Mitigação: lote pequeno e limite de 10 segundos por chamada.

---

### Decisões relacionadas

- [ADR-001: Outbox no MySQL para publicar eventos de webhook](adrs/ADR-001-outbox-no-mysql.md)
- [ADR-002: Worker em processo separado com polling de 2 segundos](adrs/ADR-002-worker-separado-em-polling.md)
- [ADR-003: Retry com backoff exponencial e DLQ em tabela separada](adrs/ADR-003-retry-com-backoff-e-dlq.md)
- [ADR-004: Assinatura HMAC-SHA256 com secret por endpoint e rotação de 24 horas](adrs/ADR-004-hmac-sha256-secret-por-endpoint.md)
- [ADR-005: Entrega at-least-once com identificador de evento no header](adrs/ADR-005-entrega-at-least-once-com-x-event-id.md)
- [ADR-006: Reuso dos padrões existentes do projeto](adrs/ADR-006-reuso-dos-padroes-do-projeto.md)
- [ADR-007: Publicação do evento dentro da transação de mudança de status](adrs/ADR-007-publicacao-do-evento-na-transacao-do-change-status.md)
