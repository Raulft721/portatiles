#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Avisa a IndexNow (Bing, Yandex y otros) de las URLs del sitemap.

Hay que ejecutarlo DESPUÉS de publicar los cambios con git push, porque
IndexNow rastrea la URL en vivo y necesita encontrar la clave en la raíz
del sitio: https://raulft721.github.io/portatiles/<CLAVE>.txt

Uso:
    python scripts/indexnow.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAVE = "9f2b7c41d8a64e0fba3517c9d24e6b83"
HOST = "raulft721.github.io"
ENDPOINT = "https://api.indexnow.org/indexnow"


def urls_del_sitemap() -> list[str]:
    xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if not (ROOT / f"{CLAVE}.txt").exists():
        raise SystemExit(f"Falta el archivo de clave {CLAVE}.txt en la raíz del sitio")

    urls = urls_del_sitemap()
    cuerpo = json.dumps({
        "host": HOST,
        "key": CLAVE,
        "keyLocation": f"https://{HOST}/portatiles/{CLAVE}.txt",
        "urlList": urls,
    }).encode("utf-8")

    peticion = urllib.request.Request(
        ENDPOINT,
        data=cuerpo,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(peticion, timeout=30) as respuesta:
            print(f"IndexNow: {respuesta.status} ({len(urls)} URLs enviadas)")
    except urllib.error.HTTPError as error:
        print(f"IndexNow respondió {error.code}: {error.read()[:200]!r}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
