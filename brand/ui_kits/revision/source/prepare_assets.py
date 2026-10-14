#!/usr/bin/env python3
"""Arma brand/assets, brand/bg, brand/uploads y references/ a partir de las carpetas originales del cliente.

Uso, desde la raíz del repo:  python3 brand/ui_kits/revision/source/prepare_assets.py
Necesita Pillow y poppler (pdftoppm). Las carpetas originales («Material Avantika», «Tipografías Avantika»
y «Set de 6 posts de LinkedIn para Avantika») no se suben al repo: aquí queda escrito qué se copió y cómo se derivó.
Nada de lo que copia se modifica; lo derivado (imagery-*, bg/, img/) se regenera con este script.
"""
import hashlib, json, pathlib, shutil, subprocess, zipfile
from PIL import Image, ImageDraw, ImageFont

R = pathlib.Path(__file__).resolve().parents[4]
MAT, TIP, SET = R / "Material Avantika", R / "Tipografías Avantika", R / "Set de 6 posts de LinkedIn para Avantika"
ELEM = TIP / "5. Elementos visulaes"
B, REF = R / "brand", R / "references"
REV = B / "ui_kits" / "revision"
HIELO, TINTA = (244, 250, 255), (29, 29, 27)
filas = []  # (destino, qué es, nombre original, medida, sha, publicado)


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def copia(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    assert sha(src) == sha(dst)


def medida(p):
    try:
        with Image.open(p) as im:
            return "%d×%d" % im.size
    except Exception:
        return "%.1f MB" % (pathlib.Path(p).stat().st_size / 1e6)


def ref(src, nombre, que, publicado=True, origen=None):
    copia(src, REF / nombre)
    filas.append((nombre, que, origen or src.name, medida(src), sha(src)[:16], publicado))


def jpg(src, dst, lado=1800, fondo=None, calidad=80):
    im = Image.open(src)
    if im.mode == "RGBA":
        base = Image.new("RGB", im.size, fondo or HIELO)
        base.paste(im, (0, 0), im)
        im = base
    im = im.convert("RGB")
    im.thumbnail((lado, lado), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, quality=calidad, optimize=True)


# ---------- Logos (copias byte a byte con nombre limpio) ----------
LOGOS = [
    ("Avantika-logo-blanco@4x (1).png", "logo-avantika-blanco.png", "Logotipo (wordmark) en blanco"),
    ("Avantika-logo-negro@4x (1).png", "logo-avantika-negro.png", "Logotipo (wordmark) en negro #000000"),
    ("Avantika-logo-tagline-blanco-azul@4x (1).png", "logo-avantika-tagline-blanco-azul.png", "Logotipo blanco con tagline Cybersecurity en cian #00F5D4"),
    ("Avantika-logo-tagline-blanco@4x (1).png", "logo-avantika-tagline-blanco.png", "Logotipo con tagline, todo en blanco"),
    ("Avantika-logo-tagline-negro-azul@4x (1).png", "logo-avantika-tagline-negro-azul.png", "Logotipo #1D1D1B con tagline en cian #00F5D4"),
    ("Avantika-logo-tagline-negro@4x (1).png", "logo-avantika-tagline-negro.png", "Logotipo #1D1D1B con tagline en #000000"),
    ("Avantika-icono-blanco@4x (1).png", "isotipo-avantika-blanco.png", "Isotipo (A triangular) en blanco"),
    ("Logo_Avantika_Blanco_Completo.png", "logo-avantika-completo-blanco.png", "Versión apilada isotipo + nombre + tagline; baja resolución y tagline en otra tipografía"),
]
for orig, limpio, que in LOGOS:
    copia(MAT / orig, B / "assets" / limpio)
    ref(MAT / orig, limpio, que)
    im = Image.open(MAT / orig).convert("RGBA")
    caja = im.getbbox()
    im = im.crop(caja)
    im.thumbnail((1200, 1200), Image.LANCZOS)
    (REV / "img" / "logos").mkdir(parents=True, exist_ok=True)
    im.save(REV / "img" / "logos" / limpio)

# ---------- Íconos (34, del zip 4x) ----------
with zipfile.ZipFile(MAT / "4x.zip") as z:
    for n in range(1, 35):
        datos = z.read("4x/Avantika-icono-%d@4x.png" % n)
        dst = B / "assets" / "icons" / ("avantika-icono-%02d.png" % n)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(datos)

# ---------- Elementos visuales ----------
for n in ("ventana-1", "ventana-2", "ventana-3", "ventana-4", "triangulo"):
    copia(ELEM / "Ventana" / "SVG" / ("Avantika-%s.svg" % n), B / "assets" / "elementos" / (n + ".svg"))
    copia(ELEM / "Ventana" / "PNG" / ("Avantika-%s.png" % n), B / "assets" / "elementos" / (n + ".png"))
copia(ELEM / "Patron" / "Avantika- patron.png", B / "assets" / "elementos" / "patron.png")
ref(ELEM / "Patron" / "Avantika- patron.png", "patron-avantika.png", "Patrón de triángulos e isotipos, #1D1D1B sobre transparente")

# ---------- Layouts (fondos) ----------
NOTAS_LAYOUT = {1: "Triángulo translúcido sobre degradado magenta, púrpura y cian", 2: "Fondo claro con interruptor, triángulos y líneas punteadas",
                3: "Fragmentos de triángulo desenfocados sobre blanco azulado", 4: "Volumen isométrico sobre cian", 5: "Franja diagonal magenta y púrpura con panel translúcido",
                6: "Ventana translúcida sobre magenta oscuro", 7: "Idéntico byte a byte a layout-06", 8: "Isotipo púrpura desenfocado sobre negro",
                9: "Malla de puntos magenta y azul sobre negro", 10: "Isotipo con efecto de barrido sobre negro", 11: "Isotipo en volumen isométrico sobre púrpura",
                12: "Ventana translúcida con luz azul y magenta sobre navy"}
for n in range(1, 13):
    src = ELEM / "Layouts" / "PNG" / ("Layouts-%02d.png" % n)
    ref(src, "layout-%02d.png" % n, NOTAS_LAYOUT[n])
    if n != 7:
        jpg(src, B / "assets" / ("imagery-layout-%02d.jpg" % n), fondo=HIELO)

# ---------- Isotipo ilustrado ----------
ISO = [("a icon 2.jpg", "isotipo-barrido.jpg", "Isotipo con efecto de barrido sobre negro, 4K", None),
       ("a icon 3.png", "isotipo-cristal.png", "Isotipo de cristal con luces, fondo transparente", TINTA),
       ("a icon 4.png", "isotipo-puntos.png", "Isotipo de puntos claros, fondo transparente; casi invisible sobre claro", TINTA),
       ("a transparent.png", "isotipo-degradado.png", "Isotipo púrpura con desenfoque, fondo transparente", HIELO),
       ("a transparent bw.png", "isotipo-degradado-bn.png", "Isotipo con desenfoque en escala de grises, fondo transparente", HIELO),
       ("a-contra.jpg", "isotipo-cristal-escena.jpg", "Isotipo de cristal en escena oscura con luz magenta", None)]
for orig, nombre, que, fondo in ISO:
    ref(MAT / orig, nombre, que)
    jpg(MAT / orig, B / "assets" / ("imagery-" + nombre.rsplit(".", 1)[0] + ".jpg"), fondo=fondo)

# ---------- Mockups de aplicación ----------
MOCK = [("Banner_Mockup (1).jpg", "mockup-banner.jpg", "Banner colgante: logotipo con tagline sobre isotipo magenta", True),
        ("Bus_Station_Citylight (1).jpg", "mockup-parabus.jpg", "Parabús: logotipo con tagline sobre isotipo púrpura", True),
        ("Carpeta_Mockup (1).jpg", "mockup-carpeta.jpg", "Carpetas negras con isotipo púrpura", True),
        ("Cup_Mockup2.jpg", "mockup-taza.jpg", "Taza con patrón en magenta y púrpura", True),
        ("Business_Card_Mockup.jpg", "mockup-tarjetas.jpg", "Tarjetas de presentación; trae nombre y correo de una persona", False),
        ("Business_Card_Mockup_6 (1).jpg", "mockup-tarjetas-2.jpg", "Tarjetas de presentación, vista 2; trae nombre y correo", False),
        ("Firma_correo.jpg", "mockup-firma-correo.jpg", "Firma de correo; trae nombre, teléfono, correo y dirección", False),
        ("gafete.jpg", "mockup-gafete.jpg", "Gafete con retrato, nombre, cargo y código QR", False)]
for orig, nombre, que, publico in MOCK:
    ref(MAT / orig, nombre, que, publicado=publico)
    # Con datos de una persona: copia chica. Las tarjetas bajan a 360 px porque a 640 aún se leía el correo.
    jpg(MAT / orig, B / "assets" / ("imagery-" + nombre), lado=1800 if publico else (360 if "tarjetas" in nombre else 640))

# ---------- QR (no se publican: no se pudo leer a dónde llevan) ----------
for orig, nombre in [("QR Avantika - CEO - Negro transparente.png", "qr-ceo-negro.png"), ("QR Avantika - ETIQUETA - Negro transparente.png", "qr-etiqueta-negro.png"),
                     ("QR Avantika - LIBRETA - Negro transparente.png", "qr-libreta-negro.png"), ("QR Avantika - PLAYERA - Blanco transparente.png", "qr-playera-blanco.png"),
                     ("QR Avantika - PLAYERA - Negro.png", "qr-playera-negro.png")]:
    ref(MAT / orig, nombre, "Código QR con isotipo al centro; destino sin verificar", publicado=False)

# ---------- Piezas de LinkedIn ----------
POSTS = {1: "Post #SoporteTI", 2: "Post #Ciberseguridad", 3: "Post #GestiónTI", 4: "Post #UnSoloEquipo", 5: "Post #CyberForAI", 6: "Post #Infraestructura",
         7: "Carrusel A, lámina 01/03", 8: "Carrusel A, lámina 02/03", 9: "Carrusel A, lámina 03/03",
         10: "Carrusel B, lámina 01/03", 11: "Carrusel B, lámina 02/03", 12: "Carrusel B, lámina 03/03"}
for n, que in POSTS.items():
    ref(SET / ("%d.png" % n), "post-linkedin-%02d.png" % n, que)
    jpg(SET / ("%d.png" % n), B / "assets" / ("imagery-post-linkedin-%02d.jpg" % n), lado=1080, calidad=84)

# ---------- Documentos del cliente, sin modificar ----------
UP = B / "uploads"
for src, sub in [(MAT / "Avatika-color (2).pdf", ""), (MAT / "Avantika hoja membretada.pdf", ""), (MAT / "Paleta de color Avantika.png", ""),
                 (MAT / "AI.zip", ""), (MAT / "4x.zip", ""), (MAT / "Layoutd.ai", ""),
                 (ELEM / "Patron" / "Avantika- patron.ai", "5. Elementos visulaes/Patron"), (ELEM / "Ventana" / "AI" / "Avatika-ventana.ai", "5. Elementos visulaes/Ventana/AI"),
                 (TIP / "Swiza Complete Desktop" / "Swiza_desktop_license.pdf", "Tipografías")]:
    copia(src, UP / sub / src.name)

# ---------- Fuentes: copia local, fuera del repo público por licencia ----------
for src in sorted((TIP / "Swiza Complete Desktop").glob("*.otf")):
    copia(src, B / "assets" / "fonts" / "Swiza" / src.name)
copia(TIP / "Swiza Complete Desktop" / "Swiza_desktop_license.pdf", B / "assets" / "fonts" / "Swiza" / "Swiza_desktop_license.pdf")
for src in sorted((TIP / "nebulica" / "otf").glob("*.otf")):
    copia(src, B / "assets" / "fonts" / "Nebulica" / src.name)
copia(TIP / "nebulica" / "variable" / "Nebulica-VF.ttf", B / "assets" / "fonts" / "Nebulica" / "Nebulica-VF.ttf")

# ---------- Documentos como imagen ----------
(B / "bg").mkdir(exist_ok=True)
subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", str(MAT / "Avatika-color (2).pdf"), str(B / "bg" / "color-p01")], check=True)
subprocess.run(["pdftoppm", "-r", "110", "-png", "-singlefile", str(MAT / "Avantika hoja membretada.pdf"), str(B / "bg" / "hoja-membretada-p01")], check=True)
jpg(MAT / "Paleta de color Avantika.png", B / "bg" / "paleta-de-color.jpg", lado=1536, calidad=84)

# ---------- Especímenes tipográficos (imagen, porque las fuentes no se pueden distribuir) ----------
NAVY = (1, 30, 94)
SW, NB = TIP / "Swiza Complete Desktop", TIP / "nebulica" / "otf"
(REV / "img" / "tipo").mkdir(parents=True, exist_ok=True)


def lamina(nombre, renglones, ancho=1600, margen=56, fondo=HIELO):
    alto = margen * 2 + sum(t + s for _, _, t, s, _ in renglones)
    im = Image.new("RGB", (ancho, alto), fondo)
    d = ImageDraw.Draw(im)
    y = margen
    for texto, fuente, tam, sep, color in renglones:
        d.text((margen, y), texto, font=ImageFont.truetype(str(fuente), tam), fill=color)
        y += tam + sep
    im.save(REV / "img" / "tipo" / nombre, optimize=True)


PURP = (135, 0, 125)
lamina("nebulica.png", [("Aa", NB / "Nebulica-Bold.otf", 220, 30, NAVY), ("Nebulica", NB / "Nebulica-Bold.otf", 64, 22, NAVY),
                        ("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", NB / "Nebulica-Medium.otf", 44, 14, NAVY), ("abcdefghijklmnñopqrstuvwxyz 0123456789", NB / "Nebulica-Medium.otf", 44, 30, NAVY),
                        ("Thin  ExtraLight  Light  Regular", NB / "Nebulica-Light.otf", 40, 12, PURP), ("Medium  SemiBold  Bold  ExtraBold  Black", NB / "Nebulica-Bold.otf", 40, 0, PURP)])
lamina("swiza.png", [("Aa", SW / "Swiza-Light.otf", 220, 30, NAVY), ("Swiza", SW / "Swiza-Bold.otf", 64, 22, NAVY),
                     ("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ", SW / "Swiza-Regular.otf", 44, 14, NAVY), ("abcdefghijklmnñopqrstuvwxyz 0123456789", SW / "Swiza-Regular.otf", 44, 30, NAVY),
                     ("Thin  ExtraLight  Light  Regular", SW / "Swiza-Light.otf", 40, 12, PURP), ("Medium  SemiBold  Bold  ·  con itálicas", SW / "Swiza-SemiBold.otf", 40, 0, PURP)])
lamina("escala.png", [("Display · 56 · Nebulica Bold", SW / "Swiza-Regular.otf", 22, 10, PURP), ("Un solo equipo para tu TI", NB / "Nebulica-Bold.otf", 112, 44, NAVY),
                      ("H1 · 40 · Nebulica Bold", SW / "Swiza-Regular.otf", 22, 10, PURP), ("Soporte que responde", NB / "Nebulica-Bold.otf", 80, 44, NAVY),
                      ("H2 · 32 · Nebulica SemiBold", SW / "Swiza-Regular.otf", 22, 10, PURP), ("Infraestructura sin sorpresas", NB / "Nebulica-SemiBold.otf", 64, 44, NAVY),
                      ("H3 · 24 · Nebulica SemiBold", SW / "Swiza-Regular.otf", 22, 10, PURP), ("Ciberseguridad", NB / "Nebulica-SemiBold.otf", 48, 44, NAVY),
                      ("Subtítulo · 20 · Swiza Light", SW / "Swiza-Regular.otf", 22, 10, PURP), ("Tu tecnología al ritmo de tu operación.", SW / "Swiza-Light.otf", 40, 44, NAVY),
                      ("Cuerpo · 16 · Swiza Regular", SW / "Swiza-Regular.otf", 22, 10, PURP), ("Mesa de ayuda, técnicos en sitio y en campo.", SW / "Swiza-Regular.otf", 32, 44, NAVY),
                      ("Botón · 14 · Swiza SemiBold", SW / "Swiza-Regular.otf", 22, 10, PURP), ("Agenda tu diagnóstico", SW / "Swiza-SemiBold.otf", 28, 0, NAVY)])
# El tagline del logotipo comparado con Swiza Light (evidencia de la atribución tipográfica)
logo = Image.open(MAT / "Avantika-logo-tagline-negro-azul@4x (1).png").convert("RGBA")
im = Image.new("RGB", (1300, 400), (255, 255, 255))
im.paste(logo, (28, 24), logo)
ImageDraw.Draw(im).text((432, 300), "Cybersecurity", font=ImageFont.truetype(str(SW / "Swiza-Light.otf"), 71), fill=NAVY)
im.save(REV / "img" / "tipo" / "tagline-vs-swiza.png", optimize=True)

# ---------- Procedencia ----------
(REV / "source" / "referencias.json").write_text(json.dumps(
    [{"archivo": a, "que": q, "original": o, "medida": m, "sha256_16": s, "publicado": p} for a, q, o, m, s, p in filas],
    ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("listo:", len(filas), "referencias")
