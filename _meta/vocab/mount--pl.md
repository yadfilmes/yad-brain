---
id: mount--pl
title: PL (Positive Lock)
type: mount
zona: universal
aliases: [PL, "PL mount", "Positive Lock", "montagem PL"]
tags: [mount, optica, cine, padrao]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  see_also: [mount--e]
sources:
  - {url: "https://www.arri.com", tier: oficial, ret: 2026-07-26, nota: "origem ARRI do padrão"}
---

# PL (Positive Lock)

**TL;DR** — mount padrão do cinema profissional, criado pela ARRI: trava
mecânica de quatro flanges, sem contatos elétricos na versão clássica, flange
focal distance de 52 mm. É o encaixe que praticamente todo parque de lentes
cine de aluguel usa.

## Specs-chave

| campo | valor |
|---|---|
| flange_focal_distance_mm | 52 |
| travamento | anel de rosca sobre quatro flanges (positive lock) |
| contatos eletronicos | não na versão clássica; a variante /i e LDS carregam dados de lente |
| origem | ARRI |

## Por que importa

O FFD de 52 mm é grande — por isso lentes PL adaptam bem para mounts curtos
(E, RF, L), mas o caminho inverso é opticamente impossível sem elemento
corretor. Na prática: **corpo com mount curto aceita PL por adaptador; corpo
PL não aceita lente de mirrorless.**

## Conexões

Usado nativamente ou por troca em [[pyxis-6k]] e, via adaptador, em
[[venice-2]].
