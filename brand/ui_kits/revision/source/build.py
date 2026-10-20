#!/usr/bin/env python3
"""Genera index.html (la página de revisión) y source/contrast-pairs.json.

Uso, desde brand/ui_kits/revision:  python3 source/build.py
Solo biblioteca estándar. Los textos y datos de la revisión viven en este archivo.
Los colores se leen de brand/tokens/colors.css: aquí no se repite ningún HEX de marca.
"""
import html
import json
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FECHA = "13 de octubre de 2026"
LOGOS = "img/logos/"
IMG = "../../assets/imagery-"
ICONOS = "../../assets/icons/avantika-icono-"
ELEM = "../../assets/elementos/"
L_NEGRO = LOGOS + "logo-avantika-negro.png"
L_BLANCO = LOGOS + "logo-avantika-blanco.png"
LT_BLANCO_AZUL = LOGOS + "logo-avantika-tagline-blanco-azul.png"
LT_BLANCO = LOGOS + "logo-avantika-tagline-blanco.png"
LT_NEGRO_AZUL = LOGOS + "logo-avantika-tagline-negro-azul.png"
LT_NEGRO = LOGOS + "logo-avantika-tagline-negro.png"
ISO_BLANCO = LOGOS + "isotipo-avantika-blanco.png"
COMPLETO = LOGOS + "logo-avantika-completo-blanco.png"
PH = '<span class="av-ph">[Dato por validar]</span>'

# ---------- Tokens: única fuente de verdad ----------
_css = (RAIZ.parent.parent / "tokens" / "colors.css").read_text(encoding="utf-8")
TOKENS = dict(re.findall(r"--av-([a-z-]+):\s*(#[0-9A-Fa-f]{6})", _css))
CYAN, PURPLE, MAGENTA = TOKENS["cyan"], TOKENS["purple"], TOKENS["magenta"]
HIELO, NAVY, BLANCO, TINTA = TOKENS["hielo"], TOKENS["navy"], TOKENS["blanco"], TOKENS["tinta"]
LINEA, LINEA_INV, NAVY_HOVER, PLACEHOLDER = TOKENS["line"], TOKENS["line-inverse"], TOKENS["navy-hover"], TOKENS["placeholder"]
# Valores que aparecen en el material pero NO son tokens: se muestran solo como hallazgo.
PNG_NAVY, PNG_NEGRO, POSTS_VIOLETA, ICONO_AZUL = "#16213A", "#1C1C1E", "#9E009C", "#071436"


def e(texto):
    return html.escape(texto, quote=True)


def T(plantilla, **kw):
    for k, v in kw.items():
        plantilla = plantilla.replace("{{" + k + "}}", str(v))
    faltan = re.findall(r"\{\{(\w+)\}\}", plantilla)
    assert not faltan, faltan
    return plantilla


# ---------- Contraste ----------
def _lum(hexa):
    hexa = hexa.lstrip("#")
    canales = [int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in canales]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contraste(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


# (etiqueta, uso, texto, fondo, mínimo exigido en el uso propuesto)
PARES = [
    ("Navy sobre blanco azulado", "texto y titulares sobre el fondo por defecto", NAVY, HIELO, 4.5),
    ("Blanco azulado sobre navy", "botón primario, bandas y pie", HIELO, NAVY, 4.5),
    ("Navy sobre blanco", "campos de formulario y tarjetas", NAVY, BLANCO, 4.5),
    ("Blanco azulado sobre púrpura", "banda de cierre y badges", HIELO, PURPLE, 4.5),
    ("Púrpura sobre blanco azulado", "eyebrows y números de acento", PURPLE, HIELO, 4.5),
    ("Cian sobre navy", "tagline, badge inverso y pleca sobre oscuro", CYAN, NAVY, 4.5),
    ("Cian sobre tinta", "tagline del logotipo sobre el negro de las aplicaciones", CYAN, TINTA, 4.5),
    ("Blanco azulado sobre tinta", "logotipo blanco sobre el negro de las aplicaciones", HIELO, TINTA, 4.5),
    ("Magenta sobre blanco azulado", "solo pleca, subrayado y foco; no es color de texto", MAGENTA, HIELO, 3.0),
    ("Placeholder sobre blanco", "texto de ayuda dentro de los campos", PLACEHOLDER, BLANCO, 4.5),
]
# Combinaciones que se muestran como advertencia, no como uso del sistema.
PARES_EVITAR = [
    ("Cian sobre blanco azulado", "así queda el tagline del archivo «negro-azul» sobre fondo claro", CYAN, HIELO),
    ("Cian sobre blanco", "así aparece el tagline en las piezas de LinkedIn claras", CYAN, BLANCO),
    ("Blanco azulado sobre magenta", "texto sobre un botón o banda magenta", HIELO, MAGENTA),
    ("Magenta sobre navy", "magenta como texto normal sobre bandas navy", MAGENTA, NAVY),
    ("Púrpura sobre navy", "púrpura y navy juntos sin un claro de por medio", PURPLE, NAVY),
    ("Púrpura sobre tinta", "texto púrpura sobre el negro de las aplicaciones", PURPLE, TINTA),
    ("Magenta sobre púrpura", "la combinación del patrón de la taza, como texto", MAGENTA, PURPLE),
]


def nivel(ratio):
    if ratio >= 7:
        return "AAA", ""
    if ratio >= 4.5:
        return "AA", ""
    if ratio >= 3:
        return "Solo texto grande", " av-nivel--no"
    return "No pasa", " av-nivel--no"


def filas_contraste():
    filas = []
    for etiqueta_, uso, fg, bg, _ in PARES:
        r = contraste(fg, bg)
        txt, clase = nivel(r)
        filas.append(
            '<tr><td><span class="av av-muestra" style="background:%s;color:%s">Avantika Aa</span></td>'
            '<td><b>%s</b><br>%s</td><td>%.2f:1</td><td><span class="av-nivel%s">%s</span></td></tr>'
            % (bg, fg, e(etiqueta_), e(uso), r, clase, txt))
    for etiqueta_, uso, fg, bg in PARES_EVITAR:
        r = contraste(fg, bg)
        txt, clase = nivel(r)
        filas.append(
            '<tr><td><span class="av av-muestra" style="background:%s;color:%s">Avantika Aa</span></td>'
            '<td><b>%s</b> · evitar<br>%s</td><td>%.2f:1</td><td><span class="av-nivel%s">%s</span></td></tr>'
            % (bg, fg, e(etiqueta_), e(uso), r, clase, txt))
    return "\n".join(filas)


# ---------- Piezas de carcasa ----------
ESTADOS = {"guia": "De la guía", "bno": "Propuesta BnO", "falta": "Falta"}


def marca(tipo):
    return '<span class="marca marca--%s" aria-hidden="true"></span>' % tipo


def estado(tipo, texto=None):
    extra = " estado--falta" if tipo == "falta" else ""
    return '<span class="estado%s">%s%s</span>' % (extra, marca(tipo), e(texto or ESTADOS[tipo]))


def etiqueta(tipo):
    return '<span class="etiqueta">%s%s</span>' % (marca(tipo), ESTADOS[tipo])


def bloque(ident, titulo, resumen, tipo, fuente, cuerpo, revisar=None, texto_estado=None):
    partes = ['<section class="bloque" id="%s" aria-labelledby="t-%s">' % (ident, ident),
              '<div class="bloque__cabeza"><div><h2 id="t-%s">%s</h2><p class="bloque__resumen">%s</p></div>'
              % (ident, e(titulo), resumen)]
    if tipo:
        partes.append('<div class="bloque__meta">%s<span class="fuente">%s</span></div>'
                      % (estado(tipo, texto_estado), e(fuente)))
    partes.append("</div>")
    partes.append(cuerpo)
    if revisar:
        partes.append('<div class="revisar"><h3>Para revisar</h3><ul>%s</ul></div>'
                      % "".join("<li>%s</li>" % r for r in revisar))
    partes.append("</section>")
    return "\n".join(partes)


def sub(texto, tipo=None, nota=None):
    return '<h3 class="subtitulo">%s%s%s</h3>' % (
        e(texto), " " + etiqueta(tipo) if tipo else "", " <small>%s</small>" % nota if nota else "")


def celda(fondo, logo, pie, mal=False, foto=None, estilo_logo="", clase="", pos="50% 50%"):
    interior = ""
    if foto:
        interior += '<img class="av-fondo" src="%s" alt="" style="object-position:%s">' % (foto, pos)
    interior += '<img class="av-encima" src="%s" alt="" style="%s">' % (logo, estilo_logo)
    return ('<figure class="av-celda%s"><div class="av-celda__lona %s" style="background-color:%s">%s</div>'
            '<figcaption>%s</figcaption></figure>' % (" av-celda--mal" if mal else "", clase, fondo, interior, pie))


# ---------- Datos ----------
SECCIONES = [
    ("resumen", "Resumen", None),
    ("logotipo", "Logotipo y firma", "guia"),
    ("color", "Color", "guia"),
    ("tipografia", "Tipografía", "guia"),
    ("iconos", "Íconos", "guia"),
    ("fotografia", "Fotografía e imaginería", "guia"),
    ("espaciado", "Espaciado y retícula", "bno"),
    ("componentes", "Componentes web", "bno"),
    ("landing", "Landing de ejemplo", "bno"),
    ("posts", "Posts para redes", "bno"),
    ("stories", "Story y Reel", "bno"),
    ("piezas", "Piezas producidas", "guia"),
    ("voz", "Voz y tono", "bno"),
    ("reglas", "Reglas y contenido", "falta"),
    ("huecos", "Huecos por completar", "falta"),
]

COBERTURA = {
    "logotipo": "8 PNG: logotipo en blanco y negro, cuatro versiones con el tagline Cybersecurity, isotipo en blanco y una versión apilada. No hay manual, vector ni reglas de uso.",
    "color": "5 colores con nombre y HEX en un PDF, y una segunda paleta en PNG que no coincide. El PDF rotula mal el HEX del cian. Los roles son propuesta.",
    "tipografia": "Dos familias con sus archivos: Nebulica y Swiza. Ningún documento dice para qué sirve cada una, y sus licencias no permiten redistribuirlas ni usar Swiza en web.",
    "iconos": "34 íconos en PNG de 522 px, en un solo color. Sin nombres, sin vector utilizable y sin reglas.",
    "fotografia": "272 fotos de una sesión del equipo (22 seleccionadas: oficina, detalle, retratos y equipo), 11 fondos de marca, 6 ilustraciones del isotipo y 8 mockups. Sin criterio fotográfico escrito.",
    "espaciado": "El material no define espaciado, radios ni retícula. Proponemos base 8, esquinas rectas y márgenes para 4:5 y 9:16.",
    "componentes": "No existen. Proponemos botones, campos, tarjetas y badges armados con los tokens.",
    "landing": "No hay sitio de referencia en el material. Armamos un ejemplo con placeholders donde falta dato validado.",
    "posts": "Cuatro modos de pieza en 4:5 armados con la paleta, las tipografías, los fondos y las fotos de la marca, como alternativa a las piezas recibidas.",
    "stories": "Los dos carruseles de LinkedIn recibidos, llevados a vertical 9:16 con sus mismos textos.",
    "piezas": "12 imágenes de LinkedIn: 6 posts y 2 carruseles de 3 láminas. No usan la paleta ni las tipografías de la marca, y recomponen el logotipo.",
    "voz": "No hay documento de voz. Reunimos la visión rotulada en la oficina, el lema «YOU CAN» y los textos de las piezas, y proponemos un tono a partir de eso.",
    "reglas": "El cliente no entregó reglas de contenido. Proponemos seis reglas provisionales.",
    "huecos": "Lista priorizada de lo que hay que pedir al cliente o definir internamente.",
}

FOTOS_EQUIPO = {
    "Oficina y centro de monitoreo": [
        ("foto-soc-you-can", "10024.JPG", "Centro de monitoreo", "Muro de pantallas y el letrero «YOU CAN · END OF STORY». Las pantallas muestran tableros reales: revisar antes de recortar."),
        ("foto-soc-pantallas", "1001.JPG", "Muro de pantallas", "La misma escena con el letrero en primer plano."),
        ("foto-oficina-equipo", "1007.JPG", "Mesa de ayuda", "Equipo con diademas; buena para soporte."),
        ("foto-oficina-mesa-ayuda", "10014.JPG", "Especialista en su estación", "Encuadre cerrado, mira a pantalla."),
        ("foto-oficina-especialista", "10017.JPG", "Especialista con diadema", "Luz de día, fondo limpio."),
        ("foto-oficina-laptop", "10033.JPG", "Especialista en laptop", "Perfil, deja aire a la derecha."),
        ("foto-oficina-soporte", "1009.JPG", "Soporte en escritorio", "Con diadema y dos pantallas."),
        ("foto-oficina-escritorio", "10030.JPG", "Colaboradora de espaldas", "No se ve el rostro: útil mientras no haya autorizaciones."),
        ("foto-oficina-vision", "10039.JPG", "Sala con la visión en el muro", "El texto de la visión se lee en la pared."),
    ],
    "Detalle": [
        ("foto-detalle-teclado-1", "10012.JPG", "Manos en el teclado", "Sin rostros: la más segura para pauta."),
        ("foto-detalle-teclado-2", "10013.JPG", "Teclado mecánico", "Luz de color del teclado; tono más técnico."),
        ("foto-detalle-teclado-3", "10031.JPG", "Manos en laptop", "Fondo blanco, muy limpia."),
    ],
    "Equipo": [
        ("foto-equipo-panoramica", "panoramica.jpg", "Foto grupal", "4160 × 1740, sin EXIF: la única que no viene de la cámara de la sesión."),
        ("foto-equipo-evento", "10089.JPG", "Evento del equipo", "El isotipo púrpura en la pantalla. Hay bebidas en primer plano."),
        ("foto-equipo-reconocimientos", "100148.JPG", "Reconocimientos", "Entrega de diplomas en el evento."),
    ],
}
RETRATOS = [("foto-retrato-claro-01", "10059.JPG", "Fondo blanco"), ("foto-retrato-claro-02", "10071.JPG", "Fondo blanco"),
            ("foto-retrato-claro-03", "10072.JPG", "Fondo blanco"), ("foto-retrato-claro-04", "10081.JPG", "Fondo blanco"),
            ("foto-retrato-oscuro-01", "100206.JPG", "Fondo negro"), ("foto-retrato-oscuro-02", "100216.JPG", "Fondo negro"),
            ("foto-retrato-oscuro-03", "100377.JPG", "Fondo negro")]

FONDOS = [
    ("layout-01", "layout-01.png", "3050 × 1664", "Triángulo translúcido", "Degradado magenta, púrpura y cian con efecto cristal."),
    ("layout-02", "layout-02.png", "3053 × 1666", "Interruptor y flechas", "Fondo claro con un interruptor, triángulos y líneas punteadas. Sugiere un lenguaje de interfaz."),
    ("layout-03", "layout-03.png", "3050 × 1664", "Fragmentos desenfocados", "Trozos del isotipo en púrpura y magenta sobre blanco azulado."),
    ("layout-04", "layout-04.png", "3050 × 1664", "Volumen isométrico", "Único fondo donde el cian ocupa toda la superficie."),
    ("layout-05", "layout-05.png", "3050 × 1664", "Franja diagonal", "Magenta y púrpura con un panel translúcido."),
    ("layout-06", "layout-06.png", "3050 × 1664", "Ventana sobre magenta", "Panel translúcido con la forma de la ventana 4. Layouts-07 es este mismo archivo, byte a byte."),
    ("layout-08", "layout-08.png", "3050 × 1664", "Isotipo púrpura sobre negro", "El tratamiento que usan carpetas, gafete y parabús."),
    ("layout-09", "layout-09.png", "3050 × 1660", "Malla de puntos", "Parece imagen de stock: no tiene geometría de la marca."),
    ("layout-10", "layout-10.png", "3052 × 1665", "Isotipo con barrido", "Mismo motivo que isotipo-barrido.jpg."),
    ("layout-11", "layout-11.png", "3050 × 1664", "Isotipo isométrico", "Volumen en magenta, navy y cian sobre púrpura."),
    ("layout-12", "layout-12.png", "3050 × 1656", "Ventana sobre navy", "Panel translúcido con luz azul y magenta."),
]
ISOTIPOS = [
    ("isotipo-degradado", "isotipo-degradado.png", "3666 × 4014", "Isotipo con degradado púrpura", "Fondo transparente; aquí sobre blanco azulado."),
    ("isotipo-degradado-bn", "isotipo-degradado-bn.png", "3666 × 4014", "Isotipo en escala de grises", "El de la hoja membretada."),
    ("isotipo-cristal", "isotipo-cristal.png", "2880 × 1620", "Isotipo de cristal", "Fondo transparente; aquí sobre tinta."),
    ("isotipo-cristal-escena", "isotipo-cristal-escena.jpg", "2880 × 1620", "Isotipo de cristal en escena", "Luz magenta sobre negro."),
    ("isotipo-barrido", "isotipo-barrido.jpg", "3840 × 2160", "Isotipo con barrido", "4K sobre negro."),
    ("isotipo-puntos", "isotipo-puntos.png", "2880 × 1620", "Isotipo de puntos", "Casi invisible: puntos claros muy tenues sobre transparente."),
]
MOCKUPS = [
    ("mockup-banner", "mockup-banner.jpg", "4000 × 3000", "Banner", "Logotipo con tagline sobre isotipo magenta."),
    ("mockup-parabus", "mockup-parabus.jpg", "2250 × 3000", "Parabús", "Logotipo con tagline sobre isotipo púrpura."),
    ("mockup-carpeta", "mockup-carpeta.jpg", "4500 × 3000", "Carpetas", "Negro con isotipo púrpura."),
    ("mockup-taza", "mockup-taza.jpg", "1080 × 1080", "Taza", "Patrón en magenta y púrpura. Baja resolución."),
    ("mockup-tarjetas", "mockup-tarjetas.jpg", "3000 × 2250", "Tarjetas de presentación", "Aquí a 360 px: el original trae nombre y correo de una persona y no se publica."),
    ("mockup-tarjetas-2", "mockup-tarjetas-2.jpg", "3000 × 2250", "Tarjetas, vista 2", "Aquí a 360 px por la misma razón."),
    ("mockup-firma-correo", "mockup-firma-correo.jpg", "4500 × 3000", "Firma de correo", "Aquí a 640 px: el original trae teléfono, correo y dirección, que a este tamaño no se leen."),
    ("mockup-gafete", "mockup-gafete.jpg", "1760 × 1080", "Gafete", "Aquí a 640 px: trae retrato, nombre, cargo y un código QR, que a este tamaño no se puede escanear."),
]

# Textos literales de las 12 piezas de LinkedIn recibidas (ver campaigns/linkedin-set-6-posts/guion.md).
PIEZAS = [
    (1, "Post · #SoporteTI", "Soporte que / Responde / Cuando lo necesitas"),
    (2, "Post · #Ciberseguridad", "Datos seguros / Negocio / Imparable"),
    (3, "Post · #GestiónTI", "Ordena / Protege / Crece"),
    (4, "Post · #UnSoloEquipo", "Un solo equipo / Cobertura / Nacional"),
    (5, "Post · #CyberForAI", "IA en tu empresa / Sin riesgos / Sin frenos"),
    (6, "Post · #Infraestructura", "Infraestructura / Sin caídas / Sin sorpresas"),
    (7, "Carrusel A · 01/03", "Lunes, 9 am / El sistema cayó / Nadie responde"),
    (8, "Carrusel A · 02/03", "Nadie / falló / Creciste"),
    (9, "Carrusel A · 03/03", "Hoy, tu empresa / no se detiene."),
    (10, "Carrusel B · 01/03", "Tu empresa ya usa IA. / ¿Sabes qué datos le está dando?"),
    (11, "Carrusel B · 02/03", "La IA no es el riesgo. / Los accesos sin control, sí."),
    (12, "Carrusel B · 03/03", "Tú sigue corriendo. / Nosotros cuidamos tu espalda."),
]

# Verticales: los dos carruseles recibidos, con sus textos literales. (fondo, posición, titular, apoyo)
VERTICALES = [
    ("Vertical A · «Nadie falló. Creciste.»", [
        ("foto-detalle-teclado-1", "50%", "Lunes, 9 am. El sistema cayó. Nadie responde.", "Ventas detenidas. Clientes esperando. Y tú, sin saber a quién llamar."),
        ("layout-05", "30%", "Nadie falló. Creciste.", "Tu empresa avanzó más rápido que tu tecnología."),
        ("foto-soc-you-can", "30%", "Hoy, tu empresa no se detiene.", "Un solo equipo ordena, protege y monitorea tu TI."),
    ]),
    ("Vertical B · «La IA no es el riesgo»", [
        ("layout-09", "40%", "Tu empresa ya usa IA. ¿Sabes qué datos le está dando?", "Tu equipo conecta copilotos y automatizaciones todos los días. Y eso es bueno."),
        ("layout-06", "50%", "La IA no es el riesgo. Los accesos sin control, sí.", "Datos sensibles en herramientas abiertas."),
        ("layout-08", "50%", "Tú sigue corriendo. Nosotros cuidamos tu espalda.", "Protegemos tus datos para que adoptes IA sin frenar tu operación."),
    ]),
]

REGLAS_BNO = [
    "Toda cifra o compromiso de servicio (disponibilidad, tiempos de respuesta, SLA, horario de monitoreo, cobertura, precio, «sin costo») se escribe solo si el cliente la validó por escrito. Si no, va como [Dato por validar] o no va.",
    "No prometer resultados absolutos de seguridad: «sin riesgos», «sin caídas», «100 % seguro» o «imparable» necesitan aprobación expresa del cliente, porque en ciberseguridad son promesas difíciles de sostener.",
    "No nombrar clientes, marcas de fabricantes ni certificaciones sin autorización y comprobante.",
    "El logotipo y el isotipo se insertan desde su archivo oficial, sin redibujar, recolorear ni recomponer. El tagline en cian solo sobre fondos oscuros.",
    "Solo los cinco colores de la paleta y las dos tipografías de la marca. Los degradados entran únicamente con los fondos entregados.",
    "Personas en imagen solo con la fotografía propia del equipo, con autorización de uso de imagen, o con fotografía con licencia. Nunca imágenes generadas con IA presentadas como el equipo o las oficinas de Avantika.",
]

# (título, qué pasa, acción, prioridad, quién)
HUECOS = [
    ("Manual de marca",
     "No hay guía ni manual. Recibimos archivos sueltos y una carpeta llamada «5. Elementos visulaes», lo que sugiere que existen las carpetas 1 a 4 (probablemente logotipo, color, tipografía y aplicaciones) y no llegaron.",
     "Pedir el manual completo o las carpetas 1 a 4 del kit de marca.", "Alta", "Cliente"),
    ("Logotipo en vector",
     "Todos los logos son PNG. El archivo AI.zip contiene solo «Asset 79.ai», que corresponde a los íconos y además está guardado sin contenido PDF, así que no se pudo abrir.",
     "Pedir logotipo, isotipo y versiones con tagline en SVG, AI o PDF vectorial.", "Alta", "Cliente"),
    ("HEX del cian mal rotulado",
     "El PDF de color escribe «Neon cyan · Hex: 87007d», el mismo valor que el púrpura. El triángulo cian del propio PDF, los logos y la paleta en PNG coinciden en #00F5D4, que es el que usamos.",
     "Confirmar #00F5D4 y corregir el PDF.", "Alta", "Cliente"),
    ("Navy y negros que no coinciden entre archivos",
     "El PDF define el navy como #011E5E. La paleta en PNG lo cambia por #16213A y agrega un negro #1C1C1E. Los logos «negros» vienen en #000000 (sin tagline) y #1D1D1B (con tagline), y un mismo archivo mezcla los dos. Los mockups usan fondos entre #202020 y #272727, y los íconos están en #071436.",
     "Definir un solo navy y un solo negro, y decir si el negro es color de marca.", "Alta", "Cliente"),
    ("Licencias de las tipografías",
     "La licencia de Swiza es de escritorio para 5 equipos: prohíbe redistribuir los archivos y convertirlos a webfont. Nebulica no trae licencia; el archivo dice «All rights reserved». Por eso no subimos las fuentes al repo y la página usa un fallback.",
     "Pedir licencia web de Swiza y el comprobante de Nebulica, o elegir alternativas con licencia abierta.", "Alta", "Cliente"),
    ("Piezas de LinkedIn fuera de identidad",
     "Las 12 piezas usan un violeta que no está en la paleta, dos tipografías que no son Nebulica ni Swiza y un logotipo recompuesto (isotipo con degradado junto al nombre) que no existe como archivo. El tagline va en cian sobre blanco, a 1.40:1.",
     "Confirmar quién las produjo y si están publicadas o aprobadas. Decidir si se rehacen con el sistema.", "Alta", "Equipo BnO"),
    ("Cifras y promesas sin respaldo en las piezas",
     "Las piezas afirman «Disponibilidad 99%», «Monitoreo 24/7», «SLA cumplido», cobertura «en todo México», «Sin caídas», «Sin riesgos» y un diagnóstico «sin costo». Nada de eso tiene respaldo en el material.",
     "Pedir al cliente la validación por escrito de cada afirmación antes de publicar o pautar.", "Alta", "Cliente"),
    ("Reglas de contenido",
     "El cliente no entregó reglas de qué se puede decir y qué no, ni lista oficial de servicios, ni datos de contacto vigentes.",
     "Pedir servicios, afirmaciones permitidas, restricciones legales y contactos. Mientras tanto aplican las seis reglas provisionales de esta página.", "Alta", "Cliente"),
    ("Para qué sirve cada tipografía",
     "Llegaron dos familias sin instrucciones. En el material, Swiza compone el tagline del logotipo y las tarjetas; Nebulica aparece en el nombre de la firma de correo. Proponemos Nebulica para titulares y Swiza para textos.",
     "Validar la propuesta con el cliente o con quien diseñó la marca.", "Alta", "Cliente"),
    ("Datos del proyecto",
     "Quién aprueba por el cliente, el equipo y el consultor asignados no venían en el encargo. En la ficha están como «sin confirmar».",
     "Completar operacion/FICHA.md.", "Alta", "Equipo BnO"),
    ("Tagline en cian sobre fondos claros",
     "La versión «negro-azul» del logotipo combina el nombre en oscuro con el tagline en cian. Sobre blanco o blanco azulado el tagline queda a 1.33:1 y no se lee.",
     "Confirmar que sobre claro se usa la versión de una sola tinta, y sobre qué fondo se pensó la versión «negro-azul».", "Media", "Cliente"),
    ("Isotipo solo en blanco",
     "El isotipo llegó únicamente en blanco. En tarjetas, carpetas y gafete aparece con degradado púrpura, y en las piezas de LinkedIn con otro degradado, pero no hay archivo de isotipo en negro ni a color plano.",
     "Pedir el isotipo en negro, en color plano y la versión oficial con degradado.", "Media", "Cliente"),
    ("Versión apilada del logotipo",
     "Logo_Avantika_Blanco_Completo.png (1000 × 669) apila isotipo, nombre y tagline, pero el tagline está en otra tipografía y con otro espaciado que en las versiones @4x. Solo existe en blanco.",
     "Confirmar si la versión apilada es oficial y pedirla en alta, con el tagline correcto.", "Media", "Cliente"),
    ("Reglas de uso del logotipo",
     "No hay área de protección, tamaño mínimo, fondos permitidos ni usos incorrectos. Los que muestra esta página son propuesta.",
     "Pedirlas o aprobar las propuestas.", "Media", "Cliente"),
    ("Autorización de uso de imagen",
     "Las 272 fotos de la sesión del equipo muestran a colaboradores identificables y, en el evento, a algunos niños. No consta que haya autorización para usarlas en pauta, sitio o redes.",
     "Confirmar las autorizaciones y la lista de personas que no deben aparecer. Mientras tanto, las 22 fotos seleccionadas son solo para revisión interna.", "Alta", "Cliente"),
    ("Criterio fotográfico",
     "La sesión tiene dos estilos de retrato (fondo blanco y fondo negro) y fotos de oficina con luz de día. No hay regla de cuál usar, de encuadre ni de tratamiento de color.",
     "Aprobar la propuesta de esta página: retrato oscuro para piezas oscuras, retrato claro para el sitio, sin filtros ni duotonos.", "Media", "Equipo BnO"),
    ("Pantallas visibles en las fotos de oficina",
     "El muro de pantallas muestra tableros de monitoreo con nombres de servidores y el sistema de tickets. A 1800 px no se leen, pero en recortes grandes podrían.",
     "Revisar cada foto con pantallas antes de usarla en pauta, o pedir una toma con pantallas genéricas.", "Baja", "Equipo BnO"),
    ("«YOU CAN · END OF STORY» y #ValoresAvantika",
     "En la oficina hay un letrero «YOU CAN · END OF STORY» con la A de la marca, y en el evento una tarjeta con #ValoresAvantika y #YouCan. Ninguno aparece en el material de marca.",
     "Preguntar si es un lema oficial, si es solo interno y si se puede usar en comunicación externa.", "Baja", "Cliente"),
    ("Íconos sin nombre ni vector",
     "Los 34 íconos vienen numerados, sin nombre ni significado asignado, en PNG de 522 px y en un azul (#071436) que no es el navy de la paleta. El vector «Asset 79.ai» no abre fuera de Illustrator.",
     "Pedir el set en SVG con nombres, y confirmar su color.", "Media", "Cliente"),
    ("Archivos de Illustrator sin compatibilidad PDF",
     "«Asset 79.ai», «Avantika- patron.ai» y «Avatika-ventana.ai» se guardaron sin contenido PDF y solo abren en Illustrator. «Layoutd.ai» sí abre, pero pesa 88 MB y no se subió al repo.",
     "Pedirlos de nuevo con «Crear archivo compatible con PDF» o exportados a SVG.", "Media", "Cliente"),
    ("Datos de contacto contradictorios",
     "Las tarjetas y la firma usan correos con dominio avantika.com.mx; las piezas y la paleta en PNG dicen avantika.mx. El teléfono de la firma parece de muestra.",
     "Pedir dominio, teléfono, dirección y redes oficiales.", "Media", "Cliente"),
    ("Códigos QR sin verificar",
     "Recibimos 5 códigos QR (CEO, etiqueta, libreta y playera). No pudimos leer a dónde llevan con las herramientas de esta sesión, y el del CEO puede contener datos de contacto personales. No se publicaron.",
     "Escanearlos, anotar su destino y decidir si entran al repo.", "Media", "Equipo BnO"),
    ("Roles de color",
     "El PDF lista cinco colores sin decir para qué sirve cada uno. Proponemos blanco azulado de fondo, navy primario, púrpura secundario, magenta como acento pequeño y cian solo sobre oscuro.",
     "Validar con diseño y con el cliente.", "Media", "Equipo BnO"),
    ("Degradados y efecto cristal",
     "La marca vive de degradados, desenfoques y paneles translúcidos, pero no hay regla de cómo construirlos. Proponemos usarlos solo a través de los fondos entregados y no fabricarlos en CSS.",
     "Pedir la regla de construcción o aprobar la restricción.", "Media", "Cliente"),
    ("Claro u oscuro por defecto",
     "Las aplicaciones impresas son casi todas negras; los fondos y la hoja membretada, claros. No hay regla. Proponemos claro por defecto en web y navy en bandas.",
     "Decidir el modo por defecto por canal.", "Media", "Equipo BnO"),
    ("Sitio avantika.mx",
     "El material menciona el dominio pero no incluye el sitio ni su código. No lo revisamos: el encargo fue trabajar con la carpeta. En una foto de la oficina se ve el sitio con una página «Cyber360» y un botón rojo que no es de la paleta.",
     "Revisar el sitio vigente y contrastarlo con este sistema.", "Media", "Equipo BnO"),
    ("Un fondo duplicado",
     "Layouts-06.png y Layouts-07.png son el mismo archivo byte a byte. Falta el fondo que debía ser el 07.",
     "Pedir el archivo correcto.", "Baja", "Cliente"),
    ("Hoja membretada sin datos",
     "El PDF de la hoja membretada trae el logotipo y el isotipo en grises como imagen, sin dirección, teléfono ni pie legal.",
     "Pedir la versión con datos y en vector.", "Baja", "Cliente"),
    ("Nombre de la carpeta de posts",
     "La carpeta se llama «Set de 6 posts de LinkedIn» y trae 12 imágenes: 6 posts y 2 carruseles de 3 láminas.",
     "Confirmar el alcance real del set y si falta el copy de acompañamiento.", "Baja", "Equipo BnO"),
    ("Tagline frente a la oferta",
     "El logotipo dice «Cybersecurity», pero las piezas hablan también de soporte, mesa de ayuda, infraestructura y gestión de TI.",
     "Preguntar si el tagline es fijo o si habrá versiones por línea de servicio.", "Baja", "Cliente"),
    ("Escala tipográfica, estados y video",
     "No hay tamaños, colores de estado para formularios ni reglas de video. Lo que muestra esta página es propuesta.",
     "Validar la escala, derivar colores de error y éxito, y fijar reglas de video antes de producir.", "Baja", "Equipo BnO"),
    ("Erratas en nombres de archivo",
     "Varios archivos dicen «Avatika» (sin n), «Layoutd» y «visulaes».",
     "Avisar al cliente; en este repo se renombraron en references/ y se conservan tal cual en brand/uploads/.", "Baja", "Cliente"),
]


# ---------- Secciones ----------
def s_resumen():
    filas = []
    for ident, titulo, tipo in SECCIONES:
        if ident == "resumen":
            continue
        filas.append('<tr><td><a href="#%s">%s</a></td><td><span class="celda-estado">%s%s</span></td><td>%s</td></tr>'
                     % (ident, e(titulo), marca(tipo), ESTADOS[tipo] if ident != "huecos" else "%d pendientes" % len(HUECOS),
                        e(COBERTURA[ident])))
    cuerpo = T("""
<dl class="ficha">
  <div><dt>Marca</dt><dd>Avantika</dd></div>
  <div><dt>Cliente</dt><dd>Avantika · sin confirmar</dd></div>
  <div><dt>Elaboró</dt><dd>Black &amp; Orange</dd></div>
  <div><dt>Estado</dt><dd>Propuesta para comentarios</dd></div>
  <div><dt>Fecha de revisión</dt><dd>{{fecha}}</dd></div>
  <div><dt>Tokens</dt><dd><span class="fuente">brand/tokens/</span></dd></div>
  <div><dt>Secciones</dt><dd>{{n}}</dd></div>
  <div><dt>Pendientes</dt><dd>{{h}}</dd></div>
  <div><dt>Equipo y consultor</dt><dd>sin confirmar</dd></div>
  <div><dt>Aprueba por el cliente</dt><dd>sin confirmar</dd></div>
  <div class="ficha__ancha"><dt>Material revisado</dt><dd>272 fotos del equipo (sesión del 23 de diciembre de 2025, compartidas el 20 de octubre de 2026), 8 logos en PNG, un PDF de color y una paleta en PNG, las familias Nebulica y Swiza con la licencia de Swiza, 34 íconos, 12 fondos (uno repetido), 6 ilustraciones del isotipo, 4 ventanas, un patrón, 8 mockups de aplicación, la hoja membretada, 5 códigos QR, 4 archivos de Illustrator y 12 piezas de LinkedIn. No hay manual de marca.</dd></div>
</dl>
<ul class="leyenda" aria-label="Cómo leer los estados">
  <li>{{mg}}<span><b>De la guía</b></span><span>viene en el material del cliente</span></li>
  <li>{{mb}}<span><b>Propuesta BnO</b></span><span>el material no lo define; lo armamos para revisarlo</span></li>
  <li>{{mf}}<span><b>Falta</b></span><span>no existe y hay que pedirlo o definirlo</span></li>
</ul>
<table class="tabla tabla--cobertura">
  <thead><tr><th scope="col">Sección</th><th scope="col">Estado</th><th scope="col">Qué hay</th></tr></thead>
  <tbody>{{filas}}</tbody>
</table>""", fecha=FECHA, n=len(SECCIONES) - 1, h=len(HUECOS), mg=marca("guia"), mb=marca("bno"), mf=marca("falta"),
               filas="\n".join(filas))
    return bloque("resumen", "Resumen de la revisión",
                  "Avantika tiene piezas de identidad sólidas (logotipo, cinco colores, dos tipografías, íconos, fondos y una sesión de fotos del equipo), pero ningún documento "
                  "que diga cómo se usan: no llegó manual de marca. Aquí «De la guía» significa que el archivo viene en el material, no que exista una regla. "
                  "Lo más urgente es pedir el manual y los vectores, resolver las licencias tipográficas y decidir qué hacer con las piezas de LinkedIn, "
                  "que no siguen la identidad.",
                  None, "", cuerpo)


def s_logotipo():
    archivos = [
        celda(NAVY, L_BLANCO, "<b>logo-avantika-blanco</b> · 1859 × 246 · #FFFFFF"),
        celda(HIELO, L_NEGRO, "<b>logo-avantika-negro</b> · 1859 × 246 · #000000"),
        celda(NAVY, LT_BLANCO_AZUL, "<b>tagline-blanco-azul</b> · 1245 × 260 · blanco y cian"),
        celda(NAVY, LT_BLANCO, "<b>tagline-blanco</b> · 1245 × 260 · todo blanco"),
        celda(HIELO, LT_NEGRO, "<b>tagline-negro</b> · 1244 × 260 · nombre #1D1D1B y tagline #000000"),
        celda(HIELO, LT_NEGRO_AZUL, "<b>tagline-negro-azul</b> · 1244 × 260 · el tagline cian no se lee sobre claro (1.33:1)", mal=True),
        celda(NAVY, ISO_BLANCO, "<b>isotipo-blanco</b> · 923 × 808 · única versión del isotipo", estilo_logo="width:34%"),
        celda(NAVY, COMPLETO, "<b>completo-blanco</b> · 1000 × 669 · apilado, baja resolución y tagline en otra tipografía", mal=True, estilo_logo="width:46%"),
    ]
    usos = [
        celda(HIELO, L_NEGRO, "Negro sobre blanco azulado"),
        celda(BLANCO, LT_NEGRO, "Con tagline, una tinta, sobre blanco"),
        celda(NAVY, LT_BLANCO_AZUL, "Blanco y cian sobre navy"),
        celda(TINTA, LT_BLANCO_AZUL, "Blanco y cian sobre tinta " + etiqueta("guia")),
        celda(PURPLE, LT_BLANCO, "Blanco sobre púrpura"),
        celda(MAGENTA, L_BLANCO, "Blanco sobre magenta · solo a tamaño grande (3.88:1)"),
    ]
    mal = [
        celda(HIELO, LT_NEGRO_AZUL, "Tagline cian sobre claro · no se lee", mal=True),
        celda(CYAN, L_BLANCO, "Blanco sobre cian · desaparece", mal=True),
        celda(NAVY, L_NEGRO, "Negro sobre navy · no se lee", mal=True),
        celda(HIELO, L_NEGRO, "Deformado", mal=True, estilo_logo="transform:scaleY(1.9)"),
        celda(HIELO, L_BLANCO, "Sobre una zona clara de un fondo · pierde legibilidad", mal=True, foto=IMG + "layout-03.jpg"),
        celda(BLANCO, L_NEGRO, "Recompuesto con otro isotipo al lado, como en las piezas de LinkedIn", mal=True, foto=IMG + "post-linkedin-01.jpg",
              estilo_logo="display:none", pos="0% 3%"),
    ]
    elementos = "".join(
        '<figure class="av-celda"><div class="av-celda__lona" style="background-color:%s"><img src="%s%s.svg" alt=""></div><figcaption>%s</figcaption></figure>'
        % (HIELO, ELEM, n, pie) for n, pie in [
            ("triangulo", "<b>Triángulo</b> · isotipo y dos triángulos"), ("ventana-1", "<b>Ventana 1</b>"), ("ventana-2", "<b>Ventana 2</b>"),
            ("ventana-3", "<b>Ventana 3</b>"), ("ventana-4", "<b>Ventana 4</b> · la del fondo 06")])
    elementos += ('<figure class="av-celda"><div class="av-celda__lona av-patron"></div>'
                  '<figcaption><b>Patrón</b> · 1426 × 1313, #1D1D1B sobre transparente</figcaption></figure>')
    cuerpo = T("""
<div class="lienzo">
  {{s1}}
  <div class="av-grid">{{archivos}}</div>
  <p class="nota">Cada archivo se muestra sobre un fondo donde se distingue. El contorno punteado marca los dos que tienen problema. Los originales están intactos en <code>brand/assets/</code>; aquí solo se redujeron los de más de 1200 px.</p>
  {{s2}}
  <div class="av-grid">{{usos}}</div>
  <p class="nota">Solo el uso sobre tinta aparece en el material (banner, parabús y carpetas). Los demás fondos son propuesta: nada dice sobre qué colores puede ir el logotipo.</p>
  {{s3}}
  <div class="av-grid">{{mal}}</div>
  {{s4}}
  <div class="av-grid" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">
    <figure class="av-celda"><div class="av-firma" style="background:{{navy}}"><img src="{{ltba}}" alt="Avantika Cybersecurity"><img src="{{iso}}" alt=""></div><figcaption>Sobre oscuro · logotipo con tagline abajo a la izquierda e isotipo en el extremo opuesto</figcaption></figure>
    <figure class="av-celda"><div class="av-firma" style="background:{{hielo}}"><img src="{{ltn}}" alt="Avantika Cybersecurity"><span></span></div><figcaption>Sobre claro · solo el logotipo: no existe isotipo en oscuro</figcaption></figure>
  </div>
  <p class="nota">Avantika firma sola: en el material no hay marca madre ni casa matriz, y en matriz-ads no existe una marca hermana. La posición y el tamaño de la firma son propuesta.</p>
  {{s5}}
  <div class="av-elementos">{{elementos}}</div>
  <p class="nota">Las ventanas y el triángulo vienen en SVG y PNG; el patrón solo en PNG y en un .ai que no abre fuera de Illustrator. Ningún documento explica para qué sirve cada ventana: por su forma parecen marcos para imagen o texto.</p>
  {{s6}}
  <div class="av-docs">
    <figure><img class="av-hoja" src="../../bg/hoja-membretada-p01.png" alt="Hoja membretada: logotipo arriba a la izquierda e isotipo en grises abajo." loading="lazy"><figcaption><b>Hoja membretada</b>Única pieza de papelería en PDF. Sin datos de contacto.</figcaption></figure>
    <figure><img src="img/tipo/tagline-vs-swiza.png" alt="El logotipo con tagline y, debajo, la palabra Cybersecurity compuesta en Swiza Light." loading="lazy"><figcaption><b>El tagline está en Swiza Light</b>Arriba, el archivo del cliente. Abajo, «Cybersecurity» compuesto por nosotros en Swiza Light: coinciden. La tipografía del nombre AVANTIKA es un dibujo propio.</figcaption></figure>
  </div>
</div>""", s1=sub("Los 8 archivos recibidos", "guia", "PNG con fondo transparente"), archivos="".join(archivos),
               s2=sub("Usos sobre los colores de la marca", "bno"), usos="".join(usos),
               s3=sub("Usos incorrectos", "bno", "ilustrados por BnO; el material no trae ninguno"), mal="".join(mal),
               s4=sub("Firma", "bno"), navy=NAVY, hielo=HIELO, ltba=LT_BLANCO_AZUL, iso=ISO_BLANCO, ltn=LT_NEGRO,
               s5=sub("Elementos de marca", "guia", "carpeta «5. Elementos visulaes»"), elementos=elementos,
               s6=sub("Papelería y evidencia", "guia"))
    return bloque(
        "logotipo", "Logotipo y firma",
        "El nombre AVANTIKA en mayúsculas geométricas, con la primera A convertida en un triángulo abierto que también funciona sola como isotipo. "
        "Debajo, el tagline Cybersecurity. Recibimos ocho PNG; no hay vector ni manual.",
        "guia", "brand/assets/ · brand/assets/elementos/", cuerpo,
        ["No recoloreamos ni redibujamos nada. Dos archivos no son consistentes con el resto: la versión «negro-azul» (tagline ilegible sobre claro) y la versión apilada (otra tipografía en el tagline, 1000 px).",
         "Hay dos negros: #000000 en el logotipo sin tagline y #1D1D1B en las versiones con tagline. «tagline-negro» mezcla los dos en el mismo archivo. ¿Cuál es el oficial?",
         "El isotipo solo existe en blanco. Para firmar sobre claro hace falta en oscuro.",
         "Las piezas de LinkedIn usan un logotipo que no está entre los archivos: isotipo con degradado a la izquierda, nombre a la derecha y tagline diminuto en cian. ¿Existe esa versión horizontal?",
         "No hay área de protección ni tamaño mínimo. El tagline es fino (Swiza Light) y se pierde por debajo de unos 120 px de ancho de logotipo.",
         "El nombre mide 7.6 veces su alto: en formatos verticales queda muy pequeño. Conviene definir cuándo se usa el isotipo solo."])


def s_color():
    muestras = [
        ("Neon cyan", CYAN, NAVY, "R 0 G 245 B 212", "--av-cyan", "Acento sobre oscuro: tagline, badges y plecas. Nunca sobre claro."),
        ("Deep purple", PURPLE, HIELO, "R 135 G 0 B 125", "--av-purple", "Secundario: bandas de cierre, badges y eyebrows."),
        ("Vibrant magenta red", MAGENTA, NAVY, "R 255 G 0 B 94", "--av-magenta", "Acento sobre claro: plecas, subrayados y foco. No es color de texto."),
        ("Soft white blue", HIELO, NAVY, "R 244 G 250 B 255", "--av-hielo", "Fondo por defecto y texto sobre oscuro."),
        ("Deep navy blue", NAVY, HIELO, "R 1 G 30 B 94", "--av-navy", "Primario: texto, titulares, botones y bandas."),
    ]
    sw = "".join(
        '<div class="av-swatch"><div class="av-swatch__color" style="background:%s;color:%s">%s</div>'
        '<div class="av-swatch__info"><b>%s</b><code>%s · %s</code><code>%s</code><span>%s %s</span></div></div>'
        % (hexa, sobre, nombre, nombre, hexa, var, rgb, etiqueta("bno"), e(rol))
        for nombre, hexa, sobre, rgb, var, rol in muestras)
    derivados = "".join(
        '<div class="av-swatch"><div class="av-swatch__color" style="background:%s;color:%s;height:72px;font-size:14px">%s</div>'
        '<div class="av-swatch__info"><code>%s · %s</code><span>%s</span></div></div>' % d
        for d in [(LINEA, NAVY, "Filete", LINEA, "--av-line", "Navy al 16 % sobre blanco azulado. Bordes de tarjetas y divisores."),
                  (LINEA_INV, HIELO, "Filete inverso", LINEA_INV, "--av-line-inverse", "Blanco azulado al 30 % sobre navy. Divisores sobre oscuro."),
                  (NAVY_HOVER, HIELO, "Navy hover", NAVY_HOVER, "--av-navy-hover", "Navy oscurecido para el hover del botón primario."),
                  (PLACEHOLDER, BLANCO, "Placeholder", PLACEHOLDER, "--av-placeholder", "Navy al 60 % sobre blanco azulado. Texto de ayuda en campos."),
                  (BLANCO, NAVY, "Blanco", BLANCO, "--av-blanco", "Campos de formulario y tarjetas sobre blanco azulado.")])
    sueltos = "".join(
        '<div class="av-swatch"><div class="av-swatch__color" style="background:%s;color:%s;height:72px;font-size:14px">%s</div>'
        '<div class="av-swatch__info"><code>%s</code><span>%s</span></div></div>' % d
        for d in [(TINTA, HIELO, "Tinta", TINTA + " · --av-tinta", "Logotipos con tagline «negros» y patrón. Único de estos que es token, para poder mostrar el logotipo sobre su fondo."),
                  ("#000000", HIELO, "Negro", "#000000", "Logotipo sin tagline y tagline de «tagline-negro»."),
                  (PNG_NEGRO, HIELO, "Negro de la paleta PNG", PNG_NEGRO, "Rotulado en «Paleta de color Avantika.png». No está en el PDF."),
                  (PNG_NAVY, HIELO, "Navy de la paleta PNG", PNG_NAVY, "Rotulado en la paleta PNG en lugar de #011E5E."),
                  (ICONO_AZUL, HIELO, "Azul de los íconos", ICONO_AZUL, "Medido en los 34 íconos. Tampoco es el navy del PDF."),
                  (POSTS_VIOLETA, HIELO, "Violeta de las piezas", POSTS_VIOLETA, "Medido en los titulares de las piezas de LinkedIn. No es el púrpura #87007D.")])
    cuerpo = T("""
<div class="lienzo">
  {{s1}}
  <div class="av-swatches av">{{sw}}</div>
  <p class="nota">Nombres y HEX vienen de <code>Avatika-color (2).pdf</code>. El PDF no da RGB ni CMYK ni Pantone: el RGB de arriba es la conversión directa del HEX. El rol de cada color es propuesta.</p>
  {{s2}}
  <div class="av-docs">
    <figure><img src="../../bg/color-p01.png" alt="Página del PDF de color: cinco triángulos con nombre y HEX." loading="lazy"><figcaption><b>Avatika-color (2).pdf · febrero de 2025</b>Hecho en Illustrator. Rotula «Neon cyan · Hex: 87007d», el mismo valor que Deep purple. El triángulo cian mide #00F5D4.</figcaption></figure>
    <figure><img src="../../bg/paleta-de-color.jpg" alt="Paleta en PNG con seis colores y el dominio avantika.mx." loading="lazy"><figcaption><b>Paleta de color Avantika.png</b>Seis colores: cambia el navy por #16213A y agrega #1C1C1E. Usa la versión apilada del logotipo y un degradado azul que no está en ninguna paleta. Mide 1024 × 1536 y no trae autor ni fecha.</figcaption></figure>
  </div>
  <p class="nota">Criterio provisional: rige el PDF, porque está hecho en Illustrator el mismo día que el patrón y las ventanas. Del PNG solo tomamos la confirmación del cian.</p>
  {{s3}}
  <div class="av-swatches av">{{sueltos}}</div>
  {{s4}}
  <div class="av-swatches av">{{derivados}}</div>
  {{s5}}
  <div class="tabla-scroll"><table class="tabla">
    <thead><tr><th scope="col">Muestra</th><th scope="col">Combinación y uso</th><th scope="col">Contraste</th><th scope="col">Nivel</th></tr></thead>
    <tbody>{{filas}}</tbody>
  </table></div>
  <p class="nota">AA pide 4.5:1 para texto normal y 3:1 para texto grande (24 px, o 19 px en negritas) y para elementos gráficos.</p>
</div>""", s1=sub("Paleta del PDF de color", "guia"), sw=sw, s2=sub("Los dos documentos de color", "guia", "no coinciden entre sí"),
               s3=sub("Colores que aparecen en archivos y no están en el PDF", "falta", "medidos por BnO; ninguno es regla"), sueltos=sueltos,
               s4=sub("Colores derivados", "bno", "necesarios para interfaz; no son colores de marca"), derivados=derivados,
               s5=sub("Contraste de las combinaciones", "bno", "calculado con los HEX de los tokens"), filas=filas_contraste())
    return bloque(
        "color", "Color",
        "Un cian neón, un púrpura profundo, un magenta rojizo, un blanco azulado y un navy. "
        "El PDF da nombre y HEX, pero no dice para qué sirve cada color, y un segundo archivo lo contradice.",
        "guia", "brand/uploads/Avatika-color (2).pdf · brand/tokens/colors.css", cuerpo,
        ["¿Se aprueba #00F5D4 como cian? El PDF lo rotula con el HEX del púrpura.",
         "¿Rige el navy #011E5E del PDF o el #16213A de la paleta en PNG? ¿El negro es color de marca?",
         "El cian solo funciona sobre oscuro (11.13:1 sobre navy; 1.33:1 sobre blanco azulado). El magenta no alcanza AA como texto normal sobre ningún fondo de la paleta.",
         "Púrpura y navy juntos no contrastan (1.72:1): siempre necesitan un claro entre ellos.",
         "¿Se aprueban los roles: blanco azulado de fondo, navy primario, púrpura secundario, magenta de acento y cian solo sobre oscuro?",
         "Las aplicaciones impresas son negras con púrpura; el PDF no tiene negro. Falta decidir si el modo oscuro usa navy o negro.",
         "La paleta no tiene colores de estado (error, éxito, advertencia). El magenta se parece a un rojo de error: hay que evitar la confusión en formularios."])


def s_tipografia():
    escala = [
        ("Display · 56 / 1.1", '<span class="av-title" style="font-size:clamp(30px,5vw,56px)">Un solo equipo para tu TI</span>'),
        ("H1 · 40 / 1.1", '<span class="av-title" style="font-size:clamp(26px,4vw,40px)">Soporte que responde</span>'),
        ("H2 · 32 / 1.1 · 600", '<span class="av-title" style="font-size:clamp(22px,3.4vw,32px);font-weight:600">Infraestructura sin sorpresas</span>'),
        ("H3 · 24 / 1.1 · 600", '<span class="av-title" style="font-size:24px;font-weight:600">Ciberseguridad</span>'),
        ("Subtítulo · 20 / 1.5 · 300", '<span style="font-size:20px;font-weight:300">Tu tecnología al ritmo de tu operación.</span>'),
        ("Cuerpo · 16 / 1.5", '<span style="font-size:16px">Mesa de ayuda, técnicos en sitio y en campo.</span>'),
        ("Chico · 14 / 1.5", '<span style="font-size:14px">Redes, servidores y cableado que no detienen tu operación.</span>'),
        ("Leyenda · 12 / 1.5", '<span style="font-size:12px">avantika.mx</span>'),
        ("Botón · 14 · 600", '<span style="font-size:14px;font-weight:600">Agenda tu diagnóstico</span>'),
    ]
    filas = "".join('<div class="av-escala__fila"><span>%s</span><span>%s</span></div>' % f for f in escala)
    cuerpo = T("""
<div class="lienzo">
  <div class="av-aviso" id="estado-fuentes" role="status"><b>Las fuentes de la marca no viajan con esta página</b>Sus licencias no permiten redistribuirlas. Los especímenes de abajo son imágenes hechas con los archivos reales; el texto vivo de la página usa Nebulica y Swiza solo si están instaladas en tu equipo.</div>
  {{s1}}
  <div class="av-docs">
    <figure><img class="av-tipo" src="img/tipo/nebulica.png" alt="Espécimen de Nebulica: Aa, abecedario y nueve pesos de Thin a Black." loading="lazy"><figcaption><b>Nebulica · Zarma Type Foundry, 2024</b>9 pesos en OTF, 8 en TTF y un archivo variable. Sin itálicas. No viene licencia en la carpeta. En el material compone el nombre de la firma de correo. <code>--av-font-display</code></figcaption></figure>
    <figure><img class="av-tipo" src="img/tipo/swiza.png" alt="Espécimen de Swiza: Aa, abecedario y siete pesos de Thin a Bold." loading="lazy"><figcaption><b>Swiza · atipo, 2025</b>7 pesos con itálicas, en OTF. Licencia de escritorio para 5 equipos: prohíbe redistribuir y convertir a webfont. En el material compone el tagline del logotipo y las tarjetas. <code>--av-font-text</code></figcaption></figure>
  </div>
  <p class="nota">Que Nebulica sea para titulares y Swiza para textos es propuesta: ningún documento asigna funciones. Lo apoya el uso observado en tarjetas, firma y logotipo.</p>
  {{s2}}
  <img class="av-tipo" src="img/tipo/escala.png" alt="Escala tipográfica propuesta compuesta con Nebulica y Swiza." loading="lazy">
  <p class="nota">Imagen compuesta con las fuentes reales, al doble de tamaño. Tamaños en px para escritorio; la regla de reducción en móvil está por definir.</p>
  {{s3}}
  <div class="av-escala av">{{filas}}</div>
  <p class="nota">Esta tabla es texto vivo con los tokens de <code>brand/tokens/typography.css</code>. Sin las fuentes instaladas verás Helvetica Neue o Arial, que son más angostas que Nebulica: los cortes de línea cambian.</p>
</div>""", s1=sub("Las dos familias", "guia", "archivos entregados; funciones propuestas"),
               s2=sub("Escala para web", "bno", "el material no define tamaños"),
               s3=sub("La misma escala, en texto vivo", "bno", "con fallback si no tienes las fuentes"), filas=filas)
    return bloque(
        "tipografia", "Tipografía",
        "Dos familias sans: Nebulica, de formas anchas y terminales rectas, y Swiza, una grotesca limpia que ya firma el tagline del logotipo. "
        "Llegaron los archivos pero no las instrucciones, y sus licencias limitan dónde se pueden usar.",
        "guia", "brand/tokens/typography.css · brand/assets/fonts/LEEME.md", cuerpo,
        ["Swiza no se puede usar en un sitio web con la licencia recibida. ¿Se compra la licencia web o se elige una alternativa abierta para digital?",
         "Nebulica no trae licencia. ¿El cliente tiene el comprobante? Sin él no conviene producir con ella.",
         "¿Nebulica para titulares y Swiza para textos? Es la lectura del material, no una regla.",
         "Las piezas de LinkedIn no usan ninguna de las dos: alternan una condensada pesada y una geométrica redonda, a veces en el mismo set.",
         "No hay tracking, interlineado ni tamaños definidos. Proponemos titulares con interlínea 1.1 y texto a 1.5.",
         "Nebulica no tiene itálica. ¿El énfasis se resuelve con peso o con color?"])


def s_iconos():
    figs = "".join('<figure><img src="%s%02d.png" alt="" loading="lazy"><figcaption>%02d</figcaption></figure>' % (ICONOS, n, n)
                   for n in range(1, 35))
    cuerpo = T("""
<div class="lienzo">
  {{s1}}
  <div class="av-iconos">{{figs}}</div>
  <p class="nota">Vienen en <code>4x.zip</code> como «Avantika-icono-N@4x.png», de 522 × 521 px, con fondo transparente y en un solo color (#071436). Aquí sobre blanco azulado. Los números son los del archivo: el material no les pone nombre.</p>
  {{s2}}
  <div class="av-compara">
    <div><b>Construcción</b><span>Pictograma sólido dentro de un doble anillo, con una corona de trazos radiales. El anillo es parte del ícono: no se puede quitar sin redibujar.</span></div>
    <div><b>Temas</b><span>Ciberseguridad (escudos, candados, huella, malware, contraseñas), redes e infraestructura (servidor, wifi, cables, nube) y soporte (técnico, engranes, cronómetro).</span></div>
    <div><b>Marca dentro del set</b><span>El 28 (técnico con casco) lleva el isotipo de Avantika en el pecho.</span></div>
    <div><b>Tamaño</b><span>El anillo y los trazos radiales se empastan por debajo de unos 48 px. En el sitio de ejemplo van a 64 px.</span></div>
  </div>
</div>""", s1=sub("Los 34 íconos recibidos", "guia"), figs=figs, s2=sub("Lo que se observa", "bno", "lectura de BnO; no hay documento"))
    return bloque(
        "iconos", "Íconos",
        "Un set de 34 íconos de ciberseguridad, redes y soporte, todos con el mismo marco circular. "
        "Llegaron como PNG; el vector no se puede abrir.",
        "guia", "brand/assets/icons/ · brand/uploads/4x.zip", cuerpo,
        ["No tienen nombre ni significado asignado. ¿Hay una lista de qué servicio representa cada uno?",
         "Solo vienen en azul oscuro #071436, que no es el navy #011E5E. No hay versión en blanco para fondos oscuros, y recolorearlos sería modificar el archivo.",
         "El vector («Asset 79.ai») se guardó sin contenido PDF. Hace falta en SVG para usarlo en web.",
         "El marco circular los hace pesados en tamaños chicos. ¿Existe una versión sin anillo para interfaz?",
         "¿Son propios o de un banco con licencia? No hay procedencia."])


def _tarjetas(lista, clase_marco="", leyenda=None):
    return "".join(
        '<figure class="av-render"><div class="av-render__marco %s"><img src="%s%s.jpg" alt="%s" loading="lazy">%s</div>'
        '<figcaption><b>%s</b><code>%s</code> · %s px<br>%s</figcaption></figure>'
        % (clase_marco, IMG, archivo, e(titulo), leyenda or "", e(titulo), e(original), medida, e(nota))
        for archivo, original, medida, titulo, nota in lista)


def s_fotografia():
    equipo = ""
    for grupo, fotos in FOTOS_EQUIPO.items():
        equipo += '<p class="nota" style="margin:16px 0 8px"><b>%s</b></p><div class="av-renders">%s</div>' % (e(grupo), "".join(
            '<figure class="av-render"><div class="av-render__marco"><img src="%s%s.jpg" alt="%s" loading="lazy"></div>'
            '<figcaption><b>%s</b><code>%s</code><br>%s</figcaption></figure>' % (IMG, n, e(t), e(t), e(o), e(nota)) for n, o, t, nota in fotos))
    retratos = "".join('<figure><img src="%s%s.jpg" alt="Retrato de una persona del equipo de Avantika, %s" loading="lazy"><figcaption><b>%s</b><code>%s</code></figcaption></figure>'
                       % (IMG, n, e(fondo.lower()), e(fondo), e(o)) for n, o, fondo in RETRATOS)
    cuerpo = T("""
<div class="lienzo">
  {{s0}}
  {{equipo}}
  <p class="nota" style="margin:16px 0 8px"><b>Retratos</b> · 4 de unos 45 sobre fondo blanco y 3 de unos 90 sobre fondo negro</p>
  <div class="av-galeria">{{retratos}}</div>
  <p class="nota">272 fotos de una sola sesión (Sony A7 III, 23 de diciembre de 2025), compartidas el 20 de octubre de 2026 en dos carpetas y dos zip idénticos. Aquí van 22, en JPG a 1800 px. Los 272 originales (2.8 GB) se quedan en la carpeta local, fuera del repo; su inventario con hashes está en <code>source/fotos.json</code>. Se dejaron fuera de la selección las fotos donde aparecen niños.</p>
  {{s1}}
  <div class="av-compara">
    <div><b>Vestuario</b><span>Todo el equipo viste de negro. Combina con las aplicaciones negras de la marca y con la banda navy.</span></div>
    <div><b>Dos estilos de retrato</b><span>Fondo blanco con luz pareja, o fondo negro con luz lateral. Proponemos el oscuro para piezas y el claro para el sitio.</span></div>
    <div><b>Oficina</b><span>Luz de día, muebles blancos, mamparas azules y el muro de pantallas. El azul de las mamparas no es de la paleta.</span></div>
    <div><b>Sin tratamiento</b><span>Proponemos usar las fotos tal cual: sin filtros, duotonos ni degradados encima, y siempre con el texto en una banda aparte.</span></div>
    <div><b>Encuadre</b><span>Las fotos de oficina son horizontales: en 9:16 solo cabe una franja. Los retratos son verticales y funcionan en stories.</span></div>
    <div><b>Marca en la escena</b><span>El isotipo púrpura aparece en las pantallas del evento y la A de la marca en el letrero «YOU CAN».</span></div>
  </div>
  {{s2}}
  <div class="av-renders">{{fondos}}</div>
  <p class="nota">Aquí se muestran copias JPG reducidas a 1800 px. Los originales son PNG de unos 3050 × 1664 px con transparencia, y están en <code>references/</code>.</p>
  {{s3}}
  <div class="av-renders">{{isotipos}}</div>
  {{s4}}
  <div class="av-renders">{{mockups}}</div>
  <p class="nota">Son montajes sobre plantillas, no fotografías de piezas impresas. Cuatro traen datos de una persona (nombre, correo, teléfono o retrato): de esos solo se publica una copia chica, donde el correo, el teléfono y la dirección no se leen (el nombre y el cargo sí), y el original se queda fuera del repo.</p>
</div>""", s0=sub("Fotografía del equipo", "guia", "22 de 272"), equipo=equipo, retratos=retratos,
               s1=sub("Lo que se observa y cómo proponemos usarla", "bno"),
               s2=sub("Fondos de marca", "guia", "carpeta Layouts: 12 archivos, 11 distintos"), fondos=_tarjetas(FONDOS, "av-render__marco--claro"),
               s3=sub("El isotipo como ilustración", "guia"), isotipos=_tarjetas(ISOTIPOS, "av-render__marco--claro"),
               s4=sub("Aplicaciones", "guia", "8 mockups"), mockups=_tarjetas(MOCKUPS))
    return bloque(
        "fotografia", "Fotografía e imaginería",
        "Dos lenguajes: la fotografía real del equipo (oficina, centro de monitoreo, retratos y evento, todos vestidos de negro) "
        "y los fondos abstractos con degradados de magenta, púrpura, cian y navy. Las aplicaciones impresas son negras con el isotipo en púrpura.",
        "guia", "brand/assets/imagery-foto-* · references/ · brand/assets/imagery-*", cuerpo,
        ["¿Hay autorización de uso de imagen de las personas que aparecen? Sin ella, las fotos son solo para revisión interna.",
         "¿Retrato claro u oscuro? La sesión tiene los dos; proponemos oscuro en piezas y claro en el sitio.",
         "Las fotos de oficina muestran pantallas con tableros reales. ¿Se pueden publicar así?",
         "Ya hay fotos reales: ¿se dejan de usar las imágenes generadas que traen las piezas de LinkedIn?",
         "Los fondos no traen reglas: cuáles son para claro, cuáles para oscuro, y si se puede escribir encima. Proponemos no escribir sobre ellos.",
         "Fondo 09 (malla de puntos) no comparte la geometría del resto y parece de stock. ¿Tiene licencia?",
         "Los mockups traen el nombre y el correo de una persona con dominio avantika.com.mx, y las piezas dicen avantika.mx. ¿Cuál es el oficial?"])


def s_espaciado():
    pasos = [8, 16, 24, 32, 48, 64, 96, 128]
    barras = "".join('<div><i style="width:%dpx;height:%dpx"></i>%d</div>' % (min(p, 96), p, p) for p in pasos)
    cuerpo = T("""
<div class="lienzo">
  {{s1}}
  <div class="av-espacios">{{barras}}</div>
  <p class="nota"><code>--av-space-1</code> a <code>--av-space-8</code>, en px, en <code>brand/tokens/spacing.css</code>. Todo espaciado es múltiplo de 8.</p>
  {{s2}}
  <div class="av-radios">
    <div><i></i>0 · tarjetas, imágenes y bandas</div>
    <div><i style="border-radius:4px"></i>4 px · botones y campos</div>
    <div><i style="border:0;border-top:1px solid {{linea}};height:1px;margin:36px 0 35px"></i>Filete de 1 px · en vez de sombra</div>
  </div>
  {{s3}}
  <div class="av-formatos">
    <div class="av-formato"><div class="av-formato__caja" style="width:160px;height:200px"><div class="av-formato__zona" style="inset:12px">80 px</div></div>Feed 4:5 · 1080 × 1350 · margen de 80 px</div>
    <div class="av-formato"><div class="av-formato__caja" style="width:150px;height:200px"><div class="av-formato__zona" style="inset:11px">80 px</div></div>LinkedIn 3:4 · 1080 × 1440 · el formato de las piezas recibidas</div>
    <div class="av-formato"><div class="av-formato__caja" style="width:160px;height:160px"><div class="av-formato__zona" style="inset:12px">80 px</div></div>Cuadrado 1:1 · 1080 × 1080 · margen de 80 px</div>
    <div class="av-formato"><div class="av-formato__caja" style="width:135px;height:240px"><div class="av-formato__tapa" style="top:0;height:31px"></div><div class="av-formato__tapa" style="bottom:0;height:42px"></div><div class="av-formato__zona" style="left:10px;right:10px;top:31px;bottom:42px">zona segura</div></div>Story y Reel 9:16 · 1080 × 1920 · 250 px libres arriba, 340 px abajo y 80 px a los lados</div>
  </div>
  <p class="nota">Las franjas rayadas son lo que tapa la interfaz de Instagram. Las piezas de LinkedIn recibidas usan márgenes de unos 35 a 55 px, menores que los 80 que proponemos.</p>
</div>""", s1=sub("Escala de espacio", "bno"), barras=barras, s2=sub("Esquinas y filetes", "bno"), linea=LINEA, s3=sub("Formatos para redes", "bno"))
    return bloque(
        "espaciado", "Espaciado y retícula",
        "El material no define nada de esto. Proponemos una escala de base 8, esquinas rectas que acompañan los triángulos y las ventanas de la marca, "
        "filetes en lugar de sombras y márgenes fijos para las piezas de redes.",
        "bno", "brand/tokens/spacing.css · effects.css", cuerpo,
        ["¿Esquinas rectas? Las ventanas y el isotipo son angulares, pero el fondo 02 muestra un interruptor redondeado y las piezas de LinkedIn usan botones de píldora.",
         "Las ventanas tienen esquinas en chaflán. ¿Deben convertirse en la forma de tarjetas e imágenes? No lo hicimos por no inventar una regla.",
         "Falta definir ancho máximo de contenido y aire entre secciones para web; aquí usamos 1200 px y 64 px.",
         "¿El formato de LinkedIn es 3:4 (1080 × 1440), como las piezas recibidas, o 4:5?"])


def s_componentes():
    cuerpo = T("""
<div class="lienzo av" style="display:grid;gap:16px">
  {{s1}}
  <div class="av-panel">
    <div class="av-item"><a class="av-btn" href="#componentes">Agenda tu diagnóstico</a><small>Primario</small></div>
    <div class="av-item"><a class="av-btn is-hover" href="#componentes">Agenda tu diagnóstico</a><small>Primario · hover</small></div>
    <div class="av-item"><a class="av-btn is-focus" href="#componentes">Agenda tu diagnóstico</a><small>Primario · foco</small></div>
    <div class="av-item"><a class="av-btn av-btn--sec" href="#componentes">Ver servicios</a><small>Secundario</small></div>
    <div class="av-item"><a class="av-btn av-btn--sm" href="#componentes">Agendar</a><small>Chico</small></div>
    <div class="av-item"><button class="av-btn" disabled>Enviado</button><small>Deshabilitado</small></div>
    <div class="av-item"><a class="av-link" href="#componentes">Conoce al equipo</a><small>Link · subrayado en magenta</small></div>
  </div>
  <div class="av-panel av-panel--oscuro">
    <div class="av-item"><a class="av-btn av-btn--inv" href="#componentes">Agenda tu diagnóstico</a><small>Inverso</small></div>
    <div class="av-item"><a class="av-btn av-btn--inv-sec" href="#componentes">Habla con un especialista</a><small>Inverso secundario</small></div>
    <div class="av-item"><span class="av-badge av-badge--inv">Cybersecurity</span><small>Badge cian · solo sobre navy</small></div>
    <div class="av-item"><hr class="av-rule av-rule--inv"><small>Pleca cian</small></div>
  </div>
  {{s2}}
  <div class="av-panel">
    <div class="av-item"><span class="av-badge">Soporte TI</span><small>Badge de línea</small></div>
    <div class="av-item"><span class="av-badge av-badge--navy">Ciberseguridad</span><small>Badge navy</small></div>
    <div class="av-item"><span class="av-badge av-badge--purple">Infraestructura</span><small>Badge púrpura</small></div>
    <div class="av-item"><span class="av-eyebrow">Servicios</span><small>Eyebrow · púrpura, peso 600</small></div>
    <div class="av-item"><hr class="av-rule"><small>Pleca de acento · magenta, 32 × 2 px</small></div>
  </div>
  {{s3}}
  <div class="av-panel">
    <article class="av-cards">
      <div class="av-card"><div class="av-card__foto"><img src="{{img}}layout-12.jpg" alt="" loading="lazy"></div><div class="av-card__cuerpo"><span class="av-eyebrow">Servicio</span><h4 class="av-title">Ciberseguridad</h4><p>Protegemos lo que importa para que tú sigas creciendo.</p></div></div>
      <div class="av-card"><div class="av-card__cuerpo"><img src="{{ico}}28.png" alt="" style="width:64px;height:64px"><h4 class="av-title">Soporte TI</h4><p>Mesa de ayuda, técnicos en sitio y en campo.</p><p>Tiempo de respuesta: {{ph}}</p><a class="av-link" href="#componentes">Ver alcance</a></div></div>
      <div class="av-card av-card--navy"><div class="av-card__cuerpo"><span class="av-eyebrow">Diagnóstico</span><h4 class="av-title">Un solo equipo</h4><p>Ordena, protege y monitorea tu TI.</p></div></div>
    </article>
  </div>
  {{s4}}
  <div class="av-panel av-panel--blanco">
    <form class="av-form" onsubmit="return false">
      <div class="av-campo"><label for="f-nombre">Nombre completo</label><input id="f-nombre" type="text" autocomplete="off"></div>
      <div class="av-campo"><label for="f-correo">Correo de trabajo</label><input id="f-correo" type="text" placeholder="nombre@empresa.com" autocomplete="off"></div>
      <div class="av-campo"><label for="f-tel">Teléfono</label><input id="f-tel" type="text" autocomplete="off"><small>Con lada</small></div>
      <div class="av-campo"><label for="f-interes">Me interesa</label><select id="f-interes"><option>Soporte TI</option><option>Ciberseguridad</option><option>Infraestructura</option><option>IA segura</option></select></div>
      <label class="av-check"><input type="checkbox"> Acepto el aviso de privacidad</label>
    </form>
  </div>
  <p class="nota">Formulario de muestra: no envía datos. Los mismos componentes existen en React en <code>brand/components/</code>, con su ficha en <a href="../../components/core/core.card.html">core.card.html</a> y <a href="../../components/forms/forms.card.html">forms.card.html</a>.</p>
</div>""", s1=sub("Botones y links", "bno"), s2=sub("Badges, eyebrow y pleca", "bno"), s3=sub("Tarjetas", "bno"), img=IMG, ico=ICONOS, ph=PH,
               s4=sub("Formulario", "bno"))
    return bloque(
        "componentes", "Componentes web",
        "No existe ningún componente en el material. Estos son un punto de partida armado solo con los tokens: "
        "botones navy de radio mínimo, campos con borde fino, tarjetas con filete y sin sombra.",
        "bno", "brand/components/", cuerpo,
        ["¿El botón primario es navy? El magenta sería el color de acción más natural, pero no da contraste con texto claro (3.69:1) y con navy queda en 4.01:1.",
         "Las piezas de LinkedIn usan una píldora púrpura con «avantika.mx». No la adoptamos: no es un llamado a la acción y no hay regla que la respalde.",
         "El fondo 02 del material muestra un interruptor con degradado y el isotipo dentro. ¿Hay un lenguaje de interfaz diseñado que no nos llegó?",
         "Faltan estados de error y éxito para formularios; dependen de definir colores de estado."])


def s_landing():
    servicios = "".join(
        '<div class="av-card"><div class="av-card__cuerpo"><img src="%s%s.png" alt="" style="width:64px;height:64px" loading="lazy"><h4 class="av-title">%s</h4><p>%s</p></div></div>'
        % (ICONOS, n, t, p) for n, t, p in [
            ("28", "Soporte TI", "Mesa de ayuda, técnicos en sitio y en campo."),
            ("15", "Ciberseguridad", "Protegemos lo que importa para que tú sigas creciendo."),
            ("32", "Infraestructura", "Redes, servidores y cableado que no detienen tu operación."),
            ("14", "IA segura", "Protegemos tus datos para que adoptes IA sin frenar tu operación.")])
    cuerpo = T("""
<div class="lienzo">
  <div class="navegador">
    <div class="navegador__barra"><i></i><i></i><i></i><span>Vista de escritorio · ejemplo armado por BnO</span></div>
    <div class="av av-landing">
      <div class="av-landing__nav"><img src="{{ln}}" alt="Avantika"><nav><span>Servicios</span><span>Nosotros</span><span>Contacto</span></nav><a class="av-btn av-btn--sm" href="#landing">Agenda tu diagnóstico</a></div>
      <div class="av-landing__foto"><img src="{{img}}layout-12.jpg" alt=""></div>
      <div class="av-landing__banda">
        <span class="av-badge av-badge--inv">Cybersecurity</span>
        <h3 class="av-title">Un solo equipo ordena, protege y monitorea tu TI</h3>
        <p>Tu tecnología al ritmo de tu operación.</p>
        <div class="av-fila"><a class="av-btn av-btn--inv" href="#landing">Agenda tu diagnóstico</a><a class="av-btn av-btn--inv-sec" href="#landing">Habla con un especialista</a></div>
      </div>
      <div class="av-landing__seccion">
        <div style="display:grid;gap:8px"><hr class="av-rule"><span class="av-eyebrow">Servicios</span><h3 class="av-title">Ordena, protege, crece</h3></div>
        <div class="av-cards av-cards--4">{{servicios}}</div>
      </div>
      <div class="av-landing__seccion" style="padding-top:0">
        <div class="av-landing__dos" style="align-items:center">
          <div class="av-card__foto" style="aspect-ratio:3 / 2"><img src="{{img}}foto-soc-you-can.jpg" alt="Centro de monitoreo de Avantika" loading="lazy"></div>
          <div style="display:grid;gap:16px"><span class="av-eyebrow">Nosotros</span><h3 class="av-title">Un solo equipo</h3><p>Nuestra visión es ser la compañía de Ciberseguridad &amp; TI preferida en México por su confiabilidad, participación de mercado y ecosistema único de formación de especialistas.</p></div>
        </div>
      </div>
      <div class="av-landing__seccion" style="padding-top:0">
        <div class="av-landing__dos">
          <div style="display:grid;gap:16px"><span class="av-eyebrow">En cifras</span><h3 class="av-title">Cobertura y niveles de servicio</h3><p>Remoto, en sitio y en campo. Las cifras se publican cuando el cliente las valide.</p></div>
          <div class="av-datos"><div><b>{{ph}}</b><span>Disponibilidad</span></div><div><b>{{ph}}</b><span>Tiempo de respuesta</span></div><div><b>{{ph}}</b><span>Cobertura</span></div><div><b>{{ph}}</b><span>Horario de monitoreo</span></div></div>
        </div>
      </div>
      <div class="av-landing__cierre"><h3 class="av-title">Hoy, tu empresa no se detiene</h3><p>Tú sigue creciendo. Nosotros cuidamos tu espalda.</p><a class="av-btn av-btn--inv" href="#landing">Agenda tu diagnóstico</a></div>
      <div class="av-landing__pie">
        <img src="{{ltba}}" alt="Avantika Cybersecurity">
        <div><b style="font-weight:600">Contacto</b><br>{{ph}}<br>{{ph}}</div>
        <div><b style="font-weight:600">Sitio</b><br>avantika.mx</div>
        <p class="av-landing__legal">Ejemplo de BnO. Aviso de privacidad y datos legales: {{ph}}</p>
      </div>
    </div>
  </div>
  <p class="nota">La versión navegable, hecha con los componentes de React, está en <a href="../website/">brand/ui_kits/website/</a>.</p>
</div>""", ln=L_NEGRO, img=IMG, servicios=servicios, ph=PH, ltba=LT_BLANCO_AZUL)
    return bloque(
        "landing", "Landing de ejemplo",
        "Una página de captación armada con los componentes de arriba, para ver el sistema en conjunto. "
        "No copia ningún sitio existente. Todo dato sin respaldo va como placeholder.",
        "bno", "brand/ui_kits/website/", cuerpo,
        ["El titular, el apoyo, el cierre y los textos de servicio son literales de las piezas de LinkedIn. No consta que el cliente los haya aprobado. La visión de «Nosotros» está copiada del muro de la oficina.",
         "La foto del centro de monitoreo muestra a personas del equipo: necesita autorización de uso de imagen antes de ir a un sitio público.",
         "Disponibilidad, tiempos, cobertura, horario y contacto van como placeholder: las piezas dan cifras, pero nada las respalda.",
         "«IA segura» es un nombre nuestro para lo que las piezas llaman #CyberForAI. La lista oficial de servicios está por pedir.",
         "El héroe separa imagen y texto en lugar de escribir sobre el fondo. ¿Se prefiere el titular sobre la imagen?",
         "Los íconos van en su azul de archivo (#071436) sobre blanco. Sobre la banda navy no se pueden usar: no hay versión clara."])


def s_posts():
    cuerpo = T("""
<div class="lienzo">
  <div class="av-piezas">
    <figure class="av-pieza-wrap"><div class="av-pieza av-pieza--45">
      <div class="av-pieza__foto"><img src="{{img}}layout-12.jpg" alt="" loading="lazy" style="object-position:70% 50%"></div>
      <div class="av-pieza__banda"><div style="display:grid;gap:3cqw"><hr class="av-rule"><p class="av-title">Infraestructura sin caídas, sin sorpresas</p><p class="av-pieza__apoyo">Redes, servidores y cableado que no detienen tu operación.</p></div><div class="av-pieza__firmas"><img src="{{ltba}}" alt="Avantika Cybersecurity"><img src="{{iso}}" alt=""></div></div>
    </div><figcaption><b>Fondo con banda</b> · fondo de marca arriba y banda navy con titular y firma. El texto nunca va sobre la imagen.</figcaption></figure>

    <figure class="av-pieza-wrap"><div class="av-pieza av-pieza--45">
      <div class="av-pieza__foto"><img src="{{img}}foto-oficina-equipo.jpg" alt="" loading="lazy" style="object-position:60% 50%"></div>
      <div class="av-pieza__banda"><div style="display:grid;gap:3cqw"><hr class="av-rule"><p class="av-title">Soporte que responde cuando lo necesitas</p><p class="av-pieza__apoyo">Mesa de ayuda, técnicos en sitio y en campo.</p></div><div class="av-pieza__firmas"><img src="{{ltba}}" alt="Avantika Cybersecurity"><img src="{{iso}}" alt=""></div></div>
    </div><figcaption><b>Foto del equipo con banda</b> · fotografía real arriba y banda navy con titular y firma. Requiere autorización de uso de imagen.</figcaption></figure>

    <figure class="av-pieza-wrap"><div class="av-pieza av-pieza--45 av-pieza--tarjeta"><div class="av-pieza__in">
      <span class="av-pieza__num">01</span>
      <div style="display:grid;gap:3cqw"><hr class="av-rule"><p class="av-title">Datos sensibles en herramientas abiertas</p><p class="av-pieza__apoyo">La IA no es el riesgo. Los accesos sin control, sí.</p></div>
      <div class="av-pieza__firmas"><img src="{{ltn}}" alt="Avantika Cybersecurity"><span></span></div>
    </div></div><figcaption><b>Tarjeta tipográfica</b> · fondo blanco azulado, marco de filete, número en púrpura y pleca magenta. Para carruseles que explican un tema.</figcaption></figure>

    <figure class="av-pieza-wrap"><div class="av-pieza av-pieza--45 av-pieza--purple"><div class="av-pieza__in">
      <img src="{{ltb}}" alt="Avantika Cybersecurity" style="width:56cqw">
      <div style="display:grid;gap:4cqw;justify-items:center"><hr class="av-rule"><p class="av-title">Tú sigue corriendo. Nosotros cuidamos tu espalda.</p><span class="av-pieza__cta">Agenda tu diagnóstico</span></div>
      <img src="{{iso}}" alt="" style="width:10cqw">
    </div></div><figcaption><b>Cierre</b> · fondo púrpura, composición centrada y llamado a la acción. Última lámina de un carrusel.</figcaption></figure>
  </div>
  <p class="nota">Composiciones en HTML solo para revisar proporciones y jerarquía, en 4:5 (1080 × 1350) con margen de 80 px. Los textos son literales de las piezas de LinkedIn recibidas. Si no tienes las fuentes instaladas, verás el fallback.</p>
</div>""", img=IMG, ltba=LT_BLANCO_AZUL, iso=ISO_BLANCO, ltn=LT_NEGRO, ltb=LT_BLANCO)
    return bloque(
        "posts", "Posts para redes",
        "Cuatro modos de pieza para feed armados solo con lo que sí es de la marca: su paleta, sus fondos, sus fotos, su logotipo de archivo y sus dos tipografías. "
        "Son la alternativa a las piezas recibidas, que no siguen la identidad.",
        "bno", "brand/arquetipos.json", cuerpo,
        ["¿Se rehacen las piezas de LinkedIn con estos modos, o el cliente prefiere el estilo violeta con imágenes generadas que ya tiene?",
         "Proponemos no escribir sobre los fondos: son degradados con zonas muy claras y muy oscuras, y ningún color de texto contrasta en toda la superficie.",
         "La firma va abajo a la izquierda, con el isotipo en el extremo opuesto sobre oscuro. Falta la regla del cliente.",
         "Con la fotografía del equipo, la parrilla ya no depende solo de los 11 fondos. Falta la autorización de uso de imagen.",
         "El magenta queda solo como pleca. ¿Se quiere más presente? Como fondo completo no admite texto claro con buen contraste."])


def s_stories():
    filas = []
    ig = ('<span class="av-pieza__ig av-pieza__ig--arriba">Interfaz de Instagram</span>'
          '<span class="av-pieza__ig av-pieza__ig--abajo">Interfaz de Instagram</span>')
    for titulo, cuadros in VERTICALES:
        piezas = []
        for i, (foto, pos, tit, apoyo) in enumerate(cuadros):
            piezas.append(
                '<figure class="av-pieza-wrap"><div class="av-pieza av-pieza--916">'
                '<div class="av-pieza__foto"><img src="%s%s.jpg" alt="" loading="lazy" style="object-position:%s 50%%"></div>'
                '<div class="av-pieza__banda"><hr class="av-rule"><p class="av-title">%s</p><p class="av-pieza__apoyo">%s</p></div>'
                '%s</div><figcaption><b>%d a %d s</b>%s</figcaption></figure>'
                % (IMG, foto, pos, e(tit), e(apoyo), ig, i * 4, i * 4 + 4, " · gancho" if i == 0 else ""))
        piezas.append(
            '<figure class="av-pieza-wrap"><div class="av-pieza av-pieza--916 av-pieza--cierre"><div class="av-pieza__in">'
            '<img src="%s" alt="Avantika Cybersecurity"><p class="av-title">Un solo equipo ordena, protege y monitorea tu TI</p>'
            '<span class="av-pieza__cta">Agenda tu diagnóstico</span><img class="av-iso" src="%s" alt=""></div>%s</div>'
            '<figcaption><b>12 a 15 s</b> · cierre</figcaption></figure>' % (LT_BLANCO_AZUL, ISO_BLANCO, ig))
        filas.append('<div class="av-anuncio">%s<div class="av-piezas av-piezas--story">%s</div></div>'
                     % (sub(titulo, "bno"), "".join(piezas)))
    cuerpo = T("""
<div class="lienzo" id="lienzo-stories">
  <button class="boton-shell" type="button" id="boton-ig" aria-pressed="false">Mostrar lo que tapa la interfaz de Instagram</button>
  {{filas}}
  <p class="nota">Tres cuadros de 4 segundos y un cierre de 3. Los titulares son los de los dos carruseles recibidos; se unieron en una sola frase las líneas que venían partidas. El carrusel A cierra con «Agenda tu diagnóstico sin costo»: aquí se omite «sin costo» hasta que el cliente lo valide.</p>
</div>""", filas="".join(filas))
    return bloque(
        "stories", "Story y Reel",
        "Los dos carruseles de LinkedIn recibidos, llevados a vertical 9:16 de 15 segundos: foto del equipo o fondo de marca arriba, banda navy con el texto "
        "y cierre con logotipo y llamado a la acción. No hay guion ni brief de video del cliente.",
        "bno", "campaigns/linkedin-set-6-posts/guion.md", cuerpo,
        ["¿El cliente quiere formato vertical? El material solo trae piezas para LinkedIn.",
         "El vertical A ya usa fotos del equipo (manos en el teclado y el centro de monitoreo) en lugar de las personas generadas de la pieza original. El B sigue con fondos abstractos.",
         "Faltan reglas de duración, transiciones y sonido.",
         "El tagline del cierre va en cian sobre navy (11.13:1). Es el único lugar donde proponemos el cian como texto."])


def s_piezas():
    galeria = "".join(
        '<figure><img src="%spost-linkedin-%02d.jpg" alt="%s" loading="lazy"><figcaption><b>%s</b>%s</figcaption></figure>'
        % (IMG, n, e("Pieza de LinkedIn %d: %s" % (n, titular.replace(" / ", " "))), e(rotulo), e(titular))
        for n, rotulo, titular in PIEZAS)
    cuerpo = T("""
<div class="lienzo">
  {{s1}}
  <div class="av-galeria">{{galeria}}</div>
  <p class="nota">1080 × 1440 px cada una. La carpeta se llama «Set de 6 posts» y trae 12 imágenes: 6 posts y 2 carruseles de 3 láminas. No viene el texto de acompañamiento ni se sabe quién las hizo, si están publicadas o si el cliente las aprobó.</p>
  {{s2}}
  <div class="av-compara">
    <div><b>Color</b><span>La identidad usa púrpura #87007D, magenta, cian y navy. Las piezas usan un violeta cercano a #9E009C con lilas y un negro azulado; no aparecen el magenta ni el navy.</span></div>
    <div><b>Tipografía</b><span>Ni Nebulica ni Swiza. Los titulares alternan una condensada muy pesada y una geométrica redonda, a veces dentro del mismo carrusel (láminas 7, 8 y 9).</span></div>
    <div><b>Logotipo</b><span>Recompuesto: isotipo con degradado y desenfoque a la izquierda y el nombre a la derecha. Esa versión no existe entre los archivos, y el nombre no es el del archivo oficial.</span></div>
    <div><b>Tagline</b><span>En cian y diminuto. Sobre las piezas claras queda a 1.40:1: no se lee.</span></div>
    <div><b>Imagen</b><span>Personas, oficinas y objetos 3D cuya procedencia no consta; por su acabado parecen generados con IA. Ahora hay fotografía real del equipo que puede sustituirlas.</span></div>
    <div><b>Elementos de marca</b><span>No usan las ventanas, el patrón, los íconos ni los fondos entregados.</span></div>
  </div>
  {{s3}}
  <div class="av-compara">
    <div><b>«Disponibilidad 99%» · «SLA cumplido»</b><span>Pieza 3. Cifra y compromiso de nivel de servicio.</span></div>
    <div><b>«Monitoreo 24/7»</b><span>Pieza 2. Horario de operación.</span></div>
    <div><b>«Cobertura Nacional» · «en todo México»</b><span>Pieza 4. Alcance geográfico.</span></div>
    <div><b>«Sin caídas» · «Sin riesgos» · «Imparable»</b><span>Piezas 2, 5 y 6. Promesas absolutas.</span></div>
    <div><b>«Agenda tu diagnóstico sin costo»</b><span>Pieza 9. Oferta comercial.</span></div>
    <div><b>avantika.mx</b><span>En las 12 piezas. Las tarjetas usan avantika.com.mx.</span></div>
  </div>
  <p class="nota">Todas van como {{ph}} en este sistema hasta que el cliente las valide por escrito.</p>
</div>""", s1=sub("Las 12 piezas de LinkedIn", "guia"), galeria=galeria,
               s2=sub("En qué se apartan de la identidad", "bno", "comparación de BnO contra los archivos de marca"),
               s3=sub("Afirmaciones que necesitan respaldo", "falta"), ph=PH)
    return bloque(
        "piezas", "Piezas producidas",
        "Lo único producido que llegó: un set de LinkedIn. Tiene buenos textos y una estructura clara de titular en tres líneas, "
        "pero visualmente es otra marca.",
        "guia", "references/post-linkedin-*.png · campaigns/linkedin-set-6-posts/", cuerpo,
        ["¿Quién hizo estas piezas y con qué instrucciones? Si son de BnO, hay que rehacerlas; si son del cliente, hay que preguntar si ese estilo es el que quiere.",
         "¿Están publicadas? Si ya salieron, la marca tiene hoy dos apariencias en el mismo canal.",
         "Los textos funcionan y los reutilizamos en la landing y en las propuestas. ¿Están aprobados?",
         "Las personas de las imágenes: ¿hay licencia o son generadas? En las láminas 9 y 10 aparecen pantallas con texto ilegible, típico de imagen generada.",
         "La lámina 12 usa un botón violeta con «Agenda tu diagnóstico»; las demás solo «avantika.mx». ¿Cuál es el llamado a la acción?"])


def s_voz():
    cuerpo = T("""
<div class="lienzo" style="display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">
  <div class="av av-especimen">
    <hr class="av-rule">
    <span class="av-eyebrow">Soporte TI</span>
    <p class="av-title" style="font-size:28px">Soporte que responde cuando lo necesitas</p>
    <p>Mesa de ayuda, técnicos en sitio y en campo.</p>
    <div><span class="av-btn">Agenda tu diagnóstico</span></div>
    <small>Titular y apoyo literales de la pieza 1; eyebrow y botón, armado de BnO.</small>
  </div>
  <div>
    {{s0}}
    <ul style="margin:0 0 16px;padding-left:20px;display:grid;gap:6px">
      <li><b>Visión</b>, rotulada en el muro de la oficina: «Nuestra visión es ser la compañía de Ciberseguridad &amp; TI preferida en México por su confiabilidad, participación de mercado y ecosistema único de formación de especialistas.»</li>
      <li><b>Letrero de la oficina</b>: «YOU CAN · END OF STORY», con la A de la marca.</li>
      <li><b>Tarjeta del evento</b>: «Gracias por tu colaboración. Tu compromiso hace que las cosas sucedan.» · #ValoresAvantika · #YouCan</li>
    </ul>
    {{s1}}
    <ul style="margin:0;padding-left:20px;display:grid;gap:6px">
      <li>Habla de tú y al dueño o director del negocio: «tu empresa», «tu operación», «tú sigue creciendo».</li>
      <li>Titulares en tres golpes cortos, con el del medio resaltado: «Ordena / Protege / Crece».</li>
      <li>Parte del problema cotidiano, no de la tecnología: «Lunes, 9 am. El sistema cayó. Nadie responde.»</li>
      <li>Quita culpa: «Nadie falló. Creciste.» · «La IA no es el riesgo.»</li>
      <li>Promete acompañamiento: «Nosotros cuidamos tu espalda.» · «Un solo equipo.»</li>
      <li>Hashtags en una palabra: #SoporteTI, #Ciberseguridad, #GestiónTI, #UnSoloEquipo, #CyberForAI, #Infraestructura.</li>
    </ul>
    {{s2}}
    <ul style="margin:0;padding-left:20px;display:grid;gap:6px">
      <li>Mantener el tú, las frases cortas y el punto de vista del negocio.</li>
      <li>Decir qué hace Avantika con verbos concretos: ordena, protege, monitorea, responde.</li>
      <li>Cambiar los absolutos por hechos comprobables: en vez de «sin caídas», el nivel de servicio validado.</li>
      <li>Un solo llamado a la acción por pieza. Proponemos «Agenda tu diagnóstico».</li>
      <li>Sin anglicismos innecesarios: el tagline ya está en inglés.</li>
    </ul>
    {{s3}}
    <p style="margin:0">Ninguno. No hay cifras, alcances, precios ni contactos validados en el material; todo dato va como <span class="av av-ph">[Dato por validar]</span>.</p>
  </div>
</div>""", s0=sub("Lo que la empresa dice de sí misma", "guia", "transcrito de las fotos de la oficina y del evento"),
               s1=sub("Cómo escriben las piezas recibidas", "guia", "observado; no es una regla del cliente"),
               s2=sub("Cómo proponemos que escriba", "bno"), s3=sub("Datos que se pueden usar", "falta"))
    return bloque(
        "voz", "Voz y tono",
        "No hay documento de voz. Lo que sigue reúne lo que la empresa escribe sobre sí misma en su oficina y en su evento, "
        "describe cómo suenan las doce piezas de LinkedIn y propone un tono a partir de eso: directo, de tú y del lado del negocio.",
        "bno", "brand-profile.md · brand/readme.md", cuerpo,
        ["¿El cliente reconoce esta voz como suya? Sale de piezas que no sabemos si aprobó.",
         "¿Tú o usted? Las piezas usan tú; el público parece ser dirección de empresas medianas.",
         "El tagline está en inglés y un hashtag también (#CyberForAI). ¿Se permite mezclar idiomas?",
         "«Nosotros cuidamos tu espalda» se repite en dos piezas, y «YOU CAN» aparece en la oficina y en el evento. ¿Alguno es lema oficial?",
         "La visión habla de «Ciberseguridad & TI» y de formar especialistas. ¿Es el posicionamiento que debe guiar los textos?"])


def s_reglas():
    cuerpo = T("""
<div class="hueco">
  <strong>El cliente no entregó reglas de contenido</strong>
  <p>No hay documento de qué se puede decir y qué no, lista oficial de servicios, afirmaciones aprobadas, restricciones legales ni datos de contacto vigentes.</p>
  <p>Para completarlo: pedirlo al cliente. Mientras llega, proponemos trabajar con las seis reglas provisionales de abajo.</p>
</div>
<div class="lienzo" style="margin-top:32px;display:grid;gap:32px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">
  <div>{{s1}}<ol style="margin:0;padding-left:20px;display:grid;gap:8px">{{reglas}}</ol></div>
  <div>
    {{s2}}
    <p style="margin:0 0 12px">No se completa por inferencia. En esta página usamos el placeholder genérico:</p><span class="av av-ph">[Dato por validar]</span>
    {{s3}}
    <p style="margin:0">Solo dos cosas del material funcionan como regla escrita: los cinco colores del PDF y la licencia de Swiza, que prohíbe redistribuir la fuente y convertirla a webfont.</p>
  </div>
</div>""", s1=sub("Reglas provisionales", "bno", "ninguna viene del cliente"),
               reglas="".join("<li>%s</li>" % e(x) for x in REGLAS_BNO),
               s2=sub("Si falta un dato"), s3=sub("Lo que sí está escrito", "guia"))
    return bloque(
        "reglas", "Reglas y contenido",
        "Lo que cualquier persona o agente debería respetar antes de producir para Avantika. "
        "El cliente no entregó nada de esto: lo que hay es propuesta de BnO.",
        "falta", "brand/reglas-consolidadas-2026-10-13.md", cuerpo,
        ["¿Qué servicios vende Avantika, con qué nombres y en qué orden de importancia?",
         "¿Qué puede prometer? En ciberseguridad y soporte, las cifras de disponibilidad y los tiempos de respuesta suelen estar en contrato.",
         "¿Hay restricciones para nombrar clientes, fabricantes o certificaciones?",
         "¿Hay un proceso de aprobación antes de publicar o de encender formularios?"])


def s_huecos():
    orden = {"Alta": 0, "Media": 1, "Baja": 2}
    lista = sorted(HUECOS, key=lambda h: orden[h[3]])
    items = "".join(
        '<li>%s<div><b>%s</b><span>%s</span><span class="accion">Acción: %s</span>'
        '<div class="huecos__meta"><em>%s</em><em>%s</em></div></div></li>'
        % (marca("falta"), e(t), e(q), e(a), p, o) for t, q, a, p, o in lista)
    cuenta = {p: sum(1 for h in HUECOS if h[3] == p) for p in orden}
    return bloque("huecos", "Huecos por completar",
                  "Lo que habría que pedir al cliente o definir nosotros para cerrar el sistema, de mayor a menor prioridad: "
                  "%d de prioridad alta, %d media y %d baja." % (cuenta["Alta"], cuenta["Media"], cuenta["Baja"]),
                  "falta", "", '<ol class="huecos">%s</ol>' % items, texto_estado="%d pendientes" % len(HUECOS))


def pagina():
    nav = "".join('<li><a href="#%s">%s%s</a></li>'
                  % (ident, marca(tipo) if tipo else '<span class="marca" aria-hidden="true"></span>', e(titulo))
                  for ident, titulo, tipo in SECCIONES)
    secciones = "\n".join(f() for f in (s_resumen, s_logotipo, s_color, s_tipografia, s_iconos, s_fotografia, s_espaciado,
                                        s_componentes, s_landing, s_posts, s_stories, s_piezas, s_voz, s_reglas, s_huecos))
    return T("""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Avantika · Revisión del sistema de diseño</title>
<meta name="description" content="Revisión interna del sistema de diseño de Avantika: logotipo, color, tipografía, íconos, componentes, landing y piezas para redes.">
<link rel="stylesheet" href="../../tokens/fonts.css">
<link rel="stylesheet" href="../../tokens/colors.css">
<link rel="stylesheet" href="../../tokens/typography.css">
<link rel="stylesheet" href="../../tokens/spacing.css">
<link rel="stylesheet" href="../../tokens/effects.css">
<link rel="stylesheet" href="review.css">
<link rel="stylesheet" href="avantika.css">
</head>
<body>
<div class="review">
  <aside class="rail">
    <div class="rail__top">
      <div><div class="rail__agencia">black n orange</div><p class="rail__cliente">Avantika</p><p class="rail__sub">Revisión del sistema de diseño</p></div>
    </div>
    <nav class="rail__nav" aria-label="Secciones"><details open><summary>Secciones</summary><ol>{{nav}}</ol></details></nav>
    <div class="rail__pie"><p>Propuesta para comentarios</p><p>{{fecha}}</p></div>
  </aside>
  <main class="main">
    <header class="av av-hero">
      <div class="av-hero__panel">
        <img class="av-hero__logo" src="{{logo}}" alt="Avantika Cybersecurity">
        <div class="av-hero__texto">
          <span class="av-hero__estado">Propuesta para comentarios</span>
          <h1 class="av-title">Sistema de diseño</h1>
          <p>Revisión interna. Todo lo que ves está armado con los colores, los logos, los íconos y los fondos que entregó el cliente para Avantika. No llegó manual de marca: esta página sirve para decidir qué está completo, qué proponemos y qué falta pedir.</p>
        </div>
        <span style="font-size:12px">Revisión interna · {{fecha}}</span>
      </div>
      <div class="av-hero__foto"><img src="{{img}}layout-12.jpg" alt="Fondo de marca: panel translúcido con luz azul y magenta sobre navy." fetchpriority="high"></div>
    </header>
{{secciones}}
    <footer class="pie">
      <p>Herramienta interna de Black &amp; Orange para revisar sistemas de diseño. No es material para el cliente ni sustituye su guía de marca.</p>
      <p>Generado el {{fecha}} con <code>brand/ui_kits/revision/source/build.py</code> desde el repo avantika.</p>
    </footer>
  </main>
</div>
<script src="review.js"></script>
</body>
</html>
""", nav=nav, fecha=FECHA, logo=LT_BLANCO_AZUL, img=IMG, secciones=secciones)


def main():
    (RAIZ / "index.html").write_text(pagina(), encoding="utf-8")
    pares = [{"label": "%s · %s" % (et, uso), "foreground": fg, "background": bg, "minimum": minimo}
             for et, uso, fg, bg, minimo in PARES]
    (RAIZ / "source" / "contrast-pairs.json").write_text(json.dumps(pares, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("index.html y source/contrast-pairs.json generados · %d secciones · %d huecos" % (len(SECCIONES) - 1, len(HUECOS)))


if __name__ == "__main__":
    main()
