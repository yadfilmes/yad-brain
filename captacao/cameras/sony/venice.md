---
id: venice
title: Sony VENICE (primeira geração)
type: camera
brand: sony
category: cinema / full-frame
zona: universal
aliases: [VENICE, "Sony VENICE", "VENICE 1", MPC-3610]
tags: [full-frame, dual-base-iso, x-ocn, cinema-digital, legacy]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [sony]
  has_native_mount: [mount--e]
  accepts_mount: [mount--pl]
  records_codec: [prores, xavc, {to: x-ocn, via: axs-r7, nota: "só com o gravador externo acoplado"}]
  accepts_media: [midia--sxs, {to: midia--axs, via: axs-r7}]
  outputs_signal: [sdi]
  uses_battery_mount: [bat--v-mount]
  supports_transfer_function: [s-log3]
  supports_colorspace: [s-gamut3-cine]
  predecessor_of: [venice-2]
  competes_with: [alexa-35]
  certified_for: [netflix-approved]
sources:
  - {url: "https://pro.sony/s3/2018/06/27094815/4735109141-1.pdf", tier: oficial, ret: 2026-07-26, loc: "Digital Motion Picture Camera VENICE - Recording media e Interfaces", nota: "XAVC/ProRes/MPEG HD em SxS interno; X-OCN e RAW 16 bits exigem AXS-R7 com AXSM; saida SDI 6G/12G comutavel"}
---

# Sony VENICE (primeira geração)

**TL;DR** — primeira geração da linha VENICE: sensor full-frame 6K, dual base
ISO 500/2500. Grava XAVC e ProRes **internamente em [[midia--sxs]]**; [[x-ocn]]
e RAW de 16 bits só com o **gravador externo AXS-R7** acoplado, em
[[midia--axs]]. Continua muito presente em locadora, a diária bem menor que a
[[venice-2]].

## Specs-chave

| campo | valor |
|---|---|
| sensor | full-frame 6K |
| dual_base_iso | 500 / 2500 |
| mount | E-mount com trava; PL removível |
| codecs internos | [[prores]], [[xavc]], MPEG HD — em [[midia--sxs]] |
| codecs externos | [[x-ocn]] e RAW 16 bits — **exigem AXS-R7 + [[midia--axs]]** |
| saída de vídeo | [[sdi]] 6G/12G comutável |
| energia | [[bat--v-mount]] (placa do AXS-R7 ou placa acessória) |
| nd_interno | sim |

## O erro de locação que esta arquitetura produz

**X-OCN não é codec interno da VENICE 1.** Fechar a locação do corpo sem o
AXS-R7 e prometer X-OCN à pós é o erro clássico — e só aparece no primeiro dia
de set. O corpo sozinho grava XAVC/ProRes em SxS; o RAW mora no gravador
acoplado, que é item separado de orçamento, com sua própria mídia e seu
próprio leitor.

Na [[venice-2]] isso mudou: ela grava X-OCN internamente em AXS.

## Por que ainda importa

Câmera de geração anterior não vira lixo: vira **opção de custo**. Para
publicidade e conteúdo em que o salto de resolução da [[venice-2]] não muda a
entrega, a VENICE 1 entrega a mesma ciência de cor Sony e o mesmo fluxo de pós
por uma fração da diária.

A diferença prática relevante é o par de base ISO — 500/2500 contra 800/3200 —
que muda o cálculo de luz em cena noturna.

## Gotchas

- **Duas famílias de mídia no mesmo corpo** — [[midia--sxs]] interno e
  [[midia--axs]] no AXS-R7. Dois leitores, dois custos, dois fluxos de
  descarga. O custo de mídia não cai junto com a diária.
- Conferir a versão de firmware disponível na locadora: recursos variam
  bastante ao longo da vida do produto.
