---
id: s-gamut3-cine
title: S-Gamut3.Cine (Sony)
type: colorspace
brand: sony
zona: universal
aliases: ["S-Gamut3.Cine", "SGamut3.Cine", "S-Gamut3"]
tags: [cor, gamut, colorspace, sony]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [sony]
  paired_gamut: [s-log3]
  conforms_to_pipeline: [aces]
  see_also: [rec-709]
sources:
  - {url: "https://pro.sony/ue_US/technology/s-log", tier: oficial, ret: 2026-07-26}
---

# S-Gamut3.Cine (Sony)

**TL;DR** — espaço de cor da Sony pensado para trabalho de cinema: mais
contido que o S-Gamut3 puro, o que o torna mais fácil de graduar, e ainda
assim bem maior que [[rec-709]]. É o par natural da curva [[s-log3]].

## Gamut e curva: a distinção que confunde

- **Curva** ([[s-log3]]) = como o brilho é codificado
- **Gamut** (S-Gamut3.Cine) = quais cores cabem no espaço

São coisas independentes, sempre declaradas juntas. "Filmei em S-Log3" sem
dizer o gamut deixa o conform ambíguo.

## Por que a variante ".Cine"

O S-Gamut3 original é enorme — cobre cores que nenhuma tela reproduz, o que
torna o grading pouco intuitivo. A variante `.Cine` aproxima o espaço do que
o fluxo de cinema realmente usa, facilitando o trabalho do colorista sem
perda prática de informação.

## Conexões

Entra em [[aces]] pela IDT correspondente. Sai para entrega via ODT, tipicamente
para [[rec-709]] ou P3.
