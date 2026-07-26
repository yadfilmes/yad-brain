---
id: filtro-nd
title: Filtro ND (densidade neutra)
type: conceito
zona: universal
aliases: [ND, "neutral density", IRND, VND, "densidade neutra", "filtro de densidade neutra"]
tags: [exposicao, optica, filtro, fotometria]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  see_also: [venice-2, pyxis-6k]
sources:
  - {url: "https://tiffen.com", tier: oficial, ret: 2026-07-26, nota: "escala de densidade e tipos"}
---

# Filtro ND (densidade neutra)

**TL;DR** — filtro cinza que corta luz sem (idealmente) alterar cor, para
manter diafragma aberto e obturador 180° sob sol forte. Densidade em stops:
ND0.3 = 1 stop, ND0.6 = 2, ND0.9 = 3, ND1.2 = 4, ND1.8 = 6, ND2.1 = 7.

## Tipos

| tipo | quando usar | risco |
|---|---|---|
| fixo | qualidade máxima, um valor por vidro | precisa trocar vidro em set |
| variável (VND) | agilidade em documentário e run-and-gun | "cruz" escura e dominante de cor nas densidades altas |
| IRND | digital com ND forte | sem ele, pretos puxam magenta/marrom por vazamento de infravermelho |

## Por que importa

A regra do obturador 180° amarra a velocidade ao frame rate; sob sol, a única
saída para manter diafragma de trabalho é cortar luz na frente da lente. Sem
ND você escolhe entre estourar, fechar demais (e perder desfoque) ou quebrar a
cadência do movimento.

## Conexões

Câmeras com ND interno — como a [[venice-2]] — reduzem muito a troca de vidro
em set. Sem ND interno, o filtro vive no matte box.

## Gotchas

- VND barato em grande-angular: vinheta em cruz nas densidades altas.
- Empilhar ND + polarizador derruba mais luz do que a conta simples sugere e
  pode criar reflexo interno.
- ND forte em sensor digital **sem** corte de infravermelho degrada os pretos —
  é o caso clássico de precisar de IRND, não ND comum.
