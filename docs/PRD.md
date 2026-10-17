### PRD: Order Management System (OMS) Sistema de Webhooks de Notificação de Pedidos

Versão: 1.0
Data: 2026-10-17
Responsável: Vitor Oliveira

---

### Resumo

Três clientes B2B (Atlas Comercial, MaxDistribuição e Nova Cargo) pediram para ser notificados em tempo real quando o status dos pedidos deles muda. Hoje eles consultam a listagem de pedidos de tempos em tempos, o que deixa a integração lenta e cara, e a Atlas pode migrar para um concorrente se a entrega passar do fim do trimestre.

A feature envia webhooks de saída: quando o status de um pedido muda, o sistema registra um evento e o entrega ao endereço HTTPS do cliente em menos de 10 segundos, assinado para o cliente validar a origem. Falhas são repetidas com espera crescente, eventos que esgotam as tentativas ficam isolados para reprocessamento manual por um administrador, e o cliente gerencia seus webhooks e consulta o histórico de entregas pela API.

---

### Contexto e problema

Público-alvo
- Clientes B2B Atlas Comercial, MaxDistribuição e Nova Cargo, que querem ser avisados quando o status dos pedidos muda.
- Usuários do sistema que representam o cliente e cadastram webhooks pela API.
- Administradores (papel ADMIN), que reprocessam eventos que falharam.
- O PM, que documenta a integração no portal do desenvolvedor.

Cenários de uso chave
- Um cliente quer saber apenas quando o pedido vira SHIPPED ou DELIVERED e cadastra um webhook com esses dois status.
- Um cliente entra em manutenção planejada de 2 horas e recebe os eventos depois, pelas novas tentativas.
- Um cliente troca a secret do webhook sem parar a integração.
- Um cliente consulta o histórico de entregas para ver o que foi enviado e como o endereço dele respondeu.
- Um administrador reprocessa um evento que esgotou as tentativas.

Onde essa feature será implantada
- Em sistema existente: a aplicação Node.js do Order Management System, com Express, Prisma e MySQL, ganha um módulo de webhooks e um processo separado que envia os eventos.

Problemas priorizados
- Integração lenta e cara, porque os clientes consultam a listagem de pedidos de tempos em tempos. Impacto: os 3 clientes pedem tempo real, abaixo de 10 segundos. Prioridade alta.
- Risco comercial: a Atlas pode migrar para um concorrente se a entrega passar do fim do trimestre. Prioridade alta.
- A aplicação não tem nenhum mecanismo de notificação externa, de evento, de fila ou de webhook. Prioridade alta.

---

### Objetivos e métricas

| Objetivo | Métrica | Meta |
| --- | --- | --- |
| Notificar o cliente em tempo real | Tempo entre o registro do evento e o início do primeiro envio. Hipótese: este é o ponto de medição, porque a reunião não o definiu | Menor que 10 segundos |
| Nunca perder um evento | Mudanças de status confirmadas sem evento registrado | 0 mudanças sem evento |
| Cobrir a indisponibilidade do cliente | Janela total de retentativas antes de isolar o evento | Cerca de 14,6 horas, em 5 retentativas (Hipótese: depois do envio inicial) |
| Entregar no prazo | Sprints até o deploy | 3 sprints, incluindo pelo menos 2 dias úteis de revisão de segurança |

---

### Escopo

Incluso
- Cadastro, listagem, edição e remoção de webhooks, com a lista de status que cada webhook quer receber.
- Registro do evento na mesma transação da mudança de status do pedido, com o conteúdo gravado no instante da mudança.
- Envio por um processo separado da API, com assinatura HMAC-SHA256 e cinco headers.
- Repetição da entrega com espera crescente, isolamento dos eventos que esgotam as tentativas e reprocessamento manual por administrador.
- Rotação de secret pela API, com a secret anterior válida por 24 horas.
- Histórico de entregas por webhook.

Fora de escopo
- Aviso por e-mail ao cliente quando o webhook falha. Adiado para a próxima fase.
- Limitação da taxa de envio por cliente. A decisão é observar e decidir depois.
- Dashboard visual para o cliente. É projeto separado do time de frontend.
- Arquivamento das linhas entregues depois de cerca de 30 dias.
- Mais de um worker e garantia de ordem global.
- Webhook de entrada, em que o cliente enviaria eventos ao sistema.
- Endurecimento das permissões do cadastro de webhooks, adiado.
- Itens do pedido no conteúdo do evento. Descartado: o cliente consulta o pedido depois.
- Entrega exatamente uma vez. Descartada: a garantia é ao menos uma vez.
- Chamada ao cliente dentro da mudança de status do pedido. Descartada.

---

### Requisitos funcionais

#### FR-01 Cadastrar webhook
O usuário que representa um cliente cadastra o endereço HTTPS que receberá as notificações, escolhe os status que quer receber e recebe uma secret gerada pelo sistema.

**Fluxo principal**
- O usuário autenticado informa o identificador do cliente, o endereço HTTPS e a lista de status desejados.
- O sistema valida os dados e confirma que o cliente existe.
- O sistema grava o webhook como ativo e gera uma secret única para ele.
- O sistema devolve o cadastro com a secret, que aparece somente nessa resposta.

**Fluxos alternativos e exceções**
- O identificador do cliente vai no corpo da requisição, e não no token de acesso, porque o token é de um usuário do sistema.
- Um mesmo cliente pode ter vários webhooks, cada um com a sua secret.

**Erros previstos**
- Endereço malformado ou diferente de HTTPS.
- Lista de status com valor inexistente.
- Cliente inexistente.
- Token de acesso ausente ou inválido.

**Prioridade:** alta

---

#### FR-02 Listar webhooks de um cliente
O usuário consulta os webhooks cadastrados de um cliente.

**Fluxo principal**
- O usuário informa o identificador do cliente e a página desejada.
- O sistema devolve os webhooks do cliente com endereço, status assinados e situação ativa, sem a secret.

**Fluxos alternativos e exceções**
- Um cliente sem webhooks recebe uma lista vazia.
- Qualquer papel autenticado pode consultar, por decisão da reunião para esta fase.

**Erros previstos**
- Identificador do cliente ausente ou inválido.
- Token de acesso ausente ou inválido.

**Prioridade:** alta

---

#### FR-03 Editar webhook
O usuário altera o endereço, a lista de status ou a situação ativa de um webhook.

**Fluxo principal**
- O usuário informa o webhook e os campos que quer alterar.
- O sistema valida os campos e grava a alteração.
- O sistema devolve o cadastro atualizado, sem a secret.

**Fluxos alternativos e exceções**
- Desativar um webhook suspende os envios sem apagar o cadastro.
- A edição não troca a secret. A troca tem operação própria (FR-07).

**Erros previstos**
- Webhook inexistente.
- Endereço malformado ou diferente de HTTPS.
- Token de acesso ausente ou inválido.

**Prioridade:** alta

---

#### FR-04 Remover webhook
O usuário remove um webhook que o cliente não quer mais.

**Fluxo principal**
- O usuário informa o webhook a remover.
- O sistema remove o cadastro e confirma sem devolver conteúdo.

**Fluxos alternativos e exceções**
- Hipótese: os eventos pendentes do webhook removido são descartados com registro em log, porque a reunião não definiu esse caso.
- Para parar os envios sem perder o cadastro, o usuário desativa o webhook (FR-03).

**Erros previstos**
- Webhook inexistente.
- Token de acesso ausente ou inválido.

**Prioridade:** alta

---

#### FR-05 Filtrar eventos por status
Cada webhook recebe somente os eventos dos status que escolheu. O filtro é aplicado quando o evento é registrado: se nenhum webhook do cliente quer o status, nada é registrado.

**Fluxo principal**
- O usuário escolhe os status ao cadastrar ou editar o webhook.
- Quando o status de um pedido muda, o sistema seleciona os webhooks ativos do cliente cuja lista contém o novo status.
- O sistema registra um evento para cada webhook selecionado.

**Fluxos alternativos e exceções**
- Webhook inativo não recebe eventos.
- Quando nenhum webhook do cliente quer o status, a mudança de status acontece como hoje, sem evento.
- Hipótese: o status inicial PENDING não pode ser escolhido, porque nenhuma mudança de status leva a ele.

**Erros previstos**
- Lista de status com valor inexistente. Hipótese: lista com PENDING.

**Prioridade:** media

---

#### FR-06 Consultar o histórico de entregas
O cliente vê os envios feitos para um webhook, com sucesso ou falha, o conteúdo enviado, a resposta recebida e o tempo de resposta.

**Fluxo principal**
- O usuário informa o webhook e a página desejada.
- O sistema devolve os envios, do mais recente para o mais antigo, em páginas de até 100 registros.
- Cada registro traz o resultado, o conteúdo enviado, a resposta do cliente e o tempo de resposta.

**Fluxos alternativos e exceções**
- Um webhook sem envios recebe uma lista vazia.
- Hipótese: a resposta do cliente é guardada truncada em 2 KB.

**Erros previstos**
- Webhook inexistente.
- Token de acesso ausente ou inválido.

**Prioridade:** media

---

#### FR-07 Rotacionar a secret
O cliente pede uma nova secret sem parar a integração. A secret anterior continua válida por 24 horas.

**Fluxo principal**
- O usuário pede a rotação da secret de um webhook.
- O sistema gera uma nova secret e a devolve somente nessa resposta.
- O sistema mantém a secret anterior válida por 24 horas. Hipótese: a resposta informa quando ela expira.
- Depois de 24 horas, só a secret nova vale.

**Fluxos alternativos e exceções**
- Durante as 24 horas, o cliente pode validar a assinatura com qualquer uma das duas secrets.
- Hipótese: durante esse período o header de assinatura traz as duas assinaturas, a da secret nova primeiro, porque a reunião não definiu o formato.

**Erros previstos**
- Webhook inexistente.
- Token de acesso ausente ou inválido.

**Prioridade:** alta

---

#### FR-08 Registrar o evento na mudança de status
Quando o status de um pedido muda, o sistema registra o evento de notificação na mesma transação da mudança, com o conteúdo do pedido gravado naquele instante.

**Fluxo principal**
- Um usuário muda o status do pedido.
- O sistema valida a transição, atualiza o pedido e grava o histórico, como hoje.
- Na mesma transação, o sistema registra um evento para cada webhook interessado, com os dados do pedido no instante da mudança.
- O sistema confirma tudo junto.

**Fluxos alternativos e exceções**
- Se o registro do evento falhar, a mudança de status é desfeita.
- A mudança de status de um pedido sem webhook interessado segue como hoje.
- Hipótese: a criação de pedido não gera evento, porque a reunião integrou só a mudança de status. A confirmação fica com o PM.

**Erros previstos**
- Conteúdo do evento acima de 64 KB: o sistema retorna erro. Hipótese: a mudança de status também é desfeita, porque o registro do evento falha dentro da mesma transação.
- Falha do banco ao gravar o evento: a mudança de status é desfeita.

**Prioridade:** alta

---

#### FR-09 Entregar o evento assinado ao cliente
Um processo separado da API envia cada evento ao endereço do cliente com assinatura e identificadores.

**Fluxo principal**
- A cada 2 segundos o processo busca, em lote pequeno, os eventos pendentes mais antigos.
- Para cada evento, monta o envio com o conteúdo do evento e cinco headers: identificador do evento, assinatura, instante do envio, identificador do webhook e tipo do conteúdo.
- O conteúdo traz o identificador do evento, o tipo "order.status_changed", a data e a hora, os dados básicos do pedido e os status de origem e de destino, sem os itens do pedido.
- Envia ao endereço do cliente com limite de 10 segundos para a resposta.
- Uma resposta de sucesso marca o evento como entregue e registra a tentativa.

**Fluxos alternativos e exceções**
- A entrega é ao menos uma vez: o cliente pode receber o mesmo evento mais de uma vez e deduplica pelo identificador do evento.
- Os eventos do mesmo pedido saem na ordem de criação enquanto houver um único processo de envio e nenhum deles estiver em espera de nova tentativa (FR-10).
- Hipótese: uma resposta de sucesso é qualquer resposta HTTP 2xx dentro de 10 segundos.

**Erros previstos**
- Sem resposta em 10 segundos, resposta de falha ou erro de conexão contam como falha da tentativa (FR-10).

**Prioridade:** alta

---

#### FR-10 Repetir a entrega com espera crescente
Quando o envio falha, o sistema tenta de novo com esperas de 1 minuto, 5 minutos, 30 minutos, 2 horas e 12 horas.

**Fluxo principal**
- O envio falha.
- O sistema registra a tentativa e agenda a próxima.
- O sistema repete o envio depois da espera.
- Um envio com sucesso marca o evento como entregue.

**Fluxos alternativos e exceções**
- Hipótese: as 5 tentativas decididas são 5 retentativas depois do envio inicial, no máximo 6 requisições por ciclo de entrega, em uma janela de cerca de 14,6 horas.
- Um evento em espera pode ser ultrapassado pelo evento seguinte do mesmo pedido.

**Erros previstos**
- A quinta retentativa falha: o evento é isolado (FR-11).

**Prioridade:** alta

---

#### FR-11 Isolar eventos que esgotaram as tentativas
Eventos que falham em todas as tentativas vão para uma área separada, a DLQ, que guarda o conteúdo, o motivo da falha e a data.

**Fluxo principal**
- A quinta retentativa falha.
- O sistema grava na DLQ o conteúdo, o motivo da falha e a data.
- O sistema remove o evento da fila ativa.

**Fluxos alternativos e exceções**
- Os eventos da DLQ ficam como evidência para depuração e para reprocessamento.
- O cliente não é avisado por e-mail nesta fase.

**Erros previstos**
- Falha do banco ao mover o evento: a operação é desfeita e o evento continua na fila ativa.

**Prioridade:** alta

---

#### FR-12 Reprocessar manualmente um evento isolado
Um administrador devolve um evento da DLQ para a fila de envio, e o sistema registra quem executou.

**Fluxo principal**
- O administrador informa o evento da DLQ.
- O sistema recoloca o evento na fila como pendente.
- O sistema registra em log o usuário que executou.
- O processo de envio entrega o evento no próximo ciclo.

**Fluxos alternativos e exceções**
- Hipótese: o evento volta com o mesmo identificador, para o cliente reconhecer a repetição.
- Hipótese: cada evento da DLQ pode ser reprocessado uma vez, porque a reunião não definiu o que acontece com ele depois.

**Erros previstos**
- Usuário sem o papel ADMIN: acesso negado.
- Evento inexistente na DLQ.
- Hipótese: evento já reprocessado.

**Prioridade:** alta

---

### Requisitos não funcionais

Performance
- Notificar o cliente em menos de 10 segundos depois da mudança de status. A leitura a cada 2 segundos acrescenta no máximo 2 segundos. Hipótese: a meta vale quando nenhum cliente lento anterior atrasa o lote.
- Limite de 10 segundos por chamada ao endereço do cliente.
- Conteúdo do evento de até 64 KB. Acima disso, erro.

Disponibilidade
- Hipótese: a reunião não definiu meta de disponibilidade, e este documento não propõe um número.
- O processo de envio roda separado da API, então reiniciar a API não interrompe os envios.
- Um cliente fora do ar recebe novas tentativas por cerca de 14,6 horas antes de o evento ser isolado.

Segurança e autorização
- Assinatura HMAC-SHA256 do corpo de cada envio, com secret única por endpoint e rotação com 24 horas de sobreposição.
- Endereço do webhook obrigatoriamente HTTPS.
- Cadastro, listagem, edição e remoção abertos a qualquer papel autenticado, por enquanto.
- Reprocessamento restrito ao papel ADMIN, com registro em log de quem executou.
- Hipótese: a secret não aparece em logs nem em respostas de leitura, porque a reunião mandou devolvê-la só na criação e registrou o vazamento de uma secret em log de um cliente.
- Revisão de segurança de pelo menos 2 dias úteis antes do deploy.

Observabilidade
- Logs estruturados com o Pino, o logger já usado no projeto.
- Histórico de entregas por webhook, com resultado, conteúdo, resposta e tempo de resposta.
- Hipótese: métricas e rastreamento não foram discutidos na reunião e ficam como logs estruturados e consultas ao banco, sem biblioteca nova.

Confiabilidade e integridade de dados
- O evento e a mudança de status são confirmados ou desfeitos juntos.
- Entrega ao menos uma vez, com identificador único por evento.
- Ordem de entrega garantida por pedido enquanto houver um único processo de envio, sem garantia de ordem global. Limitação identificada na análise: um evento em espera de nova tentativa pode ser ultrapassado pelo seguinte do mesmo pedido.
- O conteúdo do evento é um retrato do pedido no instante da mudança.

Compatibilidade e portabilidade
- Reuso do MySQL, do Prisma, do Pino, do tratamento de erros, dos esquemas de validação e dos identificadores UUID existentes.
- API REST JSON versionada em /api/v1, com códigos de erro de prefixo WEBHOOK_.
- Nenhuma infraestrutura nova. Hipótese: nenhuma dependência npm nova, porque os recursos nativos do Node 20 bastam.

Compliance
- Auditoria do reprocessamento por log com o usuário que executou. A reunião não discutiu requisito regulatório.

Acessibilidade no frontend consumidor
- Não se aplica nesta fase: não há frontend, apenas endpoints, porque o painel visual é projeto separado.

---

### Arquitetura e abordagem

Abordagem
- O evento é gravado em uma outbox, uma tabela no banco existente, na mesma transação da mudança de status. Um processo separado consulta a outbox a cada 2 segundos e envia o evento ao cliente. A DLQ (dead letter queue) é a tabela dos eventos que esgotaram as tentativas. Ver ADR-001, ADR-002 e ADR-007.

Componentes
- Módulo de webhooks na API, no mesmo formato dos módulos existentes.
- Tabela de outbox e tabela da DLQ no MySQL.
- Processo de envio separado da API.

Integrações
- Fluxo de mudança de status de pedidos, que passa a registrar o evento na mesma transação.
- Endereços HTTPS dos clientes, que recebem as notificações.

### Decisões e trade-offs

#### Decisão: Outbox no MySQL gravada na mesma transação da mudança de status
- **Justificativa:** garante que o evento e a mudança de status são confirmados ou desfeitos juntos, sem infraestrutura nova para um time pequeno (ADR-001 e ADR-007).
- **Trade-off:** o banco relacional passa a fazer o papel de fila, com menos vazão que um serviço dedicado, e a transação do pedido fica mais longa.

#### Decisão: Processo de envio separado da API, com consulta a cada 2 segundos
- **Justificativa:** reiniciar a API não perde o envio, e o atraso adicional máximo de 2 segundos cabe no limite de 10 segundos (ADR-002).
- **Trade-off:** aceita-se até 2 segundos de atraso e a escala fica limitada a um processo, porque mais de um perde a garantia de ordem.

#### Decisão: Cinco retentativas com espera crescente e DLQ em tabela separada
- **Justificativa:** cobre cerca de 14,6 horas de indisponibilidade do cliente, não deixa evento pendurado e guarda a evidência para reprocessamento (ADR-003). Hipótese: as 5 tentativas decididas são 5 retentativas depois do envio inicial.
- **Trade-off:** um cliente fora do ar por mais tempo só recebe o evento depois de reprocessamento manual, e o aviso por e-mail ficou fora desta fase.

#### Decisão: Assinatura HMAC-SHA256 com secret por endpoint e rotação de 24 horas
- **Justificativa:** o cliente valida origem e integridade, e o vazamento de uma secret afeta um endpoint só (ADR-004).
- **Trade-off:** o sistema assume a gestão do ciclo de vida das secrets, e o header com o instante do envio não é assinado.

#### Decisão: Entrega ao menos uma vez com identificador de evento
- **Justificativa:** nenhum evento se perde por falha de confirmação, e a solução é a mesma de provedores como Stripe e GitHub (ADR-005).
- **Trade-off:** o cliente precisa deduplicar pelo identificador, e o PM documenta isso no portal do desenvolvedor.

#### Decisão: Reuso dos padrões existentes do projeto
- **Justificativa:** o módulo novo fica igual aos demais e aproveita o tratamento de erros, o log e o controle de acesso que já funcionam (ADR-006).
- **Trade-off:** o módulo herda limitações atuais do código, como a ausência de isolamento por cliente no token de acesso.

#### Decisão: Função de publicação que recebe a transação corrente
- **Justificativa:** garante a atomicidade sem acoplar o serviço de pedidos ao repositório inteiro de webhooks (ADR-007).
- **Trade-off:** o módulo de pedidos passa a depender do módulo de webhooks.

---

### Dependências

#### organizacional: Revisão de segurança antes do deploy
A Sofia, engenheira de segurança, precisa de pelo menos 2 dias úteis para revisar o código de segurança, com foco na assinatura HMAC e na geração de secret, antes do deploy. A revisão fica no fim da terceira sprint.

#### organizacional: Documentação no portal do desenvolvedor
O PM Marcos documenta no portal como integrar pela API e destaca que a entrega é ao menos uma vez e que o cliente deduplica pelo identificador do evento.

#### organizacional: Confirmação do prazo com a Atlas
O PM Marcos confirma com a Atlas a entrega prevista para o fim de novembro, dentro de 3 sprints.

#### técnica: MySQL, Prisma e uma nova migration
A feature usa o MySQL e o Prisma existentes e exige uma migration nova com as tabelas do módulo.

#### técnica: Usuários do sistema que representam clientes
O cadastro de webhooks usa os usuários atuais do sistema, autenticados por token. O token não identifica o cliente, por isso o identificador do cliente vai no corpo da requisição.

#### externa: Endereços HTTPS dos clientes
Cada cliente precisa manter um endereço HTTPS que responda em até 10 segundos, valide a assinatura e deduplique pelo identificador do evento.

---

### Riscos e mitigação

#### Cliente fora do ar por mais de 14,6 horas fica sem eventos
- **Probabilidade:** media
- **Impacto:** o cliente deixa de receber eventos até o reprocessamento manual e não é avisado da falha.
- **Mitigação:**
  - Histórico de entregas por webhook.
  - DLQ com conteúdo, motivo e data.
  - Reprocessamento por administrador.
- **Plano de contingência:** o administrador reprocessa a DLQ quando o cliente voltar.

#### Ordem dos eventos fora de sequência
- **Probabilidade:** media
- **Impacto:** o cliente recebe estados de um pedido fora da sequência, quando um evento está em nova tentativa ou quando há mais de um processo de envio.
- **Mitigação:**
  - Um único processo de envio.
  - Evento com o status de origem e o de destino.
  - Limitação documentada para os clientes no portal.
- **Plano de contingência:** particionar por pedido ou usar lock pessimista, hoje adiado.

#### Vazamento de secret
- **Probabilidade:** media
- **Impacto:** terceiros forjam notificações para o endpoint afetado.
- **Mitigação:**
  - Secret única por endpoint.
  - Rotação com 24 horas de sobreposição.
  - Hipótese: secret fora de logs e de respostas de leitura.
- **Plano de contingência:** rotacionar a secret do endpoint afetado.

#### Prazo de 3 sprints pode não ser cumprido
- **Probabilidade:** media
- **Impacto:** a Atlas pode migrar para o concorrente.
- **Mitigação:**
  - Sequência de sprints definida pela tech lead.
  - Revisão de segurança agendada com antecedência.
- **Plano de contingência:** o PM renegocia a data com a Atlas.

#### Cliente que não deduplica processa o mesmo pedido duas vezes
- **Probabilidade:** alta
- **Impacto:** pedido processado em duplicidade no sistema do cliente.
- **Mitigação:**
  - Identificador de evento em todo envio.
  - Documentação destacada no portal do desenvolvedor.
- **Plano de contingência:** o suporte orienta o cliente a deduplicar pelo identificador do evento.

#### Qualquer usuário autenticado acessa os webhooks de qualquer cliente
- **Probabilidade:** media
- **Impacto:** alteração ou leitura indevida da configuração e do histórico de outro cliente.
- **Mitigação:**
  - Risco aceito pela reunião para esta fase.
  - Revisão de segurança antes do deploy.
- **Plano de contingência:** endurecer as permissões do cadastro de webhooks, hoje adiado.

#### Cliente lento atrasa os eventos seguintes do mesmo lote
- **Probabilidade:** media
- **Impacto:** eventos de outros clientes saem depois dos 10 segundos esperados, porque o processo de envio trata um evento por vez e cada chamada pode levar até 10 segundos.
- **Mitigação:**
  - Lote pequeno de eventos por ciclo.
  - Limite de 10 segundos por chamada, que limita o atraso por evento.
- **Plano de contingência:** processar em paralelo os eventos de pedidos diferentes, mantendo a ordem por pedido, hoje fora do escopo por causa do processo de envio único.

---

### Critérios de aceitação
Checklist objetivo que define se a feature está pronta.

- Quando um pedido muda de status e o cliente tem webhook ativo que assina aquele status, existe um evento registrado na mesma transação; se a transação falha, nenhum evento existe.
- Com o processo de envio em execução e o cliente respondendo com sucesso, o primeiro envio ocorre em menos de 10 segundos depois do registro do evento.
- Falha ou ausência de resposta em 10 segundos agenda nova tentativa com esperas de 1 minuto, 5 minutos, 30 minutos, 2 horas e 12 horas.
- Depois da última retentativa com falha, o evento está na DLQ com conteúdo, motivo e data, e não está mais na fila ativa.
- Todo envio traz o identificador do evento, a assinatura, o instante do envio, o identificador do webhook e o tipo do conteúdo.
- A assinatura confere com o HMAC-SHA256 do corpo calculado com a secret do endpoint.
- A rotação de secret mantém a secret anterior válida por 24 horas.
- Endereço sem HTTPS é recusado e conteúdo de evento acima de 64 KB gera erro.
- O reprocessamento por ADMIN recoloca o evento como pendente e registra em log o usuário; um usuário OPERATOR recebe acesso negado.
- O histórico de entregas devolve até 100 envios por página, com resultado, conteúdo, resposta e tempo de resposta.
- A mudança de status de um pedido de cliente sem webhook funciona como antes.

---

### Testes e validação

Tipos de teste obrigatórios
- Testes unitários para a assinatura HMAC, a tabela de esperas, o filtro de status e a montagem do conteúdo do evento.
- Testes de integração com Vitest e supertest sobre o MySQL: atomicidade da mudança de status, cadastro e consulta de webhooks, e papel ADMIN no reprocessamento.
- Testes do processo de envio contra um servidor HTTP simulado: sucesso, timeout de 10 segundos, nova tentativa e envio para a DLQ.
- Testes de segurança: acesso negado ao OPERATOR no reprocessamento, secret ausente nas leituras e secret ausente nos logs.

Estratégia de validação
- Suíte automatizada no padrão atual de `tests/`, executada a cada alteração.
- Revisão de segurança de pelo menos 2 dias úteis antes do deploy, com foco na assinatura HMAC e na geração de secret.
- Roteiro manual com um cliente simulado para medir o limite de 10 segundos de ponta a ponta.
