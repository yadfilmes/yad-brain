# Arestas mínimas por `type`

O item 3 da rubrica R-N cobra "arestas completas e específicas para o tipo de
nó". Enquanto isso era julgamento do revisor, o produtor não tinha como
conferir antes de gastar revisão — e o item reprovou em 100% das notas
avaliadas. Este arquivo fecha o que "completas" significa, tipo por tipo, e o
`validate.py` passa a cobrar.

**Fonte única da verdade.** O `validate.py` lê este arquivo, do mesmo jeito que
lê o `edge-vocabulary.md`. Mudar a regra é editar aqui, não o script.

Como o resto do CI: **avisa em `draft`, reprova em `reviewed`.** A dívida
aparece enquanto se escreve, não na hora de promover.

---

## Piso universal (vale para todo tipo, menos dois)

Toda nota fora de `stub` declara **ao menos uma aresta que não seja
`see_also`**. `see_also` é "relacionado, sem semântica específica" — uma nota
cujo grafo inteiro é `see_also` não afirma nenhuma relação, só vizinhança.

**Isentos: `moc` e `orgao`.** Não é concessão, é a semântica dos dois tipos:

- Um **MOC** é um mapa. "Relacionado, sem semântica específica" é literalmente
  o que um mapa afirma sobre o que lista — exigir aresta tipada ali forçaria
  relação inventada.
- Um **órgão** recebe suas arestas fortes de fora: normas apontam para ele com
  `governed_by`. O vocabulário não tem aresta de saída própria de órgão (não
  existe `publishes`), e criar uma só para satisfazer esta regra seria deixar a
  régua desenhar a ontologia — inversão que este acervo evita.

A isenção foi descoberta pela própria regra: ela apontou 22 notas, e 5 delas
estavam certas. Regra nova erra nas duas direções, e a que reprova o correto é
a mais cara — some no ruído de aviso e ensina a ignorar o CI.

---

## Conjuntos por tipo

Formato lido pelo script:

- `obrigatorias:` — cada uma precisa existir (ou ser dispensada, ver abaixo)
- `uma de:` — ao menos uma do grupo; pode haver vários grupos

### `camera`

- obrigatorias: `made_by`, `has_native_mount`, `records_codec`, `accepts_media`, `outputs_signal`, `competes_with`
- uma de: `uses_battery_mount`, `powered_by`
- uma de: `alternative_to`, `budget_alternative_to`, `successor_of`, `predecessor_of`

Justificativa: são as perguntas que se faz de uma câmera antes de fechar
locação — quem fabrica, o que encaixa na frente, o que sai gravado, em que
cartão, o que sai pelo cabo, com que se alimenta, contra quem compete e o que
serve de substituto. Toda câmera profissional responde a todas.

### `switcher`

- obrigatorias: `made_by`, `accepts_signal`, `outputs_signal`, `competes_with`
- uma de: `part_of_ecosystem`, `interoperates_with`
- uma de: `controls`, `controlled_by`

Justificativa: switcher é um nó de I/O — entra sinal, sai sinal, e ele comanda
ou é comandado por algo (painel, câmera, automação). Sem isso é ficha de
catálogo.

### `fixture`

- obrigatorias: `made_by`, `competes_with`
- uma de: `powered_by`, `uses_battery_mount`
- uma de: `fits`, `part_of_ecosystem`, `accessory_for`

Justificativa: luminária sem "de onde vem a energia" e "o que encaixa nela"
(bowens, Chimera, grade própria) não permite montar um kit.

### `codec`

- obrigatorias: `made_by`
- uma de: `alternative_to`, `competes_with`
- uma de: `wraps_in`, `conforms_to_pipeline`, `paired_gamut`, `supports_colorspace`

Justificativa: a pergunta operacional sobre codec é sempre comparativa ("uso
este ou aquele?") e de container/cor ("abre onde, em que pipeline").

### `mount`

- obrigatorias: `made_by`
- uma de: `alternative_to`, `competes_with`, `successor_of`, `adapts`

Justificativa: mount só existe em relação a outro mount — flange, adaptação,
sucessão. Um mount isolado não informa nada.

### `midia`

- uma de: `implements_standard`, `governed_by`, `made_by`
- uma de: `alternative_to`, `competes_with`, `successor_of`

Justificativa: mídia profissional é padrão de consórcio, não produto de uma
marca — por isso `made_by` entra como alternativa, não como obrigatória. O que
não falta nunca é o par "com o que compete / o que substituiu".

### `colorspace` · `transfer-function`

- obrigatorias: `made_by`
- uma de: `paired_gamut`, `conforms_to_pipeline`, `governed_by`

Justificativa: curva e gamut andam em par; declarar um sem o outro é a origem
clássica de erro de pipeline.

### `interface`

- uma de: `implements_standard`, `governed_by`
- uma de: `alternative_to`, `competes_with`, `interoperates_with`

Justificativa: interface é norma encarnada em conector — quem normatiza e o que
faz o mesmo trabalho são as duas perguntas.

### `funcao`

- uma de: `reports_to`, `part_of_department`
- uma de: `produces`, `consumes`, `used_in_workflow`, `operated_by_role`

Justificativa: função se define por posição na cadeia e por entrega. Nota de
função sem nenhum dos dois é descrição de vaga, não conhecimento de set.

### `documento`

- uma de: `template_for`, `used_in_workflow`
- uma de: `produces`, `consumes`, `operated_by_role`, `used_by_role`

Justificativa: papelada só significa alguma coisa amarrada ao processo que a
gera e a quem a preenche.

### `problema`

- obrigatorias: `caused_by`, `resolved_by`
- uma de: `diagnosed_with`, `known_issue`

Justificativa: nó de diagnóstico sem causa e sem correção não resolve nada em
set. `diagnosed_with` é o teste que discrimina entre causas concorrentes.

### `norma`

- obrigatorias: `governed_by`
- uma de: `implements_standard`, `supersedes`, `requires`, `used_in_workflow`

Justificativa: norma sem órgão emissor é boato.

### `marca`

- uma de: `competes_with`, `owned_by`, `sub_brand_of`, `part_of_ecosystem`

Justificativa: era o buraco mais visível do acervo — 5 de 5 notas de marca
tinham só `see_also`. As arestas fortes de uma marca chegam **de fora**
(produtos apontam com `made_by`); o que ela declara de si é posição de mercado
e controle societário.

---

## Tipos deliberadamente abertos

`conceito`, `orgao`, `ecossistema`, `moc`, `certificacao`, `battery-mount`,
`pipeline-cor`

Não têm conjunto mínimo, e isso é decisão, não esquecimento. `conceito` é
heterogêneo demais para fechar (obturador 180°, LUT, genlock e temperatura de
cor não compartilham esqueleto). `orgao` e `battery-mount` recebem quase todas
as arestas de fora. Publicar um conjunto que não se sustenta seria repetir o
defeito que este arquivo existe para consertar — regra que o revisor cobra e
ninguém consegue auditar.

Para esses tipos vale o **piso universal**, que já é a regra que morde: pelo
menos uma aresta com semântica.

---

## Quando a aresta não se aplica: `rel_na`

O acervo tem uma convenção dura — **ausência ≠ negação**. Um conjunto mínimo
obrigatório entraria em rota de colisão com ela se a única saída fosse inventar
a aresta. A saída honesta é declarar a dispensa, com motivo:

```yaml
rel:
  made_by: [sony]
rel_na:
  outputs_signal: "corpo sem saída de vídeo — só grava interno (manual, p. 12)"
```

Regras:

- `rel_na` sem motivo não vale — a chave sozinha é reprovada.
- Uma aresta não pode estar em `rel` e em `rel_na` ao mesmo tempo.
- `rel_na` aparece no diff e é auditável pelo revisor. É uma **afirmação sobre
  o mundo**, sujeita à mesma exigência de fonte que qualquer outra.

O que `rel_na` não é: botão de silenciar o CI. Dispensa sem motivo verificável
é o mesmo defeito de uma spec sem fonte, deslocado para o grafo.
