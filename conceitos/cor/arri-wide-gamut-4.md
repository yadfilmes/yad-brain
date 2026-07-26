---
id: arri-wide-gamut-4
title: ARRI Wide Gamut 4
type: colorspace
brand: arri
zona: universal
aliases: ["ARRI Wide Gamut 4", AWG4, "AWG 4", "Wide Gamut 4"]
tags: [cor, gamut, colorspace, arri]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [arri]
  paired_gamut: [log-c4]
  conforms_to_pipeline: [aces]
  see_also: [s-gamut3-cine, rec-709]
sources:
  - {url: "https://www.arri.com/en/learn-help/learn-help-camera-system/image-science", tier: oficial, ret: 2026-07-26}
---

# ARRI Wide Gamut 4

**TL;DR** — espaço de cor da ARRI para a geração ALEV 4 ([[alexa-35]]), par
obrigatório da curva [[log-c4]]. Sucede o ARRI Wide Gamut 3 e acompanha o
salto de latitude do sensor novo.

## Gamut e curva andam juntos

`LogC4 + AWG4` é um conjunto: usar a curva de uma geração com o gamut de outra
produz cor errada de aparência plausível. O camera report precisa registrar
**os dois**.

## Conexões

Chega em [[arriraw]] da [[alexa-35]] e entra em [[aces]] pela IDT da ARRI.
Equivalente conceitual na Sony: [[s-gamut3-cine]].

## Gotchas

- Material AWG3 e AWG4 no mesmo projeto exige transformação explícita entre
  gerações — não é "a mesma cor ARRI".
