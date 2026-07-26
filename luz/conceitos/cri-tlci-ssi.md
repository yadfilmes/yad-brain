---
id: cri-tlci-ssi
title: CRI, TLCI, SSI e TM-30 — qualidade de cor de fixture
type: conceito
zona: universal
aliases: ["indice de reproducao de cor", "índice de reprodução de cor", "color rendering", "qualidade de cor de fixture"]
tags: [luz, cor, fotometria, metrica, qualidade]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  governed_by: [cie, ebu, ampas, ies]
  distinct_from: [temperatura-de-cor]
sources:
  - {url: "https://tech.ebu.ch/docs/tech/tech3355.pdf", tier: oficial, ret: 2026-07-26, loc: "EBU Tech 3355 - Method for the Assessment of the Colorimetric Properties of Luminaires", nota: "definicao do TLCI pela EBU"}
  - {url: "https://www.researchgate.net/publication/350116795_Tutorial_Background_and_Guidance_for_Using_the_ANSIIES_TM-30_Method_for_Evaluating_Light_Source_Color_Rendition", tier: educacao, ret: 2026-07-26, loc: "Tutorial - ANSI/IES TM-30 Method", nota: "TM-30 usa 99 amostras (CES) contra 8 do CRI; IES recomenda migrar de CRI para Rf; a CIE considera obsoleto o modelo de visao por tras do CRI 13.3"}
---

# CRI, TLCI, SSI e TM-30 — qualidade de cor de fixture

**TL;DR** — quatro métricas que tentam responder "essa luz reproduz cor
direito?". **CRI é a mais citada e a mais fraca**; TLCI foi feita para câmera;
SSI compara espectros; TM-30 é a mais completa. Fabricante anuncia o número que
lhe favorece — saber a diferença é o que evita comprar luz ruim com nota alta.

## As quatro, e para que servem

**Quatro métricas, quatro órgãos diferentes** — não existe "o padrão" único de
qualidade de cor, e é daí que vem boa parte da confusão comercial.

| métrica | órgão / norma | criada para | limitação |
|---|---|---|---|
| **CRI (Ra)** | **CIE** — CIE 13.3-1995 | olho humano, era da lâmpada incandescente | média de 8 cores pastel; ignora vermelho saturado (R9), justamente o do tom de pele |
| **TLCI** | **EBU** — Tech 3355 | **câmera de vídeo** | mais relevante que CRI em audiovisual |
| **SSI** | **AMPAS** (Academy) | comparar espectros entre si | não é nota única: compara uma fonte com uma referência |
| **TM-30** | **ANSI/IES** | avaliação moderna completa | dois eixos — fidelidade (Rf) e saturação (Rg) |

## Por que o CRI perdeu autoridade

Não é opinião de mercado — é posição dos próprios órgãos:

- a **CIE** considera **obsoleto** o modelo de visão de cor por trás do
  cálculo do CRI 13.3;
- a **IES recomenda a migração de CRI para Rf** (o eixo de fidelidade do
  TM-30);
- o TM-30 avalia com **99 amostras de cor (CES)** contra as **8** do CRI.

Somando às propriedades do índice: CRI é **média** (um pico ruim se dilui), e o
R9 (vermelho saturado) fica **fora** do índice principal — e é ele que decide
se pele fica viva ou acinzentada. Um fixture pode acertar o CRI e falhar no
espectro contínuo, quebrando quando combinado com outra fonte.

Pergunta útil ao alugar: qual o **R9**, o **TLCI** ou o **Rf** — não qual
o CRI.

## Conexões

Anda junto de [[temperatura-de-cor]]: são as duas metades da qualidade de cor
de um fixture. Kelvin certo com espectro ruim continua entregando pele estranha.

## Gotchas

- Comparar CRI entre fabricantes diferentes vale pouco: a condição de medição
  raramente é declarada.
- Misturar fixtures de espectros diferentes na mesma cena é fonte comum de
  dor de cabeça na pós — sobretudo com LED barato ao lado de HMI ou tungstênio.
