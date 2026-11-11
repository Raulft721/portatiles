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
from urllib.parse import quote_plus
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://raulft721.github.io/portatiles/"
INDEX = ROOT / "index.html"
FICHAS_DIR = ROOT / "portatil"
OG_DIR = ROOT / "img" / "og"
MANIFEST = ROOT / "scripts" / "og-manifest.json"

# Rivales con Windows que aparecen en la guía «MacBook o Windows».
MAC_O_WINDOWS = {"hp-pavilion-aero-13", "asus-zenbook-14-oled", "dell-xps-13",
                 "asus-rog-zephyrus-g14"}

# Amazon Afiliados. Pon aquí tu ID de afiliado (el «tag», termina en -21) y vuelve a
# ejecutar el script. Mientras esté vacío, las fichas no muestran el botón de compra ni
# el aviso de afiliación. El tag no es un secreto: aparece en todos los enlaces.
AMAZON_TAG = "comparaportat-21"
AVISO_AFILIADO = ("Como afiliado de Amazon, ComparaPortátil obtiene ingresos por las "
                  "compras adscritas que cumplen los requisitos aplicables. No cambia lo "
                  "que pagas ni las notas del comparador.")

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

def amazon_url(l):
    """Búsqueda del modelo en Amazon.es con el tag de afiliado.

    Se usa la búsqueda y no un producto concreto porque cada modelo tiene varias
    configuraciones y vendedores; así el enlace no se rompe si una se agota.
    """
    return f"https://www.amazon.es/s?k={quote_plus(l['name'])}&tag={AMAZON_TAG}"


NOTA_AFILIADO_CORTA = ("Enlace de afiliado: si compras, ComparaPortátil recibe una comisión "
                       "y tú pagas lo mismo.")


def compra_arriba(l):
    """Botón de compra visible nada más abrir la ficha, junto al precio."""
    if not AMAZON_TAG:
        return ""
    return f"""
  <div class="compra-top">
    <a class="btn" href="{esc(amazon_url(l), True)}" rel="sponsored nofollow noopener" target="_blank">Ver precio actual en Amazon</a>
    <span class="caption">{NOTA_AFILIADO_CORTA}</span>
  </div>"""


def compra_vs(a, b):
    """Un botón por modelo justo después de la respuesta rápida de una comparativa."""
    if not AMAZON_TAG:
        return ""
    botones = "\n".join(
        f'    <a class="btn" href="{esc(amazon_url(x), True)}" rel="sponsored nofollow noopener" '
        f'target="_blank">Ver el {esc(corto(x["name"]))} en Amazon</a>'
        for x in (a, b))
    return f"""
  <div class="compra-top">
{botones}
    <span class="caption">Enlaces de afiliado: si compras, ComparaPortátil recibe una comisión y tú pagas lo mismo.</span>
  </div>
"""


def compra_html(l):
    if not AMAZON_TAG:
        return ""
    return f"""
  <div class="cta compra">
    <h2>Dónde comprarlo</h2>
    <p>El precio cambia a menudo y puede haber varias configuraciones: comprueba
    procesador, memoria y almacenamiento antes de comprar.</p>
    <a class="btn" href="{esc(amazon_url(l), True)}" rel="sponsored nofollow noopener" target="_blank">Ver precio actual en Amazon</a>
    <p class="caption">{AVISO_AFILIADO}</p>
  </div>
"""


# --------------------------------------------------------------------------
# Contenido propio de cada ficha: puntos fuertes y débiles, rival y preguntas.
# Todo sale de los datos del catálogo; nada se escribe a mano por modelo.
# --------------------------------------------------------------------------

def best_cat(l):
    s = l["scores"]
    return next(k for k, _ in CATS if s[k] == max(s.values()))


def gb(texto):
    """Primera cantidad en GB de un texto («16 GB LPDDR5», «1 TB SSD»)."""
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*(TB|GB)", texto)
    if not m:
        return None
    n = float(m.group(1).replace(",", "."))
    return n * 1024 if m.group(2) == "TB" else n


def hz(texto):
    m = re.search(r"(\d+)\s*Hz", texto)
    return int(m.group(1)) if m else None


def es_arm(l):
    return "snapdragon" in l["cpu"].lower()


def rank(l, laptops, key, reverse=False):
    """Puesto de l (1 = mejor) según key; reverse=True si más es mejor."""
    vals = [key(x) for x in laptops if key(x) is not None]
    v = key(l)
    if v is None:
        return None
    return 1 + sum(1 for x in vals if (x > v if reverse else x < v))


def puntos(l, laptops):
    n = len(laptops)
    s = l["scores"]
    fuertes, debiles = [], []

    r_peso = rank(l, laptops, lambda x: x["weight"])
    r_bat = rank(l, laptops, lambda x: x.get("battery"), reverse=True)
    r_precio = rank(l, laptops, lambda x: x["price"])
    ram, alm, refresco = gb(l["ram"]), gb(l["storage"]), hz(l["screen"])
    pantalla = l["screen"].lower()

    if r_peso <= 6:
        fuertes.append(f"<strong>Ligero:</strong> {kg(l['weight'])}, el {r_peso}.º más ligero de los {n} modelos.")
    if r_bat is not None and r_bat <= 6:
        fuertes.append(f"<strong>Mucha autonomía:</strong> {l['battery']} h según el fabricante, de las seis mejores cifras del catálogo.")
    if r_precio <= 6:
        fuertes.append(f"<strong>Precio bajo:</strong> {eur(l['price'])}, entre los seis más baratos del catálogo.")
    if "oled" in pantalla or "xdr" in pantalla:
        fuertes.append(f"<strong>Pantalla de gama alta:</strong> {esc(l['screen'])}.")
    elif refresco and refresco >= 120:
        fuertes.append(f"<strong>Pantalla fluida:</strong> {refresco} Hz.")
    if "rtx" in l["gpu"].lower():
        fuertes.append(f"<strong>Gráfica dedicada:</strong> {esc(l['gpu'])}.")
    if ram and ram >= 32:
        fuertes.append(f"<strong>Mucha memoria:</strong> {esc(l['ram'])}.")
    if alm and alm >= 1024:
        fuertes.append("<strong>Almacenamiento amplio:</strong> 1 TB.")
    for k, label in CATS:
        if s[k] >= 90:
            fuertes.append(f"<strong>Nota alta para {VERB[k]}:</strong> {s[k]} de 100.")
            break

    if l["weight"] >= 2.0:
        debiles.append(f"<strong>Pesado:</strong> {kg(l['weight'])}, poco práctico para llevarlo a diario.")
    if l.get("battery") is None:
        debiles.append("<strong>Autonomía sin dato:</strong> el fabricante no publica las horas.")
    elif l["battery"] <= 7:
        debiles.append(f"<strong>Autonomía corta:</strong> {l['battery']} h según el fabricante.")
    if ram and ram <= 8:
        debiles.append(f"<strong>Memoria justa:</strong> {esc(l['ram'])}, se queda corta con muchas aplicaciones abiertas.")
    if alm and alm <= 256:
        debiles.append(f"<strong>Almacenamiento justo:</strong> {esc(l['storage'])}.")
    os_ = l["os"].lower()
    if os_.startswith("freedos"):
        debiles.append("<strong>Sin sistema operativo:</strong> hay que instalar Windows o Linux y contar con la licencia.")
    if os_.startswith("chromeos"):
        debiles.append("<strong>ChromeOS:</strong> no instala programas de Windows.")
    if es_arm(l):
        debiles.append("<strong>Procesador ARM:</strong> algunos programas antiguos, controladores y juegos con antitrampas no funcionan.")
    if r_precio > n - 6:
        debiles.append(f"<strong>Precio alto:</strong> {eur(l['price'])}, entre los seis más caros del catálogo.")
    if s["gaming"] < 40:
        debiles.append(f"<strong>No es para jugar:</strong> {s['gaming']} de 100 en juegos.")

    if not fuertes:
        k = best_cat(l)
        fuertes.append(f"<strong>Su mejor apartado:</strong> {SIN[k]}, con {s[k]} de 100.")
    if not debiles:
        k = next(k for k, _ in CATS if s[k] == min(s.values()))
        debiles.append(f"<strong>Su apartado más flojo:</strong> {SIN[k]}, con {s[k]} de 100.")
    return fuertes[:4], debiles[:4]


def rival_de(l, laptops):
    """El modelo más cercano en precio con el mismo uso principal."""
    mismos = [x for x in laptops if x["id"] != l["id"] and best_cat(x) == best_cat(l)]
    pool = mismos or [x for x in laptops if x["id"] != l["id"]]
    return min(pool, key=lambda x: (abs(x["price"] - l["price"]), x["price"]))


def preguntas(l):
    name, s = l["name"], l["scores"]
    g = s["gaming"]
    if g >= 80:
        jugar = f"Sí. Saca {g} de 100 para jugar gracias a su {l['gpu']}, de las mejores notas del catálogo en este apartado."
    elif g >= 50:
        jugar = f"Para juegos ligeros y eSports, sí. En juegos exigentes se queda corto: {g} de 100 para jugar, con {l['gpu']}."
    else:
        jugar = (f"No es su punto fuerte: {g} de 100 para jugar, con gráfica integrada ({l['gpu']}). "
                 "Sirve para juegos sencillos o en la nube.")
    if l.get("battery") is None:
        bat = ("El fabricante no publica la autonomía"
               + (f"; la batería es de {str(l['wh']).replace('.', ',')} Wh." if l.get("wh") else "."))
    else:
        bat = (f"{l['battery']} horas según el fabricante. Esa cifra se mide con brillo bajo y tareas "
               "suaves; con uso normal, cuenta con algo más de la mitad.")
    w = l["weight"]
    if w < 1.4:
        llevar = f"Sí. Con {kg(w)} se lleva en la mochila todos los días sin notarlo."
    elif w < 2.0:
        llevar = f"Se puede: {kg(w)} es un peso normal, aunque al final del día se nota más que en un ultraligero."
    else:
        llevar = f"No es lo ideal. Con {kg(w)}, más el cargador, es un equipo para mover de vez en cuando, no a diario."
    return [
        (f"¿Sirve el {name} para jugar?", jugar),
        (f"¿Cuánto dura la batería del {name}?", bat),
        (f"¿Es buena opción para llevarlo a clase o al trabajo cada día?", llevar),
    ]


def faq_html(qs):
    items = "\n".join(
        f"    <details>\n      <summary>{esc(q)}</summary>\n      <p>{esc(a)}</p>\n    </details>"
        for q, a in qs)
    return f'  <div class="faq">\n{items}\n  </div>'


def faq_ld(qs, url):
    return {
        "@type": "FAQPage",
        "@id": f"{url}#preguntas",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qs
        ],
    }


# --------------------------------------------------------------------------
# Comparativas «A vs B»
# --------------------------------------------------------------------------

VS_PAIRS = [
    ("macbook-air-13-m4", "macbook-air-13-m5"),
    ("hp-victus-15", "lenovo-loq-15"),
    ("lenovo-loq-15", "asus-tuf-gaming-a15"),
    ("macbook-air-13-m5", "dell-xps-13"),
    ("macbook-air-13-m4", "asus-zenbook-14-oled"),
    ("macbook-neo", "hp-pavilion-aero-13"),
    ("lenovo-ideapad-slim-3-15", "acer-aspire-5-15"),
    ("acer-swift-go-14", "asus-zenbook-14-oled"),
    ("samsung-galaxy-book4-pro", "samsung-galaxy-book5-pro-14"),
    ("macbook-air-15-m5", "macbook-pro-14-m5"),
    # Segunda tanda (11/11/2026), tras el primer clic en una comparativa.
    ("macbook-air-13-m4", "dell-xps-13"),
    ("hp-victus-15", "asus-tuf-gaming-a15"),
    ("lenovo-loq-15", "lenovo-loq-15irx10"),
    ("acer-nitro-v-15", "lenovo-loq-15irx10"),
    ("macbook-neo", "macbook-air-13-m4"),
    ("macbook-air-13-m5", "macbook-air-15-m5"),
    ("asus-zenbook-14-oled", "samsung-galaxy-book4-pro"),
    ("microsoft-surface-laptop-7", "macbook-air-13-m5"),
    ("acer-chromebook-plus-515", "lenovo-ideapad-slim-3-15"),
    ("asus-rog-zephyrus-g14", "asus-tuf-gaming-a16"),
]


def vs_slug(a, b):
    return f"{a['slug']}-vs-{b['slug']}"


def vs_de(l, laptops):
    """Comparativas en las que aparece l: lista de (rival, slug de la página)."""
    por = {x["slug"]: x for x in laptops}
    out = []
    for sa, sb in VS_PAIRS:
        if l["slug"] in (sa, sb):
            otro = por[sb if l["slug"] == sa else sa]
            out.append((otro, vs_slug(por[sa], por[sb])))
    return out


def corto(name):
    """Nombre sin la coletilla entre paréntesis para títulos largos."""
    return re.sub(r"\s*\((A18 Pro)\)", "", name)


def build_vs(a, b, laptops, hoy):
    slug = vs_slug(a, b)
    url = f"{SITE}vs/{slug}.html"
    na, nb = a["name"], b["name"]
    ca, cb = corto(na), corto(nb)
    sa, sb = a["scores"], b["scores"]
    ga, gb_ = overall(a), overall(b)

    title = f"{ca} vs {cb}: cuál comprar"
    if len(title) > 65:
        title = f"{ca} vs {cb}"
    desc = (f"{ca} contra {cb}: precio, peso, autonomía, pantalla y notas por uso, "
            f"con un veredicto claro según para qué lo quieras.")
    if len(esc(desc, True)) > 160:
        desc = f"{ca} contra {cb}: precio, peso, autonomía y notas por uso, con veredicto claro."

    def win(va, vb, mas_es_mejor=True, umbral=0):
        if va is None or vb is None or abs(va - vb) <= umbral:
            return "", ""
        mejor_a = (va > vb) if mas_es_mejor else (va < vb)
        return (' class="win"', "") if mejor_a else ("", ' class="win"')

    filas = []
    def fila(label, ta, tb, w=("", "")):
        filas.append(f'        <tr><th scope="row">{label}</th><td{w[0]}>{ta}</td><td{w[1]}>{tb}</td></tr>')

    fila("Precio", eur(a["price"]), eur(b["price"]), win(a["price"], b["price"], False))
    fila("Procesador", esc(a["cpu"]), esc(b["cpu"]))
    fila("Gráficos", esc(a["gpu"]), esc(b["gpu"]))
    fila("Memoria", esc(a["ram"]), esc(b["ram"]), win(gb(a["ram"]), gb(b["ram"])))
    fila("Almacenamiento", esc(a["storage"]), esc(b["storage"]), win(gb(a["storage"]), gb(b["storage"])))
    fila("Pantalla", esc(a["screen"]), esc(b["screen"]))
    fila("Peso", kg(a["weight"]), kg(b["weight"]), win(a["weight"], b["weight"], False))
    fila("Autonomía", horas(a), horas(b), win(a.get("battery"), b.get("battery")))
    fila("Sistema operativo", esc(a["os"]), esc(b["os"]))
    for k, label in CATS:
        fila(f"Nota para {VERB[k]}", f"{sa[k]} / 100", f"{sb[k]} / 100", win(sa[k], sb[k]))
    fila("Nota global", f"{ga} / 100", f"{gb_} / 100", win(ga, gb_))
    tabla = "\n".join(filas)

    # Veredicto: quién gana cada uso (diferencia de 3 puntos o más) y en global.
    gana_a = [k for k, _ in CATS if sa[k] - sb[k] >= 3]
    gana_b = [k for k, _ in CATS if sb[k] - sa[k] >= 3]
    dif = b["price"] - a["price"]
    if dif > 0:
        precio_txt = f"El {ca} cuesta {eur(dif)} menos."
    elif dif < 0:
        precio_txt = f"El {cb} cuesta {eur(-dif)} menos."
    else:
        precio_txt = "Cuestan lo mismo."

    def lista(ks):
        nombres = [VERB[k] for k in ks]
        return nombres[0] if len(nombres) == 1 else ", ".join(nombres[:-1]) + " y " + nombres[-1]

    partes = []
    if gana_a:
        partes.append(f"el {ca} es mejor para {lista(gana_a)}")
    if gana_b:
        partes.append(f"el {cb} es mejor para {lista(gana_b)}")
    if partes:
        usos_txt = "Por notas, " + "; ".join(partes) + "."
    else:
        usos_txt = "En las notas por uso están prácticamente empatados (menos de 3 puntos en cada apartado)."

    if ga - gb_ >= 2:
        global_txt = f"En la nota global gana el {ca} ({ga} frente a {gb_})."
    elif gb_ - ga >= 2:
        global_txt = f"En la nota global gana el {cb} ({gb_} frente a {ga})."
    else:
        global_txt = f"En la nota global están empatados ({ga} y {gb_})."

    # Recomendación: si uno gana en global y no es más caro, gana claro.
    if (ga - gb_ >= 2 and a["price"] <= b["price"]):
        rec = f"Si dudas entre los dos, el {ca}: tiene mejor nota y no cuesta más."
    elif (gb_ - ga >= 2 and b["price"] <= a["price"]):
        rec = f"Si dudas entre los dos, el {cb}: tiene mejor nota y no cuesta más."
    elif abs(ga - gb_) < 2:
        barato = ca if a["price"] < b["price"] else cb
        rec = (f"Si dudas entre los dos, el {barato}: rinden parecido y es el más barato."
               if a["price"] != b["price"] else
               "Elige según el apartado que más te importe.")
    else:
        mejor, peor = (ca, cb) if ga > gb_ else (cb, ca)
        rec = (f"El {mejor} es mejor en conjunto, pero el {peor} cuesta menos: "
               f"elige el {mejor} si te llega el presupuesto.")
    rapida = f"{precio_txt} {usos_txt} {global_txt} {rec}"

    def ventajas(x, sx, o, so):
        """Ventajas concretas de x frente a o: (frase para el título, frase con datos)."""
        v = []
        mejor = [k for k, _ in CATS if sx[k] - so[k] >= 3]
        if mejor:
            v.append((f"si lo que más te importa es {lista(mejor)}",
                      "<strong>Mejor nota para " + lista(mejor) + ":</strong> "
                      + (f"{sx[mejor[0]]} frente a {so[mejor[0]]}" if len(mejor) == 1 else
                         ", ".join(f"{VERB[k]} {sx[k]} frente a {so[k]}" for k in mejor)) + "."))
        if o["price"] - x["price"] >= 50:
            v.append(("si quieres gastar menos",
                      f"<strong>Más barato:</strong> cuesta {eur(o['price'] - x['price'])} menos."))
        if o["weight"] - x["weight"] >= 0.1:
            v.append(("si buscas el más ligero",
                      f"<strong>Más ligero:</strong> {kg(x['weight'])} frente a {kg(o['weight'])}."))
        bx, bo = x.get("battery"), o.get("battery")
        if bx is not None and bo is not None and bx - bo >= 2:
            v.append(("si quieres más autonomía",
                      f"<strong>Más autonomía:</strong> {bx} h frente a {bo} h según los fabricantes."))
        ax, ao = gb(x["storage"]), gb(o["storage"])
        if ax and ao and ax > ao:
            v.append(("si necesitas más almacenamiento",
                      f"<strong>Más almacenamiento:</strong> {esc(x['storage'])} frente a {esc(o['storage'])}."))
        rx, ro = gb(x["ram"]), gb(o["ram"])
        if rx and ro and rx > ro:
            v.append(("si trabajas con muchas aplicaciones a la vez",
                      f"<strong>Más memoria:</strong> {esc(x['ram'])} frente a {esc(o['ram'])}."))
        px, po = x["screen"].lower(), o["screen"].lower()
        if ("oled" in px or "xdr" in px) and not ("oled" in po or "xdr" in po):
            v.append(("si quieres mejor pantalla",
                      f"<strong>Mejor pantalla:</strong> {esc(x['screen'])}."))
        if "táctil" in px and "táctil" not in po:
            v.append(("si quieres pantalla táctil",
                      f"<strong>Pantalla táctil:</strong> {esc(x['screen'])}."))
        # Gráfica: solo cuando la comparación es clara (misma gama y generación más
        # nueva, o misma generación y gama superior). Ej.: RTX 4060 → 5060, 5050 → 5060.
        gx, go_ = re.search(r"RTX (\d)0(\d)0", x["gpu"]), re.search(r"RTX (\d)0(\d)0", o["gpu"])
        if gx and go_:
            genx, gamx, geno, gamo = int(gx[1]), int(gx[2]), int(go_[1]), int(go_[2])
            if gamx == gamo and genx > geno:
                v.append(("si quieres la gráfica más nueva",
                          f"<strong>Gráfica de generación más nueva:</strong> {esc(x['gpu'])} frente a {esc(o['gpu'])}."))
            elif genx == geno and gamx > gamo:
                v.append(("si quieres más potencia gráfica",
                          f"<strong>Gráfica de gama superior:</strong> {esc(x['gpu'])} frente a {esc(o['gpu'])}."))
        # Pantalla más grande (al menos una pulgada).
        sx, so_ = re.search(r'(\d+(?:,\d)?)"', x["screen"]), re.search(r'(\d+(?:,\d)?)"', o["screen"])
        if sx and so_:
            px_, po_ = float(sx[1].replace(",", ".")), float(so_[1].replace(",", "."))
            if px_ - po_ >= 1:
                v.append(("si quieres una pantalla más grande",
                          f"<strong>Pantalla más grande:</strong> {sx[1]}\" frente a {so_[1]}\"."))
        # Sistema operativo. «FreeDOS» significa que viene sin sistema: no es una
        # preferencia, es una desventaja del otro modelo.
        sin_x, sin_o = x["os"].lower().startswith("freedos"), o["os"].lower().startswith("freedos")
        if sin_o and not sin_x:
            v.append((f"si no quieres instalar el sistema operativo",
                      f"<strong>Incluye {esc(x['os'])}:</strong> el otro se vende sin sistema operativo."))
        elif x["os"] != o["os"] and not sin_x and not sin_o:
            v.append((f"si prefieres {x['os'].replace(' 11', '')}",
                      f"<strong>Sistema operativo:</strong> {esc(x['os'])}."))
        return v

    def bloque(x, sx, otro, so):
        v = ventajas(x, sx, otro, so)
        if v:
            motivo = v[0][0]
            li = "\n".join(f"      <li>{t}</li>" for _, t in v[:4])
        else:
            motivo = "si lo encuentras más barato"
            li = (f"      <li>Frente al {esc(corto(otro['name']))} no tiene ninguna ventaja clara en los datos: "
                  "solo compensa con una buena oferta.</li>")
        compra = (f'\n      <a class="link amazon" href="{esc(amazon_url(x), True)}" '
                  f'rel="sponsored nofollow noopener" target="_blank">Ver precio en Amazon →</a>'
                  if AMAZON_TAG else "")
        return f"""  <h2>Elige el {esc(corto(x['name']))} {motivo}</h2>

  <ul>
{li}
  </ul>

  <div class="duelo">
    <div class="par"><a class="link" href="../portatil/{x['slug']}.html">Ficha del {esc(x['name'])} →</a>{compra}</div>
  </div>
"""

    otras = []
    for sa_, sb_ in VS_PAIRS:
        if (sa_, sb_) == (a["slug"], b["slug"]):
            continue
        por = {x["slug"]: x for x in laptops}
        xa, xb = por[sa_], por[sb_]
        otras.append(f'    <li><a href="{vs_slug(xa, xb)}.html">{esc(corto(xa["name"]))} vs {esc(corto(xb["name"]))}</a></li>')
    otras = "\n".join(otras[:5])

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            organizacion_ld(),
            {
                "@type": "Article",
                "@id": f"{url}#articulo",
                "headline": f"{ca} vs {cb}: diferencias y cuál comprar",
                "description": desc,
                "image": f"{SITE}img/og/default.jpg",
                "datePublished": "2026-11-08",
                "dateModified": hoy.isoformat(),
                "inLanguage": "es",
                "author": {"@id": f"{SITE}#organizacion"},
                "publisher": {"@id": f"{SITE}#organizacion"},
                "mainEntityOfPage": url,
                # «Thing» y no «Product»: Google exige offers, review o aggregateRating
                # en cada Product, y la comparativa no los tiene (la reseña está en
                # la ficha de cada modelo).
                "about": [
                    {"@type": "Thing", "name": na, "url": f"{SITE}portatil/{a['slug']}.html"},
                    {"@type": "Thing", "name": nb, "url": f"{SITE}portatil/{b['slug']}.html"},
                ],
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{url}#migas",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
                    {"@type": "ListItem", "position": 2, "name": "Comparativas",
                     "item": f"{SITE}#comparativas"},
                    {"@type": "ListItem", "position": 3, "name": f"{ca} vs {cb}", "item": url},
                ],
            },
        ],
    }
    pie = AVISO_AFILIADO if AMAZON_TAG else PIE_SIN

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
<meta property="og:type" content="article" />
<meta property="og:site_name" content="ComparaPortátil" />
<meta property="og:locale" content="es_ES" />
<meta property="og:title" content="{esc(ca, True)} vs {esc(cb, True)}" />
<meta property="og:description" content="{esc(desc, True)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE}img/og/default.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
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
      <a href="../#comparativas">Comparativas</a>
      <a href="../#guias">Guías</a>
    </div>
    <a href="../" class="nav-spacer" style="font-size:13.5px;font-weight:600;">Volver al inicio</a>
  </div>
</nav>

<header class="hero wrap read">
  <nav class="crumbs" aria-label="Ruta de navegación">
    <a href="../">Inicio</a>
    <span class="sep" aria-hidden="true">›</span>
    <a href="../#comparativas">Comparativas</a>
    <span class="sep" aria-hidden="true">›</span>
    <span aria-current="page">{esc(ca)} vs {esc(cb)}</span>
  </nav>
  <div class="kicker">Comparativa</div>
  <h1>{esc(ca)} vs {esc(cb)}</h1>
  <div class="meta">
    <span>Actualizada el {fecha_larga(hoy)}</span>
    <span>·</span>
    <span>precios orientativos</span>
  </div>
</header>

<article class="wrap read">

  <div class="callout">
    <strong>Respuesta rápida.</strong> {esc(rapida)}
  </div>
{compra_vs(a, b)}
  <h2>Especificaciones lado a lado</h2>

  <div class="table-wrap vs-table">
    <table>
      <thead>
        <tr><th></th><th>{esc(ca)}</th><th>{esc(cb)}</th></tr>
      </thead>
      <tbody>
{tabla}
      </tbody>
    </table>
  </div>
  <p class="caption">En azul, el mejor dato de cada fila cuando la diferencia es clara. Autonomía según el fabricante; las notas son las del comparador (0 a 100).</p>

{bloque(a, sa, b, sb)}
{bloque(b, sb, a, sa)}
  <div class="cta">
    <h2>Compáralos con tu perfil</h2>
    <p>En el comparador puedes cambiar el perfil de uso y ver cómo cambia el resultado.</p>
    <a class="btn" href="../?a={a['id']}&amp;b={b['id']}#comparador">Abrir el comparador</a>
  </div>

  <h2>Otras comparativas</h2>

  <ul>
{otras}
  </ul>

</article>

<footer>
  <div class="wrap foot">
    <span><b>ComparaPortátil</b> · Comparativa con precios orientativos de referencia; varían según tienda y disponibilidad. {pie}</span>
    <span><a href="../">Inicio</a> · <a href="../#comparativas">Comparativas</a> · <a href="../#guias">Guías</a> · <a href="../metodologia.html">Metodología</a> · <a href="../contacto.html">Contacto</a></span>
  </div>
</footer>

</body>
</html>
"""


def comparativas_html(laptops):
    """Lista de comparativas para la portada (entre marcadores)."""
    por = {x["slug"]: x for x in laptops}
    items = []
    for sa, sb in VS_PAIRS:
        a, b = por[sa], por[sb]
        items.append(f'      <li><a href="vs/{vs_slug(a, b)}.html">{esc(corto(a["name"]))} '
                     f'<span>vs</span> {esc(corto(b["name"]))}</a></li>')
    return "\n".join(items)


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
    elif price_rank > len(laptops) - 4:
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
        texto = "mismo precio" if delta == 0 else f"{signo}{eur(abs(delta))}"
        alts.append(
            f'    <li><a href="{x["slug"]}.html">{esc(x["name"])}</a>'
            f'<span class="delta">{texto}</span></li>'
        )
    alts = "\n".join(alts)

    pie_afiliado = AVISO_AFILIADO if AMAZON_TAG else PIE_SIN

    extra = ""
    guias = []
    if l["price"] <= 800 or scores["estudio"] >= 85:
        guias.append(('<li><a href="../guias/mejor-portatil-estudiar.html">'
                      'Mejor portátil para estudiar por menos de 800 €</a></li>'))
    if scores["gaming"] >= 60:
        guias.append(('<li><a href="../guias/portatil-gaming-1000-euros.html">'
                      'Portátil gaming por menos de 1.100 €</a></li>'))
    if l["os"] == "macOS" or slug in MAC_O_WINDOWS:
        guias.append(('<li><a href="../guias/macbook-o-windows.html">'
                      'MacBook o Windows: cuál elegir según tu presupuesto</a></li>'))
    if l["weight"] < 1.4:
        guias.append(('<li><a href="../guias/portatil-ligero.html">'
                      'Mejor portátil ligero por menos de 1,4 kg</a></li>'))
    if guias:
        extra = ('\n  <h2>Guías relacionadas</h2>\n\n  <ul>\n    '
                 + "\n    ".join(guias) + "\n  </ul>\n")

    # Contenido propio de la ficha.
    fuertes, debiles = puntos(l, laptops)
    li_f = "\n".join(f"    <li>{t}</li>" for t in fuertes)
    li_d = "\n".join(f"    <li>{t}</li>" for t in debiles)
    puntos_html = f"""
  <h2>Puntos fuertes y débiles</h2>

  <div class="pros-cons">
    <div>
      <h3>A favor</h3>
      <ul>
{li_f}
      </ul>
    </div>
    <div>
      <h3>En contra</h3>
      <ul>
{li_d}
      </ul>
    </div>
  </div>
"""
    rv = rival_de(l, laptops)
    comparativas = vs_de(l, laptops)
    vs_rival = next((s for o, s in comparativas if o["id"] == rv["id"]), None)
    rs = rv["scores"]
    k = best
    enlace_vs = (f' <a href="../vs/{vs_rival}.html">Ver la comparativa completa</a>.'
                 if vs_rival else "")
    rival_html = f"""
  <h2>Rival directo: {esc(rv['name'])}</h2>

  <p>Es el modelo del catálogo más cercano en precio que también destaca para {VERB[k]}.{enlace_vs}</p>

  <div class="table-wrap">
    <table>
      <thead>
        <tr><th></th><th>{esc(name)}</th><th><a href="{rv['slug']}.html">{esc(rv['name'])}</a></th></tr>
      </thead>
      <tbody>
        <tr><th scope="row">Precio</th><td>{eur(l['price'])}</td><td>{eur(rv['price'])}</td></tr>
        <tr><th scope="row">Peso</th><td>{kg(l['weight'])}</td><td>{kg(rv['weight'])}</td></tr>
        <tr><th scope="row">Autonomía</th><td>{horas(l)}</td><td>{horas(rv)}</td></tr>
        <tr><th scope="row">Nota para {VERB[k]}</th><td>{scores[k]} / 100</td><td>{rs[k]} / 100</td></tr>
        <tr><th scope="row">Nota global</th><td>{overall(l)} / 100</td><td>{overall(rv)} / 100</td></tr>
      </tbody>
    </table>
  </div>
"""
    qs = preguntas(l)
    faq_bloque = f"\n  <h2>Preguntas frecuentes</h2>\n\n{faq_html(qs)}\n"
    if comparativas:
        extra += ('\n  <h2>Comparativas</h2>\n\n  <ul>\n    '
                  + "\n    ".join(f'<li><a href="../vs/{s}.html">{esc(corto(name))} vs {esc(corto(o["name"]))}</a></li>'
                                  for o, s in comparativas)
                  + "\n  </ul>\n")

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
                # No hay oferta de venta: el precio es orientativo y el sitio no
                # vende ni gestiona envíos o devoluciones. La valoración es la
                # reseña editorial que se ve en «Para quién es».
                "review": {
                    "@type": "Review",
                    "author": {
                        "@type": "Organization",
                        "name": "ComparaPortátil",
                        "url": SITE,
                    },
                    "reviewRating": {
                        "@type": "Rating",
                        "ratingValue": str(overall(l)),
                        "bestRating": "100",
                        "worstRating": "0",
                    },
                    "reviewBody": parrafo,
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
            faq_ld(qs, url),
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
  <p class="lead">{esc(lead)}</p>{compra_arriba(l)}
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
{puntos_html}{compra_html(l)}
  <h2>Notas por uso</h2>

  <p class="caption">Escala de 0 a 100. En el comparador se recalculan según el perfil que elijas.
  La nota global es <strong>{overall(l)} / 100</strong>, la media de los cuatro apartados.</p>

  <div class="bars">
{bars}
  </div>

  <h2>Alternativas por precio</h2>

  <p>Los tres modelos del catálogo que más se acercan a su precio:</p>

  <ul class="alts">
{alts}
  </ul>
{rival_html}{faq_bloque}
  <div class="cta">
    <h2>Compáralo con otro modelo</h2>
    <p>Abre el comparador con este portátil ya cargado y enfréntalo a cualquiera de los {len(laptops)}.</p>
    <a class="btn" href="../?a={l['id']}#comparador">Abrir el comparador</a>
  </div>
{extra}
</article>

<footer>
  <div class="wrap foot">
    <span><b>ComparaPortátil</b> · Precios orientativos de referencia: varían según tienda y disponibilidad, y algún modelo puede estar descatalogado. Fotografía de producto del fabricante, usada con fines informativos. {pie_afiliado}</span>
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
            (f"{SITE}guias/portatil-ligero.html", "0.8"),
            (f"{SITE}guias/macbook-o-windows.html", "0.8"),
            (f"{SITE}metodologia.html", "0.6"),
            (f"{SITE}sobre.html", "0.5"),
            (f"{SITE}contacto.html", "0.4")]
    urls += [(f"{SITE}portatil/{l['slug']}.html", "0.7") for l in laptops]
    por = {l["slug"]: l for l in laptops}
    urls += [(f"{SITE}vs/{vs_slug(por[a], por[b])}.html", "0.7") for a, b in VS_PAIRS]
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
# Guías: enlace de compra junto a cada «Ficha del …» y aviso en el pie
# --------------------------------------------------------------------------

PIE_SIN = "Sin anuncios ni enlaces de afiliado."
RE_GUIA_LINK = re.compile(
    r'(<a class="link" href="\.\./portatil/([a-z0-9-]+)\.html">[^<]*</a>)'
    r'(\s*<a class="link amazon"[^>]*>[^<]*</a>)?')


def patch_guias(laptops):
    """Añade (o quita, si no hay tag) el enlace a Amazon en las guías. Es idempotente."""
    por_slug = {l["slug"]: l for l in laptops}
    for guia in sorted((ROOT / "guias").glob("*.html")):
        texto = guia.read_text(encoding="utf-8")

        def enlace(m):
            l = por_slug.get(m.group(2))
            if not AMAZON_TAG or l is None:
                return m.group(1)
            return (m.group(1) + "\n      "
                    f'<a class="link amazon" href="{esc(amazon_url(l), True)}" '
                    f'rel="sponsored nofollow noopener" target="_blank">Ver precio en Amazon →</a>')

        nuevo = RE_GUIA_LINK.sub(enlace, texto)
        if AMAZON_TAG:
            nuevo = nuevo.replace(PIE_SIN, AVISO_AFILIADO)
        else:
            nuevo = nuevo.replace(AVISO_AFILIADO, PIE_SIN)
        if nuevo != texto:
            guia.write_text(nuevo, encoding="utf-8", newline="\n")


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
    source = patch_between(source, "<!-- comparativas:inicio -->", "<!-- comparativas:fin -->",
                           comparativas_html(laptops))
    source = actualizar_conteos(source, laptops)
    # El comparador de la portada usa el mismo tag de afiliado.
    source, n = re.subn(r'const AMAZON_TAG = "[^"]*";', f'const AMAZON_TAG = "{AMAZON_TAG}";', source)
    if n != 1:
        raise SystemExit("No encuentro const AMAZON_TAG en index.html")
    INDEX.write_text(source, encoding="utf-8", newline="\n")

    # Comparativas A vs B
    por = {l["slug"]: l for l in laptops}
    VS_DIR = ROOT / "vs"
    VS_DIR.mkdir(exist_ok=True)
    for sa, sb in VS_PAIRS:
        a, b = por[sa], por[sb]
        (VS_DIR / f"{vs_slug(a, b)}.html").write_text(
            build_vs(a, b, laptops, hoy), encoding="utf-8", newline="\n")

    # Fichas
    FICHAS_DIR.mkdir(parents=True, exist_ok=True)
    for l in laptops:
        (FICHAS_DIR / f"{l['slug']}.html").write_text(
            build_ficha(l, laptops, hoy), encoding="utf-8", newline="\n")

    patch_guias(laptops)

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
