---
id: braw
title: Blackmagic RAW
type: codec
brand: blackmagic-design
zona: universal
aliases: [BRAW, "Blackmagic RAW", ".braw"]
tags: [codec, raw, aquisicao, blackmagic]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [blackmagic-design]
  part_of_ecosystem: [ecossistema-blackmagic]
  conforms_to_pipeline: [aces]
  alternative_to: [x-ocn, arriraw]
  see_also: [pyxis-6k]
sources:
  - {url: "https://www.blackmagicdesign.com/products/blackmagicraw", tier: oficial, ret: 2026-07-26, loc: "Blackmagic RAW - constant bitrate e constant quality", cit: "Blackmagic RAW 3:1, 5:1, 8:1 and 12:1 use constant bitrate encoding to give customers the best possible images with predictable and consistent file sizes", nota: "o que cada familia de modo garante"}
---

# Blackmagic RAW

**TL;DR** — codec RAW parcialmente debayerizado da Blackmagic: guarda a
informação de sensor como RAW, mas move parte do processamento para dentro do
arquivo. Resultado prático: peso e fluidez de edição muito melhores que RAW
tradicional, mantendo controle de ISO, balanço e curva na pós.

## O que o diferencia

| aspecto | comportamento |
|---|---|
| debayer | parcial, feito na câmera — arquivo já chega parcialmente processado |
| controles preservados | ISO, white balance, curva/gamma editáveis depois |
| modos | taxa constante (ex.: 12:1, 8:1, 5:1, 3:1) ou qualidade constante (Q0, Q1, Q3, Q5) |
| metadados de cor | carrega o pipeline Blackmagic (Film Gen5) embutido |

## Por que importa no fluxo

Como os metadados de cor viajam no arquivo, o material entra num projeto
gerenciado no Resolve **sem LUT intermediária** — o caminho de cor já está
declarado. É o que torna o [[pyxis-6k]] uma câmera de fluxo sério apesar do
preço.

## Gotchas

- Taxa constante (12:1) dá previsibilidade de storage; qualidade constante (Q5)
  dá previsibilidade de imagem. Escolher pelo que o job precisa prever.
- Suporte fora do ecossistema Blackmagic é bom, mas não universal — conferir a
  versão do NLE antes de prometer entrega.
