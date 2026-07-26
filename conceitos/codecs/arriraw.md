---
id: arriraw
title: ARRIRAW
type: codec
brand: arri
zona: universal
aliases: [ARRIRAW, "ARRI RAW", .ari]
tags: [codec, raw, aquisicao, arri, cinema]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [arri]
  paired_gamut: [log-c4]
  alternative_to: [x-ocn, braw]
  conforms_to_pipeline: [aces]
sources:
  - {url: "https://www.arri.com/en/learn-help/learn-help-camera-system/camera-workflow", tier: oficial, ret: 2026-07-26, nota: "definição e fluxo"}
---

# ARRIRAW

**TL;DR** — formato RAW não comprimido (ou com compressão sem perdas) das
câmeras ARRI: os dados do sensor saem sem debayer, preservando o máximo de
maleabilidade para cor e VFX. É o negativo digital mais "cru" dos formatos
de uso corrente — e o mais pesado.

## O que o define

| aspecto | comportamento |
|---|---|
| debayer | feito na pós, não na câmera |
| compressão | sem perdas (ou nenhuma), conforme o modo |
| curva associada | [[log-c4]] na geração atual |
| peso | o maior entre os formatos de aquisição correntes |

## Por que importa

Onde há VFX pesado, chroma key exigente ou grading extremo, o debayer na pós
é a diferença entre conseguir e não conseguir. O preço é storage e tempo de
processamento — por isso muita produção grava ARRIRAW só nas cenas que
precisam e ProRes no resto.

Essa decisão de **misturar formatos dentro do mesmo job** é rotina, não
exceção: vale planejar no gear list e no orçamento de mídia
(`tools/calc/storage.py`).

## Conexões

Sai da [[alexa-35]] junto de [[log-c4]] e do gamut ARRI Wide Gamut 4. Entra em
[[aces]] pela IDT da ARRI, sem LUT criativa no caminho técnico.

## Gotchas

- Alguns NLEs precisam de plugin ou versão específica para ler `.ari` — checar
  antes de prometer prazo de montagem.
- "ARRIRAW" não é uma qualidade única: há modos e resoluções distintos;
  registrar qual foi usado no camera report.
