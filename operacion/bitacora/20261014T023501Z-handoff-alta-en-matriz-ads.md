---
fecha: "2026-10-14T02:35:01Z"
tipo: handoff
titulo: "Alta en matriz-ads"
---
# Handoff — alta de Avantika en matriz-ads · 2026-10-13

## Pedido
Subir el sistema de diseño de Avantika a `Black-and-Orange/matriz-ads`, dentro de `clients/avantika`, en la rama `main`.

## Hecho
- Se copió a `clients/avantika/` el contenido versionado del repo `Black-and-Orange/avantika` (commit 0e56498): `brand/`, `campaigns/`, `operacion/`, `references/`, `brand-profile.md` y `client.json`.
- Se agregó `AGENTS.md` de entrada para agentes, con el mismo formato que `clients/boma-riviera`.
- No se copiaron `index.html`, `.nojekyll`, `.gitignore` ni `.claude/`: solo sirven a GitHub Pages y al preview local del otro repo.

## Funciona
- La página de revisión sigue publicada desde el repo `avantika`: https://black-and-orange.github.io/avantika/

## No funciona
- No se corrió `node bin/matriz.mjs handoff avantika`, `brand` ni ningún otro comando de `matriz`: el alta se hizo copiando archivos, sin `new-client`. `client.json` no está probado contra el CLI.

## Pendientes
- Siguen fuera de cualquier repo: fuentes Swiza y Nebulica, originales de tarjetas, firma, gafete y QR, y `Layoutd.ai`.
- Fila 47 de `docs/operacion/inventario-diseno-bno.md` (Avantika, «Sin registro en repo») quedó sin actualizar.
- Avantika no está en el Client Hub. Cliente, equipo, consultor y aprobador: sin confirmar.

## Siguiente paso
Correr `node bin/matriz.mjs handoff avantika` y `doctor` en un workspace completo para confirmar que el CLI reconoce al cliente, y actualizar el inventario.
