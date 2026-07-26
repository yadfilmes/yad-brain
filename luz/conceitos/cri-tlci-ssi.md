---
id: cri-tlci-ssi
title: CRI, TLCI, SSI e TM-30 — qualidade de cor de fixture
type: conceito
zona: universal
aliases: [CRI, TLCI, SSI, "TM-30", Ra, "índice de reprodução de cor", "color rendering"]
tags: [luz, cor, fotometria, metrica, qualidade]
status: draft
confidence: media
updated: 2026-07-26
rel:
  see_also: [temperatura-de-cor]
sources:
  - {url: "https://www.arri.com/en/lighting", tier: oficial, ret: 2026-07-26, nota: "métricas declaradas de fixtures"}
---

# CRI, TLCI, SSI e TM-30 — qualidade de cor de fixture

**TL;DR** — quatro métricas que tentam responder "essa luz reproduz cor
direito?". **CRI é a mais citada e a mais fraca**; TLCI foi feita para câmera;
SSI compara espectros; TM-30 é a mais completa. Fabricante anuncia o número que
lhe favorece — saber a diferença é o que evita comprar luz ruim com nota alta.

## As quatro, e para que servem

| métrica | criada para | limitação |
|---|---|---|
| **CRI (Ra)** | olho humano, era da lâmpada incandescente | média de 8 cores pastel; ignora vermelho saturado (R9), justamente o do tom de pele |
| **TLCI** | **câmera de vídeo**, pela EBU | mais relevante que CRI em audiovisual |
| **SSI** | comparar espectros entre si (Academy) | não é nota única: compara uma fonte com uma referência |
| **TM-30** | avaliação moderna completa (IES) | dois eixos — fidelidade (Rf) e saturação (Rg) |

## A armadilha do CRI 95+

Quase todo LED moderno anuncia CRI acima de 95, e ainda assim há diferença
visível entre eles na câmera. Motivos:

- CRI é **média**: um pico ruim se dilui.
- O R9 (vermelho saturado) fica de fora do índice principal — e é ele que
  decide se pele fica viva ou acinzentada.
- Fixture pode acertar o CRI e falhar no espectro contínuo, quebrando quando
  combinado com outra fonte.

Pergunta útil ao alugar: qual o **R9** e qual o **TLCI**, não qual o CRI.

## Conexões

Anda junto de [[temperatura-de-cor]]: são as duas metades da qualidade de cor
de um fixture. Kelvin certo com espectro ruim continua entregando pele estranha.

## Gotchas

- Comparar CRI entre fabricantes diferentes vale pouco: a condição de medição
  raramente é declarada.
- Misturar fixtures de espectros diferentes na mesma cena é fonte comum de
  dor de cabeça na pós — sobretudo com LED barato ao lado de HMI ou tungstênio.
