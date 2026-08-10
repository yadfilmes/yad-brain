#!/usr/bin/env python3
"""
YAD PROPOSAL BUILD — content.json + dna/*.css + assets/ → três saídas.

    dist/proposta.html   arquivo único, tudo embutido, abre por duplo clique
    dist/index.html      versão com assets soltos, para publicar no link
    dist/proposta.pdf    impressão determinística (precisa de chromium)

Uso:  python3 build.py [--pdf]

Sem dependências obrigatórias. `fonttools` é opcional e só serve para
subsetar a fonte — sem ele, a fonte inteira é embutida e o arquivo
fica ~25 KB maior.
"""
import base64, json, mimetypes, re, shutil, subprocess, sys, unicodedata
from html import escape
from pathlib import Path

RAIZ = Path(__file__).parent
ASSETS, DIST = RAIZ / "assets", RAIZ / "dist"
mimetypes.add_type("image/avif", ".avif")


# ─────────────────────────────────────────────── helpers

PLACEHOLDER = (
    "data:image/svg+xml;base64," + base64.b64encode(
        b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 10">'
        b'<rect width="16" height="10" fill="#1b2128"/>'
        b'<text x="8" y="5.6" fill="#5c6a78" font-size="1.1" font-family="sans-serif"'
        b' text-anchor="middle">asset ausente</text></svg>').decode())


def datauri(nome: str) -> str:
    p = ASSETS / nome
    if not p.exists():
        print(f"  ! asset ausente: {nome}")
        return PLACEHOLDER
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def stag(i: int) -> str:
    """Índice de stagger. No scroll o atraso é deslocamento de range."""
    return f' style="--i:{i}"'


def split_letters(linhas, start=0):
    """SplitText em tempo de build: cada caractere vira um span com --i.
    Zero JavaScript no cliente, e funciona em file:// e no PDF."""
    out, i = [], start
    for linha in linhas:
        chars = "".join(
            f'<span class="ch" style="--i:{i + n}">{escape(c)}</span>'
            for n, c in enumerate(linha)
        )
        i += len(linha) + 2
        out.append(f'<span class="ln">{chars}</span>')
    return f'<span class="split" aria-hidden="true">{"".join(out)}</span>'


def sec(b, classes="", extra=""):
    tone = b.get("tone", "")
    brk = " break" if b.get("break") else ""
    cls = " ".join(x for x in ("section", tone, classes) if x) + brk
    return f'<section class="{cls}" id="{b["id"]}"{extra}>'


def head(b):
    h = f'<div class="kicker">{b["kicker"]}</div>' if b.get("kicker") else ""
    if b.get("title"):
        h += f'<h2>{b["title"]}</h2>'
    if b.get("lead"):
        h += f'<p class="lead">{b["lead"]}</p>'
    return f'<div data-reveal>{h}</div>' if h else ""


# ─────────────────────────────────────────────── blocos

def b_hero(b, ctx):
    m = "".join(f'<div><b>{x["k"]}</b><span>{x["v"]}</span></div>' for x in b["meta"])
    titulo_visivel = " ".join(b["title"])
    return f'''
<section class="hero" id="{b['id']}" aria-labelledby="hero-title">
  <img class="hero-bg" src="{ctx['src'](b['image'])}" alt="" aria-hidden="true">
  <div class="hero-grid">
    <div class="eyebrow">{b['eyebrow']}</div>
    <div class="badge"><strong>{b['badge']['label']}</strong><span>{b['badge']['text']}</span></div>
    <h1 id="hero-title"><span class="sr-only">{escape(titulo_visivel)}</span>{split_letters(b['title'])}</h1>
    <p class="hero-copy">{b['copy']}</p>
    <div class="hero-meta" aria-label="Resumo da proposta">{m}</div>
  </div>
</section>'''


def b_statement(b, ctx):
    itens = "".join(
        f'<article class="principle"{stag(i)}><span class="num">{x["num"]}</span>'
        f'<h3>{x["h"]}</h3><p>{x["p"]}</p></article>'
        for i, x in enumerate(b["items"]))
    return f'''{sec(b)}<div class="inner split-2">
  <div data-reveal><div class="kicker">{b['kicker']}</div><h2 class="statement">{b['statement']}</h2></div>
  <div class="stack" data-reveal="3d" data-stagger>{itens}</div>
</div></section>'''


def b_quote(b, ctx):
    return f'<div class="quote-band" id="{b["id"]}"><span>{b["text"]}</span></div>'


def b_cards(b, ctx):
    cls = "chapters" if b.get("cols") == 5 else f'grid-{b.get("cols", 3)}'
    modo = b.get("variant", "3d")
    itens = "".join(
        f'<article class="{"chapter" if b.get("cols")==5 else "card"}"'
        f' style="--i:{i};--fan:{(i - (len(b["items"])-1)/2) * 7:.1f}deg">'
        f'<span class="{"chapter-id" if b.get("cols")==5 else "label"}">{x["label"]}</span>'
        f'<h3>{x["h"]}</h3><p>{x["p"]}</p></article>'
        for i, x in enumerate(b["items"]))
    return f'''{sec(b)}<div class="inner">{head(b)}
  <div class="{cls}" data-reveal="{modo}" data-stagger>{itens}</div>
</div></section>'''


def b_deliverables(b, ctx):
    itens = "".join(
        f'<article class="deliverable"{stag(i)}><b>{x["label"]}</b>'
        f'<span class="big">{x["big"]}</span><p>{x["p"]}</p></article>'
        for i, x in enumerate(b["items"]))
    tot = "".join(f'<div><strong>{t["n"]}</strong><span>{t["l"]}</span></div>' for t in b["totals"])
    return f'''{sec(b)}<div class="inner">{head(b)}
  <div class="deliverables" data-reveal="3d" data-stagger>{itens}
    <div class="totals" aria-label="Totais da temporada">{tot}</div>
  </div>
</div></section>'''


def b_workflow(b, ctx):
    itens = "".join(
        f'<article class="flow-card"{stag(i)}><span class="tag">{x["label"]}</span><h3>{x["h"]}</h3>'
        f'<ul>{"".join(f"<li>{li}</li>" for li in x["list"])}</ul></article>'
        for i, x in enumerate(b["items"]))
    return f'''{sec(b)}<div class="inner">{head(b)}
  <div class="grid-2" data-reveal="3d" data-stagger>{itens}</div>
</div></section>'''


def b_timeline(b, ctx):
    hd = "".join(f'<span role="columnheader">{h}</span>' for h in b["head"])
    linhas = "".join(
        f'<div class="timeline-row" role="row"{stag(i)}>'
        f'<span class="stage-no" role="cell">{r["no"]}</span>'
        f'<span role="cell"><strong>{r["name"]}</strong>{r["where"]}</span>'
        f'<span class="shoot" role="cell">{r["shoot"]}</span>'
        f'<span class="delivery" role="cell">{r["delivery"]}</span></div>'
        for i, r in enumerate(b["rows"]))
    return f'''{sec(b)}<div class="inner">{head(b)}
  <div class="timeline" role="table" aria-label="Cronograma das etapas" data-stagger>
    <div class="timeline-row head" role="row">{hd}</div>{linhas}
  </div>
</div></section>'''


def b_roles(b, ctx):
    itens = "".join(
        f'<article class="role"{stag(i)}><b>{x["h"]}</b><span>{x["p"]}</span></article>'
        for i, x in enumerate(b["items"]))
    banda = f'<div class="band" data-reveal>{b["band"]}</div>' if b.get("band") else ""
    return f'''{sec(b)}<div class="inner">{head(b)}
  <div class="grid-{b.get("cols",3)}" data-reveal="3d" data-stagger>{itens}</div>{banda}
</div></section>'''


def b_steps(b, ctx):
    itens = "".join(
        f'<article class="step"{stag(i)}><small>{x["label"]}</small><h3>{x["h"]}</h3><p>{x["p"]}</p></article>'
        for i, x in enumerate(b["items"]))
    return f'''{sec(b)}<div class="inner">{head(b)}
  <div class="grid-{len(b["items"])}" data-reveal="3d" data-stagger>{itens}</div>
</div></section>'''


def b_urgency(b, ctx):
    itens = "".join(f'<div{stag(i)}><strong>{x["n"]}</strong><span>{x["l"]}</span></div>'
                    for i, x in enumerate(b["items"]))
    return f'''{sec(b)}<div class="inner urgent">
  <div data-reveal><div class="kicker">{b['kicker']}</div><h2>{b['title']}</h2><p class="lead">{b['lead']}</p></div>
  <div class="countdown" data-stagger>{itens}</div>
</div></section>'''


def b_investment(b, ctx):
    rows = "".join(
        f'<div class="breakdown-row"{stag(i)}><span>{x["l"]}</span><b>{x["v"]}</b></div>'
        for i, x in enumerate(b["breakdown"]))
    t = b["total"]
    rows += (f'<div class="breakdown-row total" style="--i:{len(b["breakdown"])}">'
             f'<span>{t["l"]}</span><b>{t["v"]}</b></div>')
    p = b["price"]
    return f'''{sec(b)}<div class="inner investment">
  <div data-reveal><div class="kicker">{b['kicker']}</div><h2>{b['title']}</h2><p class="lead">{b['lead']}</p>
    <div class="price"><small>{p['label']}</small><strong>{p['value']}</strong><span>{p['note']}</span></div>
  </div>
  <div class="breakdown" aria-label="Composição por etapa">{rows}</div>
</div></section>'''


def b_conditions(b, ctx):
    itens = "".join(
        f'<article class="condition{" wide" if x.get("wide") else ""}"{stag(i)}><h3>{x["h"]}</h3>'
        f'<ul>{"".join(f"<li>{li}</li>" for li in x["list"])}</ul></article>'
        for i, x in enumerate(b["items"]))
    nota = f'<p class="small" data-reveal style="margin-top:24px">{b["note"]}</p>' if b.get("note") else ""
    return f'''{sec(b)}<div class="inner">{head(b)}
  <div class="conditions" data-reveal="3d" data-stagger>{itens}</div>{nota}
</div></section>'''


def b_about(b, ctx):
    li = "".join(f"<li>{x}</li>" for x in b["list"])
    return f'''{sec(b)}<div class="inner about">
  <div class="brand-panel" data-reveal><img src="{ctx['src'](b['logo'])}" alt="Logo oficial YAD Filmes"></div>
  <div data-reveal><div class="kicker">{b['kicker']}</div><h2>{b['title']}</h2>
    <p class="lead">{b['lead']}</p><ul>{li}</ul></div>
</div></section>'''


def b_gallery(b, ctx):
    cards = "".join(
        f'<figure class="gallery-card"{stag(i)}><img src="{ctx["src"](x["src"])}" alt="{escape(x["alt"])}">'
        f'<figcaption><strong>{x["h"]}</strong><span>{x["p"]}</span></figcaption></figure>'
        for i, x in enumerate(b["items"]))
    return f'''{sec(b, "gallery")}<div class="inner">{head(b)}</div>
  <div class="deck-stage"><div class="deck-pin">
    <div class="gallery-grid inner" aria-label="Galeria institucional YAD Filmes">{cards}</div>
  </div></div>
</section>'''


def b_cta(b, ctx):
    acts = "".join(
        f'<a class="button{" primary" if a.get("primary") else ""}" href="{a["href"]}">{a["label"]}</a>'
        for a in b["actions"])
    return f'''{sec(b, "cta")}<div class="inner" data-reveal>
  <div class="kicker">{b['kicker']}</div><h2>{b['title']}</h2><p class="lead">{b['lead']}</p>
  <div class="cta-actions">{acts}</div>
</div></section>'''


BLOCOS = {
    "hero": b_hero, "statement": b_statement, "quote": b_quote, "cards": b_cards,
    "deliverables": b_deliverables, "workflow": b_workflow, "timeline": b_timeline,
    "roles": b_roles, "steps": b_steps, "urgency": b_urgency, "investment": b_investment,
    "conditions": b_conditions, "about": b_about, "gallery": b_gallery, "cta": b_cta,
}


# ─────────────────────────────────────────────── fonte

def fonte(texto: str, inline: bool) -> str:
    """Embute a fonte variável, subsetada para os caracteres realmente usados.
    Sem @font-face a proposta assume a fonte do sistema do cliente — e o
    tracking negativo do display, calibrado para a Inter, quebra."""
    origem = ASSETS / "inter-var.woff2"
    if not origem.exists():
        print("  ! inter-var.woff2 ausente — a tipografia vai depender da máquina do cliente")
        return ""
    arq = origem
    try:
        from fontTools import subset
        chars = sorted(set(texto) | set(" 0123456789.,:;·—–-…“”\"'()/%&+ªº°"))
        alvo = ASSETS / "inter-subset.woff2"
        opts = subset.Options()
        opts.flavor, opts.layout_features, opts.desubroutinize = "woff2", ["*"], False
        opts.drop_tables += ["DSIG"]
        f = subset.load_font(str(origem), opts)
        s = subset.Subsetter(options=opts)
        s.populate(unicodes=[ord(c) for c in chars if unicodedata.category(c) != "Cc"])
        s.subset(f)
        subset.save_font(f, str(alvo), opts)
        f.close()
        arq = alvo
        print(f"  fonte subsetada: {origem.stat().st_size/1024:.0f} KB → {alvo.stat().st_size/1024:.0f} KB "
              f"({len(chars)} caracteres)")
    except ImportError:
        print("  fonttools ausente — embutindo a fonte inteira")

    if inline:
        src = "data:font/woff2;base64," + base64.b64encode(arq.read_bytes()).decode()
    else:
        shutil.copy(arq, DIST / "assets" / arq.name)
        src = f"assets/{arq.name}"
    return (f'@font-face{{font-family:"Inter Variable";font-style:normal;font-weight:100 900;'
            f'font-display:swap;src:url("{src}") format("woff2");}}\n')


# ─────────────────────────────────────────────── montagem

def montar(dados, css_sys, inline: bool) -> str:
    meta = dados["meta"]
    if inline:
        ctx = {"src": datauri}
    else:
        (DIST / "assets").mkdir(parents=True, exist_ok=True)

        def copiar(nome):
            if not (ASSETS / nome).exists():
                print(f"  ! asset ausente: {nome}")
                return PLACEHOLDER
            shutil.copy(ASSETS / nome, DIST / "assets" / nome)
            return f"assets/{nome}"
        ctx = {"src": copiar}

    corpo = "".join(BLOCOS[b["type"]](b, ctx) for b in dados["composition"])
    texto = re.sub(r"<[^>]+>", " ", corpo) + meta["title"] + meta["footer"]["text"]

    css_dna = (RAIZ / "dna" / f'{meta["dna"]}.css').read_text(encoding="utf-8")
    css = fonte(texto, inline) + css_dna + css_sys
    css += '\n.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}\n'

    nav = "".join(f'<a href="{n["href"]}">{n["label"]}</a>' for n in meta["nav"])
    f = meta["footer"]
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark light">
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="referrer" content="no-referrer">
<meta name="description" content="{escape(meta['description'])}">
<title>{escape(meta['title'])}</title>
<style>{css}</style>
</head>
<body>
<a class="skip" href="#{dados['composition'][1]['id']}">Ir ao conteúdo</a>
<header class="topbar">
  <div class="marks">
    <img class="brand-client" src="{ctx['src'](meta['brandClient'])}" alt="{escape(meta['client'])}">
    <span class="slash" aria-hidden="true"></span>
    <img class="brand-yad" src="{ctx['src'](meta['brandYad'])}" alt="YAD Filmes">
  </div>
  <span class="top-status">{meta['status']}</span>
  <nav aria-label="Navegação da proposta">{nav}</nav>
</header>
<main>{corpo}</main>
<footer><div class="footer-inner">
  <div class="footer-brand"><img class="footer-logo" src="{ctx['src'](f['logo'])}" alt="YAD Filmes"><span>{f['contact']}</span></div>
  <div class="footer-copy"><strong>{f['title']}</strong>{f['text']}</div>
</div></footer>
</body>
</html>'''


def gerar_pdf(origem: Path, destino: Path) -> bool:
    for exe in ("chromium", "chromium-browser", "google-chrome", "chrome",
                "/opt/pw-browsers/chromium", "/root/.cache/ms-playwright/chromium/chrome-linux/chrome"):
        cam = shutil.which(exe) or (exe if Path(exe).exists() else None)
        if not cam:
            continue
        r = subprocess.run([cam, "--headless", "--disable-gpu", "--no-sandbox",
                            "--virtual-time-budget=9000", "--run-all-compositor-stages-before-draw",
                            f"--print-to-pdf={destino}", "--no-pdf-header-footer",
                            origem.resolve().as_uri()],
                           capture_output=True, timeout=180)
        if destino.exists() and destino.stat().st_size > 0:
            return True
        print("  chromium falhou:", r.stderr.decode()[-300:])
    return False


def comprimir_pdf(caminho: Path, qualidade: int = 76) -> None:
    """O Chromium reembute as fotos sem perdas — um PDF de 18 páginas passa
    de 10 MB. Aqui as imagens grandes voltam a ser JPEG. Logos com canal alfa
    ficam intocados, senão a transparência vira retângulo preto."""
    try:
        import io, pikepdf
        from PIL import Image
    except ImportError:
        return
    antes = caminho.stat().st_size
    pdf = pikepdf.open(caminho, allow_overwriting_input=True)
    trocadas = 0
    for pagina in pdf.pages:
        imagens = pagina.get_images() if hasattr(pagina, "get_images") else pagina.images
        for nome, obj in list(imagens.items()):
            try:
                if "/SMask" in obj or "/Mask" in obj:
                    continue
                img = pikepdf.PdfImage(obj).as_pil_image()
                if img.width * img.height < 90_000:
                    continue
                buf = io.BytesIO()
                img.convert("RGB").save(buf, "JPEG", quality=qualidade, optimize=True,
                                        progressive=True, subsampling=1)
                if buf.tell() >= len(obj.read_raw_bytes()):
                    continue
                novo = pdf.make_stream(buf.getvalue())
                novo.stream_dict = pikepdf.Dictionary(
                    Type=pikepdf.Name("/XObject"), Subtype=pikepdf.Name("/Image"),
                    Width=img.width, Height=img.height, BitsPerComponent=8,
                    ColorSpace=pikepdf.Name("/DeviceRGB"), Filter=pikepdf.Name("/DCTDecode"))
                pagina.Resources.XObject[nome] = novo
                trocadas += 1
            except Exception:
                continue
    pdf.save(caminho, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)
    pdf.close()
    print(f"  {trocadas} imagens recomprimidas: {antes/1e6:.2f} MB → {caminho.stat().st_size/1e6:.2f} MB")


def main():
    DIST.mkdir(exist_ok=True)
    dados = json.loads((RAIZ / "content.json").read_text(encoding="utf-8"))
    css_sys = (RAIZ / "src" / "system.css").read_text(encoding="utf-8")

    print("\n▸ arquivo único (offline, encaminhável)")
    unico = DIST / "proposta.html"
    unico.write_text(montar(dados, css_sys, inline=True), encoding="utf-8")
    print(f"  {unico.name}: {unico.stat().st_size/1e6:.2f} MB")

    print("▸ versão de link (assets soltos)")
    link = DIST / "index.html"
    link.write_text(montar(dados, css_sys, inline=False), encoding="utf-8")
    tot = sum(p.stat().st_size for p in (DIST / "assets").rglob("*")) + link.stat().st_size
    print(f"  {link.name}: {link.stat().st_size/1024:.0f} KB + assets = {tot/1e6:.2f} MB")

    if "--pdf" in sys.argv:
        print("▸ PDF determinístico")
        pdf = DIST / "proposta.pdf"
        if gerar_pdf(unico, pdf):
            comprimir_pdf(pdf)
            print(f"  {pdf.name}: {pdf.stat().st_size/1e6:.2f} MB")
        else:
            print("  chromium indisponível — rode com o Chrome instalado")

    print("▸ pacote para encaminhar")
    zipe = DIST / "proposta-bundle.zip"
    import zipfile
    with zipfile.ZipFile(zipe, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.write(unico, "proposta.html")
        if (DIST / "proposta.pdf").exists():
            z.write(DIST / "proposta.pdf", "proposta.pdf")
    print(f"  {zipe.name}: {zipe.stat().st_size/1e6:.2f} MB")


if __name__ == "__main__":
    main()
