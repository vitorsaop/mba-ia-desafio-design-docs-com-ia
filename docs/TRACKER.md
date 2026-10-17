# Tracker de Rastreabilidade

Este Tracker liga cada item dos documentos do pacote (PRD, RFC, FDD e ADRs) à sua origem. Fonte `TRANSCRICAO` indica uma fala de `TRANSCRICAO.md` e a Localização traz `[hh:mm] Nome`. Fonte `CODIGO` indica um arquivo do repositório e a Localização traz o caminho, com `:linha` quando o ponto é específico.

O Tipo `Hipótese` marca uma proposta que a reunião não decidiu: a Localização aponta a fala em que a lacuna nasceu. Prioridades dos requisitos, probabilidades e impactos dos riscos e tipos de teste são avaliação do autor; a Localização aponta a fala que originou o item. Os IDs seguem o padrão `DOCUMENTO-TIPO-NN`, por exemplo `PRD-FR-01`, `RFC-ALT-02`, `FDD-CONTRATO-03` e `ADR-002`.

| ID | Documento | Tipo | Conteúdo (resumo) | Fonte | Localização |
| --- | --- | --- | --- | --- | --- |
| PRD-OBJ-01 | docs/PRD.md | Objetivo | Notificar o cliente em tempo real: meta Menor que 10 segundos | TRANSCRICAO | [09:02] Marcos; [09:10] Larissa |
| PRD-OBJ-02 | docs/PRD.md | Objetivo | Nunca perder um evento: meta 0 mudanças sem evento | TRANSCRICAO | [09:40] Bruno |
| PRD-OBJ-03 | docs/PRD.md | Objetivo | Cobrir a indisponibilidade do cliente: meta Cerca de 14,6 horas, em 5 retentativas (Hipótese: depois do envio inicial) | TRANSCRICAO | [09:17] Diego |
| PRD-OBJ-04 | docs/PRD.md | Restrição | Entregar no prazo: meta 3 sprints, incluindo pelo menos 2 dias úteis de revisão de segurança | TRANSCRICAO | [09:46] Larissa; [09:46] Sofia |
| PRD-ESC-INC-01 | docs/PRD.md | Escopo | Cadastro, listagem, edição e remoção de webhooks, com a lista de status que cada webhook quer receber. | TRANSCRICAO | [09:31] Marcos; [09:33] Bruno |
| PRD-ESC-INC-02 | docs/PRD.md | Escopo | Registro do evento na mesma transação da mudança de status do pedido, com o conteúdo gravado no instante da mudança. | TRANSCRICAO | [09:40] Bruno; [09:52] Larissa |
| PRD-ESC-INC-03 | docs/PRD.md | Escopo | Envio por um processo separado da API, com assinatura HMAC-SHA256 e cinco headers. | TRANSCRICAO | [09:11] Diego; [09:20] Sofia; [09:44] Diego; [09:44] Sofia |
| PRD-ESC-INC-04 | docs/PRD.md | Escopo | Repetição da entrega com espera crescente, isolamento dos eventos que esgotam as tentativas e reprocessamento manual por administrador. | TRANSCRICAO | [09:17] Larissa; [09:18] Diego; [09:36] Larissa |
| PRD-ESC-INC-05 | docs/PRD.md | Escopo | Rotação de secret pela API, com a secret anterior válida por 24 horas. | TRANSCRICAO | [09:21] Sofia |
| PRD-ESC-INC-06 | docs/PRD.md | Escopo | Histórico de entregas por webhook. | TRANSCRICAO | [09:34] Marcos |
| PRD-ESC-FORA-01 | docs/PRD.md | Escopo | Aviso por e-mail ao cliente quando o webhook falha. Adiado para a próxima fase. | TRANSCRICAO | [09:37] Larissa |
| PRD-ESC-FORA-02 | docs/PRD.md | Escopo | Limitação da taxa de envio por cliente. A decisão é observar e decidir depois. | TRANSCRICAO | [09:39] Larissa |
| PRD-ESC-FORA-03 | docs/PRD.md | Escopo | Dashboard visual para o cliente. É projeto separado do time de frontend. | TRANSCRICAO | [09:40] Larissa |
| PRD-ESC-FORA-04 | docs/PRD.md | Escopo | Arquivamento das linhas entregues depois de cerca de 30 dias. | TRANSCRICAO | [09:08] Diego |
| PRD-ESC-FORA-05 | docs/PRD.md | Escopo | Mais de um worker e garantia de ordem global. | TRANSCRICAO | [09:13] Larissa; [09:13] Diego |
| PRD-ESC-FORA-06 | docs/PRD.md | Escopo | Webhook de entrada, em que o cliente enviaria eventos ao sistema. | TRANSCRICAO | [09:02] Marcos |
| PRD-ESC-FORA-07 | docs/PRD.md | Escopo | Endurecimento das permissões do cadastro de webhooks, adiado. | TRANSCRICAO | [09:37] Sofia |
| PRD-ESC-FORA-08 | docs/PRD.md | Escopo | Itens do pedido no conteúdo do evento. Descartado: o cliente consulta o pedido depois. | TRANSCRICAO | [09:43] Diego |
| PRD-ESC-FORA-09 | docs/PRD.md | Escopo | Entrega exatamente uma vez. Descartada: a garantia é ao menos uma vez. | TRANSCRICAO | [09:25] Diego |
| PRD-ESC-FORA-10 | docs/PRD.md | Escopo | Chamada ao cliente dentro da mudança de status do pedido. Descartada. | TRANSCRICAO | [09:04] Bruno; [09:06] Diego |
| PRD-FR-01 | docs/PRD.md | Requisito Funcional | Cadastrar webhook. O usuário que representa um cliente cadastra o endereço HTTPS que receberá as notificações, escolhe os status que quer... | TRANSCRICAO | [09:31] Marcos; [09:32] Larissa |
| PRD-FR-02 | docs/PRD.md | Requisito Funcional | Listar webhooks de um cliente. O usuário consulta os webhooks cadastrados de um cliente. | TRANSCRICAO | [09:33] Bruno |
| PRD-FR-03 | docs/PRD.md | Requisito Funcional | Editar webhook. O usuário altera o endereço, a lista de status ou a situação ativa de um webhook. | TRANSCRICAO | [09:33] Bruno; [09:21] Bruno |
| PRD-FR-04 | docs/PRD.md | Requisito Funcional | Remover webhook. O usuário remove um webhook que o cliente não quer mais. | TRANSCRICAO | [09:33] Bruno |
| PRD-FR-05 | docs/PRD.md | Requisito Funcional | Filtrar eventos por status. Cada webhook recebe somente os eventos dos status que escolheu. | TRANSCRICAO | [09:33] Marcos; [09:34] Bruno |
| PRD-FR-06 | docs/PRD.md | Requisito Funcional | Consultar o histórico de entregas. O cliente vê os envios feitos para um webhook, com sucesso ou falha, o conteúdo enviado, a resposta... | TRANSCRICAO | [09:34] Marcos |
| PRD-FR-07 | docs/PRD.md | Requisito Funcional | Rotacionar a secret. O cliente pede uma nova secret sem parar a integração. A secret anterior continua válida por 24 horas. | TRANSCRICAO | [09:21] Sofia |
| PRD-FR-08 | docs/PRD.md | Requisito Funcional | Registrar o evento na mudança de status. Quando o status de um pedido muda, o sistema registra o evento de notificação na mesma transação... | TRANSCRICAO | [09:40] Bruno; [09:41] Diego; [09:52] Larissa |
| PRD-FR-09 | docs/PRD.md | Requisito Funcional | Entregar o evento assinado ao cliente. Um processo separado da API envia cada evento ao endereço do cliente com assinatura e... | TRANSCRICAO | [09:09] Diego; [09:43] Diego; [09:44] Diego; [09:44] Sofia |
| PRD-FR-10 | docs/PRD.md | Requisito Funcional | Repetir a entrega com espera crescente. Quando o envio falha, o sistema tenta de novo com esperas de 1 minuto, 5 minutos, 30 minutos, 2... | TRANSCRICAO | [09:17] Larissa |
| PRD-FR-11 | docs/PRD.md | Requisito Funcional | Isolar eventos que esgotaram as tentativas. Eventos que falham em todas as tentativas vão para uma área separada, a DLQ, que guarda o... | TRANSCRICAO | [09:18] Diego |
| PRD-FR-12 | docs/PRD.md | Requisito Funcional | Reprocessar manualmente um evento isolado. Um administrador devolve um evento da DLQ para a fila de envio, e o sistema registra quem... | TRANSCRICAO | [09:18] Diego; [09:36] Sofia; [09:36] Larissa |
| PRD-RNF-01 | docs/PRD.md | Requisito Não Funcional | Performance: Notificar o cliente em menos de 10 segundos depois da mudança de status. | TRANSCRICAO | [09:02] Marcos; [09:10] Larissa |
| PRD-RNF-02 | docs/PRD.md | Requisito Não Funcional | Performance: Limite de 10 segundos por chamada ao endereço do cliente. | TRANSCRICAO | [09:42] Diego |
| PRD-RNF-03 | docs/PRD.md | Requisito Não Funcional | Performance: Conteúdo do evento de até 64 KB. Acima disso, erro. | TRANSCRICAO | [09:24] Larissa |
| PRD-RNF-04 | docs/PRD.md | Hipótese | Disponibilidade: Hipótese: a reunião não definiu meta de disponibilidade, e este documento não propõe um número. | TRANSCRICAO | [09:11] Diego |
| PRD-RNF-05 | docs/PRD.md | Requisito Não Funcional | Disponibilidade: O processo de envio roda separado da API, então reiniciar a API não interrompe os envios. | TRANSCRICAO | [09:11] Diego |
| PRD-RNF-06 | docs/PRD.md | Requisito Não Funcional | Disponibilidade: Um cliente fora do ar recebe novas tentativas por cerca de 14,6 horas antes de o evento ser isolado. | TRANSCRICAO | [09:17] Diego |
| PRD-RNF-07 | docs/PRD.md | Requisito Não Funcional | Segurança e autorização: Assinatura HMAC-SHA256 do corpo de cada envio, com secret única por endpoint e rotação com 24 horas de... | TRANSCRICAO | [09:22] Sofia |
| PRD-RNF-08 | docs/PRD.md | Requisito Não Funcional | Segurança e autorização: Endereço do webhook obrigatoriamente HTTPS. | TRANSCRICAO | [09:23] Sofia |
| PRD-RNF-09 | docs/PRD.md | Requisito Não Funcional | Segurança e autorização: Cadastro, listagem, edição e remoção abertos a qualquer papel autenticado, por enquanto. | TRANSCRICAO | [09:37] Sofia |
| PRD-RNF-10 | docs/PRD.md | Requisito Não Funcional | Segurança e autorização: Reprocessamento restrito ao papel ADMIN, com registro em log de quem executou. | TRANSCRICAO | [09:36] Sofia; [09:36] Larissa |
| PRD-RNF-11 | docs/PRD.md | Hipótese | Segurança e autorização: Hipótese: a secret não aparece em logs nem em respostas de leitura, porque a reunião mandou devolvê-la só na... | TRANSCRICAO | [09:31] Marcos; [09:22] Diego |
| PRD-RNF-12 | docs/PRD.md | Requisito Não Funcional | Segurança e autorização: Revisão de segurança de pelo menos 2 dias úteis antes do deploy. | TRANSCRICAO | [09:46] Sofia |
| PRD-RNF-13 | docs/PRD.md | Requisito Não Funcional | Observabilidade: Logs estruturados com o Pino, o logger já usado no projeto. | TRANSCRICAO | [09:29] Bruno |
| PRD-RNF-14 | docs/PRD.md | Requisito Não Funcional | Observabilidade: Histórico de entregas por webhook, com resultado, conteúdo, resposta e tempo de resposta. | TRANSCRICAO | [09:34] Marcos |
| PRD-RNF-15 | docs/PRD.md | Hipótese | Observabilidade: Hipótese: métricas e rastreamento não foram discutidos na reunião e ficam como logs estruturados e consultas ao banco, sem... | TRANSCRICAO | [09:29] Bruno; [09:30] Larissa |
| PRD-RNF-16 | docs/PRD.md | Requisito Não Funcional | Confiabilidade e integridade de dados: O evento e a mudança de status são confirmados ou desfeitos juntos. | TRANSCRICAO | [09:40] Bruno |
| PRD-RNF-17 | docs/PRD.md | Requisito Não Funcional | Confiabilidade e integridade de dados: Entrega ao menos uma vez, com identificador único por evento. | TRANSCRICAO | [09:25] Diego |
| PRD-RNF-18 | docs/PRD.md | Requisito Não Funcional | Confiabilidade e integridade de dados: Ordem de entrega garantida por pedido enquanto houver um único processo de envio, sem garantia de... | TRANSCRICAO | [09:12] Diego; [09:13] Larissa |
| PRD-RNF-19 | docs/PRD.md | Requisito Não Funcional | Confiabilidade e integridade de dados: O conteúdo do evento é um retrato do pedido no instante da mudança. | TRANSCRICAO | [09:52] Larissa |
| PRD-RNF-20 | docs/PRD.md | Requisito Não Funcional | Compatibilidade e portabilidade: Reuso do MySQL, do Prisma, do Pino, do tratamento de erros, dos esquemas de validação e dos... | TRANSCRICAO | [09:30] Larissa |
| PRD-RNF-21 | docs/PRD.md | Requisito Não Funcional | Compatibilidade e portabilidade: API REST JSON versionada em /api/v1, com códigos de erro de prefixo WEBHOOK_. | TRANSCRICAO | [09:29] Larissa |
| PRD-RNF-22 | docs/PRD.md | Requisito Não Funcional | Compatibilidade e portabilidade: Nenhuma infraestrutura nova. | TRANSCRICAO | [09:07] Diego; [09:30] Larissa |
| PRD-RNF-23 | docs/PRD.md | Requisito Não Funcional | Compliance: Auditoria do reprocessamento por log com o usuário que executou. A reunião não discutiu requisito regulatório. | TRANSCRICAO | [09:36] Sofia |
| PRD-RNF-24 | docs/PRD.md | Requisito Não Funcional | Acessibilidade no frontend consumidor: Não se aplica nesta fase: não há frontend, apenas endpoints, porque o painel visual é projeto... | TRANSCRICAO | [09:40] Larissa |
| PRD-DEC-01 | docs/PRD.md | Decisão | Decisão: Outbox no MySQL gravada na mesma transação da mudança de status | TRANSCRICAO | [09:08] Larissa; [09:40] Bruno |
| PRD-DEC-02 | docs/PRD.md | Decisão | Decisão: Processo de envio separado da API, com consulta a cada 2 segundos | TRANSCRICAO | [09:10] Larissa; [09:11] Diego |
| PRD-DEC-03 | docs/PRD.md | Decisão | Decisão: Cinco retentativas com espera crescente e DLQ em tabela separada | TRANSCRICAO | [09:17] Larissa; [09:18] Diego |
| PRD-DEC-04 | docs/PRD.md | Decisão | Decisão: Assinatura HMAC-SHA256 com secret por endpoint e rotação de 24 horas | TRANSCRICAO | [09:22] Sofia |
| PRD-DEC-05 | docs/PRD.md | Decisão | Decisão: Entrega ao menos uma vez com identificador de evento | TRANSCRICAO | [09:26] Larissa |
| PRD-DEC-06 | docs/PRD.md | Decisão | Decisão: Reuso dos padrões existentes do projeto | TRANSCRICAO | [09:30] Larissa |
| PRD-DEC-07 | docs/PRD.md | Decisão | Decisão: Função de publicação que recebe a transação corrente | TRANSCRICAO | [09:41] Bruno; [09:41] Diego |
| PRD-DEP-01 | docs/PRD.md | Dependência | organizacional: Revisão de segurança antes do deploy | TRANSCRICAO | [09:46] Sofia |
| PRD-DEP-02 | docs/PRD.md | Dependência | organizacional: Documentação no portal do desenvolvedor | TRANSCRICAO | [09:26] Marcos; [09:40] Marcos |
| PRD-DEP-03 | docs/PRD.md | Dependência | organizacional: Confirmação do prazo com a Atlas | TRANSCRICAO | [09:47] Marcos |
| PRD-DEP-04 | docs/PRD.md | Dependência | técnica: MySQL, Prisma e uma nova migration | CODIGO | prisma/schema.prisma:5 |
| PRD-DEP-05 | docs/PRD.md | Dependência | técnica: Usuários do sistema que representam clientes | TRANSCRICAO | [09:32] Marcos |
| PRD-DEP-06 | docs/PRD.md | Dependência | externa: Endereços HTTPS dos clientes | TRANSCRICAO | [09:23] Sofia |
| PRD-RISCO-01 | docs/PRD.md | Risco | Cliente fora do ar por mais de 14,6 horas fica sem eventos | TRANSCRICAO | [09:17] Marcos; [09:37] Larissa |
| PRD-RISCO-02 | docs/PRD.md | Risco | Ordem dos eventos fora de sequência | TRANSCRICAO | [09:12] Diego; [09:13] Larissa |
| PRD-RISCO-03 | docs/PRD.md | Risco | Vazamento de secret | TRANSCRICAO | [09:22] Diego |
| PRD-RISCO-04 | docs/PRD.md | Risco | Prazo de 3 sprints pode não ser cumprido | TRANSCRICAO | [09:00] Marcos; [09:46] Larissa |
| PRD-RISCO-05 | docs/PRD.md | Risco | Cliente que não deduplica processa o mesmo pedido duas vezes | TRANSCRICAO | [09:25] Sofia; [09:26] Marcos |
| PRD-RISCO-06 | docs/PRD.md | Risco | Qualquer usuário autenticado acessa os webhooks de qualquer cliente | TRANSCRICAO | [09:37] Sofia |
| PRD-RISCO-07 | docs/PRD.md | Risco | Cliente lento atrasa os eventos seguintes do mesmo lote | TRANSCRICAO | [09:12] Diego; [09:42] Diego |
| PRD-CA-01 | docs/PRD.md | Critério de Aceite | Quando um pedido muda de status e o cliente tem webhook ativo que assina aquele status, existe um evento registrado na mesma transação; se... | TRANSCRICAO | [09:40] Bruno; [09:41] Diego |
| PRD-CA-02 | docs/PRD.md | Critério de Aceite | Com o processo de envio em execução e o cliente respondendo com sucesso, o primeiro envio ocorre em menos de 10 segundos depois do registro... | TRANSCRICAO | [09:02] Marcos |
| PRD-CA-03 | docs/PRD.md | Critério de Aceite | Falha ou ausência de resposta em 10 segundos agenda nova tentativa com esperas de 1 minuto, 5 minutos, 30 minutos, 2 horas e 12 horas. | TRANSCRICAO | [09:17] Larissa; [09:42] Diego |
| PRD-CA-04 | docs/PRD.md | Critério de Aceite | Depois da última retentativa com falha, o evento está na DLQ com conteúdo, motivo e data, e não está mais na fila ativa. | TRANSCRICAO | [09:18] Diego |
| PRD-CA-05 | docs/PRD.md | Critério de Aceite | Todo envio traz o identificador do evento, a assinatura, o instante do envio, o identificador do webhook e o tipo do conteúdo. | TRANSCRICAO | [09:44] Diego; [09:44] Sofia |
| PRD-CA-06 | docs/PRD.md | Critério de Aceite | A assinatura confere com o HMAC-SHA256 do corpo calculado com a secret do endpoint. | TRANSCRICAO | [09:22] Sofia |
| PRD-CA-07 | docs/PRD.md | Critério de Aceite | A rotação de secret mantém a secret anterior válida por 24 horas. | TRANSCRICAO | [09:21] Sofia |
| PRD-CA-08 | docs/PRD.md | Critério de Aceite | Endereço sem HTTPS é recusado e conteúdo de evento acima de 64 KB gera erro. | TRANSCRICAO | [09:23] Sofia; [09:24] Larissa |
| PRD-CA-09 | docs/PRD.md | Critério de Aceite | O reprocessamento por ADMIN recoloca o evento como pendente e registra em log o usuário; um usuário OPERATOR recebe acesso negado. | TRANSCRICAO | [09:36] Sofia; [09:36] Larissa |
| PRD-CA-10 | docs/PRD.md | Critério de Aceite | O histórico de entregas devolve até 100 envios por página, com resultado, conteúdo, resposta e tempo de resposta. | TRANSCRICAO | [09:34] Marcos |
| PRD-CA-11 | docs/PRD.md | Critério de Aceite | A mudança de status de um pedido de cliente sem webhook funciona como antes. | TRANSCRICAO | [09:34] Bruno |
| PRD-TESTE-01 | docs/PRD.md | Teste | Testes unitários para a assinatura HMAC, a tabela de esperas, o filtro de status e a montagem do conteúdo do evento. | CODIGO | package.json:52 |
| PRD-TESTE-02 | docs/PRD.md | Teste | Testes de integração com Vitest e supertest sobre o MySQL: atomicidade da mudança de status, cadastro e consulta de webhooks, e papel ADMIN... | CODIGO | tests/helpers/factories.ts:76 |
| PRD-TESTE-03 | docs/PRD.md | Teste | Testes do processo de envio contra um servidor HTTP simulado: sucesso, timeout de 10 segundos, nova tentativa e envio para a DLQ. | TRANSCRICAO | [09:17] Larissa; [09:42] Diego |
| PRD-TESTE-04 | docs/PRD.md | Teste | Testes de segurança: acesso negado ao OPERATOR no reprocessamento, secret ausente nas leituras e secret ausente nos logs. | TRANSCRICAO | [09:36] Sofia; [09:22] Diego |
| PRD-TESTE-05 | docs/PRD.md | Teste | Suíte automatizada no padrão atual de tests/, executada a cada alteração. | CODIGO | tests/setup.ts:8 |
| PRD-TESTE-06 | docs/PRD.md | Teste | Revisão de segurança de pelo menos 2 dias úteis antes do deploy, com foco na assinatura HMAC e na geração de secret. | TRANSCRICAO | [09:46] Sofia |
| PRD-TESTE-07 | docs/PRD.md | Teste | Roteiro manual com um cliente simulado para medir o limite de 10 segundos de ponta a ponta. | TRANSCRICAO | [09:02] Marcos |
| RFC-PROP-01 | docs/RFC.md | Proposta | Registro atômico do evento. A mudança de status grava o evento na outbox, na mesma transação, com o conteúdo já renderizado e somente para... | TRANSCRICAO | [09:08] Larissa; [09:40] Bruno |
| RFC-PROP-02 | docs/RFC.md | Proposta | Envio por um worker separado. Um processo próprio consulta a outbox a cada 2 segundos, com um único worker, e envia cada evento ao cliente... | TRANSCRICAO | [09:10] Larissa; [09:11] Diego; [09:42] Diego |
| RFC-PROP-03 | docs/RFC.md | Proposta | Repetição e isolamento de falhas. Falha ou timeout agenda nova tentativa depois de 1 minuto, 5 minutos, 30 minutos, 2 horas e 12 horas, o... | TRANSCRICAO | [09:17] Larissa; [09:18] Diego |
| RFC-PROP-04 | docs/RFC.md | Proposta | Assinatura por endpoint. Cada envio leva uma assinatura HMAC-SHA256 do corpo, com uma secret única por endpoint, que o cliente pode... | TRANSCRICAO | [09:22] Sofia |
| RFC-PROP-05 | docs/RFC.md | Proposta | Entrega at-least-once. Cada evento leva um identificador único para o cliente deduplicar repetições. Ver ADR-005. | TRANSCRICAO | [09:26] Larissa |
| RFC-PROP-06 | docs/RFC.md | Proposta | API de configuração e histórico. Cadastro, listagem, edição e remoção de webhooks, escolha dos status que cada webhook quer receber,... | TRANSCRICAO | [09:30] Larissa; [09:36] Larissa |
| RFC-ALT-01 | docs/RFC.md | Alternativa | Alternativa: chamada HTTP síncrona no serviço de pedidos. O serviço de pedidos chamaria o cliente dentro da transação de mudança de status. | TRANSCRICAO | [09:04] Bruno; [09:06] Diego |
| RFC-ALT-02 | docs/RFC.md | Alternativa | Alternativa: Redis Streams ou outra fila externa. A entrega sairia do banco para uma fila dedicada. | TRANSCRICAO | [09:07] Larissa; [09:07] Diego |
| RFC-ALT-03 | docs/RFC.md | Alternativa | Alternativa: gatilho do banco para avisar o worker. O banco avisaria o processo de envio quando houvesse evento novo. | TRANSCRICAO | [09:09] Bruno; [09:09] Diego |
| RFC-ALT-04 | docs/RFC.md | Alternativa | Alternativa: outro número de tentativas, com retry indefinido ou apenas 3 tentativas. | TRANSCRICAO | [09:15] Diego; [09:16] Bruno; [09:16] Diego |
| RFC-ALT-05 | docs/RFC.md | Alternativa | Alternativa: entrega exatamente uma vez (exactly-once). | TRANSCRICAO | [09:25] Diego |
| RFC-ALT-06 | docs/RFC.md | Alternativa | Alternativa: worker dentro do processo da API. Trade-off do descarte: dispensaria um processo adicional, mas reiniciar a API perderia o... | TRANSCRICAO | [09:11] Diego |
| RFC-QA-01 | docs/RFC.md | Questão em Aberto | Adiada na reunião. Limitar a taxa de envio por cliente: se um cliente tiver 50 pedidos mudando de status em um minuto, ele recebe 50... | TRANSCRICAO | [09:38] Diego; [09:39] Larissa |
| RFC-QA-02 | docs/RFC.md | Questão em Aberto | Adiada na reunião. Avisar o cliente por e-mail quando o webhook falha repetidamente. Ficou para a próxima fase, depois de medir o impacto. | TRANSCRICAO | [09:37] Larissa |
| RFC-QA-03 | docs/RFC.md | Questão em Aberto | Adiada na reunião. Usar mais de um worker, particionando por pedido ou com lock pessimista. | TRANSCRICAO | [09:13] Diego |
| RFC-QA-04 | docs/RFC.md | Questão em Aberto | Adiada na reunião. Endurecer as permissões do CRUD de configuração, hoje liberado a qualquer papel autenticado. ([09:37] Sofia) | TRANSCRICAO | [09:37] Sofia |
| RFC-QA-05 | docs/RFC.md | Questão em Aberto | Adiada na reunião. Arquivar as linhas entregues da outbox depois de cerca de 30 dias. ([09:08] Diego) | TRANSCRICAO | [09:08] Diego |
| RFC-QA-06 | docs/RFC.md | Questão em Aberto | Lacuna identificada na análise. O que vai no header de assinatura durante as 24 horas de rotação, quando duas secrets são válidas, e onde a... | TRANSCRICAO | [09:21] Sofia |
| RFC-QA-07 | docs/RFC.md | Questão em Aberto | Lacuna identificada na análise. Como a secret é guardada em repouso, já que o HMAC exige a chave recuperável e a configuração atual da... | TRANSCRICAO | [09:46] Sofia |
| RFC-QA-08 | docs/RFC.md | Questão em Aberto | Lacuna identificada na análise. O header com o instante do envio não faz parte da assinatura, que cobre só o corpo, então a detecção de... | TRANSCRICAO | [09:44] Diego |
| RFC-QA-09 | docs/RFC.md | Questão em Aberto | Lacuna identificada na análise. A reunião exigiu só HTTPS e não tratou de endereços que apontam para a rede interna ou que redirecionam... | TRANSCRICAO | [09:23] Sofia |
| RFC-QA-10 | docs/RFC.md | Questão em Aberto | Lacuna identificada na análise. Um evento em espera de nova tentativa pode ser ultrapassado pelo evento seguinte do mesmo pedido, o que... | TRANSCRICAO | [09:13] Larissa |
| RFC-QA-11 | docs/RFC.md | Questão em Aberto | Lacuna identificada na análise. A criação de pedido gera evento? A reunião integrou apenas a mudança de status. ([09:40] Bruno) | TRANSCRICAO | [09:40] Bruno |
| RFC-QA-12 | docs/RFC.md | Questão em Aberto | Lacuna identificada na análise. O que acontece com os eventos pendentes quando o webhook é removido e com a linha da DLQ depois do... | TRANSCRICAO | [09:18] Diego |
| RFC-QA-13 | docs/RFC.md | Questão em Aberto | Lacuna identificada na análise. Métricas e tracing não foram discutidos; a reunião decidiu apenas reaproveitar o log existente. | TRANSCRICAO | [09:30] Larissa |
| RFC-QA-14 | docs/RFC.md | Questão em Aberto | Lacuna identificada na análise. O que significa "5 tentativas": 5 retentativas depois do envio inicial, como as 5 esperas e as "quase 15... | TRANSCRICAO | [09:17] Diego; [09:17] Larissa |
| RFC-QA-15 | docs/RFC.md | Questão em Aberto | Lacuna identificada na análise. O worker trata os eventos de um lote um por vez e cada chamada pode levar até 10 segundos, então um cliente... | TRANSCRICAO | [09:12] Diego; [09:42] Diego |
| RFC-QA-16 | docs/RFC.md | Questão em Aberto | Lacuna identificada na análise. Qual código de erro recebe uma URL sem HTTPS: o erro de validação do schema, como [09:23] Sofia descreveu,... | TRANSCRICAO | [09:23] Sofia; [09:28] Bruno |
| RFC-IMP-01 | docs/RFC.md | Impacto | A mudança de status de pedidos ganha uma chamada dentro da transação existente. | CODIGO | src/modules/orders/order.service.ts:131 |
| RFC-IMP-02 | docs/RFC.md | Impacto | Um novo processo precisa ser implantado e operado ao lado da API. | TRANSCRICAO | [09:11] Diego |
| RFC-IMP-03 | docs/RFC.md | Impacto | O banco recebe novas tabelas por uma migration aditiva. Nenhuma infraestrutura nova é necessária. | CODIGO | prisma/migrations/20260519182739_init/migration.sql |
| RFC-IMP-04 | docs/RFC.md | Impacto | O módulo novo reaproveita o tratamento de erros, o log e o controle de acesso existentes. | TRANSCRICAO | [09:30] Larissa |
| RFC-RISCO-01 | docs/RFC.md | Risco | Cliente fora do ar por mais de 14,6 horas. Probabilidade média, impacto alto para o cliente, que fica sem eventos até o reprocessamento. | TRANSCRICAO | [09:17] Marcos |
| RFC-RISCO-02 | docs/RFC.md | Risco | Ordem dos eventos fora de sequência, com evento em nova tentativa ou com mais de um worker. Probabilidade média, impacto médio. | TRANSCRICAO | [09:12] Diego |
| RFC-RISCO-03 | docs/RFC.md | Risco | Vazamento de secret. Probabilidade média, impacto alto. | TRANSCRICAO | [09:22] Diego |
| RFC-RISCO-04 | docs/RFC.md | Risco | Prazo de 3 sprints com revisão de segurança de pelo menos 2 dias úteis no fim. | TRANSCRICAO | [09:46] Sofia; [09:00] Marcos |
| RFC-RISCO-05 | docs/RFC.md | Risco | Cliente que não deduplica os eventos. Probabilidade alta, impacto médio. | TRANSCRICAO | [09:25] Sofia |
| RFC-RISCO-06 | docs/RFC.md | Risco | Cliente lento atrasando os eventos seguintes do mesmo lote. Probabilidade média, impacto médio. | TRANSCRICAO | [09:12] Diego; [09:42] Diego |
| RFC-ADR-01 | docs/RFC.md | Decisão | ADR-001: Outbox no MySQL para publicar eventos de webhook | TRANSCRICAO | [09:08] Larissa |
| RFC-ADR-02 | docs/RFC.md | Decisão | ADR-002: Worker em processo separado com polling de 2 segundos | TRANSCRICAO | [09:10] Larissa |
| RFC-ADR-03 | docs/RFC.md | Decisão | ADR-003: Retry com backoff exponencial e DLQ em tabela separada | TRANSCRICAO | [09:17] Larissa |
| RFC-ADR-04 | docs/RFC.md | Decisão | ADR-004: Assinatura HMAC-SHA256 com secret por endpoint e rotação de 24 horas | TRANSCRICAO | [09:22] Sofia |
| RFC-ADR-05 | docs/RFC.md | Decisão | ADR-005: Entrega at-least-once com identificador de evento no header | TRANSCRICAO | [09:26] Larissa |
| RFC-ADR-06 | docs/RFC.md | Decisão | ADR-006: Reuso dos padrões existentes do projeto | TRANSCRICAO | [09:30] Larissa |
| RFC-ADR-07 | docs/RFC.md | Decisão | ADR-007: Publicação do evento dentro da transação de mudança de status | TRANSCRICAO | [09:41] Bruno |
| FDD-OBJ-01 | docs/FDD.md | Objetivo | Registrar o evento na mesma transação do changeStatus. | TRANSCRICAO | [09:40] Bruno |
| FDD-OBJ-02 | docs/FDD.md | Objetivo | Iniciar o primeiro envio em menos de 10 segundos depois do registro do evento. | TRANSCRICAO | [09:02] Marcos; [09:09] Diego |
| FDD-OBJ-03 | docs/FDD.md | Objetivo | Limitar cada chamada HTTP ao cliente a 10 segundos. | TRANSCRICAO | [09:42] Diego |
| FDD-OBJ-04 | docs/FDD.md | Objetivo | Repetir falhas com esperas de 60, 300, 1.800, 7.200 e 43.200 segundos e mover o evento para a DLQ depois da 5ª retentativa. | TRANSCRICAO | [09:17] Diego |
| FDD-OBJ-05 | docs/FDD.md | Objetivo | Assinar o corpo com HMAC-SHA256 usando uma secret única por endpoint, com rotação que mantém a secret anterior válida por 24 horas. | TRANSCRICAO | [09:22] Sofia |
| FDD-OBJ-06 | docs/FDD.md | Objetivo | Garantir entrega at-least-once com o header X-Event-Id estável entre as tentativas do mesmo evento. | TRANSCRICAO | [09:25] Diego |
| FDD-OBJ-07 | docs/FDD.md | Objetivo | Recusar URL que não seja https e payload acima de 64 KB. | TRANSCRICAO | [09:23] Sofia; [09:24] Larissa |
| FDD-OBJ-08 | docs/FDD.md | Objetivo | Reaproveitar AppError, o error middleware, o Pino e requireRole sem alterá-los, com a única exceção da lista de redação do log. | TRANSCRICAO | [09:30] Larissa |
| FDD-OBJ-09 | docs/FDD.md | Hipótese | Hipótese: não acrescentar nenhuma dependência npm, porque fetch, AbortSignal.timeout e crypto do Node 20 bastam. | TRANSCRICAO | [09:30] Larissa |
| FDD-ESC-INC-01 | docs/FDD.md | Escopo | Módulo webhooks na API: cadastro, listagem, edição e remoção de webhooks, filtro de status por webhook, rotação de secret e histórico de... | TRANSCRICAO | [09:31] Marcos; [09:33] Bruno |
| FDD-ESC-INC-02 | docs/FDD.md | Escopo | Outbox gravada na transação do changeStatus, com o conteúdo do evento já renderizado. | TRANSCRICAO | [09:40] Bruno |
| FDD-ESC-INC-03 | docs/FDD.md | Escopo | Worker em processo separado com polling de 2 segundos, timeout de 10 segundos, assinatura HMAC-SHA256 e headers de identificação. | TRANSCRICAO | [09:09] Diego; [09:42] Diego; [09:44] Diego |
| FDD-ESC-INC-04 | docs/FDD.md | Escopo | Retry com backoff, DLQ em tabela separada e reprocessamento manual por ADMIN com log de quem executou. | TRANSCRICAO | [09:17] Larissa; [09:18] Diego; [09:36] Larissa |
| FDD-ESC-INC-05 | docs/FDD.md | Escopo | Matriz de erros WEBHOOK_*, logs estruturados com Pino e testes automatizados no padrão de tests/. | TRANSCRICAO | [09:28] Bruno; [09:29] Bruno |
| FDD-ESC-EXC-01 | docs/FDD.md | Escopo | Aviso por e-mail ao cliente quando o webhook falha (adiado para a próxima fase). | TRANSCRICAO | [09:37] Larissa |
| FDD-ESC-EXC-02 | docs/FDD.md | Escopo | Limitação da taxa de envio por cliente (a decisão é observar e decidir depois). | TRANSCRICAO | [09:39] Larissa |
| FDD-ESC-EXC-03 | docs/FDD.md | Escopo | Dashboard visual para o cliente (projeto do time de frontend). | TRANSCRICAO | [09:40] Larissa |
| FDD-ESC-EXC-04 | docs/FDD.md | Escopo | Arquivamento das linhas entregues depois de cerca de 30 dias. | TRANSCRICAO | [09:08] Diego |
| FDD-ESC-EXC-05 | docs/FDD.md | Escopo | Mais de um worker, particionamento por pedido e lock pessimista. | TRANSCRICAO | [09:13] Diego |
| FDD-ESC-EXC-06 | docs/FDD.md | Escopo | Webhook de entrada, em que o cliente enviaria eventos ao sistema. | TRANSCRICAO | [09:02] Marcos |
| FDD-ESC-EXC-07 | docs/FDD.md | Escopo | Endurecimento das permissões do CRUD de configuração e isolamento por customer. | TRANSCRICAO | [09:37] Sofia; [09:32] Larissa |
| FDD-ESC-EXC-08 | docs/FDD.md | Escopo | Evento na criação de pedido: a reunião integrou só a mudança de status (confirmação pendente com o PM). | TRANSCRICAO | [09:40] Bruno |
| FDD-ESC-EXC-09 | docs/FDD.md | Hipótese | Circuit breaker. | TRANSCRICAO | [09:15] Diego |
| FDD-FLUXO-01 | docs/FDD.md | Fluxo | Criação do evento na outbox. Dentro de changeStatus, depois de gravar o histórico e antes de reler o pedido, o código chama... | TRANSCRICAO | [09:40] Bruno; [09:41] Bruno |
| FDD-FLUXO-02 | docs/FDD.md | Fluxo | Processamento pelo worker. A cada 2 segundos o worker executa um ciclo. | TRANSCRICAO | [09:08] Diego; [09:09] Diego |
| FDD-FLUXO-03 | docs/FDD.md | Fluxo | Retry. Em falha, o worker grava a tentativa e soma 1 em attempts. | TRANSCRICAO | [09:17] Diego |
| FDD-FLUXO-04 | docs/FDD.md | Fluxo | DLQ. Quando a 5ª retentativa falha, uma transação insere a linha em webhook_dead_letter com o payload, o motivo da falha e a data, e apaga... | TRANSCRICAO | [09:18] Diego |
| FDD-FLUXO-05 | docs/FDD.md | Fluxo | Replay. O ADMIN chama o endpoint de replay. | TRANSCRICAO | [09:18] Diego; [09:36] Sofia |
| FDD-FLUXO-06 | docs/FDD.md | Hipótese | Worker reiniciado. Hipótese: ao iniciar, o worker devolve a PENDING as linhas em PROCESSING. | TRANSCRICAO | [09:11] Diego |
| FDD-FLUXO-07 | docs/FDD.md | Hipótese | Webhook removido ou inativo no momento do envio. Hipótese: o worker descarta o evento e registra webhook_event_discarded, sem enviar. | TRANSCRICAO | [09:33] Bruno |
| FDD-FLUXO-08 | docs/FDD.md | Hipótese | Payload acima de 64 KB. Hipótese: a função de publicação lança WEBHOOK_PAYLOAD_TOO_LARGE, o changeStatus falha com 422 e a mudança de... | TRANSCRICAO | [09:24] Larissa; [09:40] Bruno |
| FDD-FLUXO-09 | docs/FDD.md | Fluxo | Encerramento. Ao receber SIGTERM ou SIGINT, o worker termina o lote em andamento, desconecta o Prisma e sai. | CODIGO | src/server.ts:13 |
| FDD-CONTRATO-01 | docs/FDD.md | Contrato | Cadastrar webhook | TRANSCRICAO | [09:31] Marcos |
| FDD-CONTRATO-02 | docs/FDD.md | Contrato | Listar webhooks de um customer | TRANSCRICAO | [09:33] Bruno |
| FDD-CONTRATO-03 | docs/FDD.md | Contrato | Editar webhook | TRANSCRICAO | [09:33] Bruno |
| FDD-CONTRATO-04 | docs/FDD.md | Contrato | Remover webhook | TRANSCRICAO | [09:33] Bruno |
| FDD-CONTRATO-05 | docs/FDD.md | Contrato | Rotacionar a secret | TRANSCRICAO | [09:21] Sofia |
| FDD-CONTRATO-06 | docs/FDD.md | Contrato | Consultar o histórico de entregas | TRANSCRICAO | [09:34] Marcos |
| FDD-CONTRATO-07 | docs/FDD.md | Contrato | Reprocessar evento da DLQ | TRANSCRICAO | [09:18] Diego |
| FDD-CONTRATO-08 | docs/FDD.md | Contrato | Entrega do evento ao endpoint do cliente | TRANSCRICAO | [09:43] Diego; [09:44] Diego; [09:44] Sofia |
| FDD-CONTRATO-09 | docs/FDD.md | Contrato | Publicação do evento dentro da transação | TRANSCRICAO | [09:41] Bruno |
| FDD-ERRO-01 | docs/FDD.md | Erro | WEBHOOK_NOT_FOUND: Webhook inexistente | TRANSCRICAO | [09:28] Bruno |
| FDD-ERRO-02 | docs/FDD.md | Hipótese | WEBHOOK_INVALID_URL: URL malformada ou diferente de https | TRANSCRICAO | [09:23] Sofia; [09:28] Bruno |
| FDD-ERRO-03 | docs/FDD.md | Hipótese | WEBHOOK_SECRET_REQUIRED: Hipótese: webhook sem secret ativa no momento do envio | TRANSCRICAO | [09:28] Bruno |
| FDD-ERRO-04 | docs/FDD.md | Hipótese | WEBHOOK_PAYLOAD_TOO_LARGE: Payload acima de 64 KB na gravação do evento | TRANSCRICAO | [09:24] Larissa |
| FDD-ERRO-05 | docs/FDD.md | Erro | WEBHOOK_DEAD_LETTER_NOT_FOUND: Replay de linha da DLQ inexistente | TRANSCRICAO | [09:18] Diego |
| FDD-ERRO-06 | docs/FDD.md | Hipótese | WEBHOOK_ALREADY_REPLAYED: Hipótese: replay de linha da DLQ já reprocessada | TRANSCRICAO | [09:18] Diego |
| FDD-ERRO-07 | docs/FDD.md | Erro | WEBHOOK_DELIVERY_TIMEOUT: O cliente não respondeu em 10 segundos | TRANSCRICAO | [09:42] Diego |
| FDD-ERRO-08 | docs/FDD.md | Erro | WEBHOOK_DELIVERY_FAILED: Resposta fora de 200 a 299 ou erro de conexão | TRANSCRICAO | [09:15] Diego |
| FDD-ERRO-09 | docs/FDD.md | Erro | WEBHOOK_RETRIES_EXHAUSTED: A última retentativa falhou | TRANSCRICAO | [09:17] Larissa; [09:18] Diego |
| FDD-RES-01 | docs/FDD.md | Resiliência | Timeout: 10 segundos por chamada HTTP, com AbortSignal.timeout(10000) do Node 20. O estouro gera WEBHOOK_DELIVERY_TIMEOUT. | TRANSCRICAO | [09:42] Diego |
| FDD-RES-02 | docs/FDD.md | Hipótese | Retries: Hipótese de interpretação, 5 retentativas depois do envio inicial, no máximo 6 requisições por ciclo de entrega. | TRANSCRICAO | [09:17] Larissa |
| FDD-RES-03 | docs/FDD.md | Resiliência | Backoff: 60, 300, 1.800, 7.200 e 43.200 segundos, contados a partir da falha anterior. A soma é de 876 minutos, cerca de 14,6 horas. | TRANSCRICAO | [09:17] Diego |
| FDD-RES-04 | docs/FDD.md | Resiliência | Fallback: depois da 5ª retentativa o evento vai para a DLQ e só volta por reprocessamento manual de ADMIN. | TRANSCRICAO | [09:18] Diego |
| FDD-RES-05 | docs/FDD.md | Hipótese | Circuit breaker: não previsto nesta fase, porque a reunião não o discutiu. | TRANSCRICAO | [09:15] Diego |
| FDD-RES-06 | docs/FDD.md | Hipótese | Hipótese: o worker não segue redirecionamentos HTTP, para que um endereço cadastrado não leve o servidor a outro destino. | TRANSCRICAO | [09:23] Sofia |
| FDD-RES-07 | docs/FDD.md | Resiliência | Encerramento ordenado: ao receber SIGTERM ou SIGINT, o worker termina o lote em andamento antes de sair, o que o shutdown de src/server.ts... | CODIGO | src/server.ts:13 |
| FDD-RES-08 | docs/FDD.md | Resiliência | Falha permanente: o evento fica na DLQ com payload, motivo e data, como evidência para depuração e reprocessamento. | TRANSCRICAO | [09:18] Diego |
| FDD-RES-09 | docs/FDD.md | Resiliência | Aviso ao cliente: o e-mail ficou fora desta fase, então o cliente não é notificado da falha. O caminho disponível é o histórico de entregas. | TRANSCRICAO | [09:37] Larissa |
| FDD-RES-10 | docs/FDD.md | Hipótese | Hipótese: webhook removido ou inativo no envio descarta o evento com o log webhook_event_discarded. | TRANSCRICAO | [09:33] Bruno |
| FDD-INV-01 | docs/FDD.md | Invariante | Não existe status confirmado sem evento para webhook ativo que assina o status, nem evento sem status confirmado. | TRANSCRICAO | [09:40] Bruno |
| FDD-INV-02 | docs/FDD.md | Invariante | O event_id é único, nasce na gravação da outbox e é o mesmo em todas as tentativas e no replay. | TRANSCRICAO | [09:25] Diego |
| FDD-INV-03 | docs/FDD.md | Invariante | A ordem de entrega vale por order_id e só com um único worker. | TRANSCRICAO | [09:13] Larissa |
| FDD-INV-04 | docs/FDD.md | Hipótese | Hipótese: a secret nunca aparece em logs nem em leituras, e só as respostas de criação e de rotação a devolvem. | TRANSCRICAO | [09:22] Diego; [09:31] Marcos |
| FDD-INV-05 | docs/FDD.md | Hipótese | Hipótese: nenhuma linha da DLQ é apagada, porque a reunião a descreve como evidência para depuração e reprocessamento. | TRANSCRICAO | [09:18] Diego |
| FDD-OBS-01 | docs/FDD.md | Hipótese | Métricas: Hipótese: a reunião não discutiu métricas e o projeto não tem biblioteca de métricas, então elas saem como logs estruturados do... | TRANSCRICAO | [09:29] Bruno; [09:30] Larissa |
| FDD-OBS-02 | docs/FDD.md | Hipótese | Métricas: Linhas da outbox por situação (PENDING, PROCESSING, FAILED, DELIVERED), emitidas a cada ciclo do worker. | TRANSCRICAO | [09:29] Bruno |
| FDD-OBS-03 | docs/FDD.md | Hipótese | Métricas: Idade da linha PENDING mais antiga, que mede o objetivo de menos de 10 segundos. | TRANSCRICAO | [09:02] Marcos |
| FDD-OBS-04 | docs/FDD.md | Hipótese | Métricas: Quantidade de linhas na DLQ. | TRANSCRICAO | [09:18] Diego |
| FDD-OBS-05 | docs/FDD.md | Hipótese | Métricas: Tentativas por resultado: sucesso, falha e timeout. | TRANSCRICAO | [09:42] Diego |
| FDD-OBS-06 | docs/FDD.md | Hipótese | Métricas: Duração das chamadas HTTP em milissegundos (durationMs). | TRANSCRICAO | [09:42] Diego |
| FDD-OBS-07 | docs/FDD.md | Observabilidade | Logs: Formato: JSON do Pino, com o logger de src/shared/logger/index.ts. | CODIGO | src/shared/logger/index.ts:13 |
| FDD-OBS-08 | docs/FDD.md | Observabilidade | Logs: Eventos: webhook_event_enqueued, webhook_delivery_attempted, webhook_delivery_succeeded, webhook_delivery_failed,... | CODIGO | src/middlewares/request-logger.middleware.ts:14 |
| FDD-OBS-09 | docs/FDD.md | Observabilidade | Logs: Campos: eventId, webhookId, orderId, attempt, statusCode, durationMs e userId (no replay). | CODIGO | src/middlewares/request-logger.middleware.ts:14 |
| FDD-OBS-10 | docs/FDD.md | Observabilidade | Logs: Proteção de dados: a lista de redação passa a incluir *.secret e *.previous_secret, e o worker guarda o corpo da resposta do cliente... | CODIGO | src/shared/logger/index.ts:4 |
| FDD-OBS-11 | docs/FDD.md | Hipótese | Tracing: Hipótese: o projeto não tem biblioteca de tracing e a reunião mandou reaproveitar o que existe, então não há spans nesta fase. | TRANSCRICAO | [09:30] Larissa |
| FDD-OBS-12 | docs/FDD.md | Observabilidade | Tracing: Correlação: o requestId de src/middlewares/request-logger.middleware.ts identifica a chamada à API, e o eventId identifica o... | CODIGO | src/middlewares/request-logger.middleware.ts:6 |
| FDD-OBS-13 | docs/FDD.md | Observabilidade | Dashboards e alertas: Nenhum painel nesta fase. O dashboard visual da reunião é para o cliente e está fora do escopo. | TRANSCRICAO | [09:40] Larissa |
| FDD-OBS-14 | docs/FDD.md | Hipótese | Dashboards e alertas: Hipótese de alertas mínimos: idade da linha PENDING mais antiga acima de 10 segundos e DLQ com mais de 0 linhas. | TRANSCRICAO | [09:02] Marcos |
| FDD-DEP-01 | docs/FDD.md | Dependência | Node.js 20: engines.node em package.json; fetch, AbortSignal.timeout e crypto nativos dispensam biblioteca | CODIGO | package.json:7 |
| FDD-DEP-02 | docs/FDD.md | Dependência | MySQL 8.0: Imagem mysql:8.0 em docker-compose.yml; único banco, sem Redis nem broker | CODIGO | docker-compose.yml:3 |
| FDD-DEP-03 | docs/FDD.md | Dependência | Prisma 5.22.0: @prisma/client e prisma; migration aditiva; PrismaClient próprio no worker | CODIGO | package.json:26 |
| FDD-DEP-04 | docs/FDD.md | Dependência | Express 4.21.1: Rotas montadas em /api/v1; corpo JSON limitado a 1 MB na entrada | CODIGO | package.json:28 |
| FDD-DEP-05 | docs/FDD.md | Dependência | Zod 3.23.8: Schemas de corpo, params e query validados por validate | CODIGO | package.json:33 |
| FDD-DEP-06 | docs/FDD.md | Dependência | Pino 9.5.0: Logger único da API e do worker | CODIGO | package.json:30 |
| FDD-DEP-07 | docs/FDD.md | Dependência | uuid 11.0.3: Geração dos identificadores UUID; o banco também usa uuid() do Prisma | CODIGO | package.json:32 |
| FDD-DEP-08 | docs/FDD.md | Dependência | Vitest 2.1.4: Testes no padrão de tests/, com supertest 7.0.0 | CODIGO | package.json:52 |
| FDD-DEP-09 | docs/FDD.md | Dependência | Os endpoints existentes não mudam, e a resposta de sucesso de changeStatus também não. | CODIGO | src/modules/orders/order.routes.ts:19 |
| FDD-DEP-10 | docs/FDD.md | Dependência | A migration é aditiva: cria tabelas novas e não altera as existentes. | CODIGO | prisma/migrations/20260519182739_init/migration.sql |
| FDD-DEP-11 | docs/FDD.md | Hipótese | Hipótese: nenhuma dependência npm é adicionada, porque os recursos nativos do Node 20 bastam. | TRANSCRICAO | [09:30] Larissa |
| FDD-DEP-12 | docs/FDD.md | Dependência | O envelope de erro { error: { code, message, details } } e o formato de paginação { data, pagination } são os mesmos do restante da API. | CODIGO | src/middlewares/error.middleware.ts:15; src/shared/http/response.ts:22 |
| FDD-DEP-13 | docs/FDD.md | Dependência | Os campos da API de configuração usam camelCase como o restante da API. | CODIGO | src/modules/orders/order.schemas.ts:12 |
| FDD-CA-01 | docs/FDD.md | Critério de Aceite | Atomicidade: forçar erro na gravação da outbox dentro de changeStatus deixa o pedido no status anterior e sem linha no histórico. | TRANSCRICAO | [09:40] Bruno |
| FDD-CA-02 | docs/FDD.md | Critério de Aceite | Filtro: para um customer com dois webhooks, um que assina SHIPPED e outro que não, a mudança para SHIPPED cria exatamente 1 linha na outbox. | TRANSCRICAO | [09:34] Bruno |
| FDD-CA-03 | docs/FDD.md | Critério de Aceite | Assinatura: o HMAC-SHA256 calculado pelo teste com a secret do endpoint é igual ao valor de X-Signature. | TRANSCRICAO | [09:20] Sofia |
| FDD-CA-04 | docs/FDD.md | Critério de Aceite | Backoff: as esperas são 60, 300, 1.800, 7.200 e 43.200 segundos, e a falha da 6ª requisição move o evento para a DLQ, conforme a... | TRANSCRICAO | [09:17] Larissa |
| FDD-CA-05 | docs/FDD.md | Critério de Aceite | Timeout: um servidor simulado que responde depois de 10 segundos gera uma tentativa com falha WEBHOOK_DELIVERY_TIMEOUT. | TRANSCRICAO | [09:42] Diego |
| FDD-CA-06 | docs/FDD.md | Critério de Aceite | Replay: ADMIN recebe 200 e a linha volta a PENDING; OPERATOR recebe 403. | TRANSCRICAO | [09:36] Sofia; [09:18] Diego |
| FDD-CA-07 | docs/FDD.md | Critério de Aceite | Payload (Hipótese de comportamento): um payload artificial de 64 KB mais 1 byte, montado em teste unitário, lança WEBHOOK_PAYLOAD_TOO_LARGE... | TRANSCRICAO | [09:24] Larissa |
| FDD-CA-08 | docs/FDD.md | Hipótese | Secret (Hipótese de requisito): GET de webhook nunca devolve a secret; a criação e a rotação devolvem. | TRANSCRICAO | [09:31] Marcos; [09:22] Diego |
| FDD-CA-09 | docs/FDD.md | Hipótese | Logs (Hipótese de requisito): a secret não aparece em nenhuma linha de log produzida pelo módulo. | TRANSCRICAO | [09:22] Diego |
| FDD-CA-10 | docs/FDD.md | Critério de Aceite | Latência: com o worker ligado e um cliente simulado que responde em menos de 1 segundo, o primeiro envio ocorre em menos de 10 segundos... | TRANSCRICAO | [09:02] Marcos |
| FDD-CA-11 | docs/FDD.md | Critério de Aceite | Regressão: os testes existentes em tests/ continuam passando. | CODIGO | tests/orders.test.ts:11 |
| FDD-CA-12 | docs/FDD.md | Critério de Aceite | Ordem: com um worker e nenhum envio falhando, 3 mudanças de status do mesmo pedido chegam na ordem de created_at. | TRANSCRICAO | [09:12] Diego |
| FDD-RISCO-01 | docs/FDD.md | Risco | Cliente fora do ar por mais de 14,6 horas | TRANSCRICAO | [09:17] Marcos |
| FDD-RISCO-02 | docs/FDD.md | Risco | Ordem fora de sequência | TRANSCRICAO | [09:12] Diego |
| FDD-RISCO-03 | docs/FDD.md | Risco | Vazamento de secret | TRANSCRICAO | [09:22] Diego |
| FDD-RISCO-04 | docs/FDD.md | Risco | Evento duplicado em cliente que não deduplica | TRANSCRICAO | [09:25] Sofia |
| FDD-RISCO-05 | docs/FDD.md | Risco | Worker parado | TRANSCRICAO | [09:11] Diego |
| FDD-RISCO-06 | docs/FDD.md | Risco | Acesso a webhooks de qualquer customer | TRANSCRICAO | [09:37] Sofia |
| FDD-RISCO-07 | docs/FDD.md | Hipótese | Endereço cadastrado aponta para a rede interna | TRANSCRICAO | [09:23] Sofia |
| FDD-RISCO-08 | docs/FDD.md | Risco | Falha na gravação da outbox desfaz a mudança de status | TRANSCRICAO | [09:40] Bruno |
| FDD-RISCO-09 | docs/FDD.md | Risco | Cliente lento atrasa os eventos seguintes do lote | TRANSCRICAO | [09:12] Diego; [09:42] Diego |
| FDD-INT-01 | docs/FDD.md | Integração | src/modules/orders/order.service.ts:126: Chama publishWebhookEvent(tx, order, from, to) depois do histórico e antes da releitura, na mesma... | CODIGO | src/modules/orders/order.service.ts:126 |
| FDD-INT-02 | docs/FDD.md | Integração | src/modules/orders/order.service.ts:24: A função de publicação recebe o tx tipado como Prisma.TransactionClient; o alias local TxClient não... | CODIGO | src/modules/orders/order.service.ts:24 |
| FDD-INT-03 | docs/FDD.md | Integração | src/modules/orders/order.service.ts:181: A outbox guarda order_id sem chave estrangeira, para o evento sobreviver à remoção do pedido | CODIGO | src/modules/orders/order.service.ts:181 |
| FDD-INT-04 | docs/FDD.md | Integração | src/modules/orders/order.status.ts:3: Hipótese: o schema de statuses usa z.enum com PAID, PROCESSING, SHIPPED, DELIVERED e CANCELLED | CODIGO | src/modules/orders/order.status.ts:3 |
| FDD-INT-05 | docs/FDD.md | Integração | prisma/schema.prisma:74: Quatro modelos novos no mesmo padrão (ver o modelo de dados abaixo) | CODIGO | prisma/schema.prisma:74 |
| FDD-INT-06 | docs/FDD.md | Integração | prisma/migrations/20260519182739_init/migration.sql: Nova migration aditiva gerada por npm run db:migrate | CODIGO | prisma/migrations/20260519182739_init/migration.sql |
| FDD-INT-07 | docs/FDD.md | Integração | src/shared/errors/app-error.ts:3: Base das subclasses de WEBHOOK_NOT_FOUND e WEBHOOK_DEAD_LETTER_NOT_FOUND | CODIGO | src/shared/errors/app-error.ts:3 |
| FDD-INT-08 | docs/FDD.md | Integração | src/shared/errors/http-errors.ts:27: WEBHOOK_INVALID_URL por BadRequestError, WEBHOOK_PAYLOAD_TOO_LARGE por UnprocessableEntityError,... | CODIGO | src/shared/errors/http-errors.ts:27 |
| FDD-INT-09 | docs/FDD.md | Integração | src/middlewares/error.middleware.ts:14: Sem alteração. | CODIGO | src/middlewares/error.middleware.ts:14 |
| FDD-INT-10 | docs/FDD.md | Integração | src/middlewares/auth.middleware.ts:49: O CRUD usa authenticate. O replay usa authenticate e requireRole('ADMIN'), como em user.routes.ts | CODIGO | src/middlewares/auth.middleware.ts:49 |
| FDD-INT-11 | docs/FDD.md | Integração | src/middlewares/validate.middleware.ts:11: Cada rota usa validate({ params, query, body }) com schemas de webhook.schemas.ts | CODIGO | src/middlewares/validate.middleware.ts:11 |
| FDD-INT-12 | docs/FDD.md | Integração | src/modules/orders/order.schemas.ts:23: Listas de webhooks e de entregas usam o mesmo schema de paginação e a mesma resposta { data,... | CODIGO | src/modules/orders/order.schemas.ts:23 |
| FDD-INT-13 | docs/FDD.md | Integração | src/routes/index.ts:13: Acrescenta webhooks ao tipo e monta /webhooks e /admin/webhooks | CODIGO | src/routes/index.ts:13 |
| FDD-INT-14 | docs/FDD.md | Integração | src/app.ts:26: Instancia o repository, o service e o controller de webhooks | CODIGO | src/app.ts:26 |
| FDD-INT-15 | docs/FDD.md | Integração | src/shared/logger/index.ts:4: Acrescenta *.secret e *.previous_secret à redação (Hipótese) e nomeia os eventos em snake_case | CODIGO | src/shared/logger/index.ts:4 |
| FDD-INT-16 | docs/FDD.md | Integração | src/server.ts:6: src/worker.ts (arquivo novo) segue o padrão e termina o lote antes de sair | CODIGO | src/server.ts:6 |
| FDD-INT-17 | docs/FDD.md | Integração | src/config/database.ts:4: O worker importa daqui e obtém seu PrismaClient, por ser outro processo | CODIGO | src/config/database.ts:4 |
| FDD-INT-18 | docs/FDD.md | Integração | src/config/env.ts:3: O worker lê o mesmo env e, por isso, exige JWT_SECRET sem usá-lo. Hipótese: manter assim | CODIGO | src/config/env.ts:3 |
| FDD-INT-19 | docs/FDD.md | Integração | package.json:10: Acrescenta o script worker (tsx --env-file=.env src/worker.ts). | CODIGO | package.json:10 |
| FDD-INT-20 | docs/FDD.md | Integração | tests/setup.ts:8: Inclui as tabelas de webhook na limpeza e usa ADMIN e OPERATOR nos testes de replay | CODIGO | tests/setup.ts:8 |
| FDD-INT-21 | docs/FDD.md | Integração | src/worker.ts (arquivo novo): Entrada do worker: carrega o env, cria o ciclo de 2 segundos e trata SIGTERM e SIGINT | TRANSCRICAO | [09:11] Larissa |
| FDD-INT-22 | docs/FDD.md | Integração | src/modules/webhooks/webhook.controller.ts, src/modules/webhooks/webhook.service.ts, src/modules/webhooks/webhook.repository.ts,... | TRANSCRICAO | [09:27] Bruno |
| FDD-INT-23 | docs/FDD.md | Integração | src/modules/webhooks/webhook.publisher.ts (arquivo novo): Contém publishWebhookEvent (Contrato 9) | TRANSCRICAO | [09:41] Bruno |
| FDD-INT-24 | docs/FDD.md | Integração | src/modules/webhooks/webhook.worker.ts (arquivo novo): Lógica de processamento, retry e DLQ. | TRANSCRICAO | [09:28] Bruno |
| FDD-MOD-01 | docs/FDD.md | Integração | webhook_endpoints: Hipótese de nome. Colunas id UUID, customer_id, url, secret, previous_secret, previous_secret_expires_at, statuses... | TRANSCRICAO | [09:21] Bruno; [09:21] Sofia |
| FDD-MOD-02 | docs/FDD.md | Integração | webhook_outbox: colunas id UUID (igual ao event_id), webhook_id, order_id (sem chave estrangeira), event_type, payload (JSON, snapshot),... | TRANSCRICAO | [09:08] Diego; [09:25] Diego |
| FDD-MOD-03 | docs/FDD.md | Integração | webhook_dead_letter: colunas id UUID, event_id, webhook_id, payload, failure_reason, failed_at e replayed_at. | TRANSCRICAO | [09:18] Diego |
| FDD-MOD-04 | docs/FDD.md | Hipótese | webhook_deliveries: Hipótese de nome. Colunas id UUID, event_id, webhook_id, attempt, success, status_code, response_body (Hipótese:... | TRANSCRICAO | [09:34] Marcos |
| FDD-HIP-01 | docs/FDD.md | Hipótese | O campo statuses aceita PAID, PROCESSING, SHIPPED, DELIVERED e CANCELLED. | CODIGO | src/modules/orders/order.status.ts:3 |
| FDD-HIP-02 | docs/FDD.md | Hipótese | Hipótese: a rota e o formato dos parâmetros são proposta do FDD; a reunião definiu o método e o objeto, e só as rotas do histórico e do... | TRANSCRICAO | [09:31] Marcos |
| FDD-HIP-03 | docs/FDD.md | Hipótese | Hipótese: a rota e o formato dos parâmetros são proposta do FDD; a reunião definiu o método e o objeto, e só as rotas do histórico e do... | TRANSCRICAO | [09:33] Bruno |
| FDD-HIP-04 | docs/FDD.md | Hipótese | Hipótese: a rota e o formato dos parâmetros são proposta do FDD; a reunião definiu o método e o objeto, e só as rotas do histórico e do... | TRANSCRICAO | [09:33] Bruno |
| FDD-HIP-05 | docs/FDD.md | Hipótese | Hipótese: a remoção é física. Os eventos pendentes desse webhook são descartados pelo worker com o log webhook_event_discarded. | TRANSCRICAO | [09:33] Bruno |
| FDD-HIP-06 | docs/FDD.md | Hipótese | Hipótese: a rota e o formato dos parâmetros são proposta do FDD; a reunião definiu o método e o objeto, e só as rotas do histórico e do... | TRANSCRICAO | [09:33] Bruno |
| FDD-HIP-07 | docs/FDD.md | Hipótese | 200: nova secret gerada e devolvida uma única vez. A secret anterior continua válida por 24 horas, até previousSecretExpiresAt (Hipótese de... | TRANSCRICAO | [09:21] Sofia |
| FDD-HIP-08 | docs/FDD.md | Hipótese | Hipótese: o caminho /secret/rotate é proposta deste FDD, porque a reunião decidiu a capacidade e não a rota. | TRANSCRICAO | [09:21] Sofia |
| FDD-HIP-09 | docs/FDD.md | Hipótese | Hipótese: responseBody é guardado truncado em 2 KB. | TRANSCRICAO | [09:34] Marcos |
| FDD-HIP-10 | docs/FDD.md | Hipótese | 200: o evento voltou para a outbox como PENDING. Hipótese: com o mesmo eventId. | TRANSCRICAO | [09:18] Diego |
| FDD-HIP-11 | docs/FDD.md | Hipótese | 409 WEBHOOK_ALREADY_REPLAYED: a linha já foi reprocessada. Hipótese: um reprocessamento por linha. | TRANSCRICAO | [09:18] Diego |
| FDD-HIP-12 | docs/FDD.md | Hipótese | Hipótese: 200 a 299 é entrega com sucesso, e qualquer outra resposta, erro de conexão ou ausência de resposta em 10 segundos é falha e... | TRANSCRICAO | [09:42] Diego |
| FDD-HIP-13 | docs/FDD.md | Hipótese | X-Timestamp: instante do envio, para o cliente detectar replay. Hipótese: formato ISO 8601. O header não faz parte da assinatura. | TRANSCRICAO | [09:44] Diego |
| FDD-HIP-14 | docs/FDD.md | Hipótese | X-Signature: HMAC-SHA256 do corpo exato da requisição com a secret do endpoint. | TRANSCRICAO | [09:20] Sofia |
| ADR-001 | docs/adrs/ADR-001-outbox-no-mysql.md | Decisão | Outbox no MySQL para publicar eventos de webhook | TRANSCRICAO | [09:08] Larissa |
| ADR-001-ALT-01 | docs/adrs/ADR-001-outbox-no-mysql.md | Alternativa | Outbox no MySQL existente | TRANSCRICAO | [09:08] Larissa |
| ADR-001-ALT-02 | docs/adrs/ADR-001-outbox-no-mysql.md | Alternativa | Chamada HTTP síncrona dentro do serviço de pedidos | TRANSCRICAO | [09:04] Bruno |
| ADR-001-ALT-03 | docs/adrs/ADR-001-outbox-no-mysql.md | Alternativa | Redis Streams ou outra fila externa | TRANSCRICAO | [09:07] Larissa |
| ADR-002 | docs/adrs/ADR-002-worker-separado-em-polling.md | Decisão | Worker em processo separado com polling de 2 segundos | TRANSCRICAO | [09:10] Larissa |
| ADR-002-ALT-01 | docs/adrs/ADR-002-worker-separado-em-polling.md | Alternativa | Processo separado que consulta a outbox a cada 2 segundos | TRANSCRICAO | [09:09] Diego |
| ADR-002-ALT-02 | docs/adrs/ADR-002-worker-separado-em-polling.md | Alternativa | Gatilho do banco para avisar o processo | TRANSCRICAO | [09:09] Bruno |
| ADR-002-ALT-03 | docs/adrs/ADR-002-worker-separado-em-polling.md | Alternativa | Leitor dentro do processo da API | TRANSCRICAO | [09:11] Diego |
| ADR-003 | docs/adrs/ADR-003-retry-com-backoff-e-dlq.md | Decisão | Retry com backoff exponencial e DLQ em tabela separada | TRANSCRICAO | [09:17] Larissa |
| ADR-003-ALT-01 | docs/adrs/ADR-003-retry-com-backoff-e-dlq.md | Alternativa | Cinco retentativas com espera crescente e DLQ em tabela separada | TRANSCRICAO | [09:17] Larissa |
| ADR-003-ALT-02 | docs/adrs/ADR-003-retry-com-backoff-e-dlq.md | Alternativa | Outro número de tentativas, como três tentativas ou retry indefinido | TRANSCRICAO | [09:15] Diego; [09:16] Bruno |
| ADR-003-ALT-03 | docs/adrs/ADR-003-retry-com-backoff-e-dlq.md | Alternativa | Marcar o evento como falho na própria outbox, sem tabela separada | TRANSCRICAO | [09:18] Diego |
| ADR-004 | docs/adrs/ADR-004-hmac-sha256-secret-por-endpoint.md | Decisão | Assinatura HMAC-SHA256 com secret por endpoint e rotação de 24 horas | TRANSCRICAO | [09:22] Sofia |
| ADR-004-ALT-01 | docs/adrs/ADR-004-hmac-sha256-secret-por-endpoint.md | Alternativa | HMAC-SHA256 com secret única por endpoint e rotação com sobreposição de 24 horas | TRANSCRICAO | [09:22] Sofia |
| ADR-004-ALT-02 | docs/adrs/ADR-004-hmac-sha256-secret-por-endpoint.md | Alternativa | Secret global da plataforma | TRANSCRICAO | [09:21] Sofia |
| ADR-004-ALT-03 | docs/adrs/ADR-004-hmac-sha256-secret-por-endpoint.md | Hipótese | Somente HTTPS, sem assinatura do conteúdo (plausível, não discutida na reunião) | TRANSCRICAO | [09:23] Sofia |
| ADR-005 | docs/adrs/ADR-005-entrega-at-least-once-com-x-event-id.md | Decisão | Entrega at-least-once com identificador de evento no header | TRANSCRICAO | [09:26] Larissa |
| ADR-005-ALT-01 | docs/adrs/ADR-005-entrega-at-least-once-com-x-event-id.md | Alternativa | Entrega ao menos uma vez (at-least-once) com identificador do evento no header | TRANSCRICAO | [09:25] Diego |
| ADR-005-ALT-02 | docs/adrs/ADR-005-entrega-at-least-once-com-x-event-id.md | Alternativa | Entrega exatamente uma vez (exactly-once) | TRANSCRICAO | [09:25] Diego |
| ADR-005-ALT-03 | docs/adrs/ADR-005-entrega-at-least-once-com-x-event-id.md | Hipótese | Entrega ao menos uma vez sem identificador, com o cliente comparando o conteúdo | TRANSCRICAO | [09:25] Bruno |
| ADR-006 | docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md | Decisão | Reuso dos padrões existentes do projeto | TRANSCRICAO | [09:30] Larissa |
| ADR-006-ALT-01 | docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md | Alternativa | Reuso máximo dos padrões existentes | TRANSCRICAO | [09:30] Larissa |
| ADR-006-ALT-02 | docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md | Hipótese | Módulo com tratamento de erros, logs e validação próprios (plausível, não discutida | TRANSCRICAO | [09:28] Bruno |
| ADR-006-ALT-03 | docs/adrs/ADR-006-reuso-dos-padroes-do-projeto.md | Hipótese | Reuso parcial: aproveitar erros e log, mas criar validação e controle de acesso | TRANSCRICAO | [09:36] Larissa |
| ADR-007 | docs/adrs/ADR-007-publicacao-do-evento-na-transacao-do-change-status.md | Decisão | Publicação do evento dentro da transação de mudança de status | TRANSCRICAO | [09:41] Bruno |
| ADR-007-ALT-01 | docs/adrs/ADR-007-publicacao-do-evento-na-transacao-do-change-status.md | Alternativa | Função de publicação que recebe o cliente da transação corrente | TRANSCRICAO | [09:41] Diego |
| ADR-007-ALT-02 | docs/adrs/ADR-007-publicacao-do-evento-na-transacao-do-change-status.md | Alternativa | Injetar o repositório de webhooks no serviço de pedidos | TRANSCRICAO | [09:41] Bruno |
| ADR-007-ALT-03 | docs/adrs/ADR-007-publicacao-do-evento-na-transacao-do-change-status.md | Alternativa | Publicar o evento depois da confirmação da transação | TRANSCRICAO | [09:41] Diego |
