---
tipo: contexto
actualizado: 2026-10-29
tags:
  - comparaportatil
  - hosting
  - infraestructura
---

# Hosting: GitHub Pages, Vercel y alternativas

## Decisión (29/10/2026)

**No migrar a Vercel ahora.** GitHub Pages se queda hasta que haya una razón técnica o
de negocio que lo justifique: dominio propio, tráfico real o una función que GitHub
Pages no pueda dar. Cambiar de host no trae visitas y, si se hace mal, cuesta
posiciones.

## Lo que hay que tener claro

- **Vercel no es un dominio**: es otro hosting. El dominio se compra aparte y se puede
  usar con cualquiera de las dos opciones.
- **GitHub Pages ya es un CDN**: sirve el sitio desde Fastly, con HTTPS y caché. Para
  una web estática de 3 MB no hay una diferencia de velocidad que se note.
- **El cuello de botella es el contenido y la indexación**, no el hosting. Con 3
  impresiones en Search Console, cambiar de plataforma no cambia nada.

## Comparativa

| | GitHub Pages | Vercel Hobby | Vercel Pro | Cloudflare Pages |
| --- | --- | --- | --- | --- |
| Precio | Gratis | Gratis | 20 $/usuario/mes | Gratis |
| Uso comercial | Restringido por términos | **Solo personal, no comercial** | Sí | Sí |
| Ancho de banda | ~100 GB/mes (blando) | Limitado según plan | Incluido con crédito | Ilimitado en estático |
| Cabeceras propias | No | Sí | Sí | Sí |
| Redirecciones 301 | No (solo meta/JS) | Sí | Sí | Sí |
| Funciones serverless | No | Sí, con límites | Sí | Sí (Workers) |
| Previews por rama | No | Sí | Sí | Sí |
| Build | Jekyll o Actions | Sí | Sí | Sí |
| Complejidad | Mínima | Media | Media | Media |

Datos de referencia de 2026; conviene revisar las páginas de precios antes de decidir.

### El detalle que cambia la decisión: uso comercial

El plan **Hobby de Vercel es para proyectos personales y no comerciales**. Un sitio con
AdSense es monetizado; Vercel lo considera uso comercial y el plan adecuado sería
**Pro, 20 $/usuario/mes** (unos 220 €/año). Para un proyecto con 3 impresiones al mes,
no tiene sentido.

GitHub Pages también tiene una restricción: sus términos no permiten usarlo como
hosting gratuito para «un negocio online, comercio electrónico o SaaS». Un sitio de
contenido con anuncios es una zona gris; si el proyecto se convierte en un negocio,
Cloudflare Pages es una opción más limpia y sigue siendo gratis.

## Por qué no migrar ahora

1. **Cambiaría la URL.** En Vercel el sitio viviría en `algo.vercel.app` hasta que haya
   dominio propio. Eso es otra mudanza justo cuando se está intentando indexar: nuevos
   canonical, sitemap, Search Console y enlaces. Mala idea.
2. **No mejora el SEO por sí solo.** Google no premia el host; premia contenido,
   enlaces y experiencia. La velocidad ya es buena.
3. **Cuesta dinero si hay anuncios.** Hobby no vale para un sitio monetizado; Pro son
   ~220 €/año.
4. **Las ventajas no se usan.** Cabeceras, redirecciones y funciones están bien, pero
   hoy no hay formularios, API ni necesidades de SSR.
5. **Añade mantenimiento.** Otro panel, otra configuración, otro sitio donde mirar
   cuando algo falla.

## Cuándo sí merecería la pena

- **Dominio propio y necesidad de cabeceras o redirecciones 301.** Entonces:
  GitHub Pages + Cloudflare por delante (gratis) o Cloudflare Pages.
- **Funciones serverless** (precios automáticos, búsqueda, formularios): Cloudflare
  Workers/Pages o Vercel.
- **Next.js, SSR o un equipo con previews**: Vercel es de lo mejor, pero este sitio es
  HTML estático.
- **Límites de GitHub Pages**: solo si se superan los ~100 GB/mes o 1 GB de sitio, algo
  impensable a corto plazo.
- **Ingresos que justifiquen** los 20 $/mes de Vercel Pro.

## Si se quiere probar Vercel

Se puede desplegar una copia en `*.vercel.app` sin tocar producción: sirve para ver el
flujo, medir y comparar. Lo que **no** conviene es mover el sitio definitivo a una URL
de Vercel antes de tener dominio. Si algún día se migra, hacerlo con dominio propio y
con redirecciones desde la URL vieja.

## Recomendación

Quedarse en GitHub Pages. Cuando llegue el dominio, decidir en este orden:

1. GitHub Pages + Cloudflare (DNS, caché, cabeceras y redirecciones): lo más barato y
   con menos cambios.
2. Cloudflare Pages: si se quieren funciones o builds sin pagar.
3. Vercel Pro: solo si se necesita su ecosistema y los ingresos lo justifican.

## Registro de decisiones

- **29/10/2026**: evaluado Vercel. No se migra: Hobby no permite uso comercial, Pro
  cuesta ~220 €/año y el cambio de URL perjudica la indexación. GitHub Pages se queda
  hasta que haya dominio o una necesidad técnica real. Ver [[Contexto/Medicion|Medición]]
  y [[Mejoras/AdSense|AdSense]].
