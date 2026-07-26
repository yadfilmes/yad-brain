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

## R9 · Fechar os itens sub-especificados da R-N · **2 de 3 feitos**

| item | estado |
|---|---|
| **3** · arestas completas (12 pts) | **fechado na v1.1** — `_meta/arestas-minimas.md`, cobrado pelo `validate.py` |
| **11** · `confidence` coerente (4 pts) | **fechado na v1.2** — `_meta/qa/rubrica-confianca.md`, com piso mecânico |
| **4** · fontes (10 pts) | **aberto** — um binário só para três exigências (fonte oficial, URL que resolve, `loc`) |

**Correção proposta para o item 4:** dividir em parte mecânica (cada grupo de
specs referencia um id de fonte; fonte de comunidade exige permalink) e parte
de julgamento (o valor **como aparece na fonte**, com data `ret`).

**Gate G1, lacuna conhecida:** cobre número **órfão** (sem fonte ao lado); não
cobre número **mal transcrito** — valor certo atribuído ao escopo errado, ou
afirmação atribuída a fonte que não a sustenta. Foram 5 dos 6 defeitos da FX6.
Fechar isso é trabalho de rubrica, não de script: nenhum validador confere
fidelidade sem abrir a fonte.

**Sobre o corte 92 — decidido em 2026-07-26.** A recalibração foi examinada e a
decisão do dono foi **destravar, não recalibrar**: o corte nunca havia sido
testado, porque os itens 3 e 11 somavam 16 pontos inganháveis e o máximo
efetivo era 84. Corte e pesos seguem intactos. A calibração se valida agora
para a frente, num lote real sob a v1.2 — ver S.11 do protocolo.

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
