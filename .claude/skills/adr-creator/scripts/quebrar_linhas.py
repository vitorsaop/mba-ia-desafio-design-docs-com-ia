#!/usr/bin/env python3
"""Quebra linhas longas dos ADRs em 88 colunas, sem alterar o conteudo.

O limite de 100 a 250 linhas do professor conta linhas fisicas. Texto corrido escrito em uma linha so
nunca chega a 100, entao os paragrafos e os itens de lista sao quebrados em 88 colunas, o padrao de
arquivos Markdown em repositorios. O script e idempotente.

Uso: python3 .claude/skills/adr-creator/scripts/quebrar_linhas.py [raiz-do-repositorio]
"""
import glob
import os
import re
import sys
import textwrap

RAIZ = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
LIMITE = 88


def quebrar(texto):
    saida = []
    for linha in texto.split("\n"):
        if len(linha) <= LIMITE or linha.startswith(("#", "|", "```")):
            saida.append(linha)
            continue
        item = re.match(r"^(\s*(?:[-*]|\d+\.)\s+)", linha)
        if item:
            prefixo = item.group(1)
            saida.extend(
                textwrap.wrap(
                    linha[len(prefixo):],
                    LIMITE,
                    initial_indent=prefixo,
                    subsequent_indent=" " * len(prefixo),
                    break_long_words=False,
                    break_on_hyphens=False,
                )
            )
        else:
            saida.extend(textwrap.wrap(linha, LIMITE, break_long_words=False, break_on_hyphens=False))
    return "\n".join(saida)


def juntar_continuacoes(texto):
    """Desfaz quebras anteriores para o script ser idempotente: junta linhas de continuacao."""
    linhas = texto.split("\n")
    saida = []
    for i, linha in enumerate(linhas):
        anterior = saida[-1] if saida else ""
        continuacao = (
            i > 0
            and linha.strip()
            and anterior.strip()
            and not re.match(r"^(\s*([-*]|\d+\.)\s+|#|\||```|\*\*(Status|Data|ADRs Relacionados):)", linha)
            and not anterior.startswith(("#", "|", "```"))
            and not re.match(r"^\*\*(Status|Data|ADRs Relacionados):\*\*", anterior)
        )
        if continuacao:
            saida[-1] = anterior.rstrip() + " " + linha.strip()
        else:
            saida.append(linha)
    return "\n".join(saida)


def main():
    arquivos = sorted(glob.glob(os.path.join(RAIZ, "docs", "adrs", "ADR-*.md")))
    for caminho in arquivos:
        original = open(caminho, encoding="utf-8").read()
        novo = quebrar(juntar_continuacoes(original))
        if novo != original:
            open(caminho, "w", encoding="utf-8").write(novo)
            print("quebrado: " + os.path.relpath(caminho, RAIZ))
        else:
            print("sem mudanca: " + os.path.relpath(caminho, RAIZ))


if __name__ == "__main__":
    main()
