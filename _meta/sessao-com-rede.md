# Como rodar a sessão com rede (destravar o B1)

O bloqueio B1 é **política de egresso do ambiente**, não limite do projeto.
Este documento é o roteiro para a sessão que o destrava.

---

## Qual caminho escolher

### Opção A — Claude Code na sua máquina · **recomendada**

Você já tem o repositório no SSD. Rodar localmente **não passa por proxy
nenhum**: `WebFetch` e `curl` funcionam direto, e dá para abrir PDF de manual.

```bash
cd "/Volumes/U34 Bolt/Claude/YAD BRAIN/yad-brain"
git pull origin claude/audiovisual-brain-repository-p1r4l2
claude
```

*(no Windows o caminho muda; a pasta é a mesma, `YAD BRAIN/yad-brain`)*

**Confirme que destravou, antes de qualquer outra coisa:**

```bash
curl -sS -o /dev/null -w "%{http_code}\n" https://www.arri.com
```

`200` — destravado. `403` — ainda há proxy no caminho.

### Opção B — Claude Code na web, com outro ambiente

Criar um ambiente com política de rede mais ampla em
[code.claude.com/docs/en/claude-code-on-the-web](https://code.claude.com/docs/en/claude-code-on-the-web),
e abrir a sessão nele apontando para a mesma branch. Funciona, mas depende de
qual política está disponível para a sua conta — a opção A não depende de nada.

---

## O que pedir na sessão

Cole isto:

> Rode a passada de verificação de fontes (R3). A fila está em
> `_meta/fila-verificacao.md`, ordenada por organização, segurança primeiro.
> Regras em `_meta/conventions.md`, seção "A ordem das operações".
>
> Para cada fonte: abra a URL de verdade, localize o trecho que sustenta a
> afirmação da nota, preencha `cit` com as palavras da fonte e `loc` com o
> localizador real. Se a fonte não sustentar o que a nota diz, **corrija a
> nota** — nunca ajuste o `cit` para caber.
>
> Rode `python3 tools/validate.py` ao fim de cada organização e
> `python3 tools/fila_verificacao.py` para ver a fila encolher.

---

## Por onde começar, e por quê

A fila já está na ordem certa, mas o raciocínio importa:

| ordem | grupo | por quê |
|---|---|---|
| 1º | **`gov.br`** (NR-10, NR-35, ANATEL, MTE) | são as notas de **segurança**. O gate G4 exige fonte oficial, e hoje elas citam documento que ninguém abriu. Além disso o texto das NRs é público e paginado — `loc` vira `item 10.2.1`, que é o que a convenção pede |
| 2º | **ARRI · Sony · Blackmagic** | ~36 das 63 fontes. Documentação boa e paginada; resolve mais da metade da fila |
| 3º | o resto | consórcios e fabricantes menores |

**Uma organização por vez, `validate.py` ao fim de cada uma.** Não vale a pena
tentar fazer tudo de uma sentada.

---

## O que vai acontecer (e é bom que aconteça)

Espere que **algumas notas estejam erradas**. Já aconteceu três vezes só com
busca:

- `prores` citava uma URL da Apple que **não existe**;
- `x-ocn` expandia a sigla errado **no próprio título**;
- `cri-tlci-ssi` atribuía quatro métricas a um órgão só.

Com acesso real às fontes, a taxa vai subir, não descer. **Isso é o instrumento
funcionando** — cada erro achado agora é um erro que não vai para o time.

Quando a fonte contradisser a nota: **a fonte ganha.** Corrigir a nota, e se o
erro for de uma classe nova, registrar em `_meta/qa/scorecards/`.

---

## Ao terminar

1. `python3 tools/fila_verificacao.py` — a fila deve estar bem menor
2. `python3 tools/validate.py && python3 tools/build_graph.py`
3. Atualizar `_meta/qa/blocked.md`: **B1 destravado**, com a data
4. Aí sim rodar o Protocolo 92 sobre um lote — pela primeira vez com o gate G3
   alcançável, e portanto pela primeira vez com chance real de aprovar

---

## O que isto destrava

Hoje **nenhuma nota pode chegar a `reviewed`**, por melhor que seja: o gate G3
exige fonte `oficial`/`lab` com transcrição, e sem rede a transcrição não
existe. Foi por isso que 14 notas avaliadas em 5 lotes deram 0 aprovadas.

Com o B1 fora do caminho, o corte 92 volta a ser uma pergunta sobre **a
qualidade da nota** — que é o que ele sempre deveria ter medido.
