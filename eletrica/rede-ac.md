---
id: rede-ac
title: Rede elétrica AC no Brasil (127 / 220 V)
type: conceito
zona: universal
aliases: ["rede AC", "rede eletrica", "rede elétrica", "tomada", "energia da rede", "127V", "220V", "110V", "mains", "wall power"]
tags: [eletrica, energia, brasil, set, locacao]
status: draft
confidence: baixa
updated: 2026-07-26
rel:
  governed_by: [abnt]
  requires: [bitola-de-cabo]
  alternative_to: [gerador]
  see_also: [nr-10-eletricidade]
sources:
  - {url: "https://sienge.com.br/blog/o-que-e-nbr-5410/", tier: educacao, ret: 2026-07-26, loc: "NBR 5410 - divisao de circuitos", cit: "a instalação seja dividida em quantos circuitos forem necessários para iluminação, tomadas de uso geral e tomadas de uso específico", nota: "principio de divisao de circuitos da NBR 5410"}
  - {url: "https://jornalspassocidades.com.br/voltagem-127-e-220-volts-entenda-as-diferencas-e-padroes-no-brasil", tier: educacao, ret: 2026-07-26, loc: "distribuicao por regiao", cit: "os Estados das regiões Sudeste, Norte e parte do Centro-Oeste utilizam a tensão 127 V, enquanto o Sul e alguns Estados do Nordeste utilizam 220 V", nota: "dado atribuido a ABRADEE; conferir a concessionaria local, nao a regiao"}
---

# Rede elétrica AC no Brasil (127 / 220 V)

**TL;DR** — o Brasil não tem uma tensão, tem duas: **127 V** no Sudeste, Norte
e parte do Centro-Oeste; **220 V** no Sul e parte do Nordeste. A mesma luz puxa
**~1,7× mais corrente em 127 V**, e é essa conta que decide se a locação
aguenta o kit contratado. Frequência 60 Hz em todo o país.

## A conta que muda tudo

Corrente é potência dividida por tensão. Metade da tensão, quase o dobro da
corrente — para a **mesma** luz:

| carga | corrente @ 220 V | corrente @ 127 V |
|---|---|---|
| 1 × 600 W | ~3 A | ~5 A |
| 4 × 600 W | ~12 A | ~21 A |
| 1 × 2400 W | ~12 A | ~21 A |
| 2 × 2400 W | ~24 A | ~41 A |

*(fator de potência 0,92; ver a calculadora para o número exato)*

Consequência prática: um kit que roda folgado num circuito de 20 A em Porto
Alegre estoura o mesmo circuito em São Paulo. **Tensão da locação é pergunta de
orçamento, não de set.**

## Monofásico, bifásico, trifásico

| ligação | o que chega | uso típico em set |
|---|---|---|
| monofásico | uma fase + neutro | residência pequena; kit leve |
| **bifásico 127/220** | duas fases; 127 V fase-neutro, 220 V fase-fase | o arranjo mais comum em locação urbana |
| trifásico | três fases + neutro | estúdio, galpão, evento — e o único que dilui carga alta |

Em trifásico, distribuir a carga entre as fases não é refinamento: fase
desbalanceada sobrecarrega o neutro e derruba o quadro com o total ainda
dentro do limite. Ver [[balanceamento-de-fase]].

## Dimensionar antes de fechar

```
python3 tools/calc/eletrica.py --potencia 14400 --tensao 127
python3 tools/calc/eletrica.py --potencia 14400 --trifasico
```

Esses dois devolvem corrente, disjuntor e número de circuitos. A
[[bitola-de-cabo]] só entra quando há distância — o encadeamento completo
exige `--distancia`:

```
python3 tools/calc/eletrica.py --potencia 14400 --tensao 127 --distancia 40
```

É aí que aparece o problema que ninguém quer descobrir no dia.

## As premissas por trás destes números

Os valores acima saem de `tools/calc/eletrica.py`, cujas constantes são em boa
parte **premissas de planejamento**, não fatos de norma — a capacidade de
condução é aproximação conservadora, a queda máxima de 4% e a folga de 80% são
prática de dimensionamento, e o fator de potência 0,92 varia por fixture.

O registro de estado de cada constante está em `_meta/constantes-de-calculo.md`.
Serve para chegar na conversa com a ordem de grandeza certa; **não é projeto.**

## Gotchas

- **Bivolt no fixture não resolve o cabo.** Luminária bivolt aceita as duas
  tensões, mas em 127 V puxa a corrente maior — o cabo e o disjuntor têm que
  ser dimensionados para essa, não para a menor.
- **Região não é garantia.** A divisão 127/220 é tendência regional, não regra:
  há bolsões dos dois padrões dentro do mesmo estado, e prédio novo em área de
  127 V às vezes chega em 220 V. Perguntar à produção da locação **e conferir
  no quadro**, não deduzir pelo CEP.
- **Tomada disponível ≠ circuito disponível.** Várias tomadas do mesmo cômodo
  costumam estar no mesmo disjuntor. O que limita é o circuito, não o número
  de bocas.
- **Instalação antiga com carga de set é risco real**, não inconveniência.
  Verificação prévia por profissional habilitado antes do dia de gravação —
  ver [[nr-10-eletricidade]].
