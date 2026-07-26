# Bloqueios de qualidade

Artefatos que não conseguem atingir 92 por motivo **externo ao texto** — e que
por isso não devem consumir mais ciclos de correção até o bloqueio sair.
Registrar aqui é a alternativa honesta a afrouxar a régua (Protocolo 92, S.1).

---

## B1 · Nenhuma nota pode chegar a `reviewed` sem verificação de fonte

**Desde:** 2026-07-26
**Afeta:** todo o acervo (31 notas)
**Origem:** scorecard `2026-07/lote-02-rn.md`, padrão sistêmico nº 1

O item 4 da rubrica R-N (fonte oficial com localizador) reprovou 4 de 4 notas
revisadas. A correção exige abrir a documentação oficial de cada fabricante,
localizar página/tabela/seção e registrar em `loc`.

**Por que está bloqueado:** o ambiente onde as notas foram escritas não tem
acesso à rede (proxy retorna 403 para todos os hosts, incluindo `pro.sony`,
`bromptontech.com`, `docs.acescentral.com` e `gov.br`). Sem acesso às fontes
primárias, a conferência não pode ser feita — e afirmar que foi seria
exatamente o tipo de falsidade que este protocolo existe para impedir.

**O que destrava:** executar a fase de verificação num ambiente com acesso à
web (sessão do Claude Code na máquina do time, com rede), percorrendo as notas
por ordem de dependência (`_meta/gaps.md`) e preenchendo `loc` em cada fonte.

**Enquanto isso:** as notas permanecem em `draft`/`stub`, que é o estado
honesto. O acervo é utilizável — o que não se pode é declarar `reviewed` o que
não foi conferido.

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
