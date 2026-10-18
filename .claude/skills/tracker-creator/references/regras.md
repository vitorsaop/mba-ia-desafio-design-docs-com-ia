# Regras do tracker-creator

## Fonte do formato

README do desafio, requisito 5 e critérios de aceite do Tracker. O Tracker não existe no curso: é uma exigência do desafio contra alucinação.

## Formato obrigatório

```
| ID | Documento | Tipo | Conteúdo (resumo) | Fonte | Localização |
| --- | --- | --- | --- | --- | --- |
```

- ID: identificador único (exemplos do README: PRD-FR-01, RFC-ALT-02, FDD-CONTRATO-03, ADR-002).
- Documento: caminho do arquivo (`docs/PRD.md`, `docs/RFC.md`, `docs/FDD.md`, `docs/adrs/ADR-002-....md`).
- Tipo: um dos valores da lista abaixo.
- Conteúdo (resumo): uma linha.
- Fonte: `TRANSCRICAO` ou `CODIGO`.
- Localização: para `TRANSCRICAO`, `[hh:mm] Nome` (por exemplo `[09:17] Diego`); para `CODIGO`, o caminho do arquivo (por exemplo `src/modules/orders/order.service.ts`, com `:linha` opcional).

## Tipos aceitos

Requisito Funcional; Requisito Não Funcional; Objetivo; Escopo; Decisão; Trade-off; Dependência; Risco; Critério de Aceite; Teste; Restrição; Hipótese; Contrato; Erro; Alternativa; Questão em Aberto; Fluxo; Integração; Observabilidade; Resiliência; Invariante; Proposta; Impacto.

## Regra de cada ID (o enumerador cria todos)

| Documento | ID | Item |
| --- | --- | --- |
| PRD | `PRD-OBJ-NN` | linha da tabela de objetivos |
| PRD | `PRD-ESC-INC-NN`, `PRD-ESC-FORA-NN` | bullet de Incluso e de Fora de escopo |
| PRD | `PRD-FR-NN` | bloco `#### FR-NN` |
| PRD | `PRD-RNF-NN` | bullet de qualquer rótulo de Requisitos não funcionais, em ordem de aparição |
| PRD | `PRD-DEC-NN`, `PRD-DEP-NN`, `PRD-RISCO-NN` | blocos `####` de Decisões, Dependências e Riscos |
| PRD | `PRD-CA-NN`, `PRD-TESTE-NN` | bullets de Critérios de aceitação e de Testes e validação |
| RFC | `RFC-PROP-NN`, `RFC-ALT-NN`, `RFC-QA-NN`, `RFC-IMP-NN`, `RFC-RISCO-NN`, `RFC-ADR-NN` | bullets das seções Proposta técnica, Alternativas consideradas, Questões em aberto, Impacto (antes de "Riscos"), Riscos e Decisões relacionadas |
| FDD | `FDD-OBJ-NN`, `FDD-ESC-INC-NN`, `FDD-ESC-EXC-NN` | bullets das seções 2 e 3 |
| FDD | `FDD-FLUXO-NN` | bullets de Fluxo principal e Fluxos alternativos |
| FDD | `FDD-CONTRATO-NN` | `**Contrato N: ...**` |
| FDD | `FDD-ERRO-NN` | linha da matriz de erros |
| FDD | `FDD-RES-NN`, `FDD-INV-NN` | sub-bullets de resiliência e fallback; sub-bullets de invariantes |
| FDD | `FDD-OBS-NN` | bullets da seção 7 |
| FDD | `FDD-DEP-NN` | linhas da tabela da seção 8 e bullets de garantias |
| FDD | `FDD-CA-NN`, `FDD-RISCO-NN`, `FDD-INT-NN` | critérios da seção 9, riscos da seção 10, linhas da seção 11 |
| ADR | `ADR-NNN`, `ADR-NNN-ALT-NN` | a decisão do ADR e cada alternativa numerada |

## Como escolher Fonte e Localização

1. Procure o item no plano (`.claude/plano/PLANO-WEBHOOKS.md`): as colunas "Localização" já trazem os `[hh:mm] Nome` e os `caminho:linha`.
2. Confirme a fala em `TRANSCRICAO.md` com `grep -n "^\[09:17\] Diego" TRANSCRICAO.md`.
3. Confirme o arquivo e a linha abrindo o arquivo.
4. Item que decorre da reunião: `TRANSCRICAO`. Item que decorre só do código (versões, caminhos, padrões existentes): `CODIGO`.
5. Item de classe B: aponte para o item A que o obriga. Exemplo: o intervalo de 876 minutos aponta para `[09:17] Diego`.
6. Item "Hipótese:" ou lacuna: Tipo `Hipótese`; Fonte `TRANSCRICAO` com a fala onde a lacuna nasceu (coluna "Localização da origem" da seção S6 do plano), ou `CODIGO` quando a lacuna vem de uma limitação do código.
7. Várias origens: use a principal na Fonte e liste as falas com `; ` na Localização. Não misture `TRANSCRICAO` e `CODIGO` na mesma linha.

## Legenda (2 a 4 linhas, logo abaixo do título)

Diga: o que a tabela mapeia; que `TRANSCRICAO` usa `[hh:mm] Nome` de `TRANSCRICAO.md` e `CODIGO` usa o caminho do arquivo; que o Tipo `Hipótese` marca proposta sem decisão na reunião; e que os IDs seguem o padrão `DOCUMENTO-TIPO-NN`.
