---
id: aces
title: ACES (Academy Color Encoding System)
type: pipeline-cor
zona: universal
aliases: [ACES, "Academy Color Encoding System", "ACEScct", "ACEScg", AP0, AP1]
tags: [cor, pipeline, gerenciamento-de-cor, padrao, academy]
status: draft
confidence: media
updated: 2026-07-26
rel:
  governed_by: [ampas]
  see_also: [s-log3, log-c4, rec-709, braw]
sources:
  - {url: "https://docs.acescentral.com", tier: oficial, ret: 2026-07-26, nota: "documentação oficial do sistema"}
---

# ACES (Academy Color Encoding System)

**TL;DR** — sistema de gerenciamento de cor da Academia: cada câmera entra por
uma **IDT** (transformação de entrada), todo mundo trabalha num espaço comum e
enorme, e cada destino sai por uma **ODT** (transformação de saída). Resolve o
problema de misturar câmeras diferentes e entregar para telas diferentes sem
refazer o grading.

## As três peças

| peça | função |
|---|---|
| **IDT** | traz o material da câmera para o espaço comum — uma por câmera/curva |
| **espaço de trabalho** | onde a cor é manipulada (ACEScct para grading, ACEScg para VFX/render) |
| **ODT** | leva o resultado para o destino — cinema, [[rec-709]], HDR |

## Por que importa numa produtora

Três situações em que ACES paga o esforço de configurar:

1. **Multicâmera de marcas diferentes** — ARRI + Sony + Blackmagic no mesmo
   projeto, casando cor sem gambiarra de LUT.
2. **VFX** — o fornecedor recebe e devolve num espaço definido, sem "cada um
   com seu jeito".
3. **Múltiplas entregas** — cinema, streaming e broadcast saindo do mesmo
   grading por ODTs diferentes.

Para peça simples de câmera única, ACES pode ser complexidade sem retorno — o
pipeline nativo do fabricante ou o gerenciamento do Resolve resolve.

## Conexões

Recebe [[s-log3]] (Sony), [[log-c4]] (ARRI) e Blackmagic Film Gen5 ([[braw]])
por suas respectivas IDTs. É o ponto onde a espinha do grafo se fecha:
câmera → codec → curva → gamut → **pipeline**.

## Gotchas

- **IDT errada é erro silencioso**: a imagem fica plausível e a cor, errada.
  Conferir que a IDT bate com a curva declarada no camera report.
- Versão importa (ACES 1.x, 2.x): projeto e fornecedor precisam usar a mesma,
  senão o material volta diferente do que saiu.
- ACEScct e ACEScg **não** são a mesma coisa: um é para grading, outro para
  render. Trocar produz resultado sutilmente errado.
