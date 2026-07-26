# Scorecard — Lote 02 · rubrica R-N

| | |
|---|---|
| Data | 2026-07-26 |
| Rubrica | R-N (nota de conhecimento) |
| Revisor | agente independente, contexto limpo, instrução adversarial |
| Ciclo | 1 |
| Resultado | **0 de 4 aprovadas** |

## Notas avaliadas

| nota | G1 | G2 | G3 | G4 | nota | veredito |
|---|---|---|---|---|---:|---|
| `venice-2` | fail | **fail** | fail | n/a | **51** | permanece `draft` |
| `aces` | pass | pass | pass | n/a | **70** | permanece `draft` |
| `flicker-parede-led` | pass | pass | pass | n/a | **65** | permanece `draft` |
| `nr-35-trabalho-em-altura` | fail | pass | fail | **fail** | **48** | permanece `stub` |

## Padrões sistêmicos identificados

Estes são o produto mais valioso da revisão: defeitos que se repetiriam em
todas as notas futuras se não virassem regra.

1. **Fontes citam domínio, não evidência — 4/4 reprovadas.**
   `docs.acescentral.com`, `pro.sony`, `reddit.com/r/cinematography/`, o índice
   de todas as NRs em vez da NR-35. O campo `loc` existe na convenção e no
   template e teve **zero ocorrências** nas quatro notas.
   → Virou regra mecânica no `validate.py`.

2. **Arestas rasas — 4/4 reprovadas.** Três padrões: `see_also` como atalho
   onde existe aresta específica; aresta específica omitida apesar de o dado
   estar no corpo (`accepts_media`/AXS, `diagnosed_with`, `governed_by`);
   e chave declarada vazia contradizendo o próprio corpo (`variant_of: []`
   numa nota que descreve a variante).
   **`see_also` era 61 de 120 arestas do acervo** — o grafo estava bem mais
   raso do que os números sugeriam.
   → Virou aviso mecânico no `validate.py`.

3. **Alias confundido com "termo relacionado" — 3/4.** `AP0`/`AP1` como alias
   de ACES (são sub-espaços distintos, não outros nomes), enquanto nomes que a
   própria nota usa no corpo ficavam de fora ("VENICE 2 6K", "cintilação").

4. **Contradição entre frontmatter e corpo.** `confidence: alta` com specs
   vazias; `confidence: media` em conteúdo declaradamente não conferido.
   → Virou regra mecânica: `<!-- verificar -->` em spec impede `alta`.

5. **Bloqueio de processo.** `_meta/qa/scorecards/` não existia. Pela S.9.2 do
   protocolo, `reviewed` exige scorecard arquivado — logo, nenhuma nota do
   acervo podia legitimamente ser `reviewed`, independentemente da rubrica.
   → Corrigido: este arquivo inaugura o diretório.

6. **O gate de segurança não pode ser fechado por IA.** A nota `nr-35` precisa
   de nome humano no scorecard. Pior: o `validate.py` deixava passar em
   silêncio (era só aviso).
   → Virou erro mecânico: `risco: seguranca` + `reviewed` sem campo
   `revisor_humano` reprova o CI.

## Erro semântico grave encontrado

Em `flicker-parede-led`, `genlock` aparecia simultaneamente em `caused_by` e
`resolved_by` — o grafo afirmava que a mesma coisa causa e resolve o problema.
A causa é a **ausência** de genlock, não o genlock. Corrigido.

## Decisão

Nenhuma promoção. As quatro permanecem onde estavam, e os itens reprovados
viraram o plano de correção — dos quais os sistêmicos foram implementados como
regra de validação, e os de fonte estão bloqueados (ver `_meta/qa/blocked.md`).
