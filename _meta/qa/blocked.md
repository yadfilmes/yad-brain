# Bloqueios de qualidade

Artefatos que não conseguem atingir 92 por motivo **externo ao texto** — e que
por isso não devem consumir mais ciclos de correção até o bloqueio sair.
Registrar aqui é a alternativa honesta a afrouxar a régua (Protocolo 92, S.1).

---

## B1 · Leitura de fonte primária — **teto de ambiente, medido em 2026-07-26**

**Diagnóstico testado, não suposto.** Duas versões anteriores deste bloqueio
estavam erradas: a primeira dizia "sem acesso à rede" (falso — eu havia
propagado relato de subagente sem testar); a segunda dizia "parcialmente
destravado" sem nomear a causa. O quadro real, medido caminho a caminho:

| caminho | estado | por quê |
|---|---|---|
| `curl` | **bloqueado** | proxy nega CONNECT com 403 |
| `WebFetch` | **bloqueado** | 403 em todos os hosts testados — `arri.com`, `en.wikipedia.org`, `tech.ebu.ch` |
| **`WebSearch`** | **funciona** | roda pela infraestrutura da Anthropic, que está no `noProxy` |

**A causa, do próprio proxy** (`/root/.ccr/README.md`):

> **403 / 407 from the proxy** — The destination host is not allowed by your
> organization's egress policy for this session. Do not retry or route around
> it — report the blocked host.

A lista de exceção do proxy confirma: passam **só** `*.anthropic.com`, os
registries de pacote (npm, jsr, PyPI, crates.io, proxy.golang.org) e faixas
privadas. Ou seja, esta sessão tem política de egresso **"registries apenas"**.
Não é bloqueio de host, é política do ambiente — e não se contorna de dentro.

### O que isso permite e o que não permite

| tarefa | possível hoje? |
|---|---|
| confirmar que uma URL existe | sim (`WebSearch`) |
| achar a página específica em vez da raiz do domínio | sim |
| obter título de seção para `loc` | sim |
| **transcrever `cit` nas palavras da fonte** | **só quando a busca devolve a frase literal** |
| abrir PDF de manual e citar página/tabela | **não** |
| conferir tabela extensa de spec sheet | **não** |

**Teto medido:** com a passada de transcrição de 2026-07-26, **9 de 65 fontes
fortes (14%)** ganharam `cit` honesta. As outras 56 continuam marcadas — não
por preguiça, mas porque a busca devolveu resumo e não as palavras da fonte.
Preencher as 56 seria trivial e destruiria o instrumento; o campo `cit` só vale
enquanto for prova de leitura.

### O que destrava

Rodar a passada de verificação num **ambiente com política de egresso mais
ampla** — decisão de quem cria o ambiente, não ajuste de sessão. Ver
`https://code.claude.com/docs/en/claude-code-on-the-web` para as políticas
disponíveis. Alternativa equivalente: sessão de Claude Code na máquina do time,
com rede aberta.

Com `WebFetch` liberado, a passada percorre `_meta/gaps.md` por ordem de
dependência, abre cada fonte, e `loc` passa de "seção nomeada" para
"p. X, tab. Y" — que é o que a convenção pede.

**Enquanto isso:** as notas permanecem em `draft`/`stub`, que é o estado
honesto. O acervo é utilizável; o que não se pode é declarar `reviewed` o que
não foi lido na fonte.

**Origem:** scorecard `2026-07/lote-02-rn.md` (padrão nº 1) e
`2026-07/lote-04-rn.md` (regra da transcrição).

---

## B2 · A nota de segurança exige revisor humano nominal

**Desde:** 2026-07-26
**Afeta:** `seguranca/nr-35-trabalho-em-altura.md` e toda nota futura com
`risco: seguranca`
**Origem:** scorecard `2026-07/lote-02-rn.md`, gate G4

O Protocolo 92 (S.6.4) determina que o gate de segurança nunca dispensa
revisão humana. Um scorecard emitido por IA não fecha esse gate, por melhor
que seja a nota.

**O que destrava:** revisão por pessoa qualificada, registrada no campo
`revisor_humano` do frontmatter e num scorecard assinado.

**Já implementado:** o `validate.py` passou a **reprovar** (não apenas avisar)
quando `risco: seguranca` e `status: reviewed` coexistem sem `revisor_humano`.
Antes, essa violação passava pelo CI em silêncio — era o único gate do
protocolo que o CI não protegia.
