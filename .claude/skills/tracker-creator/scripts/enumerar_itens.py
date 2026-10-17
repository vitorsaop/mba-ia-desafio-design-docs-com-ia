#!/usr/bin/env python3
"""Enumera os itens identificaveis dos documentos do pacote, com IDs deterministicos.

Uso:
  python3 .claude/skills/tracker-creator/scripts/enumerar_itens.py            # lista ID, documento e texto
  python3 .claude/skills/tracker-creator/scripts/enumerar_itens.py --tabela   # linhas de tabela para preencher
  python3 .claude/skills/tracker-creator/scripts/enumerar_itens.py --json
"""
import glob
import json
import os
import re
import sys

RAIZ = os.getcwd()
for i, a in enumerate(sys.argv):
    if a == "--raiz" and i + 1 < len(sys.argv):
        RAIZ = os.path.abspath(sys.argv[i + 1])


def ler(rel):
    caminho = os.path.join(RAIZ, rel)
    return open(caminho, encoding="utf-8").read() if os.path.isfile(caminho) else ""


def h3(texto):
    partes = re.split(r"^### (.+)$", texto, flags=re.M)
    return [(partes[i].strip(), partes[i + 1]) for i in range(1, len(partes), 2)]


def topo(bloco):
    return [l[2:].strip() for l in bloco.split("\n") if l.startswith("- ")]


def aninhados(bloco):
    return [l.strip()[2:].strip() for l in bloco.split("\n") if re.match(r"^\s{2,}- ", l)]


def linhas_tabela(bloco):
    ls = [l for l in bloco.split("\n") if l.startswith("|")]
    return [[c.strip() for c in l.strip().strip("|").split("|")] for l in ls[2:]]


def rotulo_bullets(bloco, rotulo):
    m = re.search(r"^%s\s*\n((?:- .+\n?)+)" % re.escape(rotulo), bloco, re.M)
    return topo(m.group(1)) if m else []


def apos_rotulo_negrito(bloco, rotulo):
    m = re.search(r"^%s.*?\n(.*?)(?=^\*\*|\Z)" % re.escape(rotulo), bloco, re.S | re.M)
    return m.group(1) if m else ""


def blocos_h4(bloco):
    return re.split(r"^(?=#### )", bloco, flags=re.M)[1:]


def itens_prd():
    t = ler("docs/PRD.md")
    out = []
    if not t:
        return out
    corpo = dict(h3(t))
    doc = "docs/PRD.md"
    for n, r in enumerate(linhas_tabela(corpo.get("Objetivos e métricas", "")), 1):
        out.append(("PRD-OBJ-%02d" % n, doc, "Objetivo", "%s: meta %s" % (r[0], r[2] if len(r) > 2 else "")))
    esc = corpo.get("Escopo", "")
    for n, b in enumerate(rotulo_bullets(esc, "Incluso"), 1):
        out.append(("PRD-ESC-INC-%02d" % n, doc, "Escopo", b))
    for n, b in enumerate(rotulo_bullets(esc, "Fora de escopo"), 1):
        out.append(("PRD-ESC-FORA-%02d" % n, doc, "Escopo", b))
    for b in blocos_h4(corpo.get("Requisitos funcionais", "")):
        m = re.match(r"^#### (FR-\d{2}) (.+)$", b.split("\n")[0])
        if m:
            desc = next((l for l in b.split("\n")[1:] if l.strip() and not l.startswith("**")), "")
            out.append(("PRD-%s" % m.group(1), doc, "Requisito Funcional", "%s. %s" % (m.group(2), desc)))
    n = 0
    for rotulo in (
        "Performance",
        "Disponibilidade",
        "Segurança e autorização",
        "Observabilidade",
        "Confiabilidade e integridade de dados",
        "Compatibilidade e portabilidade",
        "Compliance",
        "Acessibilidade no frontend consumidor",
    ):
        for b in rotulo_bullets(corpo.get("Requisitos não funcionais", ""), rotulo):
            n += 1
            out.append(("PRD-RNF-%02d" % n, doc, "Requisito Não Funcional", "%s: %s" % (rotulo, b)))
    for n, b in enumerate(blocos_h4(corpo.get("Decisões e trade-offs", "")), 1):
        out.append(("PRD-DEC-%02d" % n, doc, "Decisão", b.split("\n")[0][5:]))
    for n, b in enumerate(blocos_h4(corpo.get("Dependências", "")), 1):
        out.append(("PRD-DEP-%02d" % n, doc, "Dependência", b.split("\n")[0][5:]))
    for n, b in enumerate(blocos_h4(corpo.get("Riscos e mitigação", "")), 1):
        out.append(("PRD-RISCO-%02d" % n, doc, "Risco", b.split("\n")[0][5:]))
    for n, b in enumerate(topo(corpo.get("Critérios de aceitação", "")), 1):
        out.append(("PRD-CA-%02d" % n, doc, "Critério de Aceite", b))
    testes = corpo.get("Testes e validação", "")
    n = 0
    for rotulo in ("Tipos de teste obrigatórios", "Estratégia de validação"):
        for b in rotulo_bullets(testes, rotulo):
            n += 1
            out.append(("PRD-TESTE-%02d" % n, doc, "Teste", b))
    return out


def itens_rfc():
    t = ler("docs/RFC.md")
    out = []
    if not t:
        return out
    corpo = dict(h3(t))
    doc = "docs/RFC.md"
    for n, b in enumerate(topo(corpo.get("Proposta técnica", "")), 1):
        out.append(("RFC-PROP-%02d" % n, doc, "Proposta", b))
    for n, b in enumerate(topo(corpo.get("Alternativas consideradas", "")), 1):
        out.append(("RFC-ALT-%02d" % n, doc, "Alternativa", b))
    for n, b in enumerate(topo(corpo.get("Questões em aberto", "")), 1):
        out.append(("RFC-QA-%02d" % n, doc, "Questão em Aberto", b))
    ir = corpo.get("Impacto e riscos", "")
    antes, _, depois = ir.partition("**Riscos**")
    for n, b in enumerate(topo(antes), 1):
        out.append(("RFC-IMP-%02d" % n, doc, "Impacto", b))
    for n, b in enumerate(topo(depois), 1):
        out.append(("RFC-RISCO-%02d" % n, doc, "Risco", b))
    for n, b in enumerate(topo(corpo.get("Decisões relacionadas", "")), 1):
        out.append(("RFC-ADR-%02d" % n, doc, "Decisão", b))
    return out


def itens_fdd():
    t = ler("docs/FDD.md")
    out = []
    if not t:
        return out
    partes = re.split(r"^### (\d+)\. (.+)$", t, flags=re.M)
    sec = {int(partes[i]): partes[i + 2] for i in range(1, len(partes), 3)}
    doc = "docs/FDD.md"
    for n, b in enumerate(topo(sec.get(2, "")), 1):
        out.append(("FDD-OBJ-%02d" % n, doc, "Objetivo", b))
    for n, b in enumerate(topo(apos_rotulo_negrito(sec.get(3, ""), "**Incluído**")), 1):
        out.append(("FDD-ESC-INC-%02d" % n, doc, "Escopo", b))
    for n, b in enumerate(topo(apos_rotulo_negrito(sec.get(3, ""), "**Excluído**")), 1):
        out.append(("FDD-ESC-EXC-%02d" % n, doc, "Escopo", b))
    n = 0
    for rotulo in ("**Fluxo principal**", "**Fluxos alternativos e exceções**"):
        for b in topo(apos_rotulo_negrito(sec.get(4, ""), rotulo)):
            n += 1
            out.append(("FDD-FLUXO-%02d" % n, doc, "Fluxo", b))
    for b in re.findall(r"^\*\*Contrato (\d+): (.+)\*\*$", sec.get(5, ""), re.M):
        out.append(("FDD-CONTRATO-%02d" % int(b[0]), doc, "Contrato", b[1]))
    s6 = sec.get(6, "")
    for n, r in enumerate([r for r in linhas_tabela(s6) if r and r[0].strip("`").startswith("WEBHOOK_")], 1):
        out.append(("FDD-ERRO-%02d" % n, doc, "Erro", "%s: %s" % (r[0].strip("`"), r[1] if len(r) > 1 else "")))
    n = 0
    for rotulo in ("- Estratégias de resiliência", "- Política de fallback"):
        trecho = s6.split(rotulo, 1)[-1].split("\n- ", 1)[0] if rotulo in s6 else ""
        for b in aninhados(trecho):
            n += 1
            out.append(("FDD-RES-%02d" % n, doc, "Resiliência", b))
    trecho = s6.split("- Invariantes", 1)[-1].split("\n- ", 1)[0] if "- Invariantes" in s6 else ""
    for n, b in enumerate(aninhados(trecho), 1):
        out.append(("FDD-INV-%02d" % n, doc, "Invariante", b))
    n = 0
    for rotulo in ("Métricas", "Logs", "Tracing", "Dashboards e alertas"):
        for b in rotulo_bullets(sec.get(7, ""), rotulo):
            n += 1
            out.append(("FDD-OBS-%02d" % n, doc, "Observabilidade", "%s: %s" % (rotulo, b)))
    s8 = sec.get(8, "")
    n = 0
    for r in linhas_tabela(s8):
        n += 1
        out.append(("FDD-DEP-%02d" % n, doc, "Dependência", "%s %s: %s" % (r[1], r[0], r[2] if len(r) > 2 else "")))
    for b in rotulo_bullets(s8, "Garantias de compatibilidade"):
        n += 1
        out.append(("FDD-DEP-%02d" % n, doc, "Dependência", b))
    for n, b in enumerate(topo(sec.get(9, "")), 1):
        out.append(("FDD-CA-%02d" % n, doc, "Critério de Aceite", b))
    for n, b in enumerate(re.split(r"^### (?=\S)", sec.get(10, ""), flags=re.M)[1:], 1):
        out.append(("FDD-RISCO-%02d" % n, doc, "Risco", b.split("\n")[0]))
    for n, r in enumerate(linhas_tabela(sec.get(11, "")), 1):
        out.append(("FDD-INT-%02d" % n, doc, "Integração", "%s: %s" % (r[0], r[2] if len(r) > 2 else "")))
    modelo = re.search(r"^\*\*Modelo de dados novo[^\n]*\*\*\s*\n((?:- .+\n?)+)", sec.get(11, ""), re.M)
    for n, b in enumerate(topo(modelo.group(1)) if modelo else [], 1):
        out.append(("FDD-MOD-%02d" % n, doc, "Integração", b))
    n = 0
    for b in aninhados(sec.get(5, "")):
        if "Hipótese" in b:
            n += 1
            out.append(("FDD-HIP-%02d" % n, doc, "Hipótese", b))
    return out


def itens_adr():
    out = []
    for caminho in sorted(glob.glob(os.path.join(RAIZ, "docs", "adrs", "ADR-*.md"))):
        nome = os.path.basename(caminho)
        m = re.match(r"^(ADR-\d{3})-", nome)
        if not m:
            continue
        t = open(caminho, encoding="utf-8").read()
        doc = "docs/adrs/" + nome
        titulo = t.split("\n")[0]
        out.append((m.group(1), doc, "Decisão", re.sub(r"^# ADR-\d{3}: ", "", titulo)))
        alt = re.search(r"^## Alternativas Consideradas\s*\n(.*?)(?=^## )", t, re.S | re.M)
        if alt:
            for n, l in enumerate([l for l in alt.group(1).split("\n") if re.match(r"^\d+\. ", l)], 1):
                out.append(("%s-ALT-%02d" % (m.group(1), n), doc, "Alternativa", re.sub(r"^\d+\. ", "", l)))
    return out


def todos():
    itens = itens_prd() + itens_rfc() + itens_fdd() + itens_adr()
    vistos = set()
    for i in itens:
        if i[0] in vistos:
            raise SystemExit("ID duplicado na enumeracao: %s" % i[0])
        vistos.add(i[0])
    return itens


def resumo(texto, limite=140):
    """Uma linha: sem links, sem negrito, sem crases e sem o caractere de coluna da tabela."""
    texto = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", texto)
    texto = re.sub(r"\*\*|`", "", texto.replace("|", "/"))
    texto = re.sub(r"\s+", " ", texto).strip()
    if len(texto) <= limite:
        return texto
    corte = texto[:limite]
    fim_de_frase = corte.rfind(". ")
    if fim_de_frase >= 50:
        return corte[: fim_de_frase + 1]
    return corte.rsplit(" ", 1)[0] + "..."


if __name__ == "__main__":
    itens = todos()
    if "--json" in sys.argv:
        print(json.dumps([{"id": i, "documento": d, "tipo": t, "texto": x} for i, d, t, x in itens], ensure_ascii=False, indent=1))
    elif "--tabela" in sys.argv:
        for i, d, t, x in itens:
            print("| %s | %s | %s | %s |  |  |" % (i, d, t, resumo(x)))
    else:
        for i, d, t, x in itens:
            print("%s\t%s\t%s" % (i, d, resumo(x)))
        print("TOTAL: %d itens" % len(itens), file=sys.stderr)
