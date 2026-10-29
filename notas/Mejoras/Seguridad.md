---
tipo: seguridad
actualizado: 2026-10-29
tags:
  - comparaportatil
  - seguridad
  - privacidad
---

# Seguridad y privacidad

Revisión del 29/10/2026. Conclusión corta: **no hay APIs, claves ni backend
expuestos**. La superficie de ataque es mínima porque el sitio es estático y no habla
con ningún servidor. Lo que hay que corregir es otra cosa: información interna
publicada sin querer y cabeceras de seguridad que GitHub Pages no permite poner.

## Inventario

- **Hosting**: GitHub Pages, HTTPS con HSTS (`max-age=31556952`). Sin servidor propio.
- **Runtime**: HTML + CSS + JavaScript. Sin base de datos, login, formularios ni pagos.
- **Datos**: el catálogo está embebido en `index.html`; no hay `fetch`, XHR ni
  WebSocket en ninguna página.
- **Terceros**: ninguno. Sin Google Fonts, sin CDN, sin analítica, sin píxeles.
- **Persistencia**: `localStorage` con una sola clave, `comparaportatil.v1`, que guarda
  perfil y los dos modelos elegidos.
- **Build**: scripts de Python que se ejecutan en local. No se ejecutan en el sitio.

## Comprobaciones hechas

| Prueba | Resultado |
| --- | --- |
| Claves, tokens y contraseñas en el repo y en todo el historial de git | 0 coincidencias |
| `http://` en páginas publicadas (contenido mixto) | 0 |
| Formularios, `iframe`, `object`, `embed` | 0 |
| `eval`, `new Function`, `document.write` | 0 |
| Manejadores inline (`onclick=`, `onerror=`…) | 0 |
| `innerHTML` con datos de la URL | No: `?a=` y `?b=` se validan contra los IDs del catálogo |
| Metadatos EXIF en las 36 imágenes | 0 |
| Enlaces externos | GitHub con `rel="noopener"` |
| `404.html` | `noindex, follow` |
| Dependencias de terceros en el frontend | Ninguna |

## Hallazgos

### S1 — El vault y los scripts son públicos (riesgo medio)

GitHub Pages publica todo el repositorio, no solo las páginas del sitio. Hoy se puede
acceder a:

```
https://raulft721.github.io/portatiles/notas/Tareas.html
https://raulft721.github.io/portatiles/notas/Inicio.html
https://raulft721.github.io/portatiles/AGENTS.md
https://raulft721.github.io/portatiles/README.md
https://raulft721.github.io/portatiles/scripts/generar.py
https://raulft721.github.io/portatiles/scripts/og-manifest.json
```

No hay secretos, pero sí información interna: tareas pendientes, decisiones, nombres de
archivos y la estructura del proyecto. Además, Jekyll convierte las notas en páginas
HTML que Google puede rastrear aunque no estén enlazadas ni en el sitemap.

**Solución recomendada**, sin sacar el vault del repo: añadir un `_config.yml` en la
raíz con una lista `exclude` para `notas`, `scripts`, `AGENTS.md` y `README.md`. Jekyll
deja de publicarlos y el vault sigue funcionando en Obsidian. Hay que comprobar después
que la web y las imágenes OG siguen sirviéndose.

Alternativas: mover el vault a un repositorio privado o dejarlo como está asumiendo que
es público. **No meter nunca una nota con datos personales, correos o capturas de
cuentas mientras esto siga así.**

### S2 — Faltan cabeceras de seguridad (riesgo bajo)

GitHub Pages solo envía HSTS. No se puede configurar CSP, `X-Frame-Options`,
`X-Content-Type-Options`, `Referrer-Policy` ni `Permissions-Policy` desde el
repositorio.

Mientras el sitio sea estático y sin terceros, el riesgo es bajo. Se puede añadir una
CSP parcial con `<meta http-equiv="Content-Security-Policy">`, sabiendo que
`frame-ancestors` no funciona en `meta` y que `report-uri` tampoco.

Propuesta para el estado actual (probar que no rompe el JS inline ni el JSON-LD):

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; object-src 'none'; base-uri 'self'; form-action 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
```

Con dominio propio y Cloudflare se pueden poner cabeceras reales (CSP, `X-Frame-Options:
DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`). Es
la vía buena, pero primero hay que probar que los anuncios de AdSense siguen cargando.

### S3 — Enlaces externos sin `noreferrer` (riesgo bajo)

El enlace a GitHub lleva `rel="noopener"`, que evita el acceso a `window.opener`. Añadir
`noreferrer` evita además enviar la URL de origen. Es cosmético, pero es gratis.

### S4 — El correo personal está en el historial de git (riesgo bajo)

Los commits están firmados con `raulferrestorres1@gmail.com`, que es público en
GitHub. No es una vulnerabilidad, pero alimenta el spam y une identidad personal con el
proyecto. Para el futuro: usar el correo noreply de GitHub
(`ID+usuario@users.noreply.github.com`). No reescribir la historia por esto.

### S5 — No hay política de divulgación de vulnerabilidades (riesgo bajo)

En un proyecto pequeño no es urgente, pero queda bien y es útil: un `SECURITY.md` en el
repo diciendo cómo avisar de un problema y qué se considera dentro de alcance. También
se puede publicar `/.well-known/security.txt`, aunque en un project site la ruta
correcta sería la del dominio raíz.

### S6 — Seguridad de la cuenta de GitHub (estado desconocido)

No se puede comprobar desde aquí. Checklist:

- [ ] 2FA o passkey activados.
- [ ] Correo de recuperación y códigos de respaldo guardados.
- [ ] Claves SSH y tokens revisados; revocar los que no se usen.
- [ ] Aplicaciones OAuth con acceso al repo revisadas.
- [ ] `main` protegida: sin force-push y, si hay CI, con checks obligatorios.
- [ ] Secret scanning y push protection activados (gratis en repos públicos).
- [ ] Private vulnerability reporting activado.
- [ ] Revisar colaboradores y despliegues de Pages.

### S7 — Imágenes de fabricante (riesgo legal, no técnico)

Las 36 fotos son de los fabricantes. Es habitual y se atribuyen, pero no equivale a
tener licencia. Si un fabricante reclama, hay que retirarlas. Para AdSense conviene
tener una alternativa propia o con licencia, al menos para las fichas principales.

### S8 — El servidor local de pruebas (riesgo local)

`python -m http.server 8000` escucha en todas las interfaces por defecto. En una red
pública, cualquiera puede leer los archivos de la carpeta. Usar siempre:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

### S9 — AdSense introduce terceros (riesgo medio, futuro)

Hoy no hay ningún script externo; con AdSense habrá varios. Eso cambia el modelo:

- Hay que actualizar la CSP para permitir los dominios de Google, o dejar de tener CSP.
- Hay que activar un CMP certificado y consentimiento para el EEE, Reino Unido y Suiza.
- Los anuncios los sirve Google, pero la responsabilidad de la política de contenido es
  del editor.
- Nunca hacer clic en los anuncios propios ni pedir clics. Google lo detecta y cierra
  la cuenta.
- Revisar el «Centro de políticas» de AdSense con frecuencia.

### S10 — Dependencias futuras (riesgo bajo ahora)

No hay librerías. Si algún día se añade una (por ejemplo, para gráficos), que sea por
CDN con `integrity` (SRI) y versión fijada, o mejor autohospedada. Sin Node ahora
mismo, cuanto menos, mejor.

## Reglas para no crear el problema

- **Todo lo que llega al navegador es público.** Nunca poner una clave de API en el
  frontend, aunque esté «ofuscada».
- Si hace falta una API, que sea serverless (Cloudflare Workers, Vercel, etc.) con la
  clave en el servidor, límites de uso y validación de entrada.
- Formularios: usar un proveedor con captcha y no un endpoint propio sin protección.
- `textContent` para datos externos; `innerHTML` solo con datos propios y escapados.
- Revisar enlaces externos: `rel="noopener noreferrer"`.
- Publicar solo lo necesario. Lo que no debe ser público, fuera de la carpeta publicada
  o en `exclude`.
- Antes de cada publicación: `python scripts/auditar-seo.py` y revisar `git status`.
- Revisar accesos y tokens una vez al año.

## Checklist de seguridad

- [ ] Añadir `_config.yml` con `exclude` para notas y scripts.
- [ ] Confirmar que las notas ya no responden en producción.
- [ ] Añadir CSP en `meta` y `referrer` (o cabeceras reales con Cloudflare).
- [ ] Añadir `noreferrer` al enlace de GitHub.
- [ ] Crear `SECURITY.md` con el canal de aviso.
- [ ] Revisar 2FA, tokens y protección de `main`.
- [ ] Activar secret scanning y private vulnerability reporting.
- [ ] Documentar el uso de `--bind 127.0.0.1` en las notas.
- [ ] Revisar la licencia de las imágenes.
- [ ] Repetir esta revisión cuando se añada AdSense o cualquier script externo.

## Relacionado

- [[Mejoras/AdSense|AdSense]]
- [[Mejoras/Legal|Legal]]
- [[Contexto/Publicacion|Publicación]]
