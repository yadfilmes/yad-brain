#!/usr/bin/env python3
"""
Calculadora de parede de LED — gabinetes, resolução, dados, energia e sincronia.

    python3 tools/calc/led_wall.py --largura 6 --altura 3 --pitch 2.6
    python3 tools/calc/led_wall.py --largura 6 --altura 3 --pitch 2.6 --fps 24
    python3 tools/calc/led_wall.py --listar

Responde as cinco perguntas que decidem um job de parede:
  1. quantos gabinetes cabem e qual a resolução final
  2. quantas portas da processadora são necessárias
  3. quanta energia — em ampères e em circuitos, a 220 V ou 127 V
  4. quanto peso a estrutura vai receber
  5. que refresh o painel precisa para o obturador da câmera não ver banda

Por que existe: a conta é encadeada (dimensão -> pitch -> pixels -> portas ->
energia) e errar no orçamento significa chegar em set com processadora
insuficiente ou circuito estourando. Ver _meta/conventions.md.

AVISO: os valores padrão são de PLANEJAMENTO, baseados em gabinete típico de
locação. Todo painel real tem ficha própria — usar os parâmetros para informar
os números do equipamento contratado. Dimensionamento elétrico definitivo é
responsabilidade de profissional habilitado (NR-10).
"""

import argparse
import math
import sys

# Perfis de gabinete comuns em locação. Números de PLANEJAMENTO: confirmar
# sempre na ficha do painel contratado.
GABINETES = {
    "500x500": (500, 500, "meio metro — o mais comum em VP e evento"),
    "500x1000": (500, 1000, "meio por um metro — menos junta na vertical"),
    "600x337": (600, 337, "formato 16:9 de alguns fabricantes"),
    "1000x1000": (1000, 1000, "um metro — instalação fixa"),
}

# Consumo por metro quadrado de painel (W/m²). Média é o consumo real numa
# imagem típica; pico é branco pleno a 100% de brilho.
CONSUMO_MEDIO_W_M2 = 250
CONSUMO_PICO_W_M2 = 800
PESO_KG_M2 = 32

# Capacidade de porta da processadora, em pixels a 60 Hz e 8 bits.
# Cai com frame rate alto, profundidade de bits maior e HDR — por isso o
# parâmetro existe. Valor conservador de planejamento.
PIXELS_POR_PORTA = 650_000


def calcular(largura_m, altura_m, pitch_mm, gab_l_mm=500, gab_a_mm=500,
             pixels_por_porta=PIXELS_POR_PORTA, tensao=220, disjuntor_a=32,
             brilho_pct=100):
    """Devolve o dimensionamento completo. Erros de entrada falham alto."""
    if min(largura_m, altura_m) <= 0:
        raise ValueError("largura e altura precisam ser positivas")
    if pitch_mm <= 0:
        raise ValueError("pitch precisa ser positivo")
    if min(gab_l_mm, gab_a_mm) <= 0:
        raise ValueError("dimensão de gabinete precisa ser positiva")
    if not 1 <= brilho_pct <= 100:
        raise ValueError("brilho deve estar entre 1 e 100 por cento")

    # --- composição física ---
    cab_x = math.ceil(largura_m * 1000 / gab_l_mm)
    cab_y = math.ceil(altura_m * 1000 / gab_a_mm)
    cabinetes = cab_x * cab_y

    px_cab_x = int(gab_l_mm / pitch_mm)
    px_cab_y = int(gab_a_mm / pitch_mm)
    res_x = cab_x * px_cab_x
    res_y = cab_y * px_cab_y
    pixels = res_x * res_y

    area_real = (cab_x * gab_l_mm / 1000) * (cab_y * gab_a_mm / 1000)

    # --- dados ---
    portas = math.ceil(pixels / pixels_por_porta) if pixels else 0

    # --- energia (brilho entra linear no consumo) ---
    fator = brilho_pct / 100
    w_medio = area_real * CONSUMO_MEDIO_W_M2 * fator
    w_pico = area_real * CONSUMO_PICO_W_M2 * fator
    a_medio = w_medio / tensao
    a_pico = w_pico / tensao
    # circuitos dimensionados pelo pico, com 80% de folga (regra de projeto)
    circuitos = math.ceil(a_pico / (disjuntor_a * 0.8)) if a_pico else 0

    return {
        "cabinetes": cabinetes, "cab_x": cab_x, "cab_y": cab_y,
        "resolucao": (res_x, res_y), "pixels": pixels,
        "largura_real_m": cab_x * gab_l_mm / 1000,
        "altura_real_m": cab_y * gab_a_mm / 1000,
        "area_m2": area_real,
        "portas": portas,
        "w_medio": w_medio, "w_pico": w_pico,
        "a_medio": a_medio, "a_pico": a_pico,
        "circuitos": circuitos,
        "peso_kg": area_real * PESO_KG_M2,
    }


def refresh_seguro(fps, shutter_denominador=None):
    """Refresh mínimo recomendado para o obturador não enxergar a varredura.

    Regra prática de campo, não norma: o refresh precisa ser múltiplo alto da
    velocidade de obturador. Abaixo de ~3840 Hz, câmera costuma ver banda.
    Ver as notas scan-rate e flicker-parede-led.
    """
    if fps <= 0:
        raise ValueError("fps precisa ser positivo")
    shutter = shutter_denominador or int(fps * 2)   # regra do obturador 180°
    return {
        "shutter_180": f"1/{int(fps * 2)}",
        "shutter_usado": f"1/{shutter}",
        "refresh_minimo_hz": 3840,
        "refresh_confortavel_hz": max(7680, shutter * 100),
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Dimensionamento de parede de LED")
    p.add_argument("--largura", type=float, help="largura desejada em metros")
    p.add_argument("--altura", type=float, help="altura desejada em metros")
    p.add_argument("--pitch", type=float, help="pixel pitch em mm (ex.: 2.6)")
    p.add_argument("--gabinete", default="500x500", help="perfil ou LxA em mm")
    p.add_argument("--porta", type=int, default=PIXELS_POR_PORTA,
                   help="capacidade de pixels por porta da processadora")
    p.add_argument("--tensao", type=int, default=220, choices=[127, 220])
    p.add_argument("--disjuntor", type=int, default=32, help="ampères por circuito")
    p.add_argument("--brilho", type=int, default=100, help="brilho em %% (afeta consumo)")
    p.add_argument("--fps", type=float, help="frame rate da câmera, para a seção de sincronia")
    p.add_argument("--listar", action="store_true", help="lista os perfis de gabinete")
    a = p.parse_args(argv)

    if a.listar:
        print("\nperfil        dimensão      descrição")
        print("-" * 62)
        for k, (l, h, d) in GABINETES.items():
            print(f"{k:<13} {l}x{h} mm   {d}")
        print(f"\nTambém aceita medida direta: --gabinete 500x500")
        print(f"Consumo de planejamento: {CONSUMO_MEDIO_W_M2} W/m² médio, "
              f"{CONSUMO_PICO_W_M2} W/m² pico\n")
        return 0

    if not all([a.largura, a.altura, a.pitch]):
        p.error("informe --largura, --altura e --pitch")

    if a.gabinete in GABINETES:
        gl, ga, _ = GABINETES[a.gabinete]
    else:
        try:
            gl, ga = (int(x) for x in a.gabinete.lower().split("x"))
        except ValueError:
            print(f"gabinete inválido: '{a.gabinete}' — use --listar", file=sys.stderr)
            return 2

    r = calcular(a.largura, a.altura, a.pitch, gl, ga, a.porta,
                 a.tensao, a.disjuntor, a.brilho)

    print(f"\nParede {a.largura} × {a.altura} m · pitch {a.pitch} mm · "
          f"gabinete {gl}×{ga} mm")
    print(f"Brilho considerado: {a.brilho}%  ·  rede {a.tensao} V\n")

    print("  COMPOSIÇÃO")
    print(f"    gabinetes            {r['cabinetes']} ({r['cab_x']} × {r['cab_y']})")
    print(f"    medida real          {r['largura_real_m']:.2f} × {r['altura_real_m']:.2f} m"
          f"   ({r['area_m2']:.1f} m²)")
    print(f"    resolução            {r['resolucao'][0]} × {r['resolucao'][1]} px")
    print(f"    total de pixels      {r['pixels']:,}".replace(",", "."))

    print("\n  DADOS")
    print(f"    portas necessárias   {r['portas']}  (a {a.porta:,} px/porta)".replace(",", "."))

    print("\n  ENERGIA")
    print(f"    consumo médio        {r['w_medio']/1000:.1f} kW   ({r['a_medio']:.0f} A)")
    print(f"    consumo de pico      {r['w_pico']/1000:.1f} kW   ({r['a_pico']:.0f} A)")
    print(f"    circuitos de {a.disjuntor} A      {r['circuitos']}  (dimensionado pelo pico, 80% de folga)")

    print("\n  ESTRUTURA")
    print(f"    peso aproximado      {r['peso_kg']:.0f} kg")

    if a.fps:
        s = refresh_seguro(a.fps)
        print("\n  SINCRONIA COM A CÂMERA")
        print(f"    obturador 180°       {s['shutter_180']} a {a.fps:g} fps")
        print(f"    refresh mínimo       {s['refresh_minimo_hz']} Hz")
        print(f"    refresh confortável  {s['refresh_confortavel_hz']} Hz")
        print("    genlock entre câmera e processadora: obrigatório em multicâmera")

    print("\n  Valores de PLANEJAMENTO. Confirmar na ficha do painel contratado.")
    print("  Dimensionamento elétrico definitivo exige profissional habilitado (NR-10).\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
