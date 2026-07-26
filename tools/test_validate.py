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

# UM CASO POR LINHA DA TABELA. O lote 04 achou a 4a linha divergindo do
# script; o lote de elétrica achou a 3a ainda divergindo, porque só a linha
# reportada tinha sido corrigida. Estes casos existem para que a régua e o
# script não voltem a separar em nenhuma linha.
checa("1a linha · lacuna vence tudo",
      V.confianca_esperada([OFICIAL_LOC, LAB_LOC], True) == "baixa")
checa("3a linha · afirmação numérica sem fonte forte -> baixa",
      V.confianca_esperada([fonte("blog", "educacao"), fonte("outro", "educacao")],
                           False, tem_numero=True) == "baixa")
checa("3a linha NÃO derruba quando há fonte forte",
      V.confianca_esperada([OFICIAL_LOC, LAB_LOC], False, tem_numero=True) == "alta")
checa("4a linha · fonte única fraca -> baixa",
      V.confianca_esperada([fonte("blog", "educacao")], False) == "baixa")
checa("4a linha · fonte única forte -> media",
      V.confianca_esperada([OFICIAL_LOC], False) == "media")
checa("5a linha · duas orgs, nenhuma forte, sem número -> media",
      V.confianca_esperada([fonte("blog", "educacao"), fonte("outro", "educacao")],
                           False) == "media")
checa("6a linha · falta loc em fonte forte -> media",
      V.confianca_esperada([fonte("sony", "oficial", loc=False), LAB_LOC],
                           False) == "media")
checa("8a linha · duas orgs, forte, com loc -> alta",
      V.confianca_esperada([OFICIAL_LOC, LAB_LOC], False) == "alta")

print("\ndetecção de afirmação numérica")
NUM = [("a tabela diz 220 V", True), ("corrente de ~11,9 A", True),
       ("bitola de 10 mm²", True), ("grava 12 bits log", True),
       ("240 Mbps sustentados", True),
       ("prosa sem número nenhum", False),
       ("atualizado em 2026-07-26", False),
       ("são três opções de menu", False)]
for txt, esperado in NUM:
    checa(f"numérica? {txt[:30]!r}",
          V.tem_afirmacao_numerica(txt) == esperado)
checa("número dentro de bloco de código é comando, não afirmação",
      not V.tem_afirmacao_numerica("veja:\n```\npython3 x.py --potencia 5000\n```"))

print("\nconteúdo de prática: reconhece a forma, não o título da seção")

# Padrão nº 15 do lote 04: o gatilho era por literal ("## Gotchas") e escapava
# renomeando a seção. E a primeira versão do gatilho novo disparava em nota que
# só MENCIONA set — as duas direções estão travadas aqui.
PRATICA = [
    ("## Gotchas\n- cabo enrolado conduz menos", True),
    ("Regra prática de campo: acender em escada", True),
    ("O erro clássico é ninguém conferir onde ligou", True),
    ("Nunca improvisar a ligação do quadro", True),
    ("Na prática, o mount decide mais que o corpo", True),
    ("Padrão de vídeo profissional sobre cabo coaxial.", False),
    ("A norma estabelece condições mínimas de segurança.", False),
    ("O sensor tem 6K e grava em 12 bits.", False),
    ("É muito usado em set de publicidade brasileira.", False),
]
for txt, esperado in PRATICA:
    checa(f"prática? {txt[:34]!r}",
          bool(V.PRATICA_NO_CORPO.search(txt)) == esperado)

checa("renomear a seção não escapa do gatilho",
      bool(V.PRATICA_NO_CORPO.search(
          "## Quando não é isso\nNunca deixar o cabo enrolado no carretel")))


print("\nwikilink de corpo")
checa("regex de wikilink acha o alvo",
      V.WIKILINK.findall("ver [[hmi]] e [[gerador]]") == ["hmi", "gerador"])
checa("wikilink com pipe e âncora é normalizado no chamador",
      V.WIKILINK.findall("[[nota|apelido]]") == ["nota|apelido"])

# Contradição achada por revisor independente no lote 04: a 4ª linha da tabela
# dizia "fonte única, qualquer tier -> baixa" e a 7ª dizia "oficial com loc,
# sem corroboração -> media". O script implementava a 7ª. Resolvido a favor
# dela; este teste trava as duas pontas para não divergirem de novo.
checa("fonte única OFICIAL com loc -> media (7ª linha da tabela)",
      V.confianca_esperada([OFICIAL_LOC], False) == "media")

checa("fonte única FRACA -> baixa (4ª linha da tabela)",
      V.confianca_esperada([fonte("blogqualquer", "educacao")], False) == "baixa")

checa("duas páginas do mesmo fabricante nunca chegam a alta",
      V.confianca_esperada([fonte("brompton", "oficial"),
                            {"url": "https://www.brompton.com/outra",
                             "tier": "oficial", "loc": "z"}], False) != "alta")


# ------------------------------------------- lacuna em prosa e origem da aresta
print("\nregra da transcrição: lacuna em prosa e domínio de aresta")

# Esta regex já custou 2 falsos positivos em 3 acertos na primeira versão.
# Os casos abaixo travam as duas direções — o que ela precisa pegar, e as
# frases de prática de set que ela NÃO pode confundir com lacuna.
PEGA = [
    "a ordem vem de padrão de campo relatado, não de teste controlado.",
    "os valores precisam sair da documentação do fabricante.",
    "conferir isso antes de virar `reviewed`.",
    "o número não foi conferido contra o manual.",
    "falta confirmar o comportamento em firmware novo.",
]
NAO_PEGA = [
    "é o ponto a conferir antes de fechar o kit.",
    "serve para conferir se a ordem das cenas respeita a luz.",
    "conferir a especificação do cabo, não só o conector.",
    "vale conferir na câmera, não a olho.",
    "pergunta útil ao alugar: qual o R9 e qual o TLCI.",
]
for frase in PEGA:
    checa(f"pega lacuna: {frase[:38]}…", bool(V.LACUNA_EM_PROSA.search(frase)))
for frase in NAO_PEGA:
    m = V.LACUNA_EM_PROSA.search(frase)
    checa(f"não confunde prática: {frase[:34]}…", not m, m.group(0) if m else "")

checa("`governed_by` aceita conceito técnico com norma (genlock -> SMPTE)",
      "conceito" in V.TIPO_DE_ORIGEM["governed_by"])
checa("`governed_by` recusa produto — produto implementa norma",
      not ({"camera", "switcher", "fixture"} & V.TIPO_DE_ORIGEM["governed_by"]))
checa("toda aresta com domínio declarado existe no vocabulário",
      all(a in VOCAB for a in V.TIPO_DE_ORIGEM),
      str([a for a in V.TIPO_DE_ORIGEM if a not in VOCAB]))


# -------------------------------------------------------------------- saída
print()
if falhas:
    print(f"FALHOU — {len(falhas)} caso(s): {', '.join(falhas)}\n")
    sys.exit(1)
print("OK — todos os casos passaram\n")
