# Scorecard — Lote 03 · rubrica R-N

| | |
|---|---|
| Data | 2026-07-26 |
| Rubrica | R-N v1.0, **inalterada** desde o lote 02 |
| Revisor | agente independente, contexto limpo, instrução adversarial |
| Resultado | **0 de 5 aprovadas** · média **49,4** (lote 02: 58,5) |

| nota | G1 | G2 | G3 | nota |
|---|---|---|---|---:|
| `ndi` | pass | **fail** | pass | 41 |
| `switcher-me` | **fail** | **fail** | pass | 32 |
| `gaffer` | pass | **fail** | **fail** | 58 |
| `mapa-de-luz` | pass | **fail** | **fail** | 58 |
| `cri-tlci-ssi` | **fail** | **fail** | pass | 58 |

## O achado central: o processo piorou, não melhorou

A média caiu. Mais grave, o grafo **regrediu** — medido nos próprios `stats.md`
commit a commit:

| momento | arestas | `see_also` | % |
|---|---:|---:|---:|
| `859ed42` (scorecard lote 02) | 120 | 61 | 50,8% |
| `549a8a6` "adensamento: 50% → 27%" | 146 | 40 | **27,4%** |
| `HEAD` (lote 03) | 194 | 79 | **40,7%** |

O lote 03 acrescentou 33 arestas, **28 delas `see_also` (85%)**. Nas 5 notas
revisadas: 12 de 15 arestas eram `see_also` (80%) — pior que os 50,8% que
haviam reprovado 4/4 no lote anterior.

**Diagnóstico do revisor, aceito integralmente:** a correção do lote 02 foi
aplicada como *faxina pontual*, não incorporada ao **ato de escrever**. O
mutirão de adensamento foi desfeito pela produção seguinte.

## A causa raiz — e a correção

As regras mecânicas criadas no lote 02 disparavam **apenas em `status:
reviewed`**. Como o bloqueio B1 impede qualquer nota de chegar lá, elas
*barravam a promoção* em vez de *induzir a correção durante a escrita*. O
defeito seguia sendo produzido em 100% das notas novas e apenas ficava
represado.

Correção aplicada: **toda regra agora avisa em `draft` e reprova em
`reviewed`**. O acervo saltou de 25 para 172 avisos — a dívida deixou de ser
invisível.

## Buracos fechados nas regras mecânicas

| buraco | correção |
|---|---|
| aviso de grafo raso só disparava com ≥4 arestas — `switcher-me` (3/3 `see_also`) e `cri-tlci-ssi` (1/1) passavam em silêncio | gatilho baixado para ≥2 |
| `loc` ausente só reprovava em `reviewed`; **zero ocorrências em 55 notas** | vira aviso em `draft` |
| alias acentuado sem par ASCII — o grep é byte a byte | novo aviso |
| `confidence: media` virou valor-padrão (5/5 idênticas, fonte única, sem corroboração) | novo aviso sugerindo `baixa` |
| prática de campo sustentada por fonte `oficial` — 5/5 do lote | novo aviso pedindo tier `comunidade`/`campo-proprio`/`lab` |

## Padrões sistêmicos novos (do lote 03)

7. **Prática de campo sob fonte oficial — 5/5.** As notas são majoritariamente
   conhecimento operacional ("montar no preview antes de cortar", "fotografar a
   montagem final") e nenhuma declara tier `comunidade` ou `campo-proprio`. O
   `AGENTS.md` proíbe explicitamente trocar um pelo outro.
8. **Heurística numérica apresentada como fato.** A tabela "1/2/3–4 M/E" e o
   "quase todo LED anuncia CRI acima de 95" passaram pela autochecagem do
   produtor. É a classe exata que o gate G1 existe para pegar.
9. **Três dos cinco tipos não têm template** (`funcao`, `documento`,
   `interface`) — o item 10 da rubrica não tem contra o que ser medido.

## Sobre a calibração do benchmark

O commit do lote declarava "45/45 no conjunto-ouro" enquanto as notas pontuavam
32–58 na R-N. Não é contradição: o conjunto-ouro mede **recuperação** (achar o
arquivo certo) e é cego ao que a R-N mede (procedência, profundidade de grafo,
tier de fonte). Registrado como item de revisão do benchmark — ver
`_meta/roadmap.md`.

## Custo de processo reconhecido

Escreveram-se 10 notas novas sob um bloqueio (B1) que já declarava que nenhuma
delas poderia chegar a `reviewed`. O custo de revisão foi gasto num lote
estruturalmente impedido de passar. **Lição:** com B1 ativo, produzir volume
antes de consertar o ato de escrever multiplica retrabalho.
