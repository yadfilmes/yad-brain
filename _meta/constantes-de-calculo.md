# Constantes de cálculo — o que é fonte e o que é premissa

O revisor do lote de elétrica encontrou o defeito que este arquivo existe para
consertar, e vale citá-lo inteiro porque é a lição:

> "Reproduzível pelo comando" foi confundido com "rastreável à fonte". A
> reprodutibilidade **é real** — mas os números saem de constantes que **não
> têm fonte nenhuma**. **Número reproduzido de constante órfã continua órfão.**

É a lei de Goodhart pela quarta vez neste projeto: otimizou-se o CI, depois a
contagem de fontes, depois a fidelidade da citação, e agora a
**reprodutibilidade**. Cada rodada o alvo fica mais sofisticado, e cada rodada
ele continua sendo alvo em vez de instrumento.

**A regra que sai daqui:** toda constante de calculadora é ou **fonte
verificada** ou **premissa declarada**. Não existe terceira categoria, e
premissa não vira fato por ser reproduzível.

---

## Estado de cada constante

Notação: **F** = fonte verificada (com `cit`) · **P** = premissa de
planejamento, escolhida por engenharia conservadora · **N** = de norma, mas a
norma não foi aberta.

### `tools/calc/eletrica.py`

| constante | valor | estado | o que destrava |
|---|---|---|---|
| `RHO_COBRE` | 0,0225 Ω·mm²/m | **P** | valor prático de projeto, acima da resistividade a 20 °C. Conferir contra tabela de fabricante de cabo |
| `CAPACIDADE_A` | tabela por bitola | **N** | é aproximação de cobre PVC, 2 condutores, ao ar livre. A tabela real da NBR 5410 depende de método de instalação, agrupamento e temperatura — e **a norma é paga**, ver [[abnt]] |
| `QUEDA_MAX_PCT` | 4,0 % | **N** | limite usual de circuito terminal; confirmar o valor e o escopo na NBR 5410 |
| `FOLGA_DISJUNTOR` | 0,8 | **P** | prática de dimensionamento, não prescrição literal de norma |
| `fp` (padrão) | 0,92 | **P** | típico de LED com fonte chaveada. **Varia por fixture** — o valor real está na folha de dados |
| `margem` gerador | 0,25 | **P** | margem de planejamento; locadora costuma trabalhar com faixa parecida |
| `partida` gerador | +0,50 | **P** | reserva para carga indutiva. Não sai de curva de arranque medida |

### O que isso significa para quem consulta

Número que sai desta calculadora serve para **chegar na conversa com ordem de
grandeza certa** — dimensionar kit, fechar orçamento, saber se a locação
aguenta. **Não serve como projeto**, e a distância entre as duas coisas é
exatamente a coluna "estado" acima.

Uma nota que publica esses números precisa dizer isso. Publicar `10 mm²` sem
dizer que a capacidade de condução por trás é aproximação conservadora é
apresentar premissa como fato.

---

## Como uma constante muda de estado

1. Abrir a fonte (norma, folha de dados, ensaio) — hoje bloqueado, ver
   `_meta/qa/blocked.md`, B1.
2. Transcrever o trecho em `cit`, na nota que usa a constante.
3. Mudar o estado aqui para **F**, com a fonte ao lado.
4. Só então a nota pode tratar o valor como fato.

**Enquanto o estado for P ou N, a nota que usa o número declara a premissa** —
em tabela, não em prosa perdida no fim.

---

## Por que isto não é `_meta/qa/blocked.md`

`blocked.md` registra o que **não se pode fazer** por impedimento externo.
Este arquivo registra o que **se está fazendo com premissa declarada** — e
continua sendo legítimo fazer. São coisas diferentes: uma é fila de espera, a
outra é contrato com quem lê.
