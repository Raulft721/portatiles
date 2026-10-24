# ComparaPortátil

Prototipo de comparador de portátiles: elige un perfil de uso, compara dos modelos y consulta qué gana según estudio, trabajo, gaming o movilidad, con el precio sobre la mesa.

## Demo

Página estática, sin backend ni dependencias. Los datos viven en `index.html` y las ilustraciones de los portátiles se generan con `art.js`.

## Uso local

Abre `index.html` en el navegador o sirve la carpeta:

```bash
python -m http.server 8000
```

Y visita `http://localhost:8000`.

## Estructura

```
index.html   → interfaz, estilos y lógica (todo en uno)
art.js       → generador de ilustraciones SVG de los portátiles
guias/       → dos guías de compra con su propia hoja de estilos
img/         → dos fotos de ambiente (Unsplash)
404.html     → página de error
```

## Aviso

Proyecto de prueba. Precios orientativos. Las ilustraciones son dibujos genéricos y no representan el aspecto real de cada modelo. No es una recomendación de compra.
