---
tipo: contexto
actualizado: 2026-10-29
tags:
  - comparaportatil
  - proyecto
---

# Proyecto

Comparador de portátiles en español, estático y sin backend. Se publica en GitHub Pages.

- Web: <https://raulft721.github.io/portatiles/>
- Repositorio: <https://github.com/Raulft721/portatiles> (rama `main`)
- Local: `python -m http.server 8000` y abrir <http://127.0.0.1:8000>

## Stack

- HTML, CSS y JavaScript sin dependencias ni build.
- `index.html` contiene la interfaz, los estilos y la lógica del comparador.
- `index.html` también es la **única fuente de verdad** del catálogo: el array `LAPTOPS`.
- `scripts/generar.py` crea las fichas, las tarjetas del catálogo, el ItemList, el
  `sitemap.xml` y el manifiesto de imágenes sociales.
- `scripts/og.ps1` genera las imágenes 1200×630 de `img/og/`.
- GitHub Pages publica directamente desde la rama `main`.

## Estructura

```
index.html              comparador + datos LAPTOPS
portatil/<slug>.html    una ficha por modelo (generada)
guias/                  dos guías de compra
metodologia.html        cómo se calculan las notas
sobre.html              información del proyecto
contacto.html           cómo avisar de errores
404.html                página de error (noindex)
img/                    fotos de producto y logo
img/og/                 imágenes sociales (generadas)
scripts/                generación, comprobaciones y publicación
notas/                  este vault de Obsidian
```

## Modelo de datos

Cada objeto de `LAPTOPS` tiene:

```
id, slug, img, name, brand, price
cpu, gpu, ram, storage, screen, weight
battery (horas o null), wh (capacidad), os
scores: { estudio, trabajo, gaming, movilidad }
grad (degradado de la tarjeta), aviso (texto opcional)
```

- `slug` se genera a partir del nombre si falta.
- `battery: null` significa que el fabricante no publica autonomía; la ficha muestra
  «Sin dato del fabricante» y el comparador no declara ganador en esa fila.
- `scores` van de 0 a 100 y el perfil equilibrado pondera un 25 % cada apartado.

## Reglas de contenido

- Todo en español, tono claro y directo, sin lenguaje de marketing.
- Los precios son **orientativos de referencia**. No afirmar que están verificados ni
  poner fecha de comprobación.
- No inventar especificaciones.
- No borrar modelos antiguos: el catálogo es acumulativo.
- Las fotos deben ser del producto real. Preferencia: CDN del fabricante; si no hay,
  tienda especializada. Formato 1000×750 JPEG, fondo blanco.
- Nada se publica sin comprobarlo antes: enlaces, JSON-LD y revisión visual.

## Flujo de trabajo

1. Cambiar el catálogo en `index.html` o el contenido de una página.
2. `python scripts/generar.py`
3. `python scripts/comprobar-enlaces.py`
4. `python scripts/auditar-seo.py --live`
5. Revisar el resultado y hacer commit.
6. `git push origin main`
7. Cuando Pages sirva la versión nueva, `python scripts/indexnow.py`.

Más detalle en [[Contexto/Publicacion|Publicación]] y [[Contexto/SEO|SEO]].

## Para agentes

`AGENTS.md`, en la raíz del repositorio, resume las instrucciones que debe seguir un
agente. Este vault es el contexto humano: [[Tareas]] es el punto de entrada.
