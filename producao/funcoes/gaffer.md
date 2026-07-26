---
id: gaffer
title: Gaffer (chefe de elétrica)
type: funcao
zona: universal
aliases: [gaffer, "chefe de eletrica", "chefe de elétrica", "chefe de eletricistas", "chief lighting technician"]
tags: [funcao, luz, eletrica, set, g-e]
status: draft
confidence: media
updated: 2026-07-26
rel:
  reports_to: [diretor-de-fotografia]
  used_in_workflow: [mapa-de-luz]
  requires: [nr-35-trabalho-em-altura]
  operated_by_role: []
  see_also: [temperatura-de-cor, cri-tlci-ssi]
sources:
  - {url: "https://www.abcine.org.br", tier: educacao, ret: 2026-07-26, nota: "nomenclatura de funções no Brasil"}
---

# Gaffer (chefe de elétrica)

**TL;DR** — chefe do departamento de elétrica: transforma a intenção do
diretor de fotografia em plano executável de luz, e responde pela equipe, pelo
equipamento e pela **segurança elétrica** do set. Não é quem escolhe o visual;
é quem faz o visual existir com segurança e dentro do tempo.

## O que faz, por fase

| fase | trabalho |
|---|---|
| prep | lista de equipamento, mapa de luz, checagem de energia da locação |
| montagem | distribui equipe, define pontos, supervisiona rigging e cabos |
| gravação | executa mudanças de luz entre planos, mantém continuidade |
| desmontagem | segurança na retirada, conferência de material |

## Onde a responsabilidade é dele, não do DoP

- **Carga elétrica**: se a locação aguenta o que foi contratado.
- **Segurança**: cabo no chão, aterramento, trabalho em altura
  ([[nr-35-trabalho-em-altura]]), carga suspensa.
- **Equipe**: quantos eletricistas, quem faz o quê.
- **Tempo**: quanto demora cada mudança de luz — informação que o assistente
  de direção precisa para montar a ordem do dia.

## Nomenclatura no Brasil

A estrutura americana (gaffer + best boy + grips) não mapeia exatamente na
brasileira, onde se fala **chefe de elétrica**, **eletricista** e
**maquinista** — e a divisão entre elétrica e maquinaria varia por região e
por produtora. Em set com equipe mista, vale alinhar os termos na primeira
reunião: é fonte real de mal-entendido.

## Ferramentas do acervo que apoiam a função

- `tools/calc/eletrica.py` — corrente, circuitos, bitola de cabo, gerador
- `tools/calc/led_wall.py` — carga e peso de parede de LED

## Conexões

Executa o que o diretor de fotografia desenha; entrega para o operador de
câmera uma cena já exposta. Decide com base em [[temperatura-de-cor]] e
[[cri-tlci-ssi]] quando há mistura de fontes.
