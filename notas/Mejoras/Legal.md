---
tipo: legal
actualizado: 2026-10-29
tags:
  - comparaportatil
  - legal
  - privacidad
  - cookies
---

# Legal y privacidad

El sitio no tiene hoy ninguna página legal. Con AdSense deja de ser opcional: Google
pide política de privacidad y consentimiento, y la ley española pide identificación del
titular y información sobre cookies. Esta nota es una lista de trabajo, **no
asesoramiento jurídico**; los textos finales conviene revisarlos con un profesional,
sobre todo si hay ingresos publicitarios.

## Páginas que hacen falta

| Página | Para qué | Obligatoria |
| --- | --- | --- |
| Aviso legal | Identificar al titular y las condiciones de uso | Sí (LSSI) |
| Política de privacidad | Explicar qué datos se tratan y por qué | Sí (RGPD) |
| Política de cookies | Consentimiento y detalle de cookies | Sí (LSSI y AEPD) |
| Términos de uso | Reglas de uso y límites de responsabilidad | Recomendada |
| Política editorial | Quién escribe, cómo se puntúa y cómo se corrige | Recomendada (confianza) |
| Contacto | Canal real de comunicación | Sí (AdSense) |

## Aviso legal

Basado en el artículo 10 de la LSSI-CE. Debe incluir:

- **Titular**: nombre y apellidos o razón social, NIF, domicilio y correo electrónico.
- **Actividad**: comparador informativo de portátiles; no es una tienda.
- **Objeto**: condiciones de acceso y uso.
- **Propiedad intelectual**: textos propios; fotografías de fabricante usadas con fines
  informativos y derechos de sus marcas.
- **Responsabilidad**: la información es orientativa, los precios cambian y no hay
  garantía de disponibilidad.
- **Enlaces externos**: no se responde de su contenido.
- **Legislación aplicable**: española.

Si no quieres publicar tu nombre, NIF y domicilio particulares, valora hacerlo con una
sociedad o un servicio de representación. Es una decisión legal y fiscal; consúltalo
antes de solicitar AdSense.

## Política de privacidad

### Qué debe contar

- **Responsable** y correo de contacto.
- **Datos que se tratan**:
  - Datos técnicos de navegación que registra GitHub Pages (IP, fecha, página).
  - El correo y el contenido si alguien escribe.
  - Preferencias guardadas en `localStorage` (perfil y modelos comparados).
  - Datos derivados de cookies publicitarias, si se aceptan.
- **Finalidades**: servir el sitio, responder consultas, medir y mostrar publicidad.
- **Base jurídica**: interés legítimo en la seguridad y el funcionamiento; consentimiento
  para cookies no técnicas y publicidad personalizada; consentimiento o contrato para
  las consultas.
- **Destinatarios**: GitHub (hosting), Google (AdSense y, si se añade, analítica),
  proveedor de correo.
- **Transferencias internacionales**: Google y GitHub pueden tratar datos fuera del EEE;
  se amparan en cláusulas contractuales tipo y decisiones de adecuación.
- **Plazos**: los mínimos necesarios; los logs, lo que conserve GitHub; las cookies, lo
  que indique la CMP.
- **Derechos**: acceso, rectificación, supresión, limitación, oposición y portabilidad,
  además de retirar el consentimiento. Reclamación ante la AEPD.
- **Menores**: el sitio no se dirige a menores de 14 años.
- **Cambios**: fecha de la última actualización.

### Texto que AdSense espera ver

La política debe mencionar, como mínimo:

- Que terceros, incluido Google, usan cookies para mostrar anuncios basados en visitas
  anteriores.
- Que el uso de cookies de publicidad permite a Google y sus socios mostrar anuncios
  basados en esas visitas.
- Cómo desactivar la publicidad personalizada: configuración de anuncios de Google
  (`https://adssettings.google.com`) y `https://www.aboutads.info`.
- Enlace a «Cómo utiliza Google la información de sitios o aplicaciones que utilizan
  sus servicios».

No copiar un texto genérico sin adaptarlo: tiene que coincidir con lo que hace el sitio.

## Política de cookies

### Consentimiento

- No se carga ninguna cookie no técnica antes de que la persona acepte.
- Aceptar y rechazar tienen el mismo peso visual. Nada de botones ocultos ni textos
  confusos.
- Se puede cambiar la decisión desde un enlace permanente «Cookies» en el pie.
- Se guarda la prueba del consentimiento (la CMP lo hace).
- Sin cookie wall: se puede leer el sitio sin aceptar.

### Qué hay que listar

- **Técnicas**: `localStorage` con `comparaportatil.v1` (perfil y comparación). No es una
  cookie, pero se explica igual.
- **Publicitarias**: las que instale Google con AdSense. La lista y la duración deben
  salir de la CMP y de la documentación vigente de Google; no copiar una tabla de hace
  años. Ejemplos habituales: `IDE`, `test_cookie`, `__gads`, `__gpi`.
- **Analíticas**: solo si se añade analítica. Hoy no hay.

### Cómo revocar

- Enlace «Cookies» en el pie que reabra el panel de consentimiento.
- Enlaces a la configuración de anuncios de Google y a `aboutads.info`.
- Instrucciones para borrar cookies en el navegador.

## Términos de uso

- El sitio es informativo; no vende ni gestiona pedidos.
- Los precios son orientativos y pueden estar desactualizados.
- Las notas son una valoración editorial basada en especificaciones y precio, no una
  prueba física.
- No hay garantía de disponibilidad ni de que el sitio esté libre de errores.
- Propiedad intelectual: textos propios; imágenes de fabricante con atribución.
- Enlaces a terceros: no se controla su contenido.
- Modificaciones: se puede cambiar el sitio y estos términos.

## Política editorial

Es la página que más confianza aporta y la que casi nadie tiene:

- Quién escribe y con qué experiencia.
- Cómo se elige un modelo para el catálogo.
- De dónde salen las especificaciones (fabricante) y cómo se calculan las notas
  (enlazar a `metodologia.html`).
- Cómo se financia el sitio y qué independencia hay frente a los anunciantes.
- Cómo se corrige un error y en cuánto tiempo se avisa.
- Qué no se acepta: pago por notas, enlaces patrocinados, regalos.

## Textos que hay que cambiar

- `index.html`: «Comparador independiente · sin anuncios ni afiliados» y el pie.
- `sobre.html`: «sin anuncios», «no hay cookies de seguimiento» y el pie.
- `metodologia.html`: «El sitio no tiene anuncios…» y el pie.
- `contacto.html`: «Sin anuncios ni enlaces de afiliado» y «no hay correo».
- `guias/*.html`: pie de las dos guías.
- `portatil/*.html`: pie de las 34 fichas, generado por `scripts/generar.py`.
- `404.html`: revisar el pie si se añade uno.

Conviene centralizar el pie en el generador para no repetir el cambio 40 veces.

## Registro y proveedores

- **GitHub Pages**: hosting. Sus logs los trata GitHub; hay que mencionarlo.
- **Google AdSense**: publicidad y consentimiento.
- **Correo**: si se usa Gmail o un dominio propio, indicar el proveedor.
- **Encargados del tratamiento**: si se usan herramientas que tratan datos por cuenta
  del titular, se necesita un contrato de encargo (DPA). GitHub y Google los ofrecen.
- **Registro de actividades**: si el tratamiento es habitual, el RGPD pide un registro
  interno. Para un sitio pequeño puede ser un documento simple.

## Checklist legal

- [ ] Decidir el titular (persona física o sociedad).
- [ ] Crear aviso legal.
- [ ] Crear política de privacidad.
- [ ] Crear política de cookies.
- [ ] Crear términos de uso.
- [ ] Crear política editorial.
- [ ] Añadir enlaces legales al pie de todas las páginas.
- [ ] Sustituir los textos de «sin anuncios» y «sin cookies».
- [ ] Activar la CMP antes de publicar anuncios.
- [ ] Probar aceptar, rechazar y cambiar de opinión.
- [ ] Revisar los textos con un profesional antes de solicitar AdSense.

## Relacionado

- [[Mejoras/AdSense|AdSense]]
- [[Mejoras/Plan|Plan de profesionalización]]
- [[Mejoras/Seguridad|Seguridad]]
