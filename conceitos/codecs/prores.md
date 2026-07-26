---
id: prores
title: Apple ProRes
type: codec
zona: universal
aliases: [ProRes, "Apple ProRes", "422 HQ", "4444 XQ"]
tags: [codec, intraframe, mezanino, entrega, apple]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  see_also: [braw]
sources:
  - {url: "https://support.apple.com/en-us/106409", tier: oficial, ret: 2026-07-26, nota: "white paper com tabela de data rates"}
---

# Apple ProRes

**TL;DR** — família de codecs intraframe da Apple que virou o padrão de fato
para mezanino e entrega em pós: cada quadro é independente, o que torna a
edição fluida e o conform previsível. Pesado no disco, leve no processador.

## Variantes, da mais leve à mais pesada

| variante | uso típico |
|---|---|
| ProRes Proxy | offline, edição em máquina fraca |
| ProRes LT | material de baixo risco, corporativo |
| ProRes 422 | broadcast, entrega comum |
| ProRes 422 HQ | **o padrão de entrega** na maioria dos contratos |
| ProRes 4444 | material com canal alpha, VFX |
| ProRes 4444 XQ | máxima qualidade, arquivo pesado |
| ProRes RAW | RAW da Apple — categoria diferente, não confundir |

Data rates variam com resolução e frame rate; para orçar storage, usar
`tools/calc/storage.py` em vez de estimativa de cabeça.

## Por que importa

Intraframe significa **sem dependência entre quadros**: cortar em qualquer
frame não exige recalcular vizinhos. É isso que torna ProRes confortável em
edição e arriscado em cartão — o mesmo material em long-GOP ocuparia uma
fração do espaço, ao custo de processador e dor de cabeça no conform.

## Gotchas

- "ProRes" sozinho não diz nada num contrato de entrega: exigir a variante
  (422 HQ ≠ 4444) e o color space junto.
- ProRes RAW é outra coisa: apesar do nome, não é variante de ProRes — não
  substitui 4444 nem se comporta como ele na pós.
