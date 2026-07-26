---
id: atem-constellation-8k
title: Blackmagic ATEM Constellation 8K
type: switcher
brand: blackmagic-design
category: live / producao broadcast
zona: universal
aliases: ["ATEM Constellation 8K", "Constellation 8K", "SWATEMSCN4/1ME4/8K"]
tags: [live, switcher, broadcast, 12g-sdi, 8k]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  made_by: [blackmagic-design]
  part_of_ecosystem: [ecossistema-blackmagic]
  accepts_signal: [sdi]
  outputs_signal: [sdi]
  controls: [tally]
  governed_by: [smpte]
  interoperates_with: [{to: ndi, via: conversor, nota: "sem NDI nativo; integracao passa por conversor dedicado"}]
  competes_with: [atem-constellation-hd]
sources:
  - {url: "https://www.blackmagicdesign.com/products/atemconstellation8k/techspecs", tier: oficial, ret: 2026-07-26, loc: "Tech Specs - Mixing Engine, Video Inputs, Video Outputs, Audio Mixer e Physical Installation", nota: "M/E, entradas, saidas, keyers, DVEs, audio e formato"}
  - {url: "https://www.blackmagicdesign.com/products/atemconstellation8k/features", tier: oficial, ret: 2026-07-26, loc: "Features - Multi View", nota: "layouts de multiview e tally"}
  - {url: "https://www.blackmagicdesign.com/products/atemconstellation8k/softwarecontrol", tier: oficial, ret: 2026-07-26, loc: "Software Control - multiplos operadores", nota: "varios controles de software simultaneos"}
  - {url: "https://www.streamingmedia.com/Producer/Articles/Editorial/Featured-Articles/Review-Blackmagic-Design-ATEM-Constellation-8K-135655.aspx", tier: educacao, ret: 2026-07-26, loc: "Review - avaliacao pratica do produto", nota: "ausencia de HDMI e publico-alvo, em uso real"}
---

# Blackmagic ATEM Constellation 8K

**TL;DR** — switcher de produção ao vivo em 2RU com **4 M/E**, **40 entradas
12G-SDI** e 16 keyers, com conversão de padrão em cada entrada. Não é para
evento pequeno: é para redação e produção com roteamento complexo. **Não tem
nenhuma entrada nem saída HDMI** — nem para o multiview.

## Specs-chave

| campo | valor |
|---|---|
| campo | até UHD | em 8K |
|---|---|---|
| M/E | 4 | 1 |
| entradas 12G-SDI | 40 independentes | 10 (quad link) |
| saídas aux 12G-SDI | 24 | — |
| keyers (chroma/linear/luma) | 16 | 4 |
| downstream keyers (DSK) | 4 | 2 |
| DVEs | 4 | 1 |
| SuperSource | 2 | 2 |
| multiview | 4 saídas independentes, cada uma em 4/7/10/13/16 janelas | 1 multiview 8K |

O nome de fábrica registra essa dualidade: **SWATEMSCN4/1ME4/8K** — 4 M/E até
UHD, 1 M/E em 8K.

| campo (não muda por modo) | valor |
|---|---|
| áudio | mixer Fairlight de 156 canais, com EQ e dinâmica |
| formato físico | 2RU, com painel de controle embutido |
| HDMI | **nenhum**, em nenhuma direção |

Toda entrada tem *up* e *cross conversion*, o que permite misturar 720p, 1080i,
1080p, UHD e 8K sem conversor externo — a característica que mais economiza
equipamento periférico neste modelo.

## Posicionamento

As 40 entradas resolvem o problema de **roteamento**, não o de corte: quem
precisa de 8 câmeras num evento não precisa disto. O público real é redação e
produção grande com muitas fontes e destinos simultâneos — e é por isso que os
4 M/E importam mais que a contagem de entradas (ver [[switcher-me]]).

Concorre, na faixa de produção grande, com o **Ross Carbonite** e o
**Panasonic AV-UHS500**. Dentro da própria casa, a linha **ATEM Constellation
HD / 4K Plus** cobre quem não precisa de 8K nem de 40 entradas — e é a
comparação que mais importa antes de fechar orçamento.

## Gotchas

- **Zero HDMI, em qualquer direção** — nem no multiview. Todo monitor de
  produção e toda fonte de computador exigem conversor. A ficha oficial
  registra *HDMI Multi View Outputs: None*, e uma review independente relata
  isso como surpresa de uso — é o ponto a conferir antes de fechar o kit.
- Sem [[ndi]] nativo: integrar com fluxo em IP passa por conversor dedicado.
- O painel embutido resolve operação simples; o ATEM Advanced Panel é peça
  separada, e portanto orçamento adicional.
- O fabricante declara suporte a vários controles de software simultâneos, com
  operadores distintos para switching, áudio, mídia e câmeras.

## Conexões

Recebe por [[sdi]] e devolve estado de ar via [[tally]]. Integra o
[[ecossistema-blackmagic]], o que reduz atrito com HyperDeck e câmeras da
mesma casa.
