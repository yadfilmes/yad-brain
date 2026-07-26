#!/usr/bin/env python3
"""
Casos-ouro do conjunto mínimo de arestas (_meta/arestas-minimas.md).

    python3 tools/test_validate.py

Por que testar isto e não o resto do validate.py: a regra do item 3 da R-N é
a única que **inventa exigência** em vez de conferir formato. Regra que
inventa exigência erra em duas direções — deixa passar o que devia pegar, e
reprova o que devia aceitar. As duas direções estão cobertas abaixo.

Precedente: o `eval.py` rodou com uma regex que omitia um campo e devolveu
100% falso por semanas. Toda regra nova nasce com teste desde então.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import validate as V

VOCAB = V.carregar_vocabulario()
REGRAS = V.carregar_arestas_minimas()

falhas = []


def checa(nome, condicao, detalhe=""):
    if condicao:
        print(f"  ok    {nome}")
    else:
        print(f"  FALHA {nome}  {detalhe}")
        falhas.append(nome)


def rodar(tipo, status, presentes, dispensas=None):
    return V.checar_arestas_minimas(
        tipo, status, set(presentes), dispensas or {}, REGRAS, VOCAB
    )


def msgs(saida):
    return " | ".join(m for _, m in saida)


def niveis(saida):
    return {n for n, _ in saida}


# ---------------------------------------------------------------- o arquivo
print("\n_meta/arestas-minimas.md é legível e fechado")

checa("o arquivo declara regra para pelo menos 10 types", len(REGRAS) >= 10,
      f"achou {len(REGRAS)}")
checa("`camera` está entre eles", "camera" in REGRAS)
checa("prosa não vira type: nenhuma chave com espaço ou maiúscula",
      all(k.islower() and " " not in k for k in REGRAS))

fora = sorted(
    a
    for r in REGRAS.values()
    for a in r["obrigatorias"] + [x for g in r["grupos"] for x in g]
    if a not in VOCAB
)
checa("toda aresta exigida existe no vocabulário fechado", not fora,
      f"fora do vocabulário: {fora}")

checa("cabeçalho com dois types rege os dois",
      REGRAS.get("colorspace") == REGRAS.get("transfer-function")
      and "colorspace" in REGRAS)

checa("`conceito` segue deliberadamente aberto", "conceito" not in REGRAS)


# ------------------------------------------------------- o que deve reprovar
print("\npega o que tem de pegar")

CAMERA_OK = ["made_by", "has_native_mount", "records_codec", "accepts_media",
             "outputs_signal", "competes_with", "uses_battery_mount",
             "budget_alternative_to"]

s = rodar("camera", "draft", [a for a in CAMERA_OK if a != "records_codec"])
checa("câmera sem records_codec é apontada", "records_codec" in msgs(s))

s = rodar("camera", "draft", [a for a in CAMERA_OK if a != "uses_battery_mount"])
checa("câmera sem nenhuma do grupo de energia é apontada",
      "ao menos uma de uses_battery_mount, powered_by" in msgs(s))

s = rodar("conceito", "draft", ["see_also"])
checa("piso universal pega grafo 100% see_also", "sem semântica" in msgs(s))

s = rodar("conceito", "draft", [])
checa("piso universal pega nota sem aresta nenhuma",
      "sem nenhuma aresta" in msgs(s))

s = rodar("marca", "draft", ["see_also"])
checa("marca só com see_also acumula piso + regra de type", len(s) == 2,
      msgs(s))


# --------------------------------------------------- o que NÃO deve reprovar
print("\naceita o que tem de aceitar")

checa("câmera completa passa limpa", not rodar("camera", "draft", CAMERA_OK),
      msgs(rodar("camera", "draft", CAMERA_OK)))

s = rodar("camera", "draft", [a for a in CAMERA_OK if a != "powered_by"])
checa("grupo satisfeito por qualquer membro basta (uses_battery_mount)",
      not s, msgs(s))

s = rodar("camera", "draft",
          [a for a in CAMERA_OK if a != "uses_battery_mount"] + ["powered_by"])
checa("grupo satisfeito pelo outro membro também basta (powered_by)",
      not s, msgs(s))

s = rodar("conceito", "draft", ["see_also", "distinct_from"])
checa("uma aresta com semântica já satisfaz o piso", not s, msgs(s))

s = rodar("camera", "stub", [])
checa("stub é silencioso — a regra não persegue esqueleto", not s, msgs(s))

s = rodar("pipeline-cor", "draft", ["governed_by"])
checa("type deliberadamente aberto não ganha exigência inventada",
      not s, msgs(s))

# A regra apontou 22 notas e 5 estavam certas. Falso positivo em regra de CI é
# mais caro que falso negativo: some no ruído e ensina a ignorar o aviso.
s = rodar("moc", "draft", ["see_also"])
checa("MOC só com see_also é a forma CORRETA de um mapa", not s, msgs(s))

s = rodar("orgao", "draft", ["see_also"])
checa("órgão recebe arestas de fora — see_also sozinho não é defeito",
      not s, msgs(s))

s = rodar("certificacao", "draft", [])
checa("certificação sem aresta nenhuma é forma correta (aponta-se para ela)",
      not s, msgs(s))

s = rodar("conceito", "draft", ["see_also"])
checa("a isenção não vazou para os demais types",
      any("sem semântica" in m for _, m in s), msgs(s))

# Segundo falso positivo achado pela regra: `made_by` só aponta para marca ou
# ecossistema. Exigi-la de um padrão ITU produziria erro de coerência de tipo
# no próprio CI — a régua não pode pedir o que o resto do validador reprova.
s = rodar("colorspace", "draft", ["governed_by", "distinct_from"])
checa("colorspace de norma passa por governed_by, sem made_by", not s, msgs(s))

s = rodar("transfer-function", "draft", ["made_by", "paired_gamut"])
checa("curva proprietária passa por made_by", not s, msgs(s))

s = rodar("colorspace", "draft", ["see_also"])
checa("colorspace sem nenhum dos dois caminhos ainda reprova", len(s) >= 2,
      msgs(s))


# -------------------------------------------------------- a régua por status
print("\navisa em draft, reprova em reviewed (regra do lote 03)")

incompleta = [a for a in CAMERA_OK if a != "records_codec"]
checa("em draft o veredito é aviso",
      niveis(rodar("camera", "draft", incompleta)) == {"aviso"})
checa("em reviewed o mesmo defeito é erro",
      niveis(rodar("camera", "reviewed", incompleta)) == {"erro"})


# ------------------------------------------------------------------- rel_na
print("\nrel_na dispensa com motivo — e só com motivo")

s = rodar("camera", "draft", [a for a in CAMERA_OK if a != "outputs_signal"],
          {"outputs_signal": "corpo sem saída de vídeo (manual, p. 12)"})
checa("dispensa com motivo satisfaz a exigência", not s, msgs(s))

s = rodar("camera", "draft", [a for a in CAMERA_OK if a != "outputs_signal"],
          {"outputs_signal": ""})
checa("dispensa sem motivo é ERRO, não aviso",
      any(n == "erro" and "sem motivo" in m for n, m in s), msgs(s))

s = rodar("camera", "draft", [a for a in CAMERA_OK if a != "outputs_signal"],
          {"outputs_signal": []})
checa("motivo que não é texto também é erro",
      any(n == "erro" and "sem motivo" in m for n, m in s), msgs(s))

s = rodar("camera", "draft", CAMERA_OK, {"outputs_signal": "motivo qualquer"})
checa("declarar e dispensar a mesma aresta é contradição",
      any("ao mesmo tempo" in m for _, m in s), msgs(s))

s = rodar("camera", "draft", CAMERA_OK, {"inventa_isso": "motivo qualquer"})
checa("dispensa de aresta fora do vocabulário é erro",
      any("fora do vocabulário" in m for _, m in s), msgs(s))

s = rodar("camera", "stub", [], {"outputs_signal": ""})
checa("stub não silencia rel_na malformado — erro de forma é sempre erro",
      any(n == "erro" for n, _ in s), msgs(s))


# ------------------------------------------------- rubrica de confiança
print("\nrubrica de confiança: o piso mecânico (item 11 da R-N)")

checa("duas páginas do mesmo fabricante são UMA organização",
      V.organizacao("https://pro.sony/x") == V.organizacao("https://www.sony.com/y"),
      f'{V.organizacao("https://pro.sony/x")} vs {V.organizacao("https://www.sony.com/y")}')

checa("fabricantes diferentes são organizações diferentes",
      V.organizacao("https://www.arri.com/a") != V.organizacao("https://www.cined.com/b"))

checa("subdomínio de suporte não vira organização nova",
      V.organizacao("https://partnerhelp.netflixstudios.com/hc") == "netflixstudios",
      V.organizacao("https://partnerhelp.netflixstudios.com/hc"))


def fonte(dominio, tier, loc=True):
    d = {"url": f"https://www.{dominio}.com/pagina", "tier": tier}
    if loc:
        d["loc"] = "secao X"
    return d


OFICIAL_LOC = fonte("sony", "oficial")
LAB_LOC = fonte("cined", "lab")

checa("duas orgs, oficial + lab, todas com loc -> alta",
      V.confianca_esperada([OFICIAL_LOC, LAB_LOC], False) == "alta",
      V.confianca_esperada([OFICIAL_LOC, LAB_LOC], False))

checa("lacuna <!-- verificar --> derruba para baixa, independente das fontes",
      V.confianca_esperada([OFICIAL_LOC, LAB_LOC], True) == "baixa")

checa("mesma organização em duas URLs não corrobora",
      V.confianca_esperada([fonte("sony", "oficial"),
                            {"url": "https://pro.sony/z", "tier": "oficial",
                             "loc": "y"}], False) == "media",
      V.confianca_esperada([fonte("sony", "oficial"),
                            {"url": "https://pro.sony/z", "tier": "oficial",
                             "loc": "y"}], False))

checa("fonte oficial única com loc -> media, não alta",
      V.confianca_esperada([OFICIAL_LOC], False) == "media")

checa("fonte única sem tier forte -> baixa",
      V.confianca_esperada([fonte("algumblog", "educacao")], False) == "baixa")

checa("duas orgs sem nenhuma oficial/lab -> media, nunca alta",
      V.confianca_esperada([fonte("blog1", "educacao"),
                            fonte("forum2", "comunidade")], False) == "media")

checa("falta de loc em fonte oficial impede alta",
      V.confianca_esperada([fonte("sony", "oficial", loc=False), LAB_LOC],
                           False) == "media")

checa("nota sem fonte nenhuma -> baixa",
      V.confianca_esperada([], False) == "baixa")


# -------------------------------------------------------------------- saída
print()
if falhas:
    print(f"FALHOU — {len(falhas)} caso(s): {', '.join(falhas)}\n")
    sys.exit(1)
print("OK — todos os casos passaram\n")
