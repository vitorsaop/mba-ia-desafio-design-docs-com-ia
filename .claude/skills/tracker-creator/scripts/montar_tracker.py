#!/usr/bin/env python3
"""Monta docs/TRACKER.md a partir dos itens enumerados e de um arquivo de proveniencia.

O arquivo de proveniencia tem uma linha por item, separada por tabulacao:
    ID <TAB> Tipo (vazio usa o sugerido pelo enumerador) <TAB> Fonte <TAB> Localizacao
Linhas que comecam com # e linhas vazias sao ignoradas.

Uso: python3 .claude/skills/tracker-creator/scripts/montar_tracker.py [--mapa caminho.tsv]
O mapa padrao e .claude/plano/FONTES-TRACKER.tsv. Termina com erro se faltar ou sobrar ID.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
RAIZ = os.getcwd()
MAPA = os.path.join(RAIZ, ".claude", "plano", "FONTES-TRACKER.tsv")
for i, a in enumerate(sys.argv):
    if a == "--mapa" and i + 1 < len(sys.argv):
        MAPA = os.path.abspath(sys.argv[i + 1])
sys.argv = [sys.argv[0], "--raiz", RAIZ]
import enumerar_itens  # noqa: E402

LEGENDA = (
    "Este Tracker liga cada item dos documentos do pacote (PRD, RFC, FDD e ADRs) à sua origem. "
    "Fonte `TRANSCRICAO` indica uma fala de `TRANSCRICAO.md` e a Localização traz `[hh:mm] Nome`. "
    "Fonte `CODIGO` indica um arquivo do repositório e a Localização traz o caminho, com `:linha` quando o ponto é específico.\n\n"
    "O Tipo `Hipótese` marca uma proposta que a reunião não decidiu: a Localização aponta a fala em que a lacuna nasceu. "
    "Prioridades dos requisitos, probabilidades e impactos dos riscos e tipos de teste são avaliação do autor; a Localização aponta a fala que originou o item. "
    "Os IDs seguem o padrão `DOCUMENTO-TIPO-NN`, por exemplo `PRD-FR-01`, `RFC-ALT-02`, `FDD-CONTRATO-03` e `ADR-002`."
)


def ler_mapa():
    if not os.path.isfile(MAPA):
        raise SystemExit(
            "Arquivo de proveniencia nao encontrado: %s\n"
            "Crie-o com uma linha por ID (ID, Tipo ou vazio, Fonte, Localizacao, separados por tabulacao); "
            "a lista de IDs vem de enumerar_itens.py. Ele e um arquivo de trabalho local, nao versionado." % MAPA
        )
    mapa = {}
    for n, linha in enumerate(open(MAPA, encoding="utf-8").read().split("\n"), 1):
        if not linha.strip() or linha.startswith("#"):
            continue
        partes = linha.split("\t")
        if len(partes) != 4:
            raise SystemExit("%s:%d: esperadas 4 colunas separadas por tabulacao" % (MAPA, n))
        id_, tipo, fonte, loc = [p.strip() for p in partes]
        if id_ in mapa:
            raise SystemExit("%s:%d: ID repetido %s" % (MAPA, n, id_))
        mapa[id_] = (tipo, fonte, loc)
    return mapa


def main():
    itens = enumerar_itens.todos()
    mapa = ler_mapa()
    ids = [i[0] for i in itens]
    faltando = [i for i in ids if i not in mapa]
    sobrando = [i for i in mapa if i not in set(ids)]
    if faltando or sobrando:
        if faltando:
            print("IDs sem proveniencia: " + ", ".join(faltando))
        if sobrando:
            print("IDs do mapa que nao existem nos documentos: " + ", ".join(sobrando))
        sys.exit(1)
    linhas = ["# Tracker de Rastreabilidade", "", LEGENDA, ""]
    linhas.append("| ID | Documento | Tipo | Conteúdo (resumo) | Fonte | Localização |")
    linhas.append("| --- | --- | --- | --- | --- | --- |")
    for id_, doc, tipo_sugerido, texto in itens:
        tipo, fonte, loc = mapa[id_]
        linhas.append(
            "| %s | %s | %s | %s | %s | %s |"
            % (id_, doc, tipo or tipo_sugerido, enumerar_itens.resumo(texto), fonte, loc)
        )
    destino = os.path.join(RAIZ, "docs", "TRACKER.md")
    open(destino, "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    print("TRACKER.md montado com %d linhas" % len(itens))


if __name__ == "__main__":
    main()
