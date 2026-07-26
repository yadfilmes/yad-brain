---
id: s-log3
title: S-Log3 (Sony)
type: transfer-function
brand: sony
zona: universal
aliases: ["S-Log3", SLog3, "S Log 3", "S-Log3/S-Gamut3.Cine"]
tags: [cor, log, curva, sony, cena-referida]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [sony]
  paired_gamut: [s-gamut3-cine]
  conforms_to_pipeline: [aces]
  distinct_from: [rec-709, s-gamut3-cine]
  see_also: [x-ocn, venice-2]
sources:
  - {url: "https://pro.sony/ue_US/technology/s-log", tier: oficial, ret: 2026-07-26, nota: "definição da curva e uso"}
---

# S-Log3 (Sony)

**TL;DR** — curva logarítmica da Sony que comprime a latitude do sensor num
sinal de 10 bits sem estourar altas nem esmagar baixas. Imagem parece lavada e
sem contraste no monitor — **isso é correto**: S-Log3 é formato de trabalho,
não de exibição.

## O que é uma curva log, em uma linha

O sensor enxerga muito mais faixa dinâmica do que 10 bits em vídeo padrão
comportam. A curva log redistribui essa faixa dando mais bits às sombras (onde
o olho enxerga ruído) e menos às altas — preservando informação que o
[[rec-709]] jogaria fora.

## Como usar na prática

| situação | prática |
|---|---|
| monitoração em set | LUT de visualização por cima (não grava a LUT) |
| exposição | expor pela ferramenta da câmera, não pelo que parece bonito no monitor |
| pós | aplicar IDT e trabalhar em espaço gerenciado ([[aces]]) |

## Conexões

Anda de par com o gamut **S-Gamut3.Cine** — dizer "S-Log3" sem dizer o gamut
é meia informação, e é a origem de metade dos problemas de cor em conform.
Nasce com o material [[x-ocn]] na [[venice-2]].

## Gotchas

- **Não confundir curva com gamut**: S-Log3 é a curva (como o brilho é
  codificado); S-Gamut3.Cine é o espaço de cor (quais cores existem). Trocar um
  pelo outro no conform desloca a cor inteira.
- Gravar com LUT "queimada" na imagem destrói a vantagem da curva — a LUT vive
  na monitoração, não no arquivo.
- Subexpor em log e levantar na pós entrega ruído. Log dá latitude, não
  imunidade a erro de exposição.
