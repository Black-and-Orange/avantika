# Revisión del sistema de diseño · Avantika

Página interna de Black & Orange para decidir qué está completo, qué proponemos y qué falta.
Publicada en https://black-and-orange.github.io/avantika/

- `index.html` se genera: no se edita a mano. Para cambiar un texto, un pendiente o una pieza,
  edita `source/build.py` y ejecuta `python3 source/build.py` desde esta carpeta.
- Usa los tokens de `../../tokens/` (el build lee los HEX de `colors.css`; no los repite), las imágenes de
  `../../assets/imagery-*.jpg`, los íconos de `../../assets/icons/` y los documentos de `../../bg/`.
- `avantika.css` son los estilos de las maquetas de la página; `review.css` y `review.js`, la carcasa neutra.
- `img/logos/` son copias de los logos reducidas a 1200 px de ancho. Los originales están en `../../assets/`.
- `img/tipo/` son especímenes en imagen de Nebulica y Swiza: las fuentes no se distribuyen (licencia).
- `source/prepare_assets.py` documenta cómo se copió y derivó todo desde las carpetas del cliente.
- `source/evidence.md` dice de dónde sale cada decisión; `source/package-validation.json` es la última validación.

Estados: "De la guía" viene en el material del cliente, "Propuesta BnO" está por validar y "Falta" hay que pedirlo o definirlo.
No hay manual de marca: "De la guía" significa que el archivo existe, no que haya una regla escrita.
