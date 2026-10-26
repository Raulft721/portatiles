# ComparaPortátil — instrucciones del proyecto

Comparador de portátiles en español, estático y sin backend. Se publica en GitHub Pages.

- Web: https://raulft721.github.io/portatiles/
- Repo: https://github.com/Raulft721/portatiles (rama `main`)
- Local: `python -m http.server 8000` y abrir http://127.0.0.1:8000

## Reglas de contenido

- Todo en español, tono claro y directo. Nada de lenguaje de marketing.
- Los precios son **orientativos de referencia**. No afirmar que están verificados ni poner fecha de comprobación.
- No inventar especificaciones. Si el fabricante no publica la autonomía, el modelo lleva
  `battery: null` y `wh` con la capacidad; la ficha muestra «Sin dato del fabricante» y el
  comparador no declara ganador en esa fila.
- No borrar modelos antiguos: el catálogo es acumulativo.
- Las fotos deben ser del producto real. Preferencia: CDN del fabricante; si no hay, foto de
  tienda especializada. Formato 1000×750 JPEG, fondo blanco, sin recortes raros.
- Nada se publica sin comprobarlo antes (enlaces, JSON-LD y revisión visual).

## Dónde están los datos

El array `LAPTOPS` de `index.html` es la única fuente de verdad. Campos por modelo:

```
id, slug, img, name, brand, price
cpu, gpu, ram, storage, screen, weight
battery (horas o null), wh (capacidad), os
scores: { estudio, trabajo, gaming, movilidad }
grad (degradado de la tarjeta), aviso (texto opcional bajo la tabla)
```

No editar a mano los bloques generados de `index.html`:

```
<!-- catalogo:inicio --> ... <!-- catalogo:fin -->
<!-- itemlist:inicio --> ... <!-- itemlist:fin -->
```

Tampoco los contadores escritos en el HTML («Compara N portátiles», «N portátiles de M marcas»):
los reescribe `generar.py` a partir del catálogo real.

## Flujo tras cambiar modelos o precios

```powershell
python scripts/generar.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/og.ps1
python scripts/comprobar-enlaces.py
```

- `generar.py` crea las fichas de `portatil/`, las tarjetas del catálogo, el ItemList, el
  `sitemap.xml` y `scripts/og-manifest.json`.
- `og.ps1` genera las imágenes sociales de `img/og/` a partir del manifiesto. **Debe conservar el
  BOM UTF-8**; si se guarda sin BOM, los acentos salen mal.
- `comprobar-enlaces.py` valida las páginas y todos los recursos locales.

Después: revisar el resultado, `git commit`, `git push origin main` y, cuando Pages ya sirva la
versión nueva, `python scripts/indexnow.py` (envía las 40 URLs a IndexNow).

## Comprobaciones recomendadas

- Que las fichas nuevas y sus OG respondan 200 en local y en producción.
- Que todos los bloques `<script type="application/ld+json">` parseen (son 40).
- Capturas para revisar el diseño. `browser.screenshot` falla en este entorno: usar Chrome
  headless con `--headless=new --virtual-time-budget=4000 --screenshot=...`.

## Entorno

Windows, PowerShell. Python 3.14 con Pillow y numpy; no hay Node. PowerShell muestra los acentos
como mojibake al imprimir por consola, pero los archivos están en UTF-8: no «arreglar» esos
caracteres.

## Pendiente (manual, fuera del repo)

- Enviar `sitemap.xml` en Search Console y pedir indexación de las fichas nuevas.
- Mantener las fotos: las de tienda se aceptan, pero siempre que se vea el producto correcto.
