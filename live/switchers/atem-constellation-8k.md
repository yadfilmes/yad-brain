---
id: atem-constellation-8k
title: Blackmagic ATEM Constellation 8K
type: switcher
brand: blackmagic-design
category: live / producao broadcast
zona: universal
aliases: ["ATEM Constellation 8K", "Constellation 8K", "ATEM Constellation"]
tags: [live, switcher, broadcast, 12g-sdi, 8k]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  made_by: [blackmagic-design]
  part_of_ecosystem: [ecossistema-blackmagic]
  accepts_signal: [sdi]
  controls: [tally]
  implements_standard: [smpte]
  incompatible_with: [{to: ndi, motivo: "sem HDMI e sem NDI nativo - integracao exige conversor"}]
sources:
  - {url: "https://www.blackmagicdesign.com/products/atemconstellation8k/techspecs", tier: oficial, ret: 2026-07-26, loc: "Tech Specs - Mixing Engine e Video Inputs", nota: "M/E, entradas, keyers, DVEs"}
  - {url: "https://www.blackmagicdesign.com/products/atemconstellation8k/features", tier: oficial, ret: 2026-07-26, loc: "Features - Multi View", nota: "layouts de multiview e tally"}
  - {url: "https://www.streamingmedia.com/Producer/Articles/Editorial/Featured-Articles/Review-Blackmagic-Design-ATEM-Constellation-8K-135655.aspx", tier: educacao, ret: 2026-07-26, loc: "Review - secao de limitacoes", nota: "ausencia de HDMI e publico-alvo, em uso real"}
---

# Blackmagic ATEM Constellation 8K

**TL;DR** — switcher de produção ao vivo em 2RU com **4 M/E**, **40 entradas
12G-SDI** e 16 keyers, com conversão de padrão em cada entrada. Não é para
evento pequeno: é para redação e produção com roteamento complexo. **Não tem
nenhuma entrada nem saída HDMI** — nem para o multiview.

## Specs-chave

| campo | valor |
|---|---|
| M/E | 4 |
| entradas | 40 × 12G-SDI em HD/UHD; as mesmas 40 viram 10 entradas 8K em quad link |
| saídas aux | 24 × 12G-SDI |
| keyers | 16 (chroma / linear / luma); 16 até UHD ou 4 em 8K |
| DVEs | 4 |
| SuperSource | 2 |
| multiview | 4 saídas independentes, cada uma em 4, 7, 10, 13 ou 16 janelas |
| áudio | mixer Fairlight de 156 canais, com EQ e dinâmica |
| formato físico | 2RU, com painel de controle embutido |

Toda entrada tem *up* e *cross conversion*, o que permite misturar 720p, 1080i,
1080p, UHD e 8K sem conversor externo — a característica que mais economiza
equipamento periférico neste modelo.

## Posicionamento

As 40 entradas resolvem o problema de **roteamento**, não o de corte: quem
precisa de 8 câmeras num evento não precisa disto. O público real é redação e
produção grande com muitas fontes e destinos simultâneos — e é por isso que os
4 M/E importam mais que a contagem de entradas (ver [[switcher-me]]).

## Gotchas

- **Zero HDMI, em qualquer direção** — nem no multiview. Todo monitor de
  produção e toda fonte de computador exigem conversor. É o item que mais
  aparece como surpresa em relato de uso real.
- Sem [[ndi]] nativo: integrar com fluxo em IP passa por conversor dedicado.
- O painel embutido resolve operação simples; produção séria costuma pedir
  ATEM Advanced Panel à parte, que é orçamento adicional.
- Vários controles de software simultâneos são suportados — vale distribuir
  switching, áudio e mídia entre operadores em vez de sobrecarregar um.

## Conexões

Recebe por [[sdi]] e devolve estado de ar via [[tally]]. Integra o
[[ecossistema-blackmagic]], o que reduz atrito com HyperDeck e câmeras da
mesma casa.
