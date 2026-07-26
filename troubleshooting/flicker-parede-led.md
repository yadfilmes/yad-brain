---
id: flicker-parede-led
title: Flicker ou banda horizontal filmando parede de LED
type: problema
zona: universal
aliases: ["flicker LED", "banda na parede de LED", "linha rolando LED", "cintilacao", "cintilação", "banding"]
tags: [led-wall, virtual-production, flicker, shutter, diagnostico]
status: draft
confidence: media
updated: 2026-07-26
rel:
  caused_by: [scan-rate, pwm-brilho-led]
  resolved_by: [shuttersync, genlock]
  diagnosed_with: [obturador-180, scan-rate]
  see_also: [obturador-180, scan-rate]
sources:
  - {url: "https://www.bromptontech.com/features/shuttersync/", tier: oficial, ret: 2026-07-26, loc: "ShutterSync - Features", nota: "exclusivo dos processadores Tessera SX40 e S8, a partir do software Tessera 3.2; opcao de Sensor Type (Any / Global / Rolling)"}
  - {url: "https://www.bromptontech.com/recreating-reality-synchronisation-artefacts/", tier: oficial, ret: 2026-07-26, loc: "Recreating Reality - Synchronisation Artefacts", nota: "mecanismo do frame blending quando a fase esta errada"}
---

# Flicker ou banda horizontal filmando parede de LED

**TL;DR** — a câmera enxerga bandas horizontais, cintilação ou linha rolando
sobre a parede de LED. Quase sempre é dessincronia entre a varredura do painel
e o obturador da câmera, não defeito do painel. Testar o shutter **antes** de
mexer em qualquer outra coisa.

## Causas prováveis, em ordem de frequência

1. **Shutter fora de múltiplo compatível** — de longe o caso mais comum.
2. **Ausência de genlock** entre câmera e processadora: sem referência comum,
   a varredura desliza ao longo do take.
3. **Scan rate baixo do painel** — painel de scan baixo entrega banda visível
   mesmo com shutter correto.
4. **ShutterSync/ajuste de fase não configurado** na processadora.
5. **Brilho muito baixo do painel**, que em alguns produtos reduz a
   profundidade efetiva de PWM e agrava a banda.

## Como discriminar

| teste | se resolver, a causa é |
|---|---|
| variar **só** o shutter (ex.: 1/50 → 1/48 → 1/100) | shutter fora de múltiplo |
| conectar genlock e repetir o take | falta de referência comum |
| subir o brilho do painel mantendo shutter | PWM/brilho |
| ajustar fase no ShutterSync da processadora | sincronia fina |

Se nenhum resolver, investigar scan rate do painel — que é característica de
hardware, não ajuste de set.

## Correções

- Casar shutter com a frequência de refresh do painel.
- Genlock entre câmera e processadora sempre que houver mais de uma câmera.
- Ajuste fino de fase na processadora — **onde existir**, ver abaixo.

### O que a fase corrige, e onde ela existe

O mecanismo: quando a fase está certa, o painel exibe **um quadro inteiro
durante todo o tempo em que o obturador está aberto**. Fase errada produz
*frame blending* — o painel começa o quadro seguinte antes de a câmera terminar
de capturar o atual.

| item | escopo |
|---|---|
| ShutterSync (Brompton) | **exclusivo** dos processadores Tessera SX40 e S8, a partir do software Tessera 3.2 |
| opção Sensor Type | `Any` (padrão, maior compatibilidade), `Global Shutter`, `Rolling Shutter` |

Isto é decisão de **orçamento de locação**, não de set: processadora fora dessa
lista não tem o ajuste, e aí a única saída é casar shutter e subir o scan rate.

## Dimensionar antes de montar

```
python3 tools/calc/led_wall.py --largura 6 --altura 3 --pitch 2.6 --fps 24
```

A seção **SINCRONIA COM A CÂMERA** devolve o refresh mínimo, o confortável e
lembra do genlock. `--largura`, `--altura` e `--pitch` são obrigatórios — boa parte deste problema se evita no orçamento, não em set.

## Quando não é isso

Se a banda **não muda** ao variar shutter, brilho e genlock, provavelmente
não é sincronia: investigar moiré (padrão do conteúdo contra a grade de
pixels), linha de LED defeituosa (banda fixa, sempre na mesma altura) ou
cabo de dados com mau contato (banda intermitente e localizada).

## Observação de confiança

Nota `draft` com `confidence: media`: a ordem das causas vem de padrão de campo
relatado, não de teste controlado. Os valores exatos de scan rate e o
comportamento por produto precisam sair da documentação do fabricante antes de
virar `reviewed`.
