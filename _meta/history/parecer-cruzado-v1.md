# Parecer — Revisão Cruzada dos Dois Planos do Cérebro Audiovisual

| | |
|---|---|
| **Objeto** | "Plano Mestre" (ChatGPT, 2.893 linhas) × "Plano v1.0" (Claude, ~940 linhas) |
| **Data** | 2026-07-23 |
| **Método** | Leitura integral dos dois documentos + 4 frentes de revisão especializadas e independentes: **A** Recuperação/Stack · **B** Modelo de Conhecimento · **C** Ingestão/Fontes/Jurídico · **D** Escopo/Benchmark/Roadmap/Operação |
| **Premissa de julgamento** | Equipe de 1–2 pessoas, sem engenheiro dedicado; consumidor primário = Claude (Grep/Glob/Read nativos); repo privado; a mão de obra escassa é a mesma que precisa curar conteúdo — cada hora de operação de infra é hora roubada da curadoria, que é o produto real |
| **Autor** | Claude (Fable 5), autor do Plano v1.0 — parecer escrito para devolução ao ChatGPT |

---

## 1. Veredito executivo

**Sobre o plano ChatGPT: aprovar a doutrina, redesenhar a execução.**

O documento é intelectualmente excelente — o melhor catálogo de *rigor epistemológico* que este projeto poderia receber. Seus princípios (§5), sua disciplina de escopo de afirmação (§3), sua taxonomia de falsos conflitos (§8.5) e sua política de fontes (§14) estão certos e foram **absorvidos**. Mas sua execução descreve a plataforma de conhecimento de uma empresa com time de engenharia de dados — cofre de evidências, RAGFlow, Qdrant, Neo4j/Graphiti, Graphify, gateway MCP com 9 ferramentas, pipeline de 14 etapas, benchmark de 11 sistemas com 19 métricas — para um operador de 1–2 pessoas. A instrução final do próprio documento (§28) pede para sair da avaliação com *"uma arquitetura menor, mais confiável e mais demonstrável — não uma lista maior de ferramentas"*. Levada a sério, essa instrução elimina a maior parte da pilha proposta.

**A arquitetura unificada que este parecer recomenda:** o chassis do Plano Claude (repositório Git/Markdown grep-first, nota atômica = única representação, grafo derivado deterministicamente, zero infra permanente) **+ os módulos de rigor do Plano ChatGPT importados como convenções e scripts, não como servidores**. O resultado das 4 frentes é uma lista de ~40 absorções concretas (Seção 7) que produzem a v1.1 do Plano Claude — significativamente melhor que a v1.0 por causa do plano ChatGPT. O cruzamento funcionou.

---

## 2. As 5 melhores decisões do plano ChatGPT

1. **Disciplina de escopo condicional** (§3): "a câmera grava 120 fps" não é uma afirmação — falta resolução, crop, codec, bit depth, mídia, firmware. É a melhor lição editorial do documento. Absorvida como regra ("spec condicional não entra sem suas condições na mesma linha") + seção `## Modos de gravação` em notas de câmera — a linha da tabela **é** o claim escopado, sem schema.
2. **Taxonomia de falsos conflitos** (§8.5): latitude declarada × medida com critério de SNR; "full frame coverage" sem diagonal; refresh sem scan/PWM/shutter; suporte oficial × workaround. Vira o guia de instrução do papel Verificador do pipeline.
3. **Calculadoras determinísticas** (§11): "fórmulas não devem ser resolvidas por memória textual" está simplesmente correto — aritmética encadeada é onde LLM erra silencioso. O Plano Claude não tinha nada disso; era sua lacuna mais injustificável, porque a correção é barata (scripts Python no repo, testados em CI).
4. **Abstenção como critério mensurável** (§20.1, §26): perguntas cujo gabarito é "o acervo não cobre — diga isso". Sem elas, a regra "não invente números" é fé, não métrica. Entra no benchmark como categoria + KPI próprio.
5. **Arestas negativas e de diagnóstico** (§8.2): `INCOMPATIBLE_WITH`/`LIMITED_BY` (incompatibilidade *conhecida* é conteúdo de altíssimo valor num banco de compatibilidade) e `CAUSES`/`RESOLVED_BY` (sem elas, "LED flicka na câmera, por quê?" — a consulta de maior valor em set — não é respondível por travessia). O vocabulário do Plano Claude não as tinha.

**Menções honrosas:** o conceito do Evidence Pack (absorvido como *contrato de resposta*, não como servidor); a captura da biblioteca SMPTE gratuita de 2026; o registro de patrocínio/equipamento cedido em reviews; a priorização firmware-first do monitoramento; o critério de saída da Fase 0 ("pilotos representáveis sem exceções estruturais graves").

---

## 3. Os 5 maiores riscos do plano ChatGPT

1. **Nunca entrega.** Infra primeiro, conteúdo depois: 8 fases, das quais as 5 primeiras produzem plataforma e piloto, não acervo. Com 1–2 pessoas, a probabilidade de chegar à Fase 8 (expansão de conteúdo) é baixa; o modo de morte mais provável do projeto é uma pilha semi-configurada e 50 notas.
2. **Múltiplas fontes de verdade dessincronizadas.** Os dados vivem em até cinco lugares (cofre, repo canônico, claims/cápsulas, índices vetoriais, grafos) — a Fase 7 inteira existe para administrar a defasagem entre eles. O modo de falha resultante é o pior que existe: **resposta errada por índice defasado, dita com confiança e com citação** — falha silenciosa. (O pior caso do grep-first é uma resposta lenta.)
3. **Fricção editorial mata a produção.** Claim de ~30 campos × confiança em 10 dimensões × duas máquinas de estado sobrepostas (12 estados editoriais + 11 temporais, sem transições definidas) = ou ninguém preenche, ou um LLM preenche mecanicamente — gerando pseudo-precisão pior que um rótulo grosso honesto.
4. **Benchmark-paralisia.** Subir e tunar honestamente 9–11 sistemas de recuperação, com adaptadores, 150–300 perguntas e 19 métricas, é um projeto de laboratório de semanas–meses full-time — consumindo o projeto real. E o resultado é quase predeterminado: o próprio §10.1 do documento antecipa a resposta por classe de pergunta.
5. **Aposta em infraestrutura jovem no caminho crítico, com custo fixo sem ganho.** O gateway MCP custa ~1,5–3,5k tokens de schema por sessão contra ~100–700 do protocolo em arquivo; o Evidence Pack alvo (1.500–3.000 tokens) não é mais barato que a nota atômica lida direto (600–2.500). E RAGFlow/Graphify — projetos de evolução rápida, com riscos que o próprio documento lista com franqueza (§7.5–7.6) — ficariam entre o conhecimento e o consumidor.

---

## 4. Respostas às 15 perguntas do documento (§1)

1. **A arquitetura em camadas é adequada ou existe solução mais simples?** Existe: o repositório *é* o banco; Grep/Glob/Read do consumidor são o motor; as camadas propostas viram convenções (contrato de resposta, escopo condicional) + 2 scripts derivados (projeção tabular CSV, consultas de caminho sobre `graph.json`). Mesma qualidade epistemológica, ~zero infra.
2. **Graphify tem o papel correto?** Não — deveria ter *menos*: um LLM re-extraindo probabilisticamente relações de um conteúdo curado que já as declara em vocabulário fechado é ruído a jusante da curadoria, e quebra o próprio critério de regressão do documento (re-execuções divergem). Papel máximo defensável: minerador offline de *arestas candidatas* sobre fontes cruas, durante a redação. Nunca no caminho de consulta.
3. **RAGFlow é o melhor motor intermediário para o piloto?** Nenhum motor intermediário: o piloto correto é repo + Claude direto. Docling entra — como ferramenta de *redação* (extrair tabelas/pinagens de manuais na ingestão), jamais de consulta. Qdrant/Neo4j/Weaviate/OpenSearch/LlamaIndex/LightRAG: rejeitados para este caso (Seção 8).
4. **Obsidian + Git + Markdown é fonte canônica sustentável por anos?** Sim — é o único ponto em que os dois planos concordam integralmente, e é a fundação inteira do plano rival. Texto puro versionado é o formato mais durável e portátil que existe.
5. **O modelo de afirmações atômicas é suficientemente rigoroso?** É rigoroso *demais na forma* e certo na doutrina. Adotar a doutrina (escopo, locator, declarado/medido/relatado, conflito preservado) como regra editorial dentro da nota; rejeitar o claim-store JSONL como unidade de armazenamento.
6. **O que está excessivamente complexo para a primeira fase?** Cofre completo com adjudicação de licença por item; pipeline de 14 etapas com dedup SimHash/MinHash; Zotero; claim-store; 10 dimensões de confiança; 23 estados; benchmark de 11 sistemas; gateway MCP; Qdrant+Neo4j+Graphiti+RAGFlow+Graphify.
7. **O que está simplificado demais para um projeto enciclopédico?** No plano ChatGPT: volume (nenhuma estimativa de notas/esforço/custo), atualidade de mercado (listas de marcas menores e menos atuais que o Apêndice A rival) e o operador (nenhum dimensionamento de quem executa). No plano Claude (corrigido nesta revisão): segurança/normas, troubleshooting, calculadoras, arquivo/entrega.
8. **A estratégia de baixo consumo de tokens está correta?** A direção sim, o mecanismo não: a economia real vem de engenharia do conteúdo (nota atômica, TL;DR, linhas auto-suficientes, slugs previsíveis, índices pré-computados), não de um gateway que adiciona custo fixo de schema e não fica abaixo do custo da leitura direta.
9. **Como melhorar a ingestão de manuais com tabelas, diagramas, pinagens?** Docling/MinerU como ferramenta do papel Pesquisador quando a fase de conteúdo encostar em PDFs; o destino é sempre a nota destilada (tabela de modos, pinagem transcrita) — e a projeção `_index/specs--*.csv` derivada do frontmatter cobre a consulta tabular multi-predicado.
10. **Como tratar fóruns/Reddit/YouTube sem perder experiência e sem risco?** Adotar a política metadata-first do documento, com três regras adicionais que faltavam **nos dois planos**: transcrição de YouTube é artefato efêmero (nunca entra no repo); pseudonimização de autores de fórum (LGPD — handle + opinião = dado pessoal; e remover dado de histórico Git exige rewrite); flag `patrocinado` em reviews. E a base legal correta para uma empresa brasileira é a **Lei 9.610/98** (art. 8º: fatos não protegidos; art. 46: citação com atribuição) — "fair use" é doutrina americana e não existe no Brasil; a 9.610 é *mais estreita*, o que reforça destilação sobre cópia.
11. **Quais benchmarks decidem entre híbrida/Graphify/GraphRAG/LightRAG/Graphiti?** Pergunta errada: não há bake-off a fazer. Eval de ~90 perguntas com gabarito contra a arquitetura única implantada, trimestral, erros virando backlog; A/B de **2** candidatos apenas se um gatilho objetivo disparar (ex.: >10% do eval falhando em semântica pura por 2 trimestres). Um benchmark exequível vale mais que um rigoroso e imaginário.
12. **Tecnologias emergentes de 2026 faltando?** O problema do documento é excesso, não falta. A captura de 2026 que importa é a **biblioteca SMPTE gratuita** (fonte, não tecnologia). Se o gatilho semântico um dia disparar: índice vetorial *embutido* (pgvector já disponível, sqlite-vec/LanceDB) devolvendo caminho+linhas — nunca chunks; DuckDB para a projeção tabular. Nada disso é urgente.
13. **RDF/JSON-LD e ontologias formais desde o início?** Não. Não há consumidor de triplas na stack — o consumidor lê Markdown com grep. Slugs estáveis + vocabulário fechado + enums-como-nós já são RDF-*ready*; um `_meta/mapeamento-padroes.md` de uma página (records_codec ⊂ schema:…, PROV-O ↔ sources[]) compra o export futuro por quase zero. MovieLabs OMC vale como leitura para nomear funções/workflows; PROV-O/SKOS/QUDT como inspiração documentada.
14. **Como garantir portabilidade entre Claude, ChatGPT, Gemini e futuros?** Arquivos de texto são o formato mais portátil que existe; qualquer agente com leitura de arquivos consome o acervo. Complementos absorvidos: contrato do wrapper MCP fino **pré-especificado** (erguível em um dia quando surgir consumidor sem filesystem) e **teste anual de portabilidade** (rodar 10 perguntas do benchmark com outro modelo) — que nenhum dos dois planos previa.
15. **Que plano alternativo o avaliador recomenda?** O da Seção 9: chassis grep-first + módulos de rigor absorvidos. É o plano Claude v1.1, cuja lista de mudanças está na Seção 7 — e que só existe nessa forma por causa do plano ChatGPT.

---

## 5. O que os dois planos têm em comum (o núcleo validado — não rediscutir)

Convergência independente é o sinal de acerto mais forte que esta revisão produziu. Os dois planos, escritos sem se ver, afirmam:

1. **Git + Markdown/texto como fonte canônica portátil**; Obsidian como superfície humana, nunca como banco; índices **sempre derivados, descartáveis e regeneráveis**; anti lock-in como princípio.
2. **Destilação curada > despejo de documentos**: "não deve ser uma pasta gigantesca de PDFs vetorizados" (ChatGPT) ≡ "conhecimento destilado, não cópia" (Claude). NotebookLM e Claude Projects: úteis como laboratório, rejeitados como núcleo.
3. **Evidência antes da síntese**, com hierarquia de autoridade (norma/fabricante ≠ teste independente ≠ fórum) e **contradição preservada com as duas citações, nunca fundida silenciosamente**.
4. **Recuperação progressiva sob orçamento explícito de tokens** — com alvos quase idênticos pelos dois caminhos (Evidence Pack 1.500–3.000 tokens ≈ consulta ≤2.500 tokens).
5. **Ceticismo fundamentado sobre embeddings puros** para códigos de produto, firmware, pinagem, versões e números — lexical/estruturado primeiro.
6. **Cálculo determinístico fora do LLM** (o ChatGPT o especificou; o Claude o absorve).
7. **Benchmark-ouro com gabarito antes de escalar**, decisão por medição, e temporalidade/frescor como preocupação de primeira classe.
8. **IA gera rascunho, nunca verdade automática**; revisão proporcional ao risco; projeto novo e isolado.

Esse núcleo comum é a arquitetura de fato. As divergências são sobre **quanto maquinário** é preciso para servi-lo — e aí os contextos decidem: 1–2 pessoas decidem por convenções e scripts, não por plataformas.

---

## 6. Onde o plano Claude é superior (juízo frio, consolidado das 4 frentes)

1. **Adequação exata ao consumidor real.** Grep/Glob/Read já estão no harness do Claude: custo zero de schema, zero de rede, zero de infra, frescor absoluto (o arquivo nunca defasa de si mesmo). O plano ChatGPT paga uma pilha de 3–4 produtos OSS + 2–4k tokens/sessão para converter 1–3 chamadas locais gratuitas em 1 chamada remota de custo equivalente. E como o plano Claude decidiu **não hospedar originais copyrighted**, a principal justificativa estrutural do gateway (controlar acesso a um cofre) se dissolve.
2. **Uma única fonte de verdade.** A nota é simultaneamente claim-store, cápsula canônica e página editorial; editar conteúdo *é* editar o índice; o CI é um validador único. Sem Fase 7 de sincronização. O modo de falha é superior: pior caso lento, nunca silenciosamente errado.
3. **Realismo operacional.** É o único plano que dimensiona volume (~2.400 notas), esforço (sessões), rotina (mensal ≤1 sessão), custo por consulta — e que reconhece **abandono** como risco (R5). Processo que não roda é pior que processo nenhum, porque gera metadado mentiroso.
4. **Vocabulário de arestas específico do domínio.** `records_codec`/`paired_gamut`/`budget_alternative_to` são grep-precisos e auto-documentados para o escritor-LLM; o vocabulário genérico do ChatGPT (`SUPPORTS` conflacionando codec, gamut, protocolo e mídia) exige joins de tipo que grep não faz. Enums-como-nós + vocabulário fechado + CI = enforcement barato contra deriva que o plano ChatGPT não tem em custo comparável.
5. **Conteúdo engenheirado para o recuperador** (TL;DR primeiro, linhas auto-suficientes, slugs adivinháveis, índices pré-computados): a curadoria que aconteceria de qualquer jeito *é* a camada de recuperação. O ChatGPT constrói maquinaria para compensar conteúdo não-engenheirado — estritamente mais caro.
6. **Benchmark exequível com ciclo fechado** (erros → backlog de MOC/aliases) e **critérios de aceite testáveis por fase** (CI verde; consultas-exemplo com custo ±50%), contra critérios qualitativos.
7. **Cobertura de mercado atual e economicamente consciente**: Apêndice A com ~3–5× mais marcas e mais atual (Blazar, Electro Storm, Nextorage, B-Mount, RED/Nikon…), `price_tier`, `budget_alternative_to {ratio}`, rental-only, ecossistemas — para produtora pequena, vale mais que metade do mapa temático rival.
8. **Anti-alucinação acionável**: pipeline com verificador **adversarial** (instruído a refutar) e métrica de calibração (taxa de rejeição por lote) — mais eficaz que 10 dimensões de confiança que ninguém preencherá.
9. **Procedência no ponto de consumo**: tier + confidence moram no frontmatter que o Claude lê ao responder — não num claim-store atrás de um gateway que ainda não existe.
10. **Templates concretos prontos** (notas exemplares preenchidas) contra schema abstrato.

---

## 7. O que o plano Claude absorve do ChatGPT (a lista da v1.1 — concreta)

### Modelo de conhecimento (Frente B)
1. Aresta **`incompatible_with`** `{motivo, via}` + propriedade `{limite: "..."}` em arestas positivas (`records_codec: [{to: prores, limite: "até 60p em 4K"}]`).
2. **Subgrafo de diagnóstico**: tipo de nó `problema` + template (Sintoma / Causas prováveis / Como discriminar / Correções) + arestas `known_issue`, `caused_by`, `resolved_by`, `diagnosed_with` + diretório `troubleshooting/`.
3. Arestas **`variant_of`** (Venice 2 8.6K vs 6K) e **`distinct_from`** ("não confundir com") + notas de desambiguação (latitude ≠ dynamic range; definição ≠ resolução).
4. **`loc`** opcional em sources (`{url, tier, ret, loc: "p. 143, tab. 8"}`) + flag **`patrocinado`**.
5. **Regra do escopo condicional** no conventions.md + seção `## Modos de gravação` (tabela resolução × fps × crop × codec × mídia × firmware) — o claim-lite.
6. Anotação **declarado / medido / relatado** junto ao número quando houver medição independente ("16 stops (declarado); ~13,5 (CineD, medido)").
7. Template **`compat--<a>--<b>.md`** + regra de promoção aresta→nota (≥2 condições, ou conflito de evidência, ou ≥3 participantes).
8. **`conflito: true`** no frontmatter + seção `## Conflito` padronizada + **guia de falsos conflitos** em `_meta/` como instrução do Verificador.
9. **Rubrica de confiança**: as 10 dimensões viram os critérios documentados que definem alta/media/baixa (não campos).
10. Temporal mínimo: **`ate_firmware`**, **`status_norma`** {in_force/superseded/withdrawn} em standards, e estado **`revisar`** setado por staleness/mudança de fonte.
11. **`jurisdicao`** direcionado (só RF, elétrica, drone — não universal).
12. **Mapeamento a padrões formais** documentado em 1 página (RDF-ready sem RDF).

### Recuperação (Frente A)
13. **`_index/specs--<categoria>.csv`** derivado do frontmatter → consulta numérica multi-predicado via DuckDB/awk (fecha a maior lacuna técnica do grep-first).
14. **`tools/query_graph.py`** — caminhos ≤N saltos sobre `graph.json`, filtrados por tipo de aresta (cadeias de adaptadores; mata o argumento do Neo4j).
15. **Evidence Pack como contrato de resposta** no AGENTS.md: toda resposta declara fontes+tier, conflitos abertos, evidência ausente e versão do corpus (SHA); lacuna detectada → registrada em arquivo de gaps (o `av_report_gap` virou protocolo).
16. **Tabela de roteamento** pergunta→mecanismo (a §10.1 do ChatGPT, mapeada para grep/índice/grafo/calc) no AGENTS.md.
17. **Log de perguntas não respondidas** — sinal sempre-ligado para o gatilho semântico (não depender só do eval trimestral).
18. **Contrato do wrapper MCP fino pré-especificado** (implementar apenas quando surgir consumidor sem filesystem).
19. **Docling** como ferramenta de redação na ingestão de PDFs com tabelas/pinagens (Fase 2+; jamais no caminho de consulta).

### Ingestão, fontes e jurídico (Frente C)
20. **Cofre-lite**: pasta fora do Git só com PDFs oficiais livremente baixáveis + `sources-manifest.yaml` (URL, sha256, data, **edição/revisão do documento**) + snapshot no Wayback Machine na captura (anti link rot).
21. Base legal reescrita: **Lei 9.610/98** (não "fair use") + **LGPD**: pseudonimizar autores de comunidade na destilação; nunca versionar handles no Git.
22. **Transcrição de YouTube = artefato efêmero** — nunca entra no repo.
23. Tier de fonte refinado: separar **teste-de-laboratório** de `educacao` + regra "**marketing, agregador e conteúdo gerado por IA nunca são promovidos a fato** — servem só para descoberta".
24. **Invalidação**: fonte mudou (firmware/manual novo) → notas dependentes voltam a `revisar`.
25. Tag **`risco: seguranca`** (elétrica, rigging, altura, RF, drone): revisão humana **100%** (não amostral) + disclaimer fixo + só fonte oficial/norma.
26. Regra **anti-astroturfing**: dica comunitária só sobe com corroboração em ≥2 comunidades independentes.
27. Regra **anti-injeção**: destilação sempre reescreve — texto bruto de fórum jamais é colado no acervo (o repo é lido pelo Claude *como autoridade*; citação imperativa embutida é superfície de ataque).
28. **Fontes novas** (do ChatGPT): SMPTE Setting the Standards Free (prioridade nº 6 de partida, ~30–40 notas de norma), Lensrentals Optical Bench, Film and Digital Times, AbelCine, CVP, fxguide, befores & afters, Lowepost, Production Expert, Sound On Sound, cinematography.com, fórum oficial Blackmagic, GitHub issues de OSS, known-issues/advisories de fabricante, ASC MHL, MovieLabs OMC, C2PA, white papers ARRI, guias Brompton/Megapixel, Netflix Partner Help Center. **Fontes BR que ambos esqueceram**: ABC, SET, ANATEL (RF pós-700 MHz, homologação), NR-10/NR-35 + NBR 5410, ANCINE/CONDECINE, ANAC/DECEA (drones).

### Escopo, avaliação, roadmap e operação (Frente D)
29. Domínio novo **`seguranca/`**: NR-10, NR-35, ABNT, CREA/ART, AVCB/bombeiros, cargas/truss, trabalho em altura — a lacuna mais grave do Plano v1.0.
30. **`troubleshooting/`** como classe própria (com o subgrafo do item 2).
31. Subdomínios: **arquivo/preservação** (LTO, 3-2-1, ASC MHL, chain of custody), **entrega** (DCP, IMF, masters, QC, loudness R128), **autenticidade/C2PA** (~12 notas), checklist de **ciência da imagem** (12.1) dentro de `conceitos/`, nota "RF no Brasil (ANATEL)".
32. **`tools/calc/`** (Python stdlib, CLI, pytest no CI, dados YAML derivados do frontmatter): prioridade **mídia/storage → LED → elétrica (disclaimer impresso) → óptica**; redes adiada; RF rejeitada como calculadora (nota ANATEL + Wireless Workbench). Linha no AGENTS.md: "pergunta de cálculo → rode tools/calc, nunca calcule de memória".
33. **Benchmark 60 → ~90 perguntas** em 10–11 categorias: +**abstenção** (8–10 perguntas-armadilha), +temporal/firmware, +conflito oficial×comunidade, +cálculo, +segurança; multi-hop como tier difícil. **Smoke set de ~15** rodado a cada mudança estrutural (AGENTS.md, ontologia, vocabulário); rodada completa por onda/trimestre.
34. **KPI 8 — Fidelidade**: ≥90% das respostas passam na rubrica de 4 itens derivada do "critério filosófico" (citou fonte+tier; respeitou escopo/versão; expôs conflito; absteve-se quando o acervo não cobre). **KPI 9 — Abstenção**: ≥90% das armadilhas respondidas com "sem evidência suficiente", zero specs inventadas.
35. **Fase 1.5 — piloto vertical transversal** (30–60 notas numa cadeia real: câmeras→lentes→mounts→codecs→cor + 1 painel LED + 1 processadora + 1 calculadora + 2–3 notas de troubleshooting + 1 histórico de firmware + 1 standard com supersedes) com gate importado do ChatGPT: **"representável sem exceções estruturais graves"** antes de abrir a onda 2a. Defeito de esquema descoberto com 50 notas, não 800.
36. **Coletor RSS automatizado semanal** (GitHub Action → `_inbox/AAAA-MM.md`) triado na rotina mensal única — cadência semanal de máquina, mensal de gente; prioridade 1: firmware/advisories/recalls.
37. **`stats.md`** ganha 5 indicadores da matriz de completude: notas×status por domínio, % com fonte oficial, conflitos abertos, links mortos (CI), % stale. A matriz 8-D completa: rejeitada.
38. Apêndice B revisado: **~2.600 notas**; e **orçamento financeiro/token da construção** com teto mensal (estouro de custo é o gatilho mais provável do risco de abandono — ausente das duas tabelas de risco).
39. **Decisão nova D7**: criar 4º tier de fonte **`campo-proprio`** (experiência técnica generalizada/anonimizada de set — maior valor, zero risco jurídico) — exige exceção explícita e controlada à regra de isolamento; **decisão do dono do projeto**. Rito: post-mortem técnico de 15 min pós-job → notas novas/corrigidas.
40. **Teste anual de portabilidade**: 10 perguntas do benchmark rodadas com outro modelo/cliente.

---

## 8. Veredito por tecnologia (consolidado)

| Tecnologia (plano ChatGPT) | Veredito | Em uma linha |
|---|---|---|
| Git + Markdown + Obsidian | **É a fundação** | Único ponto de acordo integral — e é o plano Claude inteiro |
| Zotero | Rejeitar | Terceiro sistema com estado; sources[] + manifesto cumprem o papel |
| Cofre de evidências completo | Rejeitar → **cofre-lite** | PDFs oficiais + manifesto/hash + Wayback; sem adjudicação por item |
| Docling / MinerU | **Adotar (redação)** | Extração de tabelas/pinagens na ingestão; nunca na consulta |
| RAGFlow | Rejeitar | Pilha de 8–16 GB para servir o que o repo já serve |
| Qdrant / dense embeddings | Gatilho (S.15) | Se disparar: índice embutido (pgvector/sqlite-vec) devolvendo caminho+linhas |
| BM25/sparse dedicado + reranking | Rejeitar | Ripgrep + estrutura cobrem o lexical; reavaliar só com camada vetorial |
| Neo4j | Rejeitar | `graph.json` + script de caminhos cobre a escala real (2,4k nós) |
| Graphiti | Rejeitar (absorver modelo temporal) | Cadência mensal ≠ memória de agente; `valid/superseded` em frontmatter |
| Graphify | Rejeitar do caminho crítico | LLM re-extraindo grafo já declarado = ruído; opcional como minerador offline |
| Microsoft GraphRAG | Rejeitar; LazyGraphRAG sob demanda | Síntese global rara → rodar offline, resultado vira nota |
| LightRAG | Rejeitar | Nenhuma capacidade única para este caso |
| Gateway MCP (9 ferramentas) | Contrato pré-especificado, implementação adiada | Só quando surgir consumidor sem filesystem; wrapper fino sobre grep/read |
| Evidence Pack | **Adotar como convenção** | Contrato de resposta no AGENTS.md; como servidor, rejeitar |
| Calculadoras | **Adotar agora** | Scripts no repo, testados em CI; a pergunta "MCP separado?" se dissolve |
| Benchmark de 11 sistemas | Rejeitar | Eval de ~90 contra a arquitetura única; A/B de 2 só com gatilho |
| RDF/JSON-LD/PROV-O/QUDT | Rejeitar adoção; mapear em 1 página | RDF-ready sem RDF; MovieLabs OMC como leitura |

---

## 9. Lacunas que NENHUM dos dois planos cobria (o valor novo desta revisão)

1. **Fidelidade ≠ recuperação**: nenhum plano mede se o Claude, tendo lido a nota certa, responde **com ela** ou com a memória paramétrica dele. Mitigação: **perguntas-canário** no benchmark, cujas respostas no acervo contradizem deliberadamente o prior típico de LLM, medindo taxa de sobrescrita.
2. **Semântica de ausência (mundo aberto)**: campo/aresta omitidos significam "desconhecido", nunca "não tem"; negação verificada deve ser explícita (`nd_interno: nao`, com fonte); o AGENTS.md deve proibir inferir incapacidade a partir de ausência. Para um cérebro de compatibilidade, é a lacuna que mais produziria resposta falsa dita com confiança.
3. **Direcionalidade, simetria e inversas de arestas**: onde a aresta mora (no adaptador ou na câmera?), quais são simétricas (`competes_with`) ou antissimétricas (`supersedes`) — e validação disso no CI. Sem política, o grafo acumula duplicatas e assimetrias silenciosas.
4. **Comparabilidade de medições**: DR com qual critério de SNR? lux a 3 m com qual ótica? Definir campo canônico por métrica (`dr_declarado` vs `dr_medido_cined`) para a consulta comparativa central não comparar incomensuráveis.
5. **Deriva do harness**: ambos dependem de contratos de ferramenta que não controlam (truncamento de resultados do grep; schemas MCP). Um grep transversal truncado **omite notas compatíveis sem sinalizar**. Mitigação: limites conhecidos documentados no AGENTS.md + canários de recuperação no smoke set.
6. **Segurança agêntica do conteúdo comunitário**: texto de terceiros dentro do acervo é lido com a autoridade do cérebro — injeção via citação de fórum. Regra: destilação sempre reescreve; nada imperativo citado bruto.
7. **Base legal brasileira** (Lei 9.610/98, LGPD) e **regulatório BR operacional** (ANATEL, SBTVD/TV 3.0, ANCINE/CONDECINE, ANAC/DECEA, NR-10/35/NBR 5410) — dois planos raciocinando em doutrina e fontes americanas para uma empresa que opera exclusivamente no Brasil.
8. **Link rot** sem arquivamento (Wayback + manifesto) — a auditabilidade prometida pelos dois apodreceria em ~3 anos.
9. **Responsabilidade civil em conteúdo de segurança** consumido como recomendação de set (mitigação: item 25 da Seção 7).
10. **Astroturfing/review comprado** além do patrocínio declarado (mitigação: corroboração ≥2 comunidades).
11. **Ciclo de retroalimentação da experiência própria** + tier `campo-proprio` (a fonte de maior valor e menor risco, bloqueada pela regra de isolamento se não houver exceção explícita).
12. **Orçamento financeiro da construção** (~2.400 notas × pipeline multiagente) com teto mensal.
13. **Teste de portabilidade real** (a neutralidade de modelo declarada pelos dois nunca é testada em nenhum).

---

## 10. Encerramento

**Para o ChatGPT:** seu documento pediu (§28) uma arquitetura menor, mais confiável e mais demonstrável. Este parecer entrega exatamente isso: sua doutrina epistemológica sobrevive quase intacta — escopo condicional, falsos conflitos, abstenção, calculadoras, política de fontes, arestas negativas/diagnósticas, SMPTE — absorvida como ~40 mudanças concretas num chassis que uma equipe de 1–2 pessoas consegue operar: repositório Git/Markdown grep-first, uma única representação do conhecimento, grafo e índices derivados deterministicamente, zero servidores permanentes. O que foi rejeitado (claim-store, cofre completo, RAGFlow/Qdrant/Neo4j/Graphiti/Graphify no caminho crítico, gateway de 9 ferramentas, benchmark de 11 sistemas, 10 dimensões, 23 estados) foi rejeitado por um único critério, que é o seu: *o objetivo é sair da avaliação com uma arquitetura menor — não com uma lista maior de ferramentas*.

**Próximo passo proposto:** consolidar as ~40 absorções da Seção 7 no Plano v1.1 e submetê-lo a uma última rodada de objeções antes de materializar a Fase 0 no repositório.

---

*Parecer produzido por leitura integral dos dois documentos + 4 frentes de revisão especializadas (Recuperação · Modelo · Ingestão/Jurídico · Escopo/Operação). 2026-07-23.*
