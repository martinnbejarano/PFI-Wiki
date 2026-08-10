#!/usr/bin/env python3
"""Renderiza los .drawio del wiki a PNG con el visor de draw.io en Chrome headless.

El XML viaja en el fragmento de la URL (después del #), que no se envía al servidor.
"""
import pathlib
import tempfile
import re
import subprocess
import sys
import urllib.parse

DIAG = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(tempfile.gettempdir()) / "pfi-diagramas-render"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE = "https://viewer.diagrams.net/?highlight=0000ff&nav=0&toolbar=0&layers=0&lightbox=0#R"

# Ancho de ventana objetivo; el alto sale de la relación de aspecto de la página.
ANCHO = 1500
MAX_ALTO = 2400


def page_size(xml: str):
    w = re.search(r'pageWidth="(\d+)"', xml)
    h = re.search(r'pageHeight="(\d+)"', xml)
    return (int(w.group(1)) if w else 1169, int(h.group(1)) if h else 826)


def render(path: pathlib.Path, escala: str = "2") -> pathlib.Path:
    xml = path.read_text()
    pw, ph = page_size(xml)
    alto = min(MAX_ALTO, max(700, round(ANCHO * ph / pw)))
    url = BASE + urllib.parse.quote(xml, safe="")
    destino = OUT / f"{path.stem}.png"
    subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         f"--force-device-scale-factor={escala}",
         f"--window-size={ANCHO},{alto}", "--virtual-time-budget=20000",
         f"--screenshot={destino}", url],
        capture_output=True, timeout=180)
    return destino


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    objetivos = sys.argv[1:] or [p.stem for p in sorted(DIAG.glob("*.drawio"))]
    for stem in objetivos:
        src = DIAG / f"{stem}.drawio"
        if not src.exists():
            print(f"✗ no existe: {src}")
            continue
        d = render(src)
        kb = d.stat().st_size // 1024 if d.exists() else 0
        print(f"{'✓' if kb else '✗'} {d.name} ({kb} KB)")
