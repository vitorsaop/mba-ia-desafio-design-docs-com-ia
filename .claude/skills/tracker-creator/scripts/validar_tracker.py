#!/usr/bin/env python3
"""Valida docs/TRACKER.md contra o formato do README e contra a transcricao e o codigo.

Uso: python3 .claude/skills/tracker-creator/scripts/validar_tracker.py [raiz-do-repositorio]
Saida: uma linha por problema e, no fim, "RESULTADO: PASS" ou "RESULTADO: FAIL".
"""
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
RAIZ = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.getcwd()
sys.argv = [sys.argv[0], "--raiz", RAIZ]
import enumerar_itens  # noqa: E402

ARQUIVO = os.path.join(RAIZ, "docs", "TRACKER.md")
TEMPLATE = os.path.join(AQUI, "..", "assets", "template-tracker.md")
CABECALHO = ["ID", "Documento", "Tipo", "Conteúdo (resumo)", "Fonte", "Localização"]
EM_DASH = "\u2014"
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50]")
TIPOS = {
    "Requisito Funcional", "Requisito Não Funcional", "Objetivo", "Escopo", "Decisão", "Trade-off",
    "Dependência", "Risco", "Critério de Aceite", "Teste", "Restrição", "Hipótese", "Contrato", "Erro",
    "Alternativa", "Questão em Aberto", "Fluxo", "Integração", "Observabilidade", "Resiliência",
    "Invariante", "Proposta", "Impacto",
}
CITACAO = re.compile(r"^\[(\d\d:\d\d)\] ([A-Za-zÀ-ÿ]+)$")

problemas = []


def falha(msg):
    problemas.append(msg)


def tokens_do_template():
    texto = open(TEMPLATE, encoding="utf-8").read()
    return {"[%s]" % t for t in re.findall(r"\[([^\[\]\n]{2,})\]", texto)}


def inicios_transcricao():
    s = set()
    for l in open(os.path.join(RAIZ, "TRANSCRICAO.md"), encoding="utf-8").read().split("\n"):
        m = re.match(r"^\[(\d\d:\d\d)\] ([^:]+):", l)
        if m:
            s.add((m.group(1), m.group(2)))
    return s


def main():
    if not os.path.isfile(ARQUIVO):
        print("FALHA: docs/TRACKER.md nao existe")
        print("RESULTADO: FAIL")
        sys.exit(1)
    texto = open(ARQUIVO, encoding="utf-8").read()
    if EM_DASH in texto:
        falha("contem travessao (U+2014)")
    if EMOJI.search(texto):
        falha("contem emoji")
    for t in sorted(tokens_do_template()):
        if t in texto:
            falha("sobrou o placeholder do template %s" % t)

    linhas = texto.split("\n")
    idx = next((i for i, l in enumerate(linhas) if l.startswith("| ID ")), None)
    if idx is None:
        falha("tabela sem a linha de cabecalho que comeca com '| ID '")
        finalizar()
    cab = [c.strip() for c in linhas[idx].strip().strip("|").split("|")]
    if cab != CABECALHO:
        falha("cabecalho %s; esperado %s" % (cab, CABECALHO))
    if not re.match(r"^\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|$", linhas[idx + 1]):
        falha("linha separadora da tabela invalida")

    inicios = inicios_transcricao()
    linhas_tabela = []
    for l in linhas[idx + 2 :]:
        if not l.startswith("|"):
            if l.strip():
                falha("texto depois da tabela: %r" % l[:60])
            continue
        celulas = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(celulas) != 6:
            falha("linha com %d colunas (esperado 6): %r" % (len(celulas), l[:60]))
            continue
        linhas_tabela.append(celulas)

    ids = set()
    n_transcricao = n_codigo = 0
    for id_, doc, tipo, resumo, fonte, loc in linhas_tabela:
        if not all([id_, doc, tipo, resumo, fonte, loc]):
            falha("linha %s com celula vazia" % (id_ or "?"))
            continue
        if id_ in ids:
            falha("ID repetido: %s" % id_)
        ids.add(id_)
        if not os.path.isfile(os.path.join(RAIZ, doc)):
            falha("%s: documento inexistente %s" % (id_, doc))
        if tipo not in TIPOS:
            falha("%s: Tipo %r fora de %s" % (id_, tipo, sorted(TIPOS)))
        if fonte == "TRANSCRICAO":
            n_transcricao += 1
            for parte in [p.strip() for p in loc.split(";")]:
                m = CITACAO.match(parte)
                if not m:
                    falha("%s: Localizacao %r nao esta no formato '[hh:mm] Nome'" % (id_, parte))
                elif (m.group(1), m.group(2)) not in inicios:
                    falha("%s: %s nao existe na transcricao" % (id_, parte))
        elif fonte == "CODIGO":
            n_codigo += 1
            for parte in [p.strip() for p in loc.split(";")]:
                caminho = re.sub(r":\d+$", "", parte.strip("`"))
                if not os.path.isfile(os.path.join(RAIZ, caminho)):
                    falha("%s: caminho de codigo inexistente %r" % (id_, parte))
        else:
            falha("%s: Fonte %r deve ser TRANSCRICAO ou CODIGO" % (id_, fonte))

    total = len(linhas_tabela)
    if total == 0:
        falha("tabela sem linhas")
    else:
        if n_transcricao * 100 < 70 * total:
            falha("so %.0f%% das linhas tem Fonte TRANSCRICAO; o README exige 70%% ou mais" % (100.0 * n_transcricao / total))
        if n_codigo < 5:
            falha("%d linhas com Fonte CODIGO; o README exige 5 ou mais" % n_codigo)

    esperados = {i[0]: i for i in enumerar_itens.todos()}
    faltando = sorted(set(esperados) - ids)
    cobertura = 100.0 * (len(esperados) - len(faltando)) / max(len(esperados), 1)
    print("linhas: %d | TRANSCRICAO: %d | CODIGO: %d | itens dos documentos: %d | cobertura: %.1f%%"
          % (total, n_transcricao, n_codigo, len(esperados), cobertura))
    if cobertura < 80:
        falha("cobertura de %.1f%%; o README exige 80%% ou mais. Faltam: %s" % (cobertura, ", ".join(faltando[:30])))
    elif faltando:
        print("AVISO: itens sem linha (%d): %s" % (len(faltando), ", ".join(faltando[:40])))
    for i in sorted(ids - set(esperados)):
        print("AVISO: ID %s nao corresponde a nenhum item enumerado dos documentos" % i)
    for id_, doc, *_ in linhas_tabela:
        if id_ in esperados and esperados[id_][1] != doc:
            falha("%s: Documento %s difere do enumerado %s" % (id_, doc, esperados[id_][1]))

    finalizar()


def finalizar():
    for p in problemas:
        print("FALHA: " + p)
    print("RESULTADO: " + ("PASS" if not problemas else "FAIL"))
    sys.exit(0 if not problemas else 1)


if __name__ == "__main__":
    main()
