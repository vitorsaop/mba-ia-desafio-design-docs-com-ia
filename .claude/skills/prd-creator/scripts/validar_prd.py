#!/usr/bin/env python3
"""Valida docs/PRD.md contra assets/template-prd.md e contra o README do desafio.

Uso: python3 .claude/skills/prd-creator/scripts/validar_prd.py [raiz-do-repositorio]
Saida: uma linha por problema e, no fim, "RESULTADO: PASS" ou "RESULTADO: FAIL".
"""
import os
import re
import sys

RAIZ = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
ARQUIVO = os.path.join(RAIZ, "docs", "PRD.md")
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "template-prd.md")

EM_DASH = "\u2014"
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50]")
VAGOS = ["etc.", "entre outros", "e assim por diante", "adequad", "robust"]
SECOES = [
    "Resumo",
    "Contexto e problema",
    "Objetivos e métricas",
    "Escopo",
    "Requisitos funcionais",
    "Requisitos não funcionais",
    "Arquitetura e abordagem",
    "Decisões e trade-offs",
    "Dependências",
    "Riscos e mitigação",
    "Critérios de aceitação",
    "Testes e validação",
]
ROTULOS_CONTEXTO = ["Público-alvo", "Cenários de uso chave", "Onde essa feature será implantada", "Problemas priorizados"]
ROTULOS_RNF = [
    "Performance",
    "Disponibilidade",
    "Segurança e autorização",
    "Observabilidade",
    "Confiabilidade e integridade de dados",
    "Compatibilidade e portabilidade",
    "Compliance",
    "Acessibilidade no frontend consumidor",
]
ROTULOS_ARQ = ["Abordagem", "Componentes", "Integrações"]
CITACAO = re.compile(r"\[(\d\d:\d\d)\] ([A-Za-zÀ-ÿ]+)")
CAMINHO = re.compile(
    r"`((?:src|prisma|tests|docs)/[A-Za-z0-9_./-]*[A-Za-z0-9_]|package\.json|docker-compose\.yml)(?::\d+)?`"
)

problemas = []


def falha(msg):
    problemas.append(msg)


def tokens_do_template():
    texto = open(TEMPLATE, encoding="utf-8").read()
    return {"[%s]" % t for t in re.findall(r"\[([^\[\]\n]{3,})\]", texto)}


def secoes(texto):
    partes = re.split(r"^### (.+)$", texto, flags=re.M)
    return partes[0], [(partes[i].strip(), partes[i + 1]) for i in range(1, len(partes), 2)]


def bullets(bloco):
    return [l for l in bloco.split("\n") if l.startswith("- ")]


def rotulos_com_bullets(corpo, rotulos, nome_secao):
    """Cada rotulo e uma linha sozinha, seguida de bullets; a ordem deve ser a do template."""
    ultimo = -1
    for r in rotulos:
        m = re.search(r"^%s\s*\n((?:- .+\n?)+)" % re.escape(r), corpo, re.M)
        if not m:
            falha("%s: rotulo %r ausente ou sem bullets" % (nome_secao, r))
            continue
        if m.start() < ultimo:
            falha("%s: rotulo %r fora de ordem" % (nome_secao, r))
        ultimo = m.start()


def tabela(bloco):
    linhas = [l for l in bloco.split("\n") if l.startswith("|")]
    if len(linhas) < 2:
        return [], []
    cab = [c.strip() for c in linhas[0].strip().strip("|").split("|")]
    return cab, [[c.strip() for c in l.strip().strip("|").split("|")] for l in linhas[2:]]


def validar_requisitos(corpo):
    blocos = re.split(r"^(?=#### )", corpo, flags=re.M)[1:]
    if len(blocos) < 8:
        falha("ha %d requisitos funcionais; o README exige 8 ou mais" % len(blocos))
    for esperado, b in enumerate(blocos, start=1):
        titulo = b.split("\n")[0]
        m = re.match(r"^#### FR-(\d{2}) \S", titulo)
        if not m or int(m.group(1)) != esperado:
            falha("requisito %d: titulo deve ser '#### FR-%02d Nome' (achei %r)" % (esperado, esperado, titulo))
            continue
        id_ = "FR-%02d" % esperado
        resto = b.split("\n", 1)[1].strip("\n")
        if not resto or resto.startswith("**"):
            falha("%s sem a linha de descricao logo abaixo do titulo" % id_)
        for rotulo in ("**Fluxo principal**", "**Fluxos alternativos e exceções**", "**Erros previstos**"):
            m2 = re.search(r"^%s\s*\n((?:- .+\n?)+)" % re.escape(rotulo), b, re.M)
            if not m2:
                falha("%s sem %s seguido de bullets" % (id_, rotulo))
            elif rotulo == "**Fluxo principal**" and len(bullets(m2.group(1))) < 2:
                falha("%s: Fluxo principal precisa de 2 ou mais passos" % id_)
        if not re.search(r"^\*\*Prioridade:\*\* (alta|media|baixa)$", b, re.M):
            falha("%s sem '**Prioridade:** alta|media|baixa'" % id_)


def validar_riscos(corpo):
    blocos = re.split(r"^(?=#### )", corpo, flags=re.M)[1:]
    if len(blocos) < 2:
        falha("ha %d riscos; o README exige 2 ou mais" % len(blocos))
    for b in blocos:
        titulo = b.split("\n")[0]
        if not re.search(r"^- \*\*Probabilidade:\*\* (baixa|media|alta)$", b, re.M):
            falha("risco %r sem '- **Probabilidade:** baixa|media|alta'" % titulo)
        if not re.search(r"^- \*\*Impacto:\*\* \S", b, re.M):
            falha("risco %r sem Impacto" % titulo)
        if not re.search(r"^- \*\*Mitigação:\*\*\s*\n\s{2,}- \S", b, re.M):
            falha("risco %r sem Mitigacao com sub-bullets" % titulo)
        if not re.search(r"^- \*\*Plano de contingência:\*\* \S", b, re.M):
            falha("risco %r sem Plano de contingencia" % titulo)


def main():
    if not os.path.isfile(ARQUIVO):
        print("FALHA: docs/PRD.md nao existe")
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
    baixo = texto.lower()
    for v in VAGOS:
        if v in baixo:
            falha("termo vago proibido: %r" % v)
    if sum(1 for l in linhas if l.strip() == "---") < 10:
        falha("faltam separadores '---' entre as secoes (minimo 10)")

    cabecalho, partes = secoes(texto)
    if not re.match(r"^### PRD: \S", linhas[0]):
        falha("a primeira linha deve ser '### PRD: produto feature'")
    topo = "\n".join(linhas[:8])
    if not re.search(r"^Versão: \S", topo, re.M):
        falha("cabecalho sem 'Versão:'")
    if not re.search(r"^Data: \d{4}-\d{2}-\d{2}$", topo, re.M):
        falha("cabecalho sem 'Data: AAAA-MM-DD'")
    if not re.search(r"^Responsável: \S", topo, re.M):
        falha("cabecalho sem 'Responsável:'")

    titulos = [t for t, _ in partes]
    # o titulo do documento tambem e um '### ': PRD: ...
    if not titulos or not titulos[0].startswith("PRD:"):
        falha("titulo do documento ausente")
    if titulos[1:] != SECOES:
        falha("secoes %s; esperado %s" % (titulos[1:], SECOES))
        finalizar()
    corpo = {t: c for t, c in partes[1:]}

    if len(corpo["Resumo"].strip().strip("-").strip()) < 80:
        falha("Resumo muito curto")

    rotulos_com_bullets(corpo["Contexto e problema"], ROTULOS_CONTEXTO, "Contexto e problema")

    cab, dados = tabela(corpo["Objetivos e métricas"])
    if cab != ["Objetivo", "Métrica", "Meta"]:
        falha("tabela de objetivos deve ter o cabecalho | Objetivo | Métrica | Meta |")
    if not dados:
        falha("tabela de objetivos sem linhas")
    for d in dados:
        if len(d) != 3 or not all(d):
            falha("linha de objetivo incompleta: %r" % d)
        elif not re.search(r"\d", d[2]):
            falha("meta sem valor numerico: %r" % d[2])

    esc = corpo["Escopo"]
    m_inc = re.search(r"^Incluso\s*\n((?:- .+\n?)+)", esc, re.M)
    m_fora = re.search(r"^Fora de escopo\s*\n((?:- .+\n?)+)", esc, re.M)
    if not m_inc or len(bullets(m_inc.group(1))) < 3:
        falha("Escopo: 'Incluso' ausente ou com menos de 3 itens")
    if not m_fora or len(bullets(m_fora.group(1))) < 2:
        falha("Escopo: 'Fora de escopo' ausente ou com menos de 2 itens (README)")

    validar_requisitos(corpo["Requisitos funcionais"])

    rnf = corpo["Requisitos não funcionais"]
    rotulos_com_bullets(rnf, ROTULOS_RNF, "Requisitos não funcionais")
    disp = re.search(r"^Disponibilidade\s*\n((?:- .+\n?)+)", rnf, re.M)
    if disp and "Hipótese" not in disp.group(1) and "%" not in disp.group(1):
        falha("Disponibilidade sem meta numerica deve conter 'Hipótese:'")
    if disp and "%" in disp.group(1) and "Hipótese" not in disp.group(1):
        falha("Disponibilidade com porcentagem sem origem na reuniao: marque como 'Hipótese:'")

    rotulos_com_bullets(corpo["Arquitetura e abordagem"], ROTULOS_ARQ, "Arquitetura e abordagem")

    decs = re.split(r"^(?=#### )", corpo["Decisões e trade-offs"], flags=re.M)[1:]
    if len(decs) < 5:
        falha("Decisoes e trade-offs tem %d decisoes; o plano preve 7" % len(decs))
    for d in decs:
        t = d.split("\n")[0]
        if not t.startswith("#### Decisão: "):
            falha("titulo de decisao fora do padrao '#### Decisão: ...': %r" % t)
        if not re.search(r"^- \*\*Justificativa:\*\* \S", d, re.M) or not re.search(r"^- \*\*Trade-off:\*\* \S", d, re.M):
            falha("decisao %r sem Justificativa e Trade-off" % t)

    deps = re.split(r"^(?=#### )", corpo["Dependências"], flags=re.M)[1:]
    if not deps:
        falha("Dependencias vazia")
    for d in deps:
        t = d.split("\n")[0]
        if not re.match(r"^#### (organizacional|técnica|externa): \S", t):
            falha("dependencia fora do padrao '#### organizacional|técnica|externa: titulo': %r" % t)
        if len(d.split("\n", 1)[-1].strip()) < 20:
            falha("dependencia %r sem descricao" % t)

    validar_riscos(corpo["Riscos e mitigação"])

    ca = corpo["Critérios de aceitação"]
    if "Checklist objetivo que define se a feature está pronta." not in ca:
        falha("Criterios de aceitacao sem a linha 'Checklist objetivo que define se a feature está pronta.'")
    if len(bullets(ca)) < 8:
        falha("Criterios de aceitacao tem %d itens; o plano preve 11" % len(bullets(ca)))

    rotulos_com_bullets(corpo["Testes e validação"], ["Tipos de teste obrigatórios", "Estratégia de validação"], "Testes e validação")

    inicios = set()
    for l in open(os.path.join(RAIZ, "TRANSCRICAO.md"), encoding="utf-8").read().split("\n"):
        m = re.match(r"^\[(\d\d:\d\d)\] ([^:]+):", l)
        if m:
            inicios.add((m.group(1), m.group(2)))
    for h, n in CITACAO.findall(texto):
        if (h, n) not in inicios:
            falha("citacao inexistente na transcricao: [%s] %s" % (h, n))
    for l in linhas:
        for c in CAMINHO.findall(l):
            if not os.path.exists(os.path.join(RAIZ, c)) and "arquivo novo" not in l and "arquivos novos" not in l:
                falha("caminho inexistente no repositorio: %s" % c)

    finalizar()


def finalizar():
    for p in problemas:
        print("FALHA: " + p)
    print("RESULTADO: " + ("PASS" if not problemas else "FAIL"))
    sys.exit(0 if not problemas else 1)


if __name__ == "__main__":
    main()
