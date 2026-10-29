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
| Rich Results Test (ficha) | 3 elementos válidos, solo avisos no críticos |
| Rich Results Test (portada) | Carrusel válido |
| `robots` de páginas indexables | `index, follow` |
| `404.html` | `noindex, follow` |

Conclusión: no hay un bloqueo técnico evidente. Las causas más probables son URLs
antiguas que devolvieron 404 antes de que existieran las fichas, variantes duplicadas
descubiertas por Google o errores 5xx puntuales de GitHub Pages.

## Qué se ha corregido

- Los enlaces internos ya no apuntan a `index.html`: usan `./` desde la raíz y `../`
  desde `portatil/` y `guias/`. Así Google no descubre una segunda URL de la portada.
- Se añadió `scripts/auditar-seo.py`, que comprueba sitemap, canonical, metadatos,
  JSON-LD y, con `--live`, el estado HTTP de las URLs publicadas.
- El generador usa el mismo criterio en las fichas nuevas.

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
4. Reenviar `sitemap.xml` y pulsar **Validar corrección** en el informe.
5. Inspeccionar una o dos URLs afectadas con **Inspeccionar URL**.

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
