#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audita la salud SEO del sitio antes de publicar.

Comprueba que el sitemap y las páginas coinciden, que cada página indexable
tiene los metadatos mínimos y que los datos estructurados parsean. Con --live
además consulta las URLs publicadas y verifica que respondan 200 sin
redirecciones ni canonical distinto.

Uso:
    python scripts/auditar-seo.py
    python scripts/auditar-seo.py --live

No modifica ningún archivo. Sale con código 1 si encuentra errores.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from generar import SITE, parse_laptops  # noqa: E402

INDEX = ROOT / "index.html"
SITEMAP = ROOT / "sitemap.xml"
ROBOTS = ROOT / "robots.txt"
NOT_FOUND = ROOT / "404.html"

TITLE_MAX = 65
DESC_MIN = 60
DESC_MAX = 165
UA = "ComparaPortatil-SEO-Audit/1.0"


def load_laptops():
    return parse_laptops(INDEX.read_text(encoding="utf-8"))


def expected_pages(laptops):
    """URL publicada -> archivo local, solo para páginas indexables."""
    pages = {
        SITE: INDEX,
        f"{SITE}guias/mejor-portatil-estudiar.html": ROOT / "guias" / "mejor-portatil-estudiar.html",
        f"{SITE}guias/portatil-gaming-1000-euros.html": ROOT / "guias" / "portatil-gaming-1000-euros.html",
        f"{SITE}metodologia.html": ROOT / "metodologia.html",
        f"{SITE}sobre.html": ROOT / "sobre.html",
        f"{SITE}contacto.html": ROOT / "contacto.html",
    }
    for laptop in laptops:
        pages[f"{SITE}portatil/{laptop['slug']}.html"] = ROOT / "portatil" / f"{laptop['slug']}.html"
    return pages


def first(pattern, text, flags=re.S):
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else None


def local_path_from_url(url):
    if not url.startswith(SITE):
        return None
    relative = url[len(SITE):]
    if relative == "":
        return INDEX
    return ROOT / relative


def audit_page(url, path, title_seen, desc_seen):
    errors, warnings = [], []
    if not path.exists():
        return [f"{url}: falta el archivo {path.relative_to(ROOT)}"], []

    text = path.read_text(encoding="utf-8")
    title = first(r"<title>(.*?)</title>", text)
    desc = first(r'<meta name="description" content="(.*?)"', text)
    robots = first(r'<meta name="robots" content="(.*?)"', text)
    canonical = first(r'<link rel="canonical" href="(.*?)"', text)
    lang = first(r'<html[^>]+lang="([^"]+)"', text)
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", text, re.S)

    if not title:
        errors.append(f"{url}: sin <title>")
    else:
        if len(title) > TITLE_MAX:
            warnings.append(f"{url}: título de {len(title)} caracteres (máximo recomendado {TITLE_MAX})")
        if title in title_seen:
            errors.append(f"{url}: título duplicado con {title_seen[title]}")
        title_seen[title] = url

    if not desc:
        errors.append(f"{url}: sin meta description")
    else:
        if not (DESC_MIN <= len(desc) <= DESC_MAX):
            warnings.append(f"{url}: meta description de {len(desc)} caracteres (recomendado {DESC_MIN}-{DESC_MAX})")
        if desc in desc_seen:
            errors.append(f"{url}: meta description duplicada con {desc_seen[desc]}")
        desc_seen[desc] = url

    if not robots or "noindex" in robots:
        errors.append(f"{url}: no es indexable (robots: {robots or 'sin etiqueta'})")
    elif "index" not in robots:
        errors.append(f"{url}: la etiqueta robots no permite indexar ({robots})")

    if canonical != url:
        errors.append(f"{url}: canonical incorrecto ({canonical or 'sin canonical'})")

    if lang != "es":
        errors.append(f"{url}: idioma del documento ({lang or 'sin lang'})")

    if len(h1s) != 1:
        errors.append(f"{url}: {len(h1s)} etiquetas h1 (debe haber una)")

    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"{url}: JSON-LD no válido ({exc})")

    if re.search(r'href="(?:\.\./)?index\.html', text):
        warnings.append(f"{url}: enlace interno a index.html; usa ./ o ../ para no crear una URL duplicada")

    image = first(r'<meta property="og:image" content="(.*?)"', text)
    if image:
        image_path = local_path_from_url(image)
        if image_path and not image_path.exists():
            errors.append(f"{url}: og:image no existe ({image})")

    return errors, warnings


def audit_sitemap(pages):
    errors, warnings = [], []
    if not SITEMAP.exists():
        return ["falta sitemap.xml"], []
    text = SITEMAP.read_text(encoding="utf-8")
    locs = re.findall(r"<loc>(.*?)</loc>", text)
    if len(locs) != len(set(locs)):
        errors.append("sitemap.xml contiene URLs repetidas")

    expected = set(pages)
    found = set(locs)
    for url in sorted(expected - found):
        errors.append(f"sitemap.xml: falta {url}")
    for url in sorted(found - expected):
        errors.append(f"sitemap.xml: URL no indexable o inexistente {url}")

    for url in locs:
        path = local_path_from_url(url)
        if path is None:
            warnings.append(f"sitemap.xml: URL fuera del sitio {url}")
        elif not path.exists():
            errors.append(f"sitemap.xml: el archivo local no existe para {url}")

    lastmods = re.findall(r"<lastmod>(.*?)</lastmod>", text)
    for value in lastmods:
        try:
            parsed = date.fromisoformat(value)
        except ValueError:
            errors.append(f"sitemap.xml: lastmod inválido ({value})")
            continue
        if parsed > date.today():
            warnings.append(f"sitemap.xml: lastmod futuro ({value})")

    return errors, warnings


def audit_not_found():
    errors, warnings = [], []
    if not NOT_FOUND.exists():
        return ["falta 404.html"], []
    text = NOT_FOUND.read_text(encoding="utf-8")
    robots = first(r'<meta name="robots" content="(.*?)"', text)
    if not robots or "noindex" not in robots:
        errors.append("404.html debe llevar noindex")
    if not first(r"<title>(.*?)</title>", text):
        warnings.append("404.html no tiene título")
    return errors, warnings


def audit_robots():
    errors, warnings = [], []
    if not ROBOTS.exists():
        return ["falta robots.txt"], []
    text = ROBOTS.read_text(encoding="utf-8")
    if "Sitemap:" not in text:
        warnings.append("robots.txt no incluye la línea Sitemap:")
    if "Disallow: /" in text:
        errors.append("robots.txt bloquea todo el sitio")
    return errors, warnings


def live_check(pages, timeout, base):
    errors, warnings = [], []
    for url in sorted(pages):
        live_url = base + url[len(SITE):] if url.startswith(SITE) else url
        request = urllib.request.Request(live_url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                status = response.status
                final = response.geturl()
                body = response.read(200_000).decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            errors.append(f"{live_url}: HTTP {exc.code}")
            continue
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{live_url}: no se pudo consultar ({exc})")
            continue

        if status != 200:
            errors.append(f"{live_url}: HTTP {status}")
        if final != live_url:
            warnings.append(f"{live_url}: redirige a {final}")
        canonical = first(r'<link rel="canonical" href="(.*?)"', body)
        if canonical != url:
            errors.append(f"{live_url}: canonical distinto ({canonical or 'sin canonical'})")
    return errors, warnings


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Audita el SEO técnico del sitio.")
    parser.add_argument("--live", action="store_true", help="consulta también las URLs publicadas")
    parser.add_argument(
        "--base",
        default=SITE,
        help="URL base para --live (por ejemplo, http://127.0.0.1:8000/)",
    )
    parser.add_argument("--timeout", type=int, default=20, help="timeout por petición en segundos")
    args = parser.parse_args()
    base = args.base if args.base.endswith("/") else args.base + "/"

    laptops = load_laptops()
    pages = expected_pages(laptops)

    errors, warnings = [], []
    title_seen, desc_seen = {}, {}
    for url, path in sorted(pages.items()):
        page_errors, page_warnings = audit_page(url, path, title_seen, desc_seen)
        errors += page_errors
        warnings += page_warnings

    for name, result in (
        ("sitemap", audit_sitemap(pages)),
        ("404", audit_not_found()),
        ("robots", audit_robots()),
    ):
        errors += result[0]
        warnings += result[1]

    if args.live:
        live_errors, live_warnings = live_check(pages, args.timeout, base)
        errors += live_errors
        warnings += live_warnings

    print(f"Auditoría SEO — {date.today().isoformat()}")
    print(f"Portátiles en el catálogo: {len(laptops)}")
    print(f"Páginas indexables: {len(pages)}")
    print(f"Sitemap: {len(re.findall(r'<loc>', SITEMAP.read_text(encoding='utf-8')))} URLs")
    print(f"Modo en vivo: {'sí (' + base + ')' if args.live else 'no'}")
    print()

    if warnings:
        print(f"ADVERTENCIAS ({len(warnings)})")
        for item in warnings:
            print(f"  · {item}")
        print()

    if errors:
        print(f"ERRORES ({len(errors)})")
        for item in errors:
            print(f"  ✗ {item}")
        print("\nLa auditoría ha fallado.")
        sys.exit(1)

    print("Sin errores de SEO técnico.")


if __name__ == "__main__":
    main()
