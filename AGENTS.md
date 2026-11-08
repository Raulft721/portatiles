# ComparaPortátil — instrucciones del proyecto

Comparador de portátiles en español, estático y sin backend. Se publica en GitHub Pages.

- Web: https://raulft721.github.io/portatiles/
- Repo: https://github.com/Raulft721/portatiles (rama `main`)
- Local: `python -m http.server 8000 --bind 127.0.0.1` y abrir http://127.0.0.1:8000
- Search Console: propiedad de prefijo `https://raulft721.github.io/portatiles/`, verificada.
  Línea base del 27/10/2026: 0 clics, 3 impresiones, CTR 0 %, posición media 38. No sirve
  para decidir todavía; el detalle está en `notas/Contexto/Medicion.md`.

## Contexto y tareas

El vault de Obsidian de `notas/` es contexto antiguo: se puede consultar si hace falta,
pero **no hay que actualizarlo** (ni tareas, ni diario, ni registro de cambios).

**`notas/` es privado y no se versiona.** Está en `.gitignore`: no añadirlo al repo ni
forzarlo con `git add -f`. Se queda solo en el equipo del autor. El contenido sigue
disponible en el historial de Git antiguo, pero no se publica ni se actualiza.

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
- Nunca poner claves, tokens ni datos personales en el repositorio: GitHub Pages publica
  todo lo que hay en `main`. El sitio es estático y no debe llamar a APIs con secretos
  desde el navegador.
- Las fichas **no llevan `Offer`**: el sitio no vende, así que no puede declarar precio,
  envíos ni devoluciones. En su lugar llevan una `Review` editorial (nota global como
  `reviewRating` y el párrafo «Para quién es» como `reviewBody`). No añadir
  `aggregateRating` sin reseñas reales.

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
python scripts/auditar-seo.py
```

- `generar.py` crea las fichas de `portatil/`, las tarjetas del catálogo, el ItemList, el
  `sitemap.xml` y `scripts/og-manifest.json`.
- `og.ps1` genera las imágenes sociales de `img/og/` a partir del manifiesto. **Debe conservar el
  BOM UTF-8**; si se guarda sin BOM, los acentos salen mal.
- `comprobar-enlaces.py` valida las páginas y todos los recursos locales.
- `auditar-seo.py` comprueba sitemap, canonical, metadatos y JSON-LD. Con `--live` consulta las
  URLs publicadas. No modifica archivos.

Después: revisar el resultado, `git commit`, `git push origin main` y, cuando Pages ya sirva la
versión nueva, `python scripts/auditar-seo.py --live` y `python scripts/indexnow.py` (envía todas
las URLs del sitemap a IndexNow).

## Comprobaciones recomendadas

- Que las fichas nuevas y sus OG respondan 200 en local y en producción.
- Que todos los bloques `<script type="application/ld+json">` parseen y que
  `python scripts/auditar-seo.py --live` termine sin errores.
- Capturas para revisar el diseño. `browser.screenshot` falla en este entorno: usar Chrome
  headless con `--headless=new --virtual-time-budget=4000 --screenshot=...`.

## Entorno

Windows, PowerShell. Python 3.14 con Pillow y numpy; no hay Node. PowerShell muestra los acentos
como mojibake al imprimir por consola, pero los archivos están en UTF-8: no «arreglar» esos
caracteres.

## Contenido generado

- **Fichas:** además de la ficha técnica, `generar.py` calcula a partir de los datos los
  puntos fuertes y débiles, el rival directo (el más cercano en precio con el mismo uso
  principal) y tres preguntas frecuentes con su `FAQPage`. No se escriben a mano.
- **Comparativas `vs/`:** la lista de parejas está en `VS_PAIRS` de `generar.py`. Cada
  página sale de los datos (tabla, respuesta rápida y ventajas de cada modelo). Para añadir
  una, se añade la pareja y se vuelve a generar: sitemap, portada y fichas se actualizan solos.
- **Guías nuevas:** hay que añadirlas a `build_sitemap` en `generar.py` y a
  `expected_pages` en `scripts/auditar-seo.py`.

## Amazon Afiliados

El tag va en la constante `AMAZON_TAG` de `scripts/generar.py`. Con el tag puesto,
`generar.py` añade el bloque «Dónde comprarlo» a cada ficha y el enlace a Amazon en las
guías, con `rel="sponsored nofollow"` y el aviso obligatorio de afiliación. Con la
constante vacía, lo quita. Los textos fijos de `index.html`, `sobre.html`,
`metodologia.html` y `contacto.html` que dicen «sin enlaces de afiliado» se cambian a mano.
No mostrar precios «de Amazon»: los precios del sitio son orientativos y propios.

## Pendiente (manual, fuera del repo)

- Seguimiento en Search Console: la validación de indexación se pidió el 29/10 y se
  enviaron varias URLs a indexar. Comprobar el estado el 3–5/11 y la indexación el
  12/11 y el 26/11. El detalle está en `notas/Tareas.md`.
- Mantener las fotos: las de tienda se aceptan, pero siempre que se vea el producto correcto.
