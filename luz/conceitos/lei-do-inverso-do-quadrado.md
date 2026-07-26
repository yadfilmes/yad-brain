---
id: lei-do-inverso-do-quadrado
title: Lei do inverso do quadrado
type: conceito
zona: universal
aliases: ["inverse square law", "lei do quadrado inverso", "queda de luz", "falloff"]
tags: [luz, fotometria, exposicao, fisica]
status: draft
confidence: media
updated: 2026-07-26
rel:
  see_also: [temperatura-de-cor, filtro-nd]
sources:
  - {url: "https://www.arri.com/en/lighting", tier: oficial, ret: 2026-07-26, nota: "dados fotométricos por distância"}
---

# Lei do inverso do quadrado

**TL;DR** — dobrar a distância entre a luz e o sujeito derruba a intensidade a
**um quarto** (dois stops), não à metade. É a física que explica por que
aproximar a luz um pouco muda tudo, e por que a fotometria do fabricante só
faz sentido com a distância declarada junto.

## A conta em stops

| distância | intensidade relativa | diferença |
|---|---|---|
| 1 m | 100% | referência |
| 1,4 m | 50% | −1 stop |
| 2 m | 25% | −2 stops |
| 2,8 m | 12,5% | −3 stops |
| 4 m | 6,25% | −4 stops |

Regra de bolso: **multiplicar a distância por 1,4 = perder 1 stop.**

## Por que isso decide o visual da cena

A queda não é uniforme no espaço: perto da fonte, um passo do ator muda muito a
exposição; longe, quase não muda.

| situação | consequência prática |
|---|---|
| luz **perto** do sujeito | queda rápida — fundo escurece, mas o ator "queima" se andar para a frente |
| luz **longe** | queda lenta — exposição estável em movimento, fundo acompanha |

É por isso que separar sujeito do fundo é, muitas vezes, questão de mover a
luz — não de acrescentar outra.

## Fotometria de fabricante

Todo dado de lux publicado vem amarrado a uma distância (tipicamente 1 m ou
3 m). Comparar dois fixtures exige a **mesma distância** e a mesma ótica —
comparar "lux a 1 m" de um com "lux a 3 m" de outro é erro que aparece direto
em tabela de comparação mal feita.

## Gotchas

- A lei vale para fonte pontual. Softbox grande perto do sujeito comporta-se
  de forma mais suave que a fórmula sugere.
- Refletor e ambiente devolvem luz: em sala pequena e clara, a queda medida é
  menor que a teórica.
