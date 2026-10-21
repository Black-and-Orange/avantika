---
name: avantika-design
description: Sistema de diseño de Avantika (servicios de TI y ciberseguridad, México) armado por Black & Orange — logos, paleta, tipografías, íconos, fotos del equipo, fondos, tokens CSS, componentes React, UI kit, arquetipos de piezas y reglas de contenido. Úsala siempre que vayas a diseñar, escribir o revisar cualquier cosa de Avantika: landing, sitio, post o carrusel de LinkedIn, story, banner, presentación, mailing, prompt de imagen, maqueta en HTML o código de producción, aunque no se mencione «sistema de diseño». También para revisar si una pieza de Avantika respeta la marca. Use it for any Avantika (avantika.mx, «Cybersecurity») design, copy or brand-compliance task.
---

# Avantika · sistema de diseño

Avantika es una empresa mexicana de **servicios de TI y ciberseguridad** para empresas: soporte y mesa de ayuda, ciberseguridad, gestión de TI, infraestructura y adopción segura de IA. Su logotipo lleva el tagline *Cybersecurity*.

Este paquete lo armó Black & Orange el 13 de octubre de 2026 y se actualizó el 20 de octubre. Su página de revisión, con todo explicado y visible, está en https://black-and-orange.github.io/avantika/

## Lo primero que tienes que saber

**No existe manual de marca.** Del cliente vienen *archivos*: logos, un PDF de color, dos tipografías, íconos, fondos, una sesión de fotos y doce piezas de LinkedIn. Casi todo lo demás (para qué sirve cada color, qué tipografía va en titulares, tamaños, componentes, composición de piezas, voz y reglas de contenido) es **propuesta de Black & Orange sin aprobar**. Cuando expliques una decisión a alguien, distingue entre «viene del cliente» y «es propuesta»; no presentes una propuesta como regla oficial. Lo que falta pedir está en `references/pendientes.md`.

**Ningún dato comercial está validado.** Disponibilidad, SLA, tiempos de respuesta, horario de monitoreo, cobertura, precios, clientes, certificaciones y contacto van siempre como `[Dato por validar]`. Las piezas de LinkedIn del cliente dicen «Disponibilidad 99%», «Monitoreo 24/7», «Cobertura nacional» y «diagnóstico sin costo»; no las repitas sin validación escrita, porque en ciberseguridad esas promesas suelen estar en contrato.

## Identidad en una pantalla

| Tema | Qué usar | Origen |
|---|---|---|
| Logotipo | PNG de `assets/` sin recolorear, redibujar ni recomponer. Sobre claro: `logo-avantika-negro.png` o `logo-avantika-tagline-negro.png`. Sobre navy o negro: `logo-avantika-blanco.png` o `logo-avantika-tagline-blanco-azul.png` (tagline en cian). | Archivos del cliente; usos, propuesta |
| Isotipo | `isotipo-avantika-blanco.png`. Solo existe en blanco: solo sobre oscuro. | Cliente |
| Color | Cian `#00F5D4` · púrpura `#87007D` · magenta `#FF005E` · blanco azulado `#F4FAFF` · navy `#011E5E` | PDF de color (el PDF rotula mal el HEX del cian; usa `#00F5D4`) |
| Roles de color | Fondo blanco azulado, texto y botones navy, púrpura secundario (cierres, badges, números), magenta solo en plecas y detalles, cian solo sobre oscuro | Propuesta |
| Tipografía | Nebulica (titulares, bold, altas y bajas) y Swiza (textos; light, regular y semibold) | Archivos del cliente; funciones, propuesta |
| Íconos | 34 PNG en `assets/icons/`, en `#071436`, con marco circular. Nunca por debajo de 48 px. | Cliente |
| Imagen | Fotos del equipo (`assets/imagery-foto-*`) y fondos abstractos (`assets/imagery-layout-*`). Siempre sin filtros y sin texto encima: el texto va en una banda sólida aparte. | Cliente; uso, propuesta |
| Forma | Esquinas rectas (radio 0; 4 px en controles), filetes de 1 px en lugar de sombras, espaciado en múltiplos de 8 | Propuesta |

### Contraste: lo que sí y lo que no

Funciona: navy sobre blanco azulado (14.8:1), blanco azulado sobre púrpura (8.6:1), cian sobre navy (11.1:1). **No funciona**: cian sobre claro (1.33:1; por eso el archivo `logo-avantika-tagline-negro-azul.png` no se usa sobre fondos claros), púrpura sobre navy (1.72:1) y texto claro sobre magenta (3.69:1). El magenta no es color de texto. Los pares completos están en `references/contraste.json`.

## Cómo empezar según lo que te pidan

**Maqueta o página en HTML.** Enlaza `styles.css` (importa todos los tokens) y usa las variables `--av-*` en lugar de HEX sueltos. Copia los assets que necesites conservando la ruta relativa. `ui_kits/website/` es una landing completa de referencia (React por CDN, se sirve por http): héroe navy con la foto del centro de monitoreo, servicios en lista, historia en tres pasos, equipo con su visión y cierre púrpura.

**Código de producción en React.** Los componentes están en `components/core/` (Button, Badge, Card, Divider) y `components/forms/` (Input, Select, Checkbox). Cada uno trae su `.jsx`, sus tipos en `.d.ts` y un `.prompt.md` con el uso correcto. Usan solo variables de `tokens/`.

**Post, carrusel o story.** Lee `references/arquetipos.json`. Hay cuatro modos: tarjeta tipográfica (A1), fondo de marca con banda navy (A2), cierre centrado sobre púrpura o navy (A3) y foto del equipo con banda (A4). Márgenes de 80 px; en 9:16, 250 px libres arriba y 340 abajo. El formato de LinkedIn que usa el cliente es 3:4 (1080 × 1440).

**Prompt para un modelo de imagen.** Antepón los bloques de `references/prompts-imagen.json` y respeta `references/reglas.md`. El arte final no debe inventar personas, oficinas ni pantallas con texto: usa las fotos reales como referencia o los fondos oficiales.

**Textos.** Lee la sección de voz de `references/sistema.md`. La voz que proponemos sale de las piezas del cliente: de tú, frases cortas, desde el problema del negocio («Lunes, 9 am. El sistema cayó. Nadie responde.») y con acompañamiento («Nosotros cuidamos tu espalda.»). CTA propuesto: «Agenda tu diagnóstico». La visión de la empresa, rotulada en su oficina, sí es texto del cliente: «Nuestra visión es ser la compañía de Ciberseguridad & TI preferida en México por su confiabilidad, participación de mercado y ecosistema único de formación de especialistas.» Textos literales de las piezas: `references/textos-linkedin.md`.

**Revisar una pieza.** Compárala con la tabla de arriba y con `references/reglas.md`. Errores frecuentes, que ya aparecen en las piezas de LinkedIn del cliente: violeta fuera de paleta, tipografías ajenas, logotipo recompuesto con un isotipo con degradado, tagline cian sobre fondo claro y cifras sin respaldo.

## Tipografías: no vienen en este paquete

Las licencias de Swiza (atipo) y Nebulica (Zarma Type) no permiten redistribuir los archivos, y la de Swiza no cubre uso web. `tokens/fonts.css` las busca **instaladas** en el equipo con `local()`; si no están, el navegador cae a Helvetica Neue o Arial y lo que veas no será fiel. Para producir con fidelidad, pide las fuentes a Black & Orange e instálalas. Nunca las subas a un repo, a un drive público ni a un sitio. Hay especímenes en imagen en `assets/tipo/`. Detalle en `assets/fonts/LEEME.md`.

## Fotos del equipo

Hay 22 fotos seleccionadas de una sesión de 272 (23 de diciembre de 2025): centro de monitoreo y oficina, manos en el teclado, retratos sobre fondo blanco y negro, y el evento del equipo. **Todavía no hay autorización de uso de imagen** de las personas que aparecen: sirven para maquetas internas, no para pauta, sitio ni redes hasta que el cliente la confirme. Las de manos en el teclado (`imagery-foto-detalle-teclado-*`) no muestran rostros. Las pantallas del centro de monitoreo muestran tableros reales; no las uses en recortes grandes sin revisarlas.

## Mapa del paquete

| Ruta | Qué es |
|---|---|
| `styles.css`, `tokens/` | Tokens CSS: color, tipografía, fuentes, espacio y efectos. Única fuente de verdad. |
| `assets/` | Logos, isotipo, `icons/`, `elementos/` (ventanas, triángulos, patrón), `tipo/` (especímenes) e imágenes `imagery-*` a 1800 px |
| `components/` | Componentes React con tipos y guía de uso |
| `guidelines/` | Tarjetas HTML de marca, color, tipografía, espacio y efectos |
| `ui_kits/website/` | Landing y contacto de referencia |
| `references/sistema.md` | El sistema completo explicado (léelo para cualquier trabajo de más de una pieza) |
| `references/reglas.md` | Seis reglas de contenido y marca, listas para un prompt |
| `references/arquetipos.json` | Modos de pieza para redes |
| `references/prompts-imagen.json` | Bloques maestros para prompts de imagen |
| `references/perfil.md` | Perfil de marca en una página |
| `references/textos-linkedin.md` | Transcripción de las 12 piezas de LinkedIn del cliente |
| `references/pendientes.md` | Lo que falta pedir o definir, por prioridad |
| `references/contraste.json` | Pares de color con su uso y mínimo |
