---
id: balanceamento-de-fase
title: Balanceamento de fase em set trifásico
type: conceito
zona: universal
aliases: ["balanceamento de fase", "balanceamento de fases", "equilibrar fases", "desequilibrio de fase", "desequilíbrio de fase", "phase balancing", "trifasico", "trifásico"]
tags: [eletrica, trifasico, set, gaffer, distribuicao]
status: draft
confidence: baixa
updated: 2026-07-26
rel:
  requires: [rede-ac, nr-10-eletricidade]
  see_also: [gerador, bitola-de-cabo]
sources:
  - {url: "https://sienge.com.br/blog/o-que-e-nbr-5410/", tier: educacao, ret: 2026-07-26, loc: "NBR 5410 - divisao de circuitos", cit: "a instalação seja dividida em quantos circuitos forem necessários para iluminação, tomadas de uso geral e tomadas de uso específico", nota: "a divisao de circuitos e o que torna o balanceamento possivel"}
---

# Balanceamento de fase em set trifásico


**TL;DR** — em trifásico, o que derruba o quadro raramente é a carga **total**:
é a carga concentrada **numa fase**. Três disjuntores de 20 A comportam **48 A**
distribuídos (regra dos 80% de carga, a mesma de [[bitola-de-cabo]]) e desarmam
com 16 A numa fase só. Distribuir não é capricho — é o que faz o total caber.

## O erro clássico

O plano de luz soma 7,2 kW, o quadro é trifásico, e ninguém confere onde cada
coisa foi ligada. A elétrica puxa da tomada mais perto, e o resultado é uma
fase carregada e duas ociosas.

O sintoma é enganoso: **o total está dentro do limite** e mesmo assim desarma.
Quem não pensa em fase procura defeito no disjuntor.

## Como distribuir

A regra de campo é simples e é o que o cálculo faz: **a maior carga vai sempre
para a fase mais leve**, em ordem decrescente.

Exemplo com 6,6 kW, **em 220 V, FP 0,92** — a corrente muda com a tensão, e
sem ela a tabela não afirma nada (ver [[rede-ac]]):

| fase | cargas | total | corrente @ 220 V | corrente @ 127 V |
|---|---|---|---|---|
| A | 2400 | 2400 W | ~11,9 A | ~20,5 A |
| B | 1200 + 600 + 600 | 2400 W | ~11,9 A | ~20,5 A |
| C | 1200 + 600 | 1800 W | ~8,9 A | ~15,4 A |

Desequilíbrio: **27%** — e aqui ele é **inevitável**, não um erro de
distribuição.

```
python3 tools/calc/eletrica.py --fases 2400,1200,1200,600,600,600
python3 tools/calc/eletrica.py --fases 2400,1200,1200,600,600,600 --tensao 127
```

## Quando o desequilíbrio é inevitável

**Carga não se divide entre fases.** Um fixture de 2,4 kW liga numa fase, e
pronto. Se a maior carga isolada for maior que um terço do total, equilíbrio
perfeito é impossível por aritmética — não por má distribuição.

Saber disso evita duas perdas de tempo reais: redistribuir o irredistribuível,
e culpar a elétrica por um limite do plano de luz. **A saída, quando importa, é
mudar o plano** — dois fixtures menores no lugar de um grande — não insistir na
tomada.

## O neutro

Em sistema equilibrado, as correntes das três fases se cancelam em boa parte no
neutro. Desequilibrado, sobra corrente circulando ali. Por isso fase
desbalanceada não é só risco de desarme: é o neutro trabalhando para o que
talvez não tenha sido dimensionado.

## As premissas por trás destes números

Os valores acima saem de `tools/calc/eletrica.py`, cujas constantes são em boa
parte **premissas de planejamento**, não fatos de norma — a capacidade de
condução é aproximação conservadora, a queda máxima de 4% e a folga de 80% são
prática de dimensionamento, e o fator de potência 0,92 varia por fixture.

O registro de estado de cada constante está em `_meta/constantes-de-calculo.md`.
Serve para chegar na conversa com a ordem de grandeza certa; **não é projeto.**

## Gotchas

- **Conferir onde está ligado, não onde se planejou ligar.** O mapa de fases
  vale o que valer a checagem no quadro — extensão remanejada no meio do dia
  desfaz o balanceamento sem avisar ninguém.
- **Somar potência de placa não é somar consumo real**, mas para balancear é o
  que se tem — e erra para o lado seguro.
- **Gerador tem o mesmo problema.** [[gerador]] trifásico desbalanceado sofre
  igual, e ainda com menos folga que a rede.

## Estado desta nota

`confidence: baixa`: o método guloso (maior carga na fase mais leve) é
**prática de campo** codificada na calculadora deste acervo, não regra de
norma. <!-- verificar: limites de desequilíbrio admissíveis na NBR 5410 e na
prescrição das concessionárias -->
