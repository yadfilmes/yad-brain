# Parecer — YAD Proposal Experience v1.0

**Documento analisado:** `YAD_Proposal_Experience_Planejamento.md` (v1.0, 10/08/2026)
**Data do parecer:** 10 de agosto de 2026
**Postura:** arquiteto de software + engenharia de produto, adversarial por instrução do próprio plano (§64: "não assumir que a arquitetura está correta")

> **Nota de escopo.** Este documento trata de **outro projeto** que não o YAD BRAIN. Está arquivado aqui em `_meta/history/` por conveniência de versionamento; não faz parte do acervo de conhecimento audiovisual e não é validado pelo `tools/validate.py`. Se o Proposal Experience ganhar repositório próprio, este arquivo migra para lá.

---

## 1. Veredito em uma página

O plano está **acima da média de planos técnicos** e o diagnóstico central está correto: biblioteca de componentes em vez de templates, conteúdo separado de design, IA como camada de comando sobre um sistema validado — e não como geradora de código. As três ideias que sustentam o produto (§3.1, §7, §45) são as certas, e a ordem proposta no roadmap (proposta real primeiro, plataforma depois) é rara e madura.

Os problemas não estão na filosofia. Estão em três lugares:

**1. Escala.** O plano descreve um produto para vender a outras agências, não uma ferramenta interna para uma produtora. Payload + PostgreSQL + S3 + renderer Astro + camada de IA + Client DNA + versionamento + analytics + aprovação + export offline é de 6 a 12 meses de trabalho para um time pequeno. A Fase 1 está certa; as Fases 6–10 são uma startup.

**2. Está gerenciando o risco errado.** O plano cuida com esmero do risco *técnico* (performance, fallback, lock-in) e quase não cuida do risco *real*: o de o design system nunca convergir. O problema mais difícil deste projeto não é Astro vs Next — é que **"cada cliente parecer personalizado" (§62) e "sistema opinionado, componentes reutilizáveis" (§61.8) estão em tensão direta.** Essa tensão *é* o projeto. Resolvê-la é escolher onde mora a personalidade: nos tokens, não nos layouts (§6 desta análise).

**3. Três decisões concretas de arquitetura precisam mudar** — a mais importante sendo a separação Studio/Renderer em dois apps, que é a maior fonte de dívida técnica do plano inteiro.

**Se eu pudesse mudar uma única linha do plano:** trocar "Renderer: Astro + React Islands, projeto separado" por "um único app Next.js". Isso resolve, de uma vez, as perguntas 3, 4 e 7 da própria lista de §63.

---

## 2. O que o plano acerta (e não deve ser mexido)

| Acerto | Por quê importa |
|---|---|
| §3.1 — IA não gera HTML/CSS/JS do zero | É a diferença entre um produto e um gerador de bugs. Correto e não-negociável. |
| §7 — conteúdo independente da camada visual | É o que faz "R$ 385.000 → R$ 370.000" ser um campo, não um redesign. |
| §45 — o ativo é o design system, não a tecnologia | Verdade literal. Toda a stack é substituível; o sistema visual não. |
| §49–52 — proposta real antes de plataforma | Inverte o erro clássico. Mantenha essa ordem com unhas e dentes. |
| §61.1 — não antecipar complexidade | Princípio certo. O próprio plano o viola (ver §7 desta análise). |
| §66 — regra de ouro (3D só se agregar) | Correta. Eu apenas a aplicaria com mais violência do que o plano aplica. |
| §11 — três níveis de intensidade | Boa ideia de produto: transforma "quanto capricho?" numa escolha explícita em vez de uma negociação interna. |

---

## 3. As três correções que mudam o projeto

### 3.1 Um app, não dois — Next.js, sem Astro

O plano propõe Payload (que é Next.js) para o Studio **e** Astro para o Renderer. O problema: **Payload v3 não é um backend separado — ele se instala dentro do seu app Next.js**, na pasta `app/(payload)`. Ou seja: você já tem um Next.js rodando. Acrescentar Astro significa:

- dois build systems, dois bundlers, duas configurações de fonte e asset;
- **duas bibliotecas de componentes** — ou uma package compartilhada que precisa compilar para os dois (o pior dos mundos);
- lógica de preview duplicada — que é exatamente a pergunta 7 de §63 ("como implementar preview sem duplicar lógica?"). Essa pergunta não tem resposta boa dentro da arquitetura proposta; ela tem resposta trivial fora dela;
- dois deploys, dois domínios, duas superfícies de bug.

Num único app Next.js, **os mesmos componentes React renderizam o Live Preview do admin e a proposta pública.** O Live Preview do Payload existe precisamente para isso: renderiza seu front-end dentro do painel e atualiza enquanto você digita, sem salvar.

**"Mas Astro entrega menos JavaScript."** Entrega — e a vantagem é real e mensurável para sites de conteúdo. Só que aqui ela é pequena diante do custo: o JS que uma proposta realmente carrega é dominado por GSAP (~50–70 KB gzip com ScrollTrigger) e, se houver, Three.js (150 KB+) — não por React. E o App Router com React Server Components já envia **zero JS** para as seções estáticas. A vantagem das ilhas do Astro sobre RSC em 2026 é menor do que o custo de operar dois apps.

Regra geral: **Astro é a resposta certa para um site de conteúdo com 500 páginas e nenhum acoplamento a CMS; é a resposta errada quando seu CMS é um app Next.js e seu requisito nº 1 de UX é preview em tempo real (§18).**

*(Isso não é um demérito do Astro. Astro 6 saiu em março/2026 com a Environment API do Vite, Fonts API e CSP API, e a Astro Technology Company foi adquirida pela Cloudflare em janeiro/2026, seguindo MIT e open source. Se um dia o renderer for desacoplado do CMS, Astro 6 + Cloudflare é uma excelente casa.)*

### 3.2 Publicar = congelar

A pergunta 19 de §63 — "como versionar componentes sem quebrar propostas antigas?" — tem duas respostas. A cara: manter `hero@1`, `hero@2`, `hero@3` vivos para sempre, cada proposta antiga fixando sua versão. É o que fazem produtos com milhares de clientes. Para um time pequeno é uma âncora.

A barata: **no momento de publicar, a proposta vira um snapshot estático imutável** — HTML + assets renderizados e guardados. A proposta enviada nunca mais depende do código atual. Você pode reescrever a biblioteca inteira na segunda-feira e a proposta da BYD de março continua idêntica ao que o cliente viu.

Consequências, todas boas:

- **Q19 desaparece.** Não existe "quebrar proposta antiga".
- **Q4 ("gerar versões estáticas independentes") ganha resposta natural** — o snapshot *é* a versão estática, gerado uma vez no publish, não um build por proposta.
- **§37 e §38 (standalone e export offline) viram quase de graça** — o snapshot mais os assets já são o `.zip`.
- **§20 (versionamento V1/V2/V3)** fica honesto: cada versão publicada é um snapshot próprio, comparável, restaurável, e o cliente que abriu a V2 continua vendo a V2.

O registro editável (no CMS ou no repo) e o artefato publicado passam a ser **duas coisas diferentes**. Essa separação é a decisão mais barata e de maior efeito do projeto inteiro.

### 3.3 A IA e a interface chamam a mesma API de comandos

O plano trata prompt (§12.3) e interface (§12.1, §12.2) como dois caminhos, e depois pede que "prompt não seja obrigatório" (§13). Do jeito que está descrito, isso significa implementar duas vezes.

A saída: **toda mutação de uma proposta é uma função tipada.** Um módulo `commands.ts` com um conjunto pequeno e fechado:

```
setInvestment(value, currency)      swapBlockVariant(blockId, variant)
setValidity(days)                   reorderSections(fromIndex, toIndex)
setDirection(direction)             insertBlock(type, variant, atIndex)
setMotionIntensity(0..3)            removeBlock(blockId)
setCopy(blockId, field, text)       setClientDNA(clientId)
```

A interface chama essas funções. A camada de IA chama **as mesmas funções**, expostas como *tools* com schema estrito. Não existe caminho de código em que o modelo escreva o objeto inteiro.

Isso responde a Q6 e Q7 de §64 de uma vez, e responde melhor do que "structured JSON": ver §8 desta análise.

---

## 4. O que mudou no mundo desde que o plano foi escrito

Cinco fatos de 2025–2026 que alteram decisões específicas do documento.

| Fato | Efeito no plano |
|---|---|
| **Figma comprou a Payload (jun/2025).** Licença MIT e self-hosting inalterados; **inscrições novas no Payload Cloud pausadas**; a v4 é um redesenho do admin em linguagem Figma e seguia em beta pré-produção em meados de 2026. | Payload continua defensável — mas **self-host, não Payload Cloud**, e **fixe a v3** (estável, com suporte oficial a Next.js 16). O roadmap agora atende também ao Figma Sites; alinhamento futuro é incerto. Mitigação: é MIT e self-hosted — no pior caso, congela-se a versão. |
| **Cloudflare comprou a Astro (jan/2026).** Astro 6 lançou em 10/03/2026 (Environment API do Vite, Fonts API, CSP API, Live Content Collections). Segue MIT. | Astro está saudável. A recomendação de não usá-lo aqui é sobre **arquitetura de dois apps**, não sobre a qualidade do Astro. |
| **GSAP é 100% gratuito desde abril/2025**, incluindo os antigos plugins de clube — SplitText, ScrollTrigger, ScrollSmoother, MorphSVG — inclusive para uso comercial (Webflow adquiriu a GreenSock em out/2024). | A objeção histórica de licenciamento sumiu. §26 e §27 (letterings com SplitText) ficam viáveis sem custo. Em compensação, GSAP agora pertence a uma empresa — vale manter o uso **cirúrgico**, não estrutural. |
| **Animações CSS dirigidas por scroll (`animation-timeline: scroll()` / `view()`) atingiram baseline entre navegadores em 2026** (Chrome/Edge 115+, Firefox 132+, Safari 18+; cobertura global estimada em ~84% em meados de 2026), assim como a View Transitions API. Rodam no compositor, com 0 KB de JS. | Boa parte do que se usava ScrollTrigger para fazer agora é CSS. Isso muda a resposta da Q9 (ver §5 desta análise). |
| **Three.js: WebGPURenderer pronto para produção com fallback automático para WebGL2**, e o TSL compila o mesmo shader para WGSL e GLSL. R3F v9 aceita `gl` assíncrono. | §30 ("WebGPU quando disponível ↓ WebGL2 fallback") deixou de ser estratégia a implementar e virou comportamento padrão de um `import`. Um parágrafo inteiro do plano virou linha de código. |

---

## 5. Respostas diretas às 20 perguntas de §64

| # | Pergunta | Resposta curta |
|---|---|---|
| 1 | Arquitetura mais simples em 2026? | **Sim: um app Next.js.** Ver §3.1. |
| 2 | Payload + PostgreSQL é a melhor escolha? | Para a fase com equipe editando, sim (self-host, v3). **Para o MVP, não use CMS nenhum** — ver abaixo. |
| 3 | Astro + Islands é o melhor renderer? | Não *neste* projeto. Next.js, mesmo app. Astro é ótimo, no lugar errado. |
| 4 | Melhor forma de gerar versões estáticas? | Snapshot no publish (§3.2). Não faça um build por proposta. |
| 5 | Como estruturar o Proposal Schema? | Três camadas: `content` / `art` / `composition`. Ver §7. |
| 6 | Prompts sem quebrar o design? | Comandos tipados com enums fechados + validação Zod + budget de performance. Ver §8. |
| 7 | Structured JSON ou actions/tools? | **Tools/actions**, com folga. Ver §8. |
| 8 | Design system com variedade sem parecer template? | Variedade mora nos tokens e na mídia, não na contagem de layouts. Ver §6. |
| 9 | GSAP + Motion + CSS é redundante? | **Sim, parcialmente.** Corte o Motion do v1. CSS primeiro (inclusive scroll-driven), GSAP só para sequências cinematográficas. |
| 10 | Three.js + R3F é a melhor escolha? | É — mas a pergunta certa é se 3D entra no v1. **Não entra.** Ver §6.3. |
| 11 | Spline no workflow? | Sim, como look-dev. Nunca no runtime (o runtime dele é pesado e vira o gargalo). |
| 12 | Rive na stack principal? | Nem principal nem opcional no v1. **Corte.** Ícone e loader se resolvem com SVG/CSS. |
| 13 | Otimizar vídeo, 3D e motion no mobile? | Respostas concretas em §9. |
| 14 | Menor MVP possível? | Menor que a Fase 1 do plano. Ver §10. |
| 15 | Ordem ideal de implementação? | Ver §10 — com uma inversão importante: **editar valores comerciais vem antes de qualquer UI de design.** |
| 16 | O que parece overengineering? | Lista em §7. |
| 17 | O que remover? | Lista em §7. |
| 18 | O que gera dívida técnica? | Astro+Next (nº 1), GSAP como camada padrão, blocos do CMS acoplados ao artefato publicado, tema como string. Ver §7.3. |
| 19 | Risco de lock-in? | Baixo-a-médio, e o item mais caro não é software: **é banda de vídeo.** Ver §7.4. |
| 20 | O que eu escolheria hoje? | §11. |

### Sobre a pergunta 2, em detalhe: o MVP não deve ter CMS

Payload é uma boa escolha *para o momento em que existe uma equipe editando*. Mas nas Fases 1–3 do próprio roadmap existe **uma pessoa** fazendo propostas, e o schema ainda está se mexendo toda semana.

O valor de um CMS é edição multiusuário e edição por quem não programa. Nenhum dos dois é verdade na Fase 1. E um CMS **congela o schema exatamente quando o schema precisa mudar**: cada mudança de bloco vira migração de banco.

Recomendação: nas Fases 1–3, o conteúdo é um arquivo `content/propostas/byd-song-pro.json` validado por Zod, no repositório. O Payload entra na Fase 6, quando a equipe comercial realmente editar. Isso preserva o §61.1 do próprio plano — que a tabela de stack de §42 viola ao já nomear o CMS na v1.

Comparativo, para registro:

| Opção | Quando faz sentido aqui |
|---|---|
| **JSON no repo + Zod** | Fases 1–3. Zero infra, schema livre, diff no git, rollback grátis. **É o que eu usaria para começar.** |
| **Payload (self-host, v3)** | Fase 6+. Admin, versões, drafts, uploads, Live Preview e permissões prontos, dentro do mesmo app Next. Melhor custo-benefício do grupo. |
| **Sanity** | Alternativa real e forte — melhor experiência de edição do mercado e preview maduro. Perde por ser SaaS com preço por assento/documento e por levar o schema para fora do repo. |
| **Directus / Strapi** | Directus é orientado a banco (fraco para composição de blocos); Strapi tem DX inferior para este caso. Nenhum dos dois ganha do Payload aqui. |
| **Convex / Firebase** | Não são CMS. Escolhê-los = construir o admin inteiro. Fora. |
| **Supabase** | O plano o descarta corretamente como núcleo (§43). Mas note: **Supabase + um formulário próprio é viável**, porque uma proposta tem pouquíssimos campos comerciais. Vale como plano B se o Payload incomodar. |

---

## 6. O problema que o plano não resolve: variedade vs sistema

Este é o ponto mais importante do parecer e o que menos aparece nas 20 perguntas.

### 6.1 Onde mora a personalidade

O plano lista **~40 componentes** em 7 famílias (§8.1–8.7). Isso é uma lista de desejos, não um v1 — e, pior, é a resposta errada para a pergunta certa. Mais layouts não produzem mais personalidade; produzem mais superfície para manter e mais chance de a proposta parecer uma colcha.

Numa peça premium, a sensação de "feito para este cliente" vem, nesta ordem:

1. **tipografia** (par tipográfico, escala, peso, tracking, tratamento de caixa);
2. **cor e luz** (paleta, contraste, temperatura, como o preto é preto);
3. **tratamento de imagem** (grade, grão, duotone, corte, proporção);
4. **ritmo e timing** (altura das seções, duração e curva das entradas, quanto tempo o olho fica parado);
5. **um momento assinatura** — uma coisa memorável, uma só;
6. e só então, layout.

Ou seja: **a personalidade mora nos tokens, e o "cheiro de template" vem do ritmo repetido, não do layout repetido.** Duas propostas com o mesmo grid e curvas de motion diferentes parecem projetos diferentes; duas propostas com layouts diferentes e o mesmo timing parecem o mesmo produto.

Isso reorienta a Fase 4: a camada de tokens precisa ser **grossa** (incluindo espaçamento, ritmo, curvas e durações), e a lista de blocos precisa ser **fina**.

### 6.2 O tamanho certo da biblioteca

Para o v1: **~8 tipos de bloco × 2–3 variantes estruturais.** Algo como:

```
hero (3)  ·  manifesto (2)  ·  escopo (3)  ·  galeria (3)
timeline (2)  ·  investimento (2)  ·  prova/case (2)  ·  cta (2)
```

19 variantes cobrem praticamente tudo que uma proposta comercial precisa dizer. O resto do plano (§8) é backlog de 2027.

E uma regra de direção: **um momento assinatura por proposta.** Um. Um lettering que se desmonta, uma cena que faz scrub, um reveal de produto. Não cinco. Uma proposta não é um showreel de recursos — e o próprio plano sabe disso quando escreve §66.

### 6.3 Por que o 3D sai do v1

O plano já hesita corretamente (§66: "se uma proposta puder ser excelente sem 3D, não usar 3D"). Eu iria mais longe: **corte 3D realtime inteiro do MVP.**

Argumento honesto: uma sequência **pré-renderizada** do mesmo GLB — feita em Blender/C4D, em 4K, com o tempo de render que se quiser — **fica mais bonita** que WebGL em tempo real, carrega mais rápido, funciona em qualquer aparelho, dispensa fallback e dispensa budget de GPU. E a YAD é uma produtora: já tem o pipeline, a equipe e o olho para renderizar frames bonitos. Essa é uma vantagem competitiva que a maioria dos estúdios de web não tem — e o plano a ignora ao escolher realtime.

3D em tempo real só se paga quando o cliente **interage**: configurador, exploded view que ele controla, girar o produto. Fora disso é gimmick caro. Quando esse dia chegar, Three.js + R3F é a escolha certa e o fallback já vem de graça.

---

## 7. O corte: o que sai do v1

### 7.1 Fora agora

| Item | Por quê sai | Quando volta |
|---|---|---|
| Renderer Astro separado | Duplica biblioteca, build e preview | Nunca, na prática |
| 3D realtime (Three.js/R3F) | Sequência pré-renderizada é melhor e mais barata (§6.3) | Quando houver interação real |
| Rive | Ferramenta + runtime inteiros para ícones e loaders | Fase 3+, se doer |
| Spline no runtime | Runtime pesado, lock-in | Só como look-dev, sempre |
| Motion (ex-Framer Motion) | Terceira biblioteca de animação sobrepondo as outras duas | Quando um componente precisar de layout animation/gestos |
| Export offline (§38) | O snapshot do publish já resolve 90% (§3.2) | Se um cliente pedir |
| Analytics (§39) | Fase futura pelo próprio plano | Fase 9, e usando o player de vídeo |
| Aprovação/assinatura (§40) | **Não construa** — integre (§12.6) | Fase 9, via Clicksign/D4Sign/ZapSign |
| Proposal Director (§17, §57) | Últimos 5% de valor, primeiros 50% de complexidade | Depois do schema estável, se ainda fizer sentido |
| Client DNA como sistema (§6, §54) | Antes do 3º cliente recorrente é abstração especulativa | Quando houver o 3º |
| Classificação A/B/C + bloqueio (§32) | Um teste de Lighthouse no CI faz isso | Se as propostas começarem a pesar |
| Estratégia de fallback WebGPU (§30) | Virou comportamento padrão do Three.js | Já resolvido |
| CMS na v1 (§19) | Congela o schema na hora errada | Fase 6 |

Isso é um corte grande. Nada nessa lista é irreversível, e nada nela está no caminho crítico entre hoje e *"a proposta da YAD parece extraordinária e o valor muda em 5 segundos"*.

### 7.2 O que fica, e é pouco

Next.js 16 · TypeScript · React · CSS moderno (custom properties, container queries, scroll-driven animations, View Transitions) · GSAP (só ScrollTrigger/SplitText, e só onde CSS não chega) · vídeo em CDN de vídeo · Cloudflare R2 para assets · Zod · JSON no repo.

### 7.3 Dívida técnica provável

1. **Astro + Next (nº 1 com folga).** Duas bibliotecas de componentes é a dívida que não se paga: ela cresce a cada bloco novo.
2. **GSAP como camada padrão em vez de exceção.** Timelines presas a scroll são a coisa mais difícil de refatorar depois, porque vazam suposições de DOM para dentro dos componentes. Use como bisturi.
3. **Blocos do CMS como fonte do artefato publicado.** Se a proposta enviada é renderizada a partir do registro do CMS, toda mudança de schema é uma migração retroativa. O snapshot (§3.2) corta isso.
4. **`"theme": "byd-dark"` como string (§15).** Tema por string sempre vira um `switch` gigante. Guarde **tokens resolvidos**, não o nome do tema.
5. **Mídia como upload do CMS.** Vídeo e GLB dentro do CMS acabam mal (o próprio plano avisa em §21 quanto ao banco — a mesma lógica vale para o CMS). Caminho de CDN desde o dia 1.

### 7.4 Lock-in — o item caro não é software

- **Payload:** MIT, self-hostável. Risco = roadmap agora orientado ao Figma. Mitigação = fixar versão. Aceitável.
- **GSAP:** grátis, mas da Webflow. Uso cirúrgico limita a exposição.
- **Astro:** agora da Cloudflare, segue MIT. Irrelevante se não for usado.
- **Vercel — este é o que importa.** Uma proposta premium é *pesada de banda*: um hero de 200 MB visto 200 vezes são 40 GB. No plano Pro da Vercel a banda é cobrada acima do incluso (na casa de US$ 0,15/GB), enquanto a Cloudflare não cobra egresso de assets estáticos. **Coloque mídia em Cloudflare R2 / Stream desde o dia 1, mesmo rodando o app na Vercel.** É uma linha de configuração hoje e uma migração depois. Esta é a decisão de custo com maior alavancagem do plano inteiro.

---

## 8. Proposal Schema e camada de IA

### 8.1 Três camadas, não um objeto plano

O exemplo de §15 tem um defeito estrutural: `hero` é um objeto de primeira classe e todo o resto é um array de strings. Isso faz do hero um caso especial permanente e impede que qualquer bloco não-hero receba opções.

Estrutura recomendada:

```json
{
  "meta":  { "id": "byd-song-pro-2026", "version": 3, "status": "draft" },

  "content": {
    "client": "BYD", "project": "Lançamento Song Pro",
    "manifesto": "…", "escopo": [ … ], "entregaveis": [ … ],
    "cronograma": [ … ],
    "investimento": { "value": 370000, "currency": "BRL" },
    "validade_dias": 30, "condicoes": "…"
  },

  "art": {
    "dna": "byd",
    "type":    { "display": "…", "body": "…", "scale": 1.333, "case": "upper" },
    "color":   { "bg": "#07080A", "fg": "#F2F2F0", "accent": "#E3002B" },
    "image":   { "grade": "cool-contrast", "grain": 0.12 },
    "motion":  { "curve": "expo-out", "duration": 1.2, "intensity": 2 },
    "rhythm":  { "sectionHeight": "tall", "density": "airy" }
  },

  "composition": [
    { "id": "b1", "type": "hero",        "variant": "cinematic-video",
      "media": ["hero-song-pro.mp4"], "options": { "overlay": 0.4 } },
    { "id": "b2", "type": "manifesto",   "variant": "big-type" },
    { "id": "b3", "type": "escopo",      "variant": "horizontal-story" },
    { "id": "b7", "type": "investimento","variant": "premium-statement" },
    { "id": "b8", "type": "cta",         "variant": "signature" }
  ]
}
```

Três regras que fazem esse schema durar:

- **Tudo é bloco.** Hero não é campo, é `composition[0]`. Sem casos especiais.
- **Todo bloco tem `id` estável.** É o que permite comandos ("mova b3 para antes de b2") e diffs legíveis.
- **`art` guarda valores resolvidos, não nomes.** `"dna": "byd"` é conveniência de UI; os tokens efetivos vão junto, para o snapshot ser autossuficiente.

### 8.2 Tools, não JSON — e por quê

A pergunta 7 (§64) é a mais afiada do documento, e a resposta é **actions/tools**, não "modelo devolve o JSON".

Se o modelo devolve o objeto inteiro, mesmo com JSON Schema estrito, você ganha: nada que valide *semântica* (uma variante que não existe, um bloco duplicado, uma combinação que estoura o orçamento de performance), nenhum diff legível, nenhum undo barato, e o risco permanente de o modelo reescrever campos que ninguém pediu para mexer.

Com um conjunto fechado de comandos tipados:

- **variantes viram `enum`** — é *impossível* o modelo inventar um hero que não existe;
- **cada mudança é um diff** — mostrável na tela, desfazível, logável, auditável;
- **a interface manual sai de graça** — os botões chamam as mesmas funções, e §13 ("prompt não deve ser obrigatório") deixa de ser trabalho extra;
- **as regras de composição ficam em código**, onde se testam — inclusive o alerta de §32 ("Hero3D-Ultra + Gallery3D + 4 vídeos 4K = bloqueado").

Na API da Anthropic isso é `tools` com `strict: true` (parâmetros validados contra o schema, sem "quase certo"). O `output_config.format` (structured outputs) continua útil, mas para outra coisa: **extrair briefing** — transformar transcrição de reunião em `content` estruturado. São dois usos diferentes e ambos cabem.

Fluxo:

```
linguagem natural → LLM (tools, strict) → comandos tipados
                                          ↓
                          validação Zod + regras de composição
                                          ↓
                             novo estado → diff → preview
```

### 8.3 Modelo e custo

Para este trabalho, custo é irrelevante — vale registrar para tirar a variável da mesa:

| Modelo | ID | Preço (US$/milhão de tokens, entrada/saída) | Uso aqui |
|---|---|---|---|
| Claude Opus 5 | `claude-opus-5` | 5 / 25 | Composição inicial e escrita de copy (Proposal Director, quando chegar) |
| Claude Sonnet 5 | `claude-sonnet-5` | 3 / 15 (promocional 2 / 10 até 31/08/2026) | **Padrão para a camada de comando** |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 1 / 5 | Edições de campo ("investimento vira 370 mil") |

Uma proposta inteira, com dezenas de idas e vindas, custa **centavos**. A decisão de modelo aqui é sobre qualidade de julgamento, não sobre custo.

---

## 9. Mobile, vídeo, 3D e motion — respostas concretas (Q13)

**Vídeo** (o item que mais pesa numa proposta premium):

- AV1 com fallback H.264; HLS para qualquer coisa acima de ~15 s. `poster` sempre. `preload="none"` fora da primeira dobra.
- **Encode mobile separado** — 720p, e recortado para o enquadramento vertical se for hero. Não sirva o arquivo de desktop reduzido: o enquadramento cinematográfico horizontal morre no celular.
- Hospedagem: **não sirva MP4 solto de um bucket** para hero. Perde bitrate adaptativo e o cliente no 4G vê buffer. Ordem de grandeza em 2026: Bunny é o mais barato; **Cloudflare Stream tem a melhor relação custo/simplicidade** (encode e storage embutidos, sem taxa de encode); Mux custa mais e se paga se você quiser **analytics por espectador** — o que, aliás, é a parte mais interessante do §39 ("o cliente assistiu ao filme inteiro?").

**3D**, se e quando entrar:

- `gltf-transform` no CLI. **Meshopt** para geometria (decode rápido) — Draco comprime mais, mas o decode trava visivelmente num celular mediano.
- **KTX2/Basis para texturas** — geralmente é a parte mais pesada do modelo, e KTX2 economiza download *e* memória de GPU. ETC1S para tamanho, UASTC para qualidade.
- Cap de textura em 1K–2K. GLB servido com Brotli. Lazy-load abaixo da dobra.

**Motion:**

- `prefers-reduced-motion` **no nível do token** — um caminho `motion.intensity = 0`, não um monte de `if` espalhado.
- Mobile recebe **um preset reduzido próprio**, não o preset de desktop escalado. Scroll-jacking em celular é onde propostas premium viram propostas irritantes.

**Fontes:**

- Variable fonts, subset, self-host WOFF2, `font-display: swap` com fallback de métrica ajustada (`size-adjust`) para não ter salto de layout.

---

## 10. Roteiro revisado

Semanas, não fases — e com uma inversão importante em relação ao plano.

| # | Entrega | Semanas | Observação |
|---|---|---|---|
| 1 | **Proposta real nº 1**, escrita à mão, no stack final. Conteúdo já em JSON, tokens já em CSS custom properties. Sem admin, sem IA, sem biblioteca. | 2–3 | A restrição artificial é o ponto: **proibido escrever CSS fora do sistema de tokens.** 10% menos perfeita, 300% mais reaproveitável. |
| 2 | **Proposta real nº 2**, cliente com identidade oposta. Regra: só pode mexer no JSON e nos tokens. | 1–2 | **Este é o experimento.** O que você for obrigado a codar é a lista honesta do que ainda não é sistema. |
| 3 | Extrair componentes — **só o que repetiu nas duas** | 1 | Depois da nº 2, não depois da nº 1. Um ponto não define uma reta. |
| 4 | Publicação: URL, slug não-adivinhável, senha, `noindex`, expiração, **snapshot congelado** | 1 | Ver §3.2 e §12.5. |
| 5 | **Formulário de campos comerciais** (investimento, prazo, validade, condições, textos) | 1 | **Aqui mora 80% do valor operacional.** O critério de §62 ("valores alterados em segundos") se cumpre na semana 6, não no mês 6. |
| 6 | UI de blocos: reordenar, trocar variante, adicionar, remover | 2 | Já sobre a API de comandos (§3.3). |
| 7 | Payload, **se e quando** houver mais de dois editores | 2–3 | Migra o JSON para o CMS; o snapshot continua sendo a saída. |
| 8 | Camada de IA sobre a API de comandos já estável | 1–2 | Barata porque os comandos já existem. |
| 9 | Analytics + aceite (integrado, não construído) | 1–2 | |
| 10 | Export offline, se alguém pedir | — | Provavelmente ninguém pede. |

**Timebox:** se as propostas 1 e 2 não estiverem prontas em ~6 semanas de trabalho parcial, o escopo está errado — não o time.

---

## 11. O que eu escolheria hoje (Q20)

```
Um app Next.js 16 (App Router, RSC) · TypeScript
Deploy: Vercel ou Cloudflare Workers
Conteúdo: JSON tipado + Zod no repositório (Payload v3 self-host na fase 6+)
Mídia: Cloudflare R2 (assets) + Cloudflare Stream (vídeo) — desde o dia 1
Estilo: CSS moderno — custom properties, container queries,
        scroll-driven animations, View Transitions
Motion cinematográfico: GSAP (ScrollTrigger + SplitText), cirúrgico
3D: nenhum. Sequências pré-renderizadas pela própria equipe.
Design system: ~8 blocos × 2–3 variantes + camada grossa de tokens
IA: tools com strict schema sobre commands.ts · Sonnet 5 (Haiku 4.5 nos campos)
Publicação: snapshot congelado + slug opaco + senha + noindex + validade
```

Uma frase: **o produto é um repositório de tokens e oito blocos, com um formulário na frente e um congelador na saída.** Todo o resto é fase 2.

---

## 12. O que o plano não pergunta — e deveria

Sete pontos ausentes das 20 perguntas que pesam mais do que várias delas.

### 12.1 Quem, exatamente, opera isso?

O plano diz "a equipe comercial edita sem programar" (§62). Numa produtora, a equipe comercial costuma ser **uma ou duas pessoas** — às vezes o próprio sócio. Se for esse o caso, metade da plataforma não tem usuário. E se a resposta honesta for "quem escreve as propostas sou eu", então o produto certo é **um repositório muito bom + um formulário**, e o trabalho mais valioso da IA não é mover blocos: é escrever.

Essa resposta muda o roadmap inteiro. Vale respondê-la antes da linha 1 de código.

### 12.2 O gargalo é o texto, não o layout

Uma proposta premium se ganha ou se perde no manifesto, no enquadramento do escopo e na forma de apresentar o investimento. O plano trata conteúdo como campo a preencher (§7) e gasta as energias de IA em direção de arte ("deixe mais elegante", "troque o hero").

Onde as horas realmente vão: **transformar uma reunião de 50 minutos em três parágrafos que fazem a diretoria querer aprovar.** É aí que uma camada de IA paga o próprio custo em uma semana — e a YAD já tem esse ativo escrito, na forma da skill `diretor-comercial-yad`. Ligar a plataforma a ela vale mais que o Proposal Director inteiro.

### 12.3 A métrica ausente

§62 mede carregamento, mobile, fallback, bugs. Não mede a única coisa que justifica o projeto:

> **Hoje uma proposta leva X horas para ficar pronta. A meta é Y.**

E a métrica de segunda ordem, que é o business case de verdade: **taxa de fechamento e ticket médio, antes e depois.** Se a plataforma não move esses números, ela é uma peça de portfólio — o que é legítimo, mas é uma decisão diferente e deve ser tomada conscientemente.

### 12.4 Fontes licenciadas são exposição jurídica real

Usar a tipografia corporativa da BYD, da Nestlé ou da Yamaha como webfont em `propostas.yadfilmes.com` exige **licença de webfont que cubra o domínio da YAD**. A licença do cliente normalmente **não** se estende ao domínio da agência, e a licença desktop de agência cobre o trabalho de design, não a distribuição web em produção. Licenças de webfont são escopadas por domínio (e às vezes por faixa de tráfego).

Mitigação prática, sem virar caso jurídico:

- tipografia do cliente **rasterizada** — em KV, letterings e frames renderizados (isso é uso de arte, não de fonte);
- texto vivo em um par tipográfico que a YAD licencia uma vez e usa em todas as propostas — e que passa a ser parte da identidade "YAD faz propostas assim";
- quando o cliente exigir a fonte dele em texto vivo, pedir a ele a licença de webfont ou uma autorização escrita.

Isso vira uma linha do Client DNA: `fontLicense: "raster-only" | "webfont-ok"`.

### 12.5 Segurança do link é requisito, não vantagem

§36 lista "senha" e "controle de acesso" como **vantagens** do formato online. São requisitos. Um orçamento vazado é dano comercial direto — para a YAD e para o cliente.

Mínimo do v1: slug não-adivinhável (não `/byd/song-pro`), senha opcional, `noindex` + `X-Robots-Tag`, data de expiração, e nenhum valor comercial em `<meta>` de preview (o preview do WhatsApp vaza mais coisa do que as pessoas imaginam). Some a isso o combinado com o cliente sobre uso de marca e KV — proposta com logo do cliente não vai para portfólio sem autorização.

### 12.6 Construir vs assinar — separe as duas partes

Existem produtos que fazem "proposta como microsite" com analytics, template e assinatura eletrônica: Qwilr, Storydoc, Proposify, PandaDoc, Better Proposals — na faixa de dezenas de dólares por usuário/mês.

Nenhum deles jamais vai parecer um filme da YAD. É exatamente por isso que se constrói. **Mas eles resolvem de graça a parte que não é diferencial:** link, analytics, aceite, assinatura.

Recomendação híbrida: **construa a experiência; não construa a camada de aceite/assinatura.** No Brasil, assinatura eletrônica com validade (Lei 14.063 / ICP-Brasil) é Clicksign, D4Sign ou ZapSign — integração de dias, não de meses. §40 deveria dizer "integrar", não "criar".

### 12.7 Uma proposta é um documento com prazo de validade

O plano trata a proposta como uma peça publicada. Ela é também um instrumento comercial que **expira** (§7 já prevê "Validade"). Isso tem consequências de produto que ninguém pensa até doer: o que o cliente vê quando abre um link vencido? E quando o valor mudou depois que ele já viu a V1? O snapshot por versão (§3.2) resolve a parte técnica; a parte de produto precisa de uma decisão explícita.

---

## 13. Riscos que podem matar o projeto

| Risco | Sinal de alerta | Mitigação |
|---|---|---|
| **A proposta nº 1 fica linda e nada nela sobrevive ao cliente nº 2** | Você escreveu CSS fora do sistema de tokens "só desta vez" | Decidir tokens e lista de blocos **antes** de desenhar. Proibição explícita de CSS fora do sistema. É o único jeito. |
| **Vira projeto paralelo que compete com trabalho faturado** | Semana 8 e a proposta nº 2 não existe | Timebox de 6 semanas para as duas primeiras. Se estourar, o escopo está errado. |
| **Plataforma pronta, ninguém usa** | O sócio continua fazendo proposta no Figma "porque é mais rápido" | Etapa 5 (formulário de campos comerciais) antes de qualquer UI de design. Ganhar o hábito antes de ganhar o recurso. |
| **Banda de vídeo vira custo surpresa** | Primeira fatura de deploy | R2/Stream desde o dia 1 (§7.4) |
| **Design system engessa a direção de arte** | Diretor de arte reclama que "tudo fica igual" | Tokens grossos + um momento assinatura por proposta (§6). Se ainda assim engessar, o problema é escopo do bloco, não do sistema — e a resposta é uma variante nova, não uma exceção. |
| **Payload muda de rumo sob o Figma** | v4 muda a API do admin | Fixar v3, self-host, snapshot como saída. O CMS é substituível por construção. |

---

## 14. Critérios de sucesso revisados

O §62 é bom, mas mede a coisa errada primeiro. Ordem proposta:

**Operacional (o que justifica o projeto)**
- Tempo de produção de uma proposta caiu de X para Y horas
- Alterar valor, prazo ou validade: menos de 60 segundos, sem desenvolvedor
- Histórico completo por versão, com autor e data
- Nenhuma proposta enviada quebrou depois de enviada *(garantido por construção, via snapshot)*

**Comercial (o que prova o projeto)**
- Taxa de fechamento e ticket médio, antes e depois
- Tempo entre envio e resposta do cliente

**Visual**
- Duas propostas de clientes diferentes não parecem o mesmo produto
- Cada proposta tem exatamente um momento memorável
- O time interno acha a proposta boa o bastante para mostrar como trabalho

**Técnico**
- LCP < 2,5 s no 4G em celular mediano, com hero em vídeo
- `prefers-reduced-motion` respeitado no nível de token
- Zero valor comercial exposto em URL pública ou preview de link

---

## 15. Resumo executivo

1. **Mantenha** a filosofia: IA comanda um sistema validado, conteúdo separado do design, proposta real antes de plataforma. Está certo.
2. **Faça um app só** — Next.js. Astro fora. Isso resolve as perguntas 3, 4 e 7 de §63 de uma vez.
3. **Publicar = congelar.** Snapshot imutável por versão. Isso resolve a pergunta 19 e entrega §37/§38 quase de graça.
4. **Toda mutação é um comando tipado.** Interface e IA chamam as mesmas funções. Tools com `strict`, não JSON solto.
5. **Personalidade mora nos tokens.** ~8 blocos × 2–3 variantes, camada de tokens grossa, um momento assinatura por proposta.
6. **Corte 3D, Rive, Spline, Motion, export offline, Proposal Director e o CMS do v1.** Tudo volta depois; nada disso está no caminho crítico.
7. **Mídia em Cloudflare desde o dia 1.** É a decisão de custo com maior alavancagem do plano.
8. **Formulário de campos comerciais na semana 6**, não no mês 6. É onde mora o valor operacional.
9. **Responda antes de codar:** quem opera isso, e quanto tempo custa hoje fazer uma proposta.
10. **Resolva a licença de fonte e a segurança do link** antes da primeira proposta ir para um cliente.

O plano descreve uma plataforma. O que a YAD precisa primeiro é de **duas propostas extraordinárias e um formulário**. A plataforma é o que sobra quando essas duas propostas revelarem o que de fato se repete.

---

## Fontes consultadas

Verificações feitas em 10/08/2026.

- [Welcoming Payload to the Figma Team — Figma](https://www.figma.com/blog/payload-joins-figma/)
- [Payload CMS 2026: Why Figma Bought It — Techsy](https://techsy.io/en/blog/payload-cms-guide)
- [Payload CMS 4.0: Latest Status — Build with Matija](https://www.buildwithmatija.com/blog/payload-4-0)
- [Payload CMS + Next.js 16 compatibility — Build with Matija](https://www.buildwithmatija.com/blog/payload-cms-nextjs-16-compatibility-breakthrough)
- [Live Preview — Payload Docs](https://payloadcms.com/docs/live-preview/overview)
- [Cloudflare Acquires Astro — Cloudflare press release](https://www.cloudflare.com/press/press-releases/2026/cloudflare-acquires-astro-to-accelerate-the-future-of-high-performance-web-development/)
- [Astro 6.0 — Astro](https://astro.build/blog/astro-6/)
- [Webflow makes GSAP 100% free — Webflow](https://webflow.com/blog/gsap-becomes-free)
- [Standard License — GSAP](https://gsap.com/community/standard-license/)
- [Motion (prev Framer Motion)](https://motion.dev/)
- [A guide to Scroll-driven Animations with just CSS — WebKit](https://webkit.org/blog/17101/a-guide-to-scroll-driven-animations-with-just-css/)
- [View Transitions API and CSS Scroll-Driven Animations — Frontend Horizon](https://www.frontendhorizon.com/blog/view-transitions-api-and-css-scroll-driven-animations-the-browser-wins-of-2026)
- [What's New in Three.js (2026): WebGPU, New Workflows — Utsubo](https://www.utsubo.com/blog/threejs-2026-what-changed)
- [WebGPURenderer — three.js docs](https://threejs.org/docs/pages/WebGPURenderer.html)
- [v9 Migration Guide — React Three Fiber](https://r3f.docs.pmnd.rs/tutorials/v9-migration-guide)
- [glTF Transform](https://gltf-transform.dev/) · [gltfpack / meshoptimizer](https://meshoptimizer.org/gltf/)
- [Mux vs Cloudflare Stream vs Bunny Stream 2026 — PkgPulse](https://www.pkgpulse.com/guides/mux-vs-cloudflare-stream-vs-bunny-stream-video-cdn-2026)
- [Cloudflare Workers vs Vercel (2026) — Morph](https://www.morphllm.com/comparisons/cloudflare-workers-vs-vercel)
- [Font licensing explained for designers and brands — Monotype](https://www.monotype.com/font-licensing-explained-designers-and-brands)
- [Font Licensing Explained: 2026 Guide — Inkbot Design](https://inkbotdesign.com/font-licensing/)
- [Best proposal software 2026 — Cobl](https://www.cobl.ai/blog/best-proposal-software)
- Preços e IDs de modelo Claude: skill `claude-api` (cache de 24/06/2026)
