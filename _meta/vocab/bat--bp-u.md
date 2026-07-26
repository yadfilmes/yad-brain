---
id: bat--bp-u
title: BP-U (padrão de bateria Sony)
type: battery-mount
zona: universal
aliases: ["BP-U", "BPU", "BP-U series", "serie BP-U", "BP-U30", "BP-U35", "BP-U60", "BP-U70", "BP-U100"]
tags: [energia, bateria, sony, camcorder]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [sony]
  alternative_to: [bat--v-mount]
sources:
  - {url: "https://pro.sony/ue_US/products/camera-batteries-and-power-supplies/bp-u35", tier: oficial, ret: 2026-07-26, loc: "BP-U35 Lithium-ion Battery (35 Wh)", nota: "capacidade 35 Wh e tensao 14,4 V"}
  - {url: "https://pro.sony/ue_US/products/camera-batteries-and-power-supplies/bp-u70", tier: oficial, ret: 2026-07-26, loc: "BP-U70 Lithium-ion Battery (72 Wh)", nota: "capacidade 72 Wh"}
---

# BP-U (padrão de bateria Sony)

**TL;DR** — bateria **encaixada no corpo**, não em placa traseira: o padrão da
linha de camcorder e cinema compacta da Sony. É o que permite [[fx6]] e
[[pyxis-6k]] operarem no ombro sem cauda de bateria — e é por isso que a
autonomia se conta em Wh, não em "uma bateria".

## Specs-chave

| modelo | capacidade | tensão |
|---|---|---|
| BP-U35 | 35 Wh | 14,4 V |
| BP-U70 | 72 Wh | 14,4 V |
| BP-U100 | 97 Wh (linha atual) | 14,4 V |

| campo | valor |
|---|---|
| origem | Sony |
| encaixe | compartimento no corpo da câmera |
| usado por | [[fx6]], FX9, FS5, FS7, linha PMW · e o [[pyxis-6k]] da Blackmagic |

## Por que a Blackmagic adotou padrão da Sony

O [[pyxis-6k]] aceita placa BP-U — decisão de mercado, não de engenharia: é o
parque de bateria que o operador de documentário já tem. Padrão de bateria é
efeito de rede, e adotar o do concorrente custa menos que convencer o mercado
a comprar um novo.

## Gotchas

- **Wh define autonomia, o encaixe não.** Trocar BP-U35 por BP-U70 dobra o
  tempo sem mudar nada no rig — é a decisão de kit mais barata que existe.
- Muito anúncio de terceiro lista compatibilidade como "PXW-FX6". O código
  Sony da FX6 é **ILME-FX6V**; PXW é a linha broadcast. A bateria serve, mas
  o código está errado — e código errado em planilha de locação vira item
  errado no caminhão.
- Adaptador V-Mount → BP-U (*dummy battery*) existe e é comum em rig de estúdio,
  onde autonomia importa mais que peso no ombro.
