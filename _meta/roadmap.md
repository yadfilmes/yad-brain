# Roadmap — capacidades planejadas

Decisões já tomadas e desenhadas que **ainda não foram implementadas**.
Existe para que não se percam entre uma sessão e outra.

Diferente de `_meta/gaps.md` (notas que faltam escrever, gerado por script) e
de `_meta/qa/blocked.md` (o que está travado por motivo externo).

---

## R1 · Camada de preços · **prioridade alta**

Diária por equipamento em camada separada (`_precos/`), zona `yad`, com
`data_cotacao` obrigatória e validade de 90 dias.

Desenho completo em `_meta/conventions.md`, seção "Preço".

**Destrava:** orçamento montado pelo cérebro, e a comparação custo × resultado
cruzando com `budget_alternative_to`.
**Ao implementar:** atualizar a Q28 do conjunto-ouro.

---

## R2 · Calculadoras · **as quatro de prioridade alta estão feitas**

Só existe `tools/calc/storage.py`. Ordem de valor por esforço:

| família | uso | estado |
|---|---|---|
| mídia / storage | diário | **feito** |
| parede de LED | gabinetes, portas, potência, peso, shutter × scan × refresh | **feito** |
| elétrica | corrente, circuitos, cabo/queda, gerador, balanceamento de fase | **feito** |
| óptica | FOV, enquadramento, profundidade, hiperfocal, equivalência | **feito** |
| áudio / timecode | conversão 23.976 ↔ 29.97, drift, delay por distância | sob demanda |
| redes | ST 2110, NDI, SRT | adiado até haver job IP |
| RF | **rejeitada como calculadora** — usar Wireless Workbench; o acervo precisa é da nota "RF no Brasil (ANATEL)" | — |

---

## R3 · Passada de verificação de fontes · **DESBLOQUEADA (parcial)**

Descoberto em 2026-07-26 que `WebSearch` funciona neste ambiente, embora
`curl` e `WebFetch` estejam bloqueados. Dá para trocar raiz de domínio por
página específica e preencher `loc` no nível de seção — o defeito que
reprovou 9 de 9 notas.

**Trabalho:** percorrer as 55 notas na ordem de dependência, buscar a página
específica de cada fonte, preencher `loc`, e acrescentar tier não-oficial onde
a nota faz afirmação de prática.

Roteiro: percorrer as notas na ordem de `_meta/gaps.md`, abrir a fonte oficial
de cada uma, registrar página/tabela/seção.

---

## R4 · Domínios ainda não escritos

Ordem sugerida (a de captação e cor já existem):

1. **Iluminação e elétrica** — o maior em volume e o mais usado no dia a dia
2. **Live e broadcast** — espinha de sinal feita (SDI, NDI, M/E, tally, rede); faltam switchers, roteamento e intercom
3. **Produção** — DoP, gaffer, ordem do dia e mapa de luz feitos; faltam demais funções e documentos
4. **Áudio** — microfones, wireless, mixers, timecode
5. **Grip e suporte**
6. **Pós** — softwares, plugins, entrega (DCP/IMF), arquivo (LTO, ASC MHL)

---

## R9 · Fechar os itens sub-especificados da R-N · **prioridade alta**

O item 3 virou mecânico na v1.1 da rubrica (`_meta/arestas-minimas.md`). Ficam
dois, com correção desenhada e **não aplicada** — mexer em régua por conta
própria é o que a meta-regra 8 proíbe.

| item | defeito | correção proposta |
|---|---|---|
| **4** (10 pts) | um binário só para três exigências diferentes (fonte oficial, URL que resolve, `loc`) | dividir: parte mecânica (cada grupo de specs referencia um id de fonte; fonte de comunidade exige permalink) + parte de julgamento (o valor **como aparece na fonte**, com data `ret`) |
| **11** (4 pts) | cobra coerência com uma "rubrica de confiança (fontes × corroboração)" **que não existe no repositório** | escrever a rubrica de confiança em `_meta/qa/`, ou remover o item — hoje ele é inauditável por construção |

**Gate G1, lacuna conhecida:** cobre número **órfão** (sem fonte ao lado); não
cobre número **mal transcrito** — valor certo atribuído ao escopo errado, ou
afirmação atribuída a fonte que não a sustenta. Foram 5 dos 6 defeitos da FX6.
Fechar isso é trabalho de rubrica, não de script: nenhum validador confere
fidelidade sem abrir a fonte.

**Aritmética que o dono precisa ver antes de decidir:** com os pesos atuais e
corte em 92, a perda máxima tolerada é **8 pontos** — o que torna os itens 1, 2,
3 e 4 gates disfarçados (falhar um sozinho já reprova). Ou os pesos se
achatam, ou esses quatro viram gates declarados, ou o corte desce. **As três
saídas são decisão do dono** — ver `2026-07/fx6-esforco-maximo-rn.md`.

---

## R7 · Templates faltantes · **prioridade alta**

`funcao`, `documento` e `interface` estão em produção sem template em
`_meta/templates/`. Pela regra de fechamento do Protocolo 92 (S.3), tipo sem
template não deveria estar em produção — o item 10 da rubrica não tem contra o
que ser medido.

---

## R8 · Calibrar o conjunto-ouro · **prioridade média**

O benchmark deu 45/45 enquanto a rubrica R-N reprovava as mesmas notas com
32–58. Não é contradição: ele mede **recuperação**, e é cego a procedência,
profundidade de grafo e tier de fonte. Avaliar se cabe uma categoria que
exercite isso, ou aceitar explicitamente que são instrumentos de eixos
diferentes.

---

## R5 · Site estático · **fase 3**

Vista derivada publicada (tipo Quartz) com busca e link compartilhável.
Decisão tomada: **privado para o time** primeiro; abertura ou venda depois.
Ver `_meta/conventions.md` para o zoneamento que já prepara isso.

---

## R6 · Tier `campo-proprio` · **decisão do dono pendente**

O tier existe nas convenções, mas nunca foi usado. É a experiência técnica de
set da própria equipe — a fonte de maior valor e menor risco jurídico do
acervo, e o que mais diferencia este cérebro de qualquer documentação pública.

Exige uma exceção explícita à regra de isolamento: experiência técnica
generalizada e anonimizada entra; dado de cliente, contrato e orçamento não.

**Rito sugerido:** post-mortem técnico de 15 minutos ao fim de cada job →
notas novas ou corrigidas.
