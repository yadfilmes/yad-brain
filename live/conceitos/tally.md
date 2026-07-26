---
id: tally
title: Tally (sinalização de câmera no ar)
type: conceito
zona: universal
aliases: [tally, "luz de tally", "red light", "sinalização de no ar"]
tags: [live, switcher, operacao, multicamera]
status: draft
confidence: media
updated: 2026-07-26
rel:
  see_also: [switcher-me, ndi, sdi]
sources:
  - {url: "https://www.blackmagicdesign.com/products/atem", tier: oficial, ret: 2026-07-26, nota: "saídas de tally"}
---

# Tally (sinalização de câmera no ar)

**TL;DR** — luz que avisa **quem está no ar** (vermelho) e, em muitos sistemas,
quem está no preview (verde). Parece detalhe; na prática é o que impede o
operador de reenquadrar durante o take e o apresentador de olhar para a câmera
errada.

## Quem precisa ver

| pessoa | por quê |
|---|---|
| operador de câmera | não mexer no enquadramento enquanto está no ar |
| apresentador / entrevistado | saber para onde olhar |
| assistentes de palco | não cruzar o quadro ativo |

## Como chega até a câmera

| via | observação |
|---|---|
| cabo de tally dedicado | tradicional, confiável, mais um cabo a puxar |
| embutido no [[sdi]] | dados auxiliares junto do sinal de retorno |
| sobre [[ndi]] | vai junto no mesmo cabo de rede — vantagem real do IP |
| sistemas sem fio | prático em set grande; depende de bateria e RF |

## Gotchas

- **Tally atrasado é pior que tally nenhum**: o operador confia e mexe no
  quadro achando que saiu do ar. Testar a latência ponta a ponta antes.
- Em produção com gravação ISO de todas as câmeras, tally verde ajuda o
  operador a preparar o próximo enquadramento sem ansiedade.
- Apresentador que não enxerga tally acaba olhando para a câmera errada — em
  palco largo, vale luz de tally maior que a padrão.

## Conexões

O estado vem do [[switcher-me]]: program acende vermelho, preview acende verde.
