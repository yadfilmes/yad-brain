---
id: 00-indice-mestre
title: Índice mestre
type: moc
zona: universal
aliases: ["indice mestre", "mapa do acervo", "start here"]
tags: [moc, navegacao]
status: draft
confidence: baixa
updated: 2026-07-26
rel:
  see_also: [venice-2, alexa-35, pyxis-6k]
sources:
  - {url: "interno", tier: campo-proprio, ret: 2026-07-26, nota: "curadoria própria de navegação"}
---

# Índice mestre

**TL;DR** — ponto de entrada humano do acervo. Ler este arquivo custa pouco e
diz para onde ir; ler o acervo inteiro custa caro e quase nunca é necessário.
Os índices automáticos ficam em `_index/`; este aqui é curado à mão.

## Por domínio

| domínio | o que tem hoje |
|---|---|
| **Captação** | [[venice-2]] · [[alexa-35]] · [[pyxis-6k]] · [[mount--pl]] · [[mount--e]] |
| **Pós e formatos** | [[braw]] · [[prores]] |
| **Conceitos** | [[filtro-nd]] · [[obturador-180]] · [[genlock]] |
| **Diagnóstico** | [[flicker-parede-led]] |
| **Segurança** | [[nr-35-trabalho-em-altura]] |
| **Luz** | [[ls-600d-pro]] · [[evoke-2400b]] · [[temperatura-de-cor]] · [[cri-tlci-ssi]] · [[lei-do-inverso-do-quadrado]] |
| **Live** | [[sdi]] · [[ndi]] · [[switcher-me]] · [[tally]] · [[rede-gigabit]] |
| **Produção** | [[diretor-de-fotografia]] · [[gaffer]] · [[ordem-do-dia]] · [[mapa-de-luz]] |
| **Marcas** | [[sony]] · [[arri]] · [[blackmagic-design]] · [[aputure]] · [[nanlux]] |

## Índices automáticos

- `_index/por-tipo.md` — tudo agrupado por tipo de entidade
- `_index/por-marca.md` — tudo agrupado por fabricante
- `_index/backlinks.md` — quem aponta para quem
- `_index/specs.csv` — projeção tabular, para filtro numérico e multi-critério
- `_graph/stats.md` — progresso, cobertura e qualidade
- `_meta/gaps.md` — **a fila de trabalho**: o que escrever a seguir

## Caminhos de leitura sugeridos

**Escolher câmera para um job** → [[venice-2]] · [[alexa-35]] · [[pyxis-6k]],
depois o codec que cada uma grava e o impacto em storage
(`tools/calc/storage.py`).

**Montar fluxo de cor** → codec ([[braw]], [[prores]]) → curva → color space →
pipeline. É a espinha dorsal do grafo.

**Resolver problema em set** → começar pelo sintoma em
`troubleshooting/`, não pelo equipamento.

## Estado do acervo

Fase 1 — fundação de pé, acervo em construção. As notas estão em `draft`; para
subir a `reviewed` precisam passar pelo Protocolo 92
(`_meta/qa/protocolo-92.md`).
