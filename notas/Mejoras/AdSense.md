---
tipo: monetizacion
actualizado: 2026-10-29
tags:
  - comparaportatil
  - adsense
  - monetizacion
---

# AdSense: qué hace falta para que lo aprueben

AdSense no se aprueba por tener el sitio «bonito»: se aprueba por tener contenido
original y útil, navegación clara, páginas legales y ningún motivo de rechazo. La
revisión la hace una persona (o un sistema con revisión humana detrás) y puede tardar
desde unos días hasta varias semanas.

## Estado actual frente a los requisitos

| Requisito | Estado |
| --- | --- |
| HTTPS | ✅ GitHub Pages lo fuerza |
| Sitio accesible y navegable | ✅ 40 URLs, menú y pie |
| Contenido original y con valor | ⚠️ 34 fichas de ~350 palabras y 2 guías |
| Página «Sobre» | ✅ existe |
| Contacto | ⚠️ solo GitHub Issues, sin correo |
| Autoría identificable | ❌ no hay nombre ni página de autor |
| Política de privacidad | ❌ no existe |
| Política de cookies | ❌ no existe |
| Consentimiento (CMP) | ❌ no existe |
| Aviso legal | ❌ no existe |
| Términos de uso | ❌ no existe |
| `ads.txt` en la raíz | ❌ no existe |
| Dominio propio | ❌ `github.io/portatiles` |
| Coherencia: «sin anuncios» | ❌ se afirma en todo el sitio |
| Contenido prohibido | ✅ no hay |
| Móvil y velocidad | ⚠️ funciona, pero 2,9 MB de imágenes |
| Copyright de imágenes | ⚠️ fotos de fabricante |

## Los cuatro bloqueantes duros

### 1. `ads.txt` en la raíz del dominio

Google busca `https://<dominio>/ads.txt`, no `https://<dominio>/portatiles/ads.txt`.
En un project site de GitHub Pages la raíz pertenece a otro repositorio, así que hoy no
se puede servir. Dos salidas:

**A. Dominio propio (recomendado).** Comprar un dominio, apuntarlo a GitHub Pages y
servir `ads.txt` en la raíz. Además da correo profesional, cabeceras y una URL que la
gente recuerda.

**B. Crear el repositorio `Raulft721.github.io`.** Ese repositorio se sirve en la raíz
de `https://raulft721.github.io/`, así que su `ads.txt` sí estaría donde Google lo
busca. Es rápido, pero la identidad del sitio sigue siendo un subdominio de GitHub y no
se pueden poner cabeceras.

El archivo debe ser texto plano, UTF-8, sin redirecciones, con una línea como:

```
google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0
```

El `pub-…` es el ID de editor de AdSense y `f08c47fec0942fa0` es el identificador de
certificación de Google. `ads.txt` no suele ser obligatorio para que aprueben la
cuenta, pero sí para monetizar bien y evitar inventario no autorizado.

### 2. Privacidad, cookies y consentimiento

Con AdSense, Google y sus socios usan cookies para mostrar anuncios. Eso obliga a:

- Política de privacidad que lo explique y enlace a la configuración de anuncios de
  Google.
- Política de cookies con tabla de terceros.
- **CMP certificado por Google** para el EEE, Reino Unido y Suiza. AdSense incluye uno
  gratuito en **Privacidad y mensajes**; hay que activarlo.
- Rechazar el consentimiento tan fácil como aceptarlo. Sin cookie wall ni botones
  engañosos.
- Enlace permanente a «Cookies» en el pie de página.

Detalle de los textos en [[Mejoras/Legal|Legal]].

### 3. Quitar «sin anuncios»

Hoy se afirma en la portada, `sobre.html`, `metodologia.html`, `contacto.html`, las dos
guías, el pie de las 34 fichas y la plantilla de `generar.py`. Si se activa AdSense sin
cambiarlo, el sitio se contradice. Sustituirlo por una frase honesta:

> El sitio se financia con publicidad de Google. Los anuncios no influyen en las notas,
> en el orden del catálogo ni en las recomendaciones.

### 4. Contenido suficiente

No hay un mínimo oficial de palabras, pero sí se rechaza el «contenido de poco valor»:
páginas casi iguales, texto generado sin criterio, listas sin explicación. Con 34
fichas de 350 palabras se puede solicitar, pero es arriesgado. Antes de enviar la
solicitud:

- 10–15 fichas ampliadas a 700–900 palabras con análisis real.
- 4–6 comparativas directas y 4 guías nuevas.
- Una página de autor y una política editorial.
- Fechas reales y fuentes por ficha.

## Cómo sería el anuncio

- **Ubicaciones**: después de la introducción, entre secciones y al final del artículo.
  En las fichas, nunca entre la tabla y su explicación.
- **Sin saltos de layout**: reservar el alto del bloque para que el contenido no salte.
- **Nada de anuncios en** `404.html`, páginas vacías o páginas sin contenido propio.
- **Nada de** anuncios que parezcan menús, botones de descarga o contenido editorial.
- **Nunca** hacer clic en los anuncios propios, ni pedir clics, ni comprar tráfico.

## Cuándo solicitar

No hay prisa. Solicitar antes de tiempo suele acabar en rechazo y en una segunda
revisión más lenta. Señales de que toca:

- 2–3 meses de datos en Search Console y al menos ~100 clics/mes sostenidos, o una
  decisión consciente de invertir en el proyecto aunque el tráfico aún sea bajo.
- 10–15 fichas ampliadas y 4–6 comparativas publicadas.
- Legal, cookies y CMP funcionando.
- Dominio decidido y `ads.txt` accesible.

Si el tráfico es muy bajo, AdSense no compensa el esfuerzo: primero contenido. Ver
[[Contexto/Medicion|Medición de tráfico]].

## Plan por fases

### Fase 0 — Decidir el dominio (solo si los datos lo justifican)

- [ ] Elegir dominio y comprarlo.
- [ ] Configurarlo en GitHub Pages con HTTPS.
- [ ] Actualizar `SITE`, canonical, sitemap, OG y Search Console.
- [ ] Crear el correo profesional.

### Fase 1 — Contenido y confianza (3–4 semanas)

- [ ] Página de autor y política editorial.
- [ ] Ampliar 10 fichas.
- [ ] Escribir 4 comparativas y 2 guías.
- [ ] Añadir fuentes y fechas reales.
- [ ] Revisar imágenes y atribuciones.

### Fase 2 — Legal y cookies (1 semana)

- [ ] Aviso legal.
- [ ] Privacidad.
- [ ] Cookies.
- [ ] Términos.
- [ ] Enlaces legales en el pie de todas las páginas.
- [ ] Sustituir los textos de «sin anuncios».

### Fase 3 — Solicitud

- [ ] Cuenta de AdSense con la edad y los datos fiscales correctos.
- [ ] Añadir el sitio y verificar la propiedad como indique Google.
- [ ] Comprobar que `ads.txt` responde 200 en la raíz.
- [ ] Comprobar que no hay páginas `noindex` en el sitemap.
- [ ] Enviar la solicitud y no tocar el sitio mientras se revisa.

### Fase 4 — Tras la aprobación

- [ ] Activar el CMP de Google para el EEE, Reino Unido y Suiza.
- [ ] Colocar los bloques poco a poco y medir.
- [ ] Revisar el Centro de políticas cada semana el primer mes.
- [ ] Vigilar el RPM, la visibilidad y el CTR, pero no optimizar solo por ingresos.
- [ ] No cambiar las URLs aprobadas sin motivo.

## Riesgos de rechazo y cómo evitarlos

| Motivo típico | Cómo se evita |
| --- | --- |
| Contenido de poco valor | Ampliar fichas y añadir criterio propio |
| Sin política de privacidad | Crearla antes de solicitar |
| Sin consentimiento | Activar el CMP |
| `ads.txt` inaccesible | Dominio propio o repo raíz |
| Sitio en construcción | No solicitar con secciones vacías |
| Navegación confusa | Menú, migas y enlaces internos claros |
| Contenido copiado | Texto propio y fuentes citadas |
| Imágenes sin derechos | Propias, con licencia o atribución clara |
| Incumplir políticas | Nada de contenido engañoso ni anuncios camuflados |

## Después de aprobar

- Los ingresos con poco tráfico serán bajos; no es un fracaso, es escala.
- Una cuenta por persona. No abrir cuentas duplicadas si hay un rechazo: corregir y
  volver a solicitar.
- Guardar los datos fiscales y declarar los ingresos según corresponda. Si la actividad
  es habitual, puede implicar alta como autónomo; eso se consulta con un asesor.
- Revisar los anuncios en móvil: son la mayoría del tráfico y donde peor quedan.

## Checklist rápida antes de enviar

- [ ] Dominio propio con HTTPS.
- [ ] `ads.txt` en la raíz, 200 y sin redirección.
- [ ] Privacidad, cookies, aviso legal y términos publicados.
- [ ] Enlace a «Cookies» en el pie.
- [ ] CMP activo y probado.
- [ ] Textos de «sin anuncios» eliminados.
- [ ] Autoría y política editorial visibles.
- [ ] 10 fichas ampliadas y 4 comparativas.
- [ ] Correo de contacto real.
- [ ] Search Console sin errores y sitemap al día.
- [ ] Imágenes revisadas.
- [ ] 404 útil y sin anuncios.
- [ ] Móvil y velocidad comprobados.

## Relacionado

- [[Mejoras/Plan|Plan de profesionalización]]
- [[Mejoras/Legal|Legal]]
- [[Mejoras/Seguridad|Seguridad]]
- [[Contexto/SEO|SEO]]
