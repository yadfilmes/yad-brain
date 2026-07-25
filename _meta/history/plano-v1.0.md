# Cérebro Audiovisual — Plano de Projeto Completo

| | |
|---|---|
| **Versão** | 1.0 (planejamento — nada executado ainda) |
| **Data** | 2026-07-23 |
| **Repositório-alvo** | `yadfilmes/yad-brain` (atualmente vazio) |
| **Autor do plano** | Claude (Opus 4.8 / Fable 5), a pedido de Felype — YAD Filmes |
| **Status** | Aguardando avaliação externa antes de qualquer execução |
| **Restrição declarada** | Projeto novo e **isolado** — sem conexão com nenhum outro trabalho da YAD |

---

## 0. Como ler este documento (nota ao avaliador externo)

Este documento é **auto-contido**: foi escrito para ser avaliado por um revisor (humano ou IA) que não tem acesso à conversa que o originou. Ele descreve o planejamento completo de um projeto ainda não iniciado.

- As Seções 1–5 explicam **o quê** e **por quê** (visão, requisitos, decisão arquitetural).
- As Seções 6–14 são a **especificação técnica** (ontologia, formatos, estrutura, pipeline).
- As Seções 15–21 cobrem **execução e operação** (roadmap, avaliação, governança, riscos).
- Os Apêndices A–B trazem os dados brutos de maior volume (marcas, estimativas).
- A **Seção 24 lista perguntas específicas que pedimos ao avaliador que responda.**

---

## 1. Sumário executivo

O projeto cria um **"cérebro" de conhecimento técnico do audiovisual profissional** — câmeras, lentes, iluminação, elétrica, painéis de LED, switchers, edição, colorização, VFX, 3D, produção, funções de set e tudo adjacente — materializado como um **repositório Git real de arquivos Markdown**, estruturado como **grafo de conhecimento navegável**, e otimizado para ser consultado por **Claude (LLM)** com **custo mínimo de tokens** e latência quase nula.

A decisão arquitetural central: **não usar banco vetorial, banco de grafos nem RAG como fundação**. O sistema de arquivos é o banco de dados; as ferramentas nativas do Claude Code (`Grep`, `Glob`, `Read`) são o motor de busca; o grafo é expresso em **frontmatter YAML tipado** e **wikilinks** dentro das próprias notas, com índices derivados por script. O mesmo diretório é simultaneamente: (a) repositório Git versionado, (b) vault do Obsidian para navegação humana, (c) base de consulta do Claude.

Camadas semânticas (pgvector) e de sumarização global (GraphRAG/LazyGraphRAG) ficam **explicitamente adiadas** para uma fase opcional, ativáveis apenas mediante gatilhos objetivos definidos na Seção 15.

A construção é **incremental, em ondas por domínio**, usando um pipeline multiagente com verificação adversarial de fatos (Seção 13), porque especificação de equipamento é exatamente o tipo de conteúdo em que LLMs alucinam números. Nenhuma spec entra como "revisada" sem checagem contra fonte oficial.

Escala estimada ao fim de 12 meses: **2.000–3.000 notas atômicas** (~1,5–2,5 M tokens de acervo total), com custo típico de consulta de **~1.000–2.500 tokens lidos** (1–3 arquivos), independentemente do tamanho total do acervo.

---

## 2. Contexto e motivação

**Quem:** uma produtora audiovisual brasileira (YAD Filmes) que opera captação, iluminação, transmissão ao vivo, pós-produção e finalização — e usa Claude como assistente técnico no dia a dia.

**Dor:** o conhecimento técnico do audiovisual é vasto, fragmentado e disperso — manuais de fabricante, spec sheets, fóruns (Reddit, Lift Gamma Gain, CML), YouTube, blogs (CineD, Newsshooter), experiência de set. Consultar isso hoje significa: ou o LLM responde de memória (risco de alucinação e desatualização), ou faz busca na web a cada pergunta (lento, caro, irreproduzível), ou o humano garimpa manualmente.

**Visão:** uma "Wikipédia do audiovisual" **com base** — não só listas, mas conexões: que lente encaixa em que câmera, que codec conversa com que pipeline de cor, qual a alternativa barata de cada equipamento, o que a comunidade diz que o manual não diz. Consultável pelo Claude em segundos, gastando centenas (não dezenas de milhares) de tokens por pergunta.

**Por que um repositório (e não um SaaS de notas):**
1. **Versionamento e durabilidade** — Git é o formato mais durável e auditável que existe para texto.
2. **O Claude lê filesystem nativamente** — sem API intermediária, sem custo por chamada, sem infra.
3. **Duplo consumo** — o mesmo diretório serve humano (Obsidian) e máquina (grep) sem conversão.
4. **Construção incremental** — cada commit é um incremento rastreável; dá para construir ao longo de meses sem "big bang".

---

## 3. Objetivos, requisitos e restrições

### 3.1 Objetivos

| # | Objetivo | Medível por |
|---|---|---|
| O1 | Cobertura enciclopédica do audiovisual profissional (marcas, modelos, sistemas, conceitos, funções, workflows) | nº de notas por domínio vs. estimativa (Apêndice B) |
| O2 | Estrutura de **grafo**: conexões tipadas e navegáveis entre entidades | nº de arestas; travessias possíveis via grep |
| O3 | Consulta **rápida** (local, sem rede) e **barata em tokens** para o Claude | benchmark da Seção 17 (≤3 arquivos, ≤2.500 tokens por consulta típica) |
| O4 | **Confiabilidade**: distinção explícita entre spec oficial e opinião de comunidade; procedência em toda nota | 100% das notas com `sources`; % `reviewed` |
| O5 | **Manutenibilidade** ao longo de anos por um time pequeno | rotina mensal ≤1 sessão; CI verde |

### 3.2 Requisitos funcionais

- RF1 — Toda entidade relevante (câmera, lente, luz, software, codec, função, técnica…) tem **uma nota atômica** própria.
- RF2 — Relações entre entidades são **tipadas** (vocabulário fechado de arestas, Seção 6.4) e declaradas em frontmatter YAML.
- RF3 — Perguntas transversais ("tudo que grava BRAW", "tudo com mount PL", "alternativas baratas ao Teradek Bolt") são respondíveis com **um grep** ou **um arquivo de índice**.
- RF4 — Cada nota registra **fontes com tier** (oficial / comunidade / educação), data de captura e nível de confiança.
- RF5 — O repositório contém um **protocolo de consulta** legível pelo Claude (`AGENTS.md` + Skill) ensinando a navegar sem carregar o acervo.
- RF6 — Índices e grafo (`graph.json`, backlinks, índices cruzados) são **derivados por script** do frontmatter — nunca mantidos à mão.
- RF7 — O vault abre no Obsidian sem adaptação (wikilinks, frontmatter e estrutura compatíveis).

### 3.3 Requisitos não-funcionais (com alvos numéricos)

| Requisito | Alvo |
|---|---|
| Custo de token por consulta pontual ("specs da FX6") | ≤ 1.500 tokens lidos |
| Custo por consulta de travessia ("lentes p/ Venice 2 e por quê") | ≤ 2.500 tokens lidos |
| Custo por consulta comparativa ("Alexa 35 vs Venice 2 vs Raptor") | ≤ 6.000 tokens lidos |
| Arquivos tocados por consulta típica | 1–3 |
| Tamanho de nota atômica | 300–900 tokens (alvo ~500); dividir acima de ~1.200 |
| Latência de recuperação | local (filesystem); zero chamadas de rede |
| Links quebrados / arestas fora do vocabulário no CI | 0 |
| Infra externa obrigatória | nenhuma (Git + arquivos, apenas) |

### 3.4 Restrições

- **Isolamento**: projeto novo, sem conexão com outros repositórios, dados, clientes ou planilhas da YAD. Nenhum dado sensível ou comercial da empresa entra neste repo.
- **Copyright**: não armazenar manuais/tabelas de fabricante na íntegra. Apenas conhecimento destilado + citações curtas + URL da fonte (Seção 11.4).
- **Sem pressa, com padrão**: prioridade é qualidade e consistência do esquema, não velocidade de preenchimento.
- **Sem execução até aprovação**: este plano precede qualquer commit.

### 3.5 Fora de escopo (v1)

- Hospedar PDFs/manuais/imagens (texto apenas, por ora).
- Preços em tempo real e disponibilidade de mercado (apenas `price_tier` qualitativo).
- Inventário/patrimônio da YAD (violaria o isolamento).
- Interface própria (Obsidian e GitHub bastam).
- Busca semântica/vetorial como fundação (ver Seção 15 para os gatilhos de adoção futura).

---

## 4. Decisão arquitetural

### 4.1 O princípio: para o LLM, o sistema de arquivos É o banco de dados

O consumidor primário é o Claude operando com três ferramentas nativas: `Grep` (busca por conteúdo via ripgrep), `Glob` (busca por nome/caminho) e `Read` (leitura parcial ou total de arquivo). Juntas, elas são um motor de busca completo, local e gratuito. A forma mais barata e rápida de servir conhecimento a esse consumidor **não é** adicionar uma camada de recuperação (embeddings, banco de grafos, API) — é **estruturar os arquivos para que a busca nativa seja cirúrgica**:

1. **Nomes previsíveis** → o Claude *adivinha* o caminho (`captacao/cameras/sony/venice-2.md`) e vai direto, custo de busca ~zero.
2. **Frontmatter tipado** → perguntas estruturadas viram grep de um campo (`records_codec: .*braw`).
3. **Linhas auto-suficientes** → o grep devolve a resposta na própria linha, muitas vezes sem nem abrir o arquivo.
4. **Índices hierárquicos** → o Claude lê o mapa (pequeno), não o território (grande).

### 4.2 Evidência

A própria Anthropic construiu a recuperação do Claude Code assim: a primeira versão usava RAG/busca vetorial; foi substituída por busca agêntica com grep, que segundo o time **"superou tudo, com folga"** — por três razões que espelham exatamente este projeto: **precisão** (grep = correspondência exata; embeddings = vizinhos difusos), **frescor** (todo índice derivado defasa em relação ao arquivo editado; o arquivo nunca defasa de si mesmo) e **simplicidade** (nenhum índice para construir, sincronizar ou pagar). Para um acervo de referência majoritariamente estável, consultado por um agente com grep, essa troca é ainda mais vantajosa do que para código.

### 4.3 Alternativas consideradas (e por que não são a fundação)

| Opção | O que faz bem | Custo real para este projeto | Veredito |
|---|---|---|---|
| **Markdown + Git (vault Obsidian)** | arquivos versionados; grep/glob/read nativos; grafo via frontmatter + wikilinks; zero infra | disciplina de convenções | **FUNDAÇÃO** |
| **Obsidian (aplicativo)** | graph view, backlinks, edição confortável para humanos | nenhum (mesmos arquivos) | **SIM — camada humana** |
| **Skill do Claude (progressive disclosure)** | ~100 tokens residentes ensinam o protocolo; corpo/referências carregam sob demanda | manter 1 arquivo curto | **SIM — interface de acesso** |
| **pgvector (Supabase)** | busca semântica ("acha o parecido") | pipeline de embeddings, sync a cada edição, round-trip de rede, chunks não escolhidos pelo agente | **ADIADO** — fallback com gatilho (S.15) |
| **GraphRAG (Microsoft)** | perguntas globais/temáticas via resumos de comunidades | indexação custa 10–40× um banco vetorial; reindexação a cada mudança; segunda fonte de verdade | **NÃO** (LazyGraphRAG pontual, sob demanda, se um dia precisar de síntese global) |
| **Neo4j / Graphiti (KG temporal)** | grafo "de verdade", fatos com validade temporal | infra permanente, ETL das notas para o banco, toda travessia vira chamada de API | **NÃO** — resolve problema que não temos |
| **LlamaIndex knowledge-graph** | extração automática de triplas | framework + embeddings + estore derivado; lock-in; Claude Code não lê nativamente | **NÃO** |
| **NotebookLM** | Q&A excelente para consumo humano de um corpus | caixa-preta: não é repo, não versiona, não é consultável programaticamente pelo Claude | **NÃO como núcleo** (uso pessoal paralelo é livre) |

### 4.4 O que "graphify" significa aqui

O grafo **não requer banco de grafos**. Ele é expresso em três mecanismos baratos:

1. **Arestas tipadas no frontmatter** — cada nota declara suas relações num vocabulário fechado (`rel.compatible_with`, `rel.records_codec`, `rel.competes_with`…).
2. **Enums são nós** — mounts, codecs, color spaces, battery mounts **não são texto solto**: são arquivos próprios, referenciados por slug. Consequência: `grep -rl "mount--pl"` devolve *todos* os equipamentos compatíveis com PL — uma travessia de grafo executada em texto puro.
3. **Wikilinks no corpo** — `[[obturador-180]]` conecta prosa a conceito; Obsidian renderiza, Claude resolve via slug→arquivo.

Um script (Seção 10) percorre o frontmatter de todas as notas e **deriva**: `graph.json` (nós + arestas), índice de backlinks, e índices cruzados (por-marca, por-mount, por-codec). O grafo é sempre um **artefato derivado do conteúdo** — nunca uma segunda fonte de verdade a sincronizar.

A **espinha dorsal** do grafo — o que o torna um cérebro que raciocina, e não um catálogo — é a cadeia:

```
câmera → records_codec → codec → paired_transfer_function → gamma/log
       → paired_gamut → color space → conforms_to_pipeline → ACES/IPP2/etc.
```

É essa cadeia que responde perguntas compostas do tipo "gravei em BRAW na Pyxis, como levo isso para um projeto ACES no Resolve?" seguindo 3–4 arestas.

### 4.5 Quando reconsiderar a decisão

A fundação grep-first deve ser reavaliada apenas se, com o acervo maduro e o benchmark (Seção 17) rodando, observarmos por dois trimestres seguidos: (a) >15% das perguntas exigindo >4 chamadas de ferramenta para achar o arquivo certo, ou (b) uma classe recorrente de perguntas puramente semânticas ("aquela luz com cara de tungstênio vintage") que grep + aliases não resolvem. Nesse caso, ativa-se a camada opcional da Seção 15 — sem tocar na fundação.

---

## 5. Arquitetura em camadas

```
┌──────────────────────────────────────────────────────────────┐
│ CAMADA 4 — ACESSO                                            │
│ AGENTS.md + SKILL.md: protocolo de consulta (~100 tokens     │
│ residentes). Ensina: identificar tipo → Glob direto →        │
│ senão grep em aliases → seguir arestas → citar fontes.       │
├──────────────────────────────────────────────────────────────┤
│ CAMADA 3 — ÍNDICES & GRAFO (derivados por script)            │
│ _moc/ (mapas de conteúdo por domínio) · _index/ (por-marca,  │
│ por-mount, por-codec, backlinks) · _graph/graph.json         │
├──────────────────────────────────────────────────────────────┤
│ CAMADA 2 — METADADOS (o grafo mora aqui)                     │
│ Frontmatter YAML tipado: id, type, aliases, tags, rel{...},  │
│ sources[], confidence, status, updated                       │
├──────────────────────────────────────────────────────────────┤
│ CAMADA 1 — CONTEÚDO                                          │
│ Notas atômicas .md (300–900 tokens): TL;DR primeiro,         │
│ specs em linhas chave:valor, contexto, conexões, dicas       │
│ de comunidade citadas                                        │
└──────────────────────────────────────────────────────────────┘
   ▲ humano: Obsidian (graph view, backlinks, edição)
   ▲ máquina: Claude Code (Glob / Grep / Read)
   ▲ ambos operam sobre o MESMO diretório = o repo Git
```

Fluxo típico de consulta: pergunta → (C4) protocolo decide o alvo → (C3) opcionalmente um índice de ~200 linhas → (C1/C2) leitura de 1–3 notas → resposta com citação de fontes. O acervo pode ter 3.000 notas; a consulta continua tocando 1–3.

---

## 6. Ontologia (o esquema do grafo)

Esta seção define o vocabulário que mantém milhares de notas coerentes. É a decisão de maior alavancagem do projeto: barata de acertar agora, caríssima de corrigir depois.

### 6.1 Convenções de identidade

- **`id` (slug)**: kebab-case, ASCII puro, globalmente único, estável para sempre. Ex.: `sony-venice-2`, `aputure-ls-600d-pro`, `filtro-nd`, `mount--pl`.
- **Regra de ouro dos nomes**: nome de arquivo = slug = ASCII **sem acento** (`iluminacao.md`, nunca `iluminação.md`), porque grep é byte a byte e `iluminação ≠ iluminacao`. Acentos, apelidos e códigos de modelo vivem em `aliases` (`["VENICE 2", "MPC-3610"]`).
- **Prefixo de tipo quando ambíguo**: `mount--pl.md`, `moc--luz.md`, `_tmpl-camera.md` — desambiguação instantânea em resultados de busca.
- **Slug = link**: `[[venice-2]]` resolve por `Glob **/venice-2.md`. Nunca dois arquivos com o mesmo basename.

### 6.2 Atributos comuns (herdados por todo hardware)

`made_by→`, `part_of_series→`, `type`, `subtype`, `announced`, `released`, `discontinued`, `status_produto {shipping / legacy / announced / rental-only}`, `price_tier {budget / prosumer / professional / high-end / rental-only}`, `weight_g`, `power_draw_w`, `successor_of→`, `ecosystem→`, `tags[]`, `sources[]`, `confidence`, `status {stub / draft / reviewed}`, `updated`.

Unidades embutidas no nome do campo (`weight_g`, `focal_min_mm`, `tstop_min`, `output_lux_at_3m`) — valores numéricos puros, consultáveis por máquina.

### 6.3 Tipos de entidade (nós), por domínio

**Transversais:** Marca/Fabricante (`parent_company→`, `sub_brands[]`, ex.: amaran→Aputure, RED→Nikon, Sachtler→Videndum) · Linha de produto · Ecossistema (ex.: "mundo Blackmagic": câmera+ATEM+HyperDeck+Resolve+Videohub) · Certificação/Programa (ex.: Netflix-approved) · Órgão de norma (SMPTE, ITU-R, EBU, AMPAS/ACES, DCI, AES).

**A. Captação:** CameraBody (`sensor_format {S16/S35/FF-VV/LF/65/MFT}`, `max_resolution`, `dynamic_range_stops`, `native_iso[]`, `mount→`, `internal_codecs[]→`, `media_slots[]→`, `nd_interno`, `ibis`, `af_system`, `camera_class {cinema / broadcast-system / mirrorless-hybrid / action-pov / ptz / drone / high-speed / film}`) · Acessório de câmera (cage, baseplate; `standard {15mm LWS / 19mm studio / rosette / NATO}`).

**B. Óptica:** LensCine (`image_circle`, `prime/zoom`, `focal_min/max_mm`, `tstop_min`, `anamorphic {no/1.3x/1.5x/1.8x/2x}`, `front_diameter_mm`, `close_focus_m`, `focus_rotation_deg`, `look {clinical/vintage/warm}`, `breathing`, `rehoused_from`) · LensPhoto (`af_type`, `stabilization`, `filter_thread_mm`) · LensMount (`flange_focal_distance_mm`, `protocolo eletrônico {/i / LDS / EF / E / RF / L / Z}`) · LensAdapter (`from→`, `to→`, `optical {clear/speedbooster/tc}`, `af_passthrough`) · MatteBox (`stages`, `filter_size {4x5.65 / 6.6 / 138mm}`) · FiltroÓptico (`família {ND/IRND/Pola/diffusion/grad}`, `força`, `look {Black Pro-Mist / Glimmerglass}`) · FIZ/LensControl (`canais F-I-Z`, `protocolo→`, `lidar_af`).

**C. Luz & Elétrica:** Fixture (`emitter {LED/HMI/tungstênio/fluor}`, `form_factor {COB / painel / tubo / fresnel / space-light}`, `color_mode {daylight / bicolor / RGBWW / RGBACL}`, `cct_range_k`, `cri`, `tlci`, `ssi`, `output_lux_at_3m`, `equiv_hmi_w`, `controle[]→ {DMX/RDM/Art-Net/sACN/CRMX/app}`, `ip_rating`, `mount {bowens/spigot/yoke}`) · Modificador (`tipo {softbox/octa/lantern/snapgrid/fresnel-adapter/flag/scrim/silk}`, `fits[]→`, `diffusion_stops`) · Gelatina/Difusão (Rosco/LEE; `código`, `transmissão`) · Controle de luz (dimmer, console, node; `protocolos[]→`) · Distribuição/energia (distro, gerador, power station; `capacidade`, `pure-sine`, `ruído_dba`).

**D. Painel/parede de LED & Virtual Production:** LEDPanel (`pixel_pitch_mm`, `brightness_nits`, `refresh_hz`, `scan_rate`, `uso {on-camera-VP / broadcast-xR / touring / instalação}`, `curvatura`) · LEDProcessor (`capacidade_pixels`, `genlock`, `hdr`, `low-latency`, `sync de câmera {ShutterSync / frame remapping}`) · Tracking de câmera (`método {optical-marker / IMU / encoder}`, `latency_ms`, `protocolo {FreeD / PSN}`) · MediaServer/render (`engine→ {Unreal / Notch / Disguise}`, `nDisplay/cluster`).

**E. Grip & Movimento:** Tripé/Sticks (`bowl {75/100/150/Mitchell/flat}`, `payload_kg`) · Cabeça fluida (`payload`, `contrabalanço`, `drag`) · Gimbal/Estabilizador (`classe {motorizado / vest+arm / mecânico}`, `payload`, `eixos`) · Dolly (`tipo {doorway / studio / western / skate}`, `bitola`) · Slider · Grua/Jib/Technocrane (`alcance_m`, `remote-head-ready`) · Remote head / Motion control (`eixos`, `repetibilidade`, `protocolo→`) · Ferragem de grip (stands, clamps, apple box; `receptor {baby/junior/spigot}`).

**F. Live & Broadcast:** Switcher (`classe {compacto-streaming / produção / broadcast-M-E}`, `me_count`, `inputs`, `keyers`, `formato_max`, `hw/sw`) · Sistema live integrado (`tipo {appliance / software / cloud}`, `ndi/st2110`, `replay`, `gráficos`) · Conversor/Scaler · Router/Matrix · Multiviewer · Encoder/Streaming (`codecs[]→`, `protocolos[]→ {SRT/RTMP/RIST/NDI}`, `bonded-cellular`) · Intercom (`tipo {partyline / DECT / IP}`, `interop {Dante/AES67}`) · CG/Gráficos on-air (`engine`, `data-driven`).

**G. Monitoração:** Monitor de campo (`size_in`, `nits`, `tools {waveform / false-color / peaking / LUT / desqueeze}`, `lut_support`) · Monitor de referência (`classe {broadcast / mastering}`, `painel {dual-cell LCD / OLED}`, `peak_nits`, `gamut_coverage`, `hdr[]→ {PQ/HLG/DoVi}`, `calibração`) · Scope/WFM · EVF.

**H. Gravação & Mídia:** Recorder externo (`records_codec[]→`, `raw_over_sdi/hdmi`, `função {monitor-recorder / deck / ISO}`) · Mídia (`forma {CFexpress-A/B, SDXC UHS-II, AXS, RED MINI-MAG, Codex Compact Drive, P2, SSD}`, `sustained_write_mbs`, `certificada_para[]→`) · Leitor/Dock · Storage de pós (RAID/NAS/SAN; `throughput`, `conectividade {TB / 10-25-100GbE}`) · Estação DIT (`software[]→`, `checksum`, `cópias redundantes`).

**I. Energia:** Bateria (`mount {V-Mount / Gold-Mount / B-Mount / NP-F / BP-U}`, `wh`, `max_draw_w`, `d-tap/usb-pd`, `avião-ok`) · Plate/Mount de bateria · Carregador · Distribuição DC.

**J. Wireless & Sync:** Wireless de vídeo (`banda {5GHz / 60GHz / SDR licenciado}`, `range_m`, `latency_ms`, `sdi/hdmi`, `multicast_rx`) · Timecode wireless (`precisão_ppm`, `jam-sync`, `formatos {LTC/ACN}`) · Gerador de genlock/referência (`black-burst / tri-level / PTP`).

**K. Áudio:** Microfone (`tipo {shotgun / lav / condensador-diafragma / dinâmico / boundary}`, `padrão polar`, `alimentação {phantom / plug-in}`, `self_noise_dba`, `conector {XLR / TA5 / MicroDot / Lemo}`) · Sistema wireless (`tecnologia {digital / híbrido}`, `banda {UHF / 2.4 / DECT}`, `gravação de backup`, `encryption`) · Mixer/Recorder de campo (`preamps`, `tracks`, `32-bit float`, `timecode`, `dante`) · Monitoração/IFB · Acessórios (boom, blimp, shockmount).

**L. Software:** Software (`categoria {NLE / color / VFX-comp / 3D / render-engine / motion / design-2D / DAW / live / media-server / MAM / review / transcode-QC / DIT-dailies / video-assist / previz / scheduling-budget / roteiro / IA-generativa}`, `vendor→`, `plataformas[]`, `licença {perpétua / assinatura / free-OSS}`, `interchange {AAF / XML / EDL / OTIO / EXR / USD}`, `codecs_supported[]→`, `colorspaces_supported[]→`) · Plugin (`host[]→`, `função`) · RenderEngine (`biased/unbiased`, `gpu/cpu`, `host[]→`) · Formato de intercâmbio.

**M. Conceitos técnicos & Formatos:** Codec (`família {intra / long-GOP / RAW}`, `bit_depth`, `chroma`, `variantes`, `uso {aquisição / mezanino / entrega / proxy}`) · Container (`MXF/MOV/MP4/R3D/BRAW/EXR-seq`) · ColorSpace/Gamut (`primaries`, `scene/display-referred`) · TransferFunction (`tipo {gamma / log / PQ / HLG}`, `paired_gamut→`) · LUT (`1D/3D`, `propósito {técnica / criativa / viewing}`) · Pipeline de cor (`framework {ACES / IPP2 / ARRI / DaVinci-WG / T-CAM}`, `idt/odt`) · Resolução/Raster · Frame rate/Scan · Aspect ratio · Padrão de sinal (`família {SDI / HDMI / IP-video / controle}`, `variante {3G/6G/12G-SDI, HDMI 2.1, NDI, ST 2110, SRT, Dante, AES67}`, `max_bandwidth`, `conector→`) · Conector/Cabo (`BNC / LEMO / XLR / D-Tap / powerCON / fibra-LC`) · Protocolo de controle (`DMX512 / Art-Net / sACN / CRMX / LANC / VISCA / FreeD / LTC / PTP`) · Órgão de norma.

**N. Pessoas, Processos & Documentos:** Função/Cargo (`departamento→`, `reports_to→`, `senioridade`, `opera[]→`, `entregáveis[]→`, `contexto {cinema / publicidade / broadcast / live / corporativo}`) · Departamento (Direção, Produção, Câmera, G&E, Som, Arte, Figurino, HMU, VFX, Pós, Cor, Estúdio/Switcher, VP) · Workflow/Processo (`fase {desenvolvimento / pré / produção / pós / entrega / live}`, `passos[]`, `inputs/outputs→`, `funções[]→`, `ferramentas[]→`) · Técnica/Conceito (`domínio {exposição / iluminação / composição / movimento / cor / edição / som / VFX / VP}`, `requer[]→`) · Documento/Template (`tipo {call sheet / ordem do dia / shot list / decupagem / storyboard / cronograma / stripboard / orçamento / gear list / mapa de luz / planta / camera report / sound report / DIT report / LUT report / spec de entregáveis / EDL-AAF-XML / autorização de uso de imagem / release de locação}`, `dono→`, `fase`) · Tipo de produção (`feature / curta / série / TVC-publicidade / branded / clipe / doc / live-broadcast / esporte / corporativo / social-vertical / ICVFX`) · Facility (`estúdio / volume LED / estúdio broadcast / OB-van-flypack / ilha de edição / sala de cor / mix stage / locadora`).

### 6.4 Tipos de relação (arestas) — vocabulário fechado

Regra: **preferir a aresta específica**; `compatible_with` e `see_also` são fallbacks. Arestas podem carregar propriedades (`{via: adaptador-x}`, `{desde_firmware: 2.0}`, `{ratio: "1/10 do preço"}`).

**Proveniência e identidade**

| aresta | significado | exemplo |
|---|---|---|
| `made_by` | fabricado/comercializado por | Alexa 35 → ARRI |
| `part_of_series` | pertence à família | Bolt 6 LT → Teradek Bolt |
| `sub_brand_of` | marca de valor/casa | amaran → Aputure |
| `owned_by` | controle societário | RED → Nikon; Sachtler → Videndum |
| `rebrand_of / oem_of` | mesmo hardware, outra etiqueta | (caso a caso) |

**Compatibilidade física e elétrica**

| aresta | significado | exemplo |
|---|---|---|
| `has_native_mount` | mount de fábrica | Venice 2 → E-mount (lever lock) |
| `accepts_mount` | aceita (nativo ou trocável) | Komodo-X → RF; PL via swap |
| `adapts` | adaptador liga mount A a B | Metabones EF→E |
| `mounts_via` | lente funciona no corpo através de | lente EF → FX3 `{via: mc-11}` |
| `fits / mounts_on` | encaixe mecânico | Light Dome → bowens |
| `uses_battery_mount` | padrão de alimentação | Alexa 35 → B-Mount |
| `powered_by` | fonte de energia | LS 600d → V-Mount / AC |
| `accepts_media` | mídia gravável | FX6 → CFexpress-A, SDXC |
| `compatible_with` | fallback genérico | matte box → rods 15mm LWS |

**Sinal, dados e formato**

| aresta | significado | exemplo |
|---|---|---|
| `records_to` | grava na mídia | Komodo → CFast/CFexpress |
| `records_codec` | grava/encoda o formato | Pyxis → BRAW |
| `wraps_in` | codec → container | ProRes → MOV/MXF |
| `outputs_signal` / `accepts_signal` | I/O de sinal | ATEM → 12G-SDI in |
| `converts` | conversão A→B | Hi5: SDI → HDMI |
| `streams_via` | protocolo de contribuição | encoder → SRT |
| `implements_standard` | conforma à norma | switcher → ST 2110 |
| `supports_colorspace` / `supports_transfer_function` | gamut/curva suportados | BURANO → S-Log3 |
| `paired_gamut` | log ↔ gamut par | Log-C4 ↔ AWG4 |
| `conforms_to_pipeline` | framework de cor | Resolve → ACES 1.3 |
| `syncs_via` | timecode/genlock | recorder → LTC / UltraSync |
| `controls / controlled_by` | comando | Hi-5 → motor cforce; PTZ ← VISCA |

**Mercado, ecossistema e ciclo de vida**

| aresta | significado | exemplo |
|---|---|---|
| `part_of_ecosystem` | integra sistema interoperante | ATEM → mundo Blackmagic |
| `pairs_with` | par consagrado de campo | Alexa 35 → Signature Primes |
| `competes_with` | rival direto (mesmo tier) | Venice 2 ↔ Alexa 35 |
| `alternative_to` | substituto (qualquer tier) | FX6 → C400 |
| `budget_alternative_to` | versão barata de | Hollyland Pyro → Teradek Bolt `{ratio}` |
| `successor_of / predecessor_of` | linhagem | FX9 → FS7 |
| `accessory_for` | acessório de | Snapgrid → Light Dome |
| `certified_for` | aprovação formal | Alexa 35 → Netflix Approved |
| `interoperates_with` | trabalham juntos via padrão | Wisycom ↔ Sound Devices `{via: analog}` |

**Pessoas, processo e craft**

| aresta | significado | exemplo |
|---|---|---|
| `used_by_role / operated_by_role` | quem opera | switcher → TD; luz → gaffer |
| `part_of_department` | lotação | gaffer → G&E |
| `reports_to` | cadeia de comando | best boy → gaffer |
| `used_in_workflow` | onde entra no processo | DIT cart → dailies |
| `produces / consumes` | I/O de um workflow | offline → produz AAF |
| `template_for` | papelada ↔ processo | call sheet → diária `{dono: 1º AD}` |
| `enables_technique` | equipamento viabiliza técnica | volume LED → ICVFX |
| `requires` | pré-requisito | chroma key → luz uniforme + keyer |
| `governed_by` | norma → órgão | Rec.2020 → ITU-R |
| `supersedes` | substituição de norma/versão | ST 2110 → (caminho de) ST 2022-6 |
| `see_also` | associação livre | anamórfico ↔ 2.39:1 |

### 6.5 Vocabulário controlado (enums como nós)

Mounts, codecs, color spaces, transfer functions, battery mounts, protocolos, conectores e tiers **são arquivos** em `_meta/vocab/` ou `conceitos/`. Nenhum valor de aresta é texto livre. O CI (Seção 10) rejeita: aresta fora do vocabulário de `_meta/edge-vocabulary.md`, slug inexistente, id duplicado.

---

## 7. Estrutura do repositório

```
yad-brain/
├─ README.md                  # o que é, para quem, como navegar, convenções
├─ AGENTS.md                  # protocolo de consulta para o Claude (curto!)
├─ _meta/
│  ├─ ontology.md             # este esquema: nós, atributos, arestas
│  ├─ edge-vocabulary.md      # vocabulário FECHADO de arestas + propriedades
│  ├─ conventions.md          # slugs ASCII, unidades, idioma, aliases
│  ├─ vocab/                  # enums como nós
│  │   mount--pl.md  mount--e.md  mount--lpl.md  mount--rf.md  mount--l.md
│  │   bat--v-mount.md  bat--gold-mount.md  bat--b-mount.md ...
│  └─ templates/
│      _tmpl-equipamento.md  _tmpl-conceito.md  _tmpl-software.md
│      _tmpl-funcao.md  _tmpl-workflow.md  _tmpl-documento.md
├─ _moc/                      # Maps of Content (índices navegáveis)
│  ├─ 00-indice-mestre.md
│  ├─ moc--captacao.md  moc--luz.md  moc--pos.md  moc--live.md
│  ├─ moc--audio.md  moc--producao.md  moc--virtual-production.md
│  └─ moc--por-orcamento.md
├─ _index/                    # DERIVADOS por script (não editar à mão)
│  ├─ por-marca.md  por-mount.md  por-codec.md  por-funcao.md
│  └─ backlinks.md
├─ _graph/                    # DERIVADOS por script
│  ├─ graph.json  stats.md  orfaos.md
├─ marcas/                    # 1 hub por fabricante
│  ├─ arri.md  sony.md  blackmagic-design.md  canon.md  red.md
│  ├─ aputure.md  nanlux.md  astera.md  brompton.md  teradek.md ...
├─ captacao/
│  ├─ cameras/{arri,sony,red,blackmagic,canon,panasonic,...}/<modelo>.md
│  ├─ lentes/{cooke,zeiss,arri,angenieux,fujinon,sigma,dzofilm,laowa,...}/
│  ├─ adaptadores/  filtros/  matte-box/  fiz/
│  └─ acessorios/
├─ luz/
│  ├─ fixtures/{aputure,arri,nanlite,nanlux,astera,godox,kino-flo,...}/
│  ├─ modificadores/  gelatinas/  controle-dmx/  eletrica-distro/
├─ led-vp/
│  ├─ paineis/  processadores/  tracking/  media-servers/
├─ grip/
│  ├─ tripes-cabecas/  gimbals/  dollies/  gruas/  sliders/  ferragens/
├─ live/
│  ├─ switchers/{blackmagic,grass-valley,ross,sony,panasonic,vmix,...}/
│  ├─ conversores-roteamento/  encoders-streaming/  graficos/  intercom/
├─ monitoracao/
│  ├─ campo/  referencia/  scopes/
├─ gravacao-midia/
│  ├─ recorders/  midias/  leitores/  storage-pos/  dit/
├─ energia/
│  ├─ baterias/  carregadores/  distro-dc/  geradores-stations/
├─ wireless-sync/
│  ├─ video/  timecode/  genlock/
├─ audio/
│  ├─ microfones/  wireless/  mixers-recorders/  monitoracao-ifb/  acessorios/
├─ software/
│  ├─ nle/  color/  vfx/  3d/  render/  motion-design/  design-2d/
│  ├─ live-vp/  mam-review/  transcode-qc/  dit-dailies/  audio-pos/
│  ├─ previz/  producao-gestao/  roteiro/  ia-generativa/
│  └─ plugins/{after-effects,premiere,resolve,c4d,...}/
├─ conceitos/
│  ├─ codecs/  containers/  color-spaces/  transfer-functions/  luts/
│  ├─ pipelines-cor/  resolucoes/  frame-rates/  aspect-ratios/
│  └─ tecnicas/   # exposicao.md, obturador-180.md, chroma-key.md, icvfx.md...
├─ sinais-padroes/
│  ├─ interfaces/  # 12g-sdi.md, hdmi-2-1.md, ndi.md, st-2110.md, srt.md...
│  ├─ conectores/  # bnc.md, lemo.md, d-tap.md, powercon.md...
│  ├─ protocolos-controle/  # dmx512.md, art-net.md, crmx.md, visca.md...
│  └─ orgaos/      # smpte.md, itu-r.md, ebu.md, aces.md...
├─ producao/
│  ├─ funcoes/{direcao,camera,g-e,som,arte,producao,pos,vfx,live,vp}/
│  ├─ workflows/{pre,producao,pos,entrega,live}/
│  ├─ documentos/  # call-sheet.md, decupagem.md, mapa-de-luz.md...
│  └─ tipos-de-producao/
├─ glossario/
│  └─ glossario-a-f.md  glossario-g-m.md  glossario-n-z.md
└─ tools/                     # scripts de manutenção (Seção 10)
   ├─ build_graph.py  validate.py  staleness_report.py
   └─ ci.yml (GitHub Actions)
```

Racional: pastas espelham a ontologia (previsibilidade para Glob); subpasta por marca nos domínios volumosos (câmeras, lentes, fixtures, switchers) para o caminho ser adivinhável: `captacao/cameras/sony/venice-2.md`.

---

## 8. Formato da nota (a peça que faz tudo funcionar)

### 8.1 Esquema de frontmatter

```yaml
---
id: <slug único>            # obrigatório, imutável
title: <nome canônico>      # com acentos/maiúsculas normais
type: <tipo de nó>          # do vocabulário da Seção 6.3
brand: <slug da marca>      # se aplicável
category: <subcategoria>
aliases: [<apelidos, códigos de modelo, grafias com acento>]
tags: [<3–8 tags>]
status: stub | draft | reviewed
confidence: alta | media | baixa
updated: AAAA-MM-DD
rel:                        # ARESTAS — só vocabulário fechado, só slugs
  <aresta>: [<slug>, <slug>]
  <aresta>: [{to: <slug>, via: <slug>, nota: "<curta>"}]  # com propriedades
sources:
  - {url: "<url>", tier: oficial | comunidade | educacao, ret: AAAA-MM-DD, nota: "<o que veio daqui>"}
---
```

### 8.2 Estrutura do corpo (ordem fixa)

1. `# Título`
2. **`**TL;DR** — `** uma linha que resolve 80% das consultas (o grep com `-C2` devolve isso).
3. `## Specs-chave` — tabela ou linhas `chave: valor` (uma informação por linha; grep-friendly).
4. `## Posicionamento` — onde entra, contra quem compete, forças/fraquezas, para quem faz sentido.
5. `## Conexões` — prosa curta com wikilinks explicando *por que* as arestas existem.
6. `## Dicas de comunidade` — cada bullet **com citação** (fonte + tier); opinião nunca disfarçada de spec.
7. `## Gotchas` — pegadinhas reais de uso.

Regras de escrita: nota atômica (um conceito por arquivo); 300–900 tokens; **linhas auto-suficientes** (chave e valor na mesma linha, nunca espalhados em prosa); dividir a nota se passar de ~1.200 tokens; número sem fonte não entra — lacuna honesta é melhor que número inventado.

### 8.3 Exemplo preenchido — equipamento

> Os números abaixo são ilustrativos do formato; na execução real, cada um passa pelo fact-check da Seção 13 antes de `status: reviewed`.

```markdown
---
id: sony-venice-2
title: Sony VENICE 2
type: camera
brand: sony
category: cinema / full-frame
aliases: [VENICE 2, MPC-3610, Venice2]
tags: [full-frame, dual-base-iso, x-ocn, cinema-digital, 8k]
status: reviewed
confidence: alta
updated: 2026-07-23
rel:
  made_by: [sony]
  has_native_mount: [mount--e]
  accepts_mount: [{to: mount--pl, via: adaptador-pl-sony, nota: "PL removível"}]
  records_codec: [x-ocn, prores-422hq, xavc]
  records_to: [midia--axs]
  uses_battery_mount: [bat--bp-gl]
  supports_transfer_function: [s-log3]
  supports_colorspace: [s-gamut3-cine]
  competes_with: [arri-alexa-35, red-v-raptor-xl]
  successor_of: [sony-venice]
  certified_for: [netflix-approved]
  pairs_with: [sony-rialto-2]
  operated_by_role: [operador-de-camera, primeiro-ac]
  see_also: [dual-base-iso, x-ocn]
sources:
  - {url: "https://pro.sony/...", tier: oficial, ret: 2026-07-23, nota: "specs"}
  - {url: "https://reddit.com/r/cinematography/...", tier: comunidade, ret: 2026-07-23, nota: "experiência base 3200"}
---

# Sony VENICE 2

**TL;DR** — topo de linha de cinema digital da Sony: sensor full-frame 8.6K
(versão 6K disponível), dual base ISO 800/3200, grava X-OCN interno em mídia
AXS, mount E com trava + PL. Rival direta da ARRI Alexa 35; forte em baixa
luz e em rigs compactos via extensão Rialto.

## Specs-chave
| campo | valor |
|---|---|
| sensor_format | full-frame 8.6K (ou 6K, corpo idêntico) |
| dual_base_iso | 800 / 3200 |
| dynamic_range_stops | 16 (declarado Sony) |
| mount | E-mount com lever lock; PL por adaptador |
| codecs internos | X-OCN (XT/ST/LT), ProRes 422 HQ, XAVC |
| midia | cartões AXS (leitor AXS-AR3) |
| nd_interno | sim — 8 estágios (0.3–2.4) |

## Posicionamento
Disputa o mesmo mercado da [[arri-alexa-35]] em cinema e publicidade
high-end; leva vantagem em resolução/low-light, perde em simplicidade de
ecossistema de acessórios. O corpo destacável ([[sony-rialto-2]]) é o
diferencial em carros, cockpits e gimbal pesado.

## Conexões
Fluxo de cor nativo: [[s-log3]] + [[s-gamut3-cine]] → conform em
[[aces]] ou pipeline Sony. Mídia AXS exige leitor próprio no carrinho de
[[dit]]. ND interno de 8 estágios reduz dependência de [[filtro-nd]] no
matte box.

## Dicas de comunidade
- Base 3200 é utilizável para noite urbana com ruído fino; evitar subexpor
  e "levantar depois" — r/cinematography (comunidade).
- Rialto exige gerenciamento de cabo rigoroso em movimento — fórum
  CML (comunidade).

## Gotchas
- Cartões AXS e leitor são caros e exclusivos: orçar mídia junto com a diária.
- ProRes interno limita frame rates vs. X-OCN: conferir tabela por modo.
```

### 8.4 Exemplo preenchido — conceito

```markdown
---
id: filtro-nd
title: Filtro ND (densidade neutra)
type: conceito
category: optica / exposicao
aliases: [ND, neutral density, IRND, VND]
tags: [exposicao, filtro, optica, fotometria]
status: reviewed
confidence: alta
updated: 2026-07-23
rel:
  requires: []
  pairs_with: [matte-box]
  used_by_role: [primeiro-ac, gaffer]
  see_also: [exposicao, obturador-180, nd-interno, polarizador]
sources:
  - {url: "https://tiffen.com/...", tier: oficial, ret: 2026-07-23}
---

# Filtro ND (densidade neutra)

**TL;DR** — filtro cinza que corta luz sem (idealmente) alterar cor, para
manter diafragma aberto e obturador 180° sob sol. Densidades em stops:
ND0.3 = 1 stop, 0.6 = 2, 0.9 = 3, 1.2 = 4, 1.8 = 6, 2.1 = 7.

## Tipos
- fixo: qualidade máxima, um valor por vidro
- variável (VND): dois polarizadores; prático, mas risco de "X" escuro e
  dominante em densidades altas
- IRND: bloqueia infravermelho — essencial em sensores digitais com ND
  forte, evita pretos amarronzados/magenta

## Conexões
Regra do [[obturador-180]] + sol = ND quase obrigatório. Câmeras com
[[nd-interno]] (FX6, Venice, C400) reduzem a troca de vidro no
[[matte-box]]. Ver também [[polarizador]] para reflexos (efeito distinto).

## Gotchas
- VND barato em grande-angular: vinheta em cruz nas densidades altas.
- Empilhar ND + pola derruba ~1,5 stop extra e pode criar moiré de reflexo.
```

### 8.5 Por que este formato é barato (mecânica de tokens)

- O **TL;DR na primeira linha do corpo** faz `grep -i -C2 "venice"` devolver a essência sem `Read`.
- O **frontmatter** transforma pergunta estruturada em grep de campo: `grep -rl "records_codec:.*x-ocn"`.
- A **nota atômica** faz o `Read` completo custar ~500 tokens, não 20.000.
- Os **slugs previsíveis** fazem o Glob acertar de primeira, sem busca exploratória.

---

## 9. Índices: MOCs e índices cruzados

### 9.1 MOCs (Maps of Content) — os hubs do grafo

Um MOC por domínio (~100–250 linhas), curado, com uma linha por item: `[[slug]] — descrição de 10 palavras`. O Claude lê **um** MOC (barato) e salta para **uma** nota. Exemplo de trecho de `moc--luz.md`:

```markdown
# MOC — Luz & Elétrica

## COB / ponto (bowens)
- [[aputure-ls-600d-pro]] — COB 600W daylight, referência de custo-benefício
- [[aputure-electro-storm-xt26]] — 2600W bicolor, topo da linha 2025+
- [[nanlux-evoke-2400b]] — 2400W bicolor, rival direto do XT26
...

## Painéis
- [[arri-skypanel-s60-c]] — painel RGBW referência de estúdio
...

## Ver também
[[moc--captacao]] · [[moc--virtual-production]] · [[por-marca]]
```

### 9.2 Índices cruzados (derivados)

`_index/por-mount.md`, `por-codec.md`, `por-marca.md`, `por-funcao.md` — gerados pelo script a partir do frontmatter. Uma pergunta transversal ("o que grava ProRes internamente?") vira a leitura de **uma seção de um arquivo**, em vez de N greps + N reads. `_index/backlinks.md` responde "quem referencia X?" com um `Read` (o equivalente ao painel de backlinks do Obsidian, que o Claude não vê).

---

## 10. Grafo derivado: geração, validação e CI

**`tools/build_graph.py`** (roda em pre-commit e/ou GitHub Actions):
1. Percorre todo `.md`, parseia frontmatter.
2. Valida: id único; `type` conhecido; arestas ∈ `edge-vocabulary.md`; todo slug referenciado existe; datas válidas; `sources` presente quando `status != stub`.
3. Emite: `_graph/graph.json` (nós+arestas, para qualquer visualização/análise futura), `_index/*.md` (cruzados + backlinks), `_graph/orfaos.md` (notas sem nenhuma aresta de entrada/saída — sinal de nota isolada), `_graph/stats.md` (contagens por tipo/domínio/status — vira painel de progresso).
4. Falha o CI se houver: link quebrado, aresta fora do vocabulário, id duplicado, nota `reviewed` sem fonte oficial em spec numérica.

**`tools/staleness_report.py`**: lista notas com `updated` > N meses em categorias quentes (câmeras, software: 12 meses; conceitos estáveis: 36) — alimenta a rotina mensal (Seção 18).

Princípio inegociável: `_index/` e `_graph/` **nunca são editados à mão**; são sempre função do conteúdo. Não existe "segunda fonte de verdade".

---

## 11. Fontes e ingestão

### 11.1 Três tiers de procedência

| tier | o que é | peso |
|---|---|---|
| `oficial` | fabricante, spec sheet, manual, norma (SMPTE/ITU), documentação do software | fatos e números — única base aceitável para spec |
| `comunidade` | Reddit, fóruns (Lift Gamma Gain, CML, BMCuser…), grupos | experiência de campo, gotchas, opinião — sempre citada como tal |
| `educacao` | CineD, Newsshooter, No Film School, YouTube educativo, blogs de fabricante | síntese e testes de laboratório — intermediário |

### 11.2 Mapa de fontes por domínio

| domínio | oficial | comunidade | educação/news |
|---|---|---|---|
| Câmera/DoP | sites e spec sheets de fabricante | r/cinematography, CML, ReduserNet, BMCuser | CineD (lab tests), Newsshooter, Y.M.Cinema, No Film School |
| Lentes | fabricantes; tabelas de cobertura | r/cinematography, ShareGrid blog | CineD, reviews técnicos YouTube |
| Luz/gaffer/elétrica | fotometria Aputure/ARRI/Nanlux; IES files | r/gaffer, grupos BR de elétrica/gaffer | canais de gaffer no YouTube, Aputure edu |
| LED wall/VP | Brompton, ROE, Megapixel, Epic (VP Field Guide) | r/virtualproduction | Y.M.Cinema, Epic Learning |
| Cor/DaVinci | manuais e treinamentos Blackmagic (gratuitos) | **Lift Gamma Gain**, r/colorists | Mixing Light, canais de coloristas |
| Edição | docs Adobe/Avid/Apple | r/editors, r/premiere, Creative COW, Avid Community | Frame.io Insider, YouTube |
| VFX/Motion | docs Adobe/Foundry/Maxon | r/AfterEffects, r/vfx, r/motiondesign | School of Motion, Video Copilot |
| 3D/Unreal | docs Maxon/Epic/SideFX | r/Cinema4D, r/unrealengine, foros Blender | Epic Learning, Greyscalegorilla |
| Live/broadcast | docs Blackmagic/vMix/Ross/GV; NDI.tv | r/VIDEOENGINEERING, fórum vMix | ProVideo Coalition, NewscastStudio |
| Áudio p/ imagem | Sound Devices, Sennheiser, Lectrosonics | r/LocationSound, Gearspace (post) | Curtis Judd, produção de som YouTube |
| Produção/set | — (pouca fonte oficial) | r/Filmmakers, grupos BR de produção | StudioBinder blog, No Film School |

### 11.3 Métodos de ingestão por tipo de fonte

- **Spec sheets oficiais**: leitura + extração estruturada para o frontmatter; síntese em prosa própria; URL na fonte. Nunca colar tabelas inteiras.
- **YouTube**: seleção de canais/vídeos-chave por domínio → transcrição → destilação em bullets de "dica de comunidade/educação" com link e timestamp aproximado.
- **Reddit/fóruns**: threads de alta votação e threads recorrentes ("best X for Y") → destilar consenso e divergência; registrar ambos ("a comunidade diverge: A defende…, B contesta…").
- **Blogs/News (RSS)**: CineD/Newsshooter para lançamentos → alimenta a rotina mensal de atualização, não o corpo principal.
- **Conflito entre fontes**: spec oficial ganha para números; comunidade ganha para comportamento real de campo; quando irreconciliável, a nota registra o conflito explicitamente com as duas citações — o cérebro não arbitra o que não sabe.

### 11.4 Copyright e uso justo

- Proibido: reproduzir manuais, tabelas extensas ou textos integrais; hospedar PDFs de terceiros.
- Permitido: fatos (specs não são protegidas como expressão), síntese em palavras próprias, citação curta com atribuição, link para a fonte.
- Benefício colateral: o que é legalmente correto aqui é também o que mantém o acervo enxuto e barato de ler.

### 11.5 Prioridade de partida (maior cobertura por esforço)

1. Manuais/sites Blackmagic (Resolve + câmeras + ATEM — cobrem 4 domínios de uma vez).
2. CineD (lab tests padronizados de câmera: DR, rolling shutter, latitude).
3. Fotometria Aputure/ARRI/Nanlux (luz).
4. r/cinematography + Lift Gamma Gain (comunidade de maior sinal).
5. 3–4 canais educativos de referência por domínio (transcrições).

---

## 12. Qualidade, confiança e frescor

- **`status`**: `stub` (só frontmatter + TL;DR; vale criar para fechar o grafo) → `draft` (corpo completo, fontes coladas, sem verificação) → `reviewed` (fact-check da Seção 13 aprovado).
- **`confidence`**: `alta` (spec oficial confirmada) / `media` (secundária confiável) / `baixa` (inferido/conflitante — explicitado no corpo).
- **Regra anti-alucinação**: número sem fonte **não entra**. Campo vazio com `<!-- verificar -->` é aceitável; número inventado, não. Especificação de equipamento é o habitat natural da alucinação de LLM — o pipeline trata isso como risco nº 1.
- **Frescor**: `updated` em toda nota; categorias quentes (câmeras, softwares, firmware) auditadas em ≤12 meses pelo staleness report; conceitos estáveis (fotometria, teoria de cor) têm tolerância de 36 meses.
- **Firmware que muda spec** (ex.: câmera ganha codec novo): atualiza a nota e registra em `## Histórico` com data e versão — sem apagar o passado.

---

## 13. Pipeline de produção de conteúdo em escala (multiagente)

Fase 2 usa lotes de 10–20 entidades por vez, com quatro papéis encadeados:

```
[A] PESQUISADOR  → colhe: 1 fonte oficial + ≥2 comunitárias/educação por
                   entidade; extrai dados brutos COM URLs; não redige.
[B] REDATOR      → preenche o template (frontmatter + corpo) a partir do
                   material de A; marca confidence por campo; não inventa.
[C] VERIFICADOR  → adversarial: confere CADA número contra a fonte oficial;
                   rejeita ou rebaixa confidence; checa arestas (mount,
                   codec) contra o vocabulário; aprova → status: reviewed.
[D] INTEGRADOR   → roda build_graph.py; conserta links; atualiza MOCs;
                   dedup de aliases; abre 1 commit/PR pequeno por lote.
```

Regras do pipeline:
- Lote pequeno e homogêneo (ex.: "10 COBs da Aputure/amaran") — o verificador compara pares e pega inconsistência entre notas irmãs.
- O verificador tem instrução explícita de **tentar refutar**, não confirmar.
- Amostragem humana: ~10% das notas `reviewed` de cada lote conferidas por olho humano (Felype/equipe) no começo; relaxa conforme a taxa de erro cair.
- Métricas por lote: % specs rejeitadas pelo verificador (proxy de alucinação), tempo por nota, tokens por nota — para calibrar o processo.

---

## 14. Interface de consulta (AGENTS.md / Skill)

Rascunho do protocolo (arquivo curto, ~60 linhas, na raiz):

```markdown
# AGENTS.md — Como consultar este cérebro

Você está num acervo de conhecimento audiovisual estruturado como grafo
em Markdown. NÃO leia diretórios inteiros. Siga o protocolo:

1. IDENTIFIQUE o tipo da entidade da pergunta (câmera? lente? conceito?
   função? software?).
2. TENTE O CAMINHO DIRETO: os slugs são previsíveis —
   Glob "captacao/cameras/**/<slug-provavel>.md". Slugs são ASCII sem
   acento, kebab-case.
3. SE NÃO ACHAR: Grep case-insensitive pelo termo em "aliases:" e no
   título; tente a grafia com e sem acento.
4. PERGUNTA TRANSVERSAL ("tudo que...", "quais X têm Y"): leia o índice
   pronto em _index/ (por-marca, por-mount, por-codec) ANTES de sair
   grepando o acervo.
5. NAVEGUE PELO GRAFO: o frontmatter "rel:" lista as arestas tipadas.
   Siga os slugs. "quem aponta para cá" está em _index/backlinks.md.
6. VISÃO DE DOMÍNIO: leia o _moc/ correspondente (1 arquivo pequeno).
7. AO RESPONDER: cite as fontes da nota e respeite "confidence" e o tier
   (oficial vs comunidade). Se a nota diz "conflito", apresente os dois
   lados. Não invente números que não estão no acervo.
8. AO ESCREVER nota nova: use _meta/templates/, vocabulário de arestas de
   _meta/edge-vocabulary.md, e as convenções de _meta/conventions.md.
```

**Fluxos exemplificados com custo estimado:**

| pergunta | caminho | custo aprox. |
|---|---|---|
| "Specs da FX6" | Glob direto → Read 1 nota | ~600 tokens |
| "Que lentes cine encaixam na Pyxis?" | Read nota (mount no frontmatter) → Read seção de `por-mount.md` | ~900 tokens |
| "Gravei BRAW; como entro num pipeline ACES?" | nota do codec → aresta → nota do pipeline | ~1.300 tokens |
| "Alexa 35 vs Venice 2 vs Raptor" | 3 notas + seção do MOC | ~2.200 tokens |
| "Monta um mapa de luz para entrevista 2 pessoas" | conceito (3-point) + 2 fixtures + template mapa-de-luz | ~2.500 tokens |

Empacotamento como **Skill** (opcional na Fase 4): `SKILL.md` com descrição de gatilho ("base de conhecimento audiovisual: equipamentos, cor, set…") — ~100 tokens residentes; o corpo replica o protocolo acima. Em sessões de Claude Code dentro do repo, o `AGENTS.md` já cumpre o papel.

---

## 15. Camadas opcionais futuras (com gatilhos objetivos)

| camada | o que adiciona | gatilho para ativar | forma correta de implementar |
|---|---|---|---|
| **pgvector (Supabase)** | busca semântica ("acha o parecido") | benchmark mostra classe recorrente de perguntas semânticas que grep+aliases não resolvem (>10% do eval por 2 trimestres) | embeddar notas; a ferramenta devolve **caminho + linhas**, nunca chunks — o Read continua local (precisão e frescor preservados). "Catálogo de fichas", não "os livros". |
| **LazyGraphRAG** | síntese global ("resuma todas as abordagens de X no acervo") | necessidade real de relatórios panorâmicos | rodar **offline, sob demanda**; o resultado vira uma nota comum do acervo. Nunca infra permanente. |
| **Visualização do grafo** | mapa visual para humanos além do Obsidian | interesse do time | página estática gerada de `graph.json` (D3/Sigma) publicada via GitHub Pages. |
| **MCP server próprio** | expor o cérebro a outros clientes (fora do Claude Code) | uso fora do Claude Code | wrapper fino sobre grep/read do repo — a fundação não muda. |

---

## 16. Roadmap detalhado

> Sem prazos-calendário rígidos (premissa: "sem pressa"); esforço em **sessões de trabalho** (1 sessão ≈ um bloco focado de algumas horas, humano + Claude).

### Fase 0 — Fundação (1–2 sessões)
Entregáveis: `README.md`, `AGENTS.md`, `_meta/ontology.md`, `_meta/edge-vocabulary.md`, `_meta/conventions.md`, templates, decisões de idioma/slug ratificadas.
**Aceite:** um terceiro (humano ou LLM) consegue criar uma nota válida lendo só `_meta/` + templates.

### Fase 1 — Esqueleto + exemplares (1–2 sessões)
Entregáveis: árvore de pastas completa; MOCs iniciais (vazios ou mínimos); `_meta/vocab/` com os enums centrais (mounts, battery mounts, codecs base); **8–12 notas exemplares** cobrindo todos os templates (2 câmeras, 2 lentes, 1 fixture, 1 painel LED, 1 switcher, 1 software, 2 conceitos, 1 função, 1 documento); `tools/validate.py` + CI rodando.
**Aceite:** CI verde; as 5 consultas-exemplo da Seção 14 executáveis de verdade com os custos previstos (±50%).

### Fase 2 — Conteúdo em ondas (a espinha do projeto; semanas–meses, em lotes)
Ordem proposta (cada onda usa o pipeline da Seção 13):
- **2a Captação** (~350–450 notas): câmeras das marcas principais, lentes cine, mounts/adaptadores, filtros, FIZ, mídias. *Justificativa de ser a 1ª: é o subgrafo mais conectado — fixa o padrão de todo o resto.*
- **2b Luz & elétrica** (~250–350): fixtures, modificadores, gelatinas, DMX/controle, distro/energia.
- **2c Pós** (~300–400): softwares, plugins principais, codecs, color spaces/curvas, pipelines de cor, workflows de conform/entrega.
- **2d Live & broadcast** (~200–300): switchers, conversão/roteamento, NDI/ST2110, encoders, intercom, gráficos.
- **2e Produção, funções & documentos** (~200–300): todas as funções por departamento, workflows por fase, templates de documentos.
- **2f Áudio + wireless/sync + monitoração + grip + LED/VP** (~400–500): completa os domínios restantes.
**Aceite por onda:** ≥90% das notas `draft`→`reviewed`; CI verde; MOC do domínio completo; amostragem humana sem erro grave.

### Fase 3 — Grafo & índices (contínua, automatizada a partir da 2a)
`build_graph.py` + índices cruzados + backlinks + relatório de órfãos rodando em CI a cada push.
**Aceite:** zero órfãos não-intencionais; índices cruzados cobrindo mount/codec/marca/função.

### Fase 4 — Otimização de acesso (1–2 sessões, após 2 ondas concluídas)
Skill empacotada; primeira rodada completa do benchmark (Seção 17); ajustes de MOC/índices guiados pelos erros do benchmark; decisão informada sobre camada semântica (Seção 15).
**Aceite:** benchmark ≥85% de acerto de recuperação com custos dentro do alvo (3.3).

### Fase 5 — Operação contínua (permanente)
Rotina mensal (Seção 18); expansão sob demanda (novos lançamentos, novos domínios como fotografia still, drones/regulação, IA generativa aplicada).

---

## 17. Avaliação contínua (benchmark de recuperação)

Criar `_meta/eval/perguntas.md` com **60 perguntas-teste** reais, 10 por categoria:
1. *Lookup direto* — "qual o dual base ISO da Venice 2?"
2. *Travessia/compatibilidade* — "que lentes EF funcionam na FX6 e via quê?"
3. *Comparativa* — "Electro Storm XT26 vs Evoke 2400B: qual leva pra externa?"
4. *Workflow* — "fluxo de proxy do BRAW pro Premiere e volta pro Resolve"
5. *Comunidade/gotcha* — "pegadinhas de VND em grande-angular?"
6. *Transversal* — "tudo da Blackmagic que entra num fluxo ao vivo com NDI"

Cada pergunta tem gabarito: arquivo(s) que deveriam ser tocados + fatos-chave da resposta. Medição (trimestral, ou após cada onda): **acerto de recuperação** (achou os arquivos certos em ≤2 chamadas?), **correção factual** (resposta bate com o gabarito?), **custo** (tokens lidos), **profundidade** (usou as arestas ou respondeu raso?). Os erros viram backlog de melhoria de MOC/aliases/índices — é assim que a estrutura evolui guiada por dado, não por opinião.

---

## 18. Governança e manutenção

- **Rotina mensal (≤1 sessão):** varrer lançamentos (CineD/Newsshooter/press releases) → criar stubs do que importa → atualizar notas afetadas por firmware/preço/descontinuação → rodar staleness report → triagem de issues.
- **Issues do GitHub** como fila de lacunas: qualquer um do time abre "falta nota do X" ou "spec Y parece errada".
- **Convenções são lei**: mudança de ontologia/aresta exige atualizar `_meta/` + script de migração das notas afetadas no mesmo PR (nunca deixar o acervo meio-migrado).
- **Branch/commit**: trabalho em branches por lote; PRs pequenos; mensagem de commit descreve o lote ("luz: 12 COBs Aputure/amaran reviewed").
- **Backup**: Git já é o backup primário; mirror opcional.
- **Privacidade**: repo privado; nada de dados de clientes/projetos da YAD (restrição 3.4).

---

## 19. Riscos e mitigações

| # | risco | prob. | impacto | mitigação |
|---|---|---|---|---|
| R1 | **Alucinação de specs** em escala | alta | alto | pipeline com verificador adversarial (S.13); regra "número sem fonte não entra"; confidence por campo; amostragem humana |
| R2 | **Deriva de vocabulário** (arestas/tipos inventados ao longo do tempo) | média | alto | vocabulário fechado + CI que rejeita aresta desconhecida |
| R3 | **Acento/Unicode quebrando grep** | certa (se ignorada) | médio | slugs ASCII; aliases com acento; protocolo manda tentar as duas grafias |
| R4 | **Notas inchando** (perde-se a propriedade "grep devolve a resposta") | média | médio | limite de ~1.200 tokens; CI avisa; dividir e linkar |
| R5 | **Abandono/estagnação** após entusiasmo inicial | média | alto | ondas pequenas com aceite claro; rotina mensal curta; stats.md mostra progresso (motivação) |
| R6 | **Copyright** (colagem indevida de manual) | baixa | alto | política da S.11.4 no `conventions.md`; verificador checa |
| R7 | **Obsolescência silenciosa** (firmware muda, nota não) | alta | médio | staleness report; rotina mensal; campo `updated` |
| R8 | **Ontologia over-engineered** (atrito para criar nota simples) | média | médio | template mínimo válido = frontmatter + TL;DR (stub); atributos são opcionais exceto id/type/status |
| R9 | **Dependência de uma pessoa** | média | médio | tudo documentado em `_meta/`; qualquer LLM/humano consegue continuar lendo só o repo |
| R10 | **Convenção errada descoberta tarde** | baixa | alto | Fases 0–1 curtas + avaliação externa (este documento) antes de escalar; migrações sempre scriptáveis (texto puro) |

---

## 20. Métricas de sucesso (KPIs)

1. **Recuperação:** ≥90% das perguntas do benchmark acham os arquivos certos em ≤2 chamadas de ferramenta.
2. **Custo:** mediana ≤2.500 tokens lidos por consulta; p95 ≤6.000.
3. **Qualidade:** 100% notas com `sources`; ≥85% do acervo `reviewed` ao fim de cada onda; taxa de rejeição do verificador < 5% nos lotes finais (proxy de que o processo aprendeu).
4. **Integridade:** 0 links quebrados / 0 arestas inválidas / 0 órfãos não-intencionais no CI.
5. **Cobertura:** Apêndice B atingido por domínio (±20%).
6. **Vitalidade:** rotina mensal executada; staleness < 10% nas categorias quentes.
7. **Uso real:** o cérebro responde consultas do dia a dia sem recorrer à web na maioria dos casos (medível pelo próprio uso nas sessões).

---

## 21. Decisões em aberto (com recomendação)

| # | decisão | opções | recomendação |
|---|---|---|---|
| D1 | Idioma | (a) PT com termos técnicos EN; (b) tudo PT; (c) bilíngue | **(a)** — é como o set fala ("full-frame", "log", "mount"); mais barato que bilíngue; slugs sempre ASCII |
| D2 | Domínio da 1ª onda | captação / luz / pós / live | **captação** — subgrafo mais conectado; fixa o padrão |
| D3 | Fundação sem camada semântica | sim / não | **sim** — pgvector só mediante gatilho da S.15 |
| D4 | Visibilidade do repo | privado / público | **privado** no início; abrir partes é decisão futura de negócio |
| D5 | Templates de documentos da YAD entram? | sim / não | **não** — violaria o isolamento; criar templates *genéricos* de mercado |
| D6 | Ferramenta de CI | GitHub Actions / pre-commit local / ambos | **ambos** (validação local rápida + Actions como guarda) |

---

## Apêndice A — Marcas e fabricantes por categoria (semente, expansível)

*Marcações: [P] premium/high-end · [$] valor/entrada · [R] rental-only. Lista de partida — o acervo cobrirá cada marca com nota-hub própria e notas por produto conforme relevância.*

**Câmeras cinema:** ARRI [P] · Sony (VENICE/BURANO/FX) · RED (Nikon) [P] · Blackmagic Design · Canon (Cinema EOS) · Panasonic (VariCam/EVA) · Z CAM · Kinefinity · DJI (Ronin 4D) · Vision Research/Phantom (high-speed) [P] · Freefly (Ember) · Panavision [R].
**Broadcast/sistema & PTZ:** Sony (HDC/HXC) · Grass Valley (LDX) · Ikegami · Hitachi · Panasonic (AK/AW-UE) · JVC · Canon · Sony FR7 · PTZOptics · BirdDog · Marshall.
**Mirrorless/híbridas:** Sony Alpha · Canon R · Nikon Z · Panasonic LUMIX · Fujifilm X/GFX · Leica · Sigma fp · OM System.
**Ação/360/drone:** GoPro · DJI (Osmo/Action/Mavic/Inspire) · Insta360 · Freefly (Alta/Astro) · Autel.

**Lentes cine:** Cooke [P] · ZEISS (Supreme/Nano/CP.3) · ARRI Signature [P] · Angénieux (Optimo) [P] · Leitz [P] · Fujinon (Premista/Cabrio + broadcast) · Canon (Sumire/CN-E/zoom broadcast) · Panavision [R] · Hawk/Vantage [R] · Tokina · Sigma Cine · Laowa (Ranger/Nanomorph/Probe) · DZOFilm (Vespid/Pictor/Arcana) · Sirui [$] · Blazar (anamórficas) · Atlas (Orion/Mercury) · XEEN/Samyang · Meike [$] · NiSi (Athena) · 7Artisans [$] · Vazen · SLR Magic · rehousing: P+S Technik · TLS · Zero Optik · IronGlass [$].
**Lentes foto:** nativas (Canon RF, Nikon Z, Sony FE, Fuji XF/GF, L-mount Alliance) · Sigma Art · Tamron · Samyang · Viltrox [$] · Voigtländer · Zeiss (Otus/Batis/Loxia) · TTArtisan [$] · Irix.
**Acessórios ópticos:** matte box: Bright Tangerine · ARRI · Tilta · Wooden Camera · Vocas · SmallRig [$]. Filtros: Tiffen (Black Pro-Mist) · Schneider · Formatt-Hitech · NiSi · PolarPro · Lee · Hoya · B+W. Adaptadores: Metabones · Sigma MC · Fringer · Techart · Novoflex · Kipon. FIZ: Preston [P] · ARRI (Hi-5/cforce) · cmotion · Teradek RT · Tilta Nucleus [$] · DJI Focus Pro (LiDAR).

**Luz:** Aputure · amaran [$] · ARRI (SkyPanel/L-series/HMI/tungstênio) [P] · Nanlite · Nanlux · Litepanels · Kino Flo · Quasar Science · Creamsource · Astera (Titan/Helios) · Godox [$] · Rotolight · Fiilex · DMG/Rosco · Hive · VELVET · Lupo · Dedolight · K5600 (Joker) · Mole-Richardson · Westcott · Zhiyun/Colbor/GVM/Neewer [$]. Entretenimento (crossover): Robe · Claypaky · Martin · Ayrton · Vari-Lite · ETC (Source Four/consoles) · Chauvet Pro · Astera. Balão/especiais: Airstar · SoftSun. Gelatinas/difusão: Rosco · LEE. Modificadores: DoPchoice (Snapbag/Snapgrid) · Chimera · Matthews (bandeiras/grip de luz) · Avenger/Manfrotto.

**LED wall & VP:** Painéis: ROE Visual [P] · INFiLED · Absen · Unilumin · AOTO · Sony (Crystal LED/VERONA) · Samsung (The Wall) · LG · Leyard/Planar · Desay. Processamento: Brompton (Tessera) [P] · Megapixel (HELIOS) [P] · NovaStar (MX/COEX) · Colorlight · Barco · Christie. Tracking: Mo-Sys (StarTracker) · stYpe · Ncam · OptiTrack · Vive Mars. Servers/engine: Disguise · Unreal (nDisplay) · Notch · Pixotope · Zero Density · Aximmetry.

**Grip & suporte:** Sachtler · Vinten · OConnor [P] · Cartoni · Miller · Ronford-Baker [P] · Manfrotto/Gitzo/Avenger · Benro/E-Image [$] · Kessler · Edelkrone · Zeapon [$] · Chapman/Leonard [R] · J.L. Fisher [R] · Panther [R] · Egripment [R] · Dana Dolly · Technocrane/Supertechno [R] · Scorpio [R] · MovieBird [R] · Stanton (Jimmy Jib) · Steadicam/Tiffen [P] · Flowcine · Easyrig · ARRI (Trinity/SRH) · Freefly (MōVI) · DJI (RS/Ronin 2) · Zhiyun/Moza [$] · MRMC (Bolt) [P] · Motorized Precision · Matthews · Modern · Kupo.

**Live/broadcast:** Switchers: Blackmagic (ATEM) · Grass Valley (K-Frame/Kayenne/AMPP) · Ross (Carbonite/Acuity/Ultrix) · Sony (XVS/MVS) · Panasonic (KAIROS/AV-HS) · NewTek-Vizrt (TriCaster) · vMix · Roland · FOR-A · Analog Way · Datavideo [$] · OBS (free). Gráficos: Vizrt · Chyron · Ross XPression · Brainstorm · Singular.live · CasparCG (free). Replay: EVS [P] · GV LiveTouch · Ross Dreamcatcher. Intercom: Clear-Com · RTS · Riedel (Bolero) [P] · Green-GO · Hollyland (Solidcom) [$]. Roteamento/IP: Evertz · Lawo · Nevion · Imagine · AJA · Blackmagic (Videohub) · Magewell · Kiloview · BirdDog (NDI).

**Monitoração:** Campo: SmallHD · Atomos · TVLogic · Osee · Portkeys [$] · Feelworld/Lilliput [$] · SWIT · Blackmagic (Video Assist). Referência: Flanders Scientific [P] · Sony BVM/PVM [P] · Canon DP-V [P] · Eizo · Postium · Konvision · Apple XDR (client). Scopes: Leader/Phabrix [P] · Telestream Prism · Tektronix · AJA · Nobe (software).

**Gravação & mídia:** Recorders: Atomos · Blackmagic (HyperDeck) · AJA (Ki Pro) · Cinedeck. Cartões: SanDisk Pro · Angelbird · ProGrade · Sony TOUGH · Lexar · Delkin · Wise · Nextorage · OWC. Proprietárias: RED MINI-MAG · Codex/ARRI Compact Drive · Sony AXS/SxS · Panasonic P2/expressP2. Storage pós: OWC · LaCie · Promise · Synology · QNAP · EditShare · Facilis · Quantum (StorNext) · Dell PowerScale. DIT: Blackjet · Sonnet.

**Energia:** Anton/Bauer [P] · IDX · Core SWX · Bebob · BLUESHAPE · SWIT · Hawk-Woods · PAG · Fxlion · Dynacore [$]. B-Mount: consórcio ARRI+Bebob+Core. Stations: EcoFlow · Bluetti · Goal Zero · Anker. Geradores: Honda · Multiquip/Whisperwatt · tow plants [R].

**Wireless & sync:** Vídeo: Teradek (Bolt/Serv/Prism) [P] · Vaxis · Hollyland (Mars/Pyro) [$] · Accsoon [$] · DJI (Transmission/SDR) · Boxx [P] · CINEGEARS · SWIT. Timecode: Tentacle Sync · Deity (TC-1) · Atomos-Timecode Systems (UltraSync) · Ambient (Lockit/NanoLockit) · Betso · Denecke · Mozegear. Genlock/PTP: AJA · Blackmagic · Evertz · Meinberg.

**Áudio:** Mics: Sennheiser (MKH 416/8060) · Schoeps (CMIT) [P] · Sanken (CS/COS-11) [P] · DPA (4017/4060/6060) [P] · Neumann · Rode (NTG) · Audio-Technica · Shure (SM7B) · Countryman (B6) · Deity [$] · Electro-Voice (RE20). Wireless: Lectrosonics [P] · Wisycom [P] · Sennheiser (EW-DX/6000) · Shure (Axient/ULX-D) · Zaxcom · Sony (DWX/UWP) · Rode (Wireless Pro) [$] · DJI Mic [$] · Deity Theos [$] · Hollyland Lark [$]. Mixers/recorders: Sound Devices (MixPre/8-series) [P] · Zaxcom [P] · Aaton (Cantar) [P] · Sonosax [P] · Zoom (F-series) [$] · Tascam [$]. Acessórios: Rycote · Cinela [P] · Bubblebee · K-Tek · Ambient · Ursa · Remote Audio. IFB: Comtek · Lectrosonics · Sennheiser. Monitoração: Sony 7506 · Sennheiser HD 25 · Beyerdynamic DT · Genelec/Neumann/ATC/Focal (salas).

**Software:** NLE: DaVinci Resolve · Premiere Pro · Final Cut Pro · Media Composer · EDIUS · Vegas · Lightworks · Kdenlive (free). Cor: Resolve · Baselight [P] · Flame/Lustre · Assimilate SCRATCH · Colorfront · Pomfort Livegrade · Colourlab AI. VFX: Nuke [P] · After Effects · Fusion · Flame · Boris FX (Sapphire/Mocha/Continuum/Silhouette) · RE:Vision · Natron (free). 3D: Cinema 4D · Maya · 3ds Max · Houdini · Blender (free) · ZBrush · Substance 3D · Modo. Render: Redshift · Octane · V-Ray · Arnold · RenderMan · Cycles · Unreal · Unity. Motion/design: AE · C4D · Cavalry · Notch · Motion · Photoshop · Illustrator · Affinity · Figma. Live/VP: Unreal · Disguise · TouchDesigner · Resolume · Hippotizer · Pixera · WATCHOUT · Ventuz · vMix · OBS · Wirecast. MAM/review: Frame.io (C2C) · Iconik · CatDV · Flow/ShotGrid · ftrack · Kitsu (free). Transcode/QC: Vantage · Elemental · Transkoder · Baton · Shutter Encoder (free) · HandBrake (free) · FFmpeg (free) · Media Encoder. DIT/dailies: Silverstack · Livegrade · YoYotta · Hedge/OffShoot · ShotPut Pro · Codex Suite · QTAKE (video assist) [P]. Previz: FrameForge · Shot Designer · Cine Tracer · Unreal. Gestão/roteiro: Movie Magic · StudioBinder · Yamdu · Final Draft · Celtx · WriterDuet. Áudio pós: Pro Tools [P] · Nuendo · Logic · Fairlight · Audition · Reaper · iZotope RX · Waves · FabFilter. IA (produção): Runway · Topaz · Firefly · Sora · Veo · Kling · Luma · ElevenLabs · Descript · Colourlab.

**Órgãos e programas:** SMPTE · ITU-R · EBU · AMPAS/ACES · DCI · AES · ASC (CDL) · AIMS (ST 2110) · Netflix Post Technology Alliance · CineD Lab (referência de teste).

---

## Apêndice B — Estimativa de volume por domínio (alvo 12 meses)

| domínio | notas (aprox.) |
|---|---|
| Câmeras (todas as classes) | 120 |
| Lentes cine + foto + acessórios ópticos + FIZ | 250 |
| Mounts, adaptadores, filtros, mídias, baterias (enums+produtos) | 150 |
| Luz (fixtures, modificadores, gelatinas, controle, elétrica) | 280 |
| LED wall & VP | 60 |
| Grip & movimento | 120 |
| Live & broadcast (switchers→intercom) | 180 |
| Monitoração & scopes | 60 |
| Gravação, storage & DIT | 90 |
| Wireless & sync | 50 |
| Áudio | 160 |
| Software + plugins | 200 |
| Conceitos (codecs, cor, técnicas, exposição…) | 250 |
| Sinais, padrões, conectores, protocolos, órgãos | 90 |
| Produção: funções, workflows, documentos, tipos | 160 |
| Marcas (hubs) | 150 |
| Glossário/MOCs/meta | 60 |
| **Total** | **~2.400** |

Com média de ~500 tokens/nota → acervo de ~1,2 M tokens. Custo de consulta continua sendo o de **1–3 notas** (~1–2,5 k tokens): o acervo cresce, a consulta não.

---

## 24. Perguntas ao avaliador (ChatGPT)

Pedimos avaliação crítica e, se possível, respostas diretas a estas questões:

1. **Arquitetura** — A tese "filesystem + grep como fundação, sem camada vetorial/grafo-DB" sustenta-se para um acervo de ~2.400 notas consultado por LLM com ferramentas de arquivo? Em que ponto de escala ou tipo de pergunta você prevê que ela quebre primeiro?
2. **Ontologia** — O vocabulário de ~40 arestas está bem dimensionado? Está faltando alguma relação importante do domínio audiovisual, ou há arestas redundantes que você fundiria?
3. **Formato da nota** — O template (frontmatter tipado + TL;DR + linhas auto-suficientes) maximiza mesmo a eficiência de tokens? Que mudança você faria?
4. **Anti-alucinação** — O pipeline pesquisador→redator→verificador adversarial→integrador (S.13) é suficiente contra specs inventadas em escala? Que salvaguarda adicional você adicionaria?
5. **Roadmap** — A ordem das ondas (captação → luz → pós → live → produção → resto) é a melhor? Os critérios de aceite por fase estão certos?
6. **Benchmark** — O desenho de avaliação (S.17) mede o que importa? Que categorias de pergunta faltam?
7. **Riscos** — Que risco relevante não está na tabela da S.19?
8. **Idioma** — Concorda com PT + termos técnicos EN + slugs ASCII (D1)? Vê problema prático que não antevimos?
9. **Visão geral** — Se você fosse vetar UMA decisão deste plano, qual seria e por quê? E qual é, na sua leitura, o ponto mais forte do desenho?

*Contexto para o avaliador: o consumidor primário é Claude (Anthropic) operando com ferramentas de leitura de arquivos (`Grep`/`Glob`/`Read`) dentro do repositório; o consumidor humano usa Obsidian/GitHub sobre os mesmos arquivos. O plano será revisado à luz da sua avaliação antes de qualquer execução.*

---

*Fim do documento — v1.0, 2026-07-23. Nada foi executado: o repositório `yad-brain` permanece vazio até a aprovação deste plano.*
