# Vocabulário de arestas (fechado)

Toda relação em `rel:` no frontmatter **precisa** estar nesta lista. O
`validate.py` lê este arquivo e rejeita qualquer aresta fora dele — é o que
impede a deriva do esquema conforme o acervo cresce.

Regra de uso: **preferir sempre a aresta específica.** `compatible_with` e
`see_also` são último recurso, não atalho.

Formato aceito no frontmatter:

```yaml
rel:
  records_codec: [braw, prores]                        # lista simples
  accepts_mount: [{to: mount--pl, via: adaptador-x}]   # com propriedades
```

Propriedades reconhecidas: `to` (obrigatória na forma longa), `via`, `limite`,
`motivo`, `desde_firmware`, `ate_firmware`, `nota`, `ratio`.

## Proveniência e identidade

- `made_by` — fabricado/comercializado por · ex: Alexa 35 → ARRI
- `part_of_series` — pertence à família · ex: Bolt 6 LT → Teradek Bolt
- `sub_brand_of` — marca de valor da mesma casa. **Datar sempre:** relação de
  marca muda — amaran era `sub_brand_of` Aputure até o spin-off de 2024. Marcas
  irmãs sob a mesma empresa não são sub-marcas uma da outra: aí é `owned_by`
  para a mãe e `distinct_from` entre si (Nanlux e Nanlite → NANGUANG)
- `owned_by` — controle societário · ex: RED → Nikon
- `variant_of` — variante do mesmo corpo/plataforma · ex: VENICE 2 6K → VENICE 2

## Compatibilidade física e elétrica

- `has_native_mount` — mount de fábrica · ex: VENICE 2 → E-mount
- `accepts_mount` — aceita (nativo ou por troca/adaptador)
- `adapts` — adaptador liga mount A a B
- `mounts_via` — lente funciona no corpo através de um adaptador
- `fits` — encaixe mecânico · ex: Light Dome → bowens
- `uses_battery_mount` — padrão de alimentação · ex: Alexa 35 → B-Mount
- `powered_by` — fonte de energia
- `accepts_media` — mídia gravável aceita
- `compatible_with` — fallback genérico (usar só quando nada específico serve)
- `incompatible_with` — incompatibilidade **conhecida e verificada** (usar `motivo`)

## Sinal, dados e formato

- `records_to` — grava na mídia
- `records_codec` — grava/encoda o formato
- `wraps_in` — codec dentro de container
- `outputs_signal` / `accepts_signal` — I/O de sinal
- `converts` — conversão de formato A→B
- `streams_via` — protocolo de contribuição/stream
- `implements_standard` — conforma a uma norma
- `supports_colorspace` — gamut suportado
- `supports_transfer_function` — curva log/HDR suportada
- `paired_gamut` — curva ↔ gamut que andam juntos
- `conforms_to_pipeline` — framework de cor
- `syncs_via` — timecode/genlock
- `controls` / `controlled_by` — comando

## Mercado, ecossistema e ciclo de vida

- `part_of_ecosystem` — integra um sistema interoperante
- `pairs_with` — par consagrado de campo
- `competes_with` — rival direto (simétrica)
- `alternative_to` — substituto de qualquer tier
- `budget_alternative_to` — versão barata de (usar `ratio`)
- `successor_of` / `predecessor_of` — linhagem
- `accessory_for` — acessório de
- `certified_for` — aprovação formal · ex: → Netflix Approved
- `interoperates_with` — trabalham juntos via padrão

## Pessoas, processo e craft

- `used_by_role` / `operated_by_role` — quem opera
- `part_of_department` — lotação
- `reports_to` — cadeia de comando
- `used_in_workflow` — onde entra no processo
- `produces` / `consumes` — I/O de um workflow
- `template_for` — papelada ↔ processo
- `enables_technique` — equipamento viabiliza técnica
- `requires` — pré-requisito
- `governed_by` — norma → órgão
- `supersedes` — substitui norma/versão anterior

## Diagnóstico (troubleshooting)

- `known_issue` — equipamento → problema conhecido
- `caused_by` — problema → causa provável
- `resolved_by` — problema → correção
- `diagnosed_with` — problema → teste que discrimina

## Associação livre

- `distinct_from` — "não confundir com" (combate sinônimo falso)
- `see_also` — relacionado, sem semântica específica

---

## Simetria e direção

| Aresta | Comportamento |
|---|---|
| `competes_with` | **simétrica** — se A compete com B, B compete com A (o `build_graph.py` gera a recíproca) |
| `successor_of` ↔ `predecessor_of` | **inversas** — declarar uma; a outra é derivada |
| `caused_by` / `resolved_by` | direcionais, sempre a partir do nó `problema` |
| demais | direcionais, declaradas no nó de origem |
