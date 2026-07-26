---
id: hmi
title: HMI — descarga de haleto metálico
type: conceito
zona: universal
risco: seguranca
jurisdicao: BR
aliases: [HMI, "haleto metalico", "haleto metálico", "metal halide", "arco voltaico", "lampada de descarga", "lâmpada de descarga", "daylight discharge"]
tags: [luz, hmi, descarga, externa, flicker, seguranca]
status: draft
confidence: baixa
updated: 2026-07-26
rel:
  requires: [rede-ac, nr-10-eletricidade]
  competes_with: [evoke-2400b]
  enables_technique: [obturador-180]
  see_also: [gerador, temperatura-de-cor, cri-tlci-ssi]
sources:
  - {url: "https://look.ams-osram.com/m/2bde01adc88df0fe/original/HMI-Family-PIB-US-version-EN.pdf", tier: oficial, ret: 2026-07-26, loc: "HMI Metal Halide Lamp Family - product information bulletin", nota: "folha da familia HMI da OSRAM. NAO foi aberta nesta sessao - egresso bloqueado, ver _meta/qa/blocked.md B1. Entra como ancora de procedencia oficial exigida pelo gate G4, e e a primeira fonte a conferir quando houver rede"}
  - {url: "https://www.tvtechnology.com/opinions/light-sources-101-hmis", tier: educacao, ret: 2026-07-26, loc: "Light Sources 101 - HMIs", cit: "HMIs put out a high amount of UV radiation and, therefore, require a UV filtering glass to protect people from the harmful rays", nota: "por que o vidro UV nao e acessorio - e barreira de protecao"}
  - {url: "http://www.lightlineelectronics.com/faq_hmi.html", tier: educacao, ret: 2026-07-26, loc: "HMI & Ballast FAQs", cit: "Electronic ballasts transform the sine wave line voltage into square wave, so the arc extinguishes just for a very short moment during zero-crossing and stays constant during the rest of the period", nota: "mecanismo do reator eletronico - a onda quadrada e o que reduz o flicker"}
  - {url: "https://donklipstein.com/shortarc.html", tier: educacao, ret: 2026-07-26, loc: "Short Arc / Compact Source Lamps", cit: "Explosions can be dangerous since they can result in red-hot (or hotter) pieces of glasslike quartz being shot out in all directions, possibly with considerable force", nota: "risco de ruptura do bulbo sob alta pressao"}
---

# HMI — descarga de haleto metálico

> ⚠️ **Conteúdo de segurança.** UV, alta pressão e alta tensão de partida.
> Esta nota é referência de **planejamento** e **não substitui** treinamento,
> procedimento do fabricante nem profissional habilitado. Nota com
> `risco: seguranca` exige revisão humana integral antes de sair de `draft`.

**TL;DR** — luz de arco elétrico com temperatura de cor de luz do dia, que
ainda ganha do LED em **potência bruta por watt consumido** e em alcance a
distância. O preço vem em três moedas: **flicker** que depende do reator,
**risco** (UV, mercúrio, alta pressão) e **inércia** — não liga e desliga como
LED.

## O que define

| aspecto | comportamento |
|---|---|
| natureza | arco elétrico em vapor de mercúrio e haletos metálicos |
| temperatura de cor | luz do dia (nominal ~5600 K), com deriva ao longo da vida da lâmpada |
| eficiência | alta em lúmen por watt — a razão de continuar existindo |
| partida | tensão alta; carga indutiva pesada — ver [[gerador]] |
| religação | **hot restrike**: apagou quente, precisa esfriar antes de reacender |

## Reator: onde mora o flicker

Duas famílias, e a diferença aparece na câmera, não no olho:

| reator | forma de onda | consequência |
|---|---|---|
| **magnético** | senoidal | brilho pulsa suavemente — flicker em várias cadências |
| **eletrônico ("flicker-free")** | **quadrada** | o arco só se apaga por um instante no cruzamento de zero |

O mecanismo, na fonte: o reator eletrônico *"transforma a tensão senoidal da
rede em onda quadrada, de modo que o arco se extingue apenas por um instante
muito curto no cruzamento de zero e permanece constante no resto do período"*.

**"Flicker-free" não é absoluto.** Ao longo da vida da lâmpada, a distância
entre eletrodos aumenta e o arco fica apagado por mais tempo a cada cruzamento
— um HMI velho volta a piscar num reator que era estável.

<!-- verificar: os limites de cadência por modo de reator (silencioso x
     flicker-free) e a fórmula de ângulo de obturador seguro em rede de 60 Hz.
     As fontes consultadas tratam de rede de 50 Hz, e o Brasil é 60 Hz — o
     número NÃO se transporta. -->

## HMI e LED: a comparação que importa em orçamento

| critério | HMI | LED de alta potência |
|---|---|---|
| potência bruta a distância | **ainda ganha** | melhorou muito, ainda não empata no topo |
| consumo elétrico | alto, e com pico de partida | menor, entrada suave |
| controle de intensidade | limitado; dimerizar altera a cor | contínuo, sem alterar a cor |
| liga/desliga | inércia; hot restrike | instantâneo |
| risco | UV, mercúrio, alta pressão | elétrico comum |
| cor | luz do dia, com deriva | ajustável, estável |

Onde LED já resolve, ele resolve com menos risco e menos gerador. HMI segue
insubstituível quando é preciso **jogar luz de dia longe**, contra sol, através
de janela ou difusão grande.

## Segurança — o que não se improvisa

- **O vidro UV é barreira, não acessório.** A fonte é explícita: HMI emite UV
  em quantidade alta e exige vidro filtrante para proteger as pessoas.
  Fixtures modernos trazem chave de segurança que impede operar com o vidro
  aberto — **contornar essa chave é exposição direta**.
- **Ruptura de bulbo é risco físico real.** Lâmpada de arco opera sob pressão
  de muitas atmosferas; a ruptura pode lançar fragmentos de quartzo
  incandescente com força.
- **Mercúrio.** Bulbo quebrado libera mercúrio — descarte e limpeza têm
  procedimento próprio, e não é varrer.
- **Hot restrike.** Não insistir em reacender quente; o procedimento é do
  fabricante.

## Gotchas

- **Dimerizar HMI não é como dimerizar LED.** Reduzir potência altera a
  temperatura de cor e pode instabilizar o arco. Controle de intensidade em HMI
  se faz com difusão, distância e grade — não com o botão.
- **Lâmpada tem horas, e a cor deriva.** Locar HMI sem perguntar as horas de
  lâmpada é aceitar cor imprevisível — e cor derivada não casa com LED na
  mesma cena.
- **Partida indutiva estoura o gerador do orçamento.** Ver [[gerador]]: um HMI
  pode mover a locação em uma faixa inteira de kVA.

## Estado desta nota

`confidence: baixa`, e a razão precisa estar explícita numa nota de segurança:

| fonte | tier | aberta na origem? |
|---|---|---|
| OSRAM — HMI Family (PIB) | `oficial` | **não** — egresso bloqueado (`_meta/qa/blocked.md`, B1) |
| TV Technology · Lightline · Klipstein | `educacao` | não; transcritas do que a busca devolveu literalmente |

Ou seja: **as três afirmações com `cit` vêm de fontes secundárias**, e a única
fonte oficial entrou como âncora de procedência — exigida pelo gate G4 — sem
ter sido lida. Para conteúdo técnico comum isso seria uma nota fraca; para
`risco: seguranca` é **insuficiente por princípio**, não por formalidade.

O que está escrito aqui sobre UV, mercúrio e ruptura de bulbo é o suficiente
para **não improvisar** — não é suficiente para servir de procedimento.

**O que destrava:** abrir a documentação da OSRAM e do fabricante do fixture
sobre manuseio de lâmpada e reator, e revisão por pessoa qualificada
registrada em `revisor_humano`.
