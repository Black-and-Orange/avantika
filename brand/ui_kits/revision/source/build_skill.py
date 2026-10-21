#!/usr/bin/env python3
"""Arma la skill distribuible «avantika-design» a partir de brand/.

Uso, desde la raíz del repo:  python3 brand/ui_kits/revision/source/build_skill.py
Sale en dist/avantika-design/ (fuera del repo) y se empaqueta con el script package_skill de skill-creator.
No incluye las fuentes (licencia), los documentos originales del cliente, la página de revisión ni las piezas de LinkedIn.
"""
import importlib.util
import pathlib
import re
import shutil

R = pathlib.Path(__file__).resolve().parents[4]
B = R / "brand"
OUT = R / "dist" / "avantika-design"

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)


def copia(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


# Tokens, CSS y runtime
for f in ["styles.css", "ds-runtime.js"]:
    copia(B / f, OUT / f)
for f in (B / "tokens").glob("*.css"):
    copia(f, OUT / "tokens" / f.name)

# Assets: logos, íconos, elementos, fotos, fondos, isotipo ilustrado y mockups
for f in (B / "assets").glob("*.png"):
    copia(f, OUT / "assets" / f.name)
for sub in ("icons", "elementos"):
    for f in (B / "assets" / sub).iterdir():
        if not f.name.startswith("."):
            copia(f, OUT / "assets" / sub / f.name)
for patron in ("imagery-foto-*.jpg", "imagery-layout-*.jpg", "imagery-isotipo-*.jpg", "imagery-mockup-*.jpg", "imagery-post-linkedin-01.jpg"):
    for f in (B / "assets").glob(patron):
        copia(f, OUT / "assets" / f.name)
leeme = (B / "assets" / "fonts" / "LEEME.md").read_text(encoding="utf-8").replace("`../../ui_kits/revision/img/tipo/`", "`../tipo/`")
leeme = leeme.replace("# Fuentes de Avantika — no se distribuyen en este repo", "# Fuentes de Avantika — no vienen en esta skill")
leeme = leeme.replace("""así que **no están
en el repo público**: viven solo en la carpeta local de trabajo (`brand/assets/fonts/Swiza/` y
`brand/assets/fonts/Nebulica/`, excluidas en `.gitignore`).""", """así que **no vienen
en esta skill**. Pídelas a Black & Orange e instálalas en tu equipo.""")
(OUT / "assets" / "fonts").mkdir(parents=True, exist_ok=True)
(OUT / "assets" / "fonts" / "LEEME.md").write_text(leeme, encoding="utf-8")
for f in (B / "ui_kits" / "revision" / "img" / "tipo").glob("*.png"):
    copia(f, OUT / "assets" / "tipo" / f.name)

# Componentes, tarjetas y UI kit (las rutas a los logos recortados de la revisión pasan a assets/)
for f in (B / "components").rglob("*"):
    if f.is_file() and not f.name.startswith("."):
        copia(f, OUT / f.relative_to(B))
for f in (B / "guidelines").glob("*.html"):
    t = f.read_text(encoding="utf-8").replace("../ui_kits/revision/img/logos/", "../assets/").replace("../ui_kits/revision/img/tipo/", "../assets/tipo/")
    (OUT / "guidelines").mkdir(exist_ok=True)
    (OUT / "guidelines" / f.name).write_text(t, encoding="utf-8")
for f in (B / "ui_kits" / "website").iterdir():
    if f.is_file():
        t = f.read_text(encoding="utf-8").replace("../revision/img/logos/", "../../assets/")
        t = t.replace("`../revision/` es la página de revisión del sistema completo (la que se publica en GitHub Pages).",
                      "La página de revisión del sistema completo está en https://black-and-orange.github.io/avantika/")
        (OUT / "ui_kits" / "website").mkdir(parents=True, exist_ok=True)
        (OUT / "ui_kits" / "website" / f.name).write_text(t, encoding="utf-8")

# Referencias de lectura
REF = OUT / "references"
REF.mkdir()
copia(B / "readme.md", REF / "sistema.md")
copia(B / "reglas-consolidadas-2026-10-13.md", REF / "reglas.md")
copia(B / "arquetipos.json", REF / "arquetipos.json")
copia(B / "matrix-blocks.json", REF / "prompts-imagen.json")
copia(R / "brand-profile.md", REF / "perfil.md")
copia(R / "campaigns" / "linkedin-set-6-posts" / "guion.md", REF / "textos-linkedin.md")
copia(B / "ui_kits" / "revision" / "source" / "contrast-pairs.json", REF / "contraste.json")

# Pendientes, desde la misma lista que usa la página de revisión
spec = importlib.util.spec_from_file_location("build", B / "ui_kits" / "revision" / "source" / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
orden = {"Alta": 0, "Media": 1, "Baja": 2}
lineas = ["# Pendientes del sistema · Avantika", "",
          "Lo que falta pedir al cliente o definir. Antes de presentar algo como regla, revisa si su tema está aquí: si lo está, es propuesta.", ""]
for prioridad in ("Alta", "Media", "Baja"):
    lineas += ["## Prioridad %s" % prioridad.lower(), ""]
    for t, q, a, p, o in sorted(build.HUECOS, key=lambda h: orden[h[3]]):
        if p == prioridad:
            lineas += ["- **%s** (%s). %s Acción: %s" % (t, o, q, a)]
    lineas.append("")
(REF / "pendientes.md").write_text("\n".join(lineas), encoding="utf-8")

# Ajustes de rutas en las referencias: en la skill todo cuelga de la raíz
for f in REF.glob("*.md"):
    t = f.read_text(encoding="utf-8")
    t = t.replace("`../references/`", "las referencias del repo (no incluidas)").replace("ui_kits/revision/", "la página de revisión (https://black-and-orange.github.io/avantika/)")
    f.write_text(t, encoding="utf-8")

shutil.copyfile(pathlib.Path(__file__).with_name("skill_SKILL.md"), OUT / "SKILL.md")

# Validación mínima del frontmatter (mismas reglas que quick_validate de skill-creator) y empaquetado .skill
md = (OUT / "SKILL.md").read_text(encoding="utf-8")
fm = re.match(r"^---\n(.*?)\n---", md, re.DOTALL).group(1)
campos = dict(re.findall(r"^([a-z-]+):\s*(.*)$", fm, re.M))
assert set(campos) <= {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}, campos.keys()
assert re.match(r"^[a-z0-9-]+$", campos["name"]) and len(campos["name"]) <= 64
assert len(campos["description"]) <= 1024 and "<" not in campos["description"] and ">" not in campos["description"], len(campos["description"])
assert sum(1 for _ in OUT.rglob("SKILL.md")) == 1
import zipfile
paquete = OUT.parent / "avantika-design.skill"
with zipfile.ZipFile(paquete, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.rglob("*")):
        if f.is_file() and f.name != ".DS_Store":
            z.write(f, f.relative_to(OUT.parent))
print("descripción:", len(campos["description"]), "caracteres · paquete:", paquete, round(paquete.stat().st_size / 1e6, 1), "MB")

total = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
print("skill en", OUT, "·", sum(1 for f in OUT.rglob("*") if f.is_file()), "archivos ·", round(total / 1e6, 1), "MB")
