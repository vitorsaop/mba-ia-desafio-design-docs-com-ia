# Plano dos design docs: Sistema de Webhooks de Notificação de Pedidos

Este arquivo é a entrada única das skills `adr-creator`, `rfc-creator`, `fdd-creator`, `prd-creator` e `tracker-creator`.
Ele não é um dos documentos entregáveis. Toda afirmação aqui aponta para uma linha da `TRANSCRICAO.md` ou para um arquivo do código.

## S0. Convenções

**Classes de cada item**

| Classe | Significado | Como entra nos documentos |
| --- | --- | --- |
| A | Decidido ou pedido na reunião | Texto direto. O Tracker aponta para `[hh:mm] Nome`. |
| B | Derivado: consequência necessária de um item A ou do código existente | Texto direto, quando o item A ou o código obriga. O Tracker aponta para o item A ou para o arquivo. |
| C | Lacuna: a reunião não decidiu | Nunca vira requisito ou decisão. Entra como questão em aberto (RFC) ou como "Hipótese:" rotulada (PRD e FDD). O Tracker aponta para a fala que originou a lacuna. |

**Metadados dos documentos**: Responsável e autor: Vitor Oliveira. Versão: 1.0. Data: 2026-10-17 (a transcrição não informa a data da reunião; usa-se a data de escrita). Nos ADRs a data usa o formato DD-MM-AAAA: 17-10-2026.

**Fonte da verdade**: a `TRANSCRICAO.md`. Se este plano divergir dela, vale a transcrição e o plano é corrigido. Uma correção vale para PRD, RFC, FDD, ADRs e Tracker.

**Formato das citações**: transcrição como `[hh:mm] Nome`; código como `caminho:linha`. Todo par `[hh:mm] Nome` deste plano existe como início de linha em `TRANSCRICAO.md`.

**Vocabulário fixo**
- Outbox: tabela no próprio banco onde o evento é gravado na mesma transação da mudança de status.
- DLQ (dead letter queue): tabela dos eventos que esgotaram as tentativas.
- At-least-once: cada evento é entregue uma ou mais vezes.
- Estados da outbox, em inglês no código: PENDING (pendente), PROCESSING (processando), FAILED (falhou, aguardando nova tentativa), DELIVERED (entregue). Fonte: `[09:08] Diego`.

**Estilo**: português simples e direto; sem emoji; sem travessão (U+2014); sem termos vagos como "adequado", "robusto", "rápido" sem número; toda hipótese começa com "Hipótese:".

## S1. Mapa do código (CODIGO)

| ID | Caminho:linha | Fato verificado | Uso no módulo de webhooks |
| --- | --- | --- | --- |
| CODE-01 | `src/modules/orders/order.service.ts:126` | `changeStatus` abre `$transaction` (L131), atualiza o pedido (L158), grava o histórico (L159) e relê o pedido (L169) | Chamar a função de publicação do evento depois do histórico (L167) e antes da releitura (L169), na mesma transação |
| CODE-02 | `src/modules/orders/order.service.ts:24` | O tipo `TxClient` é `Prisma.TransactionClient`; o construtor (L26-30) recebe `orders` e `prisma` | A função de publicação recebe o `tx`; o construtor não muda |
| CODE-03 | `src/modules/orders/order.service.ts:181` | `delete` só aceita pedido PENDING ou CANCELLED; o histórico é apagado em cascata (`prisma/schema.prisma:125`) | A outbox guarda `order_id` sem chave estrangeira para `orders`, para o evento sobreviver à remoção do pedido |
| CODE-04 | `src/modules/orders/order.status.ts:3` | O mapa de transições não tem PENDING como destino | O filtro de status do webhook aceita só PAID, PROCESSING, SHIPPED, DELIVERED e CANCELLED |
| CODE-05 | `prisma/schema.prisma:26` | Ids são `String @id @default(uuid()) @db.Char(36)`; tabelas usam `@@map` em snake_case (ex.: L37) | Novos modelos seguem o mesmo padrão |
| CODE-06 | `prisma/migrations/20260519182739_init/migration.sql` | Existe uma única migration; colunas de data são `DATETIME(3)`; charset utf8mb4 | Nova migration aditiva para as tabelas de webhook |
| CODE-07 | `src/shared/errors/app-error.ts:3` | `AppError(message, statusCode, errorCode, details)` | Base de todos os erros `WEBHOOK_*` |
| CODE-08 | `src/shared/errors/http-errors.ts:27` | `NotFoundError` tem código fixo `NOT_FOUND` (L27-31); `BadRequestError` (L3), `ConflictError` (L33) e `UnprocessableEntityError` (L39) aceitam `code`; `InvalidStatusTransitionError` (L45-53) é subclasse com código próprio | `WEBHOOK_NOT_FOUND` exige subclasse de `AppError` no padrão de L45-53 |
| CODE-09 | `src/middlewares/error.middleware.ts:14` | Trata `AppError` (L15-24), `ZodError` (L26-35), Prisma P2002 e P2025 (L37-54); o resto vira 500 (L56-64); P2003 não é tratado | Erros do módulo passam sem alteração do middleware |
| CODE-10 | `src/middlewares/auth.middleware.ts:27` | `authenticate` (L27-47) e `requireRole` (L49-61); `JwtPayload` (L19-25) só tem `sub`, `email`, `role` | CRUD com `authenticate`; replay com `authenticate` e `requireRole('ADMIN')`; o JWT não identifica o customer |
| CODE-11 | `src/modules/users/user.routes.ts:15` | Único uso atual de `requireRole('ADMIN')` | Padrão de composição para a rota de replay |
| CODE-12 | `src/middlewares/validate.middleware.ts:11` | Falha do Zod vira `ValidationError` com código `VALIDATION_ERROR` (L26-32) | Validação de corpo, query e params dos endpoints novos |
| CODE-13 | `src/modules/orders/order.schemas.ts:23` | `listOrdersQuerySchema` com `page` e `pageSize` (máximo 100, L25); campos da API em camelCase (`customerId`, `toStatus`) | Schemas de webhook seguem o padrão; paginação das listas |
| CODE-14 | `src/routes/index.ts:13` | Tipo `Controllers` (L13-19) e montagem dos routers (L24-28) | Registrar o controller e o router de webhooks e o router administrativo |
| CODE-15 | `src/app.ts:26` | `buildControllers` (L26-53) cria repository, service e controller de cada módulo; `/api/v1` em L67; `express.json({ limit: '1mb' })` em L59 | Instanciar o módulo de webhooks aqui |
| CODE-16 | `src/shared/logger/index.ts:4` | `redactPaths` (L4-11) não inclui `secret`; `createLogger` em L13-30 | Reusar o logger; acrescentar `*.secret` na redação |
| CODE-17 | `src/middlewares/request-logger.middleware.ts:5` | Gera `requestId` (L6) e loga o evento `http_request` (L14); nomes de evento de log em snake_case | Padrão de nomes dos logs do módulo e do worker |
| CODE-18 | `src/server.ts:6` | `bootstrap` (L6-22) cria a app, escuta a porta e trata SIGINT e SIGTERM; `shutdown` (L13-18) desconecta o Prisma e sai | Modelo para a entrada do worker; o worker termina o lote em andamento antes de sair |
| CODE-19 | `src/config/database.ts:4` | `createPrismaClient` (L4-8) e `prisma` (L10) | O worker importa de lá e obtém um `PrismaClient` por processo |
| CODE-20 | `src/config/env.ts:3` | `envSchema` (L3-10) exige `DATABASE_URL` e `JWT_SECRET` (L8) | O worker lê o mesmo `env` e, por isso, exige `JWT_SECRET` sem usá-lo |
| CODE-21 | `package.json:10` | Scripts `dev`, `build`, `start`, `db:*`, `test`; não há script `worker`; `engines.node` `>=20` (L7-9) | Acrescentar o script `worker`; `fetch`, `AbortSignal.timeout` e `crypto` são nativos do Node 20 |
| CODE-22 | `package.json:32` | Dependências `uuid` 11.0.3 (L32), `zod` 3.23.8, `pino` 9.5.0, `express` 4.21.1, `@prisma/client` 5.22.0, `vitest` 2.1.4 | Nenhuma dependência nova |
| CODE-23 | `docker-compose.yml:2` | O único serviço é `mysql` (imagem `mysql:8.0`, L3); não há Redis nem broker | Justifica a outbox no MySQL |
| CODE-24 | `src/shared/http/response.ts:13` | `buildPagination` (L13) e `paginated` (L22) devolvem `{ data, pagination }` | Formato das listas de webhooks e de entregas |
| CODE-25 | `tests/setup.ts:8` | `beforeEach` apaga as tabelas em ordem; `tests/helpers/factories.ts:76` tem `bootstrapAuthenticatedUser(role)`; `vitest.config.ts:15` usa `singleFork` | Estratégia de testes; as tabelas novas entram na limpeza na implementação |
| CODE-26 | `prisma/schema.prisma:25` | `User` guarda só `passwordHash` (hash de via única); não há campo que ligue `User` a `Customer` (L40-53) | Uma secret de HMAC não pode seguir o padrão de hash; não há isolamento por customer |
| CODE-27 | `tsconfig.build.json:7` | `include` cobre `src/**/*.ts` | `src/worker.ts` é compilado para `dist/worker.js` sem mudança de configuração |

## S2. Requisitos funcionais

| ID | Classe | Requisito | Localização |
| --- | --- | --- | --- |
| RF-01 | A | Cadastrar webhook por POST, com `url`, lista de status e `customerId` no corpo. A secret é gerada pelo sistema e devolvida na criação | `[09:31] Marcos`; `[09:32] Larissa` |
| RF-02 | A | Listar os webhooks de um customer | `[09:33] Bruno` |
| RF-03 | A | Editar o webhook por PATCH, incluindo o estado ativo | `[09:33] Bruno`; `[09:21] Bruno` |
| RF-04 | A | Remover o webhook por DELETE | `[09:33] Bruno` |
| RF-05 | A | Filtro por endpoint: lista de status que o webhook quer receber, aplicada na inserção na outbox. Se nenhum webhook do customer quer o status, nada é inserido | `[09:33] Marcos`; `[09:34] Bruno` |
| RF-06 | A | Histórico de entregas por webhook: últimos 100 envios com sucesso ou falha, payload, resposta e tempo de resposta (`GET /webhooks/:id/deliveries`) | `[09:34] Marcos` |
| RF-07 | A | Rotação de secret pela API. A secret anterior permanece válida por 24 horas | `[09:21] Sofia` |
| RF-08 | A | Gravar o evento na outbox na mesma transação do `changeStatus`. Se a inserção falhar, a mudança de status é revertida | `[09:40] Bruno`; `[09:41] Diego` |
| RF-09 | A | O worker busca os eventos pendentes mais antigos a cada 2 segundos, em lote pequeno, envia a requisição HTTP e marca o evento como entregue | `[09:08] Diego`; `[09:09] Diego` |
| RF-10 | A | Retry com backoff exponencial de 1 minuto, 5 minutos, 30 minutos, 2 horas e 12 horas, com 5 tentativas | `[09:17] Diego`; `[09:17] Larissa` |
| RF-11 | A | Esgotadas as tentativas, mover o evento para a DLQ (tabela separada) com payload, motivo da falha e timestamp | `[09:18] Diego` |
| RF-12 | A | Replay manual: `POST /admin/webhooks/dead-letter/:id/replay` recoloca o evento na outbox como pendente. Exige role ADMIN e registra em log quem executou | `[09:18] Diego`; `[09:36] Sofia`; `[09:36] Larissa` |
| RF-13 | A | Payload JSON com `event_id`, `event_type` igual a "order.status_changed", `timestamp` ISO 8601, `order_id`, `order_number`, `from_status`, `to_status`, `customer_id` e `total_cents`, sem itens do pedido | `[09:43] Diego` |
| RF-14 | A | Headers do envio: `X-Event-Id`, `X-Signature`, `X-Timestamp`, `X-Webhook-Id` e `Content-Type: application/json` | `[09:44] Diego`; `[09:44] Sofia` |
| RF-15 | A | O payload é gravado já renderizado (snapshot) no momento da inserção | `[09:52] Larissa`; `[09:52] Bruno` |

**Agrupamento nos 12 requisitos do PRD (blocos FR)**: FR-01 = RF-01; FR-02 = RF-02; FR-03 = RF-03; FR-04 = RF-04; FR-05 = RF-05; FR-06 = RF-06; FR-07 = RF-07; FR-08 = RF-08 e RF-15; FR-09 = RF-09, RF-13 e RF-14; FR-10 = RF-10; FR-11 = RF-11; FR-12 = RF-12.
**Prioridade (critério do autor)**: alta = o item aparece no resumo final de `[09:48] Larissa` (FR-01, FR-02, FR-03, FR-04, FR-07, FR-08, FR-09, FR-10, FR-11, FR-12); media = pedido pelo PM em `[09:31] Marcos` a `[09:34] Marcos` e ausente do resumo final (FR-05, FR-06).

## S3. Requisitos não funcionais e restrição

| ID | Classe | Requisito | Localização |
| --- | --- | --- | --- |
| RNF-01 | A | Notificação em menos de 10 segundos após a mudança de status. O polling de 2 segundos acrescenta no máximo 2 segundos | `[09:02] Marcos`; `[09:09] Diego`; `[09:10] Larissa` |
| RNF-02 | A | Atomicidade: não existe status alterado sem evento registrado, nem evento sem status alterado | `[09:40] Bruno`; `[09:41] Diego` |
| RNF-03 | A | Isolamento: cliente lento ou fora do ar não trava a mudança de status de outros pedidos e não causa rollback dela | `[09:04] Bruno` |
| RNF-04 | A | Timeout de 10 segundos por chamada HTTP; estouro conta como falha e agenda retry | `[09:42] Diego` |
| RNF-05 | A | Payload de no máximo 64 KB; acima disso, erro, sem truncar | `[09:23] Sofia`; `[09:24] Diego`; `[09:24] Larissa` |
| RNF-06 | A | URL do webhook obrigatoriamente `https` | `[09:23] Sofia` |
| RNF-07 | A | Entrega at-least-once; a deduplicação é do cliente, por `X-Event-Id` | `[09:24] Diego`; `[09:26] Larissa` |
| RNF-08 | A | Ordem de entrega garantida só por `order_id` e só enquanto houver um único worker; sem garantia de ordem global | `[09:12] Diego`; `[09:13] Larissa`; `[09:14] Marcos` |
| RNF-09 | A | Worker em processo separado da API | `[09:11] Diego` |
| RNF-10 | A | Janela total de retry de cerca de 14,6 horas (1+5+30+120+720 = 876 minutos) | `[09:17] Diego`; `[09:17] Marcos` |
| RNF-11 | A | Índices nos campos de status e `created_at` da outbox; leitura em lote pequeno | `[09:08] Diego` |
| RNF-12 | A | Reuso dos padrões do projeto: módulo em `src/modules/webhooks`, `AppError`, Pino, error middleware, schemas Zod, prefixo `WEBHOOK_`, ids UUID | `[09:30] Larissa`; `[09:51] Larissa` |
| RNF-13 | A | Mesmo banco e mesma `DATABASE_URL`; `PrismaClient` próprio no worker | `[09:30] Bruno`; `[09:11] Diego` |
| REST-01 | A | Prazo de 3 sprints, incluindo 2 dias úteis de revisão de segurança antes do deploy. A Atlas quer a entrega no fim de novembro | `[09:45] Marcos`; `[09:46] Larissa`; `[09:46] Sofia`; `[09:47] Larissa` |

## S4. Decisões técnicas e de segurança

| ID | Classe | Decisão | Localização | ADR |
| --- | --- | --- | --- | --- |
| DT-01 | A | Outbox no MySQL existente, gravada na mesma transação SQL que atualiza o pedido e o histórico | `[09:06] Diego`; `[09:08] Larissa` | ADR-001 |
| DT-02 | A | Tabelas: `webhook_outbox` (estados pendente, processando, falhou, entregue; índices em status e `created_at`), `webhook_dead_letter` e tabela de configuração (url, secret, customer_id, ativo) | `[09:08] Diego`; `[09:18] Diego`; `[09:21] Bruno` | ADR-001 |
| DT-03 | A | Ids em UUID | `[09:51] Larissa` | ADR-001 |
| DT-04 | A | Snapshot do payload na inserção | `[09:52] Larissa`; `[09:52] Diego` | ADR-001 |
| DT-05 | A | Worker em polling de 2 segundos; sem trigger de banco | `[09:09] Diego`; `[09:10] Larissa` | ADR-002 |
| DT-06 | A | Entrada nova `src/worker.ts` com script `npm run worker`; lógica em `src/modules/webhooks/webhook.worker.ts` ou `webhook.processor.ts`; um único worker | `[09:11] Larissa`; `[09:12] Diego`; `[09:28] Bruno` | ADR-002 |
| DT-07 | A | `PrismaClient` próprio no worker, com a mesma `DATABASE_URL` | `[09:30] Bruno` | ADR-002 |
| DT-08 | A | Retry com backoff 1m/5m/30m/2h/12h, 5 tentativas, DLQ em tabela separada, replay manual por endpoint administrativo | `[09:15] Diego`; `[09:17] Larissa`; `[09:18] Diego` | ADR-003 |
| DT-09 | A | At-least-once com `X-Event-Id` (UUID gerado quando o evento entra na outbox) | `[09:25] Diego`; `[09:26] Larissa` | ADR-005 |
| DT-10 | A | Função `publishWebhookEvent(tx, order, fromStatus, toStatus)` chamada pelo `changeStatus`; não se injeta o repository inteiro | `[09:41] Bruno`; `[09:41] Diego` | ADR-007 |
| DT-11 | A | Filtro de status aplicado na inserção, não no envio | `[09:34] Bruno`; `[09:34] Diego` | ADR-007 |
| DT-12 | A | Reuso máximo: módulo com controller, service, repository, routes e schemas; `AppError`; Pino; error middleware; Zod; códigos com prefixo `WEBHOOK_` | `[09:27] Bruno`; `[09:28] Bruno`; `[09:29] Larissa`; `[09:30] Larissa` | ADR-006 |
| DT-13 | A | Timeout de 10 segundos | `[09:42] Diego` | FDD |
| DT-14 | A | Formato do payload e headers | `[09:43] Diego`; `[09:44] Sofia` | FDD |
| DS-01 | A | Assinatura HMAC-SHA256 sobre o corpo, enviada em `X-Signature` | `[09:20] Sofia`; `[09:22] Sofia` | ADR-004 |
| DS-02 | A | Secret única por endpoint, nunca global | `[09:21] Sofia` | ADR-004 |
| DS-03 | A | Rotação pela API com período de 24 horas em que a secret anterior continua válida | `[09:21] Sofia`; `[09:22] Sofia` | ADR-004 |
| DS-04 | A | URL `https` obrigatória | `[09:23] Sofia` | FDD |
| DS-05 | A | Limite de 64 KB com erro | `[09:23] Sofia`; `[09:24] Diego` | FDD |
| DS-06 | A | `X-Timestamp` com o instante do envio, para o cliente detectar replay se quiser | `[09:44] Diego` | FDD |
| DS-07 | A | Replay da DLQ só para ADMIN, com log de quem executou | `[09:36] Sofia`; `[09:36] Larissa` | FDD |
| DS-08 | A | CRUD de configuração liberado a qualquer role autenticada, "por enquanto" | `[09:36] Marcos`; `[09:37] Sofia` | FDD |
| DS-09 | A | Revisão de segurança de 2 dias úteis antes do deploy, com foco em HMAC e geração de secret | `[09:46] Sofia` | PRD, RFC |
| DS-10 | C | Hipótese: a secret não aparece em logs nem em respostas de leitura. O vazamento citado em `[09:22] Diego` foi no log do cliente; a reunião só mandou devolver a secret na criação (`[09:31] Marcos`) | `[09:22] Diego`; `[09:31] Marcos`; CODE-16 | FDD |

## S5. Descartados e adiados

**Descartados (alimentam as Alternativas do RFC e dos ADRs; nunca viram requisito)**

| ID | Item descartado | Motivo | Localização |
| --- | --- | --- | --- |
| DESC-01 | Chamada HTTP síncrona dentro do service de pedidos | Cliente lento trava a mudança de status; cliente fora do ar exigiria rollback | `[09:04] Bruno`; `[09:06] Diego` |
| DESC-02 | Redis Streams, Redis Cluster ou outra fila externa | Exige infraestrutura nova para um time pequeno | `[09:07] Larissa`; `[09:07] Diego` |
| DESC-03 | Trigger de banco para avisar o worker | O MySQL não tem listener nativo; trigger só executa SQL | `[09:09] Diego` |
| DESC-04 | Retry indefinido | Evento fica pendurado para sempre se o cliente sumir | `[09:15] Diego` |
| DESC-05 | Apenas 3 tentativas | Cobre cerca de 30 minutos e um cliente já teve manutenção planejada de 2 horas | `[09:16] Bruno`; `[09:16] Diego` |
| DESC-06 | Secret global da plataforma | Se uma vaza, vazam todas | `[09:21] Sofia` |
| DESC-07 | Garantia exactly-once | Exige coordenação dos dois lados | `[09:25] Diego` |
| DESC-08 | Truncar payload acima do limite | Se chegou a esse tamanho, há algo errado | `[09:23] Sofia` |
| DESC-09 | `customer_id` vindo do JWT | O JWT é do usuário do nosso sistema, não do cliente | `[09:32] Larissa` |
| DESC-10 | Itens do pedido no payload | Evita inflar o evento; o cliente consulta `GET /orders/:id` | `[09:43] Diego` |
| DESC-11 | Guardar só `order_id` e renderizar no envio | O evento deixaria de refletir o estado do momento da mudança | `[09:52] Larissa` |
| DESC-12 | Id auto incremental | O projeto usa UUID em tudo | `[09:51] Larissa` |
| DESC-13 | DLQ como status na própria outbox | A tabela separada deixa a leitura da outbox mais limpa e serve de evidência | `[09:18] Diego` |
| DESC-14 | Worker dentro do processo da API | Reiniciar a API perderia o worker | `[09:11] Diego` |
| DESC-15 | Publicar o evento fora da transação do pedido | Perde a garantia de atomicidade | `[09:41] Diego` |

**Adiados ou fora desta fase (alimentam "Fora de escopo" do PRD e "Questões em aberto" do RFC)**

| ID | Item | Localização |
| --- | --- | --- |
| ADIA-01 | E-mail ao cliente quando o webhook falha; talvez na próxima fase | `[09:37] Larissa`; `[09:38] Marcos` |
| ADIA-02 | Rate limiting de saída por cliente: observar e decidir depois | `[09:38] Diego`; `[09:39] Larissa` |
| ADIA-03 | Dashboard visual para o cliente; é projeto separado do time de frontend | `[09:40] Larissa` |
| ADIA-04 | Arquivamento das linhas entregues após cerca de 30 dias | `[09:08] Diego` |
| ADIA-05 | Vários workers: particionar por `order_id` ou usar lock pessimista | `[09:13] Diego` |
| ADIA-06 | Endurecer as permissões do CRUD de configuração | `[09:37] Sofia` |
| ADIA-07 | Webhook de entrada (o cliente enviar eventos para o sistema) | `[09:02] Marcos` |

## S6. Lacunas e conflitos (nada disso vira requisito)

| ID | Classe | Lacuna ou conflito | Tratamento nos documentos | Localização da origem |
| --- | --- | --- | --- | --- |
| LAC-01 | C | "5 tentativas" admite duas leituras: 5 envios no total ou 1 envio mais 5 retentativas | Adotar 1 envio inicial mais 5 retentativas, no máximo 6 requisições por ciclo de entrega, rotulado "Hipótese:" ou "Interpretação adotada:" em todos os documentos; um replay inicia novo ciclo. A soma dos 5 intervalos é 876 minutos, o que bate com "quase 15 horas entre primeira falha e última tentativa" | `[09:17] Diego`; `[09:17] Larissa` |
| LAC-02 | B | O backoff exige guardar a data da próxima tentativa; a reunião cita só os índices de status e `created_at` | O FDD acrescenta a coluna `next_attempt_at` e um índice composto | `[09:08] Diego`; `[09:17] Diego` |
| LAC-03 | B | O histórico de entregas exige registrar cada tentativa e nenhuma tabela para isso foi citada | O FDD propõe a tabela `webhook_deliveries`, uma linha por tentativa. Hipótese: guardar o corpo da resposta truncado em 2 KB | `[09:34] Marcos` |
| LAC-04 | C | Durante as 24 horas da rotação não se definiu o que vai em `X-Signature` nem onde fica a secret anterior | RFC: questão em aberto. FDD: Hipótese de duas assinaturas em hexadecimal separadas por vírgula, a nova primeiro; a secret anterior e o instante de expiração ficam na tabela de configuração | `[09:21] Sofia` |
| LAC-05 | C | Armazenamento da secret em repouso: o HMAC exige a chave recuperável (não serve hash) e `env.ts` não tem chave de cifra | RFC: questão em aberto, para a revisão de segurança | `[09:46] Sofia`; `[09:21] Sofia` |
| LAC-06 | C | O HMAC cobre só o corpo (`[09:22] Sofia`), então `X-Timestamp` pode ser alterado e a detecção de replay fica fraca | RFC: questão em aberto; PRD e FDD: risco | `[09:44] Diego`; `[09:22] Sofia` |
| LAC-07 | C | A reunião exigiu só `https`. Não se tratou de destinos internos da nossa infraestrutura (SSRF: o servidor chamar uma URL que aponta para dentro da rede) nem de redirecionamentos | RFC: questão em aberto; FDD: Hipótese de não seguir redirecionamentos | `[09:23] Sofia` |
| LAC-08 | C | Sem isolamento por customer: o JWT não tem customer (CODE-10) e `User` não se liga a `Customer` (CODE-26). Qualquer role autenticada gerencia e lê as entregas de qualquer customer | Risco aceito por decisão da reunião; registrado em PRD, RFC e FDD | `[09:32] Larissa`; `[09:36] Marcos`; `[09:37] Sofia` |
| LAC-09 | C | Ordem e retry: se o evento N está em espera de retry, o evento N+1 do mesmo pedido pode chegar antes | Entra na limitação conhecida de ordem | `[09:13] Larissa`; `[09:12] Diego` |
| LAC-10 | C | Linhas em PROCESSING quando o worker cai: a recuperação não foi discutida | FDD: Hipótese de devolver a PENDING, ao iniciar, as linhas em PROCESSING; a duplicata possível é coberta pelo at-least-once | `[09:11] Diego` |
| LAC-11 | C | Onde o limite de 64 KB é verificado e o que acontece. Um erro dentro do `changeStatus` reverte a mudança de status | Hipótese: verificar na inserção, com rollback e status 422, coerente com `[09:40] Bruno`; a reunião decidiu só "erro caso ultrapasse". O payload só tem campos escalares, então o limite funciona como proteção | `[09:23] Sofia`; `[09:24] Larissa`; `[09:40] Bruno` |
| LAC-12 | C | `http://` pode gerar `VALIDATION_ERROR` (Zod, CODE-12) ou `WEBHOOK_INVALID_URL` | Adotar `WEBHOOK_INVALID_URL`, status 400. O Zod valida só o tipo e o tamanho do campo; o service interpreta a URL e recusa o que não for `https` | `[09:23] Sofia`; `[09:28] Bruno` |
| LAC-13 | C | `WEBHOOK_SECRET_REQUIRED` foi citado sem semântica, e a secret é gerada pelo sistema | FDD: Hipótese de o código indicar webhook sem secret ativa no momento do envio (falha interna do worker) | `[09:28] Bruno` |
| LAC-14 | B | A criação do pedido (PENDING) não gera evento: a reunião integra só o `changeStatus`, e PENDING não é destino de transição (CODE-04) | O filtro aceita 5 status. Confirmação com o PM fica como questão em aberto | `[09:40] Bruno` |
| LAC-15 | C | Não se decidiu o que ocorre com eventos pendentes quando o webhook é removido, nem o destino da linha da DLQ após o replay | FDD: Hipótese de exclusão física do cadastro com descarte logado dos eventos pendentes; a linha da DLQ é mantida com `replayed_at` | `[09:33] Bruno`; `[09:18] Diego` |
| LAC-16 | C | Métricas e tracing não foram discutidos; só o Pino (`[09:29] Bruno`) e o reuso máximo (`[09:30] Larissa`) | FDD: Hipótese de métricas emitidas como logs estruturados e consultas SQL, tracing por correlação de identificadores, sem biblioteca nova | `[09:29] Bruno`; `[09:30] Larissa` |
| LAC-17 | C | O ponto de medição dos "10 segundos" não foi definido | Hipótese: da criação da linha na outbox até o início do primeiro envio | `[09:02] Marcos` |
| LAC-18 | B | `[09:10] Larissa` diz "latência mínima de 2 segundos no pior caso" | Os documentos dizem "latência adicional máxima de 2 segundos" | `[09:10] Larissa` |
| LAC-19 | C | Critério de sucesso da entrega não foi definido | Hipótese: qualquer resposta HTTP 2xx dentro de 10 segundos é sucesso; qualquer outra coisa é falha | `[09:42] Diego` |
| LAC-20 | B | Nomes dos campos da API de configuração: o código usa camelCase (CODE-13) e o payload do evento usa snake_case por decisão (`[09:43] Diego`) | API de configuração em camelCase (`customerId`, `statuses`, `active`); payload e headers do evento exatamente como decididos | `[09:31] Marcos`; `[09:43] Diego` |
| LAC-21 | C | O worker trata os eventos de um lote em sequência e cada chamada pode levar até 10 segundos. Um cliente lento atrasa os eventos seguintes e pode quebrar a meta de 10 segundos para eles | Registrar como risco e como questão em aberto; nenhuma mudança de decisão, porque a reunião definiu um único worker | `[09:12] Diego`; `[09:42] Diego` |
| LAC-22 | C | "Nenhuma dependência npm nova" não foi dita na reunião; decorre do reuso máximo e dos recursos nativos do Node 20 | Rotular "Hipótese:" | `[09:30] Larissa` |
| LAC-23 | C | O modelo de dados (colunas, índice composto, tabela de tentativas, secret anterior) é desenho do FDD; a reunião citou só `status` e `created_at` da outbox, os campos da configuração e o conteúdo da DLQ | Rotular "Hipótese de desenho" e registrar cada tabela no Tracker | `[09:08] Diego`; `[09:18] Diego`; `[09:21] Bruno` |

## S7. Insumos por documento

### S7.1 ADRs (adr-creator)

Sete arquivos em `docs/adrs/`, numeração de 001 a 007, Status "Aceito", data 17-10-2026.
Cobertura das 6 decisões obrigatórias do README: ADR-001 (Outbox), ADR-003 (retry e DLQ), ADR-004 (HMAC), ADR-005 (at-least-once), ADR-002 (worker em polling), ADR-006 (reuso).
Regra de conteúdo: os ADRs falam de conceitos. Nomes de tabela, classe, método e endpoint ficam no FDD. Nomes de headers do protocolo (`X-Event-Id`, `X-Signature`) e `HMAC-SHA256` podem aparecer porque são a própria decisão. Caminhos de arquivo só na seção Referências.

| ADR | Arquivo | Título | Decisões | Opções (a primeira é a escolhida) | ADRs relacionados |
| --- | --- | --- | --- | --- | --- |
| ADR-001 | `ADR-001-outbox-no-mysql.md` | Outbox no MySQL para publicar eventos de webhook | DT-01 a DT-04 | 1 Outbox no MySQL (DESC: nenhuma); 2 Chamada HTTP síncrona no service de pedidos (DESC-01); 3 Redis Streams ou fila externa (DESC-02) | ADR-002, ADR-007 |
| ADR-002 | `ADR-002-worker-separado-em-polling.md` | Worker em processo separado com polling de 2 segundos | DT-05 a DT-07 | 1 Processo separado com polling de 2 s; 2 Trigger de banco para avisar o worker (DESC-03); 3 Worker dentro do processo da API (DESC-14) | ADR-001, ADR-003 |
| ADR-003 | `ADR-003-retry-com-backoff-e-dlq.md` | Retry com backoff exponencial e DLQ em tabela separada | DT-08 | 1 Cinco retentativas com backoff 1m/5m/30m/2h/12h e DLQ separada; 2 Outro número de tentativas: 3 tentativas ou retry indefinido (DESC-04, DESC-05); 3 Marcar como falho na própria outbox, sem tabela separada (DESC-13) | ADR-001, ADR-002, ADR-005 |
| ADR-004 | `ADR-004-hmac-sha256-secret-por-endpoint.md` | Assinatura HMAC-SHA256 com secret por endpoint e rotação de 24 horas | DS-01 a DS-03 | 1 HMAC-SHA256 com secret por endpoint e rotação; 2 Secret global da plataforma (DESC-06) | ADR-005, ADR-006 |
| ADR-005 | `ADR-005-entrega-at-least-once-com-x-event-id.md` | Entrega at-least-once com identificador de evento no header | DT-09 | 1 At-least-once com `X-Event-Id`; 2 Exactly-once (DESC-07) | ADR-001, ADR-003 |
| ADR-006 | `ADR-006-reuso-dos-padroes-do-projeto.md` | Reuso dos padrões existentes do projeto | DT-12 | 1 Reuso máximo dos padrões existentes; 2 Módulo novo com erros, logs e validação próprios (plausível, não discutido) | ADR-004, ADR-007 |
| ADR-007 | `ADR-007-publicacao-do-evento-na-transacao-do-change-status.md` | Publicação do evento dentro da transação do changeStatus | DT-10, DT-11 | 1 Função de publicação que recebe o cliente transacional; 2 Injetar o repository de webhooks no service de pedidos (discutido em `[09:41] Bruno`); 3 Publicar depois do commit (DESC-15) | ADR-001, ADR-005 |

**Consequências de cada ADR** (3 parágrafos: Positivas, Negativas, Trade-off):

| ADR | Positivas | Negativas | Trade-off |
| --- | --- | --- | --- |
| ADR-001 | Rollback leva o evento junto; sem infraestrutura nova; payload estável porque é snapshot | Carga extra no banco transacional; a tabela cresce porque o arquivamento ficou fora do escopo (ADIA-04); falha na outbox reverte a mudança de status | Simplicidade operacional em troca de usar o banco relacional como fila, com menos vazão que um broker dedicado |
| ADR-002 | A API reinicia sem perder o worker; atraso adicional máximo de 2 s cabe nos 10 s | Leituras periódicas mesmo sem eventos; ordem só com um worker (LAC-09); um processo a mais para implantar e operar | Previsibilidade e simplicidade em troca de até 2 s de atraso e de escala horizontal limitada |
| ADR-003 | Cobre cerca de 14,6 h de indisponibilidade; nenhum evento fica pendurado; a DLQ guarda a evidência para depuração | Cliente fora por mais de 14,6 h exige replay manual; sem e-mail ao cliente nesta fase (ADIA-01) | Janela longa de espera pelo cliente em troca de eventos que só terminam em DLQ depois de cerca de 14,6 h |
| ADR-004 | Vazamento fica restrito a um endpoint; o cliente valida com biblioteca padrão; rotação sem parada | O sistema precisa guardar a secret de forma recuperável (LAC-05); o `X-Timestamp` não é assinado (LAC-06); gestão de duas secrets por 24 h | Segurança por endpoint em troca de gerenciar o ciclo de vida das secrets |
| ADR-005 | Nenhum evento é perdido; sem coordenação entre os dois lados | O cliente precisa deduplicar; duplicatas são possíveis após falha | Simplicidade do emissor em troca de responsabilidade do cliente, que o PM documenta no portal (`[09:26] Marcos`) |
| ADR-006 | Consistência com o restante do código; erros e logs tratados no mesmo lugar; menos código novo | O erro "não encontrado" existente tem código fixo, então `WEBHOOK_NOT_FOUND` exige especialização; a redação de logs precisa cobrir secrets; o worker exige `JWT_SECRET` | Consistência em troca de herdar as limitações atuais do código |
| ADR-007 | Garantia de atomicidade; baixo acoplamento do service de pedidos | A transação de status fica mais longa (consulta de webhooks e inserções); o módulo de pedidos passa a depender do módulo de webhooks | Atomicidade forte em troca de mais trabalho dentro da transação existente |

**Referências por ADR** (mínimo 3, máximo 5, todas verificadas):
- ADR-001: `prisma/schema.prisma:74`; `src/modules/orders/order.service.ts:131`; `src/modules/orders/order.service.ts:159`; `docker-compose.yml:2`.
- ADR-002: `src/server.ts:6`; `src/config/database.ts:4`; `src/config/env.ts:3`; `package.json:10`.
- ADR-003: `src/middlewares/auth.middleware.ts:49`; `src/shared/logger/index.ts:13`; `prisma/schema.prisma:116`.
- ADR-004: `src/shared/logger/index.ts:4`; `src/middlewares/auth.middleware.ts:27`; `src/config/env.ts:3`; `prisma/schema.prisma:25`.
- ADR-005: `prisma/schema.prisma:26`; `package.json:32`; `src/middlewares/request-logger.middleware.ts:6`.
- ADR-006: `src/shared/errors/app-error.ts:3`; `src/middlewares/error.middleware.ts:14`; `src/middlewares/auth.middleware.ts:49`; `src/shared/logger/index.ts:13`; `src/modules/orders/order.routes.ts:12`.
- ADR-007: `src/modules/orders/order.service.ts:126`; `src/modules/orders/order.service.ts:159`; `src/modules/orders/order.status.ts:3`; `src/modules/orders/order.service.ts:24`.

**Marcadores `[PRECISA DE INFORMAÇÃO: ...]` permitidos (máximo 4 por ADR)**
- ADR-002: comportamento do worker ao reiniciar com eventos em processamento (LAC-10).
- ADR-003: destino da linha da DLQ depois do reprocessamento (LAC-15).
- ADR-004: conteúdo do header de assinatura durante a janela de 24 horas (LAC-04); armazenamento da secret em repouso (LAC-05).
- ADR-007: se a criação do pedido deve gerar evento (LAC-14).

### S7.2 RFC (rfc-creator)

`docs/RFC.md`, RFC-001, Status "Em revisão", entre 2 e 4 páginas (700 a 2300 palavras). O curso não traz template de RFC; a estrutura é a lista do README, na ordem.
Revisores (tabela de metadados): Larissa (Tech Lead), Marcos (Product Manager), Bruno (Engenheiro Pleno, time de Pedidos), Diego (Engenheiro Sênior, time de Plataforma), Sofia (Engenheira de Segurança). Fonte dos papéis: cabeçalho de `TRANSCRICAO.md`.

**Proposta técnica (bullets, sem detalhe do FDD)**: PROP-1 outbox no MySQL na mesma transação do changeStatus (ADR-001, ADR-007); PROP-2 worker em processo separado com polling de 2 s (ADR-002); PROP-3 retry com backoff e DLQ, com replay manual por ADMIN (ADR-003); PROP-4 assinatura HMAC-SHA256 com secret por endpoint (ADR-004); PROP-5 entrega at-least-once com `X-Event-Id` (ADR-005); PROP-6 API REST de configuração e histórico no padrão dos módulos existentes (ADR-006).

**Alternativas consideradas (cada uma com o trade-off do descarte)**: DESC-01, DESC-02, DESC-03, DESC-04 e DESC-05 (juntas), DESC-07, DESC-14.

**Questões em aberto**
- Levantadas e adiadas na reunião: ADIA-02 (rate limiting), ADIA-01 (e-mail), ADIA-05 (vários workers), ADIA-06 (endurecer permissões), ADIA-04 (arquivamento).
- Lacunas identificadas na análise (prefixo "análise:"): LAC-04, LAC-05, LAC-06, LAC-07, LAC-09, LAC-14, LAC-15, LAC-16.

**Impacto**: `changeStatus` ganha uma chamada dentro da transação (CODE-01); novo processo a operar; novas tabelas e uma migration aditiva (CODE-06); nenhuma dependência nova (CODE-22); sem mudança nos endpoints existentes.
**Riscos**: RISK-01, RISK-02, RISK-03, RISK-04, RISK-05.

### S7.3 FDD (fdd-creator)

`docs/FDD.md`: 10 seções do template e a seção 11 do README. Responsável: Vitor Oliveira.

**Modelo de dados (vai na seção 11, linha de `prisma/schema.prisma`)**. Nomes de tabela: `webhook_outbox` e `webhook_dead_letter` vêm de `[09:08] Diego` e `[09:18] Diego`. Os demais nomes são Hipótese (LAC-02, LAC-03, LAC-04, LAC-15).

| Tabela | Colunas | Origem |
| --- | --- | --- |
| `webhook_endpoints` (Hipótese de nome) | `id` UUID; `customer_id`; `url`; `secret`; `previous_secret` e `previous_secret_expires_at` (LAC-04); `statuses` (lista JSON de status); `active`; `created_at`; `updated_at` | `[09:21] Bruno` |
| `webhook_outbox` | `id` UUID, igual ao `event_id`; `webhook_id`; `order_id` (sem chave estrangeira, CODE-03); `event_type`; `payload` JSON (snapshot); `status` (PENDING, PROCESSING, FAILED, DELIVERED); `attempts`; `next_attempt_at` (LAC-02); `created_at`; `updated_at`. Índices: `status`, `created_at` e (`status`, `next_attempt_at`) | `[09:08] Diego`; `[09:25] Diego` |
| `webhook_dead_letter` | `id` UUID; `event_id`; `webhook_id`; `payload`; `failure_reason`; `failed_at`; `replayed_at` (LAC-15) | `[09:18] Diego` |
| `webhook_deliveries` (Hipótese de nome) | `id` UUID; `event_id`; `webhook_id`; `attempt`; `success`; `status_code`; `response_body` truncado em 2 KB; `duration_ms`; `created_at` | `[09:34] Marcos` (LAC-03) |

**Fluxos** (cada item vira bullet; use os rótulos "Criação do evento na outbox", "Processamento pelo worker", "Retry", "DLQ", "Replay")
1. Criação do evento na outbox: dentro de `changeStatus`, depois do histórico (CODE-01), `publishWebhookEvent(tx, order, from, to)` consulta os webhooks ativos do `order.customerId` cujo `statuses` contém o novo status; para cada um monta o payload (RF-13), valida o tamanho (RNF-05), e insere uma linha PENDING com `attempts` 0 e `next_attempt_at` igual ao instante atual. Sem webhook interessado, nada é inserido (RF-05). Qualquer erro propaga e reverte a transação (RF-08).
2. Processamento pelo worker: a cada 2 s busca o lote de linhas PENDING, ou FAILED com `next_attempt_at` vencido, ordenadas por `created_at`; marca PROCESSING; carrega o webhook; assina o corpo; envia `POST` com timeout de 10 s e os 5 headers; resposta 2xx marca DELIVERED e grava a tentativa; qualquer outra marca a tentativa como falha.
3. Retry: na falha, `attempts` aumenta de 1; se o número de retentativas feitas for menor que 5, a linha vira FAILED com `next_attempt_at` igual ao instante atual mais o atraso da posição (1 min, 5 min, 30 min, 2 h, 12 h). O envio inicial mais 5 retentativas dá no máximo 6 requisições (LAC-01).
4. DLQ: quando a 5ª retentativa falha, uma transação insere a linha em `webhook_dead_letter` com payload, motivo e timestamp e apaga a linha da outbox.
5. Replay: `POST` administrativo com ADMIN; em uma transação cria de novo a linha na outbox com o mesmo `id` (mesmo `X-Event-Id`), status PENDING e `attempts` 0, e marca `replayed_at` na DLQ; registra em log o `userId` (RF-12). Replay de linha já reprocessada devolve 409 `WEBHOOK_ALREADY_REPLAYED`.
6. Alternativos: worker reiniciado devolve PROCESSING a PENDING (LAC-10); webhook removido ou inativo no momento do envio descarta o evento com log (LAC-15); payload acima de 64 KB reverte a mudança de status.

**Diagramas**: dois blocos Mermaid na seção 4: (a) sequência da criação do evento e do envio pelo worker; (b) estados da linha da outbox (PENDING, PROCESSING, FAILED, DELIVERED e a saída para a DLQ).

**Contratos** (formato camelCase na API de configuração, LAC-20; envelope de erro `{ "error": { "code", "message", "details" } }` do CODE-09; listas no formato do CODE-24; todos os endpoints exigem `Authorization: Bearer`)

| ID | Contrato | Tipo | Rota | Status | Origem |
| --- | --- | --- | --- | --- | --- |
| CT-01 | Cadastrar webhook | endpoint | `POST /api/v1/webhooks` | 201; 400 `VALIDATION_ERROR` ou `WEBHOOK_INVALID_URL`; 401; 404 `NOT_FOUND` (customer inexistente) | RF-01 |
| CT-02 | Listar webhooks de um customer | endpoint | `GET /api/v1/webhooks?customerId=&page=&pageSize=` | 200; 400; 401 | RF-02 |
| CT-03 | Editar webhook | endpoint | `PATCH /api/v1/webhooks/:id` | 200; 400; 401; 404 `WEBHOOK_NOT_FOUND` | RF-03, RF-05 |
| CT-04 | Remover webhook | endpoint | `DELETE /api/v1/webhooks/:id` | 204; 401; 404 `WEBHOOK_NOT_FOUND` | RF-04 |
| CT-05 | Rotacionar secret | endpoint | `POST /api/v1/webhooks/:id/secret/rotate` (caminho é Hipótese; a reunião definiu só a capacidade, `[09:21] Sofia`) | 200; 401; 404 `WEBHOOK_NOT_FOUND` | RF-07 |
| CT-06 | Histórico de entregas | endpoint | `GET /api/v1/webhooks/:id/deliveries?page=&pageSize=` (`pageSize` máximo 100, CODE-13) | 200; 401; 404 `WEBHOOK_NOT_FOUND` | RF-06 |
| CT-07 | Replay da DLQ | endpoint | `POST /api/v1/admin/webhooks/dead-letter/:id/replay` | 200; 401; 403 `FORBIDDEN`; 404 `WEBHOOK_DEAD_LETTER_NOT_FOUND`; 409 `WEBHOOK_ALREADY_REPLAYED` | RF-12 |
| CT-08 | Entrega do evento ao cliente | endpoint de saída | `POST <url do cliente>` com os 5 headers e o payload de RF-13; sucesso é HTTP 2xx em até 10 s (LAC-19) | 2xx sucesso; demais, falha | RF-09, RF-13, RF-14 |
| CT-09 | Publicação do evento | function | `publishWebhookEvent(tx, order, fromStatus, toStatus): Promise<void>` | lança `WEBHOOK_PAYLOAD_TOO_LARGE` | RF-08, DT-10 |

Exemplos: o corpo de CT-01 tem `url`, `customerId` e `statuses` (valores `PAID`, `PROCESSING`, `SHIPPED`, `DELIVERED`, `CANCELLED`); a resposta 201 devolve `id`, `customerId`, `url`, `statuses`, `active`, `secret`, `createdAt`. A secret só aparece nas respostas de CT-01 e CT-05 (DS-10). A lista de CT-06 traz, por item: `eventId`, `attempt`, `success`, `statusCode`, `responseBody`, `durationMs`, `payload`, `createdAt`.

**Matriz de erros** (colunas: Código, Condição, Status HTTP, Tratamento, Notas)

| Código | Condição | Status | Tratamento | Origem |
| --- | --- | --- | --- | --- |
| `WEBHOOK_NOT_FOUND` | Webhook inexistente | 404 | Subclasse de `AppError` com código próprio (CODE-08) | `[09:28] Bruno` |
| `WEBHOOK_INVALID_URL` | URL malformada ou diferente de `https` | 400 | `BadRequestError` com código próprio (LAC-12) | `[09:23] Sofia`; `[09:28] Bruno` |
| `WEBHOOK_SECRET_REQUIRED` | Webhook sem secret ativa no momento do envio (Hipótese, LAC-13) | interno | A tentativa conta como falha e segue o retry | `[09:28] Bruno` |
| `WEBHOOK_PAYLOAD_TOO_LARGE` | Payload acima de 64 KB na inserção | 422 | `UnprocessableEntityError`; reverte a mudança de status (LAC-11) | `[09:23] Sofia`; `[09:24] Larissa` |
| `WEBHOOK_DEAD_LETTER_NOT_FOUND` | Replay de linha inexistente | 404 | Subclasse de `AppError` | `[09:18] Diego` |
| `WEBHOOK_ALREADY_REPLAYED` | Replay de linha já reprocessada (Hipótese, LAC-15) | 409 | `ConflictError` com código próprio | `[09:18] Diego` |
| `WEBHOOK_DELIVERY_TIMEOUT` | O cliente não respondeu em 10 s | interno | Falha da tentativa; retry | `[09:42] Diego` |
| `WEBHOOK_DELIVERY_FAILED` | Resposta fora de 2xx ou erro de conexão | interno | Falha da tentativa; retry | `[09:15] Diego` |
| `WEBHOOK_RETRIES_EXHAUSTED` | A última retentativa falhou | interno | Move para a DLQ e guarda o código da última falha | `[09:17] Larissa`; `[09:18] Diego` |

Códigos existentes reaproveitados sem alteração: `VALIDATION_ERROR`, `UNAUTHORIZED`, `FORBIDDEN`, `NOT_FOUND`, `INTERNAL_SERVER_ERROR`.

**Resiliência**: timeout 10 s (RNF-04); retries 5 com backoff 1m/5m/30m/2h/12h (RF-10); fallback = DLQ mais replay manual por ADMIN; e-mail adiado (ADIA-01); circuit breaker não previsto (não discutido na reunião); recuperação do worker (LAC-10); término ordenado do lote ao receber SIGTERM (CODE-18).
**Invariantes**: não existe status alterado sem evento (RNF-02); `event_id` é único e estável, inclusive no replay; ordem por `order_id` só com um worker (RNF-08); a secret nunca aparece em logs nem em leituras (DS-10); nenhuma linha de DLQ é apagada.

**Observabilidade (tudo Hipótese, LAC-16)**: Métricas: linhas da outbox por status; idade da linha PENDING mais antiga (mede RNF-01); tamanho da DLQ; tentativas por resultado; duração das chamadas. Emitidas como logs estruturados do Pino a cada ciclo do worker e consultáveis por SQL. Logs: eventos em snake_case como no CODE-17 (`webhook_event_enqueued`, `webhook_delivery_attempted`, `webhook_delivery_succeeded`, `webhook_delivery_failed`, `webhook_moved_to_dead_letter`, `webhook_replay_requested`, `webhook_event_discarded`, `webhook_worker_started`, `webhook_worker_shutdown`); campos `eventId`, `webhookId`, `orderId`, `attempt`, `statusCode`, `durationMs`, `userId`; redação de `*.secret`. Tracing: não há biblioteca de tracing em `package.json`; correlação por `eventId` no worker e `requestId` (CODE-17) na API, sem spans. Dashboards e alertas: nenhum painel nesta fase (ADIA-03 é do cliente); alertas mínimos sugeridos: idade da linha mais antiga acima de 10 s e DLQ com mais de 0 linhas.

**Dependências e compatibilidade (tabela Versão mínima, Componente, Observações; fonte CODE-21, CODE-22, CODE-23)**: Node 20; MySQL 8.0; Prisma 5.22.0; Express 4.21.1; Zod 3.23.8; Pino 9.5.0; uuid 11.0.3; Vitest 2.1.4. Garantias: endpoints existentes e resposta de `changeStatus` não mudam; migration aditiva; nenhuma dependência nova.

**Critérios de aceite técnicos**: ver S8.

**Riscos do FDD**: RISK-01, RISK-02, RISK-03, RISK-05, RISK-06, RISK-07, RISK-08, RISK-09.

**Seção 11 (Integração com o sistema existente)**: tabela Caminho, Situação atual, Integração, com as linhas CODE-01, CODE-02, CODE-03, CODE-04, CODE-05, CODE-06, CODE-08, CODE-09, CODE-10, CODE-11, CODE-12, CODE-14, CODE-15, CODE-16, CODE-18, CODE-19, CODE-20, CODE-21, CODE-25. Arquivos novos aparecem com o sufixo "(arquivo novo)": `src/worker.ts`, `src/modules/webhooks/webhook.controller.ts`, `webhook.service.ts`, `webhook.repository.ts`, `webhook.routes.ts`, `webhook.schemas.ts`, `webhook.publisher.ts` (função `publishWebhookEvent`), `webhook.worker.ts` ou `webhook.processor.ts`.

### S7.4 PRD (prd-creator)

`docs/PRD.md`, produto "Order Management System (OMS)", feature "Sistema de Webhooks de Notificação de Pedidos".

**Resumo**: três clientes B2B (Atlas Comercial, MaxDistribuição e Nova Cargo) pedem notificação em tempo real quando o status dos pedidos muda; hoje consultam `GET /orders` repetidamente (`[09:00] Marcos`). A Atlas pode migrar para um concorrente se a entrega passar do fim do trimestre (`[09:00] Marcos`). A feature envia webhooks de saída assinados, com retry e reprocessamento manual.

**Público-alvo**: clientes B2B Atlas Comercial, MaxDistribuição e Nova Cargo (`[09:00] Marcos`); usuários do nosso sistema que representam o cliente e cadastram webhooks pela API (`[09:32] Marcos`); administradores (role ADMIN) que reprocessam eventos (`[09:36] Sofia`); PM que documenta a integração no portal do desenvolvedor (`[09:26] Marcos`).

**Cenários de uso chave**: receber aviso quando o pedido vira SHIPPED e DELIVERED (`[09:33] Marcos`); cliente com manutenção planejada de 2 horas recebe os eventos depois (`[09:16] Diego`); cadastrar um webhook e receber a secret; rotacionar a secret sem parar a integração (`[09:21] Sofia`); consultar o histórico de entregas (`[09:34] Marcos`); ADMIN reprocessa evento da DLQ (`[09:18] Diego`).

**Onde será implantada**: sistema existente. A aplicação Node.js com Express, Prisma e MySQL ganha um módulo de webhooks e um processo worker (CODE-15, CODE-23).

**Problemas priorizados**: (1) integração lenta e cara porque os clientes consultam `GET /orders` de tempos em tempos, prioridade alta (`[09:00] Marcos`); (2) risco de perder a Atlas, prioridade alta (`[09:00] Marcos`); (3) a aplicação não tem nenhum mecanismo de notificação externa, prioridade alta (README, Contexto).

**Objetivos e métricas (tabela Objetivo, Métrica, Meta)**

| Objetivo | Métrica | Meta | Origem |
| --- | --- | --- | --- |
| Notificar o cliente em tempo real | Tempo entre a criação da linha na outbox e o início do primeiro envio (Hipótese de ponto de medição, LAC-17) | Menor que 10 segundos | `[09:02] Marcos` |
| Nunca perder um evento | Mudanças de status confirmadas sem evento registrado | 0 (100% com evento na mesma transação) | `[09:40] Bruno` |
| Cobrir a indisponibilidade do cliente | Janela total de retentativas antes da DLQ | Cerca de 14,6 horas, em 5 retentativas | `[09:17] Diego` |
| Entregar no prazo | Sprints até o deploy | 3 sprints, com 2 dias úteis de revisão de segurança | `[09:46] Larissa`; `[09:46] Sofia` |

**Escopo**: Incluso = RF-01 a RF-15 (resumidos), mais o worker e a DLQ. Fora de escopo = ADIA-01 a ADIA-07 e os descartados relevantes ao produto (DESC-01, DESC-07, DESC-10).

**Requisitos funcionais**: os 12 blocos FR do agrupamento da S2, com fluxo principal, fluxos alternativos e exceções, erros previstos e prioridade. Nomes: FR-01 Cadastrar webhook; FR-02 Listar webhooks de um cliente; FR-03 Editar webhook; FR-04 Remover webhook; FR-05 Filtrar eventos por status; FR-06 Consultar o histórico de entregas; FR-07 Rotacionar a secret; FR-08 Registrar o evento na mudança de status; FR-09 Entregar o evento assinado; FR-10 Repetir a entrega com espera crescente; FR-11 Isolar eventos que esgotaram as tentativas; FR-12 Reprocessar manualmente um evento isolado.

**Requisitos não funcionais**: RNF-01 a RNF-13 distribuídos nos 8 rótulos do template. Disponibilidade: "Hipótese: a reunião não definiu meta de uptime" mais RNF-09 e RNF-10. Compliance: auditoria do replay por log (DS-07); nenhum requisito regulatório foi discutido. Acessibilidade no frontend consumidor: não se aplica, não há frontend nesta fase (ADIA-03).

**Arquitetura e abordagem** (nível de produto, sem nomes de tabela): Abordagem = outbox no banco existente, worker separado em polling, assinatura HMAC, retry com DLQ. Componentes = módulo de webhooks na API; tabela de outbox no MySQL; processo worker; DLQ. Integrações = fluxo de mudança de status de pedidos; endpoints HTTPS dos clientes.

**Decisões e trade-offs**: as 7 decisões dos ADRs, cada uma com Justificativa e Trade-off (S7.1).

**Dependências**
- organizacional: Revisão de segurança (`[09:46] Sofia`), 2 dias úteis antes do deploy, no fim da sprint 3.
- organizacional: Documentação no portal do desenvolvedor (`[09:26] Marcos`; `[09:40] Marcos`), com ênfase no at-least-once e na deduplicação por `X-Event-Id`.
- organizacional: Confirmação do prazo com a Atlas (`[09:47] Marcos`).
- técnica: MySQL e Prisma existentes e uma migration nova (CODE-06, CODE-23).
- técnica: Usuários do sistema que representam o cliente (`[09:32] Marcos`).
- externa: Endpoints `https` dos clientes (`[09:23] Sofia`).

**Riscos do PRD**: RISK-01, RISK-02, RISK-03, RISK-04, RISK-05, RISK-07.

**Critérios de aceitação**: ver S8.

**Testes e validação**: tipos obrigatórios = unitários (assinatura HMAC, tabela de backoff, filtro de status, montagem do payload); integração com Vitest e supertest sobre MySQL (CODE-25: atomicidade do `changeStatus`, CRUD, role ADMIN no replay); worker contra servidor HTTP simulado (sucesso, timeout de 10 s, retry, DLQ); segurança (403 para OPERATOR no replay, secret ausente nas leituras, redação em logs). Estratégia de validação = suíte automatizada no padrão atual de `tests/`; revisão de segurança de 2 dias úteis (`[09:46] Sofia`); roteiro manual com um cliente simulado para medir o limite de 10 s.

### S7.5 Riscos (avaliação do autor para probabilidade e impacto; a origem de cada risco é citada)

| ID | Risco | Probabilidade | Impacto | Mitigação | Contingência | Origem |
| --- | --- | --- | --- | --- | --- | --- |
| RISK-01 | Cliente indisponível por mais de 14,6 horas e o evento termina na DLQ sem aviso (e-mail adiado) | média | O cliente deixa de receber eventos até o replay manual | Histórico de entregas; DLQ preserva payload e motivo; replay por ADMIN | ADMIN reprocessa a DLQ quando o cliente voltar | `[09:17] Marcos`; `[09:37] Larissa` |
| RISK-02 | Ordem dos eventos não garantida com mais de um worker ou com evento em retry (LAC-09) | média | O cliente recebe estados fora de sequência | Um único worker; limitação documentada; o payload traz `from_status` e `to_status` | Particionar por `order_id` ou usar lock pessimista (ADIA-05) | `[09:12] Diego`; `[09:13] Larissa` |
| RISK-03 | Vazamento de secret, no cliente ou nos nossos logs | média | Terceiros forjam notificações para o endpoint | Secret por endpoint; rotação com 24 h; redação de `*.secret`; secret só nas respostas de criação e rotação | Rotacionar a secret do endpoint afetado | `[09:22] Diego` |
| RISK-04 | Prazo de 3 sprints com revisão de segurança no fim | média | A Atlas pode migrar para o concorrente | Sequência de sprints definida por Larissa; revisão agendada com antecedência | Marcos renegocia a data com a Atlas | `[09:00] Marcos`; `[09:46] Larissa` |
| RISK-05 | Entrega duplicada quebra o sistema de um cliente que não deduplica | alta | Pedido processado duas vezes no cliente | `X-Event-Id` em todo envio; documentação destacada no portal | Suporte orienta o cliente a deduplicar por `X-Event-Id` | `[09:25] Sofia`; `[09:26] Marcos` |
| RISK-06 | Worker parado: eventos se acumulam e passam de 10 s | baixa | Quebra do RNF-01 | Processo separado da API; alerta pela idade da linha mais antiga (Hipótese) | Reiniciar o worker; as linhas pendentes são enviadas em ordem | `[09:11] Diego` |
| RISK-07 | Qualquer role autenticada gerencia webhooks de qualquer customer (LAC-08) | média | Alteração ou leitura indevida da configuração de outro cliente | Registrado como risco aceito; revisão de segurança | Endurecer permissões (ADIA-06) | `[09:37] Sofia` |
| RISK-08 | Cadastro de URL que aponta para a rede interna (LAC-07) | baixa | O servidor faz requisições a serviços internos | Hipótese: não seguir redirecionamentos; análise da Sofia | Desativar o webhook (`active` falso) | `[09:23] Sofia` |
| RISK-09 | Falha na inserção da outbox reverte a mudança de status do pedido | baixa | Pedido não muda de status enquanto a outbox falhar | É o comportamento decidido: nunca status sem evento; testes de atomicidade | Corrigir a causa na outbox; o pedido pode repetir a mudança | `[09:40] Bruno` |

## S8. Critérios de aceite

**PRD (checklist de produto)**
1. Quando um pedido muda de status e o customer tem webhook ativo que assina aquele status, existe um evento registrado na mesma transação; se a transação falha, nenhum evento existe.
2. Com o worker em execução e o cliente respondendo com sucesso, o primeiro envio ocorre em menos de 10 segundos depois do registro do evento.
3. Falha ou ausência de resposta em 10 segundos agenda nova tentativa com esperas de 1 minuto, 5 minutos, 30 minutos, 2 horas e 12 horas.
4. Depois da última retentativa com falha, o evento está na DLQ com payload, motivo e timestamp, e não está mais na outbox.
5. Todo envio traz os headers `X-Event-Id`, `X-Signature`, `X-Timestamp`, `X-Webhook-Id` e `Content-Type: application/json`.
6. A assinatura confere com o HMAC-SHA256 do corpo calculado com a secret do endpoint.
7. A rotação de secret mantém a secret anterior válida por 24 horas.
8. URL `http` é recusada e payload acima de 64 KB gera erro.
9. O replay por ADMIN recoloca o evento como pendente e registra em log o usuário; usuário OPERATOR recebe 403.
10. O histórico de entregas devolve até 100 envios com sucesso ou falha, payload, resposta e tempo de resposta.
11. Mudança de status de pedido de customer sem webhook funciona como antes.

**FDD (critérios técnicos, com medida)**
1. Teste de atomicidade: forçar erro na inserção da outbox dentro de `changeStatus` deixa o pedido no status anterior e sem linha no histórico.
2. Teste de filtro: para um customer com dois webhooks (um assina SHIPPED, outro não), a mudança para SHIPPED cria exatamente 1 linha na outbox.
3. Teste de assinatura: o HMAC-SHA256 calculado pelo teste com a secret do endpoint é igual ao valor de `X-Signature`.
4. Teste de backoff: as cinco esperas são 60 s, 300 s, 1.800 s, 7.200 s e 43.200 s, e a 6ª requisição falha leva à DLQ.
5. Teste de timeout: um servidor simulado que responde depois de 10 s gera falha da tentativa.
6. Teste de replay: ADMIN recebe 200 e a linha volta a PENDING com o mesmo `event_id`; OPERATOR recebe 403; segundo replay recebe 409.
7. Teste de payload: um payload de 64 KB mais 1 byte lança `WEBHOOK_PAYLOAD_TOO_LARGE` e reverte a mudança de status.
8. Teste de leitura: `GET` de webhook nunca devolve a secret; criação e rotação devolvem.
9. Teste de log: a secret não aparece em nenhuma linha de log produzida pelo módulo.
10. Teste de latência: com o worker ligado e cliente simulado respondendo em menos de 1 s, o primeiro envio ocorre em menos de 10 s.
11. Teste de regressão: os testes existentes de `tests/` continuam passando.
12. Teste de ordem: com um worker, 3 mudanças de status do mesmo pedido chegam em ordem de `created_at` quando nenhum envio falha.

## S9. Regras do Tracker

IDs seguem o enumerador de `tracker-creator/scripts/enumerar_itens.py`. Cada linha cita uma única Fonte: `TRANSCRICAO` (com `[hh:mm] Nome`) ou `CODIGO` (com caminho existente). Itens de classe B apontam para o item A de origem (se a origem é a reunião) ou para o arquivo (se a origem é o código). Itens de classe C e "Hipótese:" apontam para a fala que originou a lacuna e têm Tipo "Hipótese".
