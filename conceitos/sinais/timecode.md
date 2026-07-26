---
id: timecode
title: Timecode — jam sync, drift e drop frame
type: conceito
zona: universal
aliases: [timecode, "time code", TC, LTC, "jam sync", jamsync, "drop frame", "non-drop frame", NDF, DF, "SMPTE 12M", sincronia]
tags: [timecode, audio, sincronia, multicamera, pos, set]
status: draft
confidence: baixa
updated: 2026-07-26
rel:
  governed_by: [smpte]
  requires: [genlock]
  distinct_from: [genlock]
  see_also: [obturador-180]
sources:
  - {url: "https://tentaclesync.com/products/sync-e", tier: oficial, ret: 2026-07-26, loc: "SYNC E - especificacoes", cit: "accurate with a drift of less than 1 Frame within 24 Hours and can act as Timecode Source or Jam-Sync to any External Timecode Source", nota: "ordem de grandeza do drift de um gerador dedicado"}
  - {url: "https://forum.tentaclesync.com/home/question/drop-frame-drop-frame/", tier: comunidade, ret: 2026-07-26, loc: "thread Drop Frame / Non-Drop Frame", cit: "23.976 does not have a Drop Frame option because of the integer number of frames", nota: "por que nao existe 23,976 DF"}
  - {url: "https://gearspace.com/board/post-production-forum/184636-definitive-explanation-29-97-23-98-timecode.html", tier: comunidade, ret: 2026-07-26, loc: "thread sobre 29,97 e 23,98", cit: "Two devices that independently start at 01:00:00:00 do not stay in sync -- they drift apart because their internal crystals run at slightly different rates", nota: "a razao fisica do drift, e por que jam sync nao e opcional"}
---

# Timecode — jam sync, drift e drop frame

**TL;DR** — timecode é o **endereço** de cada quadro, não a batida do relógio.
Duas máquinas que começam no mesmo número **não ficam juntas**: os cristais
correm em ritmos ligeiramente diferentes e elas afastam ao longo do dia. Por
isso existe *jam sync* — e por isso ele se repete, não se faz uma vez.

## Timecode não é genlock

Confusão frequente, e cara:

| | o que faz |
|---|---|
| **timecode** | dá **nome** a cada quadro, para a pós casar as trilhas |
| **[[genlock]]** | alinha **quando** cada quadro começa, para o switcher cortar sem quebrar |

Multicâmera ao vivo precisa dos dois. Ficção com som separado precisa
principalmente de timecode. Ter um não dispensa o outro.

## Por que o drift acontece

A causa é física, não de configuração: *"dois dispositivos que começam
independentemente em 01:00:00:00 não permanecem em sincronia — eles se afastam
porque seus cristais internos correm em ritmos ligeiramente diferentes."*

Daí a rotina de set: **jam sync periódico**. Um gerador dedicado mantém drift
abaixo de 1 quadro em 24 h; câmera e gravador sozinhos, não.

| prática | efeito |
|---|---|
| jam no início do dia | resolve o dia curto |
| **re-jam após troca de bateria** | o relógio interno some junto com a energia |
| re-jam a cada bloco | o seguro para diária longa |

## Drop frame: o que ele dropa (e o que não dropa)

A 29,97 fps o contador perde ~0,03 quadro por segundo — cerca de **108 quadros
por hora** de defasagem entre o número e o relógio de parede.

**Drop frame corrige a contagem, não o vídeo.** *Nenhum quadro do vídeo é
descartado* — o que se pula é a numeração, para que o timecode volte a bater
com o tempo real. Só isso.

| cadência | tem drop frame? |
|---|---|
| 29,97 | sim — DF ou NDF, e é preciso escolher |
| 23,976 | **não** — não existe 23,976 DF |
| 24 · 25 · 30 exatos | não faz sentido: não há defasagem a corrigir |

## Gotchas

- **Misturar DF e NDF na mesma produção é causa clássica de deriva.** A decisão
  é do projeto, e vale para câmera, som e pós — não se resolve depois.
- **Trocar bateria zera o relógio.** É o furo mais comum de jam sync: a câmera
  volta com timecode livre e ninguém percebe até a montagem.
- **Timecode de câmera "free run" ≠ jam.** Free run continua correndo, mas
  correndo *sozinho* — o drift é exatamente o mesmo.
- **Anotar a cadência no camera report.** Timecode certo com cadência errada
  declarada faz a pós casar tudo deslocado.

## Estado desta nota

`confidence: baixa`, pela 1ª linha da rubrica de confiança: há
`<!-- verificar -->` no corpo. As fontes são uma `oficial` (spec do gerador) e
duas de `comunidade`; os números de drift e de defasagem estão transcritos
delas, mas **nenhum saiu de norma SMPTE aberta na origem** — o egresso está bloqueado
(`_meta/qa/blocked.md`, B1).
<!-- verificar: SMPTE 12M para a definicao normativa de drop frame e a lista
     de cadencias suportadas -->
