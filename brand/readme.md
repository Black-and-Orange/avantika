# Avantika — Design System

Avantika es una empresa de **servicios de TI y ciberseguridad** para empresas en México. Sus piezas
de LinkedIn hablan de soporte y mesa de ayuda, ciberseguridad, gestión de TI, infraestructura y
adopción segura de IA. El logotipo lleva el tagline `Cybersecurity`.

Estado: **propuesta para comentarios, 2026-10-13**. No llegó manual de marca: lo que viene en los
archivos del cliente es identidad; todo lo demás es propuesta de BnO y está por validar.

## Fuentes

- `uploads/Avatika-color (2).pdf` — una página con cinco colores, nombre y HEX. Imagen en `bg/color-p01.png`.
- `uploads/Paleta de color Avantika.png` — segunda paleta, de seis colores, que no coincide con el PDF.
- `uploads/Avantika hoja membretada.pdf` — papelería. Imagen en `bg/hoja-membretada-p01.png`.
- `assets/logo-avantika-*.png`, `isotipo-avantika-blanco.png` — 8 PNG; no hay vector.
- `assets/icons/` — 34 íconos PNG de 522 px (de `uploads/4x.zip`).
- `assets/elementos/` — 4 ventanas y un trío de triángulos (SVG y PNG) y un patrón (PNG).
- `assets/fonts/` — Nebulica y Swiza. **No están en el repo**: ver `assets/fonts/LEEME.md`.
- `../references/` — originales renombrados: 12 fondos, 6 ilustraciones del isotipo, 8 mockups, 12 piezas
  de LinkedIn, 5 QR y logos (ver `../references/PROCEDENCIA.md`).
- `uploads/` — además, 4 archivos de Illustrator; tres no abren fuera de Illustrator.
- `assets/imagery-foto-*.jpg` — 22 fotos del equipo seleccionadas de 272 (compartidas el 2026-10-20). Los
  originales no están en el repo; inventario con hashes en `ui_kits/revision/source/fotos.json`.
- No se entregó manual, sitio, Figma, reglas de contenido ni datos comerciales. No hay marca madre ni
  marcas hermanas en matriz-ads. El UI kit, los arquetipos y las reglas son una **aplicación original**.

## Arquitectura de marca

- **Logotipo** — `AVANTIKA` en mayúsculas geométricas; la primera A es un triángulo abierto. Mide 7.6 : 1.
- **Tagline** — `Cybersecurity`, en Swiza Light, centrado debajo. Existe en una tinta y en cian `#00F5D4`.
- **Isotipo** — la A triangular. Solo existe en blanco.
- **Elementos** — trío de triángulos, cuatro «ventanas» de esquinas en chaflán y un patrón de triángulos.
- Avantika firma sola: no hay firma de casa matriz.
- No hay área de protección, tamaño mínimo, fondos permitidos ni usos incorrectos documentados.

### Archivos que no son consistentes

- `logo-avantika-tagline-negro-azul.png`: tagline cian que sobre claro queda a 1.33:1.
- `logo-avantika-completo-blanco.png`: versión apilada de 1000 px con el tagline en otra tipografía.
- Dos negros: `#000000` (logotipo sin tagline) y `#1D1D1B` (con tagline); `tagline-negro` mezcla ambos.

### Reglas de logotipo (propuesta BnO)

Correcto: negro o `#1D1D1B` de una tinta sobre blanco o blanco azulado; blanco, con o sin tagline cian,
sobre navy o negro; blanco sobre púrpura.
Incorrecto: tagline cian sobre claro, blanco sobre cian, negro sobre navy, deformado, sobre zonas claras
de un fondo, o recompuesto con otro isotipo (como en las piezas de LinkedIn). Nunca se recolorea.

## CONTENT FUNDAMENTALS

El cliente **no entregó reglas de contenido**. Lo que sigue sale de las 12 piezas de LinkedIn y es propuesta.

- **Idioma**: español de México. El tagline está en inglés.
- **Visión** (rotulada en el muro de la oficina, visible en las fotos): «Nuestra visión es ser la compañía de
  Ciberseguridad & TI preferida en México por su confiabilidad, participación de mercado y ecosistema único
  de formación de especialistas.» En la oficina y en el evento aparece además «YOU CAN · END OF STORY» y
  #ValoresAvantika; no consta si son lemas para uso externo.
- **Persona**: de tú, al dueño o director de la empresa.
- **Estructura**: titular en tres golpes cortos con el del medio resaltado (`Ordena / Protege / Crece`).
- **Punto de vista**: el problema del negocio antes que la tecnología; acompañar, no culpar.
- **Prohibido sin validación**: cifras y compromisos (`Disponibilidad 99%`, `Monitoreo 24/7`, `SLA cumplido`,
  `en todo México`, `sin costo`) y absolutos (`sin caídas`, `sin riesgos`, `imparable`).
- **Datos**: no hay ninguno validado; todo va como `[Dato por validar]`.
- **Caja**: titulares y botones en altas y bajas. Nada en mayúsculas sostenidas, salvo el logotipo.
- **CTA (propuesta BnO)**: `Agenda tu diagnóstico`.
- **Ejemplo** (textos literales de la pieza 1)
  - Eyebrow: `Soporte TI`
  - Titular: `Soporte que responde cuando lo necesitas`
  - Apoyo: `Mesa de ayuda, técnicos en sitio y en campo.`
  - CTA: `Agenda tu diagnóstico`

## VISUAL FOUNDATIONS

**Color.** Cinco colores en el PDF, con nombre y HEX: Neon cyan `#00F5D4` (el PDF lo rotula `87007d`
por error), Deep purple `#87007D`, Vibrant magenta red `#FF005E`, Soft white blue `#F4FAFF` y Deep navy
blue `#011E5E`. Roles propuestos: blanco azulado de fondo, navy primario, púrpura secundario, magenta
como acento solo en marcas pequeñas y cian solo sobre oscuro. Cian sobre claro (1.33:1), púrpura sobre
navy (1.72:1) y texto claro sobre magenta (3.69:1) no contrastan. No hay colores de estado.

**Tipografía.** *Nebulica* para titulares (700; 600 en H2 y H3) y *Swiza* para textos (400; 300 en
subtítulos; 600 en botones y etiquetas). La asignación es propuesta. `tokens/fonts.css` las busca
instaladas con `local()`; si no están, cae a Helvetica Neue o Arial. Escala propuesta: 56 / 40 / 32 /
24 / 20 / 16 / 14 / 12 px.

**Layout y espaciado (propuesta BnO).** Escala base 8, de 8 a 128 px. Contenido en una medida de
1200 px. Piezas de redes: margen de 80 px en 4:5, 3:4 y 1:1; en 9:16, 250 px libres arriba, 340 px abajo
y 80 px a los lados.

**Imagen.** Dos lenguajes. La **fotografía del equipo** (`assets/imagery-foto-*.jpg`, 22 de una sesión de
272 del 23 de diciembre de 2025): centro de monitoreo, oficina, manos en el teclado, retratos sobre fondo
blanco o negro y el evento del equipo, todos vestidos de negro. Y los **11 fondos abstractos**
(`assets/imagery-layout-*.jpg`) con degradados, desenfoque y paneles translúcidos. Las fotos van tal cual,
sin filtros ni degradados encima. El texto **no va sobre la imagen**: se usa una banda sólida navy junto a
ella. Las personas necesitan autorización de uso de imagen antes de ir a pauta o a un sitio público
(pendiente con el cliente).

**Esquinas, bordes y sombras (propuesta BnO).** Radio 0 en tarjetas, imágenes y bandas; 4 px en
controles. Profundidad con filetes de 1 px (`--av-line`, `--av-line-inverse`), sin sombras. Los
degradados no se fabrican en CSS.

## Iconografía

34 íconos en `assets/icons/`, numerados y sin nombre: pictograma sólido dentro de un doble anillo con
trazos radiales, en `#071436`. No hay versión clara ni vector utilizable. No bajar de 48 px.

## Índice

| Ruta | Qué es |
| --- | --- |
| `styles.css` | Importa todos los tokens |
| `tokens/` | `colors.css`, `typography.css`, `fonts.css`, `spacing.css`, `effects.css`: la fuente de verdad |
| `assets/` | Logos, `icons/`, `elementos/`, imágenes a 1800 px (`imagery-*.jpg`, con las fotos en `imagery-foto-*`) y `fonts/` (solo el LEEME) |
| `bg/` | Documentos del cliente como imagen |
| `guidelines/` | Tarjetas de marca, color, tipografía, espacio y efectos |
| `components/` | `core/` (Button, Badge, Card, Divider) y `forms/` (Input, Select, Checkbox) en React |
| `ui_kits/website/` | Sitio de captación de ejemplo |
| `ui_kits/revision/` | Página de revisión del sistema: cobertura, contraste, piezas y pendientes |
| `arquetipos.json` | Arquetipos de pieza para la parrilla |
| `matrix-blocks.json` | Bloques maestros de prompt |
| `reglas-consolidadas-2026-10-13.md` | Reglas propuestas para el Client Hub |
| `uploads/` | Fuentes del cliente, sin modificar |

## Reglas que el código debe cumplir

- Sin `box-shadow` como recurso de tarjeta: se usan filetes.
- Sin `linear-gradient` ni `radial-gradient` como identidad: los degradados entran con `imagery-layout-*`.
- Ningún peso de fuente arriba de 700.
- Solo dos familias: Nebulica y Swiza, por `local()`. Nunca desde un CDN ni con los archivos en el repo.
- Espaciado en múltiplos de 8.
- `--av-cyan` nunca como texto o filete sobre fondo claro; `--av-magenta` nunca como fondo de texto.
- Ningún color fuera de `tokens/colors.css`.
- Los logos e íconos se usan desde su archivo: sin `filter`, sin recolorear, sin recomponer.
