---
id: pressuposto-real
title: Pressuposto real (orçamento fechado → caixa da produção)
type: documento
zona: universal
aliases: ["pressuposto", "presuposto", "pressuposto real", "orçamento real", "orcamento real", "distribuição real", "distribuicao real", "real do job", "budget real", "actuals"]
tags: [producao, financeiro, documento, orcamento, planilha]
status: draft
confidence: media
updated: 2026-08-10
rel:
  template_for: [producao]
  used_in_workflow: [producao]
  used_by_role: [produtor-executivo, diretor-de-fotografia]
  see_also: [ordem-do-dia]
sources:
  - {url: "arquivo interno YAD: PRESSUPOSTO_LIVE_BYD_23_E_24.06.xlsx", tier: campo-proprio, ret: 2026-08-10, loc: "aba '.', linhas 9-103", cit: "CONCEITO EQUIPE / CONCEITO DIVERSOS / IMPOSTO / COMISSÃO / CONCEITO ALIMENTAÇÃO / CONCEITO TRANSPORTE ... NOTA FISCAL 15% ... RESUMO GERAL / TOTAL DE ENTRADAS / TOTAL DE DESPESAS / LUCRO", nota: "estrutura em blocos por área e o fecho entradas − despesas = lucro; alíquota de 15% naquele job"}
  - {url: "arquivo interno YAD: BARRETOS_2026__V2.xlsx", tier: campo-proprio, ret: 2026-08-10, loc: "Sheet1, linhas 50-67", cit: "TÉCNICO SISTEMA - TODAS AS DIÁRIAS / ASSISTENTE GERAL - TODAS AS DIÁRIAS / TÉCNICO CAMERAS - TODAS AS DIÁRIAS ... VALOR EQUIPE ... PROPOSTA FINAL ALEX (VALOR 2025 +8% INFLAÇÃO)", nota: "diárias de equipe como preço de venda, e o valor fechado que virou a entrada bruta do pressuposto"}
---

# Pressuposto real (orçamento fechado → caixa da produção)

**TL;DR** — orçamento é o que o **cliente paga**; pressuposto real é o que a
**produção gasta**. São dois documentos, nunca o mesmo arquivo editado. A conta
que liga um ao outro é sempre a mesma: `entrada bruta − imposto = entrada
líquida`, e é da **líquida** que sai todo pagamento. Gerar com
`tools/pressuposto_real.py`.

## Por que não se edita o orçamento

O orçamento tem preço de tabela, desconto negociado e itens que existem para
compor valor. O pressuposto tem cachê combinado, combustível, hospedagem e
conserto de caminhão — coisas que nunca apareceram na proposta. Reaproveitar o
arquivo mistura as duas verdades e produz o erro clássico: **planejar gasto em
cima do valor bruto**, esquecendo que o imposto já comeu uma fatia.

## As três abas

| aba | quem mexe | o que tem |
|---|---|---|
| `RESUMO` | ninguém | entradas, imposto, saídas por área, lucro, caixa — tudo fórmula |
| `SAIDAS` | produção | um gasto por linha, área escolhida numa listinha |
| `AREAS` | quem organiza | a lista de áreas; escrever uma nova aqui já aparece no RESUMO |

**Regra de ouro:** quem preenche mexe só em `SAIDAS`. Célula amarela é campo
para digitar; o resto é fórmula.

## A conta, na ordem

```
entrada bruta  (o que o cliente paga, somando as parcelas)
  − imposto    (% sobre a bruta — 16% na YAD hoje)
= entrada líquida
  − saídas     (equipe + transporte + alimentação + hospedagem + …)
= lucro
```

A **alíquota fica numa célula só**, editável, no bloco de entradas. Job com
regime diferente é trocar aquele número, não refazer a planilha.

## Áreas padrão

`EQUIPE` · `TRANSPORTE E LOGÍSTICA` · `ALIMENTAÇÃO` · `HOSPEDAGEM` ·
`EQUIPAMENTO E MANUTENÇÃO` · `LOCAÇÃO DE TERCEIROS` · `PRODUÇÃO E DIVERSOS` ·
`COMISSÃO`

As seis primeiras vieram dos blocos que a YAD já usava no pressuposto da BYD;
`HOSPEDAGEM` e `EQUIPAMENTO E MANUTENÇÃO` entraram porque job de estrada tem
diária de hotel e caminhão que quebra — e isso não cabia em "diversos".

## Como gerar

```
python3 tools/pressuposto_real.py --saida PRESSUPOSTO_JOB.xlsx          # em branco
python3 tools/pressuposto_real.py --exemplo job.json                    # molde do config
python3 tools/pressuposto_real.py --config job.json --saida JOB.xlsx    # já preenchido
```

O `job.json` guarda entradas, saídas e áreas. Vale versionar junto do job: é
ele, não a planilha, que registra de onde cada número veio.

## Gotchas

- **Cachê de equipe não é o valor do orçamento.** A linha "TÉCNICO CÂMERAS
  R$ 500/diária" na proposta é preço de venda; o combinado com a pessoa é outro
  número. Puxar um pelo outro infla ou espreme o lucro sem ninguém notar.
- **Uma linha de gasto, uma área.** Sem área, o valor cai na linha
  `SEM ÁREA` do resumo — que fica vermelha de propósito. O total nunca perde
  dinheiro, mas a distribuição mente até alguém classificar.
- **Quem entra sem cachê entra mesmo assim**, com valor zero. Some da conta,
  não some da escala — e no ano seguinte ninguém lembra que ele estava lá.
- **Parcela recebida ≠ parcela combinada.** O bloco `CAIXA` separa "já andou"
  de "falta"; lucro no papel com 50% a receber não paga fornecedor.
- **Rótulo de célula não pode começar com `=`** — o Excel lê como fórmula.
  Custou um `#REF!` no primeiro teste.

## Conexões

Consome o orçamento fechado e a escala de equipe; alimenta o financeiro e o
fechamento do job. Anda junto da [[ordem-do-dia]]: a escala que a ordem do dia
publica é a mesma que vira linha de `EQUIPE` aqui.
