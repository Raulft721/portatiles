# ComparaPortátil

Prototipo de comparador de portátiles: elige un perfil de uso, compara dos modelos y consulta qué gana según estudio, trabajo, gaming o movilidad, con el precio sobre la mesa.

## Demo

Página estática, sin backend ni dependencias. Los datos viven en `index.html` y cada modelo usa una fotografía de producto guardada en `img/`.

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
img/         → fotos de producto de los 22 modelos y dos imágenes de ambiente
404.html     → página de error
```

## Aviso

Proyecto de prueba. Precios orientativos. Las fotografías son imágenes de producto de cada fabricante y se usan únicamente con fines informativos; los derechos pertenecen a sus respectivas marcas. No es una recomendación de compra.
