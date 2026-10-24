# ComparaPortátil

Prototipo de comparador de portátiles: elige un perfil de uso, compara dos modelos y consulta qué gana según estudio, trabajo, gaming o movilidad, con el precio sobre la mesa.

## Demo

Página estática, sin backend ni dependencias. Los datos viven en `index.html` y las fotos en `img/`.

## Uso local

Abre `index.html` en el navegador o sirve la carpeta:

```bash
python -m http.server 8000
```

Y visita `http://localhost:8000`.

## Estructura

```
index.html   → interfaz, estilos y lógica (todo en uno)
guias/       → dos guías de compra con su propia hoja de estilos
img/         → fotos ilustrativas (Unsplash)
404.html     → página de error
```

## Aviso

Proyecto de prueba. Precios orientativos y fotos de stock que no corresponden necesariamente al modelo exacto. No es una recomendación de compra.
