# Protocolo de consulta

Você está num acervo de conhecimento audiovisual estruturado como grafo em
Markdown. **Não leia diretórios inteiros.** Este arquivo é o mapa; siga-o.

## Como achar (nesta ordem)

1. **Caminho direto.** Os slugs são previsíveis: ASCII, kebab-case, sem acento.
   `Glob **/venice-2.md` acerta na primeira tentativa quase sempre.
2. **Alias.** Não achou? `Grep` no campo `aliases:` — lá estão apelidos,
   códigos de modelo, grafias com acento e o termo em inglês.
   Tente com e sem acento: grep é byte a byte, `iluminação ≠ iluminacao`.
3. **Índice pronto.** Pergunta transversal ("tudo que…", "quais X têm Y")
   → leia `_index/` **antes** de sair grepando o acervo:
   - `_index/por-tipo.md` · `_index/por-marca.md` — navegação por categoria
   - `_index/backlinks.md` — "quem aponta para cá?"
   - `_index/specs.csv` — projeção tabular; para filtro numérico ou
     multi-critério, processe este CSV em vez de abrir dezenas de notas
4. **Campo do frontmatter.** Pergunta estruturada vira um grep só:
   `Grep "records_codec:.*braw"` responde "o que grava BRAW?" sem abrir arquivo.
5. **Travessia do grafo.** O bloco `rel:` lista as arestas tipadas — siga os
   slugs. `_graph/graph.json` tem o grafo inteiro se precisar de caminho longo.

## Como responder

**Contrato de resposta — toda resposta declara:**
- **Fonte e tier.** `oficial` e `lab` sustentam **número**; `comunidade` e
  `campo-proprio` sustentam **prática de campo e gotcha**; `educacao` sustenta
  **síntese e contexto** — e só sustenta prática quando o trecho citado for
  ele próprio sobre a prática. Nunca troque um pelo outro.
- **Escopo.** Spec condicional vai com as condições: "120 fps *@ 4K crop,
  firmware ≥ 3.0*". Número sem escopo é meia-verdade.
- **Conflito**, quando a nota registrar um: apresente os dois lados.
- **Confiança**, quando não for `alta`.

**Abstenção é resposta correta.** Se o acervo não cobre, diga "não tenho
evidência suficiente no acervo" e registre a lacuna. Nunca preencha com
memória própria: o valor deste cérebro é ser verificável, e uma spec
inventada destrói mais do que dez notas boas constroem.

**Ausência ≠ negação.** Campo omitido significa "desconhecido", nunca "não
tem". Só afirme que algo não existe se a nota disser explicitamente — em
prosa, ou no bloco `rel_na:`, que é negação verificada e traz o motivo.

## Cálculo

Nunca calcule de cabeça. Bitrate, storage, potência, autonomia:

```
python3 tools/calc/storage.py --codec prores-422hq-4k --horas 6 --cameras 2
python3 tools/calc/storage.py --listar
```

Aritmética encadeada é onde o erro passa despercebido — por isso é função
testada, não memória.

## Segurança

Notas com `risco: seguranca` (elétrica, rigging, altura, RF, drone):
cite a norma, reproduza o disclaimer e **não improvise**. Se a resposta puder
virar decisão de set com risco físico, diga explicitamente que não substitui
profissional habilitado.

## Ao escrever: a ordem das operações

Este acervo já reprovou **8 de 9 vezes pela mesma causa** — não número
inventado, e sim **afirmação certa no escopo errado, ou atribuída a fonte que
não a sustenta**. Pesquisar mais não corrige; o que corrige é a ordem:

```
ERRADO   afirmar → achar URL que hospede → descrever a fonte
CERTO    abrir a fonte → transcrever em `cit` → escrever a partir da transcrição
```

- Fonte `oficial`/`lab` carrega **`cit`**: o trecho **nas palavras da fonte**,
  idioma original, sem paráfrase. Não dá para transcrever sem ler — é essa a
  função do campo.
- `loc` diz **onde**; `cit` diz **o quê**. Repetir o título nos dois não vale.
- Afirmação que nenhum `cit` sustenta não entra — ou vira lacuna declarada.
- **Lacuna se declara em `<!-- verificar -->`**, nunca só em prosa: em
  português corrido ela é invisível para a máquina, e a nota acaba com
  confiança mais alta do que merece.

## Ao escrever ou editar

- Modelos em `_meta/templates/` · regras em `_meta/conventions.md`
- Arestas **só** do vocabulário fechado: `_meta/edge-vocabulary.md`
- Cada `type` tem arestas obrigatórias: `_meta/arestas-minimas.md`. Não se
  aplica ao caso? Dispense em `rel_na:` **com motivo** — nunca em silêncio.
- Antes de commitar:
  ```
  python3 tools/validate.py && python3 tools/build_graph.py
  ```
- Nada em `_index/` e `_graph/` se edita à mão — é tudo derivado.
- Nota nova nasce `stub` ou `draft`. Para virar `reviewed`, passa pelo
  Protocolo 92 (`_meta/qa/protocolo-92.md`): nota ≥ 92 numa rubrica binária
  revisada em contexto limpo.

## O que fazer com lacuna

`_meta/gaps.md` é a fila de trabalho: slugs citados que ainda não existem,
ordenados por quantas notas dependem deles. Referenciar nota inexistente é
normal — é assim que a fila se forma. O que não pode é uma nota `reviewed`
apontar para o vazio.

## Custos de referência

Uma consulta bem conduzida custa entre 25 e 2.500 tokens (1 a 3 arquivos).
Se você está lendo mais que isso, provavelmente pulou um índice.
