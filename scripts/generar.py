#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las fichas de portátil, el catálogo pre-renderizado y el sitemap.

La fuente de datos es el array LAPTOPS de index.html. A partir de él se crea:

  portatil/<slug>.html   → una ficha estática por modelo
  index.html             → tarjetas del catálogo en HTML (bloques entre marcadores)
  sitemap.xml            → todas las URLs
  scripts/og-manifest.json → datos para que scripts/og.ps1 genere las imágenes sociales

Uso:
    python scripts/generar.py

Después de cambiar precios o modelos en index.html, vuelve a ejecutarlo.
"""

from __future__ import annotations

import html
import json
import math
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://raulft721.github.io/portatiles/"
INDEX = ROOT / "index.html"
FICHAS_DIR = ROOT / "portatil"
OG_DIR = ROOT / "img" / "og"
MANIFEST = ROOT / "scripts" / "og-manifest.json"

CATS = (("estudio", "Estudiar"), ("trabajo", "Trabajar"),
        ("gaming", "Jugar"), ("movilidad", "Moverse"))

VERB = {"estudio": "estudiar", "trabajo": "trabajar",
        "gaming": "jugar", "movilidad": "moverse"}

USE = {"estudio": "estudiar y tomar apuntes",
       "trabajo": "trabajar todo el día",
       "gaming": "jugar con soltura",
       "movilidad": "llevarlo encima a diario"}

SIN = {"estudio": "el uso académico", "trabajo": "el trabajo intensivo",
       "gaming": "el gaming", "movilidad": "la portabilidad"}

MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre")


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------

def esc(text, quote=False):
    return html.escape(str(text), quote=quote)


def slugify(name):
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("+", " plus ")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def js_round(x):
    """Math.round de JavaScript (0,5 hacia arriba)."""
    return math.floor(x + 0.5)


def eur(n):
    return f"{n} €"


def kg(n):
    if n is None:
        return "sin dato"
    return f"{n:.2f}".replace(".", ",") + " kg"


def horas(l):
    """Autonomía declarada, con la capacidad si el fabricante no da horas."""
    if l.get("battery") is None:
        return ("Sin dato del fabricante"
                + (f" (batería de {str(l['wh']).replace('.', ',')} Wh)" if l.get("wh") else ""))
    return f"{l['battery']} h según el fabricante"


def overall(laptop):
    """Nota con el perfil equilibrado (25 % por apartado), igual que en la web."""
    return js_round(sum(laptop["scores"].values()) * 0.25)


def fecha_larga(d):
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def parse_laptops(source):
    start = source.index("const LAPTOPS = [")
    end = source.index("];", start)
    block = source[start + len("const LAPTOPS = "):end + 1]
    block = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', block)
    block = re.sub(r",\s*([}\]])", r"\1", block)
    return json.loads(block)


def patch_between(source, start_marker, end_marker, content):
    if start_marker not in source or end_marker not in source:
        raise SystemExit(f"Falta el marcador {start_marker} en index.html")
    pre, rest = source.split(start_marker, 1)
    _, post = rest.split(end_marker, 1)
    return f"{pre}{start_marker}\n{content}\n{end_marker}{post}"


# --------------------------------------------------------------------------
# index.html: slugs y tarjetas
# --------------------------------------------------------------------------

def ensure_slugs(source, laptops):
    """Añade el campo slug a cada modelo si todavía no lo tiene."""
    changed = False
    for l in laptops:
        if l.get("slug"):
            continue
        l["slug"] = slugify(l["name"])
        needle = f'id: "{l["id"]}", img:'
        replacement = f'id: "{l["id"]}", slug: "{l["slug"]}", img:'
        if needle in source:
            source = source.replace(needle, replacement, 1)
            changed = True
        else:
            raise SystemExit(f"No encuentro el modelo {l['id']} para añadirle el slug")
    return source, changed


def card_html(l, score):
    image = l["img"]
    slug = l["slug"]
    return f"""      <article class="card">
        <div class="thumb">
          <a class="thumb-hit" href="portatil/{slug}.html" tabindex="-1" aria-hidden="true"></a>
          <img class="shot" src="{image}" alt="{esc(l['name'], True)}" loading="lazy" width="1000" height="750">
          <span class="brand-chip">{esc(l['brand'])}</span>
        </div>
        <div class="card-body">
          <h3><a href="portatil/{slug}.html">{esc(l['name'])}</a></h3>
          <div class="specs">{esc(l['cpu'])}<br>{esc(l['ram'])} · {esc(l['storage'])}<br>{esc(l['screen'])}</div>
          <div class="bottom">
            <div class="p">{eur(l['price'])}</div>
            <div class="score" title="Nota para Equilibrado">{score} / 100</div>
          </div>
          <div class="actions">
            <button class="btn-mini" data-set="A" data-id="{l['id']}">Comparar como A</button>
            <button class="btn-mini" data-set="B" data-id="{l['id']}">Comparar como B</button>
          </div>
        </div>
      </article>"""


def organizacion_ld():
    """Nodo Organization compartido por todas las páginas."""
    return {
        "@type": "Organization",
        "@id": f"{SITE}#organizacion",
        "name": "ComparaPortátil",
        "url": SITE,
        "logo": {
            "@type": "ImageObject",
            "url": f"{SITE}img/logo.png",
            "width": 512,
            "height": 512,
        },
        "sameAs": ["https://github.com/Raulft721/portatiles"],
    }


def itemlist_ld(laptops):
    data = {
        "@context": "https://schema.org",
        "@graph": [
            organizacion_ld(),
            {
                "@type": "WebSite",
                "@id": f"{SITE}#web",
                "name": "ComparaPortátil",
                "url": SITE,
                "inLanguage": "es",
                "publisher": {"@id": f"{SITE}#organizacion"},
            },
            {
                "@type": "ItemList",
                "@id": f"{SITE}#catalogo",
                "name": "Catálogo de portátiles de ComparaPortátil",
                "numberOfItems": len(laptops),
                "itemListOrder": "https://schema.org/ItemListOrderDescending",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i + 1,
                        "name": l["name"],
                        "url": f"{SITE}portatil/{l['slug']}.html",
                    }
                    for i, l in enumerate(laptops)
                ],
            },
        ],
    }
    return (f'<script type="application/ld+json">\n'
            f'{json.dumps(data, ensure_ascii=False, indent=2)}\n'
            f'</script>')


# --------------------------------------------------------------------------
# Fichas
# --------------------------------------------------------------------------

def build_ficha(l, laptops, hoy):
    name = l["name"]
    slug = l["slug"]
    url = f"{SITE}portatil/{slug}.html"
    scores = l["scores"]

    # CATS está en orden fijo: en caso de empate gana el apartado que aparece antes.
    best = next(k for k, _ in CATS if scores[k] == max(scores.values()))
    worst = next(k for k, _ in CATS if scores[k] == min(scores.values()))

    max_score = max(x["scores"][best] for x in laptops)
    lighter_rank = 1 + sum(1 for x in laptops if x["weight"] < l["weight"])
    price_rank = 1 + sum(1 for x in laptops if x["price"] < l["price"])

    if lighter_rank == 1:
        weight_line = f"Es el más ligero de los {len(laptops)} modelos."
    elif lighter_rank <= 4:
        weight_line = f"Con {kg(l['weight'])} es el {lighter_rank}.º más ligero de los {len(laptops)} modelos."
    elif lighter_rank > len(laptops) - 4:
        weight_line = f"Con {kg(l['weight'])} está entre los más pesados del catálogo."
    else:
        weight_line = f"Pesa {kg(l['weight'])}."

    if price_rank == 1:
        price_line = f"Es el más barato del catálogo, con {eur(l['price'])}."
    elif price_rank <= 4:
        price_line = f"Cuesta {eur(l['price'])}, entre los cuatro más baratos del catálogo."
    elif price_rank >= 19:
        price_line = f"Cuesta {eur(l['price'])}, entre los cuatro más caros del catálogo."
    else:
        price_line = f"Cuesta {eur(l['price'])}, en la mitad de la tabla de precios."

    if scores[best] == max_score:
        first = f"Es de los mejores del catálogo en {SIN[best]}: {scores[best]} de 100."
    else:
        first = f"Su mejor baza es {SIN[best]}, con {scores[best]} de 100."
    segundo = f"Para {VERB[worst]} se queda en {scores[worst]} de 100."

    parrafo = " ".join([first, segundo, weight_line, price_line])

    lead = (f"{name} cuesta {eur(l['price'])} y llega con {l['cpu']}, {l['ram']}, "
            f"{l['storage']} y pantalla {l['screen']}. Un portátil de {l['os']} "
            f"pensado para {USE[best]}.")

    bars = "\n".join(
        f'    <div class="bar"><span>{label}</span>'
        f'<span class="bar-track"><i style="width:{scores[key]}%"></i></span>'
        f'<span class="bar-val">{scores[key]}</span></div>'
        for key, label in CATS
    )

    # Los equipos que se venden sin sistema operativo necesitan un aviso explícito.
    sin_so = l["os"].strip().lower().startswith(("freedos", "sin sistema", "sin so"))
    aviso_so = ("" if not sin_so else
                "\n  <p class=\"caption\">Se vende sin sistema operativo: hay que "
                "instalar Windows o Linux y contar con la licencia.</p>")
    if l.get("aviso"):
        aviso_so += f"\n  <p class=\"caption\">{esc(l['aviso'])}</p>"

    cercanos = sorted((x for x in laptops if x["id"] != l["id"]),
                      key=lambda x: abs(x["price"] - l["price"]))[:3]
    alts = []
    for x in cercanos:
        delta = x["price"] - l["price"]
        signo = "+" if delta > 0 else "−"
        alts.append(
            f'    <li><a href="{x["slug"]}.html">{esc(x["name"])}</a>'
            f'<span class="delta">{signo}{eur(abs(delta))}</span></li>'
        )
    alts = "\n".join(alts)

    extra = ""
    guias = []
    if l["price"] <= 800 or scores["estudio"] >= 85:
        guias.append(('<li><a href="../guias/mejor-portatil-estudiar.html">'
                      'Mejor portátil para estudiar por menos de 800 €</a></li>'))
    if scores["gaming"] >= 60:
        guias.append(('<li><a href="../guias/portatil-gaming-1000-euros.html">'
                      'Portátil gaming por menos de 1.100 €</a></li>'))
    if guias:
        extra = ('\n  <h2>Guías relacionadas</h2>\n\n  <ul>\n    '
                 + "\n    ".join(guias) + "\n  </ul>\n")

    title = f"{name}: precio y ficha técnica"
    desc = (f"{name} por {eur(l['price'])}: {l['cpu']}, {l['ram']} y {l['storage']}. "
            f"Ficha técnica, notas por uso y alternativas.")
    og_image = f"{SITE}img/og/{slug}.jpg"

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "name": name,
                "image": f"{SITE}{l['img']}",
                "description": (f"{name}: {l['cpu']}, {l['gpu']}, {l['ram']}, "
                                f"{l['storage']} y pantalla {l['screen']}."),
                "brand": {"@type": "Brand", "name": l["brand"]},
                "category": "Portátiles",
                "offers": {
                    "@type": "Offer",
                    "url": url,
                    "priceCurrency": "EUR",
                    "price": str(l["price"]),
                    "availability": "https://schema.org/InStock",
                    "itemCondition": "https://schema.org/NewCondition",
                },
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{url}#migas",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
                    {"@type": "ListItem", "position": 2, "name": "Catálogo",
                     "item": f"{SITE}#catalogo"},
                    {"@type": "ListItem", "position": 3, "name": name, "item": url},
                ],
            },
            {
                "@type": "WebPage",
                "@id": f"{url}#pagina",
                "url": url,
                "name": f"{name}: precio y ficha técnica",
                "inLanguage": "es",
                "isPartOf": {"@id": f"{SITE}#web"},
                "breadcrumb": {"@id": f"{url}#migas"},
                "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}{l['img']}"},
                "dateModified": hoy.isoformat(),
                "publisher": {"@id": f"{SITE}#organizacion"},
            },
        ],
    }

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc, True)}" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
<link rel="canonical" href="{url}" />
<link rel="icon" href="../favicon.svg" type="image/svg+xml" />
<link rel="stylesheet" href="../contenido.css" />
<link rel="stylesheet" href="ficha.css" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="ComparaPortátil" />
<meta property="og:locale" content="es_ES" />
<meta property="og:title" content="{esc(name, True)}: {eur(l['price'])}" />
<meta property="og:description" content="{esc(desc, True)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{og_image}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{esc(name, True)}" />
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
</head>
<body>

<nav class="nav">
  <div class="wrap nav-in">
    <a href="../" class="logo">
      <span class="logo-mark">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="4" width="18" height="12" rx="2"/><path d="M2 20h20"/>
        </svg>
      </span>
      ComparaPortátil
    </a>
    <div class="nav-links">
      <a href="../#comparador">Comparador</a>
      <a href="../#catalogo">Catálogo</a>
      <a href="../guias/mejor-portatil-estudiar.html">Estudiar</a>
      <a href="../guias/portatil-gaming-1000-euros.html">Gaming</a>
    </div>
    <a href="../#catalogo" class="nav-spacer" style="font-size:13.5px;font-weight:600;">Ver los {len(laptops)} modelos</a>
  </div>
</nav>

<header class="hero wrap read">
  <nav class="crumbs" aria-label="Ruta de navegación">
    <a href="../">Inicio</a>
    <span class="sep" aria-hidden="true">›</span>
    <a href="../#catalogo">Catálogo</a>
    <span class="sep" aria-hidden="true">›</span>
    <span aria-current="page">{esc(name)}</span>
  </nav>
  <div class="kicker">{esc(l['brand'])} · {esc(l['os'])}</div>
  <h1>{esc(name)}</h1>
  <div class="meta">
    <span class="price-strong">{eur(l['price'])}</span>
    <span>·</span>
    <span>precio orientativo</span>
    <span>·</span>
    <span>Ficha actualizada el {fecha_larga(hoy)}</span>
  </div>
  <p class="lead">{esc(lead)}</p>
</header>

<article class="wrap read">

  <figure class="ficha-photo">
    <img src="../{l['img']}" alt="{esc(name, True)} sobre fondo blanco" width="1000" height="750" />
  </figure>

  <h2>Ficha técnica</h2>

  <div class="table-wrap spec-wrap">
    <table>
      <tbody>
        <tr><th scope="row">Procesador</th><td>{esc(l['cpu'])}</td></tr>
        <tr><th scope="row">Gráficos</th><td>{esc(l['gpu'])}</td></tr>
        <tr><th scope="row">Memoria</th><td>{esc(l['ram'])}</td></tr>
        <tr><th scope="row">Almacenamiento</th><td>{esc(l['storage'])}</td></tr>
        <tr><th scope="row">Pantalla</th><td>{esc(l['screen'])}</td></tr>
        <tr><th scope="row">Peso</th><td>{kg(l['weight'])}</td></tr>
        <tr><th scope="row">Autonomía</th><td>{horas(l)}</td></tr>
        <tr><th scope="row">Sistema operativo</th><td>{esc(l['os'])}</td></tr>
        <tr><th scope="row">Precio</th><td>{eur(l['price'])} orientativo</td></tr>
      </tbody>
    </table>
  </div>

  <h2>Para quién es</h2>

  <p>{esc(parrafo)}</p>

  <ul>
    <li><strong>Encaja</strong> si lo que más te importa es {USE[best]}, y el presupuesto llega a {eur(l['price'])}.</li>
    <li><strong>Busca otra opción</strong> si lo que prima es {SIN[worst]}: aquí saca {scores[worst]} de 100.</li>
  </ul>
{aviso_so}

  <h2>Notas por uso</h2>

  <p class="caption">Escala de 0 a 100. En el comparador se recalculan según el perfil que elijas.</p>

  <div class="bars">
{bars}
  </div>

  <h2>Alternativas por precio</h2>

  <p>Los tres modelos del catálogo que más se acercan a su precio:</p>

  <ul class="alts">
{alts}
  </ul>

  <div class="cta">
    <h2>Compáralo con otro modelo</h2>
    <p>Abre el comparador con este portátil ya cargado y enfréntalo a cualquiera de los {len(laptops)}.</p>
    <a class="btn" href="../?a={l['id']}#comparador">Abrir el comparador</a>
  </div>
{extra}
</article>

<footer>
  <div class="wrap foot">
    <span><b>ComparaPortátil</b> · Precios orientativos de referencia: varían según tienda y disponibilidad, y algún modelo puede estar descatalogado. Fotografía de producto del fabricante, usada con fines informativos. Sin anuncios ni enlaces de afiliado.</span>
    <span><a href="../">Inicio</a> · <a href="../#catalogo">Catálogo</a> · <a href="../metodologia.html">Metodología</a> · <a href="../sobre.html">Sobre</a> · <a href="../contacto.html">Contacto</a></span>
  </div>
</footer>

</body>
</html>
"""


# --------------------------------------------------------------------------
# Sitemap
# --------------------------------------------------------------------------

def actualizar_conteos(source, laptops):
    """Sustituye los números escritos a mano por el recuento real del catálogo."""
    total = len(laptops)
    marcas = len({l["brand"] for l in laptops})
    for patron, nuevo in (
        (r"Compara \d+ portátiles", f"Compara {total} portátiles"),
        (r"\d+ portátiles de \d+ marcas", f"{total} portátiles de {marcas} marcas"),
        (r"DATOS \(\d+ portátiles", f"DATOS ({total} portátiles"),
        (r"Ver los \d+ modelos", f"Ver los {total} modelos"),
    ):
        source = re.sub(patron, nuevo, source)
    return source


def build_sitemap(laptops, hoy):
    urls = [(SITE, "1.0"),
            (f"{SITE}guias/mejor-portatil-estudiar.html", "0.8"),
            (f"{SITE}guias/portatil-gaming-1000-euros.html", "0.8"),
            (f"{SITE}metodologia.html", "0.6"),
            (f"{SITE}sobre.html", "0.5"),
            (f"{SITE}contacto.html", "0.4")]
    urls += [(f"{SITE}portatil/{l['slug']}.html", "0.7") for l in laptops]
    cuerpo = "\n".join(
        f"""  <url>
    <loc>{u}</loc>
    <lastmod>{hoy.isoformat()}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{p}</priority>
  </url>"""
        for u, p in urls
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{cuerpo}\n</urlset>\n")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    hoy = date.today()
    source = INDEX.read_text(encoding="utf-8")
    laptops = parse_laptops(source)

    source, changed = ensure_slugs(source, laptops)
    if changed:
        INDEX.write_text(source, encoding="utf-8", newline="\n")

    # Tarjetas del catálogo, ordenadas igual que en la web (perfil equilibrado).
    ordenados = sorted(laptops, key=lambda l: -overall(l))
    cards = "\n".join(card_html(l, overall(l)) for l in ordenados)
    source = patch_between(source, "<!-- catalogo:inicio -->", "<!-- catalogo:fin -->", cards)
    source = patch_between(source, "<!-- itemlist:inicio -->", "<!-- itemlist:fin -->",
                           itemlist_ld(laptops))
    source = actualizar_conteos(source, laptops)
    INDEX.write_text(source, encoding="utf-8", newline="\n")

    # Fichas
    FICHAS_DIR.mkdir(parents=True, exist_ok=True)
    for l in laptops:
        (FICHAS_DIR / f"{l['slug']}.html").write_text(
            build_ficha(l, laptops, hoy), encoding="utf-8", newline="\n")

    # Sitemap
    (ROOT / "sitemap.xml").write_text(build_sitemap(laptops, hoy),
                                      encoding="utf-8", newline="\n")

    # Manifiesto para las imágenes sociales
    OG_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(
        [{"slug": l["slug"], "name": l["name"], "price": eur(l["price"]),
          "brand": l["brand"], "img": l["img"]} for l in laptops],
        ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    print(f"{len(laptops)} fichas generadas en portatil/")
    print("index.html: catálogo pre-renderizado y ItemList")
    print("sitemap.xml actualizado")
    print("scripts/og-manifest.json listo para scripts/og.ps1")

    largos = [(t, len(t)) for t in
              [f"{l['name']}: precio y ficha técnica" for l in laptops] if len(t) > 60]
    if largos:
        print("\nAVISO: títulos de más de 60 caracteres:")
        for t, n in largos:
            print(f"  {n}  {t}")


if __name__ == "__main__":
    main()
