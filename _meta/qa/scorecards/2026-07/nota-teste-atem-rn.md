# Scorecard — nota-teste `atem-constellation-8k` · rubrica R-N

| | |
|---|---|
| Data | 2026-07-26 |
| Objetivo | testar se as correções de processo consertaram o **ato de escrever** |
| Revisor | agente independente, contexto limpo, instrução adversarial, com verificação externa via busca |
| Resultado | **39/100 — reprovada.** Mas **4/4 gates aprovados**, inédito no projeto |

## O achado estrutural — e é o mais importante do projeto até aqui

> A nota tem **zero avisos** no `validate.py` — única em todo o acervo de 57
> notas, num total de 162 avisos — e pontua **39**.

As regras mecânicas funcionaram como projetadas e **mediram a coisa errada**.
Cada uma virou um *proxy* satisfeito na forma:

| regra | satisfeita? | o que escapou |
|---|---|---|
| `loc` preenchido | sim | cobria 6 das 9 linhas da tabela de specs |
| tier não-oficial presente | sim | nenhum praticante — só fabricante e revista |
| `see_also` ≤ 50% | **0%** | duas arestas semanticamente **erradas** e uma omissão óbvia |

**Diagnóstico aceito:** o ato de escrever mudou onde a régua é mecânica e
**não mudou onde ela é semântica**. É lei de Goodhart aplicada ao próprio
protocolo: a validação virou alvo em vez de instrumento.

As três reprovações mais pesadas (itens 2, 3 e 5 = 35 pts) são todas de classe
que nenhuma regra detectava: condição derrubada de uma linha de spec, aresta
apontando para tipo errado de nó, alias colidindo com outro produto.

## O que de fato melhorou

| padrão sistêmico | estado |
|---|---|
| nº 8 · heurística numérica como fato | **resolvido — o maior ganho.** 11 de 11 números conferidos contra o fabricante, zero divergência. A classe de erro que o projeto mais teme não apareceu |
| nº 1 · fonte cita domínio, `loc` vazio | resolvido na forma |
| nº 4 · `confidence` incoerente | resolvido: primeiro `alta` do acervo que sobrevive a auditoria |
| nº 2 · `see_also` como atalho | **acabou** (0 de 6 arestas, contra 12 de 15 no lote 03) |

Primeira vez em três lotes que **nenhum gate reprova** — inclusive o G1, com
auditoria externa linha a linha.

## O que persiste

- **Aresta omitida com o dado no corpo** (`outputs_signal` num switcher) e uma
  variante nova e pior: **aresta de tipo errado**. O grafo ficou menos raso e
  mais *incorreto*.
- **Alias colidindo com produto vizinho**: `"ATEM Constellation"` é o nome de
  outra linha em produção — grep devolveria a nota errada.
- **Prática sem praticante**: quatro afirmações de campo apoiadas em fabricante
  e revista, incluindo um superlativo sobre distribuição de relatos tirado de
  n=1.

## Correções aplicadas nesta rodada

Todos os 6 itens reprovados foram corrigidos, entre eles:

- tabela de specs reescrita em **dois modos (até UHD × em 8K)** — em 8K os 4
  M/E viram 1, os 4 DVEs viram 1, o multiview vira único; o próprio SKU
  registra isso (`SWATEMSCN4/1ME4/8K`)
- `implements_standard: [smpte]` → `governed_by: [smpte]` (SMPTE é órgão)
- `incompatible_with: [ndi]` removida — violava a convenção "ausência ≠
  negação": não há incompatibilidade verificada, há ausência de suporte nativo
- alias `"ATEM Constellation"` removido e nota `atem-constellation-hd` criada
  como `stub` para desambiguar
- concorrentes nomeados; superlativo de n=1 substituído pelo fato verificável

## Regra mecânica nova, derivada desta revisão

**Coerência de tipo de aresta**: `governed_by` só aponta para `orgao`,
`records_codec` só para `codec`, `has_native_mount` só para `mount`, e assim
por diante. Implementada — e na primeira execução encontrou **o mesmo defeito
em `live/sinais/sdi.md`**, que estava no acervo sem ninguém ver.

## Recomendação registrada pelo revisor

> "Se o alarme de distribuição existe para pegar notas empilhadas logo acima de
> 92, o inverso também merece atenção — uma nota com CI perfeitamente limpo e
> nota 39 é o sinal de que a validação mecânica virou alvo em vez de
> instrumento."

Duas outras regras recomendadas ficam no roadmap: dedup de alias contra o
acervo, e checagem de cobertura entre `loc` declarado e grupos de spec na
tabela.
