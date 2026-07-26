---
id: fx6
title: Sony FX6
type: camera
brand: sony
category: cinema / full-frame compacta
zona: universal
aliases: [FX6, "Sony FX6", ILME-FX6V, "Cinema Line FX6", PXW-FX6]
tags: [full-frame, dual-base-iso, xavc, nd-interno, documentario, corporativo]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  made_by: [sony]
  has_native_mount: [mount--e]
  records_codec: [xavc]
  supports_transfer_function: [s-log3]
  supports_colorspace: [s-gamut3-cine]
  conforms_to_pipeline: [aces]
  budget_alternative_to: [{to: venice-2, ratio: "ordem de 1/6 do corpo"}]
  competes_with: [pyxis-6k]
  alternative_to: [filtro-nd]
  see_also: [obturador-180]
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
de 11,7 stops.

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
| 4K UHD full frame | 3840 × 2160 | 120 | XAVC-I / XAVC-L, 10 bits 4:2:2 |
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
| rolling shutter | 8,7 ms | full frame, 3840 × 2160, 25 fps, XAVC |
| rolling shutter | 7,7 ms | 120 fps |

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

- **O codec grava 8 canais de áudio**, mesmo o manual declarando até 4. É
  característica do codec Sony, confirmada pelo fabricante segundo relatos de
  usuários — e quebra o *link* de proxy no Final Cut, porque o proxy interno
  sai com contagem de canais diferente do original. Quem depende de proxy
  interno precisa testar o fluxo antes do job.
- **Autofoco é confiável para manter, não para racking.** Relato recorrente de
  proprietários: o sistema segura o sujeito bem, mas transições de foco
  deliberadas continuam pedindo mão ou motor.
- Sem controle de foco externo por acessórios que a FX3 aceita — assimetria
  que surpreende quem monta kit misto.
- Dobradiça do monitor é ponto frágil relatado com frequência; vale suporte
  próprio em uso pesado.
