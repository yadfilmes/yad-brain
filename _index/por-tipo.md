# Índice por tipo

Gerado por `tools/build_graph.py` — não editar à mão.

## battery-mount

- [[bat--b-mount]] — padrão de bateria de 24 V criado por consórcio (ARRI, Bebob, Core SWX) para equipamento que consome mais do qu

## camera

- [[alexa-35]] — câmera de cinema Super35 da ARRI com sensor 4.6K de geração nova (ALEV 4) e o salto de latitude que definiu a 
- [[fx6]] — câmera de cinema full-frame compacta da Sony com sensor 10,2 MP BSI, **ND eletrônico interno variável** e dual
- [[pyxis-6k]] — câmera de cinema full-frame 6K da Blackmagic que grava [[braw]] internamente, vendida em versões de mount dist
- [[venice]] — primeira geração da linha VENICE: sensor full-frame 6K, dual base ISO 500/2500 e gravação [[x-ocn]] em [[midia
- [[venice-2]] — câmera de cinema digital full-frame da Sony com sensor 8.6K (há versão 6K no mesmo corpo), dual base ISO 800/3

## certificacao

- [[netflix-approved]] — lista de câmeras que a Netflix aceita como principal em produções originais. O critério central é **resolução 

## codec

- [[arriraw]] — formato RAW não comprimido (ou com compressão sem perdas) das câmeras ARRI: os dados do sensor saem sem debaye
- [[braw]] — codec RAW parcialmente debayerizado da Blackmagic: guarda a informação de sensor como RAW, mas move parte do p
- [[prores]] — família de codecs intraframe da Apple que virou o padrão de fato para mezanino e entrega em pós: cada quadro é
- [[x-ocn]] — formato de negativo digital da Sony, gravado pelos corpos VENICE. Guarda a informação de sensor com compressão
- [[xavc]] — família de codecs de gravação da Sony baseada em H.264/H.265, usada dos corpos de broadcast aos de cinema como

## colorspace

- [[arri-wide-gamut-4]] — espaço de cor da ARRI para a geração ALEV 4 ([[alexa-35]]), par obrigatório da curva [[log-c4]]. Sucede o ARRI
- [[rec-709]] — o padrão de cor da televisão HD e, na prática, o denominador comum de entrega até hoje: gamut relativamente pe
- [[s-gamut3-cine]] — espaço de cor da Sony pensado para trabalho de cinema: mais contido que o S-Gamut3 puro, o que o torna mais fá

## conceito

- [[cri-tlci-ssi]] — quatro métricas que tentam responder "essa luz reproduz cor direito?". **CRI é a mais citada e a mais fraca**;
- [[filtro-nd]] — filtro cinza que corta luz sem (idealmente) alterar cor, para manter diafragma aberto e obturador 180° sob sol
- [[genlock]] — sinal de referência comum que faz vários equipamentos varrerem o quadro no mesmo instante. Sem ele, cada câmer
- [[lei-do-inverso-do-quadrado]] — dobrar a distância entre a luz e o sujeito derruba a intensidade a **um quarto** (dois stops), não à metade. É
- [[obturador-180]] — manter o obturador em 180° (velocidade = 1 ÷ (2 × frame rate)) entrega o borrão de movimento a que o olho está
- [[pwm-brilho-led]] — LED não regula intensidade baixando tensão: ele **pisca muito rápido** e o tempo ligado define o brilho aparen
- [[rede-gigabit]] — vídeo sobre IP exige rede **dedicada**: gigabit no mínimo, switch gerenciado, e nada de compartilhar com a int
- [[scan-rate]] — quantas vezes por segundo o painel redesenha a imagem inteira, em Hz. O olho humano se satisfaz com pouco; **a
- [[shuttersync]] — recurso das processadoras Brompton que alinha a varredura do painel com o obturador da câmera, permitindo ajus
- [[switcher-me]] — **M/E (Mix/Effects)** é um bloco completo de mistura: escolhe fontes, aplica transição e chaves, e entrega um 
- [[tally]] — luz que avisa **quem está no ar** (vermelho) e, em muitos sistemas, quem está no preview (verde). Parece detal
- [[temperatura-de-cor]] — CCT, em Kelvin, descreve se a luz é "quente" (3200 K, tungstênio) ou "fria" (5600 K, luz do dia). Mas **um eix

## documento

- [[mapa-de-luz]] — planta baixa da cena com posição, altura, modificador e potência de cada fixture, mais a posição de câmera. Se
- [[ordem-do-dia]] — documento diário que diz a **cada pessoa** onde estar, a que horas, para filmar o quê. Emitido pela assistênci

## ecossistema

- [[ecossistema-blackmagic]] — o conjunto de câmera, switcher, gravador, conversores e software da Blackmagic desenhado para funcionar junto:

## fixture

- [[evoke-2400b]] — COB bicolor de 2400 W, na faixa de potência que compete com HMI grande. É a resposta da categoria a quem preci
- [[ls-600d-pro]] — COB de 600 W daylight com montagem Bowens, resistente a intempérie e alimentável por AC ou bateria. Virou o ca

## funcao

- [[diretor-de-fotografia]] — responsável autoral pela imagem: define câmera, lente, luz, paleta e movimento, em serviço da narrativa que o 
- [[gaffer]] — chefe do departamento de elétrica: transforma a intenção do diretor de fotografia em plano executável de luz, 

## interface

- [[ndi]] — vídeo profissional trafegando sobre rede Ethernet comum, com descoberta automática de fontes. Troca cabo coaxi
- [[sdi]] — padrão de vídeo profissional sobre cabo coaxial com conector BNC: **trava**, aceita tirada longa e não negocia

## marca

- [[aputure]] — fabricante fundada em 2013, sede em Shenzhen, que reposicionou o mercado de iluminação: potência e recursos de
- [[arri]] — fabricante alemã centenária, referência de cinema em três frentes ao mesmo tempo: câmeras (ALEXA), iluminação 
- [[blackmagic-design]] — fabricante australiana que mudou o preço-base do mercado: câmeras de cinema, switchers ATEM, conversores, grav
- [[nanlux]] — marca de alta potência da chinesa **NANGUANG** (Guangdong NANGUANG Photo & Video Systems), irmã da Nanlite e p
- [[sony]] — fabricante japonesa presente em quase toda a cadeia audiovisual: câmeras de cinema (CineAlta/VENICE), broadcas

## midia

- [[midia--axs]] — mídia proprietária da Sony para as câmeras VENICE, exigida pelas taxas do [[x-ocn]]. Exclusiva do ecossistema:
- [[midia--cfexpress-a]] — formato menor do padrão CFexpress, adotado pela Sony nas linhas Alpha e Cinema Line. **Não é intercambiável co
- [[midia--cfexpress-b]] — padrão aberto de cartão de alta velocidade (PCIe/NVMe por baixo), adotado por praticamente todo fabricante de 

## moc

- [[00-indice-mestre]] — ponto de entrada humano do acervo. Ler este arquivo custa pouco e diz para onde ir; ler o acervo inteiro custa

## mount

- [[mount--e]] — mount eletrônico da Sony com flange focal distance curto (18 mm), usado da mirrorless de entrada ao topo de ci
- [[mount--lpl]] — mount da ARRI criado para formato grande: diâmetro maior e flange focal distance menor que o [[mount--pl]] (44
- [[mount--pl]] — mount padrão do cinema profissional, criado pela ARRI: trava mecânica de quatro flanges, sem contatos elétrico

## norma

- [[nr-35-trabalho-em-altura]] — norma regulamentadora brasileira que rege qualquer atividade executada acima de 2 metros do nível inferior com

## orgao

- [[ampas]] — a Academia (a mesma do Oscar) mantém um braço de ciência e tecnologia que publica padrões de uso corrente na i
- [[itu-r]] — órgão da ONU que publica as recomendações da série **BT**, que definem os padrões de imagem de televisão do mu
- [[mte]] — órgão federal que edita e mantém as **Normas Regulamentadoras (NRs)**, de cumprimento obrigatório em qualquer 
- [[smpte]] — sociedade de engenheiros que normatiza boa parte da infraestrutura técnica de cinema e televisão: [[sdi]], tim

## pipeline-cor

- [[aces]] — sistema de gerenciamento de cor da Academia: cada câmera entra por uma **IDT** (transformação de entrada), tod

## problema

- [[flicker-parede-led]] — a câmera enxerga bandas horizontais, cintilação ou linha rolando sobre a parede de LED. Quase sempre é dessinc

## switcher

- [[atem-constellation-8k]] — switcher de produção ao vivo em 2RU com **4 M/E**, **40 entradas 12G-SDI** e 16 keyers, com conversão de padrã
- [[atem-constellation-hd]] — linha de switchers ATEM Constellation **distinta do modelo 8K**, para produção que não precisa de 8K nem de 40

## transfer-function

- [[log-c4]] — curva logarítmica da ARRI para a geração ALEVE 4 ([[alexa-35]]), desenhada para a latitude maior desse sensor.
- [[s-log3]] — curva logarítmica da Sony que comprime a latitude do sensor num sinal de 10 bits sem estourar altas nem esmaga
