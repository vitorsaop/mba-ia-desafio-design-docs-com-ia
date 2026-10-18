### FDD: [nome da feature]

Versão: [versão]
Data: [data]
Responsável: [responsável técnico]

---

### 1. Contexto e motivação técnica

[explicar o problema técnico, encaixe no HLD, atores e limites]

---

### 2. Objetivos técnicos
- [objetivo 1 com medida/invariante]
- [objetivo 2 com medida/invariante]

---

### 3. Escopo e exclusões

**Incluído**
- [item 1]
- [item 2]

**Excluído**
- [item A]
- [item B]

---

### 4. Fluxos detalhados e diagramas
**Fluxo principal**
- [passo 1]
- [passo 2]

**Fluxos alternativos e exceções**
- [variação 1]
- [variação 2]

**Diagramas** (opcional)
- [sequência/estados/fluxo]

---

### 5. Contratos públicos (assinaturas, endpoints, headers, exemplos)
**Contrato [N]: [nome do contrato]**
- Tipo: [function|method|endpoint|queue|stream|sdk]
- Assinatura/Rota: [ex: POST /v1/limiter/check]
- Método: [GET|POST|...]
- Semântica de status/headers:
  - [status/header 1: significado]
  - [status/header 2: significado]

**Exemplo de requisição**
```json
{}
```

**Exemplo de resposta**
```json
{}
```

---

### 6. Erros, exceções e fallback
- Matriz de erros previstos e tratamentos
- Estratégias de resiliência: [timeouts, retries, backoff, circuit breaker]
- Política de fallback
- Invariantes: [lista de invariantes críticos]

---

### 7. Observabilidade
Métricas
- [métrica 1]
- [métrica 2]

Logs
- Formato e campos essenciais

Tracing
- Spans principais e amostragem

Dashboards e alertas
- [painel/alerta mínimo]

---

### 8. Dependências e compatibilidade

| Versão mínima | Componente | Observações |
| --- | --- | --- |
| [vX.Y] | [comp 1] | [notas] |

Garantias de compatibilidade
- [ex: paridade entre modos de storage, versionamento semântico]

---

### 9. Critérios de aceite técnicos
- [critério 1 objetivo]
- [critério 2 objetivo]
- [critério 3 objetivo]

---

### 10. Riscos e mitigação
### [Risco 1]
- Probabilidade: [baixa|média|alta]
- Impacto: [impacto esperado]
- Mitigação:
  - [ação 1]
  - [ação 2]
- Plano de contingência: [plano B]
### [Risco 2]
- Probabilidade: [baixa|média|alta]
- Impacto: [impacto esperado]
- Mitigação:
  - [ação 1]
- Plano de contingência: [plano B]

---

### 11. Integração com o sistema existente

| Caminho | Situação atual | Integração do módulo de webhooks |
| --- | --- | --- |
| [caminho do arquivo] | [o que existe hoje] | [como o módulo se integra] |
