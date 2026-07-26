---
id: log-c4
title: LogC4 (ARRI)
type: transfer-function
brand: arri
zona: universal
aliases: [LogC4, "Log C4", "ARRI LogC4", "LogC"]
tags: [cor, log, curva, arri, cena-referida]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [arri]
  paired_gamut: [arri-wide-gamut-4]
  conforms_to_pipeline: [aces]
  distinct_from: [rec-709]
  see_also: [arriraw, alexa-35, s-log3]
sources:
  - {url: "https://www.arri.com/en/learn-help/learn-help-camera-system/image-science", tier: oficial, ret: 2026-07-26, nota: "documentação de ciência de cor"}
---

# LogC4 (ARRI)

**TL;DR** — curva logarítmica da ARRI para a geração ALEVE 4 ([[alexa-35]]),
desenhada para a latitude maior desse sensor. Sucede o LogC3, e **não é
intercambiável com ele**: material das duas gerações precisa de transformação
correta no conform, não de LUT improvisada.

## Por que existe uma curva nova

O sensor da geração 4 enxerga mais do que a curva anterior comportava. Manter
o LogC3 significaria desperdiçar a latitude extra ou distorcer a resposta —
então a ARRI redesenhou a curva junto com o gamut ARRI Wide Gamut 4.

## Conexões

Anda de par com o gamut **ARRI Wide Gamut 4**. Chega da [[alexa-35]] junto do
[[arriraw]] e entra em [[aces]] pela IDT correspondente.

Equivalente conceitual na Sony: [[s-log3]] — mesma ideia, curvas diferentes e
**não** intercambiáveis.

## Gotchas

- **LogC3 ≠ LogC4.** LUT de LogC3 aplicada em material LogC4 entrega cor
  errada com aparência plausível — o pior tipo de erro, porque passa
  despercebido até a entrega.
- Misturar câmeras de gerações diferentes no mesmo job exige declarar a curva
  de cada uma no camera report; o colorista não adivinha.
