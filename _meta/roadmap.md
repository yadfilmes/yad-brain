# Roadmap — capacidades planejadas

Decisões já tomadas e desenhadas que **ainda não foram implementadas**.
Existe para que não se percam entre uma sessão e outra.

Diferente de `_meta/gaps.md` (notas que faltam escrever, gerado por script) e
de `_meta/qa/blocked.md` (o que está travado por motivo externo).

---

## R1 · Camada de preços · **prioridade alta**

Diária por equipamento em camada separada (`_precos/`), zona `yad`, com
`data_cotacao` obrigatória e validade de 90 dias.

Desenho completo em `_meta/conventions.md`, seção "Preço".

**Destrava:** orçamento montado pelo cérebro, e a comparação custo × resultado
cruzando com `budget_alternative_to`.
**Ao implementar:** atualizar a Q28 do conjunto-ouro.

---

## R2 · Calculadoras · **as quatro de prioridade alta estão feitas**

Só existe `tools/calc/storage.py`. Ordem de valor por esforço:

| família | uso | estado |
|---|---|---|
| mídia / storage | diário | **feito** |
| parede de LED | gabinetes, portas, potência, peso, shutter × scan × refresh | **feito** |
| elétrica | corrente, circuitos, cabo/queda, gerador, balanceamento de fase | **feito** |
| óptica | FOV, enquadramento, profundidade, hiperfocal, equivalência | **feito** |
| áudio / timecode | conversão 23.976 ↔ 29.97, drift, delay por distância | sob demanda |
| redes | ST 2110, NDI, SRT | adiado até haver job IP |
| RF | **rejeitada como calculadora** — usar Wireless Workbench; o acervo precisa é da nota "RF no Brasil (ANATEL)" | — |

---

## R3 · Passada de verificação de fontes · **bloqueada**

Nenhuma nota vira `reviewed` sem conferir fonte contra documentação oficial e
preencher `loc`. Exige rede — ver `_meta/qa/blocked.md`, bloqueio B1.

Roteiro: percorrer as notas na ordem de `_meta/gaps.md`, abrir a fonte oficial
de cada uma, registrar página/tabela/seção.

---

## R4 · Domínios ainda não escritos

Ordem sugerida (a de captação e cor já existem):

1. **Iluminação e elétrica** — o maior em volume e o mais usado no dia a dia
2. **Live e broadcast** — espinha de sinal feita (SDI, NDI, M/E, tally, rede); faltam switchers, roteamento e intercom
3. **Produção** — DoP, gaffer, ordem do dia e mapa de luz feitos; faltam demais funções e documentos
4. **Áudio** — microfones, wireless, mixers, timecode
5. **Grip e suporte**
6. **Pós** — softwares, plugins, entrega (DCP/IMF), arquivo (LTO, ASC MHL)

---

## R5 · Site estático · **fase 3**

Vista derivada publicada (tipo Quartz) com busca e link compartilhável.
Decisão tomada: **privado para o time** primeiro; abertura ou venda depois.
Ver `_meta/conventions.md` para o zoneamento que já prepara isso.

---

## R6 · Tier `campo-proprio` · **decisão do dono pendente**

O tier existe nas convenções, mas nunca foi usado. É a experiência técnica de
set da própria equipe — a fonte de maior valor e menor risco jurídico do
acervo, e o que mais diferencia este cérebro de qualquer documentação pública.

Exige uma exceção explícita à regra de isolamento: experiência técnica
generalizada e anonimizada entra; dado de cliente, contrato e orçamento não.

**Rito sugerido:** post-mortem técnico de 15 minutos ao fim de cada job →
notas novas ou corrigidas.
