# Handoff — fotografía del equipo en el sistema · 2026-10-20

## Pedido
«Me compartieron fotos, ya las dejé dentro de assets, en brand, puedes agregarlas para uso en el design system.»

## Hecho
- Se revisaron las 272 fotos (dos carpetas de 136 y dos zip con el mismo contenido): sesión del 23 de diciembre de 2025 en oficina, centro de monitoreo, retratos sobre fondo blanco y negro, detalles de teclado y el evento del equipo.
- Se seleccionaron 22 y se derivaron a `brand/assets/imagery-foto-*.jpg` (1800 px, orientación EXIF aplicada) con `source/prepare_assets.py`. Inventario de las 272 con hashes en `brand/ui_kits/revision/source/fotos.json`.
- Página de revisión: la sección «Fotografía e imaginería» ahora muestra la fotografía del equipo y el criterio propuesto; posts con un cuarto modo «Foto del equipo con banda»; el vertical A usa dos fotos; landing con sección «Nosotros»; «Voz y tono» recoge la visión rotulada en la oficina, el letrero «YOU CAN · END OF STORY» y la tarjeta #ValoresAvantika. Pendientes: de 29 a 32.
- Nueva tarjeta `brand/guidelines/brand-photography.html`, arquetipo A4, regla 6 y bloque de prompt actualizados, UI kit con «Nosotros».

## Funciona
- Las rutas de las 22 fotos resuelven en la página, el UI kit y la tarjeta.

## No funciona
- Nada conocido.

## Pendientes
- Autorización de uso de imagen de las personas que aparecen (prioridad alta, cliente). Hasta tenerla, las fotos son para revisión interna.
- Los 272 originales siguen solo en la carpeta local, fuera del repo (`.gitignore`).
- Revisar las pantallas del centro de monitoreo antes de usar esas fotos en recortes grandes.

## Siguiente paso
Confirmar con el cliente las autorizaciones y si «YOU CAN» y la visión pueden usarse en comunicación externa.
