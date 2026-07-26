---
id: rf-anatel
title: RF sem fio no Brasil — faixas, homologação e o buraco dos 700 MHz
type: conceito
zona: universal
jurisdicao: BR
aliases: ["RF", "microfone sem fio", "wireless", "lapela sem fio", "sem fio", "ANATEL", "homologacao ANATEL", "homologação ANATEL", "700 MHz", "600 MHz", "frequencia", "frequência"]
tags: [audio, rf, wireless, brasil, anatel, regulatorio, locacao]
status: draft
confidence: baixa
updated: 2026-07-26
rel:
  governed_by: [anatel]
  requires: [timecode]
  see_also: [diretor-de-fotografia]
sources:
  - {url: "https://anatel.gov.br/legislacao/component/content/article/96-atos-de-requisitos-tecnicos-de-certificacao/2017/1139-ato-14448", tier: oficial, ret: 2026-07-26, loc: "Ato de requisitos tecnicos de certificacao", cit: "Equipamentos de microfone sem fio operando nas faixas de frequências de 54-72 MHz, 76-88 MHz, 174-216 MHz, 470-608 MHz e 614-806 MHz", nota: "faixas sujeitas aos requisitos tecnicos. NAO aberta na origem - egresso bloqueado, B1"}
  - {url: "https://musicaemercado.org/microfones-sem-fio-em-700mh/", tier: educacao, ret: 2026-07-26, loc: "Microfones sem fio em 700 MHz deverão ser trocados", cit: "as bandas disponíveis estão reservadas para a telefonia celular", nota: "o que aconteceu com a faixa apos a transicao da TV digital"}
  - {url: "https://abcpcertificacao.com.br/sobre-anatel-normas-para-certificacao-de-microfones-com-tecnologia-sem-fio/", tier: educacao, ret: 2026-07-26, loc: "Normas ANATEL para certificacao de microfones sem fio", cit: "É obrigatório que o fabricante ou importador do microfone possua uma autorização para comercializar o produto no Brasil, incluindo o registro junto à ANATEL e a obtenção de um número de homologação", nota: "a exigencia de homologacao recai sobre fabricante/importador"}
---

# RF sem fio no Brasil — faixas, homologação e o buraco dos 700 MHz

**TL;DR** — microfone sem fio no Brasil opera em **uso secundário**: divide
espectro com TV e telefonia, e **quem chegou primeiro não tem prioridade**.
A transição da TV digital e a chegada do 4G levaram embora a faixa de 700 MHz,
que era onde metade do parque de locação trabalhava. Equipamento importado sem
**homologação ANATEL** é risco jurídico, não economia.

## O que "uso secundário" significa na prática

Não é figura de linguagem: significa que **o serviço primário tem o direito**,
e o microfone tem que sair. Foi o que aconteceu quando a faixa de 700 MHz foi
destinada à telefonia móvel — equipamento legal, comprado de boa-fé, virou
inutilizável por decisão regulatória.

Consequência para orçamento: **RF é ativo com prazo de validade regulatório**,
diferente de lente ou tripé. Comprar parque grande de sem fio numa faixa é
apostar que a faixa continua disponível.

## Faixas sujeitas aos requisitos técnicos

Conforme o ato da ANATEL citado, equipamentos de microfone sem fio operando
nestas faixas atendem aos requisitos técnicos:

| faixa |
|---|
| 54–72 MHz |
| 76–88 MHz |
| 174–216 MHz |
| **470–608 MHz** |
| **614–806 MHz** |

<!-- verificar: a destinacao vigente dentro de 614-806 MHz apos a transicao da
     TV digital e a licitacao de 700 MHz. A faixa aparece no ato, mas parte
     dela foi destinada a telefonia — o ato citado e de 2017 e a situacao
     mudou. NAO usar esta tabela para decidir compra sem conferir a norma
     vigente na ANATEL. -->

## Homologação: de quem é a obrigação

A exigência recai sobre **fabricante ou importador** — registro na ANATEL e
número de homologação para comercializar no país. Para a produtora, o efeito é
prático:

| situação | risco |
|---|---|
| equipamento comprado no Brasil, com número de homologação | o esperado |
| importado direto, sem homologação | comercialização irregular; e o equipamento pode operar em faixa não permitida aqui |
| kit alugado | perguntar o número de homologação **antes**, não no dia |

Equipamento vendido para o mercado americano ou europeu costuma vir em faixas
que **não coincidem** com as brasileiras. "Funciona" e "é legal aqui" são
perguntas diferentes.

## Gotchas

- **Sempre conferir a faixa antes de fechar locação**, não o modelo. O mesmo
  modelo é vendido em versões de faixa diferente por região.
- **Varredura no local, no dia anterior quando der.** A ocupação de espectro
  muda por cidade e por horário; o que estava limpo no escritório pode não
  estar na locação.
- **Nunca improvisar canal "que estava livre da última vez".** Uso secundário
  significa exatamente que a última vez não garante nada.
- Evento grande e broadcast na mesma região disputam o mesmo espectro —
  coordenação de frequência deixa de ser luxo e vira pré-produção.

## Estado desta nota

`confidence: baixa`. Duas razões, e as duas importam:

1. **A fonte oficial não foi aberta na origem** (egresso bloqueado —
   `_meta/qa/blocked.md`, B1); a citação veio do que a busca devolveu.
2. **O ato citado é de 2017 e o espectro mudou desde então.** Esta nota serve
   para saber *quais perguntas fazer* — não para decidir compra nem para
   afirmar o que está vigente hoje.

**O que destrava:** consultar a página de legislação da ANATEL sobre serviço
auxiliar de radiodifusão, e registrar a destinação vigente por faixa com a data.
