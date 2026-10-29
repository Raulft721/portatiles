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
- [x] Sustituir el `Offer` por una `Review` editorial en las 34 fichas, para no declarar
  envíos ni devoluciones que el sitio no gestiona (29/10/2026, commit `d50f636`).
- [x] Mostrar la nota global (`N / 100`) en la ficha, para que coincida con el
  `reviewRating` del JSON-LD (29/10/2026).
- [x] Revalidar en Rich Results Test: Producto, Migas y Reseñas válidos, sin avisos
  críticos ni no críticos (29/10/2026).
- [x] Cambiar los enlaces internos de `index.html` a `./` y `../` para no crear una URL
  duplicada de la portada (29/10/2026).
- [x] Añadir `scripts/auditar-seo.py` y documentar su uso (29/10/2026).
- [x] Confirmar que Search Console está configurada con la propiedad de prefijo
  `https://raulft721.github.io/portatiles/` y anotar la línea base: 0 clics, 3
  impresiones, CTR 0 %, posición media 38 (27/10/2026).
- [ ] Abrir **Search Console → Indexación → Páginas**, filtrar por «No indexada» y anotar
  el motivo exacto y las URLs afectadas de los correos. Sin ese dato solo se pueden
  descartar causas técnicas.
- [ ] Confirmar que el sitemap enviado es
  `https://raulft721.github.io/portatiles/sitemap.xml` (no el de la raíz del host).
- [ ] Reenviar `sitemap.xml` en Search Console después de publicar esta versión.
- [x] Pedir **Validar corrección** en el informe de indexación (29/10/2026).
- [x] Solicitar indexación de las páginas principales con **Inspeccionar URL → Solicitar
  indexación** (29/10/2026).
- [ ] En **Mejoras → Fichas de comerciantes** y **Fragmentos de productos**, pulsar
  **Validar corrección** tras el cambio a `Review` y comprobar en 2–4 semanas que los
  avisos han desaparecido.
- [ ] Inspeccionar una o dos URLs afectadas con «Inspeccionar URL» y comprobar que
  Google ve la versión nueva (canonical y contenido).
- [ ] Volver a revisar la indexación el **12/11/2026** (2 semanas) y el **26/11/2026**
  (4 semanas).
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

### Seguimiento de la validación

- **29/10/2026**: validación solicitada y varias URLs enviadas a indexar.
- **3–5/11/2026**: mirar el estado en el informe. Puede seguir «Iniciada»; es normal.
  - «Correcta»: Google acepta que el problema está resuelto, pero **no** garantiza que
    todas las URLs se indexen.
  - «Fallida»: el informe dirá qué URLs siguen mal; revisarlas una a una.
- **12/11/2026** y **26/11/2026**: revisar «Indexación → Páginas».
- No volver a pulsar «Validar corrección» mientras esté en curso. No acelera nada y
  reinicia la espera.
- «Solicitar indexación» tiene un cupo diario. No repetir la misma URL cada día.

## Medición — antes de invertir en dominio

- [ ] Revisar **Search Console → Rendimiento** el **28/11/2026**, **28/12/2026** y
  **27/01/2027** (30, 60 y 90 días).
- [ ] Revisar **Indexación → Páginas** y anotar cuántas URLs están indexadas y cuántas
  no, con su motivo.
- [ ] Anotar clics, impresiones, CTR, posición media y consultas principales.
- [ ] Localizar páginas sin impresiones (contenido o enlazado) y páginas con clics
  (candidatas a ampliar).
- [ ] Decidir si se compra dominio con los criterios de [[Contexto/Medicion|Medición]].
- [x] Evaluar Vercel frente a GitHub Pages: no migrar ahora (29/10/2026). Ver
  [[Contexto/Hosting|Hosting]].
- [ ] Revisar la decisión de hosting cuando haya dominio, tráfico o una necesidad
  técnica (funciones, redirecciones, cabeceras).
- [ ] Opcional: añadir analítica sin cookies si se quiere el total de visitas, no solo
  las de Google.

## Prioridad alta — profesionalización y AdSense

Plan detallado en [[Mejoras/Plan|Plan de profesionalización]]. Bloqueantes en
[[Mejoras/AdSense|AdSense]] y obligaciones en [[Mejoras/Legal|Legal]].

- [ ] Decidir el dominio propio **cuando los datos de tráfico lo justifiquen** (o antes
  de AdSense, por `ads.txt`; como mínimo, crear el repo `Raulft721.github.io` para
  servirlo en la raíz).
- [ ] Crear aviso legal, privacidad, cookies y términos, y enlazarlos en el pie de todas
  las páginas ([[Mejoras/Legal|Legal]]).
- [ ] Activar el CMP de Google y probar aceptar, rechazar y cambiar de opinión.
- [ ] Sustituir los textos «sin anuncios» de portada, sobre, metodología, contacto,
  guías y fichas (incluido `scripts/generar.py`).
- [ ] Página de autor y política editorial.
- [ ] Ampliar 10 fichas a 700–900 palabras y escribir 4 comparativas.
- [ ] Eliminar el correo personal de los commits futuros (usar el noreply de GitHub).
- [ ] Añadir `_config.yml` para no publicar `notas/` ni `scripts/` ([[Mejoras/Seguridad|Seguridad]]).
- [ ] Revisar la licencia de las fotos de fabricante.
- [ ] Solicitar AdSense solo cuando la checklist de [[Mejoras/AdSense|AdSense]] esté
  completa.

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
- [x] Volver a ejecutar `python scripts/auditar-seo.py --live` con la versión de datos
  estructurados publicada: sin errores (29/10/2026).
- [ ] Ejecutar `python scripts/generar.py` y `scripts/og.ps1` solo cuando cambien
  modelos o imágenes sociales.
- [x] Ejecutar `python scripts/indexnow.py` cuando GitHub Pages ya sirve la versión nueva
  (29/10/2026, 200 OK con 40 URLs).
- [ ] Revisar Search Console: sitemap, indexación y posibles acciones manuales.
- [ ] Mantener el diario del vault al terminar cada sesión.

## Ideas para más adelante

Todo el detalle está en [[Mejoras/Plan|Plan de profesionalización]].

- [ ] Buscador por nombre o marca y filtros por precio, peso y RAM.
- [ ] Comparar tres modelos y copiar el enlace de la comparación.
- [ ] Añadir un pequeño resumen de «mejor por presupuesto» en la portada.
- [ ] Enlazar cada ficha con su comparativa directa.
- [ ] Páginas de categoría con contenido propio, no solo listados.
- [ ] Medir rendimiento con Lighthouse y corregir el contraste de `.pill` y `.score`.

## Historial

- **29/10/2026**: auditoría completa, enlaces internos corregidos, script de auditoría
  y creación de este vault. Después, datos estructurados corregidos: `Offer` fuera y
  `Review` editorial en su lugar. Revisión de seguridad (sin claves ni APIs expuestas) y
  plan de profesionalización y AdSense. Ver [[Diario/2026-10-29]].
