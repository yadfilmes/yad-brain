# Conjunto-ouro de avaliação

Instrumento que mede se o cérebro **acerta**, não só se responde barato.
Executado por `tools/eval.py` (parte mecânica) e por revisão de resposta
(parte de julgamento).

## Como ler

Cada pergunta declara:

- `espera:` arquivos que a resposta correta precisa tocar. Vazio = **armadilha
  de abstenção**: o acervo não cobre, e a resposta certa é dizer isso.
- `busca:` o caminho de recuperação documentado no `AGENTS.md`
  (`glob:<slug>` · `grep:<padrão>` · `indice:<arquivo>`)
- `fatos:` termos que precisam aparecer na resposta (checagem de conteúdo)

O `tools/eval.py` verifica mecanicamente a parte de **recuperação**: se a
busca documentada encontra os arquivos esperados. A correção factual e a
qualidade da abstenção continuam exigindo leitura humana ou de agente.

## Categorias

`lookup` · `travessia` · `comparativa` · `workflow` · `gotcha` · `transversal`
`temporal` · `conflito` · `calculo` · `seguranca` · `abstencao` · `canario`

---

## lookup — fato direto

### Q01 · lookup · Qual o dual base ISO da VENICE 2?
- espera: captacao/cameras/sony/venice-2.md
- busca: glob:venice-2
- fatos: 800, 3200

### Q02 · lookup · O que é X-OCN?
- espera: conceitos/codecs/x-ocn.md
- busca: glob:x-ocn
- fatos: negativo, Sony, XT, ST, LT

### Q03 · lookup · Qual o flange focal distance do mount PL?
- espera: _meta/vocab/mount--pl.md
- busca: glob:mount--pl
- fatos: 52

### Q04 · lookup · O que significa ND 0.9?
- espera: conceitos/tecnicas/filtro-nd.md
- busca: glob:filtro-nd
- fatos: 3 stops

### Q05 · lookup · Qual a velocidade de obturador a 180 graus em 25 fps?
- espera: conceitos/tecnicas/obturador-180.md
- busca: glob:obturador-180
- fatos: 1/50

---

## travessia — exige seguir arestas

### Q06 · travessia · Gravei BRAW na Pyxis. Como levo isso para um projeto ACES?
- espera: conceitos/codecs/braw.md, conceitos/cor/aces.md
- busca: glob:pyxis-6k -> grep:conforms_to_pipeline -> glob:aces
- fatos: IDT, Film Gen5, espaço comum

### Q07 · travessia · Que mídia a VENICE 2 usa e o que isso implica no orçamento?
- espera: captacao/cameras/sony/venice-2.md, _meta/vocab/midia--axs.md
- busca: glob:venice-2 -> grep:accepts_media -> glob:midia--axs
- fatos: AXS, leitor, proprietária

### Q08 · travessia · Qual curva e qual gamut saem da ALEXA 35?
- espera: captacao/cameras/arri/alexa-35.md, conceitos/cor/log-c4.md, conceitos/cor/arri-wide-gamut-4.md
- busca: glob:alexa-35 -> glob:log-c4 -> glob:arri-wide-gamut-4
- fatos: LogC4, ARRI Wide Gamut 4

### Q09 · travessia · Lente PL serve na ALEXA 35?
- espera: captacao/cameras/arri/alexa-35.md, _meta/vocab/mount--lpl.md
- busca: glob:alexa-35 -> glob:mount--lpl
- fatos: LPL, adaptador

---

## comparativa

### Q10 · comparativa · VENICE 2 ou ALEXA 35 para um longa?
- espera: captacao/cameras/sony/venice-2.md, captacao/cameras/arri/alexa-35.md
- busca: grep:competes_with
- fatos: full-frame, Super35, latitude, resolução

### Q11 · comparativa · Qual a alternativa barata à VENICE 2?
- espera: captacao/cameras/blackmagic/pyxis-6k.md
- busca: grep:budget_alternative_to
- fatos: Pyxis, BRAW

### Q12 · comparativa · BRAW, X-OCN ou ARRIRAW: qual pesa menos?
- espera: conceitos/codecs/braw.md, conceitos/codecs/x-ocn.md, conceitos/codecs/arriraw.md
- busca: grep:alternative_to
- fatos: debayer parcial, ARRIRAW mais pesado

---

## workflow

### Q13 · workflow · Por que preciso de ND se posso fechar o diafragma?
- espera: conceitos/tecnicas/filtro-nd.md, conceitos/tecnicas/obturador-180.md
- busca: glob:filtro-nd -> glob:obturador-180
- fatos: obturador 180, desfoque, movimento

### Q14 · workflow · Como misturar ARRI e Sony no mesmo projeto sem quebrar a cor?
- espera: conceitos/cor/aces.md
- busca: glob:aces
- fatos: IDT, espaço comum, ODT

---

## gotcha — armadilha real de campo

### Q15 · gotcha · Posso usar LUT de LogC3 em material LogC4?
- espera: conceitos/cor/log-c4.md
- busca: glob:log-c4
- fatos: não, plausível, erro silencioso

### Q16 · gotcha · Filtro ND variável tem algum problema?
- espera: conceitos/tecnicas/filtro-nd.md
- busca: glob:filtro-nd
- fatos: cruz, grande-angular, dominante

### Q17 · gotcha · A parede de LED está estourando. Baixo o brilho?
- espera: led-vp/conceitos/pwm-brilho-led.md
- busca: glob:pwm-brilho-led
- fatos: piora, PWM, ND, diafragma

---

## transversal — exige índice, não grep bruto

### Q18 · transversal · Que câmeras do acervo gravam ProRes?
- espera: captacao/cameras/sony/venice-2.md, captacao/cameras/arri/alexa-35.md, captacao/cameras/sony/venice.md
- busca: grep:records_codec:.*prores
- fatos: VENICE 2, ALEXA 35

### Q19 · transversal · Quais notas são da marca Sony?
- espera: _index/por-marca.md
- busca: indice:_index/por-marca.md
- fatos: VENICE, X-OCN, S-Log3

---

## temporal

### Q20 · temporal · A VENICE 1 ainda faz sentido hoje?
- espera: captacao/cameras/sony/venice.md
- busca: glob:venice
- fatos: custo, 500, 2500, locadora

### Q21 · temporal · O mount LPL substituiu o PL?
- espera: _meta/vocab/mount--lpl.md, _meta/vocab/mount--pl.md
- busca: glob:mount--lpl -> glob:mount--pl
- fatos: adaptador, formato grande, coexistem

---

## conflito — oficial contra comunidade

### Q22 · conflito · A base ISO 3200 da VENICE 2 é utilizável de verdade?
- espera: captacao/cameras/sony/venice-2.md
- busca: glob:venice-2
- fatos: comunidade, relato, subexpor

---

## calculo — nunca de cabeça

### Q23 · calculo · Quanto storage para 6 h de ProRes 422 HQ em 4K, 2 câmeras?
- espera: tools/calc/storage.py
- busca: glob:storage
- fatos: 9.50 TB, 2.38 TB

### Q24 · calculo · Quantos cartões de 1 TB para uma diária de BRAW 12:1?
- espera: tools/calc/storage.py
- busca: glob:storage
- fatos: calculadora

### Q35 · calculo · Quantos gabinetes e quanta energia para uma parede de 6 x 3 m em P2.6?
- espera: tools/calc/led_wall.py
- busca: glob:led_wall
- fatos: 72 gabinetes, 2304, circuitos

### Q36 · calculo · Que refresh o painel precisa para filmar a 24 fps sem banda?
- espera: tools/calc/led_wall.py, led-vp/conceitos/scan-rate.md
- busca: glob:led_wall -> glob:scan-rate
- fatos: 3840, obturador, genlock

### Q37 · calculo · A locação aguenta 14 kW de parede de LED a 60 m do quadro?
- espera: tools/calc/eletrica.py
- busca: glob:eletrica
- fatos: corrente, circuitos, bitola, queda de tensão

### Q38 · seguranca · Posso dimensionar a elétrica do set eu mesmo?
- espera: tools/calc/eletrica.py, seguranca/nr-35-trabalho-em-altura.md
- busca: glob:eletrica -> glob:nr-35
- fatos: não substitui, profissional habilitado, NR-10, CREA

### Q39 · calculo · Qual a profundidade de campo de uma 50 mm em T2.8 a 3 m, full frame?
- espera: tools/calc/optica.py
- busca: glob:optica
- fatos: hiperfocal, 2.74, 3.32

### Q40 · calculo · Que focal em Super 35 dá o mesmo enquadramento de uma 50 mm full frame?
- espera: tools/calc/optica.py
- busca: glob:optica
- fatos: 1.39, 36 mm, crop

---

## seguranca — exige norma e disclaimer

### Q25 · seguranca · Preciso de algo especial para montar truss alto?
- espera: seguranca/nr-35-trabalho-em-altura.md
- busca: glob:nr-35
- fatos: NR-35, 2 metros, não substitui

### Q26 · seguranca · Quem regula isso no Brasil?
- espera: conceitos/orgaos/mte.md, seguranca/nr-35-trabalho-em-altura.md
- busca: glob:mte -> glob:nr-35
- fatos: MTE, NR

### Q41 · lookup · Qual a diferença entre 3G-SDI e 12G-SDI?
- espera: live/sinais/sdi.md
- busca: glob:sdi
- fatos: 12 Gb/s, UHD 60p, quad link

### Q42 · comparativa · SDI ou NDI para um evento multicâmera?
- espera: live/sinais/sdi.md, live/sinais/ndi.md
- busca: glob:sdi -> glob:ndi
- fatos: latência, rede dedicada, previsibilidade

### Q43 · travessia · Quantos M/E preciso num switcher para evento com telão?
- espera: live/conceitos/switcher-me.md
- busca: glob:switcher-me
- fatos: 2, composições simultâneas, aux

### Q44 · workflow · Quem responde pela carga elétrica do set?
- espera: producao/funcoes/gaffer.md
- busca: glob:gaffer
- fatos: gaffer, chefe de elétrica, locação aguenta

### Q45 · travessia · O que precisa constar num mapa de luz para orçar energia?
- espera: producao/documentos/mapa-de-luz.md, tools/calc/eletrica.py
- busca: glob:mapa-de-luz -> glob:eletrica
- fatos: potência, circuito, fase

---

## abstencao — o acervo NÃO cobre; a resposta certa é dizer isso

### Q27 · abstencao · Qual a latitude medida da Sony BURANO?
- espera:
- busca: glob:burano
- fatos: sem evidência suficiente

### Q28 · abstencao · Qual o preço de diária de uma ALEXA 35 em São Paulo?
- espera: captacao/cameras/arri/alexa-35.md
- busca: glob:alexa-35
- fatos: sem evidência suficiente, fora de escopo
- avalia: julgamento

> Abstenção de **conteúdo**, não de acervo: a nota certa é encontrada, mas não
> cobre preço — e preço está fora do escopo declarado do projeto. A recuperação
> acerta; quem precisa se abster é a resposta. Avaliação mecânica não decide
> isto: exige a rubrica R-R.

### Q29 · abstencao · Que lentes anamórficas a YAD tem em estoque?
- espera:
- busca: glob:anamorfica
- fatos: sem evidência suficiente, não é escopo deste acervo

### Q30 · abstencao · Qual o consumo em watts do SkyPanel S60-C?
- espera:
- busca: glob:skypanel
- fatos: sem evidência suficiente

### Q31 · conflito · Quantos fps a VENICE 2 faz em 4K crop?
- espera: captacao/cameras/sony/venice-2.md
- busca: glob:venice-2
- fatos: não conferido, verificar, pendente

---

## canario — a resposta no acervo contraria o prior típico de um LLM

Medem se o sistema responde **com o acervo** ou com a memória do modelo.
Falha de canário é falha de sistema, investigada fora do ciclo normal
(Protocolo 92, S.6.3).

### Q32 · canario · Para corrigir parede de LED estourada na câmera, o certo é baixar o brilho do painel?
- espera: led-vp/conceitos/pwm-brilho-led.md
- busca: glob:pwm-brilho-led
- fatos: não, piora, PWM
- prior: a intuição (e a maioria dos textos) diz que baixar brilho resolve

### Q33 · canario · A ALEXA 35 é full-frame?
- espera: captacao/cameras/arri/alexa-35.md
- busca: glob:alexa-35
- fatos: Super35, não full-frame
- prior: câmera de topo em 2026 costuma ser presumida full-frame

### Q34 · canario · ProRes RAW é uma variante do ProRes 4444?
- espera: conceitos/codecs/prores.md
- busca: glob:prores
- fatos: não, categoria diferente
- prior: o nome sugere família única

---

## Notas de manutenção

- Perguntas com `espera:` vazio são armadilhas: qualquer arquivo citado na
  resposta é **falso positivo**.
- Ao crescer o acervo, converter armadilhas em perguntas reais (Q30 vira
  `lookup` quando existir nota do SkyPanel) e criar novas armadilhas.
- Alvo do conjunto: ~90 perguntas. Faltam sobretudo `live`, `audio`,
  `iluminacao` e `producao`, domínios ainda não escritos.
