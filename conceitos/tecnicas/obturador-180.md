---
id: obturador-180
title: Regra do obturador 180°
type: conceito
zona: universal
aliases: ["180 degree shutter", "shutter 180", "regra dos 180 graus", "ângulo de obturador"]
tags: [exposicao, movimento, motion-blur, cadencia]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  see_also: [filtro-nd, flicker-parede-led]
sources:
  - {url: "https://www.arri.com", tier: oficial, ret: 2026-07-26, nota: "convenção de ângulo de obturador"}
---

# Regra do obturador 180°

**TL;DR** — manter o obturador em 180° (velocidade = 1 ÷ (2 × frame rate))
entrega o borrão de movimento a que o olho está acostumado no cinema. A 24 fps
isso é ~1/48; a 25 fps, 1/50; a 30 fps, 1/60.

## A conta

| frame rate | velocidade a 180° |
|---|---|
| 24 fps | 1/48 |
| 25 fps | 1/50 |
| 30 fps | 1/60 |
| 50 fps | 1/100 |
| 60 fps | 1/120 |

## Por que importa

O obturador é a única variável de exposição que **também** controla o
movimento. Fechar para 90° dá imagem estroboscópica (útil em ação e combate);
abrir para 270° ou 360° borra e amolece. Por isso, sob sol, não se corrige
exposição no obturador — corrige-se com [[filtro-nd]], mantendo o 180°.

É essa amarração que torna o ND item obrigatório de kit, não acessório.

## Conexões

Em parede de LED, o obturador deixa de ser só escolha estética e vira questão
de sincronia: ver [[flicker-parede-led]].

## Gotchas

- Câmera que mostra ângulo (180°) e câmera que mostra velocidade (1/48) estão
  dizendo a mesma coisa — a conversão depende do frame rate, então mudar a
  cadência muda a velocidade equivalente.
- Luz de LED barata pode bater com certas velocidades e gerar cintilação; aí a
  escolha é entre 180° e imagem limpa.
