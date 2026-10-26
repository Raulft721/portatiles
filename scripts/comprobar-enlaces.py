#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprueba enlaces y recursos locales de las páginas del sitio."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent

PAGES = sorted(ROOT.glob("*.html")) \
    + sorted((ROOT / "guias").glob("*.html")) \
    + sorted((ROOT / "portatil").glob("*.html"))

ATTR = re.compile(r'(?:href|src)="([^"]+)"')


def resolve(page: Path, target: str):
    if target.startswith(("http://", "https://", "mailto:", "data:", "#", "//")):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    if target.startswith("/"):
        return ROOT / target.lstrip("/")
    return (page.parent / unquote(target)).resolve()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    missing = []
    total = 0
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        for target in ATTR.findall(text):
            if "${" in target or "&" in target:
                continue
            path = resolve(page, target)
            if path is None:
                continue
            total += 1
            if not path.exists():
                missing.append((page.relative_to(ROOT), target, path.relative_to(ROOT) if str(path).startswith(str(ROOT)) else path))

    print(f"{len(PAGES)} páginas, {total} referencias locales revisadas")
    if missing:
        print(f"\n{len(missing)} enlaces rotos:")
        for page, target, dest in missing:
            print(f"  {page}: {target}  ->  {dest}")
        sys.exit(1)
    print("Sin enlaces rotos")


if __name__ == "__main__":
    main()
