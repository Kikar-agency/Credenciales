"""
Genera las credenciales en PDF a partir de config.yml y personas.yml.

Uso:
    python generar.py              -> genera todas
    python generar.py lucas        -> solo las que tengan "lucas" en el nombre
"""
import re
import sys
import unicodedata
from pathlib import Path

import yaml
from PIL import Image, ImageOps
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent
SALIDA = RAIZ / "pdf"
PLANTILLA = RAIZ / "plantilla"


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


CACHE = RAIZ / ".cache"


def preparar_firma(ruta):
    """Si la firma es una foto/escaneo (tinta oscura sobre papel claro),
    la convierte a trazo blanco sobre fondo transparente y la recorta."""
    im = Image.open(ruta)
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA") and im.getextrema()[-1][0] < 255:
        return ruta  # ya tiene transparencia: se usa tal cual
    gris = ImageOps.grayscale(im.convert("RGB"))
    tinta = ImageOps.invert(gris)
    tinta = ImageOps.autocontrast(tinta, cutoff=(60, 0.5))
    # limpia el gris del papel y refuerza el trazo
    tinta = tinta.point(lambda v: 0 if v < 70 else min(255, int((v - 70) * 255 / 120)))
    caja = tinta.getbbox()
    if caja:
        tinta = tinta.crop(caja)
    salida = Image.new("RGBA", tinta.size, (255, 255, 255, 0))
    salida.putalpha(tinta)
    CACHE.mkdir(exist_ok=True)
    destino = CACHE / (ruta.stem + ".png")
    salida.save(destino)
    return destino


def cargar():
    cfg = yaml.safe_load((RAIZ / "config.yml").read_text(encoding="utf-8"))
    personas = yaml.safe_load((RAIZ / "personas.yml").read_text(encoding="utf-8")) or []
    errores = []
    for i, p in enumerate(personas, 1):
        for campo in ("nombre", "cargo", "foto"):
            if not p.get(campo):
                errores.append(f"Persona #{i}: falta '{campo}'")
        p["nombre"] = str(p.get("nombre", "")).strip().upper()
        p["cargo"] = str(p.get("cargo", "")).strip().upper()
        p["fechas"] = p.get("fechas", True) not in (False, "no", "NO", "No")
        foto = RAIZ / "fotos" / str(p.get("foto", ""))
        if p.get("foto") and not foto.is_file():
            errores.append(f"{p['nombre']}: no encuentro la foto 'fotos/{p['foto']}'")
        p["foto_url"] = foto.as_uri() if foto.is_file() else ""
        p["firma_url"] = ""
        if p.get("firma"):
            firma = RAIZ / "firmas" / str(p["firma"])
            if firma.is_file():
                p["firma_url"] = preparar_firma(firma).as_uri()
            else:
                errores.append(f"{p['nombre']}: no encuentro la firma 'firmas/{p['firma']}'")
    if errores:
        print("\nHAY ERRORES EN LOS DATOS:\n  - " + "\n  - ".join(errores))
        sys.exit(1)
    return cfg, personas


def main():
    cfg, personas = cargar()
    filtro = " ".join(sys.argv[1:]).strip().lower()
    elegidas = [p for p in personas if not filtro or filtro in slug(p["nombre"]).replace("-", " ") or filtro in p["nombre"].lower()]
    if not elegidas:
        print(f"Nadie coincide con '{filtro}'")
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(PLANTILLA), autoescape=True)
    tpl = env.get_template("credencial.html")
    firmas_fijas = {
        "presidente": (RAIZ / "assets/firmas-fijas/presidente.png").as_uri(),
        "vicepresidente": (RAIZ / "assets/firmas-fijas/vicepresidente.png").as_uri(),
    }
    tmp = PLANTILLA / "_temp.html"
    (SALIDA / "credenciales").mkdir(parents=True, exist_ok=True)

    def pdf(page, paginas, destino):
        tmp.write_text(tpl.render(cfg=cfg, paginas=paginas, firmas_fijas=firmas_fijas), encoding="utf-8")
        page.goto(tmp.as_uri())
        page.wait_for_selector("body[data-listo='1']", state="attached", timeout=30000)
        page.pdf(path=str(destino), prefer_css_page_size=True, print_background=True)
        print("  ->", destino.relative_to(RAIZ))

    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        page = nav.new_page()
        pdf(page, [{"tipo": "frente"}], SALIDA / "frente.pdf")
        for p in elegidas:
            pdf(page, [{"tipo": "frente"}, {"tipo": "dorso", "persona": p}],
                SALIDA / "credenciales" / f"{slug(p['nombre'])}.pdf")
        if not filtro:
            todas = []
            for p in personas:
                todas += [{"tipo": "frente"}, {"tipo": "dorso", "persona": p}]
            pdf(page, todas, SALIDA / "TODAS-las-credenciales.pdf")
        nav.close()
    tmp.unlink(missing_ok=True)
    print(f"\nListo: {len(elegidas)} credencial(es).")


if __name__ == "__main__":
    main()
