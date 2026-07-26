---
id: x-ocn
title: X-OCN (eXtended Original Camera Negative)
type: codec
brand: sony
zona: universal
aliases: [X-OCN, XOCN, "X-OCN XT", "X-OCN ST", "X-OCN LT"]
tags: [codec, raw, aquisicao, sony, cinema]
status: draft
confidence: baixa
updated: 2026-07-26
rel:
  made_by: [sony]
  paired_gamut: [s-log3]
  alternative_to: [braw, arriraw]
  distinct_from: [xavc]
  accepts_media: [midia--axs]
sources:
  - {url: "https://pro.sony/ue_US/technology/x-ocn", tier: oficial, ret: 2026-07-26, nota: "definição e variantes"}
---

# X-OCN (eXtended Original Camera Negative)

**TL;DR** — formato de negativo digital da Sony, gravado pelos corpos VENICE.
Guarda a informação de sensor com compressão eficiente, entregando qualidade
próxima de RAW linear com arquivos bem menores. Vem em três pesos: XT, ST e LT.

## Variantes

| variante | posicionamento |
|---|---|
| X-OCN XT | maior qualidade, maior arquivo — trabalho de alto padrão e VFX |
| X-OCN ST | equilíbrio; o "padrão" da maioria dos jobs |
| X-OCN LT | mais leve; longas jornadas, multicâmera, orçamento de mídia apertado |

<!-- verificar — data rates por variante e resolução devem sair da tabela
     oficial da Sony antes desta nota virar reviewed -->

## Por que importa

É o que torna a [[venice-2]] viável em produção longa: RAW linear puro
consumiria mídia numa taxa que inviabiliza diárias grandes. O X-OCN entrega
latitude e maleabilidade de cor de negativo, com peso administrável — a
decisão real em set é entre XT/ST/LT, não entre RAW e não-RAW.

## Conexões

Nasce junto de [[s-log3]] e do gamut S-Gamut3.Cine: o material chega à pós
já declarando sua cena-referência, e entra em [[aces]] por IDT conhecida.

## Gotchas

- Exige mídia AXS e leitor próprio: o custo de mídia entra no orçamento junto
  do corpo, não depois.
- Comparar "X-OCN LT" com "ProRes 422 HQ" pelo tamanho de arquivo engana: são
  categorias diferentes — um é negativo, o outro é mezanino já revelado.
