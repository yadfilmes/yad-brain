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
| `RESUMO` | ninguém | timbrado, ficha de responsáveis, entradas, imposto, saídas por área, lucro, caixa — tudo fórmula |
| `SAIDAS` | produção | um gasto por linha, área escolhida numa listinha |
| `AREAS` | quem organiza | a lista de áreas; escrever uma nova aqui já aparece no RESUMO |

**Regra de ouro:** quem preenche mexe só em `SAIDAS`. Célula amarela é campo
para digitar; o resto é fórmula.

## Timbrado e ficha de responsáveis

O topo do `RESUMO` traz logo, razão social, CNPJ e contatos da YAD, e logo
abaixo a ficha que diz **quem elaborou, quem atualizou por último, em que data
e em que versão**. É o que transforma a planilha de rascunho pessoal em
documento que circula entre produção e financeiro: sem essa ficha, três
arquivos com o mesmo nome não têm como ser ordenados.

`--atualizado-por "Fulano"` carimba a data de hoje junto. Nome e data andam
sempre em par — separá-los é exatamente como o campo acaba mentindo. Os mesmos
dados vão para as propriedades do arquivo (autor, título, empresa).

A paleta é amostrada do próprio logo: `#7C3184` (roxo) → `#5CA1DC` (azul), com
`#6973B8` no meio. Verde e vermelho ficam reservados para significado — lucro
positivo e valor sem área — e nunca viram cor de marca.

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
python3 tools/pressuposto_real.py --config job.json --saida JOB_v2.xlsx \
        --atualizado-por "Fulano" --versao v2                           # revisão
```

O logo sai de `tools/assets/yad-logo.png`; `--logo outro.png` troca. Arquivo
ausente não derruba a geração — sai sem marca e avisa no terminal.

## Comissão de captação

```
--comissao 15 --comissao-base liquida    # ou: --comissao-base bruta
```

Sem o parâmetro, não nasce linha nenhuma — job sem captador fica igual.

**A base muda o valor e "15% do job" é ambíguo.** Sobre a bruta de R$ 225.000
dá R$ 33.750; sobre a líquida de R$ 189.000 dá R$ 28.350 — R$ 5.400 que só
aparecem na hora de pagar. Por isso a base sai escrita em três lugares: rótulo
do percentual, coluna FUNÇÃO e observação.

O valor é fórmula (`=ROUND(RESUMO!$C$24*RESUMO!$F$22,2)`), não número: mudar o
imposto ou o percentual recalcula a comissão, e a observação se reescreve
junto. Sem circularidade — a líquida não depende das saídas.

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
- **Zero por não ser custo ≠ zero por faltar preencher.** As duas linhas somam
  igual e significam o oposto. O que separa é o `STATUS`: linha que o cliente
  cobre fica **sem status** — nada a pagar — e a `OBS` diz quem cobre. Linha
  ainda em aberto fica `A PAGAR` com o valor amarelo. Sem essa distinção, três
  meses depois ninguém sabe se aquele campo vazio era cortesia ou esquecimento.
- **Equipe de salário fixo entra zerada — e a margem do job engana.** Quem é do
  quadro já recebeu no dia 5: linha com valor zero e status vazio. No Yamaha
  isso apagou R$ 27.600 e levou a margem de 16,2% a 54,1% — verdadeiro para o
  job, falso para o mês. Reporte o par: lucro do job e a folha que ele consumiu
  a preço de mercado.
- **Parcela recebida ≠ parcela combinada.** O bloco `CAIXA` separa "já andou"
  de "falta"; lucro no papel com 50% a receber não paga fornecedor.
- **Rótulo de célula não pode começar com `=`** — o Excel lê como fórmula.
  Custou um `#REF!` no primeiro teste.

## Conexões

Consome o orçamento fechado e a escala de equipe; alimenta o financeiro e o
fechamento do job. Anda junto da [[ordem-do-dia]]: a escala que a ordem do dia
publica é a mesma que vira linha de `EQUIPE` aqui.
