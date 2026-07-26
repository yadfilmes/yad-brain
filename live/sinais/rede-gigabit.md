---
id: rede-gigabit
title: Rede para vídeo sobre IP
type: conceito
zona: universal
aliases: ["rede gigabit", "switch gerenciado", "rede dedicada", "infraestrutura de rede"]
tags: [live, rede, ip, ndi, infraestrutura]
status: draft
confidence: media
updated: 2026-07-26
rel:
  see_also: [ndi, sdi]
sources:
  - {url: "https://ndi.video/tech/", tier: oficial, ret: 2026-07-26, nota: "requisitos de rede"}
---

# Rede para vídeo sobre IP

**TL;DR** — vídeo sobre IP exige rede **dedicada**: gigabit no mínimo, switch
gerenciado, e nada de compartilhar com a internet do escritório. A rede deixa
de ser encanamento e passa a ser equipamento de produção — com custo, teste e
responsável.

## Requisitos mínimos

| item | por quê |
|---|---|
| gigabit por porta | um fluxo [[ndi]] full consome banda real |
| switch **gerenciado** | precisa de IGMP snooping para multicast não inundar a rede |
| rede dedicada | tráfego de escritório e vídeo não convivem sob carga |
| cabo categoria adequada | Cat5e no limite; Cat6 é a escolha segura |

## O erro que derruba transmissão

Ligar as fontes num switch comum, não gerenciado. Sem IGMP snooping, tráfego
multicast é replicado para **todas** as portas: a rede satura, e o sintoma
aparece como travamento aleatório de imagem — geralmente no ar, porque é
quando a carga é máxima.

## Regra prática

Se o job depende de IP, a rede entra no orçamento como equipamento, com teste
de carga antes do dia. Rede improvisada é a causa mais comum de falha em
produção NDI.
