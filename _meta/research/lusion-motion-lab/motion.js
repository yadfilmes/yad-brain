/**
 * motion.js — kernel de motion sem dependência.
 *
 * A camada que separa "site com animação" de "site que parece caro".
 * Nada aqui é específico de WebGL: alimenta Three.js, canvas 2D ou
 * transform de DOM igualmente bem.
 *
 * Princípio único: INPUT escreve `target`, o loop aproxima `current`.
 * Nada além do loop escreve em `current`.
 *
 * ES module, zero dependência. Ver lusion-motion-teardown.md.
 */

/* ------------------------------------------------------------------ *
 * 1. Tempo
 * ------------------------------------------------------------------ */

/**
 * Relógio único da aplicação. O teto de `dt` não é refinamento: sem ele,
 * voltar de uma aba em background entrega um delta de segundos e o frame
 * seguinte teleporta a cena (ou explode a integração do spring).
 */
export class Clock {
  constructor({ maxDelta = 1 / 30 } = {}) {
    this.maxDelta = maxDelta
    this.elapsed = 0
    this.delta = 0
    this._last = null
  }

  /** Chame uma vez por frame, antes de qualquer update. */
  tick(now = performance.now()) {
    if (this._last === null) this._last = now
    this.delta = Math.min((now - this._last) / 1000, this.maxDelta)
    this._last = now
    this.elapsed += this.delta
    return this.delta
  }
}

/* ------------------------------------------------------------------ *
 * 2. Suavização
 * ------------------------------------------------------------------ */

/**
 * Damping exponencial independente de frame rate.
 *
 *   current += (target - current) * (1 - exp(-lambda * dt))
 *
 * Aplicar 60x com dt=1/60 dá o mesmo resultado que 1x com dt=1 — é essa
 * propriedade que faz o movimento sentir igual a 60 e a 144 Hz.
 *
 * `lambda` é o único parâmetro e tem leitura física: maior = mais leve.
 * Referência: lambda=4 fecha ~98% da distância em 1 s.
 *
 * Escala sugerida (ver P3 do teardown):
 *   camera 1.5-3 · objeto 3-6 · luz/detalhe 6-10 · cursor 10-20
 */
export const damp = (current, target, lambda, dt) =>
  target + (current - target) * Math.exp(-lambda * dt)

/** Versão 2D, para não repetir a chamada em x e y. */
export const damp2 = (out, target, lambda, dt) => {
  out.x = damp(out.x, target.x, lambda, dt)
  out.y = damp(out.y, target.y, lambda, dt)
  return out
}

/** Lerp cru. Existe aqui para o banco de provas mostrar por que não usar. */
export const lerp = (a, b, t) => a + (b - a) * t

export const clamp = (v, min, max) => Math.min(Math.max(v, min), max)

/** Remapeia v de [inMin,inMax] para [outMin,outMax], com corte nas pontas. */
export const mapRange = (v, inMin, inMax, outMin, outMax) =>
  outMin +
  (clamp(v, Math.min(inMin, inMax), Math.max(inMin, inMax)) - inMin) *
    ((outMax - outMin) / (inMax - inMin))

/* ------------------------------------------------------------------ *
 * 3. Spring
 * ------------------------------------------------------------------ */

/**
 * Massa-mola-amortecedor por Euler semi-implícito, em sub-passos de
 * tamanho fixo — o sub-passo é o que mantém a integração estável mesmo
 * quando o frame atrasa.
 *
 * `damping` é o ratio ζ:
 *   1.0  crítico, nunca ultrapassa  → câmera, foco, zoom (P5)
 *   0.8  overshoot mínimo           → painel, card, sheet
 *   0.6  overshoot visível          → cursor, ícone, microinteração
 *
 * `stiffness` é ω (rad/s): 8 é lento e pesado, 20 é ágil, 40 é seco.
 */
export class Spring {
  constructor(value = 0, { stiffness = 14, damping = 0.8, maxStep = 1 / 120 } = {}) {
    this.value = value
    this.target = value
    this.velocity = 0
    this.stiffness = stiffness
    this.damping = damping
    this.maxStep = maxStep
  }

  /** Salta para o valor sem animar (setup inicial, resize, teleporte). */
  set(value) {
    this.value = this.target = value
    this.velocity = 0
    return this
  }

  update(dt) {
    const steps = Math.max(1, Math.ceil(dt / this.maxStep))
    const h = dt / steps
    const w = this.stiffness
    const z = this.damping

    for (let i = 0; i < steps; i++) {
      // a = -ω²(x - alvo) - 2ζω·v   →  semi-implícito: v primeiro, depois x
      const accel = -(w * w) * (this.value - this.target) - 2 * z * w * this.velocity
      this.velocity += accel * h
      this.value += this.velocity * h
    }
    return this.value
  }

  /** Já assentou? Útil para desligar o rAF quando a cena está parada. */
  get settled() {
    return Math.abs(this.velocity) < 1e-3 && Math.abs(this.value - this.target) < 1e-3
  }
}

/* ------------------------------------------------------------------ *
 * 4. Ponteiro
 * ------------------------------------------------------------------ */

/**
 * Ponteiro com posição suavizada E velocidade suavizada.
 *
 * A velocidade é o sinal que dá peso à cena (P4): posição controla ONDE,
 * velocidade controla QUANTO — stretch, aberração, blur, agitação. Sem
 * ela o movimento fica correto e morto.
 *
 * `.ndc` sai em [-1,1] com Y para cima, pronto para uniform / raycaster.
 */
export class Pointer {
  constructor(element = window, { lambda = 8, velocityLambda = 6, velocityScale = 1 } = {}) {
    this.lambda = lambda
    this.velocityLambda = velocityLambda
    this.velocityScale = velocityScale

    this.target = { x: 0, y: 0 }   // último input cru, em px
    this.current = { x: 0, y: 0 }  // posição perseguida, em px
    this.velocity = { x: 0, y: 0 } // px/s, suavizada
    this.speed = 0                 // magnitude, suavizada
    this.ndc = { x: 0, y: 0 }
    this.down = false

    this._prev = { x: 0, y: 0 }
    this._el = element
    this._onMove = this._onMove.bind(this)
    this._onDown = () => (this.down = true)
    this._onUp = () => (this.down = false)

    element.addEventListener('pointermove', this._onMove, { passive: true })
    element.addEventListener('pointerdown', this._onDown, { passive: true })
    window.addEventListener('pointerup', this._onUp, { passive: true })
  }

  _onMove(e) {
    this.target.x = e.clientX
    this.target.y = e.clientY
  }

  /** Centraliza no viewport — chame uma vez antes do primeiro frame. */
  center(w = innerWidth, h = innerHeight) {
    this.target.x = this.current.x = this._prev.x = w / 2
    this.target.y = this.current.y = this._prev.y = h / 2
    return this
  }

  update(dt, w = innerWidth, h = innerHeight) {
    damp2(this.current, this.target, this.lambda, dt)

    // Velocidade medida sobre a posição SUAVIZADA, não sobre o input cru:
    // o input cru chega em rajadas irregulares e a derivada dele é ruído.
    const vx = (this.current.x - this._prev.x) / Math.max(dt, 1e-4)
    const vy = (this.current.y - this._prev.y) / Math.max(dt, 1e-4)
    this._prev.x = this.current.x
    this._prev.y = this.current.y

    this.velocity.x = damp(this.velocity.x, vx * this.velocityScale, this.velocityLambda, dt)
    this.velocity.y = damp(this.velocity.y, vy * this.velocityScale, this.velocityLambda, dt)
    this.speed = Math.hypot(this.velocity.x, this.velocity.y)

    this.ndc.x = (this.current.x / w) * 2 - 1
    this.ndc.y = -(this.current.y / h) * 2 + 1
    return this
  }

  dispose() {
    this._el.removeEventListener('pointermove', this._onMove)
    this._el.removeEventListener('pointerdown', this._onDown)
    window.removeEventListener('pointerup', this._onUp)
  }
}

/* ------------------------------------------------------------------ *
 * 5. Scroll virtual
 * ------------------------------------------------------------------ */

/**
 * Scroll virtual: intercepta wheel/touch, acumula num alvo e persegue.
 * Expõe `velocity` normalizada, que é o que alimenta distorção e blur.
 *
 * Alternativa pronta e mais completa: Lenis (darkroom.engineering). Este
 * existe para o caso de zero dependência — e para deixar explícito que o
 * mecanismo é o mesmo damping de sempre, aplicado ao eixo Y.
 */
export class VirtualScroll {
  constructor({
    lambda = 5,
    wheelMultiplier = 1,
    touchMultiplier = 2,
    max = Infinity,
    element = window,
  } = {}) {
    this.lambda = lambda
    this.wheelMultiplier = wheelMultiplier
    this.touchMultiplier = touchMultiplier
    this.max = max

    this.target = 0
    this.current = 0
    this.velocity = 0        // px/s, suavizada
    this.direction = 0       // -1, 0 ou 1

    this._prev = 0
    this._touchY = null
    this._el = element

    this._onWheel = this._onWheel.bind(this)
    this._onTouchStart = this._onTouchStart.bind(this)
    this._onTouchMove = this._onTouchMove.bind(this)
    this._onTouchEnd = this._onTouchEnd.bind(this)

    // passive:false porque precisamos do preventDefault para assumir o eixo
    element.addEventListener('wheel', this._onWheel, { passive: false })
    element.addEventListener('touchstart', this._onTouchStart, { passive: true })
    element.addEventListener('touchmove', this._onTouchMove, { passive: false })
    element.addEventListener('touchend', this._onTouchEnd, { passive: true })
  }

  _add(delta) {
    this.target = clamp(this.target + delta, 0, this.max)
  }

  _onWheel(e) {
    e.preventDefault()
    // deltaMode 1 = linhas, 2 = páginas. Firefox manda linha.
    const unit = e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? innerHeight : 1
    this._add(e.deltaY * unit * this.wheelMultiplier)
  }

  _onTouchStart(e) {
    this._touchY = e.touches[0].clientY
  }

  _onTouchMove(e) {
    if (this._touchY === null) return
    e.preventDefault()
    const y = e.touches[0].clientY
    this._add((this._touchY - y) * this.touchMultiplier)
    this._touchY = y
  }

  _onTouchEnd() {
    this._touchY = null
  }

  update(dt) {
    this.current = damp(this.current, this.target, this.lambda, dt)

    const raw = (this.current - this._prev) / Math.max(dt, 1e-4)
    this._prev = this.current
    this.velocity = damp(this.velocity, raw, 6, dt)
    this.direction = Math.abs(this.velocity) < 1 ? 0 : Math.sign(this.velocity)
    return this.current
  }

  /** 0..1 sobre o comprimento total — o uniform que a cena costuma querer. */
  get progress() {
    return this.max === Infinity || this.max === 0 ? 0 : this.current / this.max
  }

  dispose() {
    this._el.removeEventListener('wheel', this._onWheel)
    this._el.removeEventListener('touchstart', this._onTouchStart)
    this._el.removeEventListener('touchmove', this._onTouchMove)
    this._el.removeEventListener('touchend', this._onTouchEnd)
  }
}

/* ------------------------------------------------------------------ *
 * 6. Easings
 * ------------------------------------------------------------------ */

/**
 * Vocabulário de saída longa (P8): acelera rápido, desacelera por muito
 * tempo. É o que soa "autoral" contra o ease-in-out padrão do CSS.
 * Use para tween de duração fixa; para o que persegue input, use damp/Spring.
 */
export const ease = {
  expoOut: (t) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t)),
  expoInOut: (t) =>
    t === 0 ? 0 : t === 1 ? 1 : t < 0.5
      ? Math.pow(2, 20 * t - 10) / 2
      : (2 - Math.pow(2, -20 * t + 10)) / 2,
  quintOut: (t) => 1 - Math.pow(1 - t, 5),
  circOut: (t) => Math.sqrt(1 - Math.pow(t - 1, 2)),
  /** Overshoot explícito, para quando o spring não cabe. */
  backOut: (t) => 1 + 2.70158 * Math.pow(t - 1, 3) + 1.70158 * Math.pow(t - 1, 2),
}

/* ------------------------------------------------------------------ *
 * 7. Acessibilidade
 * ------------------------------------------------------------------ */

/**
 * `prefers-reduced-motion` não é opcional. Com a arquitetura por estado,
 * respeitar a preferência é multiplicar todos os lambdas por um fator alto
 * — o alvo é atingido quase instantaneamente e o conteúdo continua o mesmo.
 * Retorna o multiplicador a aplicar em lambda/stiffness.
 */
export const motionScale = () =>
  typeof matchMedia === 'function' &&
  matchMedia('(prefers-reduced-motion: reduce)').matches
    ? 20
    : 1
