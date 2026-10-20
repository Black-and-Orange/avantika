# Evidencia y decisiones · Avantika

Revisión del 13 de octubre de 2026. Cada decisión está en uno de cuatro estados:
documentado (la fuente lo dice), derivado (transformación reproducible de una fuente),
propuesto (decisión nueva de BnO para uso digital) o pendiente (falta o se contradice).

## Fuentes revisadas

| Fuente | Ubicación | Qué aporta |
|---|---|---|
| PDF de color | `brand/uploads/Avatika-color (2).pdf`, 1 página, Illustrator 29.2, 18 feb 2025 | Cinco colores con nombre y HEX |
| Paleta en PNG | `brand/uploads/Paleta de color Avantika.png`, 1024 × 1536 | Seis HEX; contradice al PDF |
| Logos | `brand/assets/logo-avantika-*.png`, `isotipo-avantika-blanco.png` | 8 PNG, 7 de ellos «@4x» |
| Íconos | `brand/uploads/4x.zip` → `brand/assets/icons/` | 34 PNG de 522 × 521 |
| Elementos | `brand/assets/elementos/` | 4 ventanas y triángulo (SVG, PNG) y patrón (PNG) |
| Fondos | `references/layout-01..12.png` | 12 PNG, 11 distintos |
| Isotipo ilustrado | `references/isotipo-*.png|jpg` | 6 archivos |
| Mockups | `references/mockup-*.jpg` | 8 montajes de aplicación |
| Papelería | `brand/uploads/Avantika hoja membretada.pdf` | 1 página, isotipo raster en grises |
| Tipografías | carpeta local `brand/assets/fonts/` (no publicada) | Nebulica (Zarma Type, 2024) y Swiza (atipo, 2025) |
| Licencia | `brand/uploads/Tipografías/Swiza_desktop_license.pdf` | Términos de uso de Swiza |
| Piezas | `references/post-linkedin-01..12.png` | 12 imágenes de LinkedIn |
| QR | carpeta local `references/qr-*.png` (no publicada) | 5 códigos; destino sin leer |
| Fotos del equipo | carpeta local `brand/assets/Fotos Avantika 1|2/` (no publicada), inventario en `source/fotos.json` | 272 fotos del 23 dic 2025, compartidas el 20 oct 2026; 22 derivadas en `brand/assets/imagery-foto-*.jpg` |
| Illustrator | `brand/uploads/*.ai`, `AI.zip` | 3 sin contenido PDF; `Layoutd.ai` (12 páginas) sí abre |
| matriz-ads | `clients/` (consultado el 13 de octubre de 2026) | Estructura de carpetas; no hay marca madre ni hermana de Avantika |
| boma-riviera | repo y página modelo (commit 32c9cc4) | Formato de la revisión y de los archivos |

## Documentado

- Colores del PDF, con su nombre: Deep purple `87007d`, Vibrant magenta red `ff005e`, Soft white blue `f4faff`, Deep navy blue `011e5e`.
- Licencia de Swiza: uso personal y comercial en una ubicación y hasta 5 equipos; no redistribuir, no modificar, no convertir a webfont.
- Metadatos de Nebulica: «Copyright © 2024 by Zarma Type Foundry. All rights reserved.», licencia en zarmatype.com/license.
- Textos de las 12 piezas de LinkedIn (transcritos en `campaigns/linkedin-set-6-posts/guion.md`).
- Visión rotulada en el muro de la oficina (fotos `10038.JPG` y `10039.JPG`): «Nuestra visión es ser la compañía de Ciberseguridad & TI preferida en México por su confiabilidad, participación de mercado y ecosistema único de formación de especialistas.»
- Letrero «YOU CAN · END OF STORY» en la oficina (`10024.JPG`, `1001.JPG`) y tarjeta del evento «Gracias por tu colaboración. Tu compromiso hace que las cosas sucedan.» con #ValoresAvantika y #YouCan (`10091.JPG`).

## Derivado

- Cian `#00F5D4`: el PDF lo rotula `87007d`. El valor sale del color medido en los dos logos «azul» (píxel opaco más
  frecuente después del blanco o negro) y de la etiqueta `#00f5d4` de la paleta en PNG. El triángulo cian del PDF coincide a la vista.
- Tinta `#1D1D1B`, negro `#000000`, azul de íconos `#071436`, violeta de las piezas `#9E009C`: píxel opaco más frecuente, medido con Pillow.
- El tagline está en Swiza Light: se compuso «Cybersecurity» con el archivo de la fuente y se comparó con el logotipo
  (`img/tipo/tagline-vs-swiza.png`). La firma de correo usa Nebulica por la forma de la «z» y de la «a»; es lectura visual.
- RGB de la paleta: conversión directa del HEX. El PDF no da RGB, CMYK ni Pantone.
- Filete `#CDD7E5` (navy al 16 % sobre blanco azulado), filete inverso `#4A608E` (blanco azulado al 30 % sobre navy),
  navy hover `#011646`, placeholder `#62769E` (navy al 60 % sobre blanco azulado).
- `brand/assets/imagery-*.jpg`: copias JPG a 1800 px de lado mayor, calidad 80, con Pillow. Los PNG con transparencia se
  aplanaron sobre blanco azulado o tinta. Cuatro mockups con datos de una persona se redujeron a 640 px (360 px las tarjetas) para que correo, teléfono y dirección no se lean; nombre y cargo siguen siendo legibles.
- `brand/bg/`: páginas de los PDF exportadas con `pdftoppm` y la paleta PNG pasada a JPG.
- `img/logos/`: logos reducidos a 1200 px de ancho. `img/tipo/`: especímenes compuestos con los archivos de fuente.
- Contraste: fórmula WCAG 2 sobre los HEX de `tokens/colors.css`, en `source/build.py`; el validador lo recalcula.
- `brand/assets/imagery-foto-*.jpg`: 22 fotos de la sesión, a 1800 px, calidad 80, con la orientación EXIF aplicada. La selección es de BnO: cubre oficina, detalle, retratos y equipo, y deja fuera fotos con niños o con bebidas como tema principal.
- Todo lo anterior se reproduce con `source/prepare_assets.py`.

## Propuesto

- Roles de color y el nombre corto «hielo» para Soft white blue.
- Nebulica para titulares y Swiza para textos; escala, pesos e interlíneas.
- Escala de espacio base 8, radios 0 y 4 px, filetes en lugar de sombras, degradados solo con los fondos entregados.
- Márgenes de pieza y formatos; banda navy sólida en lugar de escribir sobre los fondos.
- Usos correctos e incorrectos del logotipo; posición de la firma.
- Componentes web, landing, tres modos de post y dos verticales.
- Voz, llamado a la acción y las seis reglas provisionales.
- Criterio fotográfico: fotos tal cual, retrato oscuro para piezas y claro para el sitio, texto siempre en banda aparte; arquetipo A4.

## Pendiente y contradicciones

- No hay manual de marca. La carpeta «5. Elementos visulaes» sugiere que existen las carpetas 1 a 4.
- PDF de color contra paleta PNG: navy `#011E5E` contra `#16213A`; el PNG agrega `#1C1C1E`. Criterio provisional: rige el PDF.
- Dos negros en los logos (`#000000` y `#1D1D1B`), mezclados en `tagline-negro`.
- `tagline-negro-azul` deja el tagline a 1.33:1 sobre claro. Se conserva sin recolorear y se marca como uso a evitar.
- `logo-avantika-completo-blanco` (1000 × 669) compone el tagline en otra tipografía. Se conserva y se marca.
- `Layouts-06.png` y `Layouts-07.png` son idénticos (sha256 d5766d2ce7f1…).
- Las 12 piezas de LinkedIn no usan paleta, tipografías ni logotipo de archivo, y traen cifras sin respaldo.
- Dominio: avantika.mx (piezas, paleta PNG) contra avantika.com.mx (correos en mockups).
- Licencias: Swiza sin uso web; Nebulica sin comprobante. Por eso las fuentes no se publican.
- QR sin leer; tres `.ai` sin abrir; sitio avantika.mx sin revisar. Una foto muestra el sitio con una página «Cyber360» y un botón rojo fuera de paleta.
- Fotos: sin autorización de uso de imagen confirmada; las pantallas del centro de monitoreo muestran tableros reales.
- Cliente, equipo, consultor y aprobador: sin confirmar.
- La lista completa, con prioridad y responsable, está en la sección «Huecos por completar» de `index.html`.
