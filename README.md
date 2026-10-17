# Da Reunião ao Documento: Design Docs de Webhooks gerados com IA

Pacote de documentação técnica do Sistema de Webhooks de Notificação de Pedidos de um Order Management System (OMS), produzido a partir da transcrição de uma reunião (`TRANSCRICAO.md`) e do código existente, usando o Claude Code como ferramenta principal. O enunciado original do desafio está no repositório base: https://github.com/devfullcycle/mba-ia-desafio-design-docs-com-ia

## Sobre o desafio

Uma empresa que opera um OMS em produção decidiu, em uma reunião de cerca de 55 minutos entre tech lead, PM, engenheiros e segurança, construir webhooks de saída para três clientes B2B que hoje consultam a listagem de pedidos de tempos em tempos. As decisões foram tomadas na call, mas nada foi registrado além da transcrição. A tarefa é transformar essa transcrição e o código da aplicação (Node.js, TypeScript, Express, Prisma e MySQL) em documentação acionável: PRD, RFC, FDD, de 5 a 8 ADRs e um Tracker que liga cada item à fala ou ao arquivo de origem.

O ponto central do desafio é a fidelidade. Nada pode ser inventado, o que a reunião descartou ou adiou não pode virar requisito, e cada documento opera em uma altura diferente (produto, arquitetura, decisão pontual, implementação). A entrega é puramente documental: `src/`, `prisma/`, `tests/` e as configurações não foram alterados.

## Ferramentas de IA utilizadas

- **Claude Code** (extensão para VSCode, modelo Claude Sonnet 5.5): ferramenta principal. Leu o código e a transcrição, produziu o plano, criou as skills, executou os validadores, gerou os documentos pelas skills e fez a revisão final. Todo o trabalho desta entrega foi feito dentro de sessões do Claude Code.
- **Skill `skill-creator` da Anthropic**, usada localmente (não versionada neste repositório): serviu para criar as cinco skills do projeto e para validar o frontmatter delas (`quick_validate.py`).
- **Cinco skills criadas para este projeto** (em `.claude/skills/`): `adr-creator`, `rfc-creator`, `fdd-creator`, `prd-creator` e `tracker-creator`. Cada uma gera um tipo de documento seguindo um template e termina rodando um validador próprio.
- **Subagente de revisão independente** do Claude Code: leu os documentos, a transcrição e o código sem receber as conclusões da produção e reportou contradições e itens sem origem.
- **Material do curso como base dos templates**: o "Esqueleto de PRD" e o "Esqueleto de FDD" das páginas de Design Docs do Notion do curso, e o formato MADR estrito do plugin `adrs-management` do repositório `devfullcycle/claude-mkt-place`. O material do curso não traz template de RFC; para ele vale a lista de seções do enunciado.

## Workflow adotado

1. **Contextualização.** O Claude Code leu o enunciado, a transcrição completa e os arquivos do código que a feature toca: serviço e máquina de estados de pedidos, classes de erro, error middleware, `requireRole`, logger Pino, `schema.prisma`, `server.ts`, rotas, configuração e testes.
2. **Plano.** Antes de escrever qualquer documento, o plano separou requisitos funcionais, requisitos não funcionais, decisões técnicas, decisões de segurança, o que foi descartado, o que foi adiado e as lacunas da reunião. Cada item aponta para `[hh:mm] Nome` ou para `caminho:linha`. O plano final está em `.claude/plano/PLANO-WEBHOOKS.md`.
3. **Classes de rastreabilidade.** Todo item é classe A (decidido na reunião), B (consequência necessária de um item A ou do código) ou C (lacuna). A classe C nunca vira requisito: entra como questão em aberto no RFC ou como "Hipótese:" rotulada no PRD e no FDD.
4. **Skills por documento.** Cada skill carrega o template literal (`assets/`), as regras e a conciliação entre o enunciado e o template do curso (`references/`) e um validador estrutural (`scripts/`). A skill só termina com `RESULTADO: PASS`.
5. **Geração na ordem do enunciado:** ADRs, RFC, FDD, PRD, Tracker e, por último, este README. Correção de erro vai para o plano ou para a skill, e o documento é gerado de novo; não se edita o documento à mão para contornar o validador.
6. **Tracker verificável.** O script `enumerar_itens.py` lista os itens identificáveis dos documentos com IDs fixos. A origem de cada um fica em um arquivo de mapeamento local de trabalho (não versionado), e `montar_tracker.py` gera `docs/TRACKER.md`. O validador compara a tabela com a lista e confere que cada `[hh:mm] Nome` existe na transcrição e cada arquivo existe no repositório.
7. **Revisão independente** de contradições e invenções, depois dos validadores, por um agente que não recebeu as conclusões.
8. **Fonte da verdade e propagação.** A `TRANSCRICAO.md` prevalece sobre o plano, os documentos e o código. Cada correção da revisão foi aplicada ao plano e a todos os documentos em que o fato aparece; o script `conferir_consistencia.py` verifica que as frases corrigidas não voltam e que todo fato derivado carrega o rótulo "Hipótese:".

## Prompts customizados

**Prompt 1.** Prompt inicial do arquiteto, que definiu o papel, o critério de qualidade e as referências (ortografia revisada):

```text
Você é um arquiteto de software com profundos conhecimentos em documentações como, por
exemplo: PRD (liga visão de negócio à execução técnica; define propósito, valor e métricas;
é leve, iterativo e coescrito por PMs e tech leads); FDD (define o "como implementar" de uma
feature; é o sucessor direto do FRD, mas focado em clareza e execução técnica); RFC (promove
discussões técnicas assíncronas; amplamente usado em times maduros e open source); TRACKER
(rastreabilidade linkável entre o que foi pedido, considerando a fonte da informação e o
trecho específico).

Seu objetivo inicial é contextualizar-se do projeto a partir do README.md. Em seguida, analise
o requisito solicitado referente ao WEBHOOK para notificação, contido na transcrição
TRANSCRICAO.md. Após a compreensão total, elabore um plano em que sejam separados os
requisitos funcionais, os requisitos não funcionais, as decisões técnicas conversadas na
TRANSCRICAO.md e as decisões de segurança. Por fim, todas as decisões devem estar alinhadas
com o código-fonte existente da aplicação.

Pense passo a passo. Não use linguagem vaga, não use jargões, não use emojis, não use
linguagem ambígua. Consulte as referências oficiais sobre os documentos a serem gerados (as
páginas de Design Docs do Notion do curso).
```

**Prompt 2.** Skill `prd-creator` (arquivo completo em `.claude/skills/prd-creator/SKILL.md`; o template literal está em `assets/template-prd.md` e o validador em `scripts/validar_prd.py`):

```text
---
name: prd-creator
description: Gera docs/PRD.md, o Product Requirements Document da feature de webhooks de
notificação de pedidos (problema, público, objetivos com métricas, escopo, requisitos
funcionais e não funcionais, decisões, dependências, riscos, critérios de aceitação e
testes), exatamente no esqueleto de PRD do curso, a partir de .claude/plano/PLANO-WEBHOOKS.md,
TRANSCRICAO.md e do código. Use esta skill sempre que o usuário pedir para criar, gerar,
refazer, corrigir ou validar o PRD, o documento de produto ou os requisitos de negócio da
feature de webhooks, mesmo que ele não cite o nome da skill.
---

## Regras que não podem ser quebradas

- Mesmos títulos `###`, mesma ordem, mesmos rótulos e mesmos separadores `---` do template.
- Mínimo de 8 requisitos funcionais (o plano define 12), de 1 objetivo com métrica e meta
  numérica (o plano define 4), de 2 itens descartados ou adiados em "Fora de escopo" e de 2
  riscos com probabilidade, impacto, mitigação e plano de contingência.
- Prioridade apenas `alta`, `media` ou `baixa` (sem acento), como no template.
- Nada descartado na reunião aparece como requisito ou como item incluso.
- Português simples e direto. Sem emoji, sem travessão, sem termos vagos ("etc.",
  "entre outros", "adequado").
- Cada afirmação tem origem na transcrição ou no código. O PRD não carrega as citações; o
  Tracker as registra.
- A `TRANSCRICAO.md` é a fonte da verdade. Se o plano, um documento ou o código divergir
  dela, vale a transcrição e o plano é corrigido. Uma correção vale para todos os documentos:
  depois de mudar um fato, procure o termo em `docs/` e rode `conferir_consistencia.py`. Um
  fato que a reunião não decidiu leva "Hipótese:" em todo documento em que aparece.

Passo final obrigatório: python3 .claude/skills/prd-creator/scripts/validar_prd.py
até aparecer "RESULTADO: PASS".
```

**Prompt 3.** Skill `adr-creator` (arquivo completo em `.claude/skills/adr-creator/SKILL.md`; conciliação entre o formato do professor e o enunciado em `references/regras.md`):

```text
---
name: adr-creator
description: Gera os ADRs (Architecture Decision Records) da feature de webhooks de pedidos
em docs/adrs/ADR-NNN-titulo-em-kebab-case.md, no formato MADR estrito do curso traduzido
para pt-BR, a partir de .claude/plano/PLANO-WEBHOOKS.md, TRANSCRICAO.md e do código. Use
esta skill sempre que o usuário pedir para criar, gerar, refazer, corrigir ou validar ADRs,
registros de decisão arquitetural ou as decisões da reunião de webhooks, mesmo que ele não
cite o nome da skill.
---

## Regras que não podem ser quebradas

- Cabeçalho só com Status, Data e ADRs Relacionados. Qualquer outro campo foi proibido pelo
  professor.
- Exatamente 7 seções `##`, com os nomes e a ordem de `assets/template-adr.md`.
- Zero blocos de código. Zero nomes de classe, método, tabela, coluna ou endpoint no texto.
  Esses nomes ficam no FDD. Nomes de headers do protocolo (`X-Event-Id`, `X-Signature`) e
  `HMAC-SHA256` são permitidos porque são a própria decisão.
- Caminhos de arquivo só na seção Referências, no formato `caminho:linha`, de 3 a 5 por ADR,
  todos existentes.
- De 2 a 3 alternativas; a primeira é a escolhida. Cada alternativa tem uma subseção em
  Prós e Contras.
- Sem sugestões futuras ("considere", "avalie", "se o volume crescer"). Perguntas abertas
  vão para o RFC.
- Sem emoji e sem travessão.
- Cada afirmação tem origem na transcrição ou no código. Se não tem, ela não entra.
- A `TRANSCRICAO.md` é a fonte da verdade. Se o plano, um documento ou o código divergir
  dela, vale a transcrição e o plano é corrigido. Uma correção vale para todos os documentos:
  depois de mudar um fato, procure o termo em `docs/` e rode `conferir_consistencia.py`. Um
  fato que a reunião não decidiu leva "Hipótese:" em todo documento em que aparece.

Passo final obrigatório: python3 .claude/skills/adr-creator/scripts/validar_adr.py
até aparecer "RESULTADO: PASS".
```

As skills `rfc-creator`, `fdd-creator` e `tracker-creator` seguem a mesma estrutura e estão em `.claude/skills/`.

## Iterações e ajustes

O trabalho passou por 7 ciclos principais de geração, validação, revisão crítica e correção. Os momentos em que a IA errou ou entregou algo superficial:

1. **Plano ignorou os templates do curso.** A primeira versão do plano usou as listas de seções do enunciado como se fossem os templates, e a página do Notion não abriu pela ferramenta de página web (devolveu só o título). Depois da correção ("os requisitos do README e as estruturas dos documentos são inegociáveis"), o conteúdo das páginas foi lido pela interface pública de páginas do Notion e os templates reais de PRD e FDD foram encontrados, além do formato de ADR do professor. O plano foi reescrito com uma tabela de conciliação entre enunciado e template.
2. **Template de RFC inexistente.** O material do curso não tem RFC. Em vez de inventar um formato, o template do `rfc-creator` reproduz a lista do enunciado, na mesma ordem, e isso ficou registrado.
3. **Frontmatter inválido.** A descrição do `fdd-creator` tinha `: ` no meio do texto, o que quebra o YAML. O `quick_validate.py` do skill-creator pegou o erro antes de qualquer uso.
4. **ADRs reprovados por tamanho.** O validador reprovou 6 dos 7 ADRs: tinham de 77 a 94 linhas, abaixo das 100 que o professor lista. A correção foi em duas partes: um quebrador de linhas determinístico (88 colunas) e a inclusão de conteúdo com origem (fatores de decisão, alternativas plausíveis e prós e contras que faltavam), sem inflar com texto vazio.
5. **Validador do FDD rígido demais.** Ele não reconhecia o marcador "(arquivos novos)" no plural para linhas com vários arquivos ainda inexistentes. O defeito era do validador, não do documento, e foi corrigido no validador e na skill.
6. **Resumos do Tracker truncados.** A primeira versão do enumerador cortava frases no meio e apagava o `*` de `*.secret`. Foi corrigida, e as três alternativas de ADR que são plausíveis mas não foram discutidas na reunião passaram a ter Tipo `Hipótese`.
7. **Revisão independente.** Um agente leu a transcrição, o código e todos os documentos sem receber as conclusões e reportou 23 achados, nenhum de gravidade alta. Cada um foi conferido contra a transcrição e o código, todos procederam, e a correção foi propagada para o plano, o PRD, o RFC, o FDD, os ADRs e o Tracker:
   - **"5 tentativas" virou "1 envio mais 5 retentativas, 6 requisições" sem aviso.** A leitura é a única que usa as cinco esperas (876 minutos, as "quase 15 horas" de `[09:17] Diego`), mas é inferência. Passou a ser "Hipótese" no PRD e no FDD, "Interpretação adotada" com marcador no ADR-003 e questão em aberto no RFC; o limite vale por ciclo de entrega, porque um replay recomeça o ciclo.
   - **Rollback com erro 422 para payload acima de 64 KB.** A reunião decidiu só "erro caso ultrapasse". O restante passou a "Hipótese", e a garantia de compatibilidade do FDD ficou restrita à resposta de sucesso.
   - **"A secret nunca aparece em logs"** citava `[09:22] Diego`, que fala do log do cliente, não do nosso. Passou a "Hipótese" em todos os documentos, e a redação de log do FDD passou a cobrir também `previous_secret`.
   - **Cliente lento atrasa o lote.** O worker trata um evento por vez e cada chamada pode levar 10 segundos, o que ameaça a meta de 10 segundos. Virou risco no PRD, no RFC e no FDD, questão em aberto no RFC e ressalva no ADR-002.
   - **ADR-007 afirmava e perguntava** se a criação de pedido gera evento. Ficou só a pergunta, alinhada ao PRD, ao RFC e ao FDD.
   - **Inconsistências menores corrigidas:** exemplos do FDD (evento já entregue sendo reprocessado, data incompatível), "quatro" e "cinco" headers, "2 dias úteis" onde Sofia disse "pelo menos dois", "quatro peças" para seis elementos, ADRs relacionados assimétricos, três linhas de código imprecisas, alternativas de ADR plausíveis e não discutidas sem rótulo, e prioridades e probabilidades sem fonte (agora declaradas como avaliação do autor na legenda do Tracker).
   - **Tracker ampliado** de 298 para 322 linhas, com o modelo de dados e cada hipótese dos contratos.
   - Os marcadores `[PRECISA DE INFORMAÇÃO]` continuam em ADRs com Status "Aceito" de propósito: o formato do professor os prevê para lacunas, e o FDD as trata como "Hipótese".

Também houve uma suposição errada do Claude Code no meio do caminho: ele afirmou que o `skill-creator` não estava no `.claude/` do projeto, mas a skill havia sido instalada depois da primeira varredura de arquivos.

## Como navegar a entrega

```
.
├── README.md                          este arquivo (processo)
├── TRANSCRICAO.md                     a reunião (não alterado)
├── docs/
│   ├── PRD.md                         por que e o quê
│   ├── RFC.md                         proposta técnica para revisão
│   ├── FDD.md                         como construir, em detalhe
│   ├── TRACKER.md                     origem de cada item (fala ou arquivo)
│   └── adrs/ADR-001 ... ADR-007       uma decisão por arquivo
├── .claude/
│   ├── plano/PLANO-WEBHOOKS.md        plano que alimentou as skills
│   └── skills/                        adr-creator, rfc-creator, fdd-creator,
│                                      prd-creator, tracker-creator
└── src/ prisma/ tests/                código da aplicação (não alterado)
```

**Ordem sugerida de leitura**

1. `docs/PRD.md`: o problema, o público, as metas e o escopo.
2. `docs/RFC.md`: a proposta, as alternativas descartadas e as questões em aberto.
3. `docs/adrs/`: cada decisão fechada, de ADR-001 a ADR-007.
4. `docs/FDD.md`: fluxos, contratos HTTP, matriz de erros e a seção "Integração com o sistema existente".
5. `docs/TRACKER.md`: a origem de qualquer afirmação lida nos documentos anteriores.
6. `.claude/plano/PLANO-WEBHOOKS.md`: as lacunas e as classes A, B e C.

**Como conferir os documentos**

```bash
python3 .claude/skills/adr-creator/scripts/validar_adr.py
python3 .claude/skills/rfc-creator/scripts/validar_rfc.py
python3 .claude/skills/fdd-creator/scripts/validar_fdd.py
python3 .claude/skills/prd-creator/scripts/validar_prd.py
python3 .claude/skills/tracker-creator/scripts/validar_tracker.py
python3 .claude/skills/tracker-creator/scripts/conferir_consistencia.py
```

Cada comando termina com `RESULTADO: PASS` quando o documento segue o template e as regras do enunciado.
