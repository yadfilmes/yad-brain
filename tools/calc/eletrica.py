#!/usr/bin/env python3
"""
Calculadora elétrica de set — corrente, circuitos, cabo, gerador e fases.

    python3 tools/calc/eletrica.py --potencia 14400
    python3 tools/calc/eletrica.py --potencia 14400 --trifasico
    python3 tools/calc/eletrica.py --potencia 5000 --distancia 60
    python3 tools/calc/eletrica.py --gerador 20000
    python3 tools/calc/eletrica.py --fases 2400,1200,1200,600,600,600

⚠️  AVISO OBRIGATÓRIO
Esta ferramenta é de PLANEJAMENTO e ORÇAMENTO. Não é projeto elétrico e não
substitui profissional habilitado. Instalação, dimensionamento definitivo e
laudo são responsabilidade de engenheiro ou técnico com registro (CREA/CFT),
sob NR-10 e ABNT NBR 5410. Set de filmagem com carga alta em locação exige
verificação da instalação existente ANTES do dia de gravação.

Por que existe: a conta encadeada (potência -> corrente -> circuitos -> cabo)
é onde se descobre tarde que a locação não aguenta a luz contratada. Melhor
descobrir no orçamento.
"""

import argparse
import math
import sys

# Resistividade do cobre em temperatura de trabalho (Ω·mm²/m). Valor prático
# de projeto — acima da resistividade a 20 °C, que subestima a queda real.
RHO_COBRE = 0.0225

# Bitolas comerciais (mm²) e disjuntores comuns no Brasil (A).
BITOLAS = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120]
DISJUNTORES = [10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125]

# Capacidade de condução aproximada em cabo de cobre PVC, dois condutores
# carregados, ao ar livre. Conservador de propósito — a tabela real da NBR
# 5410 depende de método de instalação, agrupamento e temperatura ambiente.
CAPACIDADE_A = {1.5: 17.5, 2.5: 24, 4: 32, 6: 41, 10: 57, 16: 76,
                25: 101, 35: 125, 50: 151, 70: 192, 95: 232, 120: 269}

QUEDA_MAX_PCT = 4.0      # limite prático de projeto para circuito terminal
FOLGA_DISJUNTOR = 0.8    # nunca carregar disjuntor acima de 80%


def corrente(potencia_w, tensao=220, fp=0.92, trifasico=False):
    """Corrente em ampères. FP 0,92 é típico de LED com fonte chaveada."""
    if potencia_w < 0:
        raise ValueError("potência não pode ser negativa")
    if tensao <= 0:
        raise ValueError("tensão precisa ser positiva")
    if not 0 < fp <= 1:
        raise ValueError("fator de potência deve estar entre 0 e 1")
    if trifasico:
        return potencia_w / (tensao * math.sqrt(3) * fp)
    return potencia_w / (tensao * fp)


def circuitos(corrente_a, disjuntor_a=32):
    """Quantos circuitos, respeitando 80% de carga por disjuntor."""
    if disjuntor_a <= 0:
        raise ValueError("disjuntor precisa ser positivo")
    if corrente_a <= 0:
        return 0
    return math.ceil(corrente_a / (disjuntor_a * FOLGA_DISJUNTOR))


def queda_tensao(corrente_a, distancia_m, bitola_mm2, tensao=220, trifasico=False):
    """Queda de tensão percentual na ida e volta do cabo."""
    if min(distancia_m, bitola_mm2) <= 0:
        raise ValueError("distância e bitola precisam ser positivas")
    fator = math.sqrt(3) if trifasico else 2
    delta_v = (fator * RHO_COBRE * distancia_m * corrente_a) / bitola_mm2
    return 100 * delta_v / tensao


def bitola_minima(corrente_a, distancia_m, tensao=220, trifasico=False,
                  queda_max=QUEDA_MAX_PCT):
    """Menor bitola comercial que atende condução E queda de tensão.

    As duas restrições importam: cabo pode conduzir a corrente sem esquentar e
    ainda assim entregar tensão baixa demais no fim de uma tirada longa —
    situação clássica de gerador distante do set.
    """
    for b in BITOLAS:
        if CAPACIDADE_A.get(b, 0) < corrente_a:
            continue
        if queda_tensao(corrente_a, distancia_m, b, tensao, trifasico) <= queda_max:
            return b
    return None


def disjuntor_recomendado(corrente_a):
    for d in DISJUNTORES:
        if d * FOLGA_DISJUNTOR >= corrente_a:
            return d
    return None


def gerador(potencia_w, fp=0.92, margem=0.25, partida=False):
    """Dimensiona gerador em kVA.

    kVA = kW / FP, mais margem. `partida` acrescenta reserva para carga
    indutiva (HMI com reator, motor), que puxa muito mais no arranque.
    """
    if potencia_w < 0:
        raise ValueError("potência não pode ser negativa")
    kva_util = (potencia_w / 1000) / fp
    fator = 1 + margem + (0.5 if partida else 0)
    return {"kva_util": kva_util, "kva_recomendado": kva_util * fator,
            "margem_pct": fator * 100 - 100}


def balancear(cargas_w, tensao=220, fp=0.92):
    """Distribui cargas entre três fases minimizando o desequilíbrio.

    Guloso decrescente: coloca a maior carga sempre na fase mais leve. Não é
    ótimo global, mas é o que um chefe de elétrica faz na prática — e chega
    perto o bastante.
    """
    fases = [[], [], []]
    for c in sorted(cargas_w, reverse=True):
        i = min(range(3), key=lambda k: sum(fases[k]))
        fases[i].append(c)
    totais = [sum(f) for f in fases]
    correntes = [corrente(t, tensao, fp) for t in totais]
    media = sum(totais) / 3 if any(totais) else 0
    desequilibrio = (100 * (max(totais) - min(totais)) / media) if media else 0
    # Uma carga única maior que 1/3 do total torna o equilíbrio perfeito
    # impossível: carga não se divide entre fases. Sinalizar isso evita que
    # alguém perca tempo tentando redistribuir o irredistribuível.
    inevitavel = bool(cargas_w) and max(cargas_w) > media if media else False
    return {"fases": fases, "totais_w": totais, "correntes_a": correntes,
            "desequilibrio_pct": desequilibrio, "inevitavel": inevitavel,
            "maior_carga_w": max(cargas_w) if cargas_w else 0}


def aviso():
    print("\n  ⚠️  Números de PLANEJAMENTO — não é projeto elétrico.")
    print("     Dimensionamento definitivo, instalação e laudo exigem")
    print("     profissional habilitado (CREA/CFT), sob NR-10 e NBR 5410.")
    print("     Em locação, verificar a instalação existente antes do dia.\n")


def main(argv=None):
    p = argparse.ArgumentParser(description="Cálculos elétricos de set (planejamento)")
    p.add_argument("--potencia", type=float, help="carga total em watts")
    p.add_argument("--tensao", type=int, default=220, choices=[127, 220, 380])
    p.add_argument("--fp", type=float, default=0.92, help="fator de potência")
    p.add_argument("--trifasico", action="store_true")
    p.add_argument("--disjuntor", type=int, default=32, help="ampères por circuito")
    p.add_argument("--distancia", type=float, help="metros até o quadro/gerador")
    p.add_argument("--gerador", type=float, metavar="W", help="dimensionar gerador para N watts")
    p.add_argument("--partida", action="store_true", help="há carga indutiva (HMI, motor)")
    p.add_argument("--fases", help="lista de cargas em W separadas por vírgula")
    a = p.parse_args(argv)

    if a.gerador is not None:
        g = gerador(a.gerador, a.fp, partida=a.partida)
        print(f"\nGerador para {a.gerador/1000:.1f} kW  (FP {a.fp})\n")
        print(f"  potência aparente     {g['kva_util']:.1f} kVA")
        print(f"  recomendado           {g['kva_recomendado']:.1f} kVA"
              f"   (+{g['margem_pct']:.0f}% de margem)")
        if a.partida:
            print("  margem inclui reserva de partida para carga indutiva")
        aviso()
        return 0

    if a.fases:
        try:
            cargas = [float(x) for x in a.fases.split(",") if x.strip()]
        except ValueError:
            print("lista de cargas inválida", file=sys.stderr)
            return 2
        b = balancear(cargas, a.tensao, a.fp)
        print(f"\nBalanceamento de {len(cargas)} cargas em 3 fases · {a.tensao} V\n")
        for i, (f, t, c) in enumerate(zip(b["fases"], b["totais_w"], b["correntes_a"])):
            itens = " + ".join(f"{int(x)}" for x in f) or "—"
            print(f"  fase {'RST'[i]}   {t/1000:6.2f} kW  {c:5.1f} A   [{itens}]")
        print(f"\n  desequilíbrio         {b['desequilibrio_pct']:.1f}%")
        if b["inevitavel"]:
            print(f"  a maior carga ({b['maior_carga_w']:.0f} W) sozinha excede o ideal")
            print("  por fase — este desequilíbrio é forçado, não há como redistribuir")
        elif b["desequilibrio_pct"] > 15:
            print("  ⚠️  acima de 15% — redistribuir se possível")
        aviso()
        return 0

    if a.potencia is None:
        p.error("informe --potencia, --gerador ou --fases")

    i = corrente(a.potencia, a.tensao, a.fp, a.trifasico)
    n = circuitos(i, a.disjuntor)
    dj = disjuntor_recomendado(i)

    print(f"\nCarga de {a.potencia/1000:.1f} kW · {a.tensao} V · "
          f"{'trifásico' if a.trifasico else 'monofásico'} · FP {a.fp}\n")
    print(f"  corrente              {i:.1f} A")
    print(f"  disjuntor único       {dj} A" if dj else "  disjuntor único      acima da tabela")
    print(f"  ou circuitos de {a.disjuntor} A   {n}   (80% de carga por disjuntor)")

    if a.distancia:
        b = bitola_minima(i, a.distancia, a.tensao, a.trifasico)
        print(f"\n  TIRADA DE {a.distancia:.0f} m")
        if b:
            q = queda_tensao(i, a.distancia, b, a.tensao, a.trifasico)
            print(f"  bitola mínima         {b} mm²   (queda {q:.1f}%, limite {QUEDA_MAX_PCT}%)")
            print(f"  atende condução e queda de tensão")
        else:
            print("  nenhuma bitola da tabela atende — dividir a carga em mais")
            print("  circuitos ou aproximar a fonte de energia")

    aviso()
    return 0


if __name__ == "__main__":
    sys.exit(main())
