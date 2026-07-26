# Convenções do acervo

Regras que mantêm milhares de notas coerentes e baratas de consultar.
O `validate.py` faz cumprir tudo que é verificável por máquina.

## Identidade e nomes

- **Slug ASCII, sem acento, kebab-case, único no acervo inteiro.**
  `iluminacao.md`, nunca `iluminação.md` — o grep é byte a byte e
  `iluminação ≠ iluminacao`.
- **`id` == nome do arquivo** (sem `.md`). Imutável depois de criado.
- Acentos, apelidos, códigos de modelo e o termo em inglês vivem em `aliases`.
- Prefixo de tipo quando houver ambiguidade: `mount--pl`, `moc--luz`,
  `_tmpl-equipamento`.
- Um arquivo nunca repete o basename de outro — o link `[[slug]]` precisa
  resolver sem ambiguidade.

## Idioma

Prosa em **português**; termos técnicos em **inglês**, como o set fala
("full-frame", "log", "mount", "keyer"). Não traduzir o que ninguém traduz.

## Caminhos

Todo script usa **caminho relativo à raiz do repositório**, nunca absoluto.
O acervo precisa funcionar igual no SSD, em outra máquina ou num container —
com espaço no caminho ou sem.

## Tamanho e forma da nota

- **Nota atômica**: um conceito ou entidade por arquivo.
- **300–900 tokens** (alvo ~500). Acima de ~1.200: dividir e linkar.
- **TL;DR na primeira linha do corpo**, auto-suficiente — é o que o grep
  devolve, muitas vezes sem precisar abrir o arquivo.
- **Linhas auto-suficientes**: chave e valor na mesma linha. Nunca espalhar
  um dado por um parágrafo.

## Escopo condicional (regra do claim-lite)

**Spec condicional não entra sem suas condições na mesma linha.**

Errado: `frame rate máximo: 120fps`
Certo: `120 fps @ 4K S35 crop, X-OCN LT, firmware ≥ 3.0`

Quando houver vários modos, usar tabela `## Modos de gravação` com uma linha
por combinação. A linha da tabela **é** a afirmação com escopo.

## Números e fontes

- **Número sem fonte não entra.** Lacuna honesta (`<!-- verificar -->`) é
  aceitável; especificação inventada, nunca.
- Toda spec numérica exige fonte tier `oficial` ou `lab`.
- Quando houver medição independente, anotar o regime:
  `16 stops (declarado); ~13,5 (CineD, medido)`.
- Campo `loc` na fonte quando for documento paginado: `p. 143, tab. 8`.

## Tiers de fonte

| tier | o que é | serve para |
|---|---|---|
| `oficial` | fabricante, manual, norma, documentação | fatos e números |
| `lab` | teste independente com metodologia publicada | desempenho medido |
| `educacao` | blog, canal, curso | síntese e contexto |
| `comunidade` | Reddit, fórum, grupo | experiência de campo, gotchas |
| `campo-proprio` | experiência de set própria, generalizada | prática real |

**Marketing, agregador e conteúdo gerado por IA nunca são promovidos a fato** —
servem apenas para descoberta.

## Conteúdo de comunidade

- Sempre **parafrasear**; nunca colar texto bruto de fórum no acervo.
- **Nunca registrar username** (LGPD): "um colorista no thread do LGG".
- Transcrição de vídeo é artefato **efêmero** — não entra no repositório.
- Dica de comunidade só vira recomendação com corroboração em **≥2 fontes
  independentes**.

## Zoneamento (`zona`)

| valor | significado |
|---|---|
| `universal` | conhecimento do mundo — specs, conceitos, normas |
| `yad` | experiência própria de campo — não sai do time |

Dados de cliente, orçamento e contrato **não entram neste repositório**,
em zona nenhuma.

## Preço — camada separada (planejado, ainda não implementado)

Preço **não entra na nota de conhecimento**. Spec de equipamento é estável;
cotação no Brasil move com câmbio, importação, sazonalidade e negociação — e
preço velho é pior que preço nenhum, porque está confiantemente errado.

Quando for implementado, o desenho é este:

```
_precos/                        zona: yad — nunca sai do time
  diarias-AAAA.yaml             alexa-35: {valor, moeda, locadora,
                                           data_cotacao, pacote}
```

| tipo de dado | zona | vai junto se o acervo for vendido? |
|---|---|---|
| `price_tier` qualitativo (budget…high-end) | `universal` | sim — já existe hoje |
| diária de referência de mercado | `yad` | não |
| diária negociada da YAD / preço de venda | `yad` | **nunca** |

Quatro razões para ser camada separada e não campo na nota:

1. A nota fica estável e vendável — o build comercial só não inclui `_precos/`.
2. Atualizar preço não suja a nota nem invalida sua revisão no Protocolo 92.
3. Validade muito mais curta: `data_cotacao` obrigatória e **90 dias** para
   vencer (nota técnica tolera 12 meses). Vencida, a resposta avisa em vez de
   repetir número velho com cara de certeza.
4. Várias locadoras convivem para o mesmo item, cada uma com sua data — que é
   como o mercado funciona.

**O que destrava:** preço estruturado + calculadora de storage + notas de
equipamento = orçamento montado pelo cérebro, e a pergunta "qual câmera me dá
o melhor resultado por real neste job" cruzando com `budget_alternative_to`.

Ao implementar: atualizar a pergunta Q28 do conjunto-ouro, que hoje afirma que
preço está fora de escopo.

## Segurança

**Quando marcar `risco: seguranca` — decisão explícita, nunca por omissão:**

| caso | marca? |
|---|---|
| a nota descreve procedimento, norma ou limite cuja violação causa dano físico | **sim** |
| a nota é de função ou documento que *aponta* para uma norma, sem prescrever o procedimento | não — mas declara `requires:` para a nota de norma |
| a nota traz cálculo que vira decisão de instalação | não na nota; o **disclaimer vai na saída da ferramenta** |

Exemplo do acervo: `nr-35-trabalho-em-altura` é `risco: seguranca`; `gaffer`
não é, mas declara `requires: [nr-35-trabalho-em-altura]` — porque descreve
quem responde, não como executar.

Notas com `risco: seguranca` (elétrica, rigging, altura, RF, drone):
- só fonte `oficial` ou norma;
- **revisão humana 100%**, nunca amostral;
- disclaimer obrigatório de que não substitui profissional habilitado.

## Ausência ≠ negação

Campo ou aresta **omitido significa "desconhecido"**, nunca "não tem".
Negação verificada é explícita: `nd_interno: nao` com fonte.
Quem consulta não pode inferir incapacidade a partir de silêncio.

No grafo, a negação verificada é o bloco `rel_na` — "não se aplica, e eis o
porquê":

```yaml
rel:
  made_by: [sony]
rel_na:
  outputs_signal: "corpo sem saída de vídeo — só grava interno (manual, p. 12)"
```

Dispensa sem motivo é reprovada pelo CI. É afirmação sobre o mundo, sujeita à
mesma exigência de evidência que uma spec — não botão de silenciar aviso.

## Arestas mínimas por `type`

Cada `type` tem um conjunto mínimo de arestas em `_meta/arestas-minimas.md`,
cobrado pelo `validate.py` (aviso em `draft`, erro em `reviewed`). Câmera sem
`records_codec` não é nota incompleta por descuido — é nota que não responde à
pergunta pela qual alguém a abriu.

Piso que vale para todo tipo: **ao menos uma aresta que não seja `see_also`**.

## Estados

`status`: `stub` → `draft` → `reviewed` (+ `revisar` quando a fonte mudar)
`confidence`: `alta` | `media` | `baixa`

`reviewed` significa: passou pelo Protocolo 92 com nota ≥ 92 e scorecard
arquivado. Ver `_meta/qa/protocolo-92.md`.

## Direito autoral

Base legal: **Lei 9.610/98** — fatos e informações não são protegidos
(art. 8º); citação curta com atribuição para estudo e crítica (art. 46).
Não usamos a doutrina de *fair use*, que é americana.

Na prática: **destilação em expressão própria + link + citação curta**.
Nunca reproduzir manual, tabela extensa ou texto integral de terceiro.
PDF de terceiro fica **fora do repositório** (ver `.gitignore`) — no Git só
entra o manifesto com URL e hash.
