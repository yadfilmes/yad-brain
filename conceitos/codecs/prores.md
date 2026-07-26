---
id: prores
title: Apple ProRes
type: codec
zona: universal
aliases: [ProRes, "Apple ProRes", "422 HQ", "4444 XQ"]
tags: [codec, intraframe, mezanino, entrega, apple]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [apple]
  alternative_to: [braw]
  wraps_in: [mov]
sources:
  - {url: "https://support.apple.com/en-us/102207", tier: oficial, ret: 2026-07-26, loc: "About Apple ProRes", cit: "The target data rate of Apple ProRes 422 HQ is approximately 220 Mbps at 1920 x 1080 and 29.97 fps", nota: "taxas-alvo por variante; substitui a URL 106409 que o acervo citava e que nao resolve para pagina de ProRes"}
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

## Taxa-alvo, com o escopo em que ela vale

Todos os números da Apple são declarados **a 1920 × 1080 e 29,97 fps** — é a
condição, não uma nota de rodapé. Em 4K a taxa sobe na proporção da área, e é
por isso que orçar mídia pela tabela de HD subestima por volta de 4×.

| variante | taxa-alvo @ 1080p29,97 |
|---|---|
| ProRes 422 HQ | ~220 Mb/s |
| ProRes 4444 | ~330 Mb/s (fontes 4:4:4) |
| ProRes 4444 XQ | ~500 Mb/s (fontes 4:4:4) |

Para dimensionar de verdade, use a calculadora em vez da regra de três:

```
python3 tools/calc/storage.py --listar
```
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
