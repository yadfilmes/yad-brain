---
id: pwm-brilho-led
title: PWM e brilho em painel de LED
type: conceito
zona: universal
aliases: [PWM, "pulse width modulation", "modulação por largura de pulso", "brilho LED"]
tags: [led-wall, virtual-production, flicker, brilho]
status: draft
confidence: media
updated: 2026-07-26
rel:
  see_also: [flicker-parede-led, scan-rate]
sources:
  - {url: "https://www.bromptontech.com", tier: oficial, ret: 2026-07-26, nota: "processamento e profundidade de bits em baixo brilho"}
---

# PWM e brilho em painel de LED

**TL;DR** — LED não regula intensidade baixando tensão: ele **pisca muito
rápido** e o tempo ligado define o brilho aparente (PWM). Consequência
contraintuitiva: **baixar o brilho do painel piora a estabilidade na câmera**,
porque sobra menos tempo ligado para o obturador capturar.

## Por que isso vira problema em set

O reflexo natural quando a parede está estourando na câmera é abaixar o
brilho. Mas em brilho baixo:

- os pulsos ficam mais curtos e esparsos;
- o obturador pode cair entre pulsos, produzindo banda ou tremulação;
- a profundidade efetiva de cor cai, e degradês ganham degraus visíveis.

## O que fazer em vez de baixar o brilho

| situação | saída melhor |
|---|---|
| parede estourando na exposição | fechar diafragma ou usar [[filtro-nd]] |
| parede clara demais na composição | reduzir brilho **do conteúdo**, não do painel |
| ainda assim precisa reduzir | reduzir pouco e conferir na câmera, não a olho |

## Conexões

Anda junto de [[scan-rate]]: os dois definem quanta "luz por instante" o
obturador encontra. É por isso que o teste de brilho entra no roteiro de
diagnóstico de [[flicker-parede-led]].

## Gotchas

- Processadoras boas têm modos de baixa latência e de alta profundidade em
  brilho reduzido — se a parede vai rodar escura, isso deixa de ser luxo.
- O problema não aparece no olho nem no monitor de preview: só na câmera, com
  o obturador real do take.
