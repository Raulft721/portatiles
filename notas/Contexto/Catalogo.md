---
tipo: contexto
actualizado: 2026-10-29
tags:
  - comparaportatil
  - catalogo
---

# Catálogo

## Fuente de verdad

El array `LAPTOPS` de `index.html`. Todo lo demás se genera a partir de él. No editar
las fichas de `portatil/` a mano: se sobrescriben al ejecutar `generar.py`.

## Añadir un modelo

1. Añadir un objeto al final del array `LAPTOPS` con todos los campos.
2. Guardar la foto en `img/` en JPEG 1000×750, fondo blanco y sin recortes raros.
3. Ejecutar `python scripts/generar.py`.
4. Ejecutar `scripts/og.ps1` para crear su imagen social.
5. Revisar la ficha generada y el enlace desde la portada.
6. Ejecutar `comprobar-enlaces.py` y `auditar-seo.py --live`.
7. Hacer commit y publicar.

## Campos

| Campo | Qué es |
| --- | --- |
| `id` | Identificador corto usado por el comparador (`?a=…`). |
| `slug` | Parte final de la URL de la ficha; se genera del nombre si falta. |
| `img` | Ruta de la foto, por ejemplo `img/mba13-m4.jpg`. |
| `name` | Nombre comercial completo. |
| `brand` | Marca. |
| `price` | Precio orientativo en euros, sin decimales. |
| `cpu`, `gpu`, `ram`, `storage`, `screen` | Especificaciones tal y como las publica el fabricante. |
| `weight` | Peso en kilos. |
| `battery` | Horas de autonomía o `null` si el fabricante no las publica. |
| `wh` | Capacidad de la batería en vatios-hora. |
| `os` | Sistema operativo. |
| `scores` | Notas de 0 a 100: `estudio`, `trabajo`, `gaming`, `movilidad`. |
| `grad` | Degradado de la tarjeta. |
| `aviso` | Texto opcional bajo la tabla de la ficha. |

## Reglas

- No inventar especificaciones. Si no hay dato de autonomía, `battery: null`.
- No borrar modelos antiguos: el catálogo es acumulativo.
- Los precios son orientativos; no afirmar que están verificados.
- Las fotos deben ser del producto real.
- Los equipos sin sistema operativo llevan un aviso explícito; el generador lo añade
  solo si `os` empieza por FreeDOS, «Sin sistema» o «Sin SO».

## Notas generadas

- Cada ficha incluye un párrafo con su mejor y su peor apartado, su posición por peso y
  precio, tres alternativas cercanas y las guías relacionadas.
- Las tarjetas de la portada se ordenan por la nota del perfil equilibrado.
- El ItemList de la portada se genera con el mismo orden del array.

Ver también [[Contexto/Proyecto#Modelo de datos|Modelo de datos]].
