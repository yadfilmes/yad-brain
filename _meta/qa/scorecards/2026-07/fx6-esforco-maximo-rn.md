# Scorecard — `captacao/cameras/sony/fx6.md` · rubrica R-N

| | |
|---|---|
| Data | 2026-07-26 |
| Rubrica | R-N v1.0, **inalterada** |
| Revisor | agente independente, contexto limpo, instrução adversarial |
| Resultado | **32 / 100** · gate **G1 reprovado** |

## O experimento

Depois de 0 de 10 aprovadas em três lotes, a pergunta em aberto era: **o
problema é o processo de escrita ou a régua está calibrada acima do
alcançável?** A nota da FX6 foi escrita com esforço máximo de pesquisa —
`WebSearch` recém-destravado, 3 tiers de fonte, 4 URLs de página específica,
`loc` em todas as fontes, CI com zero avisos — para separar as duas hipóteses.

## A resposta do revisor

> Sim — mas não com a R-N como está escrita hoje; e **esta nota não é prova do
> contrário, porque ela reprova por defeitos genuinamente seus.**

E o achado central:

> O esforço máximo de pesquisa foi gasto **no eixo errado**. A nota trouxe 3
> tiers, 4 URLs, `loc` em todas as fontes e zero avisos de CI — e falhou em
> **fidelidade**, não em cobertura. É a lei de Goodhart um andar acima da
> rodada anterior: antes otimizou-se o CI, agora otimizou-se a **contagem de
> fontes**.

## Os seis defeitos — todos de fidelidade

| # | defeito | classe |
|---|---|---|
| 1 | "4K UHD **full frame** 120 fps" — a FX6 tem crop de ~1,1× a 120 fps | afirmação **oposta** à verdade |
| 2 | rolling shutter 8,7 ms atribuído a 3840×2160; a CineD mediu em 4096×2160 | número certo, escopo errado |
| 3 | `ratio: "ordem de 1/6 do corpo"` em `budget_alternative_to` | número sem fonte (real: 1/7–1/9) |
| 4 | problema de 8 canais de áudio atribuído ao **Final Cut**; a fonte é thread do **Premiere Pro** | atribuir à fonte o que ela não diz |
| 5 | "sem controle de foco externo" — a FX6 aceita LANC e controle por grip | gotcha falso |
| 6 | alias `PXW-FX6` — PXW é prefixo da linha broadcast, não existe FX6 PXW | identificador inventado |

Nenhum é falta de fonte. Todos são a fonte **lida errado, citada errado ou
inventada por analogia**. O gate G1 pega número órfão; não pegava nenhum
destes, porque todos tinham fonte ao lado.

## O que isto prova sobre a régua

A aritmética da R-N v1.0 com corte em 92:

| | |
|---|---|
| soma dos pesos | 100 |
| perda máxima tolerada | **8 pontos** |
| itens individualmente fatais | 1 (15), 2 (15), 3 (12), 4 (10) |
| únicos itens que sobrevivem sozinhos | 5, 6, 7 (8 pts) · 8, 9 (6) · 10 (5) · 11 (4) · 12 (3) |
| única dupla que sobrevive junta | 11 + 12 (7 pts) |

Ou seja: **os quatro itens de maior peso são gates disfarçados** — falhar
qualquer um deles sozinho já reprova, exatamente como um gate, mas sem a
honestidade de estar declarado como tal. E três dos quatro (3, 4 e o 11 que os
acompanha) são **sub-especificados**:

- **Item 3** — "arestas completas e específicas para o tipo de nó" não diz
  quais. É julgamento do revisor a cada rodada; o produtor não tem como
  conferir antes de gastar revisão.
- **Item 4** — mistura três exigências diferentes (fonte oficial, URL que
  resolve, `loc`) num único binário.
- **Item 11** — cobra coerência com uma "rubrica de confiança (fontes ×
  corroboração)" que **não existe no repositório**. Item impossível de
  auditar contra documento inexistente.

## Correções aplicadas nesta nota

Os seis defeitos foram corrigidos em `96861aa`. As arestas `see_also` e
`alternative_to` genéricas viraram `accepts_media`, `outputs_signal` e
`enables_technique`.

**A nota permanece em `draft`.** Corrigir os defeitos apontados não a promove:
o protocolo exige revisão nova em contexto limpo, e a rodada de correção não
foi revisada. Registrar aqui é o que impede o ciclo de virar autoaprovação.

## Consequência de processo

Este scorecard fecha o experimento com um veredito de duas partes, e **as duas
partes valem**:

1. **O processo de escrita tem um defeito real** que nenhuma régua conserta:
   fidelidade à fonte. Esforço de pesquisa não o corrige — foi aplicado ao
   máximo e produziu seis erros.
2. **A régua tem itens que não se pode auditar.** Item 3 vira mecânico com
   `_meta/arestas-minimas.md` (feito). Itens 4 e 11 seguem em aberto no
   `_meta/roadmap.md`.

A recalibração do corte 92 é **decisão do dono** e não foi tocada.
