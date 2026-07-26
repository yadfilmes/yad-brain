---
id: mount--lpl
title: LPL (Large Positive Lock — ARRI)
type: mount
brand: arri
zona: universal
aliases: [LPL, "LPL mount", "Large Positive Lock"]
tags: [mount, optica, cine, arri, large-format]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  made_by: [arri]
  see_also: [mount--pl, mount--e]
sources:
  - {url: "https://www.arri.com", tier: oficial, ret: 2026-07-26, nota: "especificação do mount LPL"}
---

# LPL (Large Positive Lock — ARRI)

**TL;DR** — mount da ARRI criado para formato grande: diâmetro maior e flange
focal distance menor que o [[mount--pl]] (44 mm contra 52 mm). Aceita lente PL
por adaptador; o contrário é impossível.

## Specs-chave

| campo | valor |
|---|---|
| flange_focal_distance_mm | 44 |
| diâmetro | maior que PL — comporta círculo de imagem de formato grande |
| adaptação | lente PL entra por adaptador ARRI PL-para-LPL |
| dados de lente | suporta LDS-2 |

## Por que existe

O [[mount--pl]] nasceu no mundo Super35. Sensor de formato grande exige
círculo de imagem maior, e o diâmetro do PL vira gargalo óptico. O LPL abre
espaço para lentes de cobertura maior — as Signature — mantendo
retrocompatibilidade via adaptador.

## Consequência prática no prep

Corpo LPL ([[alexa-35]]) com parque de lentes PL da locadora funciona, mas
**com adaptador no meio**: item de checklist, item de orçamento e ponto a mais
de tolerância mecânica no teste de back focus.

## Gotchas

- Adaptador PL-LPL é peça de precisão: conferir no prep, não no set.
- LPL não é "PL grande": são mounts distintos, com FFD diferente — o cálculo
  de foco muda.
