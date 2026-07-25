# YAD BRAIN — Cérebro Audiovisual

Base de conhecimento técnico do audiovisual profissional — câmeras, óptica, luz,
elétrica, painéis de LED, produção ao vivo, pós-produção, funções de set,
segurança e normas — construída como **repositório Git de arquivos Markdown**,
estruturada como **grafo navegável** e desenhada para ser consultada por IA
(Claude) com custo mínimo de tokens.

> **Estado atual: Fase 0 — fundação.** O acervo de conhecimento ainda não existe.
> Este repositório contém, por enquanto, a arquitetura, a metodologia de qualidade
> e o histórico de decisões do projeto.

---

## O princípio

**Para a IA, o sistema de arquivos é o banco de dados.** Não há banco vetorial,
banco de grafos, servidor ou API. O Claude lê os arquivos com `Grep`/`Glob`/`Read`
— busca exata, local, instantânea e gratuita. O grafo mora em relações tipadas no
frontmatter YAML de cada nota; índices e visualizações são **sempre derivados** do
conteúdo, nunca uma segunda fonte de verdade.

Consequência prática: qualquer interface (site, painel, app) é uma **vista** sobre
este repositório. Se a interface sumir, o cérebro continua íntegro. Se este
repositório sumir, não há interface que o salve — por isso ele é a única coisa
que importa preservar.

---

## Estrutura

```
_meta/
  qa/          Protocolo 92 — metodologia de validação (nota de corte 92/100)
  history/     Documentos de origem do projeto (planos, pareceres)
```

A árvore de conhecimento (`captacao/`, `luz/`, `pos/`, `live/`, `producao/`,
`seguranca/`, `conceitos/`, `troubleshooting/`…) entra na Fase 1.

### Documentos-chave

| Arquivo | O que é |
|---|---|
| `_meta/qa/protocolo-92.md` | **Como validamos tudo.** Nenhum artefato é aceito abaixo de 92/100 numa rubrica binária revisada em contexto limpo. Aprovado pela própria régua no ciclo 3 (35 → 75 → 100). |
| `_meta/history/plano-v1.0.md` | Plano de projeto original: arquitetura, ontologia, roadmap. |
| `_meta/history/parecer-cruzado-v1.md` | Revisão cruzada por 4 frentes independentes + confronto com o plano alternativo. ~40 correções que originam a v1.1. |
| `_meta/history/plano-mestre-chatgpt-2026-07-23.md` | Plano alternativo avaliado (fonte de várias absorções). |

---

## Como trabalhar neste repositório

O mesmo diretório serve três consumidores ao mesmo tempo:

| Quem | Como | Para quê |
|---|---|---|
| **Você (edição/navegação)** | Obsidian, abrindo a pasta como *vault* | Escrever, navegar o grafo, ver backlinks. O app de celular guarda tudo **offline** — o que salva em set sem sinal. |
| **Claude (consulta/construção)** | Claude Code apontado nesta pasta | Perguntar, pesquisar, escrever notas, rodar validações. |
| **Git** | `commit` / `push` | Versão, histórico e backup — a única cópia que importa. |

### Instalar no SSD externo (macOS)

```bash
# 1. Ir até a pasta desejada no SSD (aspas por causa dos espaços no nome)
cd "/Volumes/U34 Bolt/Claude"

# 2. Clonar o repositório
git clone https://github.com/yadfilmes/yad-brain.git

# 3. Entrar e ver o estado
cd yad-brain && git log --oneline
```

Resultado: `/Volumes/U34 Bolt/Claude/yad-brain`

Depois disso:
- **Obsidian** → *Open folder as vault* → aponte para essa pasta.
- **Claude Code** → abra essa pasta como diretório de trabalho.
- **Sincronizar**: `git pull` antes de trabalhar, `git push` ao terminar. O
  plugin *Obsidian Git* automatiza isso se preferir.

> **Sobre trabalhar em disco externo:** funciona bem, mas o SSD costuma ficar
> fora do Time Machine. Não tem problema — **o GitHub é o backup**. Só não
> desconecte o disco com o Obsidian ou o Claude escrevendo; se acontecer,
> `git status` mostra o estrago e um novo `clone` resolve.

---

## Qualidade

Todo artefato deste projeto passa pelo **Protocolo 92**: nota computada de
checklist binária, revisão independente em contexto limpo com instrução
adversarial, itens eliminatórios que não se compensam, e refação obrigatória
até atingir 92 — no máximo 3 ciclos, depois escala para decisão humana.

Regra de ouro do conteúdo: **número sem fonte não entra.** Lacuna honesta é
aceitável; especificação inventada, nunca.

---

## Escopo e isolamento

Projeto independente. Não contém dados de clientes, orçamentos, contratos ou
qualquer informação comercial da YAD — apenas conhecimento técnico do
audiovisual. Notas de experiência própria de set, quando existirem, são
generalizadas e anonimizadas.
