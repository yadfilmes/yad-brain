#!/usr/bin/env python3
"""
Valida o acervo. Roda no CI e antes de qualquer commit.

    python3 tools/validate.py

O que verifica (tudo derivado de _meta/conventions.md e edge-vocabulary.md):
  - frontmatter parseável e campos obrigatórios
  - id == nome do arquivo, ASCII kebab-case, único no acervo
  - arestas dentro do vocabulário fechado
  - alvo de aresta existente (link não quebrado)
  - fonte obrigatória quando status != stub
  - TL;DR presente no corpo
  - tamanho da nota dentro da faixa
  - notas de risco: fonte oficial + disclaimer + revisão humana

Sai com código 1 se houver erro. Avisos não bloqueiam.
Caminhos são sempre relativos à raiz do repositório.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import frontmatter as fm

RAIZ = Path(__file__).resolve().parent.parent
IGNORAR = {"_meta/templates", "_graph", "_index", "_cofre"}
OBRIGATORIOS = ["id", "title", "type", "status"]
STATUS_VALIDOS = {"stub", "draft", "reviewed", "revisar"}
CONFIANCA_VALIDA = {"alta", "media", "baixa"}
ZONAS_VALIDAS = {"universal", "yad"}
TIERS_VALIDOS = {"oficial", "lab", "educacao", "comunidade", "campo-proprio"}
RAIZ_DE_DOMINIO = re.compile(r"^https?://[^/]+/?$")
SLUG = re.compile(r"^[a-z0-9]+(?:[-]{1,2}[a-z0-9]+)*$")
LIMITE_PALAVRAS = 900          # ~1.200 tokens
MIN_PALAVRAS = 40

erros, avisos = [], []


def erro(arq, msg):
    erros.append(f"  {arq}\n      ERRO  {msg}")


def aviso(arq, msg):
    avisos.append(f"  {arq}\n      aviso {msg}")


def carregar_vocabulario():
    """Lê as arestas permitidas de _meta/edge-vocabulary.md."""
    caminho = RAIZ / "_meta" / "edge-vocabulary.md"
    if not caminho.exists():
        print("FATAL: _meta/edge-vocabulary.md não encontrado")
        sys.exit(1)
    texto = caminho.read_text(encoding="utf-8")
    vocab = set()
    for linha in texto.split("\n"):
        if linha.startswith("- "):
            # uma linha pode declarar mais de uma aresta:
            #   - `successor_of` / `predecessor_of` — linhagem
            vocab.update(re.findall(r"`([a-z_]+)`", linha))
    return vocab


def notas():
    """Percorre só o que é nota do acervo.

    Regra: dentro de _meta/ apenas `vocab/` contém notas (os enums-como-nós).
    Todo o resto de _meta/ é documento de apoio ou artefato gerado — inclusive
    o gaps.md que este próprio script escreve, que não pode voltar como entrada.
    """
    for p in sorted(RAIZ.rglob("*.md")):
        rel = p.relative_to(RAIZ).as_posix()
        if rel.startswith("."):
            continue
        # nota nunca mora na raiz: lá ficam os documentos do projeto
        # (README.md, AGENTS.md, ...)
        if "/" not in rel:
            continue
        if any(rel.startswith(x) for x in IGNORAR):
            continue
        if rel.startswith("_meta/") and not rel.startswith("_meta/vocab/"):
            continue
        yield p, rel


def main():
    vocab = carregar_vocabulario()
    registro, arestas_totais = {}, 0
    lista = list(notas())

    # -------- passo 1: parse e checagens locais --------
    for caminho, rel in lista:
        texto = caminho.read_text(encoding="utf-8")
        bruto, corpo = fm.split(texto)

        if bruto is None:
            erro(rel, "sem frontmatter YAML no topo")
            continue

        dados = fm.parse(bruto)

        for campo in OBRIGATORIOS:
            if not dados.get(campo):
                erro(rel, f"campo obrigatório ausente: {campo}")

        ident = dados.get("id", "")
        if ident:
            esperado = caminho.stem
            if ident != esperado:
                erro(rel, f"id '{ident}' difere do nome do arquivo '{esperado}'")
            if not SLUG.match(ident):
                erro(rel, f"id '{ident}' fora do padrão ASCII kebab-case")
            if ident in registro:
                erro(rel, f"id duplicado — já usado em {registro[ident]}")
            else:
                registro[ident] = rel

        status = dados.get("status", "")
        if status and status not in STATUS_VALIDOS:
            erro(rel, f"status inválido: '{status}'")

        conf = dados.get("confidence", "")
        if conf and conf not in CONFIANCA_VALIDA:
            erro(rel, f"confidence inválida: '{conf}'")

        zona = dados.get("zona", "")
        if zona and zona not in ZONAS_VALIDAS:
            erro(rel, f"zona inválida: '{zona}'")
        if not zona:
            aviso(rel, "sem campo 'zona' (universal | yad)")

        # fontes
        fontes = dados.get("sources") or []
        if status and status != "stub" and not fontes:
            erro(rel, f"status '{status}' exige ao menos uma fonte")
        for f in fontes:
            if isinstance(f, dict):
                t = f.get("tier", "")
                if t and t not in TIERS_VALIDOS:
                    erro(rel, f"tier de fonte inválido: '{t}'")
                url = f.get("url", "")
                if not url:
                    aviso(rel, "fonte sem url")
                # Padrão sistêmico nº 1 do scorecard 2026-07/lote-02-rn:
                # o acervo citava DOMÍNIO em vez de EVIDÊNCIA. Uma URL que é
                # só host+/ aponta para o dono do conteúdo, não para o que
                # sustenta a afirmação.
                elif RAIZ_DE_DOMINIO.match(url):
                    if status == "reviewed":
                        erro(rel, f"fonte é raiz de domínio, não evidência: {url}")
                    else:
                        aviso(rel, f"fonte é raiz de domínio (precisa de página/seção): {url}")
                if t in ("oficial", "lab") and not f.get("loc"):
                    if status == "reviewed":
                        erro(rel, f"fonte {t} sem 'loc' (página/tabela/seção): {url}")
                    else:
                        aviso(rel, f"fonte {t} sem 'loc' — a evidência precisa de página/seção")

        # Alias acentuado precisa de par ASCII: o grep é byte a byte, e
        # alias que só existe acentuado é alias que ninguém encontra.
        import unicodedata
        def _ascii(s):
            return "".join(c for c in unicodedata.normalize("NFD", s)
                           if unicodedata.category(c) != "Mn")
        apelidos = dados.get("aliases") or []
        conjunto = {a.lower() for a in apelidos if isinstance(a, str)}
        for al in apelidos:
            if isinstance(al, str) and _ascii(al) != al and _ascii(al).lower() not in conjunto:
                aviso(rel, f"alias com acento sem par ASCII: '{al}' (grep é byte a byte)")

        # Padrão novo nº 7 do lote 03: prática de campo sustentada por fonte
        # oficial. Oficial sustenta número; prática pede comunidade ou
        # campo-proprio — AGENTS.md proíbe trocar um pelo outro.
        tiers_nota = {f.get("tier") for f in fontes if isinstance(f, dict)}
        tem_pratica = any(m in corpo for m in
                          ("## Gotchas", "Regra prática", "regra prática", "prática de campo"))
        if tem_pratica and not (tiers_nota - {"oficial"}):
            aviso(rel, "conteúdo de prática apoiado só em fonte 'oficial' — "
                       "prática pede lab, educacao, comunidade ou campo-proprio")

        # 'media' virou valor-padrão automático: 5/5 notas do lote 03 com
        # fonte única, sem loc e sem corroboração. Confiança é julgamento
        # sobre evidência, não campo a preencher.
        sem_loc = all(not f.get("loc") for f in fontes if isinstance(f, dict))
        if conf == "media" and len(fontes) <= 1 and sem_loc and status != "stub":
            aviso(rel, "confidence 'media' com fonte única sem 'loc' — "
                       "sem corroboração o valor honesto é 'baixa'")

        # corpo
        if "**TL;DR**" not in corpo:
            erro(rel, "corpo sem TL;DR na abertura")

        # Padrão sistêmico nº 4: frontmatter contradizendo o corpo.
        # Nota com lacuna declarada não pode alegar confiança alta.
        pendencias = corpo.count("<!-- verificar")
        if pendencias and conf == "alta":
            erro(rel, f"confidence 'alta' com {pendencias} pendência(s) <!-- verificar --> no corpo")
        if pendencias and status == "reviewed":
            erro(rel, f"status 'reviewed' com {pendencias} pendência(s) <!-- verificar --> no corpo")
        palavras = len(corpo.split())
        if palavras > LIMITE_PALAVRAS:
            aviso(rel, f"nota longa ({palavras} palavras) — considerar dividir")
        if palavras < MIN_PALAVRAS:
            aviso(rel, f"nota muito curta ({palavras} palavras)")

        # risco: segurança
        if dados.get("risco") == "seguranca":
            tiers = {f.get("tier") for f in fontes if isinstance(f, dict)}
            if "oficial" not in tiers:
                erro(rel, "nota de segurança exige fonte tier 'oficial'")
            # o disclaimer pode estar quebrado em várias linhas, com marcas de
            # citação e negrito no meio — normalizar antes de procurar
            plano = re.sub(r"[>*_`\s]+", " ", corpo)
            if "não substitui" not in plano and "nao substitui" not in plano:
                erro(rel, "nota de segurança sem disclaimer obrigatório")
            if not dados.get("jurisdicao"):
                erro(rel, "nota de segurança sem 'jurisdicao'")
            # Gate G4 do Protocolo 92 (S.6.4): segurança nunca dispensa humano.
            # Era o único gate que o CI deixava passar em silêncio — scorecard
            # emitido por IA não fecha este gate, por melhor que seja a nota.
            if status == "reviewed" and not dados.get("revisor_humano"):
                erro(rel, "nota de segurança em 'reviewed' sem campo 'revisor_humano' "
                          "— revisão por IA não fecha o gate G4")

        dados["_rel_path"] = rel
        caminho_dados[rel] = dados

    # -------- passo 2: arestas (precisa do registro completo) --------
    for rel, dados in caminho_dados.items():
        relacoes = dados.get("rel") or {}
        if not isinstance(relacoes, dict):
            erro(rel, "bloco 'rel' malformado")
            continue
        # Padrão sistêmico nº 2: grafo raso. `see_also` era 61 de 120 arestas
        # do acervo — usado como atalho onde existia aresta específica.
        n_see_also = len(fm.alvos(relacoes.get("see_also", [])))
        n_total = sum(len(fm.alvos(v)) for v in relacoes.values())
        # Gatilho em 2, não em 4: com 4, uma nota 3/3 ou 1/1 see_also passava
        # em silêncio — foi assim que a regressão do lote 03 escapou.
        if n_total >= 2 and n_see_also / n_total > 0.5:
            aviso(rel, f"grafo raso: {n_see_also}/{n_total} arestas são 'see_also' "
                       f"— preferir aresta específica")

        for aresta, valor in relacoes.items():
            if aresta not in vocab:
                erro(rel, f"aresta fora do vocabulário fechado: '{aresta}'")
                continue
            for alvo in fm.alvos(valor):
                arestas_totais += 1
                if alvo not in registro:
                    # Referência a nota ainda não escrita é NORMAL num acervo em
                    # construção — é a fila de trabalho, não um defeito. Mas uma
                    # nota 'reviewed' não pode apontar para o vazio.
                    if dados.get("status") == "reviewed":
                        erro(rel, f"nota reviewed aponta para slug inexistente: '{alvo}' ({aresta})")
                    else:
                        lacunas.setdefault(alvo, []).append(rel)

    # -------- lacunas: a fila de trabalho --------
    if lacunas:
        destino = RAIZ / "_meta" / "gaps.md"
        linhas = [
            "# Lacunas do acervo",
            "",
            "Slugs referenciados por notas existentes que ainda não foram escritos.",
            "Gerado por `tools/validate.py` — **não editar à mão.**",
            "",
            "Isto não é erro: é a fila de trabalho, ordenada por quantas notas",
            "já dependem de cada uma. Uma nota `reviewed`, porém, não pode",
            "apontar para o vazio — aí vira erro de validação.",
            "",
            "| slug faltante | citado por | nº |",
            "|---|---|---:|",
        ]
        for slug, origens in sorted(lacunas.items(), key=lambda x: (-len(x[1]), x[0])):
            linhas.append(f"| `{slug}` | {', '.join(sorted(set(origens)))} | {len(origens)} |")
        linhas.append("")
        destino.write_text("\n".join(linhas), encoding="utf-8")

    # -------- relatório --------
    print(f"\nAcervo: {len(lista)} notas · {len(registro)} ids · {arestas_totais} arestas")
    print(f"Vocabulário: {len(vocab)} arestas permitidas")
    print(f"Lacunas: {len(lacunas)} slugs a escrever (ver _meta/gaps.md)\n")

    if erros:
        print(f"ERROS ({len(erros)})\n")
        print("\n".join(erros))
        print()
    if avisos:
        print(f"AVISOS ({len(avisos)})\n")
        print("\n".join(avisos))
        print()

    if erros:
        print(f"FALHOU — {len(erros)} erro(s), {len(avisos)} aviso(s)\n")
        return 1
    print(f"OK — 0 erros, {len(avisos)} aviso(s)\n")
    return 0


caminho_dados = {}
lacunas = {}

if __name__ == "__main__":
    sys.exit(main())
