---
id: ecossistema-blackmagic
title: Ecossistema Blackmagic
type: ecossistema
brand: blackmagic-design
zona: universal
aliases: ["ecossistema Blackmagic", "mundo Blackmagic", "fluxo Blackmagic", "BMD workflow"]
tags: [ecossistema, blackmagic, live, pos, integracao]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  made_by: [blackmagic-design]
  part_of_ecosystem: [pyxis-6k, braw]
  see_also: [aces]
sources:
  - {url: "https://www.blackmagicdesign.com", tier: oficial, ret: 2026-07-26, nota: "linhas de produto e integração"}
---

# Ecossistema Blackmagic

**TL;DR** — o conjunto de câmera, switcher, gravador, conversores e software
da Blackmagic desenhado para funcionar junto: [[braw]] da câmera abre no
Resolve com a cor já declarada, o ATEM fala com o HyperDeck, e o custo total do
fluxo cai bastante em relação a montar o mesmo com peças de fabricantes
diferentes.

## O que compõe o fluxo típico

| etapa | peça |
|---|---|
| captação | Pyxis, URSA, Pocket Cinema ([[pyxis-6k]]) |
| formato | [[braw]], com metadados de cor embutidos |
| live | switchers ATEM, conversores Mini, Videohub |
| gravação/playout | HyperDeck |
| pós | DaVinci Resolve (edição, cor, Fusion, Fairlight) |

## O valor real: atrito baixo

A vantagem não é cada peça isolada ser a melhor — raramente é. É o **atrito
próximo de zero** entre elas: menos conversor no meio, menos LUT de conserto,
menos surpresa no conform. Para produtora pequena, isso costuma valer mais que
espec superior de um item avulso.

## O custo escondido

Integrar com equipamento de fora do ecossistema às vezes exige conversor,
adaptação de sinal ou etapa extra de transcodificação. Vale conferir antes de
misturar — sobretudo em live, onde não há segunda chance.

## Conexões

O [[braw]] é a peça que amarra captação e pós; entra em [[aces]] quando o
projeto exige gerenciamento de cor entre fabricantes.
