#!/usr/bin/env python3
"""Valida docs/RFC.md contra assets/template-rfc.md e contra o README do desafio.

Uso: python3 .claude/skills/rfc-creator/scripts/validar_rfc.py [raiz-do-repositorio]
Saida: uma linha por problema e, no fim, "RESULTADO: PASS" ou "RESULTADO: FAIL".
"""
import os
import re
import sys

RAIZ = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
ARQUIVO = os.path.join(RAIZ, "docs", "RFC.md")
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "template-rfc.md")

EM_DASH = "\u2014"
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50]")
SECOES = [
    "Metadados",
    "Resumo executivo (TL;DR)",
    "Contexto e problema",
    "Proposta técnica",
    "Alternativas consideradas",
    "Questões em aberto",
    "Impacto e riscos",
    "Decisões relacionadas",
]
STATUS_OK = {"Rascunho", "Em revisão", "Aprovado", "Rejeitado"}
REVISORES = ["Larissa", "Marcos", "Bruno", "Diego", "Sofia"]
CITACAO = re.compile(r"\[(\d\d:\d\d)\] ([A-Za-zÀ-ÿ]+)")
CAMINHO = re.compile(r"`((?:src|prisma|tests|docs)/[A-Za-z0-9_./-]+|package\.json|docker-compose\.yml)(?::\d+)?`")

problemas = []


def falha(msg):
    problemas.append(msg)


def tokens_do_template():
    texto = open(TEMPLATE, encoding="utf-8").read()
    return {"[%s]" % t for t in re.findall(r"\[([^\[\]\n]{3,})\]", texto)}


def secao(texto, titulo):
    m = re.search(r"^### %s\s*\n(.*?)(?=^### |\Z)" % re.escape(titulo), texto, re.S | re.M)
    return m.group(1) if m else ""


def bullets(bloco):
    return [l for l in bloco.split("\n") if l.startswith("- ")]


def transcricao_inicios():
    inicios = set()
    for l in open(os.path.join(RAIZ, "TRANSCRICAO.md"), encoding="utf-8").read().split("\n"):
        m = re.match(r"^\[(\d\d:\d\d)\] ([^:]+):", l)
        if m:
            inicios.add((m.group(1), m.group(2)))
    return inicios


def main():
    if not os.path.isfile(ARQUIVO):
        print("FALHA: docs/RFC.md nao existe")
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

    h3 = [l[4:].strip() for l in linhas if l.startswith("### ")]
    if not h3 or not re.match(r"^RFC-\d{3}: \S", h3[0]):
        falha("o primeiro titulo deve ser '### RFC-NNN: titulo'")
    if h3[1:] != SECOES:
        falha("secoes %s; esperado %s" % (h3[1:], SECOES))
        print_resultado()

    # Metadados
    meta = secao(texto, "Metadados")
    linhas_meta = [l for l in meta.split("\n") if l.startswith("|")]
    cab = [c.strip() for c in linhas_meta[0].strip("|").split("|")] if linhas_meta else []
    if cab != ["Campo", "Valor"]:
        falha("tabela de Metadados deve ter o cabecalho | Campo | Valor |")
    campos = {}
    for l in linhas_meta[2:]:
        c = [x.strip() for x in l.strip("|").split("|")]
        if len(c) == 2:
            campos[c[0]] = c[1]
    for c in ["Autor", "Status", "Data", "Revisores"]:
        if not campos.get(c):
            falha("Metadados sem o campo %s" % c)
    if campos.get("Status") not in STATUS_OK:
        falha("Status invalido: %r" % campos.get("Status"))
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", campos.get("Data", "")):
        falha("Data fora do formato AAAA-MM-DD")
    for r in REVISORES:
        if r not in campos.get("Revisores", ""):
            falha("revisor ausente: %s" % r)

    # Proposta
    if len(bullets(secao(texto, "Proposta técnica"))) < 3:
        falha("Proposta tecnica precisa de ao menos 3 bullets")

    # Alternativas
    alts = bullets(secao(texto, "Alternativas consideradas"))
    if len(alts) < 2:
        falha("Alternativas consideradas tem %d itens; o README exige 2 ou mais" % len(alts))
    for a in alts:
        if "**Trade-off do descarte:**" not in a:
            falha("alternativa sem '**Trade-off do descarte:**': %s" % a[:60])
        if not CITACAO.search(a):
            falha("alternativa sem citacao [hh:mm] Nome: %s" % a[:60])

    # Questoes em aberto
    qs = bullets(secao(texto, "Questões em aberto"))
    adiadas = [q for q in qs if q.startswith("- **Adiada na reunião.**")]
    analise = [q for q in qs if q.startswith("- **Lacuna identificada na análise.**")]
    if len(adiadas) < 2:
        falha("Questoes em aberto tem %d adiadas na reuniao; o README exige 2 ou mais" % len(adiadas))
    if len(adiadas) + len(analise) != len(qs):
        falha("toda questao deve comecar com '**Adiada na reunião.**' ou '**Lacuna identificada na análise.**'")
    for q in adiadas:
        if not CITACAO.search(q):
            falha("questao adiada sem citacao [hh:mm] Nome: %s" % q[:60])

    # Impacto e riscos
    ir = secao(texto, "Impacto e riscos")
    if "**Impacto no sistema existente**" not in ir or "**Riscos**" not in ir:
        falha("Impacto e riscos precisa dos rotulos '**Impacto no sistema existente**' e '**Riscos**'")
    else:
        antes, depois = ir.split("**Riscos**", 1)
        if not bullets(antes) or not bullets(depois):
            falha("Impacto e riscos precisa de bullets nos dois rotulos")

    # Links para ADRs
    dec = secao(texto, "Decisões relacionadas")
    links = re.findall(r"\[(ADR-\d{3}[^\]]*)\]\((adrs/ADR-\d{3}-[a-z0-9-]+\.md)\)", dec)
    validos = [l for l in links if os.path.isfile(os.path.join(RAIZ, "docs", l[1]))]
    if len(validos) < 2:
        falha("Decisoes relacionadas tem %d links validos para ADRs; o README exige 2 ou mais" % len(validos))
    for l in links:
        if l not in validos:
            falha("link para ADR inexistente: %s" % l[1])
    dir_adrs = os.path.join(RAIZ, "docs", "adrs")
    if os.path.isdir(dir_adrs):
        existentes = {a for a in os.listdir(dir_adrs) if re.match(r"^ADR-\d{3}-.+\.md$", a)}
        linkados = {os.path.basename(l[1]) for l in validos}
        for faltando in sorted(existentes - linkados):
            falha("ADR existente nao linkado: %s" % faltando)

    # Tamanho: 2 a 4 paginas
    palavras = len(re.sub(r"[|#*`\-]", " ", texto).split())
    if not 700 <= palavras <= 2300:
        falha("tem %d palavras; 2 a 4 paginas equivalem a 700 a 2300" % palavras)

    # Citacoes e caminhos
    inicios = transcricao_inicios()
    for h, n in CITACAO.findall(texto):
        if (h, n) not in inicios:
            falha("citacao inexistente na transcricao: [%s] %s" % (h, n))
    for c in CAMINHO.findall(texto):
        if not os.path.exists(os.path.join(RAIZ, c)):
            falha("caminho inexistente no repositorio: %s" % c)

    print_resultado()


def print_resultado():
    for p in problemas:
        print("FALHA: " + p)
    print("RESULTADO: " + ("PASS" if not problemas else "FAIL"))
    sys.exit(0 if not problemas else 1)


if __name__ == "__main__":
    main()
