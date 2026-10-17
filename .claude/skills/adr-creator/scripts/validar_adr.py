#!/usr/bin/env python3
"""Valida os ADRs de docs/adrs/ contra o template MADR em pt-BR e contra o README do desafio.

Uso: python3 .claude/skills/adr-creator/scripts/validar_adr.py [raiz-do-repositorio]
Saida: uma linha por problema e, no fim, "RESULTADO: PASS" ou "RESULTADO: FAIL".
"""
import os
import re
import sys

RAIZ = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
DIR_ADRS = os.path.join(RAIZ, "docs", "adrs")
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "template-adr.md")

EM_DASH = "—"
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐]")
SECOES = [
    "Contexto e Declaração do Problema",
    "Fatores de Decisão",
    "Alternativas Consideradas",
    "Decisão",
    "Prós e Contras das Alternativas",
    "Consequências",
    "Referências",
]
STATUS_OK = {"Aceito", "Proposto", "Obsoleto", "Substituído"}
DECISOES = {
    "Outbox no MySQL": ["outbox"],
    "Retry com backoff e DLQ": ["retry", "dlq"],
    "HMAC-SHA256 com secret por endpoint": ["hmac"],
    "At-least-once com X-Event-Id": ["at-least-once"],
    "Worker em processo separado em polling": ["worker", "polling"],
    "Reuso dos padroes existentes": ["reuso"],
}
NOME_ARQUIVO = re.compile(r"^ADR-(\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
PERMITIDOS_CAMEL = {"MySQL", "PostgreSQL", "GitHub", "TypeScript", "JavaScript", "NodeJS"}
FRASES_FUTURAS = ["considere ", "avalie ", "se o volume", "pode ser necessário no futuro"]

problemas = []


def falha(arquivo, msg):
    problemas.append("%s: %s" % (arquivo, msg))


def tokens_do_template():
    texto = open(TEMPLATE, encoding="utf-8").read()
    tokens = set(re.findall(r"\[([^\[\]\n]{3,})\]", texto))
    return {"[%s]" % t for t in tokens if not t.startswith("PRECISA")}


def corpo_secao(texto, titulo):
    m = re.search(r"^## %s\s*\n(.*?)(?=^## |\Z)" % re.escape(titulo), texto, re.S | re.M)
    return m.group(1).strip("\n") if m else ""


def paragrafos(bloco):
    return [p for p in re.split(r"\n\s*\n", bloco.strip()) if p.strip()]


def validar_adr(caminho, tokens):
    nome = os.path.basename(caminho)
    m = NOME_ARQUIVO.match(nome)
    if not m:
        falha(nome, "nome fora do padrao ADR-NNN-titulo-em-kebab-case.md")
        return
    numero = m.group(1)
    texto = open(caminho, encoding="utf-8").read()
    linhas = texto.rstrip("\n").split("\n")

    if not 100 <= len(linhas) <= 250:
        falha(nome, "tem %d linhas; o limite e de 100 a 250" % len(linhas))
    if EM_DASH in texto:
        falha(nome, "contem travessao (U+2014)")
    if EMOJI.search(texto):
        falha(nome, "contem emoji")
    for t in sorted(tokens):
        if t in texto:
            falha(nome, "sobrou o placeholder do template %s" % t)
    if any(l.lstrip().startswith("```") for l in linhas):
        falha(nome, "contem bloco de codigo")

    titulo = re.match(r"^# ADR-(\d{3}): \S.*$", linhas[0])
    if not titulo:
        falha(nome, "primeira linha deve ser '# ADR-%s: titulo'" % numero)
    elif titulo.group(1) != numero:
        falha(nome, "numero do titulo (%s) difere do nome do arquivo (%s)" % (titulo.group(1), numero))

    # Cabecalho: apenas Status, Data e ADRs Relacionados
    cabecalho = []
    for l in linhas[1:]:
        if l.startswith("## "):
            break
        if l.strip():
            cabecalho.append(l)
    campos = {}
    for l in cabecalho:
        c = re.match(r"^\*\*(Status|Data|ADRs Relacionados):\*\* (.+)$", l)
        if not c:
            falha(nome, "linha de cabecalho nao permitida: %r" % l)
        else:
            campos[c.group(1)] = c.group(2).strip()
    if campos.get("Status") not in STATUS_OK:
        falha(nome, "Status ausente ou invalido (use %s)" % ", ".join(sorted(STATUS_OK)))
    if not re.match(r"^\d{2}-\d{2}-\d{4}$", campos.get("Data", "")):
        falha(nome, "Data ausente ou fora do formato DD-MM-AAAA")
    if "ADRs Relacionados" in campos:
        for ref in re.findall(r"ADR-\d{3}", campos["ADRs Relacionados"]):
            if ref == "ADR-" + numero:
                falha(nome, "ADRs Relacionados cita o proprio ADR")

    secoes = [l[3:].strip() for l in linhas if l.startswith("## ")]
    if secoes != SECOES:
        falha(nome, "secoes %s; esperado %s" % (secoes, SECOES))
        return

    contexto = corpo_secao(texto, "Contexto e Declaração do Problema")
    if len(paragrafos(contexto)) > 3 or len(contexto.split()) > 300:
        falha(nome, "Contexto passa de 3 paragrafos ou de 300 palavras")

    fatores = [l for l in corpo_secao(texto, "Fatores de Decisão").split("\n") if l.startswith("- ")]
    if not 4 <= len(fatores) <= 6:
        falha(nome, "Fatores de Decisao tem %d itens; o limite e de 4 a 6" % len(fatores))

    opcoes = [l for l in corpo_secao(texto, "Alternativas Consideradas").split("\n") if re.match(r"^\d+\. ", l)]
    if not 2 <= len(opcoes) <= 3:
        falha(nome, "Alternativas Consideradas tem %d itens; o limite e de 2 a 3" % len(opcoes))

    if not corpo_secao(texto, "Decisão").startswith('Opção escolhida: "'):
        falha(nome, "Decisao deve comecar com 'Opção escolhida: \"...\"'")

    pc = corpo_secao(texto, "Prós e Contras das Alternativas")
    subs = re.findall(r"^### (.+)$", pc, re.M)
    if len(subs) != len(opcoes):
        falha(nome, "Pros e Contras tem %d subsecoes; ha %d alternativas" % (len(subs), len(opcoes)))
    for bloco in re.split(r"^### .+$", pc, flags=re.M)[1:]:
        bons = len(re.findall(r"^- Bom, porque ", bloco, re.M))
        ruins = len(re.findall(r"^- Ruim, porque ", bloco, re.M))
        if bons < 1 or ruins < 1 or bons + ruins > 4:
            falha(nome, "cada alternativa precisa de 'Bom' e 'Ruim' e de no maximo 4 itens")

    cons = paragrafos(corpo_secao(texto, "Consequências"))
    rotulos = ["**Positivas:**", "**Negativas:**", "**Trade-off:**"]
    if len(cons) != 3 or [p[: len(r)] for p, r in zip(cons, rotulos)] != rotulos:
        falha(nome, "Consequencias deve ter 3 paragrafos iniciados por %s" % ", ".join(rotulos))

    refs = [l for l in corpo_secao(texto, "Referências").split("\n") if l.strip()]
    if not 3 <= len(refs) <= 5:
        falha(nome, "Referencias tem %d itens; o limite e de 3 a 5" % len(refs))
    for l in refs:
        r = re.match(r"^- `([^`:]+):(\d+)`$", l)
        if not r:
            falha(nome, "referencia fora do formato '- `caminho:linha`': %r" % l)
            continue
        alvo = os.path.join(RAIZ, r.group(1))
        if not os.path.isfile(alvo):
            falha(nome, "referencia a arquivo inexistente: %s" % r.group(1))
        elif int(r.group(2)) > len(open(alvo, encoding="utf-8").read().split("\n")):
            falha(nome, "linha %s alem do fim de %s" % (r.group(2), r.group(1)))

    if len(re.findall(r"\[PRECISA DE INFORMAÇÃO: [^\]]+\]", texto)) > 4 or texto.count("[PRECISA") > 4:
        falha(nome, "mais de 4 marcadores [PRECISA DE INFORMAÇÃO: ...]")

    # Conteudo proibido fora da secao Referencias
    sem_refs = texto.split("## Referências")[0]
    if "`" in sem_refs:
        falha(nome, "crase (nome de codigo) fora da secao Referencias")
    if re.search(r"/api/|\b(GET|POST|PATCH|DELETE) /", sem_refs):
        falha(nome, "endpoint no texto")
    if re.search(r"\b[a-z]{2,}_[a-z_]{2,}\b", sem_refs):
        falha(nome, "identificador snake_case (tabela ou coluna) no texto")
    for palavra in re.findall(r"\b[a-z]+[A-Z][A-Za-z]+\b|\b[A-Z][a-z]+[A-Z][A-Za-z]*\b", sem_refs):
        if palavra not in PERMITIDOS_CAMEL:
            falha(nome, "identificador de codigo no texto: %s" % palavra)
    baixo = sem_refs.lower()
    for frase in FRASES_FUTURAS:
        if frase in baixo:
            falha(nome, "sugestao futura proibida: %r" % frase)


def main():
    if not os.path.isdir(DIR_ADRS):
        print("FALHA: pasta docs/adrs/ nao existe")
        print("RESULTADO: FAIL")
        sys.exit(1)
    arquivos = sorted(os.listdir(DIR_ADRS))
    adrs = [a for a in arquivos if NOME_ARQUIVO.match(a)]
    for a in arquivos:
        if not NOME_ARQUIVO.match(a):
            falha(a, "arquivo fora do padrao ADR-NNN-titulo-em-kebab-case.md dentro de docs/adrs/")
    if not 5 <= len(adrs) <= 8:
        falha("docs/adrs", "ha %d ADRs; o README exige de 5 a 8" % len(adrs))
    numeros = [int(NOME_ARQUIVO.match(a).group(1)) for a in adrs]
    if numeros != list(range(1, len(numeros) + 1)):
        falha("docs/adrs", "numeracao deve ser sequencial a partir de 001: %s" % numeros)

    tokens = tokens_do_template()
    for a in adrs:
        validar_adr(os.path.join(DIR_ADRS, a), tokens)

    cobertas = []
    for decisao, palavras in DECISOES.items():
        if any(any(p in a for p in palavras) for a in adrs):
            cobertas.append(decisao)
        else:
            print("AVISO: nenhum ADR cobre '%s'" % decisao)
    if len(cobertas) < 5:
        falha("docs/adrs", "cobre %d das 6 decisoes obrigatorias; o README exige 5 ou mais" % len(cobertas))

    print("ADRs encontrados: %d | decisoes obrigatorias cobertas: %d/6" % (len(adrs), len(cobertas)))
    for p in problemas:
        print("FALHA: " + p)
    print("RESULTADO: " + ("PASS" if not problemas else "FAIL"))
    sys.exit(0 if not problemas else 1)


if __name__ == "__main__":
    main()
