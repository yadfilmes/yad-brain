#!/usr/bin/env python3
"""
Executa a parte mecânica do conjunto-ouro: a RECUPERAÇÃO.

    python3 tools/eval.py              # roda tudo
    python3 tools/eval.py --cat lookup # só uma categoria
    python3 tools/eval.py -v           # mostra cada pergunta

Para cada pergunta de `_meta/eval/perguntas.md`, executa a busca documentada
no AGENTS.md e verifica se ela encontra os arquivos que o gabarito espera.

O que ESTE script mede: a recuperação acerta o alvo?
O que ele NÃO mede: a resposta está factualmente correta, cita fonte e tier,
respeita escopo e se abstém quando deve. Isso exige leitura (humana ou de
agente) contra a rubrica R-R do Protocolo 92 — o script não substitui isso.

Armadilhas de abstenção (gabarito `espera:` vazio) passam quando a busca
NÃO encontra nada: é a prova de que o acervo realmente não cobre o assunto,
e portanto que abster-se é a resposta correta.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PERGUNTAS = RAIZ / "_meta" / "eval" / "perguntas.md"


def carregar():
    """Lê as perguntas do markdown — uma fonte de verdade, legível por humano."""
    if not PERGUNTAS.exists():
        print(f"FATAL: {PERGUNTAS.relative_to(RAIZ)} não encontrado")
        sys.exit(1)
    itens, atual = [], None
    for linha in PERGUNTAS.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^### (Q\d+) · (\w+) · (.+)$", linha.strip())
        if m:
            if atual:
                itens.append(atual)
            atual = {"id": m.group(1), "cat": m.group(2), "q": m.group(3),
                     "espera": [], "busca": "", "fatos": []}
            continue
        if atual is None:
            continue
        m = re.match(r"^- (espera|busca|fatos|prior|avalia):\s*(.*)$", linha.strip())
        if m:
            campo, valor = m.group(1), m.group(2).strip()
            if campo == "busca":
                atual["busca"] = valor
            elif campo == "avalia":
                atual["avalia"] = valor
            elif campo in ("espera", "fatos"):
                atual[campo] = [x.strip() for x in valor.split(",") if x.strip()]
    if atual:
        itens.append(atual)
    return itens


def executar_busca(busca):
    """Roda a busca documentada e devolve os caminhos encontrados.

    Aceita vários passos separados por ' -> ', porque travessia de grafo é
    multi-passo por definição: um grep acha o ponto de partida, o passo
    seguinte segue a aresta. Modelar isso como busca única foi o erro da
    primeira versão deste avaliador — e o próprio benchmark o revelou.
    """
    if not busca:
        return []
    achados = []
    for passo in busca.split("->"):
        achados.extend(_um_passo(passo.strip()))
    return sorted(set(achados))


def _um_passo(busca):
    tipo, _, alvo = busca.partition(":")
    try:
        if tipo == "glob":
            # sem filtro de extensão: calculadora é .py e também é alvo legítimo
            achados = [p.relative_to(RAIZ).as_posix()
                       for p in RAIZ.rglob(f"*{alvo}*")
                       if p.is_file() and ".git" not in p.as_posix()
                       and "_meta/history" not in p.as_posix()
                       and "__pycache__" not in p.as_posix()]
            return sorted(achados)
        if tipo == "grep":
            r = subprocess.run(["grep", "-rl", "--include=*.md", "-E", alvo, "."],
                               cwd=RAIZ, capture_output=True, text=True, timeout=30)
            return sorted(x[2:] if x.startswith("./") else x
                          for x in r.stdout.split("\n") if x.strip()
                          and "_meta/history" not in x)
        if tipo == "indice":
            return [alvo] if (RAIZ / alvo).exists() else []
    except Exception as e:                      # noqa: BLE001
        print(f"    (erro na busca '{busca}': {e})")
    return []


def main():
    ap = argparse.ArgumentParser(description="Avalia a recuperação do acervo")
    ap.add_argument("--cat", help="filtrar por categoria")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    itens = carregar()
    if a.cat:
        itens = [i for i in itens if i["cat"] == a.cat]
    if not itens:
        print("nenhuma pergunta selecionada")
        return 1

    por_cat, falhas, julgamento = {}, [], []
    for it in itens:
        achados = executar_busca(it["busca"])
        esperados = it["espera"]

        # Abstenção de CONTEÚDO: o arquivo existe e é o certo, mas não cobre o
        # fato perguntado. A recuperação acerta; quem precisa se abster é a
        # resposta. Nenhuma checagem mecânica decide isso — declarar em vez de
        # fingir um veredito.
        if it.get("avalia") == "julgamento":
            julgamento.append(it)
            continue

        if not esperados:
            # armadilha de abstenção: passa se a busca não achou nada
            ok = len(achados) == 0
            detalhe = "nada encontrado (correto)" if ok else f"achou {achados[:3]}"
        else:
            faltando = [e for e in esperados if e not in achados]
            ok = not faltando
            detalhe = "todos encontrados" if ok else f"não achou: {faltando}"

        c = por_cat.setdefault(it["cat"], [0, 0])
        c[1] += 1
        if ok:
            c[0] += 1
        else:
            falhas.append((it, detalhe, achados))

        if a.verbose:
            print(f"  {'OK  ' if ok else 'FALHA'} {it['id']} [{it['cat']}] {it['q'][:58]}")
            if not ok:
                print(f"        {detalhe}")

    total_ok = sum(v[0] for v in por_cat.values())
    total = sum(v[1] for v in por_cat.values())

    print(f"\nRECUPERAÇÃO: {total_ok}/{total} ({100 * total_ok // total}%)\n")
    print(f"  {'categoria':<14} {'ok':>4} {'de':>4}")
    print("  " + "-" * 24)
    for cat in sorted(por_cat):
        ok, n = por_cat[cat]
        marca = "" if ok == n else "  <-"
        print(f"  {cat:<14} {ok:>4} {n:>4}{marca}")

    if julgamento:
        print(f"\nEXIGEM JULGAMENTO ({len(julgamento)}) — fora do alcance mecânico:\n")
        for it in julgamento:
            print(f"  {it['id']} [{it['cat']}] {it['q']}")
        print()

    if falhas:
        print(f"\nFALHAS ({len(falhas)}) — viram backlog de MOC, alias ou índice:\n")
        for it, detalhe, achados in falhas:
            print(f"  {it['id']} [{it['cat']}] {it['q']}")
            print(f"       busca: {it['busca']}")
            print(f"       {detalhe}\n")

    print("Lembrete: isto mede recuperação, não correção factual nem abstenção")
    print("na resposta. Essa parte exige a rubrica R-R do Protocolo 92.\n")
    return 0 if not falhas else 1


if __name__ == "__main__":
    sys.exit(main())
