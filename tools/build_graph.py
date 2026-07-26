#!/usr/bin/env python3
"""
Deriva grafo, índices e estatísticas do acervo.

    python3 tools/build_graph.py

Gera (tudo em território derivado — NUNCA editar à mão):
    _graph/graph.json      nós + arestas, para consulta e visualização
    _graph/stats.md        painel de progresso e qualidade
    _graph/orfaos.md       notas sem nenhuma conexão
    _index/backlinks.md    quem aponta para quem
    _index/por-tipo.md     índice por tipo de entidade
    _index/por-marca.md    índice por fabricante
    _index/specs.csv       projeção tabular para consulta numérica

Nada aqui é fonte de verdade: apague tudo e rode de novo que volta idêntico.
Caminhos sempre relativos à raiz do repositório.
"""

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import frontmatter as fm

RAIZ = Path(__file__).resolve().parent.parent
IGNORAR = ("_meta/templates", "_meta/qa", "_meta/history", "_graph", "_index", "_cofre")
SIMETRICAS = {"competes_with", "interoperates_with", "distinct_from"}
INVERSAS = {"successor_of": "predecessor_of", "predecessor_of": "successor_of"}


def notas():
    for p in sorted(RAIZ.rglob("*.md")):
        rel = p.relative_to(RAIZ).as_posix()
        if rel.startswith(".") or "/" not in rel:
            continue
        if any(rel.startswith(x) for x in IGNORAR):
            continue
        if rel.startswith("_meta/") and p.name in (
            "conventions.md", "edge-vocabulary.md", "ontology.md", "gaps.md"
        ):
            continue
        yield p, rel


def main():
    nos, arestas = {}, []
    for caminho, rel in notas():
        bruto, corpo = fm.split(caminho.read_text(encoding="utf-8"))
        if bruto is None:
            continue
        d = fm.parse(bruto)
        ident = d.get("id")
        if not ident:
            continue

        m = re.search(r"\*\*TL;DR\*\*\s*[—-]?\s*(.+?)(?:\n\n|\Z)", corpo, re.S)
        tldr = " ".join(m.group(1).split())[:220] if m else ""

        nos[ident] = {
            "id": ident,
            "title": d.get("title", ident),
            "type": d.get("type", ""),
            "brand": d.get("brand", ""),
            "zona": d.get("zona", ""),
            "status": d.get("status", ""),
            "confidence": d.get("confidence", ""),
            "risco": d.get("risco", ""),
            "updated": d.get("updated", ""),
            "path": rel,
            "tldr": tldr,
            "aliases": d.get("aliases") or [],
            "tags": d.get("tags") or [],
            "n_fontes": len(d.get("sources") or []),
            "tiers": sorted({f.get("tier", "") for f in (d.get("sources") or [])
                             if isinstance(f, dict)} - {""}),
        }

        for aresta, valor in (d.get("rel") or {}).items():
            for alvo in fm.alvos(valor):
                arestas.append({"de": ident, "aresta": aresta, "para": alvo,
                                "derivada": False})

    # arestas derivadas: simetria e inversas
    existentes = {(a["de"], a["aresta"], a["para"]) for a in arestas}
    for a in list(arestas):
        if a["para"] not in nos:
            continue
        if a["aresta"] in SIMETRICAS:
            chave = (a["para"], a["aresta"], a["de"])
            if chave not in existentes:
                arestas.append({"de": a["para"], "aresta": a["aresta"],
                                "para": a["de"], "derivada": True})
                existentes.add(chave)
        elif a["aresta"] in INVERSAS:
            inv = INVERSAS[a["aresta"]]
            chave = (a["para"], inv, a["de"])
            if chave not in existentes:
                arestas.append({"de": a["para"], "aresta": inv,
                                "para": a["de"], "derivada": True})
                existentes.add(chave)

    (RAIZ / "_graph").mkdir(exist_ok=True)
    (RAIZ / "_index").mkdir(exist_ok=True)

    # ---------- graph.json ----------
    (RAIZ / "_graph" / "graph.json").write_text(
        json.dumps({"nos": list(nos.values()), "arestas": arestas},
                   ensure_ascii=False, indent=1), encoding="utf-8")

    # ---------- backlinks ----------
    entrada = defaultdict(list)
    for a in arestas:
        if not a["derivada"]:
            entrada[a["para"]].append((a["de"], a["aresta"]))
    linhas = ["# Backlinks", "",
              "Quem aponta para quem. Gerado por `tools/build_graph.py` — não editar.",
              "", "| nota | citada por |", "|---|---|"]
    for alvo in sorted(entrada):
        origens = ", ".join(f"`{o}` ({e})" for o, e in sorted(entrada[alvo]))
        linhas.append(f"| `{alvo}` | {origens} |")
    (RAIZ / "_index" / "backlinks.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")

    # ---------- índices ----------
    def indice(nome, titulo, chave):
        grupos = defaultdict(list)
        for n in nos.values():
            v = n.get(chave) or "(sem)"
            grupos[v].append(n)
        out = [f"# {titulo}", "",
               "Gerado por `tools/build_graph.py` — não editar à mão.", ""]
        for g in sorted(grupos):
            out.append(f"## {g}")
            out.append("")
            for n in sorted(grupos[g], key=lambda x: x["id"]):
                out.append(f"- [[{n['id']}]] — {n['tldr'][:110]}")
            out.append("")
        (RAIZ / "_index" / nome).write_text("\n".join(out), encoding="utf-8")

    indice("por-tipo.md", "Índice por tipo", "type")
    indice("por-marca.md", "Índice por marca", "brand")

    # ---------- projeção tabular ----------
    with (RAIZ / "_index" / "specs.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "title", "type", "brand", "zona", "status",
                    "confidence", "risco", "updated", "n_fontes", "tiers", "path"])
        for n in sorted(nos.values(), key=lambda x: x["id"]):
            w.writerow([n["id"], n["title"], n["type"], n["brand"], n["zona"],
                        n["status"], n["confidence"], n["risco"], n["updated"],
                        n["n_fontes"], "|".join(n["tiers"]), n["path"]])

    # ---------- órfãos ----------
    conectados = {a["de"] for a in arestas} | {a["para"] for a in arestas}
    orfaos = sorted(set(nos) - conectados)
    (RAIZ / "_graph" / "orfaos.md").write_text(
        "# Notas órfãs\n\nSem nenhuma aresta de entrada ou saída — provável falha "
        "de integração ao grafo.\nGerado por `tools/build_graph.py`.\n\n" +
        ("\n".join(f"- `{o}`" for o in orfaos) if orfaos else "Nenhuma. ✓") + "\n",
        encoding="utf-8")

    # ---------- stats ----------
    por_status = defaultdict(int)
    por_tipo = defaultdict(int)
    com_oficial = 0
    for n in nos.values():
        por_status[n["status"] or "(sem)"] += 1
        por_tipo[n["type"] or "(sem)"] += 1
        if "oficial" in n["tiers"] or "lab" in n["tiers"]:
            com_oficial += 1
    total = len(nos) or 1
    reais = [a for a in arestas if not a["derivada"]]

    s = ["# Estatísticas do acervo", "",
         "Gerado por `tools/build_graph.py` — não editar à mão.", "",
         "## Números gerais", "",
         f"- Notas: **{len(nos)}**",
         f"- Arestas declaradas: **{len(reais)}** (+{len(arestas) - len(reais)} derivadas por simetria/inversa)",
         f"- Notas com fonte oficial ou de laboratório: **{com_oficial}/{len(nos)}** "
         f"({100 * com_oficial // total}%)",
         f"- Notas órfãs: **{len(orfaos)}**", "",
         "## Por status", "", "| status | notas |", "|---|---:|"]
    for k in sorted(por_status):
        s.append(f"| {k} | {por_status[k]} |")
    s += ["", "## Por tipo", "", "| tipo | notas |", "|---|---:|"]
    for k in sorted(por_tipo):
        s.append(f"| {k} | {por_tipo[k]} |")
    s += ["", "## Arestas mais usadas", "", "| aresta | nº |", "|---|---:|"]
    cont = defaultdict(int)
    for a in reais:
        cont[a["aresta"]] += 1
    for k, v in sorted(cont.items(), key=lambda x: (-x[1], x[0]))[:12]:
        s.append(f"| `{k}` | {v} |")
    s.append("")
    (RAIZ / "_graph" / "stats.md").write_text("\n".join(s), encoding="utf-8")

    print(f"grafo:   {len(nos)} nós · {len(reais)} arestas declaradas "
          f"· {len(arestas) - len(reais)} derivadas")
    print(f"órfãos:  {len(orfaos)}")
    print("gerados: _graph/graph.json, stats.md, orfaos.md")
    print("         _index/backlinks.md, por-tipo.md, por-marca.md, specs.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
