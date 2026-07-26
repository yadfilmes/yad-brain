---
id: midia--axs
title: Cartão AXS (Sony)
type: midia
brand: sony
zona: universal
aliases: [AXS, "AXS card", "cartão AXS", AXSM, "AXS-R7"]
tags: [midia, cartao, sony, cinema, gravacao]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [sony]
  alternative_to: [midia--cfexpress-b]
sources:
  - {url: "https://pro.sony/ue_US/products/memory-cards", tier: oficial, ret: 2026-07-26, nota: "linha de cartões profissionais"}
---

# Cartão AXS (Sony)

**TL;DR** — mídia proprietária da Sony para as câmeras VENICE, exigida pelas
taxas do [[x-ocn]]. Exclusiva do ecossistema: precisa de leitor próprio, e o
custo dela entra no orçamento junto do corpo da câmera, não depois.

## Specs-chave

| campo | valor |
|---|---|
| fabricante | exclusivo Sony |
| usada por | [[venice-2]] e linha VENICE |
| leitor | dedicado (linha AXS-AR), não é CFexpress nem SD |
| capacidades | <!-- verificar — tabela oficial por modelo --> |

## Por que importa no orçamento

Mídia proprietária é decisão de negócio disfarçada de detalhe técnico: além do
preço por cartão, o kit exige leitor exclusivo no carrinho de DIT, e não dá
para "pegar um cartão emprestado" de outra produção com câmera diferente.

Ao orçar diária com VENICE, contar cartões suficientes para o ciclo
completo de gravar → offload → verificar → liberar, e não para o total de
horas (`tools/calc/storage.py`).

## Gotchas

- Sem leitor AXS no set, o offload para; não é item substituível na hora.
- Cartão cheio em meio a take longo é falha de planejamento de mídia, não de
  equipamento — dimensionar antes.
