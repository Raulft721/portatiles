# ComparaPortátil

Comparador de portátiles: elige un perfil de uso, compara dos modelos y consulta qué gana según estudio, trabajo, gaming o movilidad, con el precio sobre la mesa.

## Demo

Página estática, sin backend ni dependencias. Los datos viven en `index.html` y cada modelo usa una fotografía de producto guardada en `img/`.

## Uso local

Sirve la carpeta (recomendado):

```bash
python -m http.server 8000
```

Y visita `http://localhost:8000`. También puedes abrir `index.html` directamente, pero
los enlaces a la portada desde las fichas están pensados para funcionar con un servidor.

## Estructura

```
index.html   → interfaz, estilos, lógica y datos del catálogo
portatil/    → una ficha estática por modelo (generada)
guias/       → dos guías de compra
img/         → fotos de producto de los 34 modelos y dos imágenes de ambiente
scripts/     → generación, comprobaciones de enlaces y auditoría SEO
notas/       → vault de Obsidian con contexto y tareas
404.html     → página de error
```

## Notas y tareas

El contexto del proyecto y el checklist de pendientes viven en `notas/`, pensado para
abrirse como vault de Obsidian (**Abrir carpeta como vault** → `notas/`). El punto de
entrada es `notas/Inicio.md` y las tareas están en `notas/Tareas.md`.

## Comprobaciones

```bash
python scripts/generar.py
python scripts/comprobar-enlaces.py
python scripts/auditar-seo.py --live
```

## Aviso

Precios orientativos de referencia. Las fotografías son imágenes de producto de cada fabricante y se usan únicamente con fines informativos; los derechos pertenecen a sus respectivas marcas. No es una recomendación de compra.
