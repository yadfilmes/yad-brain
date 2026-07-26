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


# -------------------------------------------------------------------- saída
print()
if falhas:
    print(f"FALHOU — {len(falhas)} caso(s): {', '.join(falhas)}\n")
    sys.exit(1)
print("OK — todos os casos passaram\n")
