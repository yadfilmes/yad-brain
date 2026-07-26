---
id: genlock
title: Genlock (sincronismo de referência)
type: conceito
zona: universal
aliases: [genlock, "gen lock", "sync reference", "referência de sincronismo", "black burst", "tri-level"]
tags: [sinal, sincronia, multicamera, live, virtual-production]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  see_also: [flicker-parede-led]
sources:
  - {url: "https://www.blackmagicdesign.com", tier: oficial, ret: 2026-07-26, nota: "sync generator e entradas de referência"}
---

# Genlock (sincronismo de referência)

**TL;DR** — sinal de referência comum que faz vários equipamentos varrerem o
quadro no mesmo instante. Sem ele, cada câmera e cada processadora começa o
quadro quando quer — o que produz corte instável ao vivo e banda rolando ao
filmar tela.

## Onde é obrigatório

| situação | por quê |
|---|---|
| multicâmera ao vivo | corte limpo entre fontes; sem genlock o switcher precisa sincronizar por frame sync e adiciona latência |
| parede de LED / virtual production | casar varredura do painel com obturador da câmera ([[flicker-parede-led]]) |
| gravação externa sincronizada | manter alinhamento entre gravadores |
| chroma key com múltiplas fontes | evitar deriva entre camadas |

## Tipos de sinal de referência

- **Black burst** — legado analógico, ainda muito usado em SD/HD.
- **Tri-level sync** — padrão para HD e acima.
- **PTP (IEEE 1588)** — referência sobre rede, base de fluxos IP (ST 2110).

## Não confundir com timecode

Genlock sincroniza **quando o quadro começa**; timecode diz **qual quadro é**.
Um resolve estabilidade de imagem, o outro resolve alinhamento na pós. Ter um
não dispensa o outro — e é confusão comum em set.

## Gotchas

- Cabo de referência precisa de terminação correta; loop mal fechado degrada
  o sinal para todo mundo na cadeia.
- Câmera sem entrada de genlock não vira multicâmera de verdade: só resta
  frame sync no switcher, com o custo de latência.
