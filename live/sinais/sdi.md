---
id: sdi
title: SDI (Serial Digital Interface)
type: interface
zona: universal
aliases: [SDI, "3G-SDI", "6G-SDI", "12G-SDI", "HD-SDI", "SDI 12G"]
tags: [live, sinal, broadcast, cabo, bnc]
status: draft
confidence: media
updated: 2026-07-26
rel:
  governed_by: [smpte]
  alternative_to: [ndi]
  see_also: [genlock]
sources:
  - {url: "https://www.smpte.org/standards", tier: oficial, ret: 2026-07-26, nota: "série de normas SDI"}
---

# SDI (Serial Digital Interface)

**TL;DR** — padrão de vídeo profissional sobre cabo coaxial com conector BNC:
**trava**, aceita tirada longa e não negocia handshake como o HDMI. É a razão
de todo set e estúdio sério usar SDI onde o HDMI cairia.

## Gerações e o que cada uma carrega

| geração | banda | uso típico |
|---|---|---|
| HD-SDI | 1,485 Gb/s | HD 1080i |
| 3G-SDI | 2,970 Gb/s | 1080p60 |
| 6G-SDI | 6 Gb/s | UHD 30p |
| 12G-SDI | 12 Gb/s | **UHD 60p em cabo único** |

Antes do 12G, UHD exigia quatro cabos 3G em paralelo (*quad link*) — arranjo
que ainda existe em equipamento mais antigo e é fonte de confusão em set.

## Por que SDI e não HDMI

| aspecto | SDI | HDMI |
|---|---|---|
| conector | BNC, com trava | atrito, solta |
| distância | dezenas a centenas de metros | poucos metros na prática |
| negociação | não há — o sinal simplesmente flui | EDID/HDCP podem falhar |
| áudio embutido | sim | sim |

O ponto decisivo não é qualidade de imagem: é **previsibilidade**. Cabo que
solta ou handshake que falha no meio de um ao vivo não tem segunda chance.

## Conexões

Anda junto de [[genlock]] em qualquer operação multicâmera. Concorre com
[[ndi]] onde a infraestrutura já é de rede.

## Gotchas

- Cabo coaxial tem classificação por banda: cabo que passa 3G pode falhar em
  12G na mesma tirada. Conferir a especificação, não só o conector.
- Tirada longa em 12G é mais sensível que em 3G — em distância grande, muitas
  vezes vale converter para fibra.
