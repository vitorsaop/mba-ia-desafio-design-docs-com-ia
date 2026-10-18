# ADR-002: Worker em processo separado com polling de 2 segundos

**Status:** Aceito
**Data:** 17-10-2026
**ADRs Relacionados:** ADR-001, ADR-003

## Contexto e Declaração do Problema

A outbox (ADR-001) precisa de um leitor que busque os eventos pendentes e faça as
chamadas HTTP aos clientes. O MySQL não tem um mecanismo nativo de aviso a processos
externos como o NOTIFY/LISTEN do PostgreSQL. Um gatilho do banco só executa SQL e não
consegue avisar outro processo sem improvisos, como escrever em arquivo ou chamar um
endereço.

O leitor não pode viver dentro do processo da API: se a API reinicia, o leitor é
perdido. O requisito de negócio é entregar em menos de 10 segundos, e a reunião aceitou
de forma explícita que a leitura periódica acrescente até 2 segundos no pior caso. A API
já tem uma entrada de execução própria, e a aplicação usa um único banco, com um cliente
de banco por processo.

A questão é como o leitor descobre os eventos novos e em qual processo ele roda, sem
depender de recursos que o banco não oferece.

## Fatores de Decisão

- Entregar em menos de 10 segundos, com o atraso adicional da leitura limitado e
  conhecido.
- Reiniciar ou implantar a API sem perder o leitor de eventos.
- Usar o mesmo banco, a mesma pilha tecnológica e o mesmo acesso ao banco do restante da
  aplicação.
- Manter a ordem dos eventos de um mesmo pedido enquanto houver um único leitor.
- Evitar mecanismos improvisados de aviso entre o banco e o processo.
- Reaproveitar o padrão de inicialização e de encerramento ordenado que a API já usa.

## Alternativas Consideradas

1. Processo separado que consulta a outbox a cada 2 segundos
2. Gatilho do banco para avisar o processo
3. Leitor dentro do processo da API

## Decisão

Opção escolhida: "Processo separado que consulta a outbox a cada 2 segundos", porque
sobrevive à reinicialização da API e o atraso adicional máximo de 2 segundos cabe no
limite de 10 segundos.

O processo tem uma entrada de execução própria, iniciada por um script específico, e usa
o mesmo banco e a mesma configuração de conexão da API, com uma instância própria do
cliente de banco por ser outro processo. A cada ciclo ele busca, em lote pequeno, os
eventos pendentes mais antigos, processa e marca o resultado. O PM confirmou que o
intervalo de 2 segundos atende o requisito dos clientes.

Roda um único leitor, e a ordem de entrega é garantida por pedido enquanto for assim.
Essa limitação foi registrada na reunião como conhecida e aceita: não há garantia de
ordem global, e os clientes nunca pediram uma.

## Prós e Contras das Alternativas

### Processo separado que consulta a outbox a cada 2 segundos

- Bom, porque sobrevive à reinicialização da API.
- Bom, porque o atraso adicional máximo de 2 segundos cabe no limite de 10 segundos.
- Ruim, porque consulta o banco periodicamente mesmo quando não há eventos.
- Ruim, porque é mais um processo a implantar e a operar.

### Gatilho do banco para avisar o processo

- Bom, porque reagiria ao evento sem esperar o intervalo de consulta.
- Bom, porque eliminaria as consultas periódicas ao banco.
- Ruim, porque o MySQL não notifica processos externos e o gatilho só executa SQL.
- Ruim, porque avisar o processo exigiria improvisos, como escrever em arquivo ou chamar
  um endereço.

### Leitor dentro do processo da API

- Bom, porque não exige um processo adicional para implantar.
- Ruim, porque reiniciar a API perde o leitor e interrompe os envios.
- Ruim, porque o leitor e a API passam a compartilhar o mesmo ciclo de implantação e de
  reinício.

## Consequências

**Positivas:** A API pode ser reiniciada sem perder o leitor. O atraso adicional fica
limitado a 2 segundos, dentro do requisito de 10 segundos, e o PM confirmou que esse
intervalo atende os clientes. Nenhuma infraestrutura nova é necessária.

**Negativas:** Há consultas periódicas ao banco mesmo sem eventos. A ordem de entrega
vale só por pedido e só com um único leitor, e um evento em espera de nova tentativa
pode ser ultrapassado pelo evento seguinte do mesmo pedido. Como o leitor trata um
evento por vez, um cliente lento atrasa em até 10 segundos cada evento seguinte do lote.
O processo exige a mesma configuração de ambiente da API, inclusive variáveis que ele
não usa. [PRECISA DE INFORMAÇÃO: o que acontece com os eventos marcados como em
processamento quando o leitor reinicia?]

**Trade-off:** Ganha-se previsibilidade e simplicidade operacional. Em troca, aceita-se
até 2 segundos de atraso em cada evento e uma escala limitada, porque mais de um leitor
perde a garantia de ordem.

## Referências

- `src/server.ts:6`
- `src/config/database.ts:4`
- `src/config/env.ts:3`
- `package.json:10`
