---
id: fx6
title: Sony FX6
type: camera
brand: sony
category: cinema / full-frame compacta
zona: universal
aliases: [FX6, "Sony FX6", ILME-FX6, ILME-FX6V, ILME-FX6VK, "Cinema Line FX6"]
tags: [full-frame, dual-base-iso, xavc, nd-interno, documentario, corporativo]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  made_by: [sony]
  has_native_mount: [mount--e]
  records_codec: [xavc]
  accepts_media: [midia--cfexpress-a]
  outputs_signal: [sdi]
  enables_technique: [obturador-180]
  supports_transfer_function: [s-log3]
  supports_colorspace: [s-gamut3-cine]
  conforms_to_pipeline: [aces]
  budget_alternative_to: [venice-2]
  competes_with: [pyxis-6k]
sources:
  - {url: "https://www.sony.com/electronics/interchangeable-lens-cameras/ilme-fx6v-b", tier: oficial, ret: 2026-07-26, loc: "pagina de produto - Specifications: sensor, ISO, recording e ND", nota: "sensor, dual base ISO, formatos e ND eletronico"}
  - {url: "https://www.cined.com/sony-fx6-lab-test-external-prores-raw-vs-internal-xavc-intra/", tier: lab, ret: 2026-07-26, loc: "Lab Test - Dynamic Range e Rolling Shutter", nota: "faixa dinamica com SNR declarado e rolling shutter medido"}
  - {url: "https://www.dvxuser.com/threads/the-sony-ilme-fx6v-owners-club.374820/", tier: comunidade, ret: 2026-07-26, loc: "Owners Club - relatos de fluxo e autofoco", nota: "8 canais de audio no codec e limites de autofoco em rack"}
  - {url: "https://community.adobe.com/t5/premiere-pro-discussions/mxf-sony-fx6-and-proxy-workflow/m-p/14256982", tier: comunidade, ret: 2026-07-26, loc: "thread MXF Sony FX6 and proxy workflow", nota: "proxy interno inutilizavel em FCPX por incompatibilidade de canais"}
---

# Sony FX6

**TL;DR** — câmera de cinema full-frame compacta da Sony com sensor 10,2 MP
BSI, **ND eletrônico interno variável** e dual base ISO — o cavalo de batalha
de documentário e corporativo. Ganha do resto da faixa em pouca luz e em
agilidade de operador único; perde em faixa dinâmica medida, que fica em torno
de 11,7 stops (SNR=2, XAVC-I interno, ISO 800 — CineD, medido).

## Specs-chave

| campo | valor |
|---|---|
| sensor | full-frame BSI-CMOS, 10,2 MP (Exmor R) |
| dual base ISO | 800 / 12.800 **em S-Log3** |
| ISO máximo | 409.600 (modo de baixa luz extrema) |
| ND interno | eletrônico variável, de 1/4 a 1/128, com modo automático |
| mount | E-mount |
| curva / gamut | [[s-log3]] + [[s-gamut3-cine]] |

## Modos de gravação

| modo | resolução | fps máx | codec |
|---|---|---|---|
| C4K | 4096 × 2160 | 60 | XAVC-I / XAVC-L, 10 bits 4:2:2 |
| 4K UHD | 3840 × 2160 | 60 | XAVC-I / XAVC-L, 10 bits 4:2:2 |
| 4K UHD alta cadência | 3840 × 2160 | 120 | **crop de ~1,1× — não é full frame**; exige CFexpress Type A |
| FHD | 1920 × 1080 | 240 | XAVC-I / XAVC-L |
| RAW externo | — | — | saída por SDI/HDMI para gravador externo |

## Medições independentes

Faixa dinâmica e rolling shutter **medidos** em laboratório, com o critério de
ruído declarado — número de fabricante não é comparável a estes:

| medida | valor | condição |
|---|---|---|
| faixa dinâmica | 11,7 stops @ SNR=2; 12,8 @ SNR=1 | XAVC-I interno, ISO 800 (CineD, medido) |
| faixa dinâmica | 11,4 stops @ SNR=2; 12,6 @ SNR=1 | ProRes RAW externo, ISO 800 (CineD, medido) |
| latitude de exposição | ~8 stops (3 acima, 5 abaixo) | CineD, medido |
| rolling shutter | 8,7 ms | 4096 × 2160, 25 fps, XAVC (CineD, medido) |
| rolling shutter | 7,7 ms | 4096 × 2160, 120 fps (CineD, medido) |

Detalhe contraintuitivo do teste: o **RAW externo mede um pouco pior** que o
XAVC-I interno em faixa dinâmica. Gravar externo aqui compra maleabilidade de
pós, não latitude.

## Posicionamento

Disputa a faixa de full-frame compacta com a [[pyxis-6k]] e com a linha Canon
C400; dentro da própria casa, fica entre a FX3 (menor, sem ND interno e sem
entradas de áudio profissionais) e a FX9 (maior, para produção com equipe).

O argumento de compra não é imagem de topo — é **operação de uma pessoa só**:
ND eletrônico com automático, autofoco confiável em plano fixo e corpo que
sobe em gimbal. Para documentário e corporativo, isso vale mais que dois
stops de latitude.

Contra a [[venice-2]] não há disputa de qualidade: são faixas de preço
diferentes, e a FX6 entra como corpo B de mesma ciência de cor — mesma curva,
mesmo gamut, conform sem gambiarra.

## Conexões

O ND eletrônico interno é o que permite manter [[obturador-180]] sob sol
variável sem trocar vidro, reduzindo (sem eliminar) a dependência de
[[filtro-nd]] no matte box. Grava [[xavc]] com [[s-log3]] e
[[s-gamut3-cine]], entrando em [[aces]] pela IDT da Sony.

## Gotchas

- **O codec grava 8 canais de áudio**, mesmo o manual declarando até 4.
  Relato de comunidade no fórum do Premiere Pro: os 8 canais aparecem no
  Premiere e no Media Encoder, e o descasamento de contagem de canais entre
  original e proxy interno atrapalha o fluxo de proxy. Quem depende de proxy
  gerado na câmera precisa testar antes do job.
- **Autofoco é confiável para manter, não para racking.** Relato recorrente de
  proprietários (comunidade): o sistema segura o sujeito bem, mas transições
  de foco deliberadas continuam pedindo mão ou motor.
- **Alta cadência cobra crop e mídia.** 100/120 fps saem com crop de ~1,1× e
  exigem CFexpress Type A — não é o modo full frame que o resto da tabela
  descreve.
