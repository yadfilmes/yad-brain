---
id: xavc
title: XAVC (Sony)
type: codec
brand: sony
zona: universal
aliases: [XAVC, "XAVC-I", "XAVC Intra", "XAVC-L", "XAVC HS", "XAVC S"]
tags: [codec, sony, entrega, broadcast, aquisicao]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [sony]
  wraps_in: [mxf]
  alternative_to: [prores]
  distinct_from: [x-ocn]
sources:
  - {url: "https://pro.sony/ue_US/technology/xavc", tier: oficial, ret: 2026-07-26, nota: "família de formatos"}
---

# XAVC (Sony)

**TL;DR** — família de codecs de gravação da Sony baseada em H.264/H.265,
usada dos corpos de broadcast aos de cinema como formato **leve**, ao lado do
[[x-ocn]]. Não confundir os dois: XAVC é vídeo já revelado; X-OCN é negativo.

## Principais variantes

| variante | natureza | uso típico |
|---|---|---|
| XAVC-I (Intra) | intraframe | broadcast e jornalismo; edição fluida |
| XAVC-L (Long GOP) | interframe | arquivo pequeno, jornada longa |
| XAVC HS | HEVC | eficiência maior, exige mais processador |
| XAVC S | consumo | linha Alpha e híbridas |

## Por que importa

É a opção de "gravar leve" dentro do próprio corpo Sony: multicâmera de evento,
material de apoio, backup simultâneo ao formato pesado. Numa produção que grava
[[x-ocn]] na principal, o XAVC costuma ser o proxy gravado junto.

## Gotchas

- **Long GOP complica o conform**: cortar em qualquer frame exige recalcular
  vizinhos. Para material que vai para grading pesado, preferir Intra.
- "XAVC" sozinho não define nada num contrato — exigir a variante e o bitrate.
