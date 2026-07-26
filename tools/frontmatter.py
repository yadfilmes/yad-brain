"""
Parser mínimo de frontmatter YAML — subconjunto controlado, stdlib apenas.

Por que não usar PyYAML: o acervo precisa validar igual no SSD do time, num
container ou na máquina de qualquer pessoa, sem `pip install`. Em troca, o
frontmatter fica restrito ao subconjunto documentado em _meta/conventions.md:

    chave: valor
    chave: [item, item, "item com espaço"]
    chave: [{to: x, via: y}]
    rel:
      aresta: [alvo, alvo]
      aresta: [{to: alvo, nota: "texto"}]
    sources:
      - {url: "...", tier: oficial, ret: 2026-07-26}

Não suporta (de propósito): âncoras, multilinha, tipagem implícita.
Tudo volta como str, list ou dict de str.
"""

import re

__all__ = ["parse", "split"]


def split(text):
    """Separa (frontmatter_bruto, corpo). Retorna (None, texto) se não houver."""
    if not text.startswith("---"):
        return None, text
    fim = text.find("\n---", 3)
    if fim == -1:
        return None, text
    bruto = text[3:fim].strip("\n")
    corpo = text[fim + 4:].lstrip("\n")
    return bruto, corpo


def _tokens(s):
    """Divide por vírgula respeitando aspas e chaves aninhadas."""
    saida, atual, prof, aspas = [], "", 0, None
    for ch in s:
        if aspas:
            if ch == aspas:
                aspas = None
            atual += ch
        elif ch in "\"'":
            aspas = ch
            atual += ch
        elif ch in "{[":
            prof += 1
            atual += ch
        elif ch in "}]":
            prof -= 1
            atual += ch
        elif ch == "," and prof == 0:
            saida.append(atual.strip())
            atual = ""
        else:
            atual += ch
    if atual.strip():
        saida.append(atual.strip())
    return saida


def _limpa(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def _valor(v):
    """Converte um valor: escalar, lista ou dict."""
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        interno = v[1:-1].strip()
        if not interno:
            return []
        return [_valor(t) for t in _tokens(interno)]
    if v.startswith("{") and v.endswith("}"):
        d = {}
        for par in _tokens(v[1:-1]):
            if ":" in par:
                k, _, val = par.partition(":")
                d[k.strip()] = _limpa(val)
        return d
    return _limpa(v)


def parse(bruto):
    """Recebe o frontmatter bruto e devolve um dict."""
    dados, chave_pai = {}, None
    if not bruto:
        return dados

    for linha in bruto.split("\n"):
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue

        indentada = linha[0] in " \t"
        conteudo = linha.strip()

        # item de lista aninhada:  - {url: ..., tier: ...}
        if indentada and conteudo.startswith("- "):
            if chave_pai:
                # o bloco nasce como {} (não sabíamos se era dict ou lista);
                # ao encontrar o primeiro "- ", ele se resolve como lista
                if not isinstance(dados.get(chave_pai), list):
                    dados[chave_pai] = []
                dados[chave_pai].append(_valor(conteudo[2:]))
            continue

        if ":" not in conteudo:
            continue
        chave, _, valor = conteudo.partition(":")
        chave, valor = chave.strip(), valor.strip()

        if indentada:
            # par dentro de um bloco aninhado (ex.: rel:)
            if chave_pai:
                if not isinstance(dados.get(chave_pai), dict):
                    dados[chave_pai] = {}
                dados[chave_pai][chave] = _valor(valor) if valor else []
            continue

        if valor == "":
            chave_pai = chave
            dados[chave] = {}
        else:
            chave_pai = None
            dados[chave] = _valor(valor)

    # blocos que ficaram vazios viram lista (sources) ou dict (rel) conforme uso
    for k, v in list(dados.items()):
        if v == {} and k in ("sources", "aliases", "tags"):
            dados[k] = []
    return dados


def alvos(valor):
    """Normaliza o valor de uma aresta para a lista de slugs-alvo."""
    if isinstance(valor, str):
        return [valor] if valor else []
    if isinstance(valor, dict):
        return [valor["to"]] if "to" in valor else []
    if isinstance(valor, list):
        saida = []
        for item in valor:
            saida.extend(alvos(item))
        return saida
    return []
