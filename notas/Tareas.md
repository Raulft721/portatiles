---
tipo: tareas
actualizado: 2026-10-29
tags:
  - comparaportatil
  - tareas
---

# Tareas

Checklist vivo del proyecto. Marca `- [x]` al terminar y añade la fecha si la tarea
ha necesitado investigación. Lo urgente va arriba; lo demás, en orden de prioridad.

## Prioridad alta — indexación y Search Console

- [x] Auditar las 40 URLs del `sitemap.xml` en vivo: HTTP 200 y canonical correcto
  (29/10/2026).
- [x] Comprobar que el sitemap y las páginas locales coinciden: 40 URLs, sin faltas ni
  sobrantes (29/10/2026).
- [x] Validar los datos estructurados con Rich Results Test: ficha de portátil y portada
  sin errores críticos (29/10/2026).
- [x] Cambiar los enlaces internos de `index.html` a `./` y `../` para no crear una URL
  duplicada de la portada (29/10/2026).
- [x] Añadir `scripts/auditar-seo.py` y documentar su uso (29/10/2026).
- [ ] Abrir **Search Console → Indexación → Páginas**, filtrar por «No indexada» y anotar
  el motivo exacto y las URLs afectadas de los correos. Sin ese dato solo se pueden
  descartar causas técnicas.
- [ ] Confirmar que el sitemap enviado es
  `https://raulft721.github.io/portatiles/sitemap.xml` (no el de la raíz del host).
- [ ] Reenviar `sitemap.xml` en Search Console después de publicar esta versión.
- [ ] Pedir **Validar corrección** en el informe de indexación y esperar el resultado.
- [ ] Inspeccionar una o dos URLs afectadas con «Inspeccionar URL» y comprobar que
  Google ve la versión nueva (canonical y contenido).
- [ ] Volver a revisar la indexación en 2–4 semanas.
- [ ] Opcional: crear el repositorio `Raulft721.github.io` con un `robots.txt` en la raíz
  del host. GitHub Pages no sirve el `robots.txt` de un project site en la raíz, así que
  el actual `portatiles/robots.txt` no lo lee Google; el sitemap se envía a mano.

### Si el motivo del correo es…

- **404**: comprobar que la URL listada existe y que no es una ficha antigua con otro
  slug. Si es una URL antigua, decidir entre recuperarla o dejar que el 404 siga su curso.
- **Duplicada / canonical distinto**: no tocar el canonical salvo que esté mal. Google
  puede tardar en consolidar `/sobre` y `/sobre.html`; el canonical ya apunta a `.html`.
- **Error 5xx / redirección**: volver a solicitar la indexación cuando la URL responda
  200. GitHub Pages puede devolver 5xx puntuales.
- **Rastreada, actualmente no indexada**: no es un error técnico. Revisar contenido,
  enlaces internos y autoridad; insistir con el tiempo.

## Prioridad media — contenido y catálogo

- [ ] Revisar los precios orientativos de los modelos más antiguos y añadir `aviso` si
  alguno está descatalogado.
- [ ] Revisar que todas las autonomías sin dato del fabricante sigan con `battery: null`
  y su capacidad en `wh`.
- [ ] Revisar las fotos de producto: que sea el modelo correcto, fondo blanco y sin
  recortes raros.
- [ ] Revisar títulos de más de 60 caracteres (los avisa `generar.py`).
- [ ] Revisar las fechas visibles de las guías y su `dateModified` para que coincidan.
- [ ] Añadir modelos nuevos al array `LAPTOPS` sin borrar los antiguos.
- [ ] Valorar páginas de categoría (gaming, estudiar, trabajo) si el catálogo crece.

## Publicación y mantenimiento

- [x] Ejecutar `python scripts/generar.py` tras los cambios (29/10/2026).
- [x] Ejecutar `python scripts/comprobar-enlaces.py` (29/10/2026).
- [x] Ejecutar `python scripts/auditar-seo.py --live` (29/10/2026).
- [ ] Volver a ejecutar `python scripts/auditar-seo.py --live` cuando Pages sirva la
  versión nueva.
- [ ] Ejecutar `python scripts/generar.py` y `scripts/og.ps1` solo cuando cambien
  modelos o imágenes sociales.
- [ ] Ejecutar `python scripts/indexnow.py` cuando GitHub Pages ya sirva la versión nueva.
- [ ] Revisar Search Console: sitemap, indexación y posibles acciones manuales.
- [ ] Mantener el diario del vault al terminar cada sesión.

## Ideas para más adelante

- [ ] Añadir un pequeño resumen de «mejor por presupuesto» en la portada.
- [ ] Enlazar cada ficha con la guía que le corresponda de forma más específica.
- [ ] Estudiar un dominio propio para no depender de `github.io`.
- [ ] Medir rendimiento con Lighthouse y corregir el contraste de color detectado.

## Historial

- **29/10/2026**: auditoría completa, enlaces internos corregidos, script de auditoría
  y creación de este vault. Ver [[Diario/2026-10-29]].
