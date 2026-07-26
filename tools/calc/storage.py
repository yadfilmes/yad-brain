#!/usr/bin/env python3
"""
Calculadora de mídia e storage — quanto cartão e quanto disco um job consome.

    python3 tools/calc/storage.py --codec braw-12-1-6k --horas 6 --cameras 2
    python3 tools/calc/storage.py --listar

Por que existe: aritmética encadeada (bitrate × tempo × câmeras × cópias) é
onde LLM erra em silêncio. Aqui é função determinística, com teste de
valor-ouro rodando no CI. Ver _meta/conventions.md.

Os bitrates são valores de PLANEJAMENTO. Bitrate real varia com conteúdo,
modo e versão de firmware — para número contratual, conferir a ficha do codec
no acervo e testar com a câmera do job.
"""

import argparse
import sys

# Mbps médios de planejamento. Cada entrada deve corresponder a uma nota do
# acervo (conceitos/codecs/) — a nota é a fonte, isto é a projeção.
CODECS = {
    "braw-12-1-6k":    (270,  "Blackmagic RAW 12:1 · 6K"),
    "braw-8-1-6k":     (410,  "Blackmagic RAW 8:1 · 6K"),
    "braw-5-1-6k":     (650,  "Blackmagic RAW 5:1 · 6K"),
    "braw-3-1-6k":     (1090, "Blackmagic RAW 3:1 · 6K"),
    "prores-422hq-4k": (880,  "ProRes 422 HQ · 4K 25p"),
    "prores-4444-4k":  (1320, "ProRes 4444 · 4K 25p"),
    "prores-422-4k":   (590,  "ProRes 422 · 4K 25p"),
    "xavc-i-4k":       (240,  "XAVC-I · 4K 25p"),
    "dnxhr-hq-4k":     (870,  "DNxHR HQ · 4K 25p"),
}

GB_POR_TB = 1000  # base decimal: é como fabricante de cartão e SSD rotula


def calcular(mbps, horas, cameras=1, copias=2):
    """Devolve o consumo em GB. Erros de entrada são explícitos, não silenciosos."""
    if mbps <= 0:
        raise ValueError("bitrate precisa ser positivo")
    if horas < 0 or cameras < 1 or copias < 1:
        raise ValueError("horas >= 0, cameras >= 1, copias >= 1")
    gb_camera = (mbps * 3600 * horas) / 8 / 1000     # Mb -> MB -> GB
    gb_bruto = gb_camera * cameras
    return {
        "gb_por_camera": gb_camera,
        "gb_bruto": gb_bruto,
        "gb_total": gb_bruto * copias,
        "cartoes_1tb": -(-gb_bruto // GB_POR_TB),     # teto
        "minutos_offload_10gbps": (gb_bruto * 8) / (10 * 60),
    }


def formatar(gb):
    return f"{gb / GB_POR_TB:.2f} TB" if gb >= GB_POR_TB else f"{gb:.0f} GB"


def main(argv=None):
    p = argparse.ArgumentParser(description="Consumo de mídia e storage por diária")
    p.add_argument("--codec", help="chave do codec (ver --listar)")
    p.add_argument("--mbps", type=float, help="bitrate direto, se o codec não estiver na tabela")
    p.add_argument("--horas", type=float, default=1.0, help="horas gravadas por câmera")
    p.add_argument("--cameras", type=int, default=1)
    p.add_argument("--copias", type=int, default=2, help="original + backups (regra 3-2-1)")
    p.add_argument("--listar", action="store_true", help="lista os codecs conhecidos")
    a = p.parse_args(argv)

    if a.listar:
        print("\ncodec                bitrate    descrição")
        print("-" * 62)
        for k, (mbps, desc) in sorted(CODECS.items()):
            print(f"{k:<20} {mbps:>5} Mbps  {desc}")
        print()
        return 0

    if a.mbps:
        mbps, desc = a.mbps, f"{a.mbps} Mbps (informado)"
    elif a.codec:
        if a.codec not in CODECS:
            print(f"codec desconhecido: '{a.codec}' — use --listar", file=sys.stderr)
            return 2
        mbps, desc = CODECS[a.codec]
    else:
        p.error("informe --codec ou --mbps")

    r = calcular(mbps, a.horas, a.cameras, a.copias)
    print(f"\n{desc}")
    print(f"{a.horas}h × {a.cameras} câmera(s) × {a.copias} cópia(s)\n")
    print(f"  por câmera            {formatar(r['gb_por_camera'])}")
    print(f"  bruto (todas)         {formatar(r['gb_bruto'])}")
    print(f"  com cópias            {formatar(r['gb_total'])}")
    print(f"  cartões de 1 TB       {int(r['cartoes_1tb'])} un.")
    print(f"  offload a 10 Gb/s     {r['minutos_offload_10gbps']:.0f} min")
    print("\n  Estimativa de planejamento — bitrate real varia com conteúdo e modo.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
