---
id: switcher-me
title: M/E, program, preview e keyer — anatomia de um switcher
type: conceito
zona: universal
aliases: ["M/E", "ME", "mix effects", switcher, "vision mixer", "mixer de video", "mixer de vídeo"]
tags: [live, switcher, broadcast, operacao]
status: draft
confidence: media
updated: 2026-07-26
rel:
  accepts_signal: [sdi, ndi]
  controls: [tally]
sources:
  - {url: "https://www.blackmagicdesign.com/products/atem", tier: oficial, ret: 2026-07-26, nota: "arquitetura de M/E e keyers"}
---

# M/E, program, preview e keyer — anatomia de um switcher

**TL;DR** — **M/E (Mix/Effects)** é um bloco completo de mistura: escolhe
fontes, aplica transição e chaves, e entrega um resultado. Um switcher de
"1 M/E" monta uma composição por vez; de "4 M/E", quatro em paralelo — é a
métrica que define o que a produção consegue fazer simultaneamente.

## Os barramentos

| barramento | função |
|---|---|
| **Program** | o que está no ar, agora |
| **Preview** | o que entra no próximo corte — sempre confira aqui antes |
| **Aux** | saídas auxiliares independentes (telão, gravação, retorno) |

A disciplina de sempre montar no Preview antes de cortar é o que separa
operação profissional de acidente ao vivo.

## Keyers

| tipo | uso |
|---|---|
| **Upstream (USK)** | dentro do M/E — chroma key, sobreposição que participa da transição |
| **Downstream (DSK)** | depois do M/E — logo e legenda, que ficam no ar independentes do corte |

Regra prática: logo permanente vai no **DSK**, para não sumir a cada transição.

## Quantos M/E você realmente precisa

| operação | M/E |
|---|---|
| entrevista simples, corte entre câmeras | 1 |
| evento com telão recebendo composição diferente do ar | 2 |
| produção com cenários virtuais e múltiplos destinos | 3–4 |

Contar M/E é contar **composições simultâneas independentes**, não câmeras.
É o erro de dimensionamento mais comum ao orçar switcher.

## Conexões

Entradas chegam por [[sdi]] ou [[ndi]]; o retorno de estado para o operador de
câmera é o [[tally]].
