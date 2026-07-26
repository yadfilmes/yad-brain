---
id: temperatura-de-cor
title: Temperatura de cor (CCT) e tint
type: conceito
zona: universal
aliases: [CCT, "temperatura de cor", "correlated color temperature", Kelvin, tint, "green-magenta"]
tags: [luz, cor, fotometria, balanco-de-branco]
status: draft
confidence: alta
updated: 2026-07-26
rel:
  see_also: [cri-tlci-ssi]
  distinct_from: []
sources:
  - {url: "https://www.arri.com/en/lighting", tier: oficial, ret: 2026-07-26, nota: "faixas de CCT dos fixtures"}
---

# Temperatura de cor (CCT) e tint

**TL;DR** — CCT, em Kelvin, descreve se a luz é "quente" (3200 K, tungstênio)
ou "fria" (5600 K, luz do dia). Mas **um eixo não basta**: o tint (verde ↔
magenta) é a segunda dimensão, e é onde mora a maior parte dos problemas de
cor com LED barato e com lâmpada fluorescente de locação.

## Referências que se usa de cabeça

| fonte | CCT aproximada |
|---|---|
| vela | 1900 K |
| tungstênio de cinema | 3200 K |
| nascer/pôr do sol | 2000–3000 K |
| luz do dia padrão | 5600 K |
| céu nublado / sombra | 6500–7500 K |

## Por que o tint importa tanto quanto o Kelvin

Duas luzes podem marcar 5600 K e parecer diferentes na câmera: uma puxando
verde, outra magenta. A câmera balanceia o eixo Kelvin com facilidade; o
desvio de verde exige correção separada (no fixture, na gelatina ou na pós) e
é o que faz pele parecer doente.

Fluorescente de escritório e LED de baixa qualidade são os suspeitos de sempre
— por isso a medição em set usa colorímetro que reporta **os dois eixos**, não
só o Kelvin.

## Misturar temperaturas é escolha, não erro

Deixar a janela em 5600 K enquanto a luz interna fica em 3200 K produz o
contraste quente/frio que boa parte da publicidade usa de propósito. O erro
não é misturar: é misturar **sem decidir** e descobrir na pós.

## Conexões

Ver [[cri-tlci-ssi]] para a outra metade da qualidade de cor: um fixture pode
acertar o Kelvin e ainda assim reproduzir mal certas cores.

## Gotchas

- LED bicolor costuma ter o melhor rendimento no **meio** da faixa, não nos
  extremos: 3200 K puro num bicolor às vezes rende pior que num fixture
  dedicado a tungstênio.
- "5600 K" no visor do fixture é valor nominal; medir em set quando a cor
  importa.
