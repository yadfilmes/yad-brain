---
id: aces
title: ACES (Academy Color Encoding System)
type: pipeline-cor
zona: universal
aliases: [ACES, "Academy Color Encoding System", "ACES 2065-1"]
tags: [cor, pipeline, gerenciamento-de-cor, padrao, academy]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  governed_by: [ampas]
  supports_colorspace: [rec-709, s-gamut3-cine, arri-wide-gamut-4]
  distinct_from: [rec-709]
  see_also: [braw]
sources:
  - {url: "https://docs.acescentral.com/background/overview/", tier: oficial, ret: 2026-07-26, loc: "ACES System - Overview", nota: "arquitetura IDT / espaco de trabalho / ODT"}
  - {url: "https://docs.acescentral.com/encodings/acescct/", tier: oficial, ret: 2026-07-26, loc: "ACEScct Specification", nota: "encoding log em primarias AP1, para grading scene-referred"}
  - {url: "https://chrisbrejon.com/cg-cinematography/chapter-1-5-academy-color-encoding-system-aces/", tier: educacao, ret: 2026-07-26, loc: "Chapter 1.5 - Academy Color Encoding System", nota: "pratica de pipeline e armadilhas de IDT"}
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
| **IDT** (Input Transform) | traz o material da câmera para ACES2065-1 — uma por câmera/curva |
| **espaço de trabalho** | onde a cor é manipulada |
| **ODT** (Output Transform) | leva o resultado ACES scene-linear para o destino — cinema, [[rec-709]], HDR |

Os dois espaços de trabalho, que são a confusão mais comum:

| encoding | spec | primárias | codificação | serve para |
|---|---|---|---|---|
| **ACEScct** | S-2016-001 | AP1 | logarítmica | grading scene-referred |
| **ACEScg** | S-2014-004 | AP1 | linear | render e composição de CG |

Mesmas primárias, codificações diferentes — é por isso que trocar um pelo outro
produz resultado sutilmente errado em vez de obviamente quebrado.

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
