---
id: bitola-de-cabo
title: Bitola de cabo — condução e queda de tensão
type: conceito
zona: universal
aliases: ["bitola", "bitola de cabo", "secao do cabo", "seção do cabo", "mm2", "mm²", "cabo de energia", "extensao", "extensão", "cable gauge", "AWG"]
tags: [eletrica, cabo, dimensionamento, set, orcamento]
status: draft
confidence: baixa
updated: 2026-07-26
rel:
  governed_by: [abnt]
  requires: [rede-ac, nr-10-eletricidade]
  see_also: [gerador]
sources:
  - {url: "https://sienge.com.br/blog/o-que-e-nbr-5410/", tier: educacao, ret: 2026-07-26, loc: "NBR 5410 - objeto da norma", cit: "estabelece as condições mínimas para garantir a segurança em instalações elétricas de baixa tensão, orientando o projeto, a execução, a verificação e a manutenção", nota: "escopo da NBR 5410, que e a norma por tras do dimensionamento"}
---

# Bitola de cabo — condução e queda de tensão

**TL;DR** — bitola de cabo tem **duas** restrições, não uma. O cabo precisa
conduzir a corrente **sem esquentar** e entregar tensão suficiente **no fim da
tirada**. Em tirada longa é quase sempre a **segunda** que manda — e é a que
todo mundo esquece.

## As duas restrições, e por que a segunda surpreende

| restrição | o que acontece se falhar |
|---|---|
| **condução** | cabo aquece, isolação degrada, risco de incêndio |
| **queda de tensão** | a luz acende, mas chega menos tensão — fixture entrega menos, fonte chaveada reclama, motor perde torque |

A queda não dá sinal óbvio: nada esquenta, nada desarma. O fixture só rende
menos que o esperado, e ninguém liga o fato ao cabo.

## O exemplo que resolve a discussão

Carga de **5 kW em 220 V** (≈ 24,7 A), variando só a distância:

| tirada | bitola mínima |
|---|---|
| 10 m | 4 mm² |
| 30 m | 4 mm² |
| **60 m** | **10 mm²** |
| 100 m | 16 mm² |

**Condução sozinha pediria 4 mm² nos quatro casos.** É a queda de tensão que
força 10 mm² aos 60 m e 16 mm² aos 100 m — **dois e três degraus** na escala
comercial (4 → 6 → 10 → 16). Chegar com 4 mm² e uma tirada de 60 m não estoura disjuntor: só entrega
menos luz do que o orçamento previu.

Cada linha sai de um comando — trocando só a distância:

```
python3 tools/calc/eletrica.py --potencia 5000 --distancia 10
python3 tools/calc/eletrica.py --potencia 5000 --distancia 30
python3 tools/calc/eletrica.py --potencia 5000 --distancia 60
python3 tools/calc/eletrica.py --potencia 5000 --distancia 100
```

## O efeito da tensão, de novo

A mesma carga de 5 kW, mesma tirada de 60 m:

| tensão | corrente | bitola |
|---|---|---|
| 220 V | 24,7 A | 10 mm² |
| **127 V** | **42,8 A** | **25 mm²** |

Metade da tensão, quase o dobro da corrente — e **duas vezes e meia** o cobre.
Ver [[rede-ac]]: a tensão da locação muda o custo do cabo, não só o do
disjuntor.

## Regras que o cálculo aplica

- **Disjuntor nunca acima de 80% de carga.** Circuito no limite desarma com
  variação normal.
- **Queda máxima de 4%** em circuito terminal — limite prático de projeto.
- **Ida e volta contam.** A corrente percorre o dobro da distância física; a
  tirada de 60 m são 120 m de cobre.

## As premissas por trás destes números

Os valores acima saem de `tools/calc/eletrica.py`, cujas constantes são em boa
parte **premissas de planejamento**, não fatos de norma — a capacidade de
condução é aproximação conservadora, a queda máxima de 4% e a folga de 80% são
prática de dimensionamento, e o fator de potência 0,92 varia por fixture.

O registro de estado de cada constante está em `_meta/constantes-de-calculo.md`.
Serve para chegar na conversa com a ordem de grandeza certa; **não é projeto.**

## Gotchas

- **Cabo enrolado no carretel conduz menos.** Enrolado, ele não dissipa calor;
  a capacidade cai. Desenrolar antes de carregar, sempre.
- **Emenda e conector ruim viram ponto quente.** A bitola certa não salva uma
  conexão frouxa — o aquecimento se concentra ali.
- **AWG e mm² não são a mesma escala.** Cabo importado vem em AWG; converter
  antes de comparar, e desconfiar de equivalência arredondada para baixo.
- **Somar extensões soma distância, não capacidade.** Três de 20 m em série são
  uma tirada de 60 m, com a queda dos 60 m — e o cálculo é o da tirada inteira.
