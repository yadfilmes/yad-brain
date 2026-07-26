---
id: aces
title: ACES (Academy Color Encoding System)
type: pipeline-cor
zona: universal
aliases: [ACES, "Academy Color Encoding System", "ACES 2065-1", ACES2065-1, ACEScct, ACEScg, ACEScc, IDT, ODT, RRT, "Output Transform"]
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
  - {url: "https://docs.acescentral.com/system-components/output-transforms/", tier: oficial, ret: 2026-07-26, loc: "Output Transforms", cit: "ACES 1 defined a Reference Rendering Transform (RRT) and an Output Device Transform (ODT). In ACES 1.1 and beyond, the RRT and ODT were concatenated and designated an Output Transform (RRT+ODT)", nota: "ODT = Output DEVICE Transform; Output Transform = RRT+ODT"}
  - {url: "https://chrisbrejon.com/cg-cinematography/chapter-1-5-academy-color-encoding-system-aces/", tier: educacao, ret: 2026-07-26, loc: "Chapter 1.5 - Academy Color Encoding System", nota: "pratica de pipeline e armadilhas de IDT"}
---

# ACES (Academy Color Encoding System)

**TL;DR** — sistema de gerenciamento de cor da Academia: cada câmera entra por
uma **IDT** (transformação de entrada), todo mundo trabalha num espaço comum e
enorme, e cada destino sai por um **Output Transform**. Resolve o
problema de misturar câmeras diferentes e entregar para telas diferentes sem
refazer o grading.

## As peças do caminho

| peça | função |
|---|---|
| **IDT** (Input Device Transform) | traz o material da câmera para ACES2065-1 — uma por câmera/curva |
| **espaço de trabalho** | onde a cor é manipulada |
| **RRT** (Reference Rendering Transform) | renderização de referência, comum a todos os destinos |
| **ODT** (Output **Device** Transform) | leva a saída do RRT para um destino específico — cinema, [[rec-709]], HDR |

O caminho, em ordem: câmera → **IDT** → espaço de trabalho → **RRT** → **ODT** → tela.

**Cuidado com "Output Transform" — o termo mudou de significado.** Em ACES 1.0
o caminho é RRT → ODT, dois passos. **De ACES 1.1 em diante, RRT e ODT foram
concatenados** num passo único chamado *Output Transform* (RRT+ODT). Ou seja:
ODT ≠ Output Transform. Documentação, tutorial e menu de software escritos em
épocas diferentes usam os dois vocabulários, e é aí que a confusão nasce.

Os dois espaços de trabalho, que são a confusão mais comum:

| encoding | primárias | codificação | serve para |
|---|---|---|---|
| **ACEScct** | AP1 | logarítmica | grading scene-referred |
| **ACEScg** | AP1 | linear | render e composição de CG |

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
