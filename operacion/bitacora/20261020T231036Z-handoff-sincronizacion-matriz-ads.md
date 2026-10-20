---
fecha: "2026-10-20T23:10:36Z"
tipo: handoff
titulo: "Sincronización con matriz-ads"
---
# Handoff — sincronización con matriz-ads · 2026-10-20

## Pedido
«Sí, sincroniza» (la copia de `clients/avantika` en matriz-ads con las fotos y la landing nueva).

## Hecho
- Se trajeron al repo `avantika` los cambios que Carlos Tames hizo en matriz-ads el 2026-10-18 (commit 5a3282d): frontmatter de la bitácora, «Siguiente paso» en `campaigns/linkedin-set-6-posts/ESTADO.md` y `brand/example-recipes.json`. También la entrada «Alta en matriz-ads».
- Se copió el contenido versionado del repo `avantika` a `clients/avantika` en matriz-ads, sin borrar nada de allá, y se actualizó su `AGENTS.md` (fotos, autorización de imagen, 32 pendientes).

## Funciona
- Los dos repos quedan con el mismo contenido en `brand/`, `campaigns/`, `operacion/`, `references/`, `brand-profile.md` y `client.json`.

## No funciona
- No se regeneró `brand/example-recipes.json` con las fotos nuevas: lo arma el CLI de matriz y no se corrió.

## Pendientes
- Autorización de uso de imagen de las personas de las fotos.

## Siguiente paso
Correr el CLI de matriz para que las recetas incluyan las fotos, si se van a usar como referencia de generación.
