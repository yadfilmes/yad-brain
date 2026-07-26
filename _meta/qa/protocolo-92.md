# Protocolo 92 — Metodologia de Autovalidação com Nota de Corte

| | |
|---|---|
| **Versão** | 1.2 — ver histórico em S.11 |
| **Data** | 2026-07-24 (v1.0) · 2026-07-26 (v1.1 e v1.2) |
| **Projeto** | Cérebro Audiovisual (`yadfilmes/yad-brain`) |
| **Regra única** | Nenhum artefato do projeto é aceito com nota computada < 92/100 ou com qualquer item eliminatório reprovado. Abaixo disso: corrigir e re-revisar, até 3 ciclos; sem passar, escala para humano — **nunca** se força a nota. |
| **Destino no repo** | `_meta/qa/protocolo-92.md` (Fase 0 da fundação) |

---

## 0. O problema que este protocolo resolve (e o que ele não finge resolver)

Pedir a uma IA que "dê uma nota" ao próprio trabalho produz teatro: a nota holística gravita para logo acima do corte, porque quem produziu quer aprovar. Este protocolo torna a autovalidação **real** por quatro mecanismos, em ordem de força:

1. **A nota nunca é atribuída — é computada.** Cada tipo de artefato tem uma rubrica de itens binários (passa/não passa) com pesos fixos. Nota = soma dos pesos dos itens aprovados. "Sinto que está 93%" é proibido por construção.
2. **Quem produz nunca pontua.** A revisão roda em **contexto limpo** (agente/passada separada, sem acesso ao raciocínio de produção nem a notas anteriores), com instrução **adversarial**: procurar razões para reprovar; na dúvida, o item reprova.
3. **Máquina antes de julgamento.** Tudo que pode ser verificado mecanicamente (CI, validadores, link check, testes) é verificado por script — script não se convence com prosa bonita.
4. **Itens eliminatórios (gates).** Certas falhas reprovam o artefato inteiro, independentemente da nota — 92 pontos com um número inventado dentro é reprovado, não "quase aprovado".

**O que ele não finge resolver:** autovalidação por IA reduz erro; não o elimina. Por isso o protocolo mantém dois validadores externos permanentes: amostragem humana (S.6) e o benchmark trimestral do projeto (S.3, processos P8–P9 — que mede o sistema inteiro, não artefatos isolados). Se artefatos passam com ≥92 e o benchmark cai, a rubrica está errada — e é a rubrica que se corrige.

---

## 1. O ciclo (aplicado a todo artefato do projeto)

```
PRODUZIR (papel produtor)
   │
   ▼
[1] AUTOCHECAGEM MECÂNICA — CI/validadores/testes/link check
   │  (falhou? corrige antes de gastar revisão — máquina é de graça)
   ▼
[2] REVISÃO INDEPENDENTE — contexto limpo + rubrica + instrução adversarial
   │  entrada: SÓ o artefato + a rubrica + as fontes citadas pelo artefato.
   │  Sem score anterior, sem histórico.
   │  saída: scorecard item a item, com evidência por item reprovado
   ▼
[3] NOTA COMPUTADA + GATES
   │
   ├── nota ≥ 92 E todos os gates OK ──► ACEITO
   │      scorecard arquivado; status avança (draft→reviewed / entregável liberado)
   │
   └── nota < 92 OU gate reprovado ──► CICLO DE CORREÇÃO
          os itens reprovados SÃO o plano de correção (nada além deles é retocado)
          → corrigir → volta ao passo [1]
          → 3 ciclos sem passar? PARA. Registra blocker em _meta/qa/blocked.md,
            status rebaixado, decisão escalada ao humano.
            Aprovar "por cansaço" é violação do protocolo.
```

Semântica da nota: pesos inteiros somados produzem nota inteira de 0–100 — não existe fração nem arredondamento. Aprovação exige **as duas** condições: nota ≥ 92 **e** zero gates reprovados.

---

## 2. Meta-regras anti-manipulação (o coração do protocolo)

1. **Nota computada, nunca declarada.** O revisor entrega a checklist preenchida; a nota sai da soma. Um scorecard sem veredito item a item é inválido.
2. **Contexto limpo obrigatório.** O revisor recebe apenas: o artefato + a rubrica + as fontes citadas. Nunca recebe: a nota anterior, o número de tentativas, ou qualquer texto do produtor defendendo o trabalho.
3. **Instrução adversarial literal.** O prompt do revisor diz: "seu papel é encontrar razões para reprovar cada item; aprove um item somente quando não conseguir refutá-lo; na dúvida, reprove".
4. **Item reprovado exige evidência.** "Item 4: reprovado" não vale; vale "Item 4: reprovado — a spec de latitude (16 stops) não tem fonte na nota". Sem evidência, o scorecard volta.
5. **Gates não se compensam.** Nenhuma soma de pontos salva um artefato com gate reprovado.
6. **Scorecards são arquivados** (`_meta/qa/scorecards/AAAA-MM/…`) — trilha auditável de todas as notas, aprovadas e reprovadas.
7. **A distribuição das notas é monitorada.** O `stats.md` agrega notas por lote. Alarme objetivo (valores iniciais, ajustáveis pelo dono — S.10): **3 lotes consecutivos com média em [92, 94) e desvio-padrão < 2 pontos** é assinatura de manipulação → dispara auditoria humana amostral do lote mais recente.
8. **A rubrica é versionada e muda por PR.** Ninguém "ajusta a régua" dentro de um ciclo de correção: rubrica que valeu no ciclo 1 vale no ciclo 3.
9. **Correção cirúrgica.** No ciclo de correção, mexe-se nos itens reprovados; reescrever o artefato inteiro para "impressionar" o revisor seguinte é desperdício e ruído — e o revisor seguinte continua sem saber que houve ciclo anterior.
10. **Escalar não é falhar.** O desfecho honesto de um artefato que não atinge 92 em 3 ciclos é a fila `blocked.md` com o diagnóstico — não uma quarta tentativa com a régua afrouxada.
11. **Régua defeituosa anula a medição — nunca promove o artefato.** Se um item da rubrica for encontrado *inganhável por construção* (critério inexistente, documento citado que não existe, exigência que o próprio CI reprova), todo ciclo medido com ela é **anulado**: os artefatos voltam ao ciclo 0 e são **re-medidos do zero** com a régua corrigida.
    Três travas para que isto não vire porta dos fundos:
    - anular exige **defeito demonstrável na régua**, registrado no histórico de versões (S.11) — "o revisor foi duro" não é defeito;
    - a anulação **não concede status nenhum**: nada vira `reviewed` por anulação, só volta para a fila de medição;
    - o scorecard anulado **permanece arquivado**, marcado como anulado e com o motivo. Trilha auditável não se apaga.

    A alternativa — insistir em medir com instrumento comprovadamente quebrado, porque foi ele que valeu no ciclo 1 — transformaria a meta-regra 8 numa armadilha: a régua fica imutável **justamente** no caso em que está errada.

---

## 3. Cobertura: todo processo do projeto tem rubrica, revisor e momento

| # | Processo | Rubrica | Revisão mecânica [1] | Revisão independente [2] | Quando roda |
|---|---|---|---|---|---|
| P1 | Nota de conhecimento (equipamento/conceito/função/workflow) | **R-N** | `validate.py` (frontmatter, arestas, slugs, links) | Papel C do pipeline (Verificador), contexto limpo | Antes de `status: reviewed` |
| P2 | Documento de fundação/planejamento (README, AGENTS.md, ontologia, planos, pareceres) | **R-D** | `check_doc.py` (links, estrutura, referências cruzadas) | Agente revisor dedicado | Antes de entregar/commitar |
| P3 | Script/ferramenta (`build_graph.py`, `validate.py`, `tools/calc/*`) | **R-S** | pytest com casos-ouro no CI | Agente revisor lê código + roda casos adversariais | Antes de entrar no CI |
| P4 | Lote da Fase 2 (10–20 notas) | **R-L** | CI do lote inteiro | Papel D (Integrador) + amostragem cruzada | Antes do commit do lote |
| P5 | Índices/MOCs derivados | herdam de P3 | são saída de script testado | — (validados via P3) | A cada geração |
| P6 | Resposta de consulta em operação | **R-R** | — | **exceção declarada** à regra "quem produz nunca pontua": autoavaliação leve por resposta (custo zero); o juiz independente formal de P6 é o benchmark (P9) | Operação contínua |
| P7 | Commit/PR | gate único | CI verde + scorecards dos artefatos anexados | — | Todo commit |
| P8 | Conjunto de perguntas do benchmark + gabaritos (incl. perguntas-canário) | **R-D** (por alteração do conjunto) | script de validação do formato dos gabaritos | Agente revisor dedicado; **canários: validação humana 100%** antes de entrar | A cada alteração do conjunto |
| P9 | Execução trimestral do benchmark | **R-R** aplicada a cada resposta | script de execução/pontuação | relatório de resultados arquivado em `_meta/qa/`; falhas viram backlog | Trimestral e por onda |

Regra de fechamento: **artefato sem rubrica mapeada não existe no projeto** — se um tipo novo de trabalho surgir, o primeiro passo é dar-lhe rubrica (por PR na `_meta/qa/`).

---

## 4. As rubricas

### 4.1 R-N — Nota de conhecimento (100 pts)

**Gates (qualquer um reprovado = artefato reprovado):**
- **G1 · Anti-alucinação:** nenhum número/spec sem fonte rastreável. Lacuna honesta (`<!-- verificar -->`) é aceitável; número órfão, nunca.
- **G2 · CI limpo:** `validate.py` passa (id único, type válido, arestas no vocabulário fechado, slugs referenciados existem).
- **G3 · Procedência:** `sources[]` presente com tier correto (spec numérica exige tier oficial ou lab-test).
- **G4 · Segurança:** se `risco: seguranca` → só fonte oficial/norma, disclaimer fixo presente, marcada para revisão humana 100%.

**Itens pontuados:**

| # | Item (binário) | Peso |
|---|---|---|
| 1 | TL;DR na 1ª linha do corpo, auto-suficiente (responde "o que é e por que importa" sem abrir o resto) | 15 |
| 2 | Specs em linhas `chave: valor` greppáveis; **toda spec condicional carrega as condições na mesma linha** (claim-lite) | 15 |
| 3 | Arestas completas e específicas para o tipo de nó — **conjunto mínimo fechado em `_meta/arestas-minimas.md`**, cobrado pelo `validate.py`. O revisor confere o veredito da máquina, não recria o critério | 12 |
| 4 | Fontes: ≥1 oficial para specs; URLs resolvem; `loc` quando a fonte é documento paginado | 10 |
| 5 | Aliases completos (grafias com/sem acento, códigos de modelo, termo EN) | 8 |
| 6 | Posicionamento presente (contra quem compete, para quem faz sentido) — ficha técnica sozinha não é conhecimento | 8 |
| 7 | Dicas de comunidade parafraseadas, citadas com tier, **sem handles** (LGPD), sem colagem | 8 |
| 8 | Gotchas reais quando o item notoriamente os tem (VND barato sem "cruz" reprova) | 6 |
| 9 | Atômica e na faixa de tamanho (300–1.200 tokens) | 6 |
| 10 | Slug ASCII correto, pasta certa, template respeitado | 5 |
| 11 | `confidence` coerente com **`_meta/qa/rubrica-confianca.md`** (fontes × corroboração). Declarar mais conservador que a tabela passa; mais otimista reprova | 4 |
| 12 | `updated` e `status` corretos | 3 |

### 4.2 R-D — Documento de fundação/planejamento (100 pts)

**Gates:** **G1** nenhuma afirmação factual inventada (número, nome de produto, capacidade) sem fonte ou rótulo explícito de estimativa; **G2** auto-contido (um leitor sem acesso à conversa entende e consegue agir); **G3** toda decisão relevante tem justificativa (nenhum "porque sim").

| # | Item | Peso |
|---|---|---|
| 1 | Completude contra o escopo que o próprio documento declara (seção prometida e ausente reprova) | 20 |
| 2 | Consistência interna (nenhuma seção contradiz outra; números batem entre seções) | 15 |
| 3 | Acionabilidade: cada seção normativa produz saída concreta (regra, artefato, critério) — não opinião solta | 15 |
| 4 | Critérios de aceite/números onde o documento os promete (alvos, KPIs, limiares) | 10 |
| 5 | Riscos identificados com mitigação específica (mitigação genérica "ter cuidado" reprova) | 10 |
| 6 | Rastreabilidade: afirmações de pesquisa apontam fonte/origem | 10 |
| 7 | Clareza estrutural: um leitor acha qualquer regra em <1 min (títulos, tabelas, numeração) | 10 |
| 8 | Decisões em aberto explicitadas com recomendação (nunca escondidas) | 10 |

### 4.3 R-S — Script/ferramenta (100 pts)

**Gates:** **G1** roda sem erro no repo real; **G2** determinístico (mesmo input → mesmo output, sem rede/clock); **G3** nunca edita fonte canônica (só gera derivados `_index/`, `_graph/`); **G4** calculadora imprime disclaimer quando de domínio de risco (elétrica).

| # | Item | Peso |
|---|---|---|
| 1 | Testes com casos-ouro passando (valores conferidos contra fonte externa) | 25 |
| 2 | Casos de borda cobertos: acento/Unicode, frontmatter malformado, link quebrado, arquivo vazio | 20 |
| 3 | Saída legível e acionável (erro diz o arquivo e a linha; relatório é markdown utilizável) | 15 |
| 4 | Idempotente (rodar 2× não duplica nem corrompe) | 10 |
| 5 | Rápido o suficiente para rodar em todo commit (< ~30 s no acervo-alvo: ~2.400 notas no Apêndice B do Plano, ~2.600 após as absorções do Parecer, S.7 item 38) | 10 |
| 6 | Documentado no cabeçalho (o que faz, como rodar, o que NÃO faz) | 10 |
| 7 | Integrado ao CI | 10 |

### 4.4 R-L — Lote da Fase 2 (100 pts)

**Gates:** **G1** 100% das notas do lote individualmente aprovadas (R-N ≥92); **G2** CI verde no lote; **G3** nenhuma spec rejeitada pelo Verificador permanece no texto.

| # | Item | Peso |
|---|---|---|
| 1 | Consistência entre notas irmãs (mesmos campos preenchidos; mesma profundidade; COBs da mesma família comparáveis entre si) | 25 |
| 2 | Reciprocidade/simetria de arestas (A `competes_with` B ⇒ B `competes_with` A; direcionais sem duplicata invertida) | 20 |
| 3 | Amostragem cruzada: 2 notas do lote re-verificadas do zero contra a fonte primária, sem divergência | 20 |
| 4 | MOCs e índices do domínio atualizados com o lote | 20 |
| 5 | Dedup de aliases contra o acervo inteiro (nenhum alias aponta para 2 slugs) | 15 |

### 4.5 R-R — Resposta de consulta em operação (100 pts)

Aplicada por autoavaliação leve ao fim de cada resposta do cérebro (checklist mental de 5 itens, custo ~zero) e, formalmente, pelo benchmark trimestral:

| # | Item | Peso |
|---|---|---|
| 1 | Fontes citadas com tier (oficial vs comunidade explícito) | 30 |
| 2 | Escopo/condições respeitados (não cita "120fps" sem as condições que a nota registra) | 25 |
| 3 | Abstenção correta: acervo não cobre → diz "não tenho evidência suficiente" e registra a lacuna | 20 |
| 4 | Conflito exposto quando a nota registra um | 15 |
| 5 | Custo dentro do alvo (≤3 arquivos na consulta típica) | 10 |

---

## 5. O scorecard (formato único, arquivável, agregável)

```yaml
# _meta/qa/scorecards/2026-08/luz--aputure-ls-600d-pro--c1.yaml
artefato: luz/fixtures/aputure/ls-600d-pro.md
tipo: R-N
ciclo: 1                      # 1..3
data: 2026-08-14
revisor: verificador-lote-07  # agente/contexto, nunca o produtor
gates:
  G1-anti-alucinacao: pass
  G2-ci: pass
  G3-procedencia: pass
  G4-seguranca: n/a
itens:
  - {id: 1, peso: 15, veredito: pass}
  - {id: 2, peso: 15, veredito: fail,
     evidencia: "output_lux_at_3m sem condição de refletor/ótica na linha"}
  - {id: 3, peso: 12, veredito: pass}
  # ... todos os 12, sem exceção
nota: 85
resultado: reprovado          # => ciclo de correção com os itens 'fail'
```

O campo `ciclo` é preenchido **pelo orquestrador, depois que a revisão retorna** — o revisor nunca vê nem informa o número da tentativa (meta-regra 2).

O `build_graph.py` agrega os scorecards no `stats.md`: notas médias por lote, taxa de reprovação por item (qual item mais reprova = onde o processo de produção precisa melhorar) e o alarme de distribuição (meta-regra 7).

---

## 6. Calibração — quem valida o validador

1. **Amostragem humana:** 10% dos artefatos aprovados de cada lote inicial são conferidos por olho humano. Divergência humano×scorecard → a **rubrica** é corrigida por PR (não o caso individual). Gatilho de relaxamento (valores iniciais, ajustáveis pelo dono — S.10): **divergência < 10% por 3 lotes consecutivos → próximo degrau (10% → 5% → 2%)**; qualquer divergência grave (gate que o humano reprovaria) volta ao degrau anterior.
2. **Benchmark trimestral como juiz externo:** artefatos passando com ≥92 + benchmark caindo = rubrica medindo a coisa errada. O benchmark manda; a rubrica obedece.
3. **Perguntas-canário** (do parecer): casos no benchmark cuja resposta correta no acervo contraria o "prior" típico de LLM — medem se o sistema responde com o acervo ou com memória. Falha de canário é falha de sistema, investigada fora do ciclo normal.
4. **Limite honesto declarado:** revisor-IA compartilha vieses com produtor-IA (mesma família de modelo). O protocolo mitiga com decomposição binária + evidência obrigatória + gates mecânicos + os juízes externos acima. Reduz erro; não o zera. Por isso segurança (`G4`) nunca dispensa humano.

---

## 7. Demonstração 1 (retroativa) — o Plano v1.0 sob a R-D

Artefatos referenciados (a arquivar em `_meta/history/` na Fase 0 — ver S.9.1):
- **Plano v1.0** = `plano-cerebro-audiovisual-v1.md` (2026-07-23), o plano de projeto do Cérebro Audiovisual.
- **Parecer** = `parecer-cruzado-v1.md` (2026-07-23), revisão do Plano v1.0 por 4 frentes independentes de agentes + confronto com o "Plano Mestre" do ChatGPT (documento fornecido pelo dono do projeto em 2026-07-23).

O Parecer foi, na prática, a primeira execução do passo [2] deste protocolo — antes de ele ter nome. Pontuando o Plano v1.0 com a R-D (vereditos estritamente binários), com os achados do Parecer como evidência:

| Item | Peso | Veredito | Evidência (seção do Parecer) |
|---|---|---|---|
| 1 Completude | 20 | **fail** | Domínio de segurança/normas ausente; calculadoras ausentes; troubleshooting sem estrutura; arquivo/entrega ausentes (Parecer S.7, itens 29–32) |
| 2 Consistência | 15 | pass | Nenhuma contradição interna apontada pelas 4 frentes |
| 3 Acionabilidade | 15 | pass | Templates e critérios concretos prontos para uso |
| 4 Critérios/números | 10 | pass | Alvos de token, KPIs, aceites por fase |
| 5 Riscos c/ mitigação | 10 | **fail** | Sem risco jurídico BR (LGPD/9.610) e sem orçamento financeiro da construção (Parecer S.9, itens 7 e 12) |
| 6 Rastreabilidade | 10 | **fail** | "Fair use" citado como base legal — doutrina inaplicável a empresa brasileira (Parecer S.9, item 7) |
| 7 Clareza | 10 | pass | Estrutura numerada, tabelas, regras localizáveis |
| 8 Decisões em aberto | 10 | pass | D1–D6 explicitadas com recomendação |

**Gates:** G1 pass · G2 pass · G3 pass.
**Nota (computada): 15+15+10+10+10 = 60. Resultado: REPROVADO.**

É exatamente o que o protocolo deve fazer: a v1.0 parecia excelente a quem a escreveu; a revisão independente achou o que a satisfação própria não acha. As ~40 absorções do Parecer **são** o plano de correção do ciclo 2 — a v1.1 será submetida à mesma rubrica quando consolidada, e só avança se fizer ≥92.

*(Nota metodológica: a v1.0 foi pontuada com a régua de hoje, que inclui conhecimento produzido pela própria revisão — é o comportamento desejado: a régua evolui por PR e vale para tudo que ainda não foi aceito.)*

---

## 8. Demonstração 2 (ao vivo) — este documento sob a própria régua

Este documento foi submetido, antes da entrega, a um revisor independente em contexto limpo (agente separado, instrução adversarial, com o artefato + a R-D + as fontes citadas pelo artefato — Plano v1.0 e Parecer — em mãos), conforme o passo [2]. O scorecard real desta entrega:

**Histórico real dos ciclos** (cada revisor em contexto limpo, sem conhecimento dos ciclos anteriores; mesma rubrica do primeiro ao último — meta-regra 8):

| Ciclo | Nota | Gates | Resultado | Itens reprovados (evidência resumida) |
|---|---|---|---|---|
| 1 | 35 | 3/3 pass | reprovado | **1** benchmark/canários fora da tabela de processos, violando a própria regra de fechamento; **2** demo com crédito parcial ("12/20") e nota-intervalo ("62–70") violando o binário, entradas da revisão divergentes entre seções, ponteiro de seção errado, campo `ciclo` vazando a tentativa ao revisor; **4** alarme de distribuição e relaxamento da amostragem sem números; **6** Parecer/Plano citados sem localizador; **8** decisões em aberto escondidas (sem seção própria) |
| 2 | 75 | 3/3 pass | reprovado | **2** S.8 omitia as "fontes citadas" na descrição da entrada da revisão (divergindo de S.1/S.2.2); **6** "~2.500 arquivos" atribuído ao Apêndice B do Plano, que diz ~2.400 (conferido na fonte, linha a linha), e localizador "itens 29–33" onde os corretos eram 29–32 |
| 3 | **100** | 3/3 pass | **APROVADO** | — |

Scorecard final:

```yaml
artefato: protocolo-92.md
tipo: R-D
ciclo: 3
data: 2026-07-24
revisor: agente-independente-3 (contexto limpo, instrução adversarial;
         verificação numérica integral — 5 somas de pesos recomputadas,
         2 notas de demonstração recomputadas, 9 localizadores conferidos
         contra os arquivos-fonte)
gates: {G1: pass, G2: pass, G3: pass}
itens: 8/8 pass (20+15+15+10+10+10+10+10)
nota: 100
resultado: APROVADO
```

**Ressalvas não-bloqueantes registradas pelo revisor do ciclo 3** (entram no próximo PR da rubrica, que passará pelo seu próprio ciclo R-D): (1) o teto de 3 ciclos merece virar Q4 na S.10, como valor ajustável do dono; (2) preferir a notação "Parecer S.7:38" à "S.7 item 38" para não colidir com as referências internas; (3) o cabeçalho do script do alarme deve fixar quais scorecards entram na média (todos os ciclos ou só o final); (4) o plano do ChatGPT é a única fonte citada não verificável em arquivo — o arquivamento em `_meta/history/` (S.9.1) resolve.

O que este histórico demonstra: a régua não afrouxou entre ciclos, a nota subiu porque o artefato melhorou, e os defeitos eram reais — incluindo um número citado errado contra a fonte, exatamente a classe de erro que o projeto mais teme.

---

## 9. Integração com o Plano v1.1 (mudanças que este protocolo adiciona)

1. `_meta/qa/` entra na Fase 0: `protocolo-92.md`, rubricas, `scorecards/`, `blocked.md` — e `_meta/history/` com os artefatos de origem do projeto (`plano-cerebro-audiovisual-v1.md`, `parecer-cruzado-v1.md`, plano do ChatGPT), para que toda referência deste documento seja verificável dentro do repo.
2. O pipeline da Fase 2 ganha a formalização: papel C (Verificador) **emite scorecard R-N** por nota; papel D (Integrador) **emite scorecard R-L** por lote; `status: reviewed` passa a significar "R-N ≥ 92 + gates OK, scorecard arquivado".
3. `AGENTS.md` ganha duas linhas: o contrato de resposta (R-R) e a regra "nenhum artefato avança sem scorecard".
4. CI ganha: agregação de scorecards no `stats.md` + alarme de distribuição (valores da S.2.7) + criação do `check_doc.py` (revisão mecânica de P2: links, estrutura, referências cruzadas).
5. KPI novo no quadro do projeto: **KPI 10 — Integridade do QA**: 100% dos artefatos `reviewed` com scorecard arquivado; divergência humano×scorecard < 10% na amostragem.
6. Decisão registrada: o corte é **92** por escolha do dono do projeto; a rubrica pode evoluir, o corte só muda por decisão dele.

---

## 10. Decisões em aberto (do dono do projeto, com recomendação)

| # | Decisão | Recomendação |
|---|---|---|
| Q1 | **Governança do benchmark e das perguntas-canário** — quem valida o juiz que "manda" (S.6.2)? | Alterações do conjunto passam por R-D (processo P8); **canários só entram com validação humana 100%**, porque são o único instrumento que mede o sistema contra a memória do próprio modelo — não podem ser autorados e aprovados pela mesma IA sem olho humano. |
| Q2 | **Valores do alarme de distribuição** (S.2.7) | Iniciar com: 3 lotes consecutivos, média em [92, 94), desvio-padrão < 2. Revisar após os 5 primeiros lotes reais — valores são calibração, não dogma. |
| Q3 | **Gatilho de relaxamento da amostragem humana** (S.6.1) | Iniciar com: divergência < 10% por 3 lotes consecutivos → próximo degrau; divergência grave (gate) → degrau anterior. Segurança (`G4`) nunca relaxa. |

Cada valor acima está aplicado no texto como padrão inicial; alterá-los é prerrogativa do dono e se faz por PR na rubrica (meta-regra 8).

---

## 11. Histórico de versões da rubrica

A meta-regra 8 exige que a régua seja versionada e mude por PR, nunca dentro de
um ciclo de correção. Este é o registro.

### v1.2 — 2026-07-26 · a recalibração que não mexeu no corte

**A descoberta que mudou a pergunta.** Ao preparar a recalibração do corte 92,
a aritmética mostrou que **o corte nunca foi o gargalo**:

| item | peso | por que era inganhável |
|---|---:|---|
| 3 · arestas completas | 12 | critério não existia — julgamento do revisor a cada rodada (fechado na v1.1) |
| 11 · `confidence` coerente | 4 | a "rubrica de confiança" que ele cita **não existia no repositório** |

Dois itens inauditáveis somam **16 pontos inganháveis ⇒ máximo efetivo 84**,
contra um corte de 92. **Nenhuma nota podia passar, por melhor que fosse.** É a
explicação completa de 0 aprovadas em 11 avaliadas, sem precisar culpar as
notas: a melhor delas (`aces`, 70) perdeu apenas 14 pontos além dos
inganháveis.

**Decisão do dono: destravar, não recalibrar.** Corte 92 e os 12 pesos seguem
**exatamente como estavam**. O que muda é que o item 11 passou a ter documento:
`_meta/qa/rubrica-confianca.md`, com tabela determinística de `confidence` em
função de fontes × corroboração, piso mecânico no `validate.py` e os limites do
piso escritos na própria rubrica.

Com os dois itens fechados, o **máximo efetivo volta a 100** e o 92 passa a
significar o que sempre pretendeu: *uma nota `reviewed` tolera no máximo um
deslize moderado.* Pela primeira vez isso é uma afirmação testável.

**Efeito imediato:** 31 das 63 notas declaravam `confidence` acima do que suas
fontes sustentam — metade do acervo, invisível porque não havia régua. Todas
corrigidas para o valor honesto. O caminho de volta para `alta` é acrescentar
fonte independente com `loc`, que é o trabalho de R3.

**Ainda em aberto (R9):** o item 4 continua juntando três exigências num
binário só. E o gate G1 segue cobrindo número **órfão**, não número **mal
transcrito** — foram 5 dos 6 defeitos da FX6, e fechar isso é trabalho de
rubrica, não de script.

**Próximo passo obrigatório:** um lote real sob a v1.2. Se ainda assim nada
passar, aí sim a discussão é de calibração — e com dado, não com aritmética.

### v1.1 — 2026-07-26

**Origem:** três lotes e dois experimentos com **0 de 10 aprovadas**. O
scorecard `2026-07/fx6-esforco-maximo-rn.md` mostrou que uma nota escrita com
esforço máximo de pesquisa ainda reprova — e que parte do problema é a régua
ter itens que ninguém consegue auditar.

**Mudança única:** o **item 3 da R-N** deixou de ser julgamento e passou a
apontar para `_meta/arestas-minimas.md`, um conjunto mínimo fechado por `type`
que o `validate.py` cobra (aviso em `draft`, erro em `reviewed`).

Por que isto **não** é afrouxar a régua:

- O **peso continua 12** e a nota de corte continua **92**.
- A exigência não mudou de conteúdo — mudou de *modo de verificação*: de
  julgamento não-reprodutível para check determinístico. Um revisor complacente
  agora não consegue aprovar o item; a máquina já reprovou.
- O produtor passa a conseguir **conferir antes de gastar revisão**, que era o
  desperdício apontado no lote 03.

**O que deliberadamente NÃO mudou:**

| | |
|---|---|
| nota de corte 92 | **decisão do dono** — não se toca sem ele |
| pesos dos 12 itens | idem |
| itens 4 e 11 | conhecidamente sub-especificados; correção proposta está no `_meta/roadmap.md`, não aplicada por conta própria |
| gate G1 | segue cobrindo número órfão; **não** cobre número mal transcrito — a lacuna está registrada, não fechada |

**Efeito medido no acervo:** 162 → 216 avisos. Os 54 novos são dívida que já
existia e era invisível; nenhuma nota mudou de status por conta desta versão.

