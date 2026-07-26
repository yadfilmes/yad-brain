# Scorecard — Lote 04 · rubrica R-N v1.2

| | |
|---|---|
| Data | 2026-07-26 |
| Rubrica | **R-N v1.2** — primeira aplicação com os itens 3 e 11 auditáveis |
| Revisor | agente independente, contexto limpo, instrução adversarial |
| Propósito | testar a régua destravada: **92 é alcançável?** |
| Resultado | **0 de 3 aprovadas** · 63 · 49 · 73 |

| nota | G1 | G2 | G3 | nota |
|---|---|---|---|---:|
| `conceitos/cor/aces.md` | **fail** | pass | **fail** | 63 |
| `luz/conceitos/cri-tlci-ssi.md` | **fail** | pass | **fail** | 49 |
| `troubleshooting/flicker-parede-led.md` | **fail** | pass | **fail** | 73 |

Ciclo anterior destas notas **anulado** pela meta-regra 11 (medido com régua de
máximo efetivo 84). Este é o ciclo 1 sob a v1.2.

## O que a v1.2 provou que funciona

- **Item 3 passou nas três.** A conversão para mecânico fez exatamente o que
  devia: o revisor conferiu o veredito da máquina em vez de recriar o critério.
  Mais do que isso — ele **encontrou um defeito de grafo real** em
  `cri-tlci-ssi` e **recusou-se a usá-lo** para reprovar o item 3, registrando-o
  como defeito de régua a corrigir por PR. É a meta-regra 8 sendo respeitada
  por quem tinha incentivo para ignorá-la.
- **G2 passou nas três.** O piso mecânico segura o que promete.
- **Item 11 finalmente mede.** Reprovou nas três, e com evidência citando a
  linha aplicável da tabela — impossível na v1.0, quando não havia tabela.
- **A nota mais alta subiu de 70 para 73** sob um revisor **mais rigoroso**,
  que desta vez conferiu se a fonte sustenta a afirmação.

## O achado central: 3 de 3 reprovaram G1, e nenhuma por número inventado

| nota | defeito de G1 | classe |
|---|---|---|
| `aces` | "ODT (Output Transform)" — ODT é Output **Device** Transform; "Output Transform" é RRT+ODT de ACES 1.1 em diante. A nota apagou o RRT da arquitetura | termo trocado, atribuído a fonte que diz o contrário |
| `cri-tlci-ssi` | "é posição dos próprios órgãos" — posições da CIE e da IES atribuídas a um tutorial de terceiro em tier `educacao`; nenhum documento CIE ou IES citado | posição institucional sem a instituição |
| `flicker-parede-led` | opção *Sensor Type* colocada no escopo "Tessera 3.2"; é recurso de **3.4**. E o comando publicado do `led_wall.py` **não roda** | valor certo no escopo errado |

Somando à FX6 (5 de 6 defeitos da mesma classe): **8 de 9 defeitos de G1 em
duas rodadas são má transcrição, zero são número inventado.**

**Mecanismo, nomeado pelo revisor:** *"a anotação `nota:` da fonte está sendo
escrita a partir da memória do modelo e depois carimbada com a URL."* Não é
falta de pesquisa — a FX6 provou isso com esforço máximo. É a ordem das
operações: escreve-se a afirmação, depois procura-se a URL que a hospede.

## Defeitos nas próprias ferramentas — verificados um a um

O revisor acusou quatro coisas checáveis. **As quatro procedem**, e duas são
código escrito na mesma sessão que criou a régua:

| acusação | verificação | veredito |
|---|---|---|
| `led_wall.py --fps 24` não roda | executado: `error: informe --largura, --altura e --pitch`, exit 2 | **procede** |
| `confianca_esperada()` é mais permissiva que a rubrica que diz aplicar | 4ª linha da tabela dizia `baixa`; script devolve `media` | **procede** |
| ODT ≠ Output Transform | `docs.acescentral.com/system-components/output-transforms/` confirma | **procede** |
| Sensor Type é 3.4, não 3.2 | busca independente devolve o manual Tessera 3.4 | **procede** |

A segunda é a mais grave: **a régua e o script que a implementa discordavam, e
a nota ficava com a leitura mais generosa.** Escritos com duas horas de
diferença, pela mesma mão, e a contradição só apareceu quando alguém de fora
leu os dois lado a lado.

## Padrões sistêmicos (do revisor, aceitos)

10. **`loc` virou campo preenchido, não localizador.** O CI checa presença; os
    cinco `loc` do lote são **títulos de página ou de documento**, não trechos.
    É o padrão nº 1 do lote 02 ("citava domínio em vez de evidência")
    reencarnado um nível abaixo: agora cita-se **documento** em vez de
    evidência. Um `loc` igual ao título da página deveria reprovar.
11. **`confidence` mede diversidade de host, não corroboração.** Nas três
    notas as fontes não se corroboram — a EBU cobre só TLCI, o tutorial cobre
    só TM-30, e em `flicker` as duas URLs são a mesma empresa. Enquanto `alta`
    for alcançável juntando dois domínios que falam de assuntos diferentes, o
    campo mede host, não confiança.
12. **O campo `nota:` de `sources[]` é a declaração de cobertura, e ninguém a
    confere contra o corpo.** Em `aces`, nenhuma das anotações mencionava
    ACEScg — e havia uma linha inteira de ACEScg com número de spec no corpo.
    Um check que compare os termos das tabelas do corpo com os termos das
    anotações pegaria isso sem rede.
13. **Lacuna declarada em prosa não é lacuna para a máquina.** `flicker`
    escreveu "os valores exatos precisam sair da documentação do fabricante" em
    português corrido; como não usou `<!-- verificar -->`, a regra que derruba
    a confiança nunca disparou. **A honestidade em prosa foi premiada com
    confiança mais alta que a mesma honestidade em marcador** — incentivo
    invertido.
14. **`governed_by` usada fora do domínio definido.** O vocabulário define
    "norma → órgão"; `cri-tlci-ssi` (`type: conceito`) e `aces`
    (`type: pipeline-cor`) a usam. O `validate.py` checa coerência de tipo do
    **alvo**, nunca da **origem** — e como `cie`, `ebu` e `ies` ainda não
    existem, nem essa checagem roda.
15. **Heurística de prática é contornável por renomear seção.** O aviso de
    "prática sob fonte oficial" dispara por literais (`## Gotchas`, "regra
    prática"). `flicker` escapou por chamar a seção de "Quando não é isso".

## Correções aplicadas nesta rodada

Fatos e ferramentas — **não** os itens de rubrica, que são plano de correção do
ciclo 2 e precisam de revisão nova:

- `aces`: RRT restaurado na arquitetura, ODT corrigido para Output **Device**
  Transform, e a mudança de significado de "Output Transform" entre ACES 1.0 e
  1.1 virou seção. Números de spec sem fonte (S-2016-001, S-2014-004)
  removidos. Fonte da página de Output Transforms acrescentada.
- `cri-tlci-ssi`: TM-30 agora carrega a revisão — IES em TM-30-15, ANSI/IES a
  partir de TM-30-18.
- `flicker-parede-led`: comando publicado corrigido para a invocação que roda.
- `rubrica-confianca.md`: contradição da 4ª × 7ª linha resolvida a favor da 7ª,
  com a justificativa escrita e o "teto do fabricante único" explicitado. Três
  casos-ouro novos travam as duas pontas.
- `aliases`: siglas do próprio título entraram nas duas notas que as omitiam.

## Veredito sobre a régua

**A régua não é o problema, e agora há evidência disso e não só aritmética.**
Ela mediu, mediu o que devia, e produziu diagnóstico acionável — inclusive
contra as ferramentas de quem a escreveu. O que reprovou foi **fidelidade à
fonte**, terceira confirmação seguida.

O corte 92 segue intacto e segue não atingido. A diferença é que agora se sabe
exatamente o que falta, e não é rigor a menos.
