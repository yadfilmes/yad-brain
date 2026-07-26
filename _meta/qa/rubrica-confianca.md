# Rubrica de confiança

O item 11 da R-N cobra que o campo `confidence` seja "coerente com a rubrica de
confiança (fontes × corroboração)". **Essa rubrica não existia.** O item era
inganhável por construção: o revisor recebe instrução adversarial ("na dúvida,
reprove") e não tinha documento contra o qual conferir. Somado ao item 3, que
também era inauditável, o máximo efetivo da R-N era **84 pontos num corte de
92** — nenhuma nota podia passar, por melhor que fosse.

Este arquivo fecha o item 11. O corte 92 e os pesos seguem intactos: a decisão
do dono foi **destravar, não recalibrar**.

---

## O que `confidence` responde

Não é "quão boa é a nota". É uma pergunta só:

> **Se esta afirmação estiver errada, quão surpreso eu ficaria?**

`alta` = ficaria muito surpreso, porque duas fontes independentes localizadas
dizem o mesmo. `baixa` = não ficaria, porque é fonte única, ou não conferida, ou
o tier não sustenta o tipo de afirmação.

`confidence` qualifica **a nota como um todo** — a afirmação mais frágil que ela
carrega. Uma nota com nove specs corroboradas e uma spec de fonte única é
`media`, não `alta`. Confiança não faz média; ela segue o elo mais fraco.

---

## A tabela

Ler de cima para baixo e **parar na primeira linha que se aplica**.

| se… | `confidence` |
|---|---|
| há `<!-- verificar -->` no corpo | `baixa` |
| há conflito de fontes registrado e **não resolvido** na nota | `baixa` |
| a nota faz afirmação numérica e **não tem** fonte `oficial` nem `lab` | `baixa` |
| fonte única (uma organização só), qualquer tier | `baixa` |
| ≥2 organizações independentes, mas **nenhuma** `oficial` nem `lab` | `media` |
| ≥2 organizações independentes, ≥1 `oficial`/`lab`, mas falta `loc` em alguma delas | `media` |
| ≥1 fonte `oficial`/`lab` com `loc`, **sem** corroboração independente | `media` |
| ≥2 organizações independentes, ≥1 `oficial`/`lab`, **todas** com `loc`, sem lacuna e sem conflito aberto | `alta` |

### O que conta como "organização independente"

Duas páginas do mesmo fabricante são **uma** fonte. O manual da Sony e a página
de produto da Sony não se corroboram — repetem-se.

| combinação | independentes? |
|---|---|
| `pro.sony` + `sony.com` | **não** — mesma organização |
| Sony + CineD (lab) | sim |
| CineD + Wikipedia | sim |
| dois threads do mesmo fórum | **não** para efeito de corroboração |
| fórum do Premiere + fórum da Blackmagic | sim |

Corroboração é **a mesma afirmação em fontes que não se copiam**. Dois blogs
que citam o mesmo press release são uma fonte com dois endereços.

---

## Onde a máquina entra — e onde ela para

O `validate.py` cobra o **piso** desta rubrica: conta domínios distintos, exige
`loc` nas fontes `oficial`/`lab` e barra `alta` sem corroboração. Como todo o
resto do CI: **avisa em `draft`, reprova em `reviewed`.**

O que a máquina **não** consegue e continua sendo julgamento do revisor:

1. **Se as fontes de fato dizem a mesma coisa.** Duas URLs distintas podem
   corroborar, contradizer ou tratar de coisas diferentes. O script conta
   endereços; quem lê é que sabe se houve corroboração.
2. **Independência real por trás do domínio.** `nanlux.com` e `nanliteus.com`
   são a mesma empresa; `help.codex.online` é ARRI. O contador vê duas
   organizações e erra para o lado permissivo.
3. **Se o tier sustenta o tipo de afirmação.** Número pede `oficial`/`lab`;
   prática pede `comunidade`/`educacao`/`campo-proprio`. Há aviso mecânico
   para o caso grosseiro, não para o sutil.

Isto está escrito aqui de propósito. Item de rubrica que finge ser mecânico
quando é julgamento é o defeito que este arquivo existe para consertar —
repeti-lo em nome da conveniência seria trocar um item inauditável por um item
falsamente auditável.

---

## Como o revisor pontua o item 11

Binário, como todo item da R-N:

- **Passa** quando o valor de `confidence` é o que a tabela produz para as
  fontes daquela nota, **ou mais conservador** (a nota declara `media` onde
  caberia `alta`).
- **Reprova** quando é mais otimista que a tabela — inclusive por um degrau.

Errar para baixo não reprova. Uma nota que se declara menos confiável do que
poderia continua sendo honesta com quem consulta; o inverso, não.
