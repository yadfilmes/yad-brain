---
id: shuttersync
title: ShutterSync (Brompton)
type: conceito
brand: brompton
zona: universal
aliases: [ShutterSync, "Shutter Sync", "sincronia de obturador"]
tags: [led-wall, virtual-production, flicker, sincronia, brompton]
status: draft
confidence: media
updated: 2026-07-26
rel:
  requires: [genlock]
  see_also: [flicker-parede-led, scan-rate]
sources:
  - {url: "https://www.bromptontech.com", tier: oficial, ret: 2026-07-26, nota: "recurso de sincronização de obturador"}
---

# ShutterSync (Brompton)

**TL;DR** — recurso das processadoras Brompton que alinha a varredura do
painel com o obturador da câmera, permitindo ajuste fino de **fase** além do
casamento de frequência. É a ferramenta que resolve a banda residual quando
[[genlock]] e obturador correto já não bastam.

## O que ele resolve que o genlock sozinho não resolve

O genlock garante que câmera e painel comecem o quadro **juntos**. Mas o
obturador abre por uma fração desse quadro — e onde essa fração cai dentro do
ciclo de varredura ainda pode produzir banda. O ShutterSync ajusta esse
deslocamento.

Ordem correta de ataque em set:

1. obturador em múltiplo compatível ([[obturador-180]]);
2. [[genlock]] entre câmera e processadora;
3. ShutterSync para a fase fina;
4. só então questionar [[scan-rate]] do painel, que é hardware.

## Por que é específico de fabricante

É recurso de processadora, não padrão da indústria. Outras fabricantes têm
equivalentes com nomes próprios — ao alugar parede, perguntar **qual
processadora** e **se tem ajuste de fase** é tão importante quanto perguntar o
pixel pitch.

## Gotchas

- Ajuste feito para uma câmera não serve automaticamente para outra com
  obturador diferente: em multicâmera, testar cada uma.
- Mudou o frame rate no meio do dia? Reconferir — a fase muda junto.
