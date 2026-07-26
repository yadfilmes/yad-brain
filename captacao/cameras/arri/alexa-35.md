---
id: alexa-35
title: ARRI ALEXA 35
type: camera
brand: arri
category: cinema / super35
zona: universal
aliases: ["ALEXA 35", "Alexa 35", AL35]
tags: [super35, arriraw, cinema-digital, latitude, netflix-approved]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [arri]
  has_native_mount: [mount--lpl]
  accepts_mount: [{to: mount--pl, via: adaptador-pl-lpl, nota: "adaptador ARRI padrão"}]
  records_codec: [arriraw, prores]
  uses_battery_mount: [bat--b-mount]
  competes_with: [venice-2]
  certified_for: [netflix-approved]
  supports_transfer_function: [log-c4]
  supports_colorspace: [arri-wide-gamut-4]
  conforms_to_pipeline: [aces]
sources:
  - {url: "https://www.arri.com/en/camera-systems/cameras/alexa-35", tier: oficial, ret: 2026-07-26, nota: "sensor, mount, codecs"}
  - {url: "https://www.cined.com", tier: lab, ret: 2026-07-26, nota: "testes independentes de latitude"}
---

# ARRI ALEXA 35

**TL;DR** — câmera de cinema Super35 da ARRI com sensor 4.6K de geração nova
(ALEV 4) e o salto de latitude que definiu a régua atual do mercado. Grava
ARRIRAW e ProRes internamente; mount LPL nativo com [[mount--pl]] por
adaptador.

## Specs-chave

| campo | valor |
|---|---|
| sensor | Super35 4.6K (ALEV 4, CMOS) |
| mount | LPL nativo; PL via adaptador ARRI |
| codecs internos | ARRIRAW, [[prores]] |
| bateria | B-Mount |
| latitude | 17 stops (declarado ARRI) <!-- verificar valor medido independente --> |
| texturas | sistema de "ARRI Textures" — grão e resposta selecionáveis |

## Posicionamento

Rival direta da [[venice-2]] no topo. Troca resolução por **latitude e
previsibilidade de cor**: entrega menos pixels que a concorrência full-frame,
e ainda assim é a escolha padrão em drama e publicidade de alto padrão porque
o negativo perdoa erro de exposição e a cor casa entre gerações.

Nota importante de escopo: é **Super35**, não full-frame. Quem precisa de
formato maior olha ALEXA 265 ou LF — comparar a 35 com a Venice 2 sem dizer
isso é comparar coisas diferentes.

## Conexões

O ecossistema de acessórios ARRI (ECS, matte boxes, B-Mount) é o mais
difundido em locadora — parte do valor da câmera está fora dela.

## Gotchas

- LPL nativo: lente PL entra por adaptador, o que muda o flange e precisa
  entrar no checklist de prep.
- ARRIRAW pesa; orçar mídia e tempo de offload junto da diária
  (`tools/calc/storage.py`).
