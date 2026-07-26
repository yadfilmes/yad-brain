---
id: pyxis-6k
title: Blackmagic Pyxis 6K
type: camera
brand: blackmagic-design
category: cinema / full-frame
zona: universal
aliases: [Pyxis, "Pyxis 6K", "Blackmagic Pyxis"]
tags: [full-frame, braw, cinema-digital, custo-beneficio]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [blackmagic-design]
  has_native_mount: [mount--pl]
  accepts_mount: [mount--pl]
  records_codec: [braw]
  part_of_ecosystem: [ecossistema-blackmagic]
  competes_with: [venice-2]
  budget_alternative_to: [{to: venice-2, ratio: "ordem de 1/10 do corpo"}]
  accepts_media: [midia--cfexpress-b]
  outputs_signal: [sdi]
  uses_battery_mount: [bat--bp-u]
  conforms_to_pipeline: [aces]
sources:
  - {url: "https://www.blackmagicdesign.com/products/blackmagicpyxis", tier: oficial, ret: 2026-07-26, nota: "sensor, mounts e codecs"}
---

# Blackmagic Pyxis 6K

**TL;DR** — câmera de cinema full-frame 6K da Blackmagic que grava
[[braw]] internamente, vendida em versões de mount distintas (L-mount, EF e
PL). Entrega imagem de nível superior ao seu preço; é a porta de entrada
barata para um fluxo de cor sério no DaVinci Resolve.

## Specs-chave

| campo | valor |
|---|---|
| sensor | full-frame 6K |
| codec interno | Blackmagic RAW |
| mount | versões distintas de fábrica: L-mount, EF, PL |
| gravacao externa | SSD via USB-C |
| pipeline de cor | Blackmagic Film Gen5 |
| dual_base_iso | <!-- verificar --> |

> Esta nota está `draft` e com `confidence: media` de propósito: as specs
> numéricas precisam sair da ficha técnica oficial paginada antes de subir
> para `reviewed`.

## Posicionamento

Não compete em recurso com a [[venice-2]] — compete em **custo por imagem
utilizável**. Onde o job não paga corpo de topo, ela entrega negativo digital
com latitude honesta e um caminho de cor direto para ACES no Resolve.

## Conexões

O [[braw]] carrega os metadados de Blackmagic Film Gen5, o que dispensa LUT
intermediária ao entrar num projeto gerenciado. Com a versão de mount PL
([[mount--pl]]) todo o parque cine padrão de aluguel serve.

## Gotchas

- As versões de mount são **de fábrica**: escolher errado na compra custa caro
  depois.
- Ergonomia é de corpo caixa — orçar cage, alimentação e monitoração como
  parte do pacote, não como extra.
