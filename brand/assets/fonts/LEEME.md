# Fuentes de Avantika — no se distribuyen en este repo

El cliente entregó dos familias. Ninguna licencia permite redistribuir los archivos, así que **no están
en el repo público**: viven solo en la carpeta local de trabajo (`brand/assets/fonts/Swiza/` y
`brand/assets/fonts/Nebulica/`, excluidas en `.gitignore`).

| Familia | Fundición | Archivos recibidos | Licencia |
|---|---|---|---|
| Swiza | atipo® (2025) | 14 OTF: Thin a Bold, con itálicas | `Swiza_desktop_license.pdf`: escritorio, hasta 5 equipos en una ubicación. Prohíbe redistribuir, modificar y **convertir a formatos webfont**. |
| Nebulica | Zarma Type Foundry (2024) | 9 OTF (Thin a Black), 8 TTF y 1 variable | No viene licencia en la carpeta. El archivo dice «All rights reserved» y remite a https://zarmatype.com/license/ |

## Cómo verlas

Instala las fuentes en tu equipo. `../../tokens/fonts.css` las busca con `local()`; si no están, el
navegador usa el fallback de `../../tokens/typography.css` (Helvetica Neue o Arial).

Los especímenes de `../../ui_kits/revision/img/tipo/` son imágenes hechas con las fuentes reales, para
que la revisión las muestre aunque no estén instaladas.

## Pendiente con el cliente

- Licencia web de Swiza (o una alternativa) antes de usarla en un sitio.
- Comprobante de licencia de Nebulica y su alcance.
- Faltan `Nebulica-Thin.ttf` (solo viene en OTF) y las itálicas de Nebulica, si existen.
