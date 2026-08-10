# Memória da casa

O que a YAD já pagou, cobrou e aprendeu. **Este arquivo cresce a cada
pressuposto fechado** — é o passo 5 do fluxo, e some se ninguém escrever.

Ao acrescentar: data, job, valor e **se é cachê pago ou preço de venda**. Os
dois no mesmo arquivo sem distinção destroem o valor dele.

---

## Alíquota de imposto

| quando | alíquota | onde apareceu |
|---|---|---|
| 2026 (atual) | **16%** | Barretos 2026, novela vertical |
| 2026 (live BYD) | 15% | pressuposto BYD 23–24.06 |

Alíquota vive numa célula editável no bloco de entradas. Job com regime
diferente é trocar aquele número, não refazer a planilha.

---

## Cachês pagos (o que a pessoa recebe)

### Externa / multicam — Barretos 2026, Clube do Cowboy

| função | pessoa | valor | unidade |
|---|---|---|---|
| Assistente técnico geral | Viny | 200 | diária |
| Assistente técnico geral | Caio | 250 | diária |
| Técnico do sistema | Cassio | 800 | diária |
| Cinegrafista | Paulinho, Guilherme, Rodrigo, Kadu, Fhilippe | 500 | diária |
| Produção adm | Larissa | 2.500 | pacote |
| Responsável do sistema | Carlos | 0 | entra na escala sem cachê |

Locação de terceiro: **Danilo — câmeras broadcast, R$ 1.000/diária.**

### Live / estúdio — BYD 23 e 24.06

| função | valor | unidade |
|---|---|---|
| Assistente | 700 – 1.050 | pacote |
| Câmera | 700 – 1.400 | pacote |
| Áudio | 900 | pacote |
| Diretor de live | 800 | pacote |
| Resolume / assistente | 1.000 | pacote |
| Maquiagem | 900 | pacote |
| Design | 2.000 | pacote |
| Montagem e desmontagem de painel de LED (Natan) | 2.700 | serviço |

Fornecedores do mesmo job: estúdio 8.000 · MJ Geradores 4.500 · box truss 2.800
· lona 1.022 · acervo 1.000 · luz 3.760 · Mega 12.000 · Gabo 1.500.

Direção, DTV, roteiro, produção, motion e VMIX entraram com **zero** — equipe da
casa, sem cachê no pressuposto.

### Pós-produção — novela vertical, Movioca

| função | valor | unidade |
|---|---|---|
| Montador finalizador | 12.000 | mês |
| Montador | 7.000 | mês |
| Diretor de fotografia | 17.000 | pacote |
| Cinegrafista | 7.000 | projeto |
| Finalização de áudio | 12.000 | projeto |
| HD 24 TB | 3.500 | unidade |

---

## Preço de venda (o que o cliente paga) — NÃO é cachê

Orçamento Barretos 2026, para comparar com os cachês acima:

| linha do orçamento | valor de venda |
|---|---|
| Técnico sistema | 800/diária |
| Assistente geral | 350/diária |
| Técnico câmeras | 500/diária |

**A distância entre as duas tabelas é a margem.** O assistente geral vende a 350
e recebe 200–250. Cinegrafista vende e paga 500 — nessa função não há margem de
equipe, o lucro vem do equipamento.

Orçamento novela vertical (Movioca), para referência de escopo de pós:
color grading 25.000 · VFX + IA 13.000 · edição de som e mix 25.000 ·
legendagem PT 2.000 · legendagem EN 2.000 · licenças de trilha 1.000 ·
montador sênior 16.000/7 semanas · assistente de montagem 12.000/7 semanas.

---

## Áreas por tipo de job

Ponto de partida, não camisa de força. A pergunta certa é "onde esse job gasta".

**Externa / evento / multicam:** EQUIPE · TRANSPORTE E LOGÍSTICA · ALIMENTAÇÃO ·
HOSPEDAGEM · EQUIPAMENTO E MANUTENÇÃO · LOCAÇÃO DE TERCEIROS · PRODUÇÃO E
DIVERSOS · COMISSÃO

**Pós-produção / série / novela:** MONTAGEM E PÓS · EQUIPE TÉCNICA · FINALIZAÇÃO
· EQUIPAMENTO E MÍDIA · LICENÇAS E TRILHA · PRODUÇÃO E DIVERSOS · COMISSÃO

**Live / estúdio** (blocos do pressuposto BYD): EQUIPE · DIVERSOS · ALIMENTAÇÃO ·
TRANSPORTE · LOCAÇÃO · COMISSÃO

## Comissão de captação

Existe e é grande. **A base muda o valor e precisa ser perguntada**, porque
"15% do job" é ambíguo:

| job | percentual | base | valor |
|---|---|---|---|
| Live BYD | 10% | entrada **bruta** (94.790) | 9.479 |
| Novela vertical | 15% | entrada **líquida** (189.000) | 28.350 |

Na novela vertical, 15% sobre a bruta daria R$ 33.750 — **R$ 5.400 a mais** que
o lançado. Antes de fechar, confirmar com o captador se o combinado é sobre o
que o cliente paga ou sobre o que sobra depois do imposto.

**Lance a comissão como fórmula, não como número.** O padrão que o Felype e a
Larissa criaram na novela vertical, e que vale repetir:

- uma célula de percentual no `RESUMO`, ao lado do imposto
- a linha em `SAIDAS` com o valor unitário calculado:
  `=ROUND(RESUMO!$C$24*RESUMO!$F$22,2)` — líquida × percentual
- a observação também por fórmula, para se reescrever sozinha:
  `=TEXT(RESUMO!$F$22,"0,0%")&" da entrada líquida"`

Não gera referência circular: a líquida não depende das saídas. Se o imposto ou
a entrada mudarem, a comissão acompanha.

⚠️ Isso ainda **não** existe em `tools/pressuposto_real.py`. Regenerar uma
planilha que tenha essa customização feita à mão apaga as três células. Ou
incorpora ao gerador, ou avisa antes de regerar.

---

## Jobs fechados

### Barretos 2026 — Clube do Cowboy (v4, fechado)

19 a 31/08/2026, 10 diárias. Contato Alex (034) 99645-0612.

| | |
|---|---|
| entrada bruta | 108.500 (40.500 + 40.500 + 27.500 de extras de cinegrafistas) |
| imposto 16% | 17.360 |
| líquida | 91.140 |
| saídas | 55.400 |
| **lucro** | **35.740 — 32,9%** |

Alimentação no local e hospedagem por conta do Clube do Cowboy. Orçamento de
tabela dava 97.075; fechou em 81.000 (valor 2025 + 8% de inflação) mais os
extras.

### Novela vertical — Movioca (v1, em andamento)

| | |
|---|---|
| entrada bruta | 225.000 (270.000 do orçamento − 45.000 do estúdio, pago direto ao Estúdio São Paulo) |
| imposto 16% | 36.000 |
| líquida | 189.000 |
| montagem e pós | 52.000 |
| equipe técnica | 24.000 (DF 17.000 + cinegrafista 7.000) |
| comissão 15% da líquida | 28.350 |
| finalização · equipamento | 12.000 · 10.500 |
| saídas lançadas | 126.850 |
| **lucro antes das pendências** | **62.150 — 27,6%** |

Montagem dimensionada em 2 meses (equivalente às 7 semanas de pós do orçamento
do cliente). Cinco linhas em branco somando R$ 43.000 de escopo previsto sem
custo definido. Em aberto também: R$ 85.000 de equipe técnica e equipamentos no
orçamento do cliente, dos quais só o DF e um cinegrafista foram lançados.

A comissão entrou depois da primeira versão e derrubou a margem de 43,3% para
27,6% — quase toda a queda vem dela. Comissão não é detalhe de rodapé; num job
de escopo grande é a segunda maior saída depois da equipe.

### Live BYD 23–24.06 (referência histórica)

Entradas 94.790 · despesas 79.548,57 · **lucro 15.241,43 (16,1%)**. Imposto de
15% e comissão de 10%. É o pressuposto que deu origem ao formato.
