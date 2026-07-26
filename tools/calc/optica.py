#!/usr/bin/env python3
"""
Calculadora de óptica — campo de visão, profundidade de campo e equivalência.

    python3 tools/calc/optica.py --formato ff --focal 50 --tstop 2.8 --distancia 3
    python3 tools/calc/optica.py --equivalencia --de ff --para s35 --focal 50
    python3 tools/calc/optica.py --listar

Responde as perguntas de prep e de set:
  - que enquadramento essa lente dá neste sensor
  - de onde até onde vai ficar em foco
  - qual a hiperfocal (a partir de onde o infinito entra no foco)
  - que focal neste formato dá o mesmo enquadramento de outra em outro

AVISO: profundidade de campo depende do círculo de confusão, que é um critério
de nitidez ACEITÁVEL, não uma fronteira física. Os valores aqui são de
planejamento e prep — em set, a régua é o monitor com peaking, não a tabela.
"""

import argparse
import math
import sys

# Formatos de sensor: (largura_mm, altura_mm, descrição).
# Full frame e Super 16 são padrões estáveis. "Super 35" varia entre câmeras —
# o valor aqui é o de referência clássico; para trabalho fino, usar a medida
# do corpo específico com --largura/--altura.
FORMATOS = {
    "ff":    (36.0, 24.0, "full frame / VistaVision — 36 × 24 mm"),
    "s35":   (24.89, 18.66, "Super 35 clássico (varia por câmera)"),
    "s35og": (27.99, 19.22, "Super 35 open gate de geração recente"),
    "apsc":  (23.6, 15.7, "APS-C (Canon usa 22.3 × 14.9)"),
    "mft":   (17.3, 13.0, "Micro Quatro Terços"),
    "s16":   (12.52, 7.41, "Super 16"),
    "65":    (54.12, 25.58, "65 mm digital"),
}

# Divisor do círculo de confusão: CoC = diagonal / divisor.
# 1500 é o critério tradicional de foto; cinema em tela grande costuma exigir
# mais rigor. Parâmetro justamente porque a escolha é editorial, não física.
DIVISOR_COC = 1500


def coc(largura_mm, altura_mm, divisor=DIVISOR_COC):
    """Círculo de confusão para o formato, em mm."""
    if min(largura_mm, altura_mm) <= 0:
        raise ValueError("dimensões do sensor precisam ser positivas")
    return math.hypot(largura_mm, altura_mm) / divisor


def campo_de_visao(largura_mm, altura_mm, focal_mm):
    """Ângulos de cobertura em graus (horizontal, vertical, diagonal)."""
    if focal_mm <= 0:
        raise ValueError("focal precisa ser positiva")
    def ang(dim):
        return math.degrees(2 * math.atan(dim / (2 * focal_mm)))
    return {"horizontal": ang(largura_mm), "vertical": ang(altura_mm),
            "diagonal": ang(math.hypot(largura_mm, altura_mm))}


def enquadramento(largura_mm, altura_mm, focal_mm, distancia_m):
    """Quanto do mundo cabe no quadro, em metros, a essa distância."""
    if distancia_m <= 0:
        raise ValueError("distância precisa ser positiva")
    fator = distancia_m * 1000 / focal_mm
    return {"largura_m": largura_mm * fator / 1000,
            "altura_m": altura_mm * fator / 1000}


def hiperfocal(focal_mm, abertura, coc_mm):
    """Distância a partir da qual o infinito fica aceitavelmente nítido (m)."""
    if focal_mm <= 0 or abertura <= 0 or coc_mm <= 0:
        raise ValueError("focal, abertura e CoC precisam ser positivos")
    return ((focal_mm ** 2) / (abertura * coc_mm) + focal_mm) / 1000


def profundidade(focal_mm, abertura, distancia_m, coc_mm):
    """Limites de foco. `far` = None significa infinito."""
    if distancia_m <= 0:
        raise ValueError("distância precisa ser positiva")
    h_mm = hiperfocal(focal_mm, abertura, coc_mm) * 1000
    s = distancia_m * 1000
    perto = (s * (h_mm - focal_mm)) / (h_mm + s - 2 * focal_mm)
    if s >= h_mm:
        longe = None                      # infinito entra em foco
    else:
        longe = (s * (h_mm - focal_mm)) / (h_mm - s)
    return {
        "perto_m": perto / 1000,
        "longe_m": None if longe is None else longe / 1000,
        "total_m": None if longe is None else (longe - perto) / 1000,
        "hiperfocal_m": h_mm / 1000,
        "infinito_em_foco": longe is None,
    }


def crop(formato_a, formato_b):
    """Fator entre dois formatos, pela diagonal."""
    la, aa, *_ = FORMATOS[formato_a]
    lb, ab, *_ = FORMATOS[formato_b]
    return math.hypot(la, aa) / math.hypot(lb, ab)


def equivalencia(focal_mm, de, para):
    """Focal que dá o mesmo enquadramento ao trocar de formato."""
    if focal_mm <= 0:
        raise ValueError("focal precisa ser positiva")
    fator = crop(de, para)
    return {"fator": fator, "focal_equivalente_mm": focal_mm / fator}


def main(argv=None):
    p = argparse.ArgumentParser(description="Cálculos de óptica (planejamento e prep)")
    p.add_argument("--formato", default="ff", help="chave do formato (ver --listar)")
    p.add_argument("--largura", type=float, help="largura do sensor em mm (sobrepõe o formato)")
    p.add_argument("--altura", type=float, help="altura do sensor em mm")
    p.add_argument("--focal", type=float, help="distância focal em mm")
    p.add_argument("--tstop", type=float, help="abertura de trabalho (T ou f)")
    p.add_argument("--distancia", type=float, help="distância ao sujeito em metros")
    p.add_argument("--coc-divisor", type=int, default=DIVISOR_COC,
                   help="rigor do círculo de confusão (maior = mais exigente)")
    p.add_argument("--equivalencia", action="store_true")
    p.add_argument("--de", default="ff", help="formato de origem")
    p.add_argument("--para", default="s35", help="formato de destino")
    p.add_argument("--listar", action="store_true")
    a = p.parse_args(argv)

    if a.listar:
        print("\nchave    dimensões          descrição")
        print("-" * 64)
        for k, (l, h, d) in FORMATOS.items():
            print(f"{k:<8} {l:>5.2f} × {h:<5.2f} mm   {d}")
        print(f"\nCírculo de confusão = diagonal ÷ {DIVISOR_COC} (ajustável com --coc-divisor)")
        print("Medida direta: --largura 27.99 --altura 19.22\n")
        return 0

    if a.equivalencia:
        if not a.focal:
            p.error("--equivalencia exige --focal")
        for f in (a.de, a.para):
            if f not in FORMATOS:
                print(f"formato desconhecido: '{f}' — use --listar", file=sys.stderr)
                return 2
        e = equivalencia(a.focal, a.de, a.para)
        print(f"\n{a.focal:g} mm em {a.de} equivale, em enquadramento, a:")
        print(f"\n  {e['focal_equivalente_mm']:.1f} mm em {a.para}"
              f"   (fator de crop {e['fator']:.2f}×)\n")
        print("  Mesmo enquadramento não é mesma imagem: a profundidade de campo")
        print("  e a perspectiva de fundo mudam junto com o formato.\n")
        return 0

    if a.largura and a.altura:
        larg, alt, desc = a.largura, a.altura, "medida informada"
    elif a.formato in FORMATOS:
        larg, alt, desc = FORMATOS[a.formato]
    else:
        print(f"formato desconhecido: '{a.formato}' — use --listar", file=sys.stderr)
        return 2

    if not a.focal:
        p.error("informe --focal")

    c = coc(larg, alt, a.coc_divisor)
    fov = campo_de_visao(larg, alt, a.focal)

    print(f"\nLente {a.focal:g} mm · sensor {larg:g} × {alt:g} mm ({desc})\n")
    print("  CAMPO DE VISÃO")
    print(f"    horizontal            {fov['horizontal']:.1f}°")
    print(f"    vertical              {fov['vertical']:.1f}°")
    print(f"    diagonal              {fov['diagonal']:.1f}°")

    if a.distancia:
        e = enquadramento(larg, alt, a.focal, a.distancia)
        print(f"\n  ENQUADRAMENTO A {a.distancia:g} m")
        print(f"    cabe no quadro        {e['largura_m']:.2f} × {e['altura_m']:.2f} m")

    if a.tstop:
        h = hiperfocal(a.focal, a.tstop, c)
        print(f"\n  FOCO  (T/f {a.tstop:g} · CoC {c:.4f} mm)")
        print(f"    hiperfocal            {h:.2f} m")
        if a.distancia:
            d = profundidade(a.focal, a.tstop, a.distancia, c)
            if d["infinito_em_foco"]:
                print(f"    foco de              {d['perto_m']:.2f} m até o infinito")
            else:
                print(f"    foco de              {d['perto_m']:.2f} m a {d['longe_m']:.2f} m")
                print(f"    profundidade total    {d['total_m']:.2f} m")

    print("\n  Valores de planejamento — em set, a régua é o monitor com peaking.")
    print("  Profundidade de campo é critério de nitidez aceitável, não fronteira física.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
