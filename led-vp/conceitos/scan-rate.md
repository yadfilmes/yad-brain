---
id: scan-rate
title: Scan rate (taxa de varredura de painel de LED)
type: conceito
zona: universal
aliases: ["scan rate", "taxa de varredura", "refresh rate", "taxa de atualização", Hz]
tags: [led-wall, virtual-production, flicker, sincronia]
status: draft
confidence: media
updated: 2026-07-26
rel:
  see_also: [flicker-parede-led, genlock, obturador-180]
sources:
  - {url: "https://www.bromptontech.com", tier: oficial, ret: 2026-07-26, nota: "documentação de processamento e refresh"}
---

# Scan rate (taxa de varredura de painel de LED)

**TL;DR** — quantas vezes por segundo o painel redesenha a imagem inteira,
em Hz. O olho humano se satisfaz com pouco; **a câmera não**. Painel de scan
baixo entrega banda horizontal ou cintilação no take, mesmo parecendo perfeito
ao vivo.

## A distinção que importa

| conceito | o que é |
|---|---|
| taxa de quadros do conteúdo | quantos quadros por segundo o vídeo tem (24, 25, 60…) |
| **scan rate / refresh** | quantas vezes o painel redesenha, independente do conteúdo |

Um painel exibindo 24 fps pode estar varrendo a 1920 Hz ou a 7680 Hz — e é
essa segunda variável que decide se a câmera enxerga banda.

## Por que painel barato falha na câmera

Painel de instalação fixa e de evento é otimizado para o olho: scan baixo é
mais barato e ninguém percebe ao vivo. Painel para virtual production precisa
de scan alto porque o obturador da câmera "fatia" a imagem — e cada fatia
mostra um estágio diferente da varredura.

Regra prática de campo: para filmar, quanto maior o scan, mais folga na
escolha de obturador. Painel de evento reaproveitado em filmagem é a origem
mais comum de [[flicker-parede-led]].

## Conexões

Interage diretamente com [[obturador-180]] (a velocidade que a câmera usa) e
com [[genlock]] (a referência comum que impede a varredura de deslizar).

## Gotchas

- Especificação de fabricante às vezes mistura "refresh" e "scan" — pedir o
  número em Hz e a que ele se refere antes de fechar aluguel.
- Aumentar brilho do painel costuma melhorar a estabilidade percebida; ver
  [[pwm-brilho-led]] para entender por quê.
