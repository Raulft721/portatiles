---
tipo: contexto
actualizado: 2026-10-29
tags:
  - comparaportatil
  - publicacion
---

# Publicación

## Flujo completo

```powershell
python scripts/generar.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/og.ps1
python scripts/comprobar-enlaces.py
python scripts/auditar-seo.py
git status
git add -A
git commit -m "…"
git push origin main
```

Después de que GitHub Pages sirva la versión nueva:

```powershell
python scripts/auditar-seo.py --live
python scripts/indexnow.py
```

## Qué hace cada paso

- `generar.py`: crea `portatil/*.html`, las tarjetas del catálogo, el ItemList, el
  `sitemap.xml` y `scripts/og-manifest.json`. También reescribe los contadores del HTML.
- `og.ps1`: genera las imágenes sociales de `img/og/` a partir del manifiesto. Solo hace
  falta si cambian modelos, precios o textos de las tarjetas.
- `comprobar-enlaces.py`: valida las páginas y todos los recursos locales.
- `auditar-seo.py`: comprueba sitemap, canonical, metadatos y JSON-LD. Con `--live`
  comprueba además que las 40 URLs publicadas respondan 200.
- `indexnow.py`: envía las URLs del sitemap a IndexNow (Bing, Yandex y otros). **No es
  Google**; Google se gestiona desde Search Console.

## Avisos

- `og.ps1` **debe conservar el BOM UTF-8**. Si se guarda sin BOM, los acentos salen mal.
- No editar a mano los bloques generados de `index.html`:
  `<!-- catalogo:inicio --> … <!-- catalogo:fin -->` y
  `<!-- itemlist:inicio --> … <!-- itemlist:fin -->`.
- Tampoco editar a mano los contadores («Compara N portátiles», «N portátiles de M
  marcas»): los reescribe `generar.py`.
- Revisar el resultado antes de publicar: enlaces, JSON-LD y diseño.
- Si Pages tarda, esperar y comprobar la URL publicada antes de lanzar IndexNow.

## Comprobaciones después de publicar

```powershell
python scripts/auditar-seo.py --live
```

Y en el navegador:

- Portada: <https://raulft721.github.io/portatiles/>
- Una ficha nueva: abrir su URL y comprobar que el canonical es el `.html`.
- Sitemap: <https://raulft721.github.io/portatiles/sitemap.xml>
- 404: una URL inexistente debe devolver 404 y mostrar la página propia.

## Revertir

Si algo sale mal, `git revert <commit>` y volver a publicar. No reescribir la historia
de `main` si ya está desplegada.

## Hosting

GitHub Pages se queda por ahora. La comparación con Vercel y Cloudflare Pages está en
[[Contexto/Hosting|Hosting]]; no se migra sin dominio y sin una necesidad técnica que lo
justifique.
