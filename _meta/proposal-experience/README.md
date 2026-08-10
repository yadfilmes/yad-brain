# YAD Proposal System — protótipo

Gerador de propostas comerciais: **um conteúdo, três saídas.**

```
content.json  +  dna/<cliente>.css  +  assets/
                       ↓  python3 build.py --pdf
   dist/proposta.html        arquivo único · offline · encaminhável
   dist/index.html + assets/ versão de link
   dist/proposta.pdf         impressão determinística, para compras
   dist/proposta-bundle.zip  html + pdf, para anexar
```

> **Escopo.** Este diretório é protótipo de **outro projeto** que não o YAD BRAIN —
> está aqui sob `_meta/` por versionamento, não integra o acervo e não é lido pelo
> `tools/validate.py`. O `.gitignore` local mantém `assets/`, `dist/` e `content.json`
> **fora do repositório**: proposta real tem valor, cliente e imagem de marca, e a
> regra de isolamento do README da raiz vale aqui.
> O que se versiona é o **sistema**; o conteúdo mora no computador de quem escreve.

---

## Por que existe

Medido nas duas propostas aprovadas que originaram este protótipo:

| Problema encontrado | Efeito | Correção |
|---|---|---|
| `font-family: Inter…` sem nenhum `@font-face` | A fonte não viajava. Em Windows sem Inter o cliente via **Segoe UI** — e o `letter-spacing: -.055em` do display, calibrado para a Inter, desmontava. | Inter Variable subsetada e embutida em base64 (47 KB → **23 KB**, 99 caracteres). Obrigatório em `file://`, que não busca fonte de CDN. |
| Hero em **PNG** a 1,44 byte/px (os JPEGs do mesmo arquivo: 0,10–0,22) | 2,27 MB numa imagem só — metade do peso do documento — e ainda macia em tela retina, porque tinha só 1672 px de largura. | AVIF. As 9 imagens: **3,60 MB → 0,64 MB (17,8%)**. O hero sozinho: 2,27 → 0,16 MB. |
| Zero `@keyframes`, zero JS | Documento parado. | Camada de motion + perspectiva 3D em **CSS puro**, 0 KB de JavaScript. |
| `@media print` sem regra para `.dark` | O navegador descarta fundo na impressão por padrão: as seções escuras ficavam **texto branco em papel branco** e o valor da proposta sumia. | Inversão escuro→claro na impressão + `print-color-adjust: exact` onde o fundo é essencial + PDF gerado por Chrome headless, sem depender do diálogo do cliente. |

Resultado no piloto: **4,85 MB → 0,94 MB** no arquivo único, com tipografia correta,
motion e o PDF em 1,69 MB.

---

## Rodar

```bash
cp content.example.json content.json     # e edite
python3 build.py                         # html único + versão de link
python3 build.py --pdf                   # + PDF + zip (precisa de Chrome/Chromium)
```

Sem dependência obrigatória — só stdlib. Opcionais, e o que cada uma acrescenta:

| Pacote | Sem ele |
|---|---|
| `fonttools` + `brotli` | a fonte inteira é embutida (~25 KB a mais) |
| `pikepdf` + `pillow` | o PDF fica ~6× maior (o Chromium reembute foto sem perdas) |
| Chrome / Chromium | não gera PDF |

Converter imagem para AVIF (fora do build, uma vez por asset):

```bash
ffmpeg -i foto.png  -c:v libaom-av1 -crf 30 -still-picture 1 foto.avif
# ou:  avifenc --min 20 --max 34 foto.png foto.avif
# ou, em Python:  Image.open('foto.png').convert('RGB').save('foto.avif', quality=72)
```

Exporte o hero com **2560 px de largura** — em AVIF ele continua abaixo de 400 KB
e para de aparecer macio em tela retina.

---

## Estrutura

| Arquivo | Papel |
|---|---|
| `content.json` | **Só conteúdo.** Textos, valores, ordem dos blocos. É o que muda entre versões de uma mesma proposta. |
| `dna/<cliente>.css` | **Só identidade.** ~20 custom properties: cor, tipo, ritmo, curva e intensidade de motion. Trocar este arquivo troca a personalidade inteira sem tocar em layout. |
| `src/system.css` | O sistema. Não conhece cliente nenhum. |
| `build.py` | Renderiza, embute, imprime, empacota. |

Alterar o investimento é **um número no `content.json`** + `python3 build.py`.
Nunca se edita o HTML.

### Blocos disponíveis

`hero` · `statement` · `quote` · `cards` · `deliverables` · `workflow` · `timeline`
`roles` · `steps` · `urgency` · `investment` · `conditions` · `about` · `gallery` · `cta`

Quinze tipos, com variantes por `tone` (`white` / `dark` / `accent`), `cols` e
`variant`. O `content.example.json` exercita todos.

---

## Motion e 3D

Tudo em CSS. Nenhum JavaScript chega ao cliente — é o que permite rodar em
`file://`, dentro de e-mail corporativo e no PDF.

| Recurso | Como |
|---|---|
| Lettering do hero | O `<h1>` é dividido em caracteres **no build** (`split_letters`), cada um com `--i`. Cascata 3D por tempo, no carregamento. É a única animação temporal do sistema — o hero abre antes de existir scroll. |
| Entradas de seção | `animation-timeline: view()` com `rotateX` + `translateZ` dentro de uma `perspective`. |
| Stagger | No scroll o atraso **não é tempo**: é deslocamento de `animation-range` por `--i`. |
| Parallax do hero | `animation-timeline: scroll()` com faixa em `vh`. Deliberadamente **não** é `view()`: o hero nasce no topo do documento, então com `view()` ele já começaria a 50% do próprio range — e abriria borrado. |
| Momento assinatura | A galeria vira cena presa (`position: sticky` + `view-timeline-name`): o scroll atravessa os quatro cartões em profundidade, um por vez. Só acima de 1000 px — no celular volta a ser grade. |
| Intensidade | `--mo-intensity` no DNA: `0` desliga, `3` é máximo. Todos os deslocamentos, rotações e desfoques derivam dele. |

**Regra de segurança:** o estado final é o estado padrão. Toda animação vive dentro
de `@supports (animation-timeline: view())` **e** `prefers-reduced-motion: no-preference`.
Navegador sem suporte (≈16% em meados de 2026) mostra a página inteira, parada e
completa — nunca conteúdo invisível. Verificado: com movimento reduzido, **0 elementos**
ficam com opacidade abaixo de 0,05.

---

## Verificado no piloto

- 17 blocos renderizados, **0 erros de console**
- Movimento reduzido: 0 elementos escondidos; a cena presa vira grade
- Celular 390 px: **sem overflow horizontal**; a cena 3D não roda
- Impressão: nenhum texto branco sobre branco; o valor aparece
- PDF: 18 páginas, 7 imagens íntegras, 1,69 MB

---

## O que falta

- Vídeo (hero em movimento) — decidir entre embutir no arquivo único ou só no link
- Service worker na versão de link, para a proposta funcionar offline depois de aberta uma vez
- Slug opaco, senha e validade na publicação
- Sequência scrubada por scroll — o "3D" de verdade sem WebGL, para quando houver render de produto
