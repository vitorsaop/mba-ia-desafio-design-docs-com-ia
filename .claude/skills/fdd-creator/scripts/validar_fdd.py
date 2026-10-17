#!/usr/bin/env python3
"""Valida docs/FDD.md contra assets/template-fdd.md e contra o README do desafio.

Uso: python3 .claude/skills/fdd-creator/scripts/validar_fdd.py [raiz-do-repositorio]
Saida: uma linha por problema e, no fim, "RESULTADO: PASS" ou "RESULTADO: FAIL".
"""
import json
import os
import re
import sys

RAIZ = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
ARQUIVO = os.path.join(RAIZ, "docs", "FDD.md")
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "template-fdd.md")

EM_DASH = "\u2014"
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50]")
SECOES = [
    "Contexto e motivação técnica",
    "Objetivos técnicos",
    "Escopo e exclusões",
    "Fluxos detalhados e diagramas",
    "Contratos públicos (assinaturas, endpoints, headers, exemplos)",
    "Erros, exceções e fallback",
    "Observabilidade",
    "Dependências e compatibilidade",
    "Critérios de aceite técnicos",
    "Riscos e mitigação",
    "Integração com o sistema existente",
]
TIPOS = {"function", "method", "endpoint", "queue", "stream", "sdk"}
CITACAO = re.compile(r"\[(\d\d:\d\d)\] ([A-Za-zÀ-ÿ]+)")
CAMINHO = re.compile(
    r"`((?:src|prisma|tests|docs)/[A-Za-z0-9_./-]*[A-Za-z0-9_]|package\.json|docker-compose\.yml|tsconfig\.build\.json|vitest\.config\.ts)(?::\d+)?`"
)

problemas = []


def falha(msg):
    problemas.append(msg)


def tokens_do_template():
    texto = open(TEMPLATE, encoding="utf-8").read()
    texto = re.sub(r"```.*?```", "", texto, flags=re.S)
    return {"[%s]" % t for t in re.findall(r"\[([^\[\]\n]{3,})\]", texto)}


def separar_secoes(texto):
    partes = re.split(r"^### (\d+)\. (.+)$", texto, flags=re.M)
    cabecalho = partes[0]
    secoes = []
    for i in range(1, len(partes), 3):
        secoes.append((int(partes[i]), partes[i + 1].strip(), partes[i + 2]))
    return cabecalho, secoes


def bullets(bloco, nested=False):
    padrao = r"^\s{2,}- " if nested else r"^- "
    return [l for l in bloco.split("\n") if re.match(padrao, l)]


def apos_rotulo(bloco, rotulo):
    """Texto entre uma linha que comeca com o rotulo e a proxima linha de rotulo."""
    m = re.search(r"^%s.*?\n(.*?)(?=^\*\*|\Z)" % re.escape(rotulo), bloco, re.S | re.M)
    return m.group(1) if m else ""


def tabela(bloco):
    linhas = [l for l in bloco.split("\n") if l.startswith("|")]
    if len(linhas) < 2:
        return [], []
    cab = [c.strip() for c in linhas[0].strip().strip("|").split("|")]
    linhas_dados = []
    for l in linhas[2:]:
        linhas_dados.append([c.strip() for c in l.strip().strip("|").split("|")])
    return cab, linhas_dados


def inicios_transcricao():
    s = set()
    for l in open(os.path.join(RAIZ, "TRANSCRICAO.md"), encoding="utf-8").read().split("\n"):
        m = re.match(r"^\[(\d\d:\d\d)\] ([^:]+):", l)
        if m:
            s.add((m.group(1), m.group(2)))
    return s


def validar_contratos(corpo):
    blocos = re.split(r"^(?=\*\*Contrato \d+: )", corpo, flags=re.M)[1:]
    if not blocos:
        falha("secao 5 sem blocos '**Contrato N: nome**'")
        return
    endpoints_completos = 0
    for esperado, b in enumerate(blocos, start=1):
        m = re.match(r"^\*\*Contrato (\d+): (.+)\*\*$", b.split("\n")[0])
        if not m or int(m.group(1)) != esperado:
            falha("contratos devem ser numerados em sequencia; esperado Contrato %d" % esperado)
            continue
        nome = "Contrato %d" % esperado
        tipo = re.search(r"^- Tipo: (.+)$", b, re.M)
        rota = re.search(r"^- Assinatura/Rota: (.+)$", b, re.M)
        metodo = re.search(r"^- Método: (.+)$", b, re.M)
        sem = re.search(r"^- Semântica de status/headers:\s*\n((?:\s{2,}- .+\n?)+)", b, re.M)
        if not (tipo and rota and metodo and sem):
            falha("%s sem Tipo, Assinatura/Rota, Metodo ou Semantica de status/headers" % nome)
            continue
        if tipo.group(1).strip() not in TIPOS:
            falha("%s: Tipo %r fora de %s" % (nome, tipo.group(1).strip(), sorted(TIPOS)))
        for rotulo in ("**Exemplo de requisição**", "**Exemplo de resposta**"):
            m2 = re.search(r"^%s\s*\n```(\w*)\n(.*?)\n```" % re.escape(rotulo), b, re.S | re.M)
            if not m2:
                falha("%s sem %s com bloco de codigo" % (nome, rotulo))
                continue
            if m2.group(1) == "json":
                try:
                    json.loads(m2.group(2))
                except ValueError as e:
                    falha("%s: JSON invalido em %s (%s)" % (nome, rotulo, e))
        if tipo.group(1).strip() == "endpoint":
            if re.search(r"\b[1-5]\d\d\b", sem.group(1)) and "```" in b:
                endpoints_completos += 1
            else:
                falha("%s: endpoint sem status code na semantica" % nome)
    if endpoints_completos < 4:
        falha("ha %d endpoints completos; o README exige 4 ou mais" % endpoints_completos)


def validar_erros(corpo):
    ordem = [
        "- Matriz de erros previstos e tratamentos",
        "- Estratégias de resiliência",
        "- Política de fallback",
        "- Invariantes",
    ]
    posicoes = []
    for r in ordem:
        i = corpo.find("\n" + r) if not corpo.startswith(r) else 0
        if i < 0:
            falha("secao 6 sem o bullet %r" % r)
        posicoes.append(i)
    if all(p >= 0 for p in posicoes) and posicoes != sorted(posicoes):
        falha("secao 6: bullets fora de ordem")
    cab, dados = tabela(corpo)
    if cab != ["Código", "Condição", "Status HTTP", "Tratamento", "Notas"]:
        falha("matriz de erros deve ter o cabecalho | Código | Condição | Status HTTP | Tratamento | Notas |")
    codigos = []
    for d in dados:
        c = d[0].strip("`") if d else ""
        if not re.match(r"^WEBHOOK_[A-Z_]+$", c):
            falha("linha da matriz sem codigo WEBHOOK_*: %r" % (d[:1],))
        codigos.append(c)
    if len(codigos) < 7:
        falha("matriz tem %d codigos; o plano preve 7 ou mais" % len(codigos))
    if len(set(codigos)) != len(codigos):
        falha("codigo repetido na matriz de erros")
    if "Códigos existentes reaproveitados sem alteração:" not in corpo:
        falha("faltou a linha 'Códigos existentes reaproveitados sem alteração:'")
    resiliencia = corpo.split("- Estratégias de resiliência", 1)[-1].split("- Invariantes")[0].lower()
    for palavra in ("timeout", "retr", "backoff", "fallback"):
        if palavra not in resiliencia:
            falha("estrategias de resiliencia nao mencionam %r" % palavra)
    for rotulo in ("- Estratégias de resiliência", "- Política de fallback", "- Invariantes"):
        trecho = corpo.split(rotulo, 1)[-1].split("\n- ", 1)[0]
        if not bullets(trecho, nested=True):
            falha("%r sem sub-bullets" % rotulo)
    return set(codigos)


def validar_observabilidade(corpo):
    for rotulo in ("Métricas", "Logs", "Tracing", "Dashboards e alertas"):
        m = re.search(r"^%s\s*\n((?:- .+\n?)+)" % re.escape(rotulo), corpo, re.M)
        if not m:
            falha("secao 7 sem o rotulo %r seguido de bullets" % rotulo)


def validar_riscos(corpo):
    riscos = re.split(r"^### (?=\S)", corpo, flags=re.M)[1:]
    if len(riscos) < 2:
        falha("secao 10 tem %d riscos; o minimo e 2" % len(riscos))
    for r in riscos:
        titulo = r.split("\n")[0]
        if not re.search(r"^- Probabilidade: (baixa|média|alta)$", r, re.M):
            falha("risco %r sem 'Probabilidade: baixa|média|alta'" % titulo)
        if not re.search(r"^- Impacto: \S", r, re.M):
            falha("risco %r sem Impacto" % titulo)
        if not re.search(r"^- Mitigação:\s*\n\s{2,}- \S", r, re.M):
            falha("risco %r sem Mitigacao com sub-bullets" % titulo)
        if not re.search(r"^- Plano de contingência: \S", r, re.M):
            falha("risco %r sem Plano de contingencia" % titulo)


def validar_integracao(corpo):
    cab, dados = tabela(corpo)
    if cab != ["Caminho", "Situação atual", "Integração do módulo de webhooks"]:
        falha("tabela da secao 11 deve ter o cabecalho | Caminho | Situação atual | Integração do módulo de webhooks |")
    existentes = set()
    for d in dados:
        if len(d) != 3:
            falha("linha da secao 11 deve ter 3 colunas: %r" % d[:1])
            continue
        achados = CAMINHO.findall(d[0])
        if not achados:
            falha("linha da secao 11 sem caminho entre crases: %r" % d[0][:50])
        for c in achados:
            if os.path.exists(os.path.join(RAIZ, c)):
                existentes.add(c)
    if len(existentes) < 4:
        falha("secao 11 cita %d caminhos existentes; o README exige 4 ou mais" % len(existentes))


def main():
    if not os.path.isfile(ARQUIVO):
        print("FALHA: docs/FDD.md nao existe")
        print("RESULTADO: FAIL")
        sys.exit(1)
    texto = open(ARQUIVO, encoding="utf-8").read()
    linhas = texto.split("\n")

    if EM_DASH in texto:
        falha("contem travessao (U+2014)")
    if EMOJI.search(texto):
        falha("contem emoji")
    for t in sorted(tokens_do_template()):
        if t in texto:
            falha("sobrou o placeholder do template %s" % t)

    cabecalho, secoes = separar_secoes(texto)
    primeira = next((l for l in linhas if l.strip()), "")
    if not re.match(r"^### FDD: \S", primeira):
        falha("a primeira linha deve ser '### FDD: nome da feature'")
    topo = "\n".join(linhas[:10])
    if not re.search(r"^Versão: \S", topo, re.M):
        falha("cabecalho sem 'Versão:'")
    if not re.search(r"^Data: \d{4}-\d{2}-\d{2}$", topo, re.M):
        falha("cabecalho sem 'Data: AAAA-MM-DD'")
    if not re.search(r"^Responsável: \S", topo, re.M):
        falha("cabecalho sem 'Responsável:'")

    numeros = [s[0] for s in secoes]
    titulos = [s[1] for s in secoes]
    if numeros != list(range(1, len(SECOES) + 1)) or titulos != SECOES:
        falha("secoes numeradas %s; esperado %s" % (list(zip(numeros, titulos)), list(enumerate(SECOES, 1))))
        finalizar()
    corpo = {n: c for n, _, c in secoes}

    if len(bullets(corpo[2])) < 3:
        falha("secao 2 precisa de 3 ou mais objetivos")
    for rotulo in ("**Incluído**", "**Excluído**"):
        if rotulo not in corpo[3]:
            falha("secao 3 sem o rotulo %s" % rotulo)
    inc = apos_rotulo(corpo[3], "**Incluído**")
    exc = apos_rotulo(corpo[3], "**Excluído**")
    if len(bullets(inc)) < 2 or len(bullets(exc)) < 2:
        falha("secao 3 precisa de 2 ou mais itens em Incluído e em Excluído")

    for rotulo in ("**Fluxo principal**", "**Fluxos alternativos e exceções**", "**Diagramas**"):
        if rotulo not in corpo[4]:
            falha("secao 4 sem o rotulo %s" % rotulo)
    baixo = corpo[4].lower()
    for palavra in ("outbox", "worker", "retry", "dlq"):
        if palavra not in baixo:
            falha("secao 4 nao cobre o fluxo %r" % palavra)
    if corpo[4].count("```mermaid") < 2:
        falha("secao 4 precisa de 2 ou mais diagramas Mermaid")

    validar_contratos(corpo[5])
    codigos = validar_erros(corpo[6])
    validar_observabilidade(corpo[7])

    cab8, dados8 = tabela(corpo[8])
    if cab8 != ["Versão mínima", "Componente", "Observações"]:
        falha("tabela da secao 8 deve ter o cabecalho | Versão mínima | Componente | Observações |")
    if len(dados8) < 5:
        falha("secao 8 precisa de 5 ou mais componentes")
    if not re.search(r"^Garantias de compatibilidade\s*\n- ", corpo[8], re.M):
        falha("secao 8 sem 'Garantias de compatibilidade' seguido de bullets")

    if len(bullets(corpo[9])) < 8:
        falha("secao 9 precisa de 8 ou mais criterios")
    validar_riscos(corpo[10])
    validar_integracao(corpo[11])

    # Consistencia global
    for c in sorted(set(re.findall(r"\bWEBHOOK_[A-Z_]+\b", texto))):
        if c not in codigos:
            falha("codigo %s citado mas ausente da matriz de erros" % c)
    inicios = inicios_transcricao()
    for h, n in CITACAO.findall(texto):
        if (h, n) not in inicios:
            falha("citacao inexistente na transcricao: [%s] %s" % (h, n))
    for l in linhas:
        for c in CAMINHO.findall(l):
            if not os.path.exists(os.path.join(RAIZ, c)) and "arquivo novo" not in l and "arquivos novos" not in l:
                falha("caminho inexistente sem o sufixo '(arquivo novo)': %s" % c)

    finalizar()


def finalizar():
    for p in problemas:
        print("FALHA: " + p)
    print("RESULTADO: " + ("PASS" if not problemas else "FAIL"))
    sys.exit(0 if not problemas else 1)


if __name__ == "__main__":
    main()
