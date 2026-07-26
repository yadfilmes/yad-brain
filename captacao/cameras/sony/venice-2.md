---
id: venice-2
title: Sony VENICE 2
type: camera
brand: sony
category: cinema / full-frame
zona: universal
aliases: [VENICE 2, Venice2, MPC-3610, "VENICE II"]
tags: [full-frame, dual-base-iso, x-ocn, cinema-digital, netflix-approved]
status: draft
confidence: baixa
updated: 2026-07-26
rel:
  made_by: [sony]
  has_native_mount: [mount--e]
  accepts_mount: [{to: mount--pl, via: adaptador-pl-sony, nota: "mount PL removível de fábrica"}]
  records_codec: [x-ocn, prores, xavc]
  supports_transfer_function: [s-log3]
  supports_colorspace: [s-gamut3-cine]
  accepts_media: [midia--axs]
  outputs_signal: [sdi]
  uses_battery_mount: [bat--v-mount]
  competes_with: [alexa-35]
  successor_of: [venice]
  certified_for: [netflix-approved]
  enables_technique: [obturador-180]
  see_also: [filtro-nd]
sources:
  - {url: "https://pro.sony/ue_US/products/digital-cinema-cameras/venice-2", tier: oficial, ret: 2026-07-26, nota: "specs de sensor, ISO e mídia"}
  - {url: "https://www.reddit.com/r/cinematography/", tier: comunidade, ret: 2026-07-26, nota: "experiência com base ISO 3200 em externa noturna"}
---

# Sony VENICE 2

**TL;DR** — câmera de cinema digital full-frame da Sony com sensor 8.6K (há
versão 6K no mesmo corpo), dual base ISO 800/3200 e gravação X-OCN interna em
mídia AXS. Rival direta da [[alexa-35]]; forte em pouca luz e em rigs
compactos graças ao corpo destacável Rialto.

## Specs-chave

| campo | valor |
|---|---|
| sensor | full-frame 8.6K CMOS (versão 6K disponível no mesmo corpo) |
| dual_base_iso | 800 / 3200 |
| mount | E-mount nativo com trava; PL removível de fábrica |
| codecs internos | X-OCN (XT/ST/LT), ProRes, XAVC |
| midia | cartões AXS |
| nd_interno | sim, filtros de vidro internos |
| latitude | <!-- verificar — valor declarado pela Sony pendente de conferência em fonte oficial paginada --> |

## Modos de gravação

Toda linha carrega suas condições — spec sem escopo não vale.

| modo | resolução | fps máx | codec | observação |
|---|---|---|---|---|
| full-frame 8.6K | 8640×5760 | <!-- verificar --> | X-OCN | modo de maior área de sensor |
| 6K full-frame | 6048×4032 | <!-- verificar --> | X-OCN | também disponível no corpo 6K nativo |
| S35 4K | 4096×2160 | <!-- verificar --> | X-OCN LT | crop para lentes S35 |

> As taxas exatas por modo dependem de versão de firmware e precisam sair da
> tabela oficial da Sony antes desta nota virar `reviewed`.

## Posicionamento

Disputa o topo do mercado de cinema e publicidade com a [[alexa-35]]. Ganha em
resolução e em desempenho de pouca luz (base 3200); perde em simplicidade de
ecossistema de acessórios, onde a ARRI é mais madura. O corpo destacável
(Rialto) é o diferencial real em carro, cockpit e gimbal pesado.

## Conexões

Fluxo de cor nativo em [[s-log3]]. Mídia AXS exige leitor próprio no carrinho
de DIT — item de orçamento, não detalhe. O ND interno reduz dependência de
[[filtro-nd]] no matte box.

## Gotchas

- Cartões AXS e leitor são exclusivos e caros: orçar mídia junto da diária.
- ProRes interno limita frame rates frente ao X-OCN — conferir a tabela por
  modo antes de fechar plano de filmagem.
- Base ISO 3200 rende bem em noite urbana, mas subexpor e levantar na pós
  entrega ruído pior do que expor correto na base alta (relato de comunidade,
  não spec).
