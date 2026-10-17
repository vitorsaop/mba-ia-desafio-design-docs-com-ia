# ADR-004: Assinatura HMAC-SHA256 com secret por endpoint e rotação de 24 horas

**Status:** Aceito
**Data:** 17-10-2026
**ADRs Relacionados:** ADR-005, ADR-006

## Contexto e Declaração do Problema

Os eventos contêm dados de pedidos e saem para endereços fora da infraestrutura da
empresa. O cliente precisa conseguir validar que a requisição veio de fato do sistema e
que ninguém alterou o conteúdo no caminho. Um cliente já vazou uma secret em log de
aplicação dele, e a reunião quis limitar o dano de um vazamento desse tipo.

O padrão de mercado é assinar o conteúdo com HMAC e uma secret compartilhada, e todo
cliente sério tem biblioteca para verificar a assinatura. A aplicação hoje só autentica
usuários por token de acesso e guarda senhas apenas como hash, que não serve como chave
de assinatura. Também é preciso permitir a troca da secret sem parar a integração do
cliente.

A reunião também exigiu que o endereço do webhook use HTTPS. O HTTPS protege o canal
entre o sistema e o cliente, mas não permite que o cliente prove, a partir do conteúdo
recebido, que a requisição foi enviada pelo sistema nem que o conteúdo não foi alterado.
Por isso a assinatura é uma decisão separada.

## Fatores de Decisão

- O cliente deve conseguir validar a origem e a integridade do conteúdo.
- O vazamento de uma secret deve afetar apenas um endpoint.
- A troca de secret não pode obrigar o cliente a migrar todos os seus sistemas de uma
  vez.
- O algoritmo deve ter suporte nas bibliotecas comuns do lado do cliente.
- Hipótese: a secret deve ficar fora de logs e de respostas de leitura.
- A solução deve funcionar com o conteúdo exatamente como foi enviado, sem depender de
  reformatação.

## Alternativas Consideradas

1. HMAC-SHA256 com secret única por endpoint e rotação com sobreposição de 24 horas
2. Secret global da plataforma
3. Somente HTTPS, sem assinatura do conteúdo (plausível, não discutida na reunião)

## Decisão

Opção escolhida: "HMAC-SHA256 com secret única por endpoint e rotação com sobreposição
de 24 horas", porque limita o efeito de um vazamento a um endpoint e permite que o
cliente migre aos poucos.

A assinatura é calculada sobre o corpo da requisição e enviada em um header. A secret é
gerada pelo sistema, devolvida ao cliente na criação do endpoint e é diferente para cada
endpoint. O cliente pode pedir uma nova secret pela API; depois da rotação, a secret
anterior continua válida por 24 horas e então deixa de valer.

O HTTPS continua obrigatório no cadastro do endereço, mas é tratado como validação de
cadastro e não substitui a assinatura.

## Prós e Contras das Alternativas

### HMAC-SHA256 com secret única por endpoint e rotação com sobreposição de 24 horas

- Bom, porque um vazamento compromete apenas um endpoint.
- Bom, porque o cliente valida a assinatura com bibliotecas padrão.
- Bom, porque a sobreposição de 24 horas permite migrar sem parada.
- Ruim, porque o sistema precisa guardar a secret de forma recuperável, ao contrário das
  senhas, que ficam só como hash.

### Secret global da plataforma

- Bom, porque há uma única secret para gerenciar.
- Ruim, porque o vazamento de uma secret compromete todos os clientes.
- Ruim, porque trocar a secret afetaria todos os clientes ao mesmo tempo.

### Somente HTTPS, sem assinatura do conteúdo

- Bom, porque não exige gerenciar secrets.
- Ruim, porque o cliente não consegue provar que a requisição veio do sistema.
- Ruim, porque não atende o pedido da reunião de validar origem e integridade do
  conteúdo.

## Consequências

**Positivas:** Um vazamento fica restrito a um endpoint. O cliente verifica origem e
integridade com uma biblioteca padrão e a rotação não exige parada. Hipótese: a secret
aparece apenas nas respostas de criação e de rotação, e nunca em leituras ou em logs,
porque a reunião mandou devolvê-la na criação e registrou o vazamento de uma secret em
log de um cliente.

**Negativas:** O sistema passa a administrar duas secrets válidas durante 24 horas após
cada rotação. A assinatura cobre somente o corpo, então o header com o instante do envio
não é assinado e a detecção de replay pelo cliente fica fraca. [PRECISA DE INFORMAÇÃO:
qual é o conteúdo do header de assinatura durante a janela de 24 horas?] [PRECISA DE
INFORMAÇÃO: como a secret é guardada em repouso, já que o HMAC exige a chave
recuperável?]

**Trade-off:** Ganha-se segurança por endpoint e rotação sem parada. Em troca, assume-se
a gestão do ciclo de vida das secrets: geração, guarda recuperável, rotação e expiração.

## Referências

- `src/shared/logger/index.ts:4`
- `src/middlewares/auth.middleware.ts:27`
- `src/config/env.ts:3`
- `prisma/schema.prisma:25`
