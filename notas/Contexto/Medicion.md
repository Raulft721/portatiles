---
tipo: contexto
actualizado: 2026-10-29
tags:
  - comparaportatil
  - medicion
  - analitica
  - trafico
---

# Medición de tráfico

## Decisión (29/10/2026)

Antes de comprar dominio u hosting, medir. El dominio no hace que llegue gente por sí
solo: el tráfico depende del contenido, de la indexación y de los enlaces. Comprarlo
antes de tener datos es gastar sin saber si el problema es de visibilidad o de
contenido.

## Lo que ya se puede medir

### Search Console (gratis, sin cookies)

Es la fuente principal y ya está configurada. En **Rendimiento** da:

- Clics, impresiones, CTR y posición media.
- Consultas por las que aparece el sitio.
- Páginas, países y dispositivos.
- Evolución por fechas.

En **Indexación → Páginas** se ve qué está indexado y qué no.

No ve visitas directas, redes sociales ni tráfico que no venga de Google, pero para
decidir si el proyecto tiene tracción es suficiente. No necesita script ni
consentimiento de cookies.

### Bing Webmaster Tools

IndexNow ya envía las 40 URLs. Dar de alta el sitio en Bing permite ver impresiones y
consultas en Bing, que es una parte pequeña pero gratis de medir.

### GitHub Insights → Traffic

**No sirve para esto.** Mide visitas al repositorio, no a la web publicada. No hay logs
del sitio en GitHub Pages.

## Lo que no se puede medir sin un script

- Visitas directas (enlaces desde WhatsApp, foros, redes).
- Páginas vistas, tiempo de lectura y rebote.
- Qué contenido funciona fuera de Google.

Si lo que se quiere saber es «cuánta gente entra» en total, hace falta analítica. Si
solo se quiere saber si Google trae gente, Search Console basta.

## Opciones de analítica sin cookies

| Herramienta | Coste | Cookies | Cómo se instala | Notas |
| --- | --- | --- | --- | --- |
| Search Console | Gratis | No | Ya está | Solo tráfico de Google |
| Cloudflare Web Analytics | Gratis | No | Script | Requiere cuenta; se puede usar sin mover el DNS |
| GoatCounter | Gratis para uso personal | No | Script | Revisar licencia si el sitio se monetiza |
| Umami Cloud | Plan gratis limitado | No | Script | Alternativa sencilla |
| Plausible | De pago | No | Script | La más cuidada, pero cuesta |
| Google Analytics 4 | Gratis | Sí | Script + CMP | No recomendable ahora: obliga a consentimiento y a prisa legal |

Recomendación: **empezar solo con Search Console**. Si más adelante se quiere el total
de visitas, añadir Cloudflare Web Analytics o GoatCounter, que no usan cookies, y
mencionarlo en la política de privacidad.

## Qué mirar y durante cuánto tiempo

- Revisar a los **30, 60 y 90 días**. El primer mes no dice casi nada.
- **Impresiones por página**: si una página no tiene impresiones, o no está indexada o
  no responde a ninguna búsqueda.
- **Consultas**: si aparecen las que se esperaban («portátil para estudiar», «MacBook
  Air M4 precio»…).
- **CTR**: si hay impresiones pero poco clic, el problema es el título o la descripción.
- **Posición media**: entre 8 y 20 hay margen claro; por debajo de 5 ya se compite.
- **Páginas con clics**: son las que hay que ampliar y enlazar mejor.

## Criterios para decidir el dominio

| Señal a los 3 meses | Decisión |
| --- | --- |
| Menos de 20 clics/mes | No comprar todavía. Mejorar contenido y enlazado |
| 20–100 clics/mes | Seguir midiendo; dominio cuando se acerque a 100 o antes de AdSense |
| Más de 100 clics/mes sostenidos 2 meses | Comprar dominio y preparar AdSense |
| Se va a solicitar AdSense antes | Dominio (por `ads.txt`) o repo `Raulft721.github.io` |

No es una regla matemática: si el proyecto gusta y se quiere consolidar, el dominio
cuesta poco. Pero con 5 visitas al mes no arregla nada.

## Dominio y host: lo que cuesta de verdad

- **Dominio**: unos 10–15 € al año.
- **Host**: **no hace falta cambiarlo**. GitHub Pages sigue siendo gratis y sirve
  perfectamente con dominio propio.
- **Cloudflare**: gratis, para DNS, caché y cabeceras.
- **Correo**: un alias con el dominio se puede contratar aparte; para empezar vale un
  Gmail dedicado.

Así que el desembolso inicial es el dominio, no un hosting nuevo.

## Si se compra el dominio más adelante

- GitHub Pages no permite redirecciones de servidor. Con Cloudflare se pueden hacer
  reglas 301; sin él, habría que mantener el sitio en `github.io` y redirigir con
  `meta refresh` o JavaScript, que es peor.
- Search Console tiene «Cambio de dirección» para transferir la confianza.
- Hay que actualizar `SITE` en `scripts/generar.py`, canonical, sitemap, OG y todos los
  enlaces absolutos.
- Mantener el dominio viejo apuntando al nuevo al menos un año.
- Cuanto antes se haga, menos enlaces habrá que redirigir.

## Qué hacer mientras tanto

Nada de esto depende del dominio:

- Ampliar fichas y escribir comparativas ([[Mejoras/Plan|Plan]]).
- Páginas legales ([[Mejoras/Legal|Legal]]), que hacen falta igualmente.
- Página de autor y política editorial.
- Accesibilidad y peso de las imágenes.
- Revisar Search Console cada dos semanas.

## Registro de decisiones

- **29/10/2026**: posponer la compra de dominio y hosting hasta tener métricas de
  tráfico. Medir con Search Console; valorar analítica sin cookies si se quiere el total
  de visitas. Ver [[Tareas]].
