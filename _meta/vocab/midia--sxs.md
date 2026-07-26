---
id: midia--sxs
title: SxS
type: midia
zona: universal
aliases: [SxS, "SxS PRO", "SxS-1", "S x S", "ExpressCard SxS"]
tags: [midia, sony, cartao, xdcam, legado]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [sony]
  alternative_to: [midia--cfexpress-b]
  distinct_from: [midia--axs]
sources:
  - {url: "https://pro.sony/s3/2018/06/27094815/4735109141-1.pdf", tier: oficial, ret: 2026-07-26, loc: "VENICE - Recording media", nota: "SxS para XAVC/ProRes/MPEG HD interno na VENICE"}
---

# SxS

**TL;DR** — cartão Sony da era XDCAM, base do ExpressCard. É a mídia **interna**
da [[venice]] para XAVC, ProRes e MPEG HD — enquanto X-OCN e RAW de 16 bits
exigem o gravador externo AXS-R7 com [[midia--axs]]. Formato em fim de ciclo:
o mercado migrou para [[midia--cfexpress-b]] e CFexpress Type A.

## Specs-chave

| campo | valor |
|---|---|
| origem | Sony (com SanDisk), base ExpressCard/34 |
| usado por | [[venice]] (interno), linha XDCAM, PMW/PXW |
| famílias | SxS PRO+ (topo), SxS-1 (entrada, menor durabilidade) |
| leitor | específico — slot ExpressCard ou leitor USB dedicado |

## SxS e AXS não são a mesma coisa

Confusão real na [[venice]], e cara: são **dois caminhos de gravação
diferentes** no mesmo corpo.

| grava | mídia | onde |
|---|---|---|
| XAVC, ProRes, MPEG HD | SxS | slots internos do corpo |
| X-OCN, RAW 16 bits | [[midia--axs]] | gravador externo AXS-R7 acoplado |

Fechar locação de VENICE sem o AXS-R7 e prometer X-OCN à pós é o erro clássico
dessa arquitetura.

## Gotchas

- **SxS-1 não é SxS PRO+.** Mesma família, durabilidade e velocidade
  sustentada bem diferentes — conferir a lista homologada, não o encaixe.
- Leitor é item de kit, não acessório opcional: notebook novo não tem
  ExpressCard há mais de uma década.
- Formato de mercado em declínio; preço por TB e disponibilidade pioram com o
  tempo. Para acervo novo, não é onde investir.
