---
id: midia--cfexpress-b
title: CFexpress Type B
type: midia
zona: universal
aliases: [CFexpress, "CFexpress Type B", "CFe B", "CF express tipo B"]
tags: [midia, cartao, padrao, gravacao]
status: draft
confidence: media
updated: 2026-07-26
rel:
  governed_by: [compactflash-association]
  alternative_to: [midia--axs, midia--codex-compact-drive]
sources:
  - {url: "https://www.compactflash.org/cfexpress", tier: oficial, ret: 2026-07-26, nota: "especificação do padrão"}
---

# CFexpress Type B

**TL;DR** — padrão aberto de cartão de alta velocidade (PCIe/NVMe por baixo),
adotado por praticamente todo fabricante de câmera fora do mundo proprietário.
É o oposto do [[midia--axs]]: mesmo cartão serve câmeras de marcas diferentes.

## Specs-chave

| campo | valor |
|---|---|
| interface | PCIe / NVMe |
| formato | Type B (há também A, menor e mais lento, e C) |
| usado por | Blackmagic, Canon, Nikon, Panasonic, RED e outros |
| leitor | genérico, USB-C ou Thunderbolt |

## Por que importa

Padrão aberto significa **cartão reaproveitável entre produções e entre
marcas**, leitor barato e mercado com concorrência. Numa produtora que aluga
corpos diferentes conforme o job, isso reduz muito o custo de mídia frente a
formatos proprietários.

## Gotchas

- **Velocidade sustentada ≠ velocidade de pico.** O número grande da embalagem
  é pico; o que interessa para gravação contínua é o sustentado — conferir a
  lista de cartões homologados pelo fabricante da câmera.
- Type A e Type B não são intercambiáveis: encaixe e desempenho diferentes.
- Cartão esquenta em gravação longa; queda de desempenho por temperatura é
  causa real de take perdido.
