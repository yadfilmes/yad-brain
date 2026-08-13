# Lusion — teardown técnico e receita de motion

> Documento de pesquisa. Mora em `_meta/` de propósito: não é nota do acervo
> audiovisual, não entra no grafo e o `validate.py` não o lê. É referência de
> craft para o site/portfólio da casa.

**Data:** 2026-08-13 · **Alvo:** [lusion.co](https://lusion.co) (estúdio de
real-time/mograph, Londres)

---

## Aviso de método — leia antes de confiar em qualquer número

**Não consegui abrir o `lusion.co`.** A sessão roda atrás de um proxy de egresso
que só libera registries de pacote; o `CONNECT` para `lusion.co:443` voltou 403,
e o mesmo aconteceu com `tympanus.net` (Codrops) e `webgpu.com`. **Não existe
ferramenta Firecrawl instalada** nesta sessão (nem MCP, nem skill, nem binário) —
o `/firecrawl` do pedido não resolve para nada aqui. Portanto **nenhuma linha
abaixo vem de leitura do bundle JS do site.**

O que sustenta o documento:

| Tier | O que sustenta | De onde veio |
|---|---|---|
| `oficial` | O que o próprio estúdio declarou | Case study do Lusion na Awwwards; perfil na Communication Arts; post do estúdio no X |
| `educacao` | Técnica de terceiros | Tutorial do Codrops sobre os *curly tubes*; docs do Three.js; artigos de damping/spring |
| **`inferencia`** | **Minha leitura de engenharia** | **Não é fonte. É hipótese de quem já montou coisa parecida.** Está marcado em cada ocorrência. |

<!-- verificar: reabrir lusion.co numa sessão com rede liberada e ler o bundle
     de verdade (nome dos chunks, presença de three.module.js, GSAP, Lenis,
     WebGPURenderer, workers, .ktx2/.basis, VAT em .png/.exr). Tudo que estiver
     marcado `inferencia` neste documento vira verificado ou cai. -->

---

## TL;DR

O Lusion não ganha por causa do shader. Ganha por causa da **camada de estado
contínuo entre o input e o render** — nada no site salta, tudo persegue. A
tecnologia é comum e pública (Three.js + WebGL); o diferencial é (a) pipeline de
VFX offline assando animação em textura e (b) uma disciplina de motion onde
**nenhuma animação é disparada por evento, todas são estado perseguido a cada
frame**. A segunda parte é replicável em uma semana e é onde mora 80% da
sensação. A primeira exige Houdini e uma pessoa de VFX.

---

## Parte 1 — A stack, pelo que é verificável

### 1.1 Renderização

**`oficial`** — Todas as cenas WebGL do site são movidas por **Three.js**. Não é
engine própria, não é WebGPU declarado, não é Unity/Unreal exportado. Three.js
puro, com material e shader autorais.

Isso é a informação mais importante do documento e a mais anticlimática: **a
biblioteca é a mesma que qualquer um usa.** A diferença está no que colocam
dentro dela.

### 1.2 O pipeline offline → real-time (aqui está o ouro)

**`oficial`** — O site foi desenhado e desenvolvido em **Houdini FX, Photoshop e
VS Code**. Boa parte das animações de vértice foi **gerada no Houdini**, e o
vídeo foi renderizado em **Redshift3D**, também usado para combinar vídeo com
animação real-time.

**`oficial`** — A técnica declarada é **Vertex Animation Texture (VAT)**: em vez
de rodar simulação no browser, a simulação roda no Houdini e o **resultado é
assado em texturas PNG — uma para posições, outra para normais**. Em runtime o
vertex shader lê a textura e reposiciona os vértices; não há física acontecendo
no cliente.

**`oficial`** — Na cena de contato, uma geometria em forma de dedo arrasta um
tecido; simularam **três direções** de arrasto e guardaram os resultados em
textura. O custo declarado da técnica: **um modelo de 1,1 s com 1024 vértices
consome 792 KB só para uma direção de valores de posição.**

Esse número é a régua honesta do método. VAT compra qualidade de simulação
impossível em tempo real, e paga em **banda e memória de textura** — e paga
linearmente por direção de animação. Três direções ≈ 2,3 MB só de posição, antes
das normais.

**`inferencia`** — Para caber, o padrão da indústria é: geometria de baixa
contagem de vértices, textura em ponto flutuante ou half-float (`.exr`/`.hdr`) ou
codificação RGBA de 8 bits com faixa remapeada, e compressão GPU (KTX2/Basis) no
que for cor. Não vi o que o Lusion de fato usa.

### 1.3 Os *curly tubes*

**`educacao`** — O efeito de tubos encaracolados com espalhamento de luz da home
foi reproduzido publicamente pelo Codrops (maio/2021, "Curly Tubes from the
Lusion Website with Three.js"). A receita geral: pontos gerados por **curl
noise** → `CatmullRomCurve3` → `TubeGeometry` → material com **light scattering**
falso. Não consegui abrir o artigo para transcrever o código.

<!-- verificar: abrir o tutorial do Codrops e transcrever a matemática do
     scattering — é o que dá o "vidro leitoso" e não está reconstituído aqui. -->

### 1.4 Filosofia declarada

**`oficial`** — O estúdio afirma que a maioria das produtoras usa vídeo bem
produzido no próprio site, e que, sendo um estúdio pequeno vendendo **capacidade
de real-time**, a melhor coisa a fazer é **mostrar real-time rodando**.

Isso não é detalhe de marketing, é decisão de arquitetura: o site é o
*showreel*, e o *showreel* é executável. Para a YAD a leitura é direta — um
portfólio de audiovisual que roda vídeo é redundante com o próprio conteúdo; o
que diferencia é o que só existe rodando.

### 1.5 O que eu **não** verifiquei e não vou afirmar

Não tenho evidência para nada disto, e cada item é uma pergunta aberta para a
sessão com rede:

- Framework de front (Next/Nuxt/Vue/vanilla), bundler, roteamento.
- Se usam **Lenis** ou scroll virtual próprio.
- Se usam **GSAP** ou tweening autoral.
- Pilha de pós-processamento (bloom, DOF, motion blur) e em que ordem.
- Se há **GPGPU/FBO ping-pong** para partículas.
- Se há **raymarching/SDF** em alguma cena.
- Se migraram para **WebGPU/TSL** nas versões recentes do site.
- Estratégia de fallback mobile e de `prefers-reduced-motion`.

**`educacao`** — O que é público é o *estado do mercado* em 2026, não a escolha
do Lusion: a combinação **Lenis + GSAP ScrollTrigger + Three.js** é hoje a pilha
de produção padrão para scroll 3D premium, e o Lenis (darkroom.engineering)
virou o default de smooth scroll. Use isso como referência de ecossistema, não
como afirmação sobre o Lusion.

---

## Parte 2 — Motion: o que realmente faz o site parecer vivo

Esta é a parte que interessa, e é a parte que **não depende de Houdini nem de
WebGL**. É arquitetura de estado. Nove princípios; os cinco primeiros valem
sozinhos.

### P1 — Nada salta. Tudo persegue.

O erro que separa site bom de site premiado: usar o valor de input direto.

```js
// ERRADO — o objeto é o mouse. Cru, nervoso, sem peso.
mesh.position.x = pointer.x

// CERTO — o mouse é o alvo; o objeto persegue com massa.
target.x = pointer.x
current.x = damp(current.x, target.x, 4, dt)
mesh.position.x = current.x
```

Todo valor visível do sistema — posição de câmera, intensidade de luz, progresso
de hover, offset de scroll, força de distorção — é um par `(target, current)`. O
input escreve em `target`. O loop de render aproxima `current` de `target`. Nada
mais escreve em `current`.

Consequência que ninguém antecipa: **interações interrompidas param de quebrar.**
Não existe "animação em andamento" para cancelar, não existe conflito entre dois
tweens, não existe estado inconsistente quando o usuário sai do hover no meio.
Só existe um alvo que mudou.

### P2 — A suavização tem que ser independente de frame rate

**`educacao`** — O `lerp` ingênuo com constante fixa é dependente de frame rate:
o mesmo código fica visivelmente mais lento a 60 fps do que a 144 fps. A correção
canônica é decaimento exponencial em função de `dt`:

```js
// current += (target - current) * (1 - exp(-lambda * dt))
const damp = (current, target, lambda, dt) =>
  target + (current - target) * Math.exp(-lambda * dt)
```

Essa forma é matematicamente estável: aplicar 60 vezes com `dt = 1/60` dá o mesmo
resultado que 30 vezes com `dt = 1/30`, ou uma vez com `dt = 1`. `lambda` é o
único parâmetro e tem significado físico — **`lambda` maior = mais rápido, mais
leve.** Uma referência útil: com `lambda = 4`, a distância cai a ~2% em um
segundo.

Um site com essa correção e outro sem, com o mesmo shader, sentem-se de
categorias diferentes em monitores de 120 Hz. É o item de maior retorno por
linha de código deste documento.

### P3 — Massa diferente por camada. É parallax de comportamento.

Profundidade não se faz só deslocando camadas em velocidades diferentes; se faz
dando **inércias diferentes** a elas. Escala que uso:

| Camada | `lambda` | Sensação |
|---|---|---|
| Câmera / cena inteira | 1,5 – 3 | Pesada, cinematográfica |
| Objeto principal | 3 – 6 | Presente, responsivo |
| Luz / reflexo / detalhe | 6 – 10 | Vivo |
| Cursor custom / partícula | 10 – 20 | Colado no dedo |

O olho lê a diferença de inércia como diferença de massa, e massa como
profundidade. Um valor só para tudo achata a cena mesmo com 3D correto.

### P4 — Velocidade é sinal de primeira classe

Aqui mora o "peso" que as pessoas descrevem e não sabem nomear. Não basta seguir
a posição do ponteiro/scroll: **derive a velocidade, suavize a velocidade também,
e mande ela para o shader.** A velocidade dirige tudo que é deformação:

- estica geometria no eixo do movimento (*stretch*/*squash* em vertex shader);
- abre aberração cromática proporcional;
- aumenta o raio do motion blur;
- curva os tubos, agita as partículas, embaça o fundo.

Regra: **posição controla onde. Velocidade controla quanto.** Quando o usuário
para, a velocidade cai a zero e a cena "assenta" sozinha — e é esse assentar que
lê como material físico.

### P5 — Overshoot é escolha, não acidente

Damping exponencial nunca ultrapassa o alvo. Para elementos que precisam de
personalidade — botão, card, cursor, entrada de texto — use **spring** com
amortecimento subcrítico e um pequeno overshoot; para câmera, **nunca**.

| Elemento | ζ (damping ratio) | Por quê |
|---|---|---|
| Câmera, orbit, foco | 1,0 (crítico) | Oscilar câmera embrulha o estômago |
| Painel, card, sheet | 0,8 | Overshoot mínimo, lê como "encaixou" |
| Cursor, ícone, microinteração | 0,6 – 0,7 | Overshoot visível, lê como brincalhão |

Implementação em `motion-lab/motion.js` (`Spring`), por Euler semi-implícito, que
é estável e independente de frame rate por sub-passo fixo.

### P6 — Um clock só, e com `dt` limitado

```js
dt = Math.min((now - last) / 1000, 1 / 30)   // teto obrigatório
```

Sem o teto, voltar de uma aba em background entrega um `dt` de vários segundos e
o frame seguinte teleporta tudo — ou explode a integração do spring. Um relógio
único também garante que todas as camadas concordem sobre o tempo, o que é
pré-requisito de qualquer coreografia.

### P7 — Motion por vértice e por pixel vai para a GPU

O que é *por objeto* fica na CPU (as dezenas de `damp` acima custam nada). O que
é *por vértice ou por partícula* nunca. Três caminhos, em ordem crescente de
esforço:

1. **Vertex shader procedural** — deslocamento por curl noise, ondulação, twist.
   Barato, sem asset, controlável por uniform. É o caminho para 90% dos casos.
2. **VAT** — o caminho do Lusion. Simulação de verdade (tecido, colisão,
   fratura) assada em textura. Fidelidade máxima, custo de banda alto, animação
   fixa e não interativa (o interativo é *qual* animação e *em que fase* ela
   está).
3. **GPGPU / FBO ping-pong** — estado das partículas vive em textura, atualizado
   por um shader por frame. Interativo de verdade, simulação viva, e é a coisa
   mais cara de depurar da lista.

### P8 — Curva autoral, nunca a curva padrão

`ease-in-out` do CSS é reconhecível e barato. O vocabulário de motion premiado é
quase todo **saída longa**: acelera muito rápido, desacelera por muito tempo
(família `expo.out`, `quint.out`). Duas regras práticas:

- **Entrada de elemento**: rápido no começo, cauda longa. O usuário percebe a
  resposta imediata e a cena termina de acomodar sozinha.
- **Saída**: mais curta que a entrada, quase sempre. Saída lenta lê como travado.

### P9 — Coreografia: stagger e um sujeito por vez

Nada entra junto. Deslocamentos de 40–90 ms entre irmãos, e **um foco de
atenção por momento**. Cena onde três coisas se movem com a mesma importância
não tem hierarquia, e sem hierarquia o motion vira ruído — vale exatamente igual
para decupagem de vídeo.

---

## Parte 3 — Como montar algo inspirado (plano executável)

### 3.1 Arquitetura em quatro camadas

```
  INPUT          →  ESTADO           →  CENA            →  RENDER
  wheel/touch       target/current      three.js          composer
  pointer           damp / spring       uniforms          bloom/DOF
  resize            velocity            VAT / noise       motion blur
  intersection      progress            câmera            fallback 2D
```

A regra que sustenta tudo: **INPUT nunca fala com CENA.** Input só escreve
`target`. A cena só lê `current`. Assim o mesmo estado alimenta WebGL, DOM e o
fallback sem WebGL — e o site continua coerente quando o 3D não carrega.

### 3.2 Ordem de execução (o que fazer primeiro)

| # | Etapa | Esforço | Retorno |
|---|---|---|---|
| 1 | Clock + `damp` + `Spring` + pointer com velocidade | 1 dia | **Altíssimo** |
| 2 | Scroll virtual com damping e velocidade | 1 dia | **Altíssimo** |
| 3 | Aplicar P3 (massas por camada) no que já existe em DOM | 1 dia | Alto |
| 4 | Cena Three.js: uma peça, um material autoral | 3–5 dias | Alto |
| 5 | Velocidade → distorção no shader (P4) | 2 dias | **Altíssimo** |
| 6 | Pós: bloom + DOF sutil | 2 dias | Médio |
| 7 | VAT com Houdini | 2–4 semanas | Alto, mas só com VFX na casa |
| 8 | GPGPU partículas | 1–2 semanas | Médio, alto risco |

**As etapas 1, 2, 3 e 5 respondem pela maior parte da sensação e não exigem
Houdini nem 3D.** Comece por elas mesmo que o site final não tenha WebGL nenhum.

### 3.3 As armadilhas, na ordem em que costumam derrubar o projeto

1. **Mobile.** É onde 70% do tráfego chega e onde WebGL pesado morre. Decida no
   dia 1 se o mobile recebe a cena reduzida (menos partículas, sem pós, meia
   resolução) ou uma versão 2D. Decidir isso no fim significa refazer.
2. **`prefers-reduced-motion`.** Não é opcional e não é só "desligar animação":
   é entregar o mesmo conteúdo com transição de opacidade. Um `if` no clock que
   zera as durações resolve, se a arquitetura for por estado (P1).
3. **LCP e SEO.** Cena WebGL na dobra atrasa o LCP. O texto tem que estar em DOM
   real, renderizado antes do canvas, sempre.
4. **Peso de asset.** Os 792 KB por direção do próprio Lusion são o aviso: o
   custo do craft é banda. Orçamento declarado antes de modelar, não depois.
5. **Depurar shader.** Não tem *stack trace*. Reserve o dobro do tempo que a
   estimativa disser.
6. **Fallback de contexto perdido.** `webglcontextlost` acontece em máquina
   real. Sem tratamento, a tela fica preta e o site parece quebrado.

### 3.4 Pilha que eu recomendaria hoje

- **Motion base**: código próprio (o kernel em `lusion-motion-lab/motion.js`) —
  são ~150 linhas e evita dependência no que é mais estrutural.
- **Scroll**: Lenis, ou o `VirtualScroll` do kernel se quiser zero dependência.
- **Tween pontual de UI**: GSAP, se houver coreografia complexa de timeline.
  Para o resto, spring por estado dispensa tween.
- **3D**: Three.js. WebGPU/TSL só se houver GPGPU pesado — o ganho não paga a
  imaturidade em cena simples.
- **VFX**: Houdini + VAT quando existir alguém que faça Houdini. Antes disso,
  vertex shader procedural entrega 70% da leitura por 5% do custo.

---

## Parte 4 — O laboratório

`_meta/research/lusion-motion-lab/`

| Arquivo | O que é |
|---|---|
| `motion.js` | Kernel sem dependência: `Clock`, `damp`, `Spring`, `Pointer`, `VirtualScroll`, easings. É código de produção, não pseudocódigo. |
| `index.html` | Banco de provas. Abre no browser sem servidor e sem rede. Compara lerp ingênuo × damping × spring lado a lado, mostra o trail com massas de P3 e o scroll virtual com velocidade de P4. |

Abrir o `index.html` e arrastar o mouse rápido é mais convincente que este
documento inteiro. A diferença entre a faixa "lerp ingênuo" e a faixa "damped" é
exatamente a distância entre um site comum e um site que parece caro.

---

## Fontes

- [Case Study of Lusion by Lusion — Awwwards, Site of the Month May](https://www.awwwards.com/case-study-for-lusion-by-lusion-winner-of-site-of-the-month-may.html) · `oficial`
- [Lusion — Communication Arts, Webpicks](https://www.commarts.com/webpicks/lusion) · `oficial`
- [Lusion no X sobre Houdini e o estúdio de mograph real-time](https://x.com/lusionltd/status/1140604998138650625) · `oficial`
- [Curly Tubes from the Lusion Website with Three.js — Codrops](https://tympanus.net/codrops/2021/05/17/curly-tubes-from-the-lusion-website-with-three-js/) · `educacao` (não aberto — bloqueado)
- [Frame Rate Independent Damping using Lerp — Rory Driscoll](https://www.rorydriscoll.com/2016/03/07/frame-rate-independent-damping-using-lerp/) · `educacao`
- [My favourite animation trick: exponential smoothing — lisyarus](https://lisyarus.github.io/blog/posts/exponential-smoothing.html) · `educacao`
- [Spring-It-On: The Game Developer's Spring-Roll-Call — Daniel Holden](https://theorangeduck.com/page/spring-roll-call) · `educacao`
- [Lenis — darkroom.engineering](https://github.com/darkroomengineering/lenis) · `educacao`
- [CatmullRomCurve3 — three.js docs](https://threejs.org/docs/#api/en/extras/curves/CatmullRomCurve3) · `educacao`
