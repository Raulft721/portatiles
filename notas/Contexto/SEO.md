---
tipo: contexto
actualizado: 2026-10-29
tags:
  - comparaportatil
  - seo
  - indexacion
---

# SEO e indexación

## Estado del 29/10/2026

Google envió varios correos avisando de páginas que no había podido indexar. No se ha
podido leer el motivo exacto dentro de Search Console, así que se hizo una auditoría
técnica completa:

| Comprobación | Resultado |
| --- | --- |
| URLs del sitemap en vivo | 40/40 responden 200 |
| Canonical de cada URL | Correcto en las 40 |
| Sitemap vs. páginas locales | 40 y 40, sin faltas ni sobrantes |
| Títulos y descripciones | Únicos en todas las páginas |
| JSON-LD | Parsea en todas las páginas |
| Rich Results Test (ficha) | 3 elementos válidos, sin avisos (29/10, tras el cambio) |
| Rich Results Test (portada) | Carrusel válido |
| `robots` de páginas indexables | `index, follow` |
| `404.html` | `noindex, follow` |

Conclusión: no hay un bloqueo técnico evidente. Las causas más probables son URLs
antiguas que devolvieron 404 antes de que existieran las fichas, variantes duplicadas
descubiertas por Google o errores 5xx puntuales de GitHub Pages.

## Search Console

- **Propiedad**: prefijo de URL `https://raulft721.github.io/portatiles/`, ya
  verificada. Cubre solo esa ruta; si se cambia al dominio propio habrá que crear otra
  y usar «Cambio de dirección».
- **Sitemap enviado**: `https://raulft721.github.io/portatiles/sitemap.xml`.
- **Línea base** (captura del 27/10/2026, periodo de 3 meses): **0 clics, 3
  impresiones, CTR 0 %, posición media 38**. El sitio se publicó el 25/10, así que es
  el primer dato y no permite conclusiones.
- **Informes de mejoras**: «Fragmentos de productos» y «Fichas de comerciantes». Los
  avisos se corrigieron el 29/10; falta pulsar «Validar corrección» y esperar.
- **Indexación → Páginas**: es donde está el motivo exacto de los correos. Pendiente de
  revisar y anotar.
- **29/10/2026**: se pidió **«Validar corrección»** en el informe de indexación y se
  enviaron varias URLs con **«Solicitar indexación»**. Ahora toca esperar: la validación
  puede tardar días o semanas y no garantiza que todo se indexe.
- **Comprobación del 29/10**: `python scripts/auditar-seo.py --live` sigue sin errores;
  las 40 URLs responden 200 y el `lastmod` del sitemap es del 29/10.

Detalle y criterios de seguimiento en [[Contexto/Medicion|Medición de tráfico]].

## Datos estructurados de las fichas

Las capturas de Search Console mostraban dos avisos **no críticos** en las fichas:

- **Fichas de comerciantes**: faltaban `hasMerchantReturnPolicy` y `shippingDetails`.
- **Fragmentos de productos**: faltaban `review` y `aggregateRating`.

El sitio es un comparador, no una tienda: no puede declarar envíos, devoluciones ni
reseñas de clientes sin inventarlas. Por eso se tomó esta decisión:

- Se retiró el `Offer`. Sin oferta de venta, Google deja de tratar la ficha como ficha
  de comerciante y el informe deja de aplicar.
- Se añadió una `Review` editorial: `reviewRating` es la nota global del modelo y
  `reviewBody` es el párrafo «Para quién es» que ya se ve en la página. El autor es la
  propia Organización.
- La ficha muestra ahora «La nota global es N / 100» junto a las barras, para que el
  dato del JSON-LD esté también visible.

Resultado en Rich Results Test (29/10/2026): Producto, Migas y Fragmentos de reseñas
válidos, **sin problemas críticos ni no críticos**. Verificado sobre
`portatil/macbook-air-13-m4.html`; el resto de fichas usa la misma plantilla.

No se añadió `aggregateRating`: exigiría reseñas reales de usuarios que el sitio no
tiene.

## Qué se ha corregido

- Los enlaces internos ya no apuntan a `index.html`: usan `./` desde la raíz y `../`
  desde `portatil/` y `guias/`. Así Google no descubre una segunda URL de la portada.
- Se añadió `scripts/auditar-seo.py`, que comprueba sitemap, canonical, metadatos,
  JSON-LD y, con `--live`, el estado HTTP de las URLs publicadas.
- El generador usa el mismo criterio en las fichas nuevas.
- `Offer` sustituido por `Review` editorial en las 34 fichas (commit `d50f636`).

## Qué hacer ahora en Search Console

1. Entrar en **Indexación → Páginas**.
2. Filtrar por «No indexada» y abrir el grupo que mencionan los correos.
3. Anotar el **motivo** exacto y las URLs. Los motivos habituales:
   - **404**: la URL ya no existe o cambió de slug.
   - **Duplicada, Google ha elegido otra canónica**: normal si conviven `.html` y la
     versión sin extensión; el canonical ya apunta a `.html`.
   - **Error de servidor (5xx)**: fallo puntual de GitHub Pages; reintentar.
   - **Rastreada, actualmente no indexada**: no es un error técnico; influyen contenido,
     enlaces y autoridad.
4. En **Mejoras → Fichas de comerciantes** y **Fragmentos de productos**, pulsar
   **Validar corrección**. Google volverá a rastrear y, si todo va bien, los avisos
   desaparecen en 2–4 semanas.
5. Reenviar `sitemap.xml` y, si alguna URL concreta importa, usar **Inspeccionar URL →
   Solicitar indexación**.

El sitemap correcto es:

```
https://raulft721.github.io/portatiles/sitemap.xml
```

## Limitación de `robots.txt`

En un project site de GitHub Pages el `robots.txt` del repositorio se sirve en
`/portatiles/robots.txt`, pero los rastreadores solo leen el de la raíz del host
(`https://raulft721.github.io/robots.txt`). Ese archivo no existe y no se puede crear
desde este repositorio. No bloquea la indexación: un 404 en `robots.txt` se interpreta
como «sin restricciones». Si se quiere controlar, hay que crear el repositorio
`Raulft721.github.io` con su propio `robots.txt` y el `Sitemap:` correspondiente.

## Auditoría local

```powershell
python scripts/generar.py
python scripts/comprobar-enlaces.py
python scripts/auditar-seo.py
python scripts/auditar-seo.py --live
```

`auditar-seo.py` no modifica archivos y sale con código 1 si encuentra errores.

## Pendiente

Ver [[Tareas#Prioridad alta — indexación y Search Console]].
