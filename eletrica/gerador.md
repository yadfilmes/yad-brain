---
id: gerador
title: Gerador de set — dimensionamento em kVA
type: conceito
zona: universal
aliases: [gerador, "grupo gerador", "gerador de set", genset, "generator", kVA, "grupo motor-gerador"]
tags: [eletrica, energia, externa, orcamento, set]
status: draft
confidence: baixa
updated: 2026-07-26
rel:
  alternative_to: [rede-ac]
  requires: [bitola-de-cabo, nr-10-eletricidade]
  see_also: [balanceamento-de-fase]
sources:
  - {url: "https://sienge.com.br/blog/o-que-e-nbr-5410/", tier: educacao, ret: 2026-07-26, loc: "NBR 5410 - objeto da norma", cit: "estabelece as condições mínimas para garantir a segurança em instalações elétricas de baixa tensão, orientando o projeto, a execução, a verificação e a manutenção", nota: "a instalacao a jusante do gerador segue a mesma norma"}
---

# Gerador de set — dimensionamento em kVA

> ⚠️ Números de **planejamento e orçamento**. Não é projeto elétrico.
> Instalação, aterramento e laudo exigem profissional habilitado (CREA/CFT),
> sob [[nr-10-eletricidade]] e ABNT NBR 5410.

**TL;DR** — gerador se contrata em **kVA**, não em kW, e os dois não são a
mesma coisa: kVA = kW ÷ fator de potência. Some margem, e some **muito mais**
se houver carga indutiva ([[hmi]] com reator, motor) — o arranque puxa
bem acima do regime.

## kW não é kVA

| grandeza | o que é |
|---|---|
| **kW** | potência que vira luz e calor — o que a luminária consome |
| **kVA** | potência aparente que o gerador precisa entregar |
| **fator de potência** | a razão entre as duas; ~0,92 em LED com fonte chaveada |

Contratar gerador pelo número de kW do kit é subdimensionar por volta de 8%
antes de qualquer margem — e margem é o que separa "acendeu" de "acendeu e
segurou o dia".

## A conta, com carga de 14,4 kW

| cenário | kVA útil | **kVA a contratar** | margem |
|---|---|---|---|
| só LED (sem partida pesada) | 15,7 | **19,6** | 25% |
| com carga indutiva ([[hmi]], motor) | 15,7 | **27,4** | 75% |

A diferença entre 19,6 e 27,4 kVA é uma faixa inteira de locação — e é decidida
por **um** HMI no plano de luz. Reproduzível:

```
python3 tools/calc/eletrica.py --gerador 14400
python3 tools/calc/eletrica.py --gerador 14400 --partida
```

## Por que a carga indutiva custa tanto

LED com fonte chaveada entra suave. HMI com reator eletromagnético e motor
puxam **corrente de arranque** muito acima do regime, por instantes. O gerador
tem que aguentar esse pico sem afundar a tensão — e afundar significa apagar o
resto do set junto.

Regra de campo: **acender em escada, não tudo de uma vez.** Não substitui a
margem, mas evita o pico somado.

## Além do kVA

- **Combustível pela jornada, não pela potência.** Consumo depende de carga
  média e de horas — diária de 12 h com carga baixa e diária de 6 h no talo
  são orçamentos diferentes.
- **Ruído é decisão de direção, não de elétrica.** Gerador silenciado custa
  mais e ainda assim tem distância mínima; captação de som direto define onde
  ele pode ficar, e isso muda a [[bitola-de-cabo]] pela distância.
- **Aterramento é item, não detalhe.** Gerador em externa exige aterramento
  próprio, verificado por quem é habilitado.
- **Distância até o set entra no cabo.** Gerador longe por causa do ruído é
  tirada longa — ver a tabela de queda de tensão em [[bitola-de-cabo]].

## Estado desta nota

`confidence: baixa`: os valores de margem (25% e +50% para partida) são
**parâmetros de planejamento da calculadora deste acervo**, escolhidos como
conservadores de campo — não saem de norma nem de folha de dados de fabricante.
<!-- verificar: confirmar margens típicas de partida contra folha de dados de
     locadora de gerador e contra a curva de arranque de HMI com reator -->
