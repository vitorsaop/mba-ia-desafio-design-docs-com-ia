# ADR-006: Reuso dos padrões existentes do projeto

**Status:** Aceito
**Data:** 17-10-2026
**ADRs Relacionados:** ADR-004, ADR-007

## Contexto e Declaração do Problema

A aplicação é organizada em módulos por domínio, cada um com controlador, serviço,
repositório, rotas e esquemas de validação. Os erros usam uma classe base e códigos em
maiúsculas, como o de estoque insuficiente e o de transição de status inválida, e um
middleware de erro central converte erros da aplicação, falhas de validação e erros do
banco em respostas. O log usa Pino em todo o projeto, e existe um middleware de
permissão por papel, hoje aplicado em um único endpoint.

A reunião decidiu reaproveitar ao máximo o que já existe, em vez de criar mecanismos
novos para o módulo de webhooks. Alguns pontos do código limitam esse reuso: o tipo de
erro "não encontrado" tem código fixo, a lista de campos protegidos no log não inclui
secrets, e o token de acesso não identifica o cliente.

O módulo de webhooks tem também um segundo consumidor além da API: o processo que envia
os eventos. Esse processo roda separado da API e precisa usar o mesmo banco e o mesmo
log, o que reforça a escolha de reaproveitar o que já existe.

## Fatores de Decisão

- Consistência com os módulos existentes, para quem já conhece o código.
- Tratamento de erros e de logs em um único lugar, sem duplicação.
- Menos código novo para revisar e manter.
- Controle de acesso de administrador já disponível.
- Prefixo próprio nos códigos de erro, para identificar o módulo de origem.
- Formato de resposta de erro que os clientes da API já conhecem.

## Alternativas Consideradas

1. Reuso máximo dos padrões existentes
2. Módulo com tratamento de erros, logs e validação próprios (plausível, não discutida
   na reunião)
3. Reuso parcial: aproveitar erros e log, mas criar validação e controle de acesso
   próprios (plausível, não discutida na reunião)

## Decisão

Opção escolhida: "Reuso máximo dos padrões existentes", porque mantém o módulo de
webhooks igual aos demais e aproveita o tratamento central de erros, o log e o controle
de acesso que já funcionam.

O módulo de webhooks segue a mesma estrutura dos outros módulos. Seus erros usam a
classe base e códigos com o prefixo WEBHOOK_, tratados pelo middleware de erro central
sem mudança. A validação de entrada usa os mesmos esquemas de validação, o log usa o
Pino já configurado, a rota de reprocessamento usa o middleware de permissão por papel
com o papel de administrador, e os identificadores são UUID. O processo de envio
reaproveita o mesmo banco e o mesmo log.

## Prós e Contras das Alternativas

### Reuso máximo dos padrões existentes

- Bom, porque o módulo novo é lido e mantido como os demais.
- Bom, porque erros, validação e log passam pelos mesmos pontos centrais.
- Bom, porque o controle de acesso de administrador já existe.
- Ruim, porque herda as limitações atuais do código, como o código fixo do erro "não
  encontrado".

### Módulo com tratamento de erros, logs e validação próprios

- Bom, porque eliminaria as limitações do código atual dentro do módulo.
- Ruim, porque duplicaria mecanismos que já funcionam.
- Ruim, porque criaria um segundo padrão para o time aprender e manter.

### Reuso parcial: aproveitar erros e log, mas criar validação e controle de acesso próprios

- Bom, porque o controle de acesso poderia nascer já com isolamento por cliente.
- Ruim, porque o middleware de permissão por papel já cobre a regra de administrador
  exigida.
- Ruim, porque a reunião pediu reaproveitar também os esquemas de validação.

## Consequências

**Positivas:** O módulo entra no código com o mesmo formato dos outros, sem mudar o
tratamento central de erros. As respostas de erro mantêm o formato que os clientes da
API já conhecem, e o prefixo WEBHOOK_ separa os códigos do módulo.

**Negativas:** O tipo de erro "não encontrado" tem código fixo, então o código
WEBHOOK_NOT_FOUND exige uma especialização própria. A lista de campos protegidos no log
precisa passar a cobrir secrets. O processo de envio exige configuração que ele não usa,
porque herda a leitura de ambiente da API. O token de acesso não identifica o cliente,
por isso o CRUD de configuração fica sem isolamento por cliente, risco que a reunião
aceitou por enquanto.

**Trade-off:** Ganha-se consistência, menos código novo e um único ponto de tratamento
de erros. Em troca, o módulo herda as limitações atuais do código e precisa de ajustes
pontuais para contorná-las.

## Referências

- `src/shared/errors/app-error.ts:3`
- `src/middlewares/error.middleware.ts:14`
- `src/middlewares/auth.middleware.ts:49`
- `src/shared/logger/index.ts:13`
- `src/modules/orders/order.routes.ts:12`
