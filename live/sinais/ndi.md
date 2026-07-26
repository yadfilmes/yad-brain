---
id: ndi
title: NDI (Network Device Interface)
type: interface
zona: universal
aliases: [NDI, "NDI 5", "NDI 6", "Network Device Interface"]
tags: [live, sinal, ip, rede, streaming]
status: draft
confidence: media
updated: 2026-07-26
rel:
  made_by: [vizrt]
  alternative_to: [sdi]
  requires: [rede-gigabit]
  interoperates_with: [tally]
  distinct_from: [genlock]
sources:
  - {url: "https://ndi.video/tech/", tier: oficial, ret: 2026-07-26, nota: "especificação e variantes"}
---

# NDI (Network Device Interface)

**TL;DR** — vídeo profissional trafegando sobre rede Ethernet comum, com
descoberta automática de fontes. Troca cabo coaxial dedicado por infraestrutura
de rede: uma fonte, muitos destinos, sem matriz de roteamento.

## Variantes

| variante | compressão | uso |
|---|---|---|
| **NDI** (full) | leve, alta qualidade | produção em rede local dedicada |
| **NDI HX** | mais comprimida | câmeras PTZ, links de banda limitada |

## O que ele resolve que o SDI não resolve

- **Uma fonte, N destinos** sem matriz: qualquer máquina na rede assina a fonte.
- **Descoberta automática**: aparece na lista, não precisa saber onde está.
- **Cabo de rede** já instalado no prédio, em vez de puxar coaxial novo.
- **Bidirecional**: retorno, tally e controle no mesmo cabo.

## O que ele cobra em troca

| custo | detalhe |
|---|---|
| latência | maior que SDI — importa em ao vivo com áudio sincronizado |
| rede | **dedicada**, gigabit no mínimo, com switch gerenciado |
| compressão | mesmo "leve" é compressão; SDI não comprime |
| sincronia | não substitui [[genlock]] onde ele é exigido |

## Regra prática

Rede compartilhada com internet do escritório **não** é infraestrutura de NDI.
O tráfego de vídeo satura o switch e o problema aparece exatamente no ar. Se o
job depende de NDI, a rede entra no orçamento como equipamento.

## Conexões

Convive com [[sdi]] em quase toda produção real: SDI onde a latência e a
confiabilidade mandam, NDI onde a flexibilidade e a distância compensam.
