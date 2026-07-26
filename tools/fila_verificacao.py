#!/usr/bin/env python3
"""
Gera _meta/fila-verificacao.md — a fila de trabalho da passada R3.

    python3 tools/fila_verificacao.py

Lista toda fonte `oficial`/`lab` que ainda não tem `cit`, agrupada por
organização. Agrupar por organização e não por nota é deliberado: abrir o site
de um fabricante uma vez e resolver todas as fontes dele de uma vez custa muito
menos que pular entre domínios.

A fila encolhe sozinha conforme os `cit` são preenchidos — regenerar a qualquer
momento para ver o que falta.
"""

import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import frontmatter as fm
import validate as V

DESTINO = V.RAIZ / "_meta" / "fila-verificacao.md"

CABECALHO = """# Fila de verificação de fontes (R3)

Gerado por script — **não editar à mão.** Regenerar com:

```
python3 tools/fila_verificacao.py
```

{resumo}

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
"""


def coletar():
    itens = []
    for caminho, rel in V.notas():
        bruto, corpo = fm.split(caminho.read_text(encoding="utf-8"))
        if bruto is None:
            continue
        dados = fm.parse(bruto)
        if dados.get("status") == "stub":
            continue
        for f in dados.get("sources") or []:
            if not isinstance(f, dict):
                continue
            if f.get("tier") not in ("oficial", "lab") or f.get("cit"):
                continue
            itens.append({
                "nota": rel,
                "url": f.get("url", ""),
                "loc": f.get("loc", ""),
                "declara": f.get("nota", ""),
                "org": V.organizacao(f.get("url", "")),
                "risco": dados.get("risco", ""),
            })
    return itens


def main():
    itens = coletar()
    por_org = collections.defaultdict(list)
    for i in itens:
        por_org[i["org"]].append(i)

    resumo = (f"**{len(itens)} fontes** `oficial`/`lab` sem `cit`, em "
              f"**{len({i['nota'] for i in itens})} notas**, de "
              f"**{len(por_org)} organizações**.")
    linhas = [CABECALHO.format(resumo=resumo)]

    # segurança primeiro, depois volume decrescente
    def chave(par):
        org, lista = par
        tem_risco = any(i["risco"] == "seguranca" for i in lista)
        return (not tem_risco, -len(lista), org)

    for org, lista in sorted(por_org.items(), key=chave):
        risco = " · 🔴 contém nota de SEGURANÇA" if any(
            i["risco"] == "seguranca" for i in lista) else ""
        linhas.append(f"## `{org}` — {len(lista)} fonte(s){risco}\n")
        for i in sorted(lista, key=lambda x: x["nota"]):
            marca = " · 🔴 SEGURANÇA" if i["risco"] == "seguranca" else ""
            linhas.append(f"- [ ] **{i['nota']}**{marca}")
            linhas.append(f"  - {i['url']}")
            if i["loc"]:
                linhas.append(f"  - `loc` atual: {i['loc']}")
            if i["declara"]:
                linhas.append(f"  - a nota diz que daqui vem: {i['declara']}")
        linhas.append("")

    DESTINO.write_text("\n".join(linhas), encoding="utf-8")
    print(f"{len(itens)} fontes · {len({i['nota'] for i in itens})} notas · "
          f"{len(por_org)} organizações")
    print(f"gerado: {DESTINO.relative_to(V.RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
