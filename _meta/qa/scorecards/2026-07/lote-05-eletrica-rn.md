# Scorecard — Lote 05 · elétrica · rubrica R-N v1.2

| | |
|---|---|
| Data | 2026-07-26 |
| Rubrica | R-N v1.2, **inalterada** |
| Revisor | agente independente, contexto limpo, instrução adversarial |
| Verificação | `validate.py` · **7 comandos publicados executados** · todas as tabelas recomputadas importando `eletrica.py` · 4 buscas de conferência de `cit` |
| Resultado | **0 de 4 aprovadas** · 63 · 52 · 52 · 52 · **G1 e G3 reprovados nas quatro** |

| nota | itens reprovados | G1 | G2 | G3 | nota |
|---|---|---|---|---|---:|
| `rede-ac` | 2, 4, 7, 11 | fail | pass | fail | 63 |
| `bitola-de-cabo` | 1, 2, 4, 7 | fail | pass | fail | 52 |
| `gerador` | 1, 2, 4, 7 | fail | pass | fail | 52 |
| `balanceamento-de-fase` | 1, 2, 4, 7 | fail | pass | fail | 52 |

## O achado central: reprodutibilidade não é rastreabilidade

Este lote foi escrito com orgulho de uma coisa: **todo número publicado é
reproduzível por comando**. O revisor rodou os 7 comandos, recomputou todas as
tabelas, e confirmou — *"a reprodutibilidade é real; é o lote mais internamente
consistente que a régua já mediu"*. E então:

> Os números saem de constantes que **não têm fonte nenhuma** — `RHO_COBRE`,
> `CAPACIDADE_A`, `QUEDA_MAX_PCT`, `FOLGA_DISJUNTOR`, `fp = 0,92`, as margens
> de gerador. **Número reproduzido de constante órfã continua órfão.**

**É a lei de Goodhart pela quarta vez neste projeto**, e cada vez com um alvo
mais sofisticado:

| rodada | o que virou alvo |
|---|---|
| nota-teste ATEM | o **CI** — nota com zero avisos tirou 39 |
| FX6 | a **contagem de fontes** — 3 tiers, 4 URLs, `loc` em todas, e 6 erros |
| lote 04 | a **fidelidade da citação** — `loc` virou título, `cit` virou carimbo |
| **lote 05** | a **reprodutibilidade** — comando roda, número bate, constante não tem fonte |

## Erros factuais confirmados um a um

As quatro acusações checáveis foram verificadas contra o próprio repositório e
**as quatro procedem**:

| acusação | verificação | veredito |
|---|---|---|
| "duas e **quatro** bitolas comerciais acima" | `BITOLAS.index(16) - BITOLAS.index(4) = 3` | **procede** — erro aritmético |
| "três fases de 20 A aguentam **60 A**" | `3 × 20 × FOLGA_DISJUNTOR = 48 A` | **procede** — contradiz a regra dos 80% que o próprio acervo publica |
| `balanceamento-de-fase` nunca declara a tensão | as correntes são de 220 V; a 127 V erram por 73% | **procede** |
| comandos de `rede-ac` não produzem bitola | executado: sem `--distancia` não há bitola na saída | **procede** |

## Defeitos nas ferramentas — os dois graves

**1. `validate.py` não conferia `[[wikilink]]` de corpo.** O docstring prometia
"link não quebrado" e cobria só alvos de `rel:`. `gerador.md` passou com **zero
erros e zero avisos** carregando dois `[[hmi]]` mortos. Achado novo, não visto
nos lotes 02–04.

**2. `confianca_esperada()` continuava divergindo da tabela — na 3ª linha.**
O lote 04 achou a divergência na 4ª linha e ela foi corrigida. **A mesma classe
sobreviveu intacta na linha vizinha**, porque só a linha reportada foi
consertada. Para `rede-ac` o script devolvia `media` onde a tabela manda
`baixa`, e o CI ficava em silêncio.

Isto é mais grave que o defeito em si: **corrigir o caso reportado em vez da
classe** é como o mesmo defeito atravessa duas rodadas de revisão.

## Correções aplicadas

**Fatos:** os quatro erros acima. **Ferramentas:** check de wikilink de corpo;
`confianca_esperada()` reescrita seguindo a tabela **linha a linha**, com
`tem_afirmacao_numerica()` implementando a 3ª — e **um caso-ouro por linha da
tabela** no `test_validate.py`, para que régua e script não voltem a separar em
nenhuma delas.

**Premissas:** criado `_meta/constantes-de-calculo.md`, que registra o estado de
cada constante (**F** fonte verificada · **P** premissa de planejamento · **N**
de norma não aberta) e a regra que sai daí: *toda constante é ou fonte
verificada ou premissa declarada; premissa não vira fato por ser reproduzível.*
As quatro notas passaram a declarar isso em seção própria.

**Disclaimer:** removido das três notas onde violava a própria convenção —
`conventions.md` manda o disclaimer de cálculo para a **saída da ferramenta**,
e a ferramenta já o imprime. Ele empurrava o TL;DR para fora da primeira linha
e custava 15 pontos por nota.

**Não corrigido:** os itens 4 e 7 (procedência e tier de prática) exigem fonte
`oficial`/`lab` e fonte de campo, que dependem de B1. Ficam como plano de
correção do ciclo 2.

## Defeitos de régua registrados, não aplicados

O revisor levantou três, e **nenhum foi usado para alterar nota** — vão a PR:

1. **Colisão item 1 × disclaimer obrigatório.** Nota `risco: seguranca` é
   obrigada a carregar disclaimer; se ele vier antes do TL;DR, o item 1 reprova
   por construção — 15 pontos que `nr-10` e `nr-35` não podem recuperar. A R-N
   não diz se o disclaimer conta como corpo.
2. **G3 e item 4 medem a mesma coisa.** Decidiram-se pela mesma evidência nas
   quatro; os 10 pontos do item 4 não acrescentaram diagnóstico. É a lacuna R9
   já registrada, agora com dado.
3. **A heurística de prática do `validate.py` tem um caminho novo de escape:**
   só dispara quando os tiers são *exclusivamente* `oficial`. Com fonte
   `educacao`, prática sem fonte de prática passa em silêncio — foi o que
   ocorreu nas quatro.

## O que este lote provou

**A régua está medindo o que deve.** Ela pegou erro aritmético, contradição
interna do acervo, escopo ausente, comando que não faz o que a nota diz, e
dois defeitos nas próprias ferramentas — inclusive um que atravessou duas
revisões por ter sido corrigido caso a caso em vez de por classe.

**O que ainda reprova é procedência.** G3 caiu nas quatro pela mesma causa
única: 5 entradas de `sources[]`, todas `educacao`, quatro delas a mesma URL.
Isso não se conserta escrevendo melhor — depende de B1.
