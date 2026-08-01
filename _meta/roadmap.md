# Roadmap — onde o projeto está e o que falta

Atualizado em **2026-07-26**.

Decisões tomadas e desenhadas que **ainda não foram implementadas**, mais o
estado real de cada frente. Diferente de `_meta/gaps.md` (notas que faltam
escrever, gerado por script), de `_meta/fila-verificacao.md` (fontes a conferir,
gerado por script) e de `_meta/qa/blocked.md` (o que está travado por motivo
externo).

---

## Onde estamos, em uma tabela

| fase do plano v1.0 | alvo | estado |
|---|---|---|
| **0 · Fundação** | README, AGENTS, convenções, vocabulário, templates, CI | **feito** |
| **1 · Esqueleto + exemplares** | árvore, vocab, 8–12 notas, `validate.py` | **feito** (75 notas) |
| **2 · Conteúdo** | **~1.700 a 2.300 notas** | **75 → ~4%** ← *o gargalo real* |
| **3 · Grafo e índices** | `build_graph`, backlinks, órfãos, CI | **feito** |
| **4 · Otimização de acesso** | benchmark + skill empacotada | **~50%** — benchmark roda, skill não |
| **5 · Operação contínua** | rotina mensal, expansão sob demanda | não iniciada |

**A fábrica está pronta; o galpão está com 4% da carga.** A infraestrutura de
qualidade ficou desproporcional ao acervo — o que é custo fixo que amortiza,
mas explica a sensação de que o projeto anda devagar.

---

## O gargalo, nomeado

**Nenhuma nota pode chegar a `reviewed` neste ambiente.** O gate G3 do
Protocolo 92 exige fonte `oficial`/`lab` com transcrição verificada; o egresso
HTTP está bloqueado por política do ambiente (ver `blocked.md`, B1). Foi por
isso que **14 notas avaliadas em 5 lotes deram 0 aprovadas** — e não por rigor
excessivo da régua.

Enquanto isso, o acervo é **utilizável em `draft`**: o `AGENTS.md` obriga toda
resposta a declarar confiança, e as notas dizem o que não foi conferido.

---

## R3 · Passada de verificação de fontes · **PRÓXIMO PASSO**

**63 fontes** `oficial`/`lab` sem `cit`, em **55 notas**, de 21 organizações.

- Fila pronta: `_meta/fila-verificacao.md` (regenerar com
  `python3 tools/fila_verificacao.py`)
- Roteiro da sessão: `_meta/sessao-com-rede.md`
- Ordem: segurança primeiro, depois ARRI/Sony/Blackmagic (36 das 63)

**Destrava:** o gate G3, e com ele a possibilidade de qualquer nota alcançar
`reviewed` pela primeira vez.

---

## R4 · Domínios de conteúdo · **em andamento**

| domínio | estado |
|---|---|
| captação (câmeras, mídia, mounts, codecs) | espinha feita — 5 câmeras, 4 codecs, 7 nós de vocabulário |
| cor e pipeline | espinha feita — ACES, Rec.709, curvas, gamuts |
| live e broadcast | espinha feita — SDI, NDI, M/E, tally, rede |
| **elétrica** | **aberto** — rede AC, bitola, gerador, balanceamento, NR-10 |
| luz | parcial — 2 fixtures, 3 conceitos, HMI, 2 mounts |
| LED/VP | parcial — scan rate, PWM, flicker |
| produção | parcial — DoP, gaffer, ordem do dia, mapa de luz |
| **áudio** | **iniciado** — timecode, RF/ANATEL |
| grip e suporte | não iniciado |
| pós (softwares, plugins, entrega, arquivo) | não iniciado |

---

## R1 · Camada de preços · **prioridade alta, não iniciada**

Diária por equipamento em camada separada (`_precos/`), zona `yad`, com
`data_cotacao` obrigatória e validade de 90 dias. Desenho completo em
`conventions.md`, seção "Preço".

**Destrava:** orçamento montado pelo cérebro, e a comparação custo × resultado
cruzando com `budget_alternative_to`.
**Ao implementar:** atualizar a Q28 do conjunto-ouro.

---

## R6 · Tier `campo-proprio` · **decisão do dono pendente**

O tier existe nas convenções e **nunca foi usado**. É a experiência técnica de
set da própria equipe — a fonte de maior valor e menor risco jurídico do
acervo, e a única que nenhum concorrente pode copiar.

**Por que virou urgente:** a régua v1.3 expôs **45 avisos** de "prática sem
fonte de campo" — todas notas com `## Gotchas` sustentadas por documentação de
fabricante. É exatamente o buraco que este tier preenche.

**Rito sugerido:** post-mortem técnico de 15 min ao fim de cada job → notas
novas ou corrigidas.

---

## R9 · Itens da R-N · **2 de 3 fechados**

| item | estado |
|---|---|
| 3 · arestas completas | **fechado (v1.1)** — `_meta/arestas-minimas.md` |
| 11 · `confidence` coerente | **fechado (v1.2)** — `_meta/qa/rubrica-confianca.md` |
| 4 · fontes | **fechado (v1.3)** — virou rastreabilidade; tier forte ficou só no G3 |

**Ainda aberto — gate G1:** cobre número **órfão**, não número **mal
transcrito**. Foram 8 de 9 defeitos de G1 em duas rodadas. É trabalho de
rubrica, não de script: nenhum validador confere fidelidade sem abrir a fonte.
A regra da transcrição (`cit`) ataca a causa; falta medir se resolveu.

---

## R2 · Calculadoras · **as quatro de prioridade alta feitas**

| família | estado |
|---|---|
| mídia / storage · parede de LED · elétrica · óptica | **feitas**, 88 testes no CI |
| áudio / timecode (conversão, drift, delay) | sob demanda |
| redes (ST 2110, NDI, SRT) | adiado até haver job IP |
| RF | **rejeitada** — virou a nota `audio/rf-anatel` |

**Novo:** `_meta/constantes-de-calculo.md` registra o estado de cada constante
(fonte verificada · premissa declarada · norma não aberta). Premissa não vira
fato por ser reproduzível.

---

## R7 · Templates faltantes · **prioridade média**

`funcao`, `documento` e `interface` estão em produção sem template. Pela regra
de fechamento do Protocolo 92 (S.3), tipo sem template não deveria estar em
produção.

---

## R8 · Calibrar o conjunto-ouro · **prioridade média**

O benchmark dá nota cheia enquanto a R-N reprova as mesmas notas. Não é
contradição — ele mede **recuperação** e é cego a procedência e profundidade de
grafo. Avaliar se cabe categoria que exercite isso, ou aceitar explicitamente
que são instrumentos de eixos diferentes.

---

## R5 · Site estático · **fase 3, não iniciada**

Vista derivada publicada (tipo Quartz) com busca e link compartilhável.
Decisão tomada: **privado para o time** primeiro; abertura ou venda depois.
O zoneamento `universal`/`yad` já prepara isso a custo zero.
