---
id: nr-10-eletricidade
title: NR-10 — Segurança em Instalações e Serviços em Eletricidade
type: norma
zona: universal
risco: seguranca
jurisdicao: BR
aliases: ["NR 10", "NR-10", "NR10", "seguranca em eletricidade", "segurança em eletricidade", "norma regulamentadora 10", "SEP"]
tags: [seguranca, norma, eletrica, brasil, treinamento, gaffer]
status: draft
confidence: baixa
updated: 2026-07-26
rel:
  governed_by: [mte]
  requires: [rede-ac]
  see_also: [nr-35-trabalho-em-altura, gaffer]
sources:
  - {url: "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/arquivos/normas-regulamentadoras/nr-10.pdf", tier: oficial, ret: 2026-07-26, loc: "texto integral da NR-10 (PDF do MTE)", nota: "fonte canonica; NAO foi aberta nesta sessao - egresso bloqueado, ver _meta/qa/blocked.md B1"}
  - {url: "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-10-nr-10", tier: oficial, ret: 2026-07-26, loc: "pagina da NR-10 vigente", nota: "confirmar a versao em vigor antes de usar"}
---

# NR-10 — Segurança em Instalações e Serviços em Eletricidade

> ⚠️ **Conteúdo de segurança.** Esta nota é referência de **planejamento** e
> **não substitui** projeto elétrico, treinamento formal nem profissional
> habilitado. Nota com `risco: seguranca` exige revisão humana integral antes
> de sair de `draft` — nenhuma norma sobe por processo automático.

**TL;DR** — norma do Ministério do Trabalho que define requisitos mínimos de
segurança para quem trabalha com eletricidade, em qualquer fase (geração,
transmissão, distribuição e **consumo** — que é onde o set vive). Obrigatória
para toda empresa regida pela CLT. Na prática de audiovisual: define **quem
pode** encostar no quadro, e o treinamento que essa pessoa precisa ter.

## O que ela exige de quem trabalha

| exigência | escopo |
|---|---|
| curso NR-10 básico | **40 h** — baixa tensão |
| complementar SEP | **+40 h** — Sistema Elétrico de Potência e proximidades |
| reciclagem | **bienal**; também em troca de função, mudança de empresa, retorno de afastamento > 3 meses, ou alteração significativa na instalação |
| abrangência | todas as empresas, públicas e privadas, regidas pela CLT |

<!-- verificar: a NR-10 passou por atualização com vigência recente; conferir
     no PDF oficial do MTE quais itens mudaram antes de usar como referência
     contratual. Nenhuma fonte desta nota foi aberta na origem — só pesquisada. -->

## Por que isso aparece em set de audiovisual

O [[gaffer]] e o eletricista de set trabalham em **consumo** — quadro de
locação, extensão, distribuição, gerador. Isso está dentro do escopo da norma,
e não vira exceção por ser filmagem.

Três consequências que aparecem no orçamento, não no set:

1. **Quem mexe no quadro precisa ser habilitado e treinado.** Não é o
   assistente disponível; é função com requisito formal.
2. **Verificação prévia da instalação** em locação com carga alta — antes do
   dia, não no dia. Ver [[rede-ac]].
3. **Responsabilidade documentada.** Produtora que contrata carga de set numa
   instalação que não aguenta assume risco trabalhista, além do físico.

## Fronteira com o que este acervo faz

A [[bitola-de-cabo]] e a calculadora de elétrica são de **planejamento e
orçamento**. Dimensionamento definitivo, laudo e instalação são de engenheiro
ou técnico com registro (CREA/CFT), sob NR-10 e ABNT NBR 5410.

O acervo serve para **chegar na conversa com o número certo** — não para
substituir a conversa.

## Estado desta nota

`confidence: baixa` e `draft`, declaradamente: **nenhuma das fontes oficiais
foi aberta na origem** — o ambiente desta sessão bloqueia egresso HTTP (ver
`_meta/qa/blocked.md`, B1), e os números acima vieram de busca, não do texto da
norma. Para uma nota de segurança isso é insuficiente por princípio, não por
formalidade.

**O que destrava:** abrir o PDF do MTE, conferir item a item, e revisão por
pessoa qualificada registrada em `revisor_humano`.
