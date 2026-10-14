# Handoff — sistema de diseño inicial y estructura Matriz · 2026-10-13

## Qué se hizo
- Se revisó todo el material entregado, archivo por archivo y visualmente: 8 logos, PDF de color y paleta en PNG, tipografías Nebulica y Swiza con la licencia de Swiza, 34 íconos, 12 fondos, 6 ilustraciones del isotipo, ventanas y patrón, 8 mockups, hoja membretada, 5 QR, 4 archivos de Illustrator y 12 piezas de LinkedIn.
- Se armó el repo con la estructura de cliente de matriz-ads: `brand/`, `campaigns/`, `operacion/`, `references/`, `brand-profile.md`, `client.json`, más `index.html` y `.nojekyll` para GitHub Pages.
- Dentro de `brand/`: tokens en cinco archivos, 13 tarjetas de `guidelines/`, 7 componentes React en `components/`, UI kit en `ui_kits/website/`, `arquetipos.json`, `matrix-blocks.json` y reglas consolidadas.
- Se armó la página de revisión (`brand/ui_kits/revision/`, generada con `source/build.py`) con 14 secciones, estados De la guía / Propuesta BnO / Falta, contraste calculado y 29 pendientes priorizados.
- Se dio de alta la campaña `linkedin-set-6-posts` con la transcripción de las piezas recibidas.
- Se buscó una marca madre o hermana en `Black-and-Orange/matriz-ads`: no hay ninguna de Avantika.
- Se subió a `Black-and-Orange/avantika` (rama `main`, repo público) y se activó GitHub Pages desde `main`: https://black-and-orange.github.io/avantika/

## Qué se verificó
- Página de revisión, UI kit, fichas de componentes y tarjetas de guidelines en navegador, a 1360 px y 375 px: sin imágenes rotas ni desbordes horizontales.
- Controles probados: botón de zonas de Instagram, menú de secciones en móvil, navegación y envío del formulario de muestra del UI kit.
- Validador estático de la skill sobre `brand/`: resultado en `brand/ui_kits/revision/source/package-validation.json`.
- Las copias de logos, íconos, elementos y documentos son byte a byte las del cliente (hashes en `source/provenance.json` y `references/PROCEDENCIA.md`).
- Portabilidad: en un clon limpio del repo, en otra ruta, las 239 referencias locales de HTML, CSS y JSX resuelven, no hay rutas absolutas y el validador vuelve a pasar. Es decir, la página no depende de los archivos que quedaron fuera del repo.

## Qué no
- Nada está aprobado por el cliente: roles de color, asignación tipográfica, escala, componentes, arquetipos, reglas y textos son propuesta.
- Las tipografías no están instaladas en el equipo donde se revisó: el texto vivo se vio con fallback. Los especímenes son imágenes hechas con los archivos reales.
- No se pudo leer el destino de los 5 QR ni abrir los tres `.ai` guardados sin contenido PDF.
- No se revisó el sitio avantika.mx.
- No se generó ninguna pieza con modelo ni se probó `matriz` con este cliente. `client.json` copia de boma-riviera los valores por defecto de modelo, resolución y LLM, y lo dice en `_nota`.
- Avantika no está dada de alta en el Client Hub.
- Cliente, equipo, consultor y aprobador quedaron como «sin confirmar».

## Fuera del repo público
- Fuentes Swiza y Nebulica (licencia), originales de tarjetas, firma, gafete y QR (datos personales y destino sin verificar) y `Layoutd.ai` (88 MB). Siguen en la carpeta local y están en `.gitignore`.

## Siguiente paso
Pedir al cliente el manual de marca y los vectores, resolver las licencias tipográficas y confirmar el origen de las piezas de LinkedIn antes de abrir la primera campaña.
