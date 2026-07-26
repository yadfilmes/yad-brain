# Fila de verificação de fontes (R3)

Gerado por script — **não editar à mão.** Regenerar com:

```
python3 tools/fila_verificacao.py
```

**63 fontes** `oficial`/`lab` sem `cit`, em **55 notas**, de **21 organizações**.

## Como usar

Trabalhar **por organização**, não por nota: abrir o site do fabricante uma vez
e resolver todas as fontes dele de uma vez é muito mais rápido que pular entre
domínios. A ordem abaixo é por volume decrescente.

Para cada linha:

1. Abrir a URL. Se não resolver, **a URL é o defeito** — achar a página certa.
2. Localizar o trecho que sustenta a afirmação da nota.
3. Preencher `cit` com o trecho **nas palavras da fonte**, sem traduzir.
4. Ajustar `loc` para o localizador real (`p. 12, tab. 3`), não o título.
5. Se a fonte **não sustentar** o que a nota diz: corrigir a nota, não o `cit`.

Rodar `python3 tools/validate.py` ao fim de cada organização.

**Notas com `risco: seguranca` vêm primeiro** — o gate G4 exige fonte oficial,
e hoje elas citam documento que ninguém abriu.

## `www.gov.br` — 4 fonte(s) · 🔴 contém nota de SEGURANÇA

- [ ] **conceitos/orgaos/anatel.md**
  - https://www.gov.br/anatel/pt-br
  - `loc` atual: portal institucional
  - a nota diz que daqui vem: NAO aberta nesta sessao - egresso bloqueado, ver _meta/qa/blocked.md B1
- [ ] **conceitos/orgaos/mte.md**
  - https://www.gov.br/trabalho-e-emprego/pt-br
  - a nota diz que daqui vem: órgão responsável pelas NRs
- [ ] **seguranca/nr-10-eletricidade.md** · 🔴 SEGURANÇA
  - https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/arquivos/normas-regulamentadoras/nr-10.pdf
  - `loc` atual: texto integral da NR-10 (PDF do MTE)
  - a nota diz que daqui vem: fonte canonica; NAO foi aberta nesta sessao - egresso bloqueado, ver _meta/qa/blocked.md B1
- [ ] **seguranca/nr-10-eletricidade.md** · 🔴 SEGURANÇA
  - https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-10-nr-10
  - `loc` atual: pagina da NR-10 vigente
  - a nota diz que daqui vem: confirmar a versao em vigor antes de usar

## `look` — 1 fonte(s) · 🔴 contém nota de SEGURANÇA

- [ ] **luz/fixtures/hmi.md** · 🔴 SEGURANÇA
  - https://look.ams-osram.com/m/2bde01adc88df0fe/original/HMI-Family-PIB-US-version-EN.pdf
  - `loc` atual: HMI Metal Halide Lamp Family - product information bulletin
  - a nota diz que daqui vem: folha da familia HMI da OSRAM. NAO foi aberta nesta sessao - egresso bloqueado, ver _meta/qa/blocked.md B1. Entra como ancora de procedencia oficial exigida pelo gate G4, e e a primeira fonte a conferir quando houver rede

## `arri` — 12 fonte(s)

- [ ] **_meta/vocab/bat--b-mount.md**
  - https://www.arri.com/en/technical-data/accessories
  - a nota diz que daqui vem: adoção do padrão
- [ ] **_meta/vocab/midia--codex-compact-drive.md**
  - https://www.arri.com/en/cine-systems/cine-camera-components/recording-media/codex-compact-drive
  - `loc` atual: Codex Compact Drive
  - a nota diz que daqui vem: capacidades 1 TB e 2 TB, uso em ALEXA
- [ ] **_meta/vocab/mount--lpl.md**
  - https://www.arri.com
  - a nota diz que daqui vem: especificação do mount LPL
- [ ] **_meta/vocab/mount--pl.md**
  - https://www.arri.com
  - a nota diz que daqui vem: origem ARRI do padrão
- [ ] **captacao/cameras/arri/alexa-35.md**
  - https://www.arri.com/en/camera-systems/cameras/legacy-camera-systems/alexa-35
  - `loc` atual: Tech Data - sensor, mount, codecs, outputs
  - a nota diz que daqui vem: duas saidas 12G-SDI independentes no modelo padrao
- [ ] **captacao/cameras/arri/alexa-35.md**
  - https://www.arri.com/en/cine-systems/cine-camera-components/recording-media/codex-compact-drive
  - `loc` atual: Codex Compact Drive
  - a nota diz que daqui vem: capacidades e variante Express
- [ ] **conceitos/cor/arri-wide-gamut-4.md**
  - https://www.arri.com/en/learn-help/learn-help-camera-system/image-science
- [ ] **conceitos/cor/log-c4.md**
  - https://www.arri.com/en/learn-help/learn-help-camera-system/image-science
  - a nota diz que daqui vem: documentação de ciência de cor
- [ ] **conceitos/tecnicas/obturador-180.md**
  - https://www.arri.com
  - a nota diz que daqui vem: convenção de ângulo de obturador
- [ ] **luz/conceitos/lei-do-inverso-do-quadrado.md**
  - https://www.arri.com/en/lighting
  - a nota diz que daqui vem: dados fotométricos por distância
- [ ] **luz/conceitos/temperatura-de-cor.md**
  - https://www.arri.com/en/lighting
  - a nota diz que daqui vem: faixas de CCT dos fixtures
- [ ] **marcas/arri.md**
  - https://www.arri.com/en/company/the-arri-philosophy/arri-global-locations/arrial
  - `loc` atual: ARRIAL in Munich
  - a nota diz que daqui vem: sede em Munique desde a fundacao

## `sony` — 12 fonte(s)

- [ ] **_meta/vocab/bat--bp-u.md**
  - https://pro.sony/ue_US/products/camera-batteries-and-power-supplies/bp-u35
  - `loc` atual: BP-U35 Lithium-ion Battery (35 Wh)
  - a nota diz que daqui vem: capacidade 35 Wh e tensao 14,4 V
- [ ] **_meta/vocab/bat--bp-u.md**
  - https://pro.sony/ue_US/products/camera-batteries-and-power-supplies/bp-u70
  - `loc` atual: BP-U70 Lithium-ion Battery (72 Wh)
  - a nota diz que daqui vem: capacidade 72 Wh
- [ ] **_meta/vocab/midia--axs.md**
  - https://pro.sony/ue_US/products/memory-cards
  - a nota diz que daqui vem: linha de cartões profissionais
- [ ] **_meta/vocab/midia--sxs.md**
  - https://pro.sony/s3/2018/06/27094815/4735109141-1.pdf
  - `loc` atual: VENICE - Recording media
  - a nota diz que daqui vem: SxS para XAVC/ProRes/MPEG HD interno na VENICE
- [ ] **_meta/vocab/mount--e.md**
  - https://pro.sony
- [ ] **captacao/cameras/sony/fx6.md**
  - https://www.sony.com/electronics/interchangeable-lens-cameras/ilme-fx6v-b
  - `loc` atual: pagina de produto - Specifications: sensor, ISO, recording e ND
  - a nota diz que daqui vem: sensor, dual base ISO, formatos e ND eletronico
- [ ] **captacao/cameras/sony/venice-2.md**
  - https://pro.sony/ue_US/products/digital-cinema-cameras/venice-2
  - a nota diz que daqui vem: specs de sensor, ISO e mídia
- [ ] **captacao/cameras/sony/venice.md**
  - https://pro.sony/s3/2018/06/27094815/4735109141-1.pdf
  - `loc` atual: Digital Motion Picture Camera VENICE - Recording media e Interfaces
  - a nota diz que daqui vem: XAVC/ProRes/MPEG HD em SxS interno; X-OCN e RAW 16 bits exigem AXS-R7 com AXSM; saida SDI 6G/12G comutavel
- [ ] **conceitos/codecs/xavc.md**
  - https://pro.sony/ue_US/technology/xavc
  - a nota diz que daqui vem: família de formatos
- [ ] **conceitos/cor/s-gamut3-cine.md**
  - https://pro.sony/ue_US/technology/s-log
- [ ] **conceitos/cor/s-log3.md**
  - https://pro.sony/ue_US/technology/s-log
  - a nota diz que daqui vem: definição da curva e uso
- [ ] **marcas/sony.md**
  - https://pro.sony/ue_US/products/digital-cinema-cameras
  - `loc` atual: Digital Cinema Cameras
  - a nota diz que daqui vem: linhas VENICE, BURANO e FX

## `blackmagicdesign` — 9 fonte(s)

- [ ] **captacao/cameras/blackmagic/pyxis-6k.md**
  - https://www.blackmagicdesign.com/products/blackmagicpyxis
  - a nota diz que daqui vem: sensor, mounts e codecs
- [ ] **conceitos/sinais/genlock.md**
  - https://www.blackmagicdesign.com
  - a nota diz que daqui vem: sync generator e entradas de referência
- [ ] **live/conceitos/switcher-me.md**
  - https://www.blackmagicdesign.com/products/atem
  - a nota diz que daqui vem: arquitetura de M/E e keyers
- [ ] **live/conceitos/tally.md**
  - https://www.blackmagicdesign.com/products/atem
  - a nota diz que daqui vem: saídas de tally
- [ ] **live/switchers/atem-constellation-8k.md**
  - https://www.blackmagicdesign.com/products/atemconstellation8k/techspecs
  - `loc` atual: Tech Specs - Mixing Engine, Video Inputs, Video Outputs, Audio Mixer e Physical Installation
  - a nota diz que daqui vem: M/E, entradas, saidas, keyers, DVEs, audio e formato
- [ ] **live/switchers/atem-constellation-8k.md**
  - https://www.blackmagicdesign.com/products/atemconstellation8k/features
  - `loc` atual: Features - Multi View
  - a nota diz que daqui vem: layouts de multiview e tally
- [ ] **live/switchers/atem-constellation-8k.md**
  - https://www.blackmagicdesign.com/products/atemconstellation8k/softwarecontrol
  - `loc` atual: Software Control - multiplos operadores
  - a nota diz que daqui vem: varios controles de software simultaneos
- [ ] **marcas/blackmagic-design.md**
  - https://www.blackmagicdesign.com/au/company
  - `loc` atual: Company
  - a nota diz que daqui vem: sede em Melbourne, linhas de produto
- [ ] **marcas/ecossistema-blackmagic.md**
  - https://www.blackmagicdesign.com
  - a nota diz que daqui vem: linhas de produto e integração

## `bromptontech` — 3 fonte(s)

- [ ] **led-vp/conceitos/pwm-brilho-led.md**
  - https://www.bromptontech.com
  - a nota diz que daqui vem: processamento e profundidade de bits em baixo brilho
- [ ] **led-vp/conceitos/scan-rate.md**
  - https://www.bromptontech.com
  - a nota diz que daqui vem: documentação de processamento e refresh
- [ ] **led-vp/conceitos/shuttersync.md**
  - https://www.bromptontech.com
  - a nota diz que daqui vem: recurso de sincronização de obturador

## `nanlux` — 3 fonte(s)

- [ ] **_meta/vocab/mount--nanlux.md**
  - https://www.nanlux.com/about
  - `loc` atual: About
  - a nota diz que daqui vem: linhas de fixture e acessorios proprios da marca
- [ ] **luz/fixtures/nanlux/evoke-2400b.md**
  - https://www.nanlux.com/product/evoke-2400b
  - a nota diz que daqui vem: potência e fotometria
- [ ] **marcas/nanlux.md**
  - https://www.nanlux.com/about
  - `loc` atual: About
  - a nota diz que daqui vem: posicionamento da marca e linhas

## `acescentral` — 2 fonte(s)

- [ ] **conceitos/cor/aces.md**
  - https://docs.acescentral.com/background/overview/
  - `loc` atual: ACES System - Overview
  - a nota diz que daqui vem: arquitetura IDT / espaco de trabalho / ODT
- [ ] **conceitos/cor/aces.md**
  - https://docs.acescentral.com/encodings/acescct/
  - `loc` atual: ACEScct Specification
  - a nota diz que daqui vem: encoding log em primarias AP1, para grading scene-referred

## `aputureus` — 2 fonte(s)

- [ ] **_meta/vocab/mount--bowens.md**
  - https://www.aputureus.com/about-us.html
  - `loc` atual: About Us
  - a nota diz que daqui vem: adocao do padrao pela linha Aputure; a marca Bowens original nao opera mais
- [ ] **marcas/aputure.md**
  - https://www.aputureus.com/about-us.html
  - `loc` atual: About Us
  - a nota diz que daqui vem: fundacao em 2013, sede em Shenzhen, linhas de produto

## `itu` — 2 fonte(s)

- [ ] **conceitos/cor/rec-709.md**
  - https://www.itu.int/rec/R-REC-BT.709
  - a nota diz que daqui vem: recomendação ITU-R BT.709
- [ ] **conceitos/orgaos/itu-r.md**
  - https://www.itu.int/rec/R-REC-BT
  - a nota diz que daqui vem: série BT de recomendações

## `ndi` — 2 fonte(s)

- [ ] **live/sinais/ndi.md**
  - https://ndi.video/tech/
  - a nota diz que daqui vem: especificação e variantes
- [ ] **live/sinais/rede-gigabit.md**
  - https://ndi.video/tech/
  - a nota diz que daqui vem: requisitos de rede

## `smpte` — 2 fonte(s)

- [ ] **conceitos/orgaos/smpte.md**
  - https://www.smpte.org/standards
  - a nota diz que daqui vem: biblioteca de normas
- [ ] **live/sinais/sdi.md**
  - https://www.smpte.org/standards
  - a nota diz que daqui vem: série de normas SDI

## `abnt` — 1 fonte(s)

- [ ] **conceitos/orgaos/abnt.md**
  - https://www.abnt.org.br
  - `loc` atual: pagina institucional
  - a nota diz que daqui vem: NAO aberta nesta sessao - egresso bloqueado, ver _meta/qa/blocked.md B1

## `aputure` — 1 fonte(s)

- [ ] **luz/fixtures/aputure/ls-600d-pro.md**
  - https://www.aputure.com/products/ls-600d-pro
  - a nota diz que daqui vem: potência, fotometria e controle

## `cined` — 1 fonte(s)

- [ ] **captacao/cameras/sony/fx6.md**
  - https://www.cined.com/sony-fx6-lab-test-external-prores-raw-vs-internal-xavc-intra/
  - `loc` atual: Lab Test - Dynamic Range e Rolling Shutter
  - a nota diz que daqui vem: faixa dinamica com SNR declarado e rolling shutter medido

## `codex` — 1 fonte(s)

- [ ] **_meta/vocab/midia--codex-compact-drive.md**
  - https://help.codex.online/content/recording-media/compact-drive
  - `loc` atual: Compact Drive
  - a nota diz que daqui vem: variantes e limites de gravacao

## `compactflash` — 1 fonte(s)

- [ ] **_meta/vocab/midia--cfexpress-b.md**
  - https://www.compactflash.org/cfexpress
  - a nota diz que daqui vem: especificação do padrão

## `netflixstudios` — 1 fonte(s)

- [ ] **conceitos/certificacoes/netflix-approved.md**
  - https://partnerhelp.netflixstudios.com/hc/en-us/articles/360000579527
  - a nota diz que daqui vem: requisitos de câmera para originais

## `oscars` — 1 fonte(s)

- [ ] **conceitos/orgaos/ampas.md**
  - https://www.oscars.org/science-technology

## `tech` — 1 fonte(s)

- [ ] **luz/conceitos/cri-tlci-ssi.md**
  - https://tech.ebu.ch/docs/tech/tech3355.pdf
  - `loc` atual: EBU Tech 3355 - Method for the Assessment of the Colorimetric Properties of Luminaires
  - a nota diz que daqui vem: definicao do TLCI pela EBU

## `tiffen` — 1 fonte(s)

- [ ] **conceitos/tecnicas/filtro-nd.md**
  - https://tiffen.com
  - a nota diz que daqui vem: escala de densidade e tipos
