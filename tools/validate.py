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
# Achado do lote-teste: o CI ficou limpo com duas arestas semanticamente
# erradas. Regra de coerência de tipo — aresta X só aponta para tipo Y.
TIPO_ESPERADO = {
    "governed_by": {"orgao"},
    "implements_standard": {"norma", "padrao", "interface"},
    "made_by": {"marca", "ecossistema"},
    "has_native_mount": {"mount"},
    "accepts_mount": {"mount"},
    "uses_battery_mount": {"battery-mount"},
    "records_codec": {"codec"},
    "accepts_media": {"midia"},
    "paired_gamut": {"colorspace", "transfer-function"},
    "conforms_to_pipeline": {"pipeline-cor"},
    "reports_to": {"funcao"},
    "part_of_department": {"departamento"},
    "caused_by": {"conceito", "problema", "interface"},
}

# Padrão nº 14 do lote 04: o CI checava o tipo do ALVO e nunca o da ORIGEM.
# `governed_by` é definida no vocabulário como "norma -> órgão"; saía de nó
# `conceito` e de `pipeline-cor` sem ninguém reclamar. Aresta direcional tem
# domínio, não só contradomínio.
TIPO_DE_ORIGEM = {
    # Produto implementa norma (`implements_standard`); não é governado por
    # órgão. Conceito técnico com norma por trás (genlock -> SMPTE) entra.
    "governed_by": {"norma", "interface", "midia", "colorspace", "conceito",
                    "transfer-function", "certificacao", "pipeline-cor"},
    "caused_by": {"problema"},
    "resolved_by": {"problema"},
    "diagnosed_with": {"problema"},
    "reports_to": {"funcao"},
    "records_codec": {"camera", "switcher"},
    "has_native_mount": {"camera"},
    "template_for": {"documento"},
}

# Tipos cujas arestas fortes são de ENTRADA por desenho — grafo só de
# `see_also` neles é a forma correta, não defeito. O vocabulário não tem
# `publishes` nem `certifies`, e inventar uma para satisfazer a régua seria
# deixar a régua desenhar a ontologia.
# Justificativa em _meta/arestas-minimas.md, "Piso universal".
ISENTOS_DO_PISO = {"moc", "orgao", "certificacao"}

# Rótulos de host que não identificam organização — descartados ao contar
# fontes independentes (ver _meta/qa/rubrica-confianca.md).
RUIDO_DE_HOST = {
    "www", "pro", "docs", "doc", "support", "help", "partnerhelp", "forum",
    "blog", "shop", "store", "api", "m", "en", "us", "br", "uk", "eu",
    "com", "org", "net", "io", "co", "tv", "gov", "edu", "online", "info",
    "jp", "de", "cn", "fr", "es", "it", "nl", "au", "ca",
}
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
# 3a linha da rubrica de confianca: afirmacao numerica sem fonte forte -> baixa.
# Unidades do dominio do acervo; ver o limite declarado em rubrica-confianca.md.
NUMERO_COM_UNIDADE = re.compile(
    r"\d[\d.,]*\s*(?:A\b|V\b|W\b|kW\b|kVA\b|VA\b|mm²|mm2\b|Hz\b|kHz\b|"
    r"Mb/s|Mbps\b|Gb/s|fps\b|stops?\b|K\b|lux\b|lm\b|TB\b|GB\b|bits?\b|ms\b|m²)"
)
ORDEM_CONFIANCA = {"baixa": 0, "media": 1, "alta": 2}
MIN_CITACAO = 40               # uma frase, não um fragmento

# Padrão nº 13 do lote 04: lacuna declarada em prosa é invisível para a
# máquina, então a nota honesta em português fica com confiança MAIS ALTA que
# a mesma nota honesta em marcador. Incentivo invertido — estes padrões o
# desfazem, exigindo o `<!-- verificar -->` junto.
# Apertado depois de 2 falsos positivos em 3: "a conferir" e "para conferir"
# são conselho ao leitor sobre prática de set, não declaração de lacuna. Só
# entram padrões que falam do estado de EVIDÊNCIA DA PRÓPRIA NOTA.
LACUNA_EM_PROSA = re.compile(
    r"(precisa[m]? sair d[ao] |antes de virar\s+`?reviewed"
    r"|não (?:foi|foram|está|estão) conferid|não conferid[oa]s?\b"
    r"|(?:não|sem) (?:é |ser )?de teste controlado"
    r"|ainda não (?:verificad|confirmad|test)"
    r"|falta[m]? (?:confirmar|verificar) )",
    re.IGNORECASE,
)

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


def carregar_arestas_minimas():
    """Lê o conjunto mínimo de arestas por type de _meta/arestas-minimas.md.

    Devolve {type: {"obrigatorias": [...], "grupos": [[...], ...]}}.
    O arquivo é a fonte da verdade — mudar a regra é editar lá, não aqui.
    Formato lido:

        ### `camera`
        - obrigatorias: `made_by`, `records_codec`
        - uma de: `uses_battery_mount`, `powered_by`
    """
    caminho = RAIZ / "_meta" / "arestas-minimas.md"
    if not caminho.exists():
        return {}
    regras, atuais = {}, None
    for linha in caminho.read_text(encoding="utf-8").split("\n"):
        cab = re.match(r"^###\s+(.+)$", linha)
        if cab:
            # um cabeçalho pode reger mais de um type: "### `a` · `b`"
            nomes = re.findall(r"`([a-z-]+)`", cab.group(1))
            atuais = []
            for n in nomes:
                regras[n] = {"obrigatorias": [], "grupos": []}
                atuais.append(n)
            continue
        if not atuais or not linha.startswith("- "):
            continue
        rotulo, _, resto = linha[2:].partition(":")
        arestas = re.findall(r"`([a-z_]+)`", resto)
        if not arestas:
            continue
        chave = "obrigatorias" if rotulo.strip() == "obrigatorias" else \
                "grupos" if rotulo.strip() == "uma de" else None
        for n in atuais:
            if chave == "obrigatorias":
                regras[n]["obrigatorias"].extend(arestas)
            elif chave == "grupos":
                regras[n]["grupos"].append(arestas)
    # seções de prosa que não declaram regra nenhuma não viram tipo
    return {t: r for t, r in regras.items() if r["obrigatorias"] or r["grupos"]}


def organizacao(url):
    """Extrai o 'token de marca' de uma URL, para contar fontes independentes.

    Duas páginas do mesmo fabricante não se corroboram — repetem-se. Este é o
    piso mecânico da rubrica de confiança: `pro.sony` e `www.sony.com` viram
    ambos "sony". Limite conhecido e documentado: `nanlux.com` e
    `nanliteus.com` são a mesma empresa e contam como duas — o contador erra
    para o lado permissivo, e por isso o item 11 mantém parte de julgamento.
    """
    m = re.match(r"^https?://([^/]+)", url or "")
    if not m:
        return url or ""
    partes = [p for p in m.group(1).lower().split(".") if p not in RUIDO_DE_HOST]
    return partes[0] if partes else m.group(1).lower()


def tem_afirmacao_numerica(corpo):
    """A nota publica número com unidade, ou linha de tabela com número?

    Piso mecânico, com o limite declarado: acerta spec ("220 V", "10 mm²",
    "~11,9 A") e erra para o lado permissivo em prosa que só cita quantidade.
    Ignora datas ISO e números dentro de bloco de código, que são comando e
    não afirmação.
    """
    limpo = re.sub(r"```.*?```", "", corpo or "", flags=re.S)
    limpo = re.sub(r"\d{4}-\d{2}-\d{2}", "", limpo)
    return bool(NUMERO_COM_UNIDADE.search(limpo))


def confianca_esperada(fontes, tem_lacuna, tem_numero=False):
    """Aplica a tabela de _meta/qa/rubrica-confianca.md, LINHA A LINHA.

    Devolve o valor MAIS ALTO que as fontes sustentam. A nota pode declarar
    esse valor ou um mais conservador; declarar mais otimista é que reprova.

    A ordem das linhas É a regra: lê-se de cima para baixo e para na primeira
    que se aplica. O lote 04 achou a 4ª linha divergindo do script; o lote de
    elétrica achou a 3ª ainda divergindo, porque só a linha reportada tinha
    sido corrigida. Agora a função segue a tabela inteira, e `test_validate.py`
    tem um caso por linha para que as duas não voltem a separar.
    """
    tiers = {f.get("tier") for f in fontes if isinstance(f, dict)}
    orgs = {organizacao(f.get("url", "")) for f in fontes if isinstance(f, dict)}
    orgs.discard("")
    forte = bool(tiers & {"oficial", "lab"})
    sem_loc = any(f.get("tier") in ("oficial", "lab") and not f.get("loc")
                  for f in fontes if isinstance(f, dict))

    if tem_lacuna:                      # 1ª linha
        return "baixa"
    if tem_numero and not forte:        # 3ª linha
        return "baixa"
    if len(orgs) < 2:                   # 4ª linha
        return "baixa" if not forte else "media"
    if not forte:                       # 5ª linha
        return "media"
    if sem_loc:                         # 6ª linha
        return "media"
    return "alta"                       # 8ª linha


def checar_arestas_minimas(tipo, status, presentes, dispensas, regras, vocab):
    """Aplica o conjunto mínimo de arestas. Função pura — testável isolada.

    `presentes` é o conjunto de arestas declaradas em `rel` com pelo menos um
    alvo; `dispensas` é o dict `rel_na` (aresta -> motivo).

    Devolve lista de ("erro"|"aviso", mensagem). A regra do lote 03 vale aqui
    como no resto do CI: avisa em `draft`, reprova em `reviewed`.
    """
    saida = []
    nivel = "erro" if status == "reviewed" else "aviso"
    silencioso = status in ("", "stub")

    for aresta, motivo in sorted(dispensas.items()):
        if aresta not in vocab:
            saida.append(("erro", f"'rel_na' dispensa aresta fora do vocabulário: '{aresta}'"))
        elif aresta in presentes:
            saida.append(("erro", f"aresta '{aresta}' declarada em 'rel' e dispensada "
                                  f"em 'rel_na' ao mesmo tempo"))
        if not (isinstance(motivo, str) and motivo.strip()):
            saida.append(("erro", f"'rel_na: {aresta}' sem motivo — dispensa é afirmação "
                                  f"sobre o mundo, não botão de silenciar o CI"))

    if silencioso:
        return saida

    # piso universal: pelo menos uma aresta com semântica.
    # `moc` e `orgao` são isentos por semântica do tipo, não por concessão —
    # ver _meta/arestas-minimas.md. Um mapa afirma vizinhança; um órgão recebe
    # suas arestas de fora.
    if tipo not in ISENTOS_DO_PISO:
        if not presentes:
            saida.append((nivel, "nota sem nenhuma aresta — o acervo é o grafo"))
        elif not presentes - {"see_also"}:
            saida.append((nivel, "grafo sem semântica: todas as arestas são 'see_also' "
                                 "(ver _meta/arestas-minimas.md, piso universal)"))

    regra = regras.get(tipo)
    if regra:
        resolvidas = presentes | set(dispensas)
        ausentes = [a for a in regra["obrigatorias"] if a not in resolvidas]
        if ausentes:
            saida.append((nivel, f"type '{tipo}' exige aresta(s) {', '.join(ausentes)} "
                                 f"— declarar, ou dispensar com motivo em 'rel_na'"))
        for grupo in regra["grupos"]:
            if not set(grupo) & resolvidas:
                saida.append((nivel, f"type '{tipo}' exige ao menos uma de "
                                     f"{', '.join(grupo)}"))
    return saida


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
    minimas = carregar_arestas_minimas()
    registro, tipos, arestas_totais = {}, {}, 0
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
                tipos[ident] = dados.get("type", "")

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
                # Regra da transcrição (conventions.md): fonte forte carrega o
                # trecho NAS PALAVRAS DA FONTE. 8 de 9 reprovações de G1 em
                # dois lotes foram má transcrição — e não dá para transcrever
                # literalmente sem abrir a fonte. O campo é a prova de leitura.
                if t in ("oficial", "lab"):
                    cit = (f.get("cit") or "").strip()
                    loc = (f.get("loc") or "").strip()
                    if not cit:
                        msg = (f"fonte {t} sem 'cit' — transcrever o trecho que "
                               f"sustenta a afirmação, nas palavras da fonte: {url}")
                        (erro if status == "reviewed" else aviso)(rel, msg)
                    elif len(cit) < MIN_CITACAO:
                        aviso(rel, f"'cit' curta demais ({len(cit)} caracteres) — "
                                   f"transcrever a frase, não um fragmento: {url}")
                    elif loc and cit.lower() == loc.lower():
                        erro(rel, f"'cit' idêntica a 'loc' — 'loc' diz ONDE, "
                                  f"'cit' diz O QUÊ: {url}")
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

        # Lacuna declarada em prosa precisa do marcador junto — senão a
        # honestidade em português vale mais confiança que a mesma honestidade
        # em `<!-- verificar -->` (padrão nº 13 do lote 04).
        if not pendencias and status != "stub":
            achado = LACUNA_EM_PROSA.search(corpo)
            if achado:
                msg = (f"lacuna declarada em prosa (\"{achado.group(0)}\") sem "
                       f"'<!-- verificar -->' — o marcador é o que a máquina lê")
                (erro if status == "reviewed" else aviso)(rel, msg)

        # Piso mecânico da rubrica de confiança (_meta/qa/rubrica-confianca.md).
        # Declarar mais conservador que a tabela é permitido e honesto; mais
        # otimista, não. O que a máquina NÃO confere está escrito na rubrica:
        # se as fontes de fato dizem a mesma coisa é julgamento do revisor.
        if conf and status != "stub":
            teto = confianca_esperada(fontes, pendencias > 0,
                                      tem_afirmacao_numerica(corpo))
            if ORDEM_CONFIANCA[conf] > ORDEM_CONFIANCA[teto]:
                msg = (f"confidence '{conf}' acima do que as fontes sustentam "
                       f"('{teto}') — ver _meta/qa/rubrica-confianca.md")
                (erro if status == "reviewed" else aviso)(rel, msg)
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
        dados["_corpo"] = corpo
        caminho_dados[rel] = dados

    # -------- passo 2: arestas (precisa do registro completo) --------
    for rel, dados in caminho_dados.items():
        # Wikilink de corpo apontando para o vazio. O docstring deste script
        # prometia "link não quebrado" e cobria só alvos de `rel:` — uma nota
        # passava com 0 erros e 0 avisos carregando [[hmi]] morto no texto.
        # Achado do lote de elétrica, defeito de régua nº 1.
        for alvo in set(WIKILINK.findall(dados.get("_corpo", ""))):
            alvo = alvo.split("|")[0].split("#")[0].strip()
            if not alvo or alvo in registro:
                continue
            if dados.get("status") == "reviewed":
                erro(rel, f"wikilink de corpo aponta para slug inexistente: [[{alvo}]]")
            else:
                aviso(rel, f"wikilink de corpo aponta para slug inexistente: [[{alvo}]]")
                lacunas.setdefault(alvo, []).append(rel)

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

        # ---- conjunto mínimo de arestas por type (_meta/arestas-minimas.md) ----
        # Item 3 da R-N ("arestas completas e específicas para o tipo de nó")
        # era julgamento do revisor e reprovava 100% das notas sem que o
        # produtor pudesse conferir antes. Aqui vira check determinístico.
        dispensas = dados.get("rel_na") or {}
        if not isinstance(dispensas, dict):
            erro(rel, "bloco 'rel_na' malformado — esperado 'aresta: motivo'")
            dispensas = {}
        for nivel, msg in checar_arestas_minimas(
            dados.get("type", ""),
            dados.get("status", ""),
            {a for a, v in relacoes.items() if fm.alvos(v)},
            dispensas,
            minimas,
            vocab,
        ):
            (erro if nivel == "erro" else aviso)(rel, msg)

        for aresta, valor in relacoes.items():
            if aresta not in vocab:
                erro(rel, f"aresta fora do vocabulário fechado: '{aresta}'")
                continue
            # Aresta declarada sem alvo (`template_for: []`) é TODO esquecido:
            # parece grafo para quem lê o frontmatter e não é nada para o grep.
            if not fm.alvos(valor):
                aviso(rel, f"aresta '{aresta}' declarada sem alvo — "
                           f"preencher ou remover")
            origem_ok = TIPO_DE_ORIGEM.get(aresta)
            tipo_origem = dados.get("type", "")
            if origem_ok and tipo_origem and tipo_origem not in origem_ok:
                msg = (f"aresta '{aresta}' saindo de type '{tipo_origem}' "
                       f"(esperado: {'/'.join(sorted(origem_ok))}) — "
                       f"ver _meta/edge-vocabulary.md")
                (erro if dados.get("status") == "reviewed" else aviso)(rel, msg)

            for alvo in fm.alvos(valor):
                arestas_totais += 1
                esperado = TIPO_ESPERADO.get(aresta)
                if esperado and alvo in registro:
                    tipo_alvo = tipos.get(alvo, "")
                    if tipo_alvo and tipo_alvo not in esperado:
                        erro(rel, f"aresta '{aresta}' aponta para type '{tipo_alvo}' "
                                  f"(esperado: {'/'.join(sorted(esperado))}) — alvo '{alvo}'")
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
