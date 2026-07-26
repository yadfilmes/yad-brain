---
id: mapa-de-luz
title: Mapa de luz (lighting diagram)
type: documento
zona: universal
aliases: ["mapa de luz", "lighting diagram", "planta de luz", "light plot", "diagrama de iluminacao", "diagrama de iluminação"]
tags: [producao, documento, luz, prep, g-e]
status: draft
confidence: media
updated: 2026-07-26
rel:
  template_for: [gaffer]
  produces: [ordem-do-dia]
  consumes: [diretor-de-fotografia]
  used_in_workflow: [gaffer]
sources:
  - {url: "https://www.abcine.org.br", tier: educacao, ret: 2026-07-26, nota: "prática de documentação de set"}
---

# Mapa de luz (lighting diagram)

**TL;DR** — planta baixa da cena com posição, altura, modificador e potência de
cada fixture, mais a posição de câmera. Serve para montar rápido, para
remontar igual em outro dia, e para orçar equipamento e energia antes de
chegar na locação.

## O que registrar por fixture

| campo | por que importa |
|---|---|
| posição na planta | remontagem e ordem de montagem |
| altura e angulação | o mesmo fixture entrega imagem diferente |
| modificador | softbox, grid, difusão, bandeira |
| potência e intensidade | orçamento elétrico e continuidade |
| temperatura de cor | mistura de fontes é decisão, não acaso |
| circuito / fase | evita descobrir sobrecarga na hora |

## Três usos que justificam o trabalho

1. **Montar rápido.** Equipe monta sem esperar instrução verbal a cada passo.
2. **Continuidade.** Cena que retoma em outro dia precisa da mesma luz — e
   memória não basta.
3. **Orçar antes.** Somando as potências, `tools/calc/eletrica.py` diz quantos
   circuitos e que cabo — antes de descobrir em set que a locação não aguenta.

## Conexões

Nasce do plano do [[diretor-de-fotografia]] e é executado pelo [[gaffer]].
Alimenta o tempo de montagem que a [[ordem-do-dia]] precisa prever.

## Gotchas

- Mapa sem altura e sem angulação é meia informação: a planta baixa não mostra
  a dimensão que mais muda o resultado.
- Registrar o que foi **efetivamente montado**, não só o planejado — set muda,
  e é a versão real que serve à continuidade.
- Fotografar a montagem final complementa o mapa e custa trinta segundos.
