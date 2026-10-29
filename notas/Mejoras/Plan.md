---
tipo: mejoras
actualizado: 2026-10-29
tags:
  - comparaportatil
  - mejoras
  - producto
  - contenido
  - seo
---

# Plan de profesionalización

Objetivo: que el sitio se lea como un proyecto editorial cuidado y no como un
prototipo, y que esté listo para monetizar sin perder la credibilidad que ya tiene.
Las tareas concretas están en [[Tareas]]; aquí está el criterio y el orden.

## Dónde estamos (29/10/2026)

| Área | Estado |
| --- | --- |
| Catálogo | 34 portátiles, 34 fichas generadas |
| Contenido | 2 guías + portada, metodología, sobre y contacto |
| Fichas | ~350 palabras cada una (mín. 328, máx. 375) |
| Stack | HTML, CSS y JS estático; sin dependencias ni build |
| Datos | array `LAPTOPS` en `index.html` |
| SEO técnico | 40 URLs, canonical, sitemap y JSON-LD correctos |
| Accesibilidad | Lighthouse 0,96; falla el contraste de `.pill` y `.score` |
| Rendimiento | 36 JPG, ~2,9 MB en total; `loading="lazy"` y dimensiones puestas |
| Legal | sin aviso legal, privacidad, cookies ni términos |
| Autoría | anónima: no hay nombre ni página de autor |
| Dominio | `raulft721.github.io/portatiles/` |
| Cookies y terceros | ninguno; solo `localStorage` con las preferencias |

## La regla de oro

Cada cambio debería responder a una de estas tres preguntas: **¿ayuda a decidir la
compra?**, **¿demuestra que hay alguien detrás?** o **¿hace más fácil usar el sitio?**.
Si no responde a ninguna, es ruido.

## P0 — imprescindible antes de AdSense

### 1. Dominio propio

**Decisión del 29/10/2026**: no comprarlo todavía. Primero se mide el tráfico con
Search Console y se decide con datos; el dominio no genera visitas por sí solo. Ver
[[Contexto/Medicion|Medición de tráfico]]. Sigue siendo imprescindible **antes de pedir
AdSense**, porque `ads.txt` tiene que estar en la raíz.

Es la mejora con más efecto sobre la percepción de seriedad y desbloquea cosas que en
GitHub Pages no se pueden hacer:

- `https://comparaportatil.es` (o el nombre que se elija) en lugar de una ruta de
  `github.io`.
- `ads.txt` en la raíz del dominio, que es donde Google lo busca.
- Correo profesional (`hola@…`) para contacto y para la cuenta de AdSense.
- Cabeceras de seguridad reales si se pone Cloudflare delante.
- Control del `robots.txt` raíz.

Al cambiar de dominio hay que actualizar `SITE` en `scripts/generar.py`, el canonical,
el sitemap, las imágenes OG y Search Console (y usar «Cambio de dirección»). Cuanto
antes se haga, menos cuesta.

### 2. Autoría y transparencia

Ahora mismo el sitio dice «proyecto personal» pero no dice quién. Para un comparador
que pide confianza (y para AdSense) conviene:

- Página **Quién escribe** con nombre, qué haces, por qué este proyecto y cómo
  contactarte. Sin currículum inflado.
- **Política editorial**: cómo se eligen los modelos, de dónde salen las notas, cómo se
  corrigen los errores, qué no se acepta (patrocinios, regalos, enlaces pagados).
- **Fuente por ficha**: enlace a la página oficial del fabricante y fecha de consulta.
  Se puede añadir un campo `fuente` al modelo de datos.
- **Historial de cambios**: al menos un registro de correcciones relevantes.
- Firma visible en las guías: «Por … · actualizado el …».

### 3. Páginas legales

Detalle en [[Mejoras/Legal|Legal]]. Como mínimo: aviso legal, privacidad, cookies y
términos. Sin ellas AdSense no aprueba el sitio, y con anuncios son obligatorias de
todas formas.

### 4. Contenido con sustancia

34 fichas de 350 palabras y 2 guías es poco para un comparador que quiere ser
referencia. No hace falta multiplicar páginas: hace falta que las que hay valgan más.

- Ampliar cada ficha a 700–900 palabras **sin relleno**: para quién es, para quién no,
  qué se echa en falta, rival directo, cuándo merece la pena pagar la diferencia.
- 8–10 comparativas directas («MacBook Air M4 vs M5», «LOQ vs TUF A15»…), que es lo
  que busca la gente y lo que demuestra criterio.
- 4–6 guías por presupuesto (500, 700, 900, 1.200 €) y por uso (programar, diseño,
  viaje, universidad).
- Glosario y preguntas frecuentes reales, no relleno.
- Cada página nueva debe tener una intención de búsqueda clara y no canibalizar otra.

### 5. Quitar la promesa de «sin anuncios»

Aparece en la portada, en `sobre.html`, `metodologia.html`, `contacto.html`, las dos
guías, el pie de las 34 fichas y el generador. Si se activa AdSense sin cambiarlo, el
sitio se contradice y eso es un problema de confianza y de políticas. Hay que
sustituirlo por una explicación honesta: «el sitio se financia con publicidad de
Google; los anuncios no influyen en las notas ni en el orden del catálogo».

## P1 — producto y experiencia

- **Buscador** por nombre o marca. Es la función que más se echa en falta con 34
  modelos.
- **Filtros y orden**: precio, peso, RAM, marca y uso; ordenar por nota, precio o
  ligereza. Los chips de perfil actuales no filtran, solo cambian la nota.
- **Comparar tres modelos** o, al menos, permitir guardar una comparación y copiar el
  enlace (`?a=…&b=…` ya funciona).
- **Enlace compartible** con botón «Copiar enlace» y confirmación accesible.
- **Estado vacío** claro cuando no hay resultados.
- **Favoritos** en `localStorage`, sin cuentas.
- **404 útil**: buscador, enlaces a catálogo y guías. Ahora solo tiene un enlace.
- **Accesibilidad**:
  - Corregir el contraste de `.pill` y `.score` (Lighthouse).
  - `:focus-visible` en enlaces, botones y tarjetas.
  - Enlace «Saltar al contenido».
  - `aria-live="polite"` en el veredicto del comparador para lectores de pantalla.
  - Revisar el orden de tabulación de las tarjetas.
- **Rendimiento**: `srcset` + WebP/AVIF, precarga de la imagen principal y medir LCP.
  Los 2,9 MB actuales se notan en móvil.
- **Modo oscuro**: opcional, solo si no resta claridad.

## P1 — contenido y confianza

- Ficha de cada modelo con **«Para quién no es»**: es lo que más diferencia a un
  comparador honesto.
- **Precio y contexto**: explicar si el precio es de lanzamiento, de liquidación o
  histórico, sin inventar fecha de comprobación.
- **Alternativas** ya existen; añadir por qué se descartan.
- **Fotos**: idealmente propias o con licencia. Si se mantienen las del fabricante,
  atribución clara y disposición a retirarlas si lo piden.
- **Página de correcciones** con los cambios importantes y su fecha.

## P2 — SEO y mantenimiento

- Páginas de categoría con contenido propio (`/mejores/portatiles-gaming.html`, etc.),
  no solo un listado generado.
- Enlazado interno: cada ficha a su guía y a su comparativa; cada guía a las fichas.
- `author` como `Person` en guías y reseñas, cuando exista la página de autor.
- `SearchAction` en `WebSite` cuando haya buscador.
- Revisar títulos de más de 60 caracteres y descripciones fuera de rango.
- `lastmod` del sitemap solo cuando cambie el contenido de verdad.
- Excluir el vault y los scripts de la publicación (ver [[Mejoras/Seguridad|Seguridad]]).
- IndexNow después de cada publicación; Search Console, revisión mensual.

## P2 — infraestructura

- **CI en GitHub Actions**: comprobar enlaces, auditar SEO y validar HTML en cada push.
- **Tests de datos**: slugs únicos, campos obligatorios, precios numéricos, imágenes
  existentes.
- **Script de imágenes huérfanas**: fotos en `img/` que no usa ningún modelo.
- **Registro de cambios** en el README o en una página del sitio.
- **Copia de seguridad** fuera de GitHub (el repo no es una copia).
- **Revisión trimestral**: precios, enlaces, imágenes, contenido desactualizado.

## Qué evitar

- Inventar reseñas, valoraciones de usuarios o «opiniones verificadas».
- Fechas de actualización que no correspondan a cambios reales.
- Popups, autoplay, banners que tapen el contenido o anuncios que parezcan navegación.
- Meter AMP, frameworks o dependencias solo por moda.
- Páginas de categoría vacías o duplicadas para captar tráfico.
- Copiar descripciones del fabricante o de otras webs.

## Métricas para saber si funciona

- Páginas indexadas y impresiones en Search Console.
- CTR y posición media de las fichas y guías.
- Tiempo hasta la aprobación de AdSense y, después, RPM y visibilidad.
- Búsquedas internas sin resultados (cuando exista buscador).

## Orden recomendado

1. Medir el tráfico 2–3 meses con Search Console ([[Contexto/Medicion|Medición]]).
2. Decidir dominio con esos datos; correo profesional si se compra.
3. Legal y cookies ([[Mejoras/Legal|Legal]]).
4. Autoría y política editorial.
5. Ampliar 10 fichas y escribir 4 comparativas.
6. Producto: buscador, filtros y accesibilidad.
7. Seguridad y exclusión de notas ([[Mejoras/Seguridad|Seguridad]]).
8. Solicitud de AdSense.
