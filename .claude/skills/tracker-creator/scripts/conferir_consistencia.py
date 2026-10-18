#!/usr/bin/env python3
"""Confere a consistencia entre PRD, RFC, FDD e ADRs depois de uma correcao.

A TRANSCRICAO.md e a fonte da verdade. Um fato que a reuniao nao decidiu precisa aparecer com o
rotulo "Hipotese" em todo documento em que aparece, e frases corrigidas nao podem voltar.

Uso: python3 .claude/skills/tracker-creator/scripts/conferir_consistencia.py [raiz-do-repositorio]
Saida: uma linha por problema e, no fim, "RESULTADO: PASS" ou "RESULTADO: FAIL".
"""
import glob
import os
import re
import sys

RAIZ = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()

# Frases que ja foram corrigidas e nao podem voltar (regex, motivo).
PROIBIDAS = [
    (r"quatro headers", "o envio tem cinco headers (X-Event-Id, X-Signature, X-Timestamp, X-Webhook-Id, Content-Type)"),
    (r"Quatro peças", "a proposta do RFC tem seis elementos"),
    (r"no máximo 6 requisições por evento", "o limite vale por ciclo de entrega; um replay inicia novo ciclo"),
    (r"A criação de pedido não grava evento", "a reuniao nao decidiu se a criacao de pedido gera evento"),
    (r"a resposta de `changeStatus` não mudam?", "so a resposta de sucesso nao muda; ha um erro novo de payload"),
    (r"Nenhuma dependência nova e nenhuma infraestrutura nova", "dependencia npm nova e hipotese"),
    (r"(?<!pelo menos )(?<!pelo menos\d)\b(dois|2) dias úteis", "Sofia disse 'pelo menos dois dias uteis'"),
]

# Fatos derivados: a linha (ou o titulo com o paragrafo seguinte) precisa trazer um destes rotulos.
HIPOTESE = r"Hipótese|hipótese|Interpretação|interpretação|Lacuna identificada na análise|Limitação identificada|Consequência identificada"
ROTULADAS = [
    (r"6 requisições", HIPOTESE, "interpretacao de '5 tentativas'"),
    (r"\b422\b", HIPOTESE, "rollback e status 422 do limite de 64 KB"),
    (r"2 KB", HIPOTESE, "truncamento da resposta do cliente"),
    (r"previousSecretExpiresAt|informa quando ela expira", HIPOTESE, "campo de expiracao da secret anterior"),
    (r"fora de logs|em logs nem|nunca aparece em logs|não aparece em logs", HIPOTESE, "secret fora de logs e de leituras"),
    (r"dependência npm|dependência nova|biblioteca nova", HIPOTESE, "nenhuma dependencia nova"),
    (r"(5|cinco|Cinco) retentativas", HIPOTESE, "interpretacao de '5 tentativas'"),
    (r"já reprocessad|um segundo replay|ALREADY_REPLAYED", HIPOTESE, "semantica do replay"),
]
# Pares que valem so para PRD, RFC e FDD (nos ADRs o nome da opcao repete a decisao e o marcador cobre a lacuna).
SO_FORA_DOS_ADRS = {r"(5|cinco|Cinco) retentativas"}

problemas = []


def unidades(texto):
    """Linhas fora de blocos de codigo; um titulo '#' leva junto as linhas ate a linha em branco."""
    dentro = False
    linhas = []
    for l in texto.split("\n"):
        if l.lstrip().startswith("```"):
            dentro = not dentro
            continue
        if not dentro:
            linhas.append(l)
    saida = []
    i = 0
    while i < len(linhas):
        l = linhas[i]
        if l.startswith("#"):
            bloco = [l]
            j = i + 1
            while j < len(linhas) and linhas[j].strip():
                bloco.append(linhas[j])
                j += 1
            saida.append(" ".join(bloco))
        else:
            saida.append(l)
        i += 1
    return saida


def desquebrar(texto):
    sys.path.insert(0, os.path.join(RAIZ, ".claude", "skills", "adr-creator", "scripts"))
    import quebrar_linhas
    return quebrar_linhas.juntar_continuacoes(texto)


def main():
    arquivos = [os.path.join(RAIZ, "docs", n) for n in ("PRD.md", "RFC.md", "FDD.md")]
    arquivos += sorted(glob.glob(os.path.join(RAIZ, "docs", "adrs", "ADR-*.md")))
    for caminho in arquivos:
        if not os.path.isfile(caminho):
            problemas.append("%s: arquivo ausente" % os.path.relpath(caminho, RAIZ))
            continue
        rel = os.path.relpath(caminho, RAIZ)
        texto = open(caminho, encoding="utf-8").read()
        eh_adr = "/adrs/" in caminho
        if eh_adr:
            texto = desquebrar(texto)
        sem_codigo = "\n".join(u for u in unidades(texto))
        for padrao, motivo in PROIBIDAS:
            for m in re.finditer(padrao, sem_codigo):
                problemas.append("%s: frase proibida %r (%s)" % (rel, m.group(0), motivo))
        for u in unidades(texto):
            for padrao, rotulo, assunto in ROTULADAS:
                if padrao in SO_FORA_DOS_ADRS and eh_adr:
                    continue
                if re.search(padrao, u) and not re.search(rotulo, u):
                    problemas.append("%s: falta rotulo de hipotese (%s): %s" % (rel, assunto, u.strip()[:110]))
    for p in problemas:
        print("FALHA: " + p)
    print("RESULTADO: " + ("PASS" if not problemas else "FAIL"))
    sys.exit(0 if not problemas else 1)


if __name__ == "__main__":
    main()
