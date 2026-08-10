#!/usr/bin/env python3
"""Exporta los .drawio a PNG recortado en documento/chapters/figures/."""
import pathlib

from PIL import Image, ImageChops

import render as R

FIGS = pathlib.Path(__file__).resolve().parents[3] / "documento" / "chapters" / "figures"
MARGEN = 24


def recortar(path: pathlib.Path) -> tuple:
    im = Image.open(path).convert("RGB")
    fondo = Image.new("RGB", im.size, (255, 255, 255))
    caja = ImageChops.difference(im, fondo).getbbox()
    if not caja:
        return im.size
    x0, y0, x1, y1 = caja
    x0, y0 = max(0, x0 - MARGEN), max(0, y0 - MARGEN)
    x1, y1 = min(im.width, x1 + MARGEN), min(im.height, y1 + MARGEN)
    im.crop((x0, y0, x1, y1)).save(path, optimize=True)
    return (x1 - x0, y1 - y0)


if __name__ == "__main__":
    FIGS.mkdir(parents=True, exist_ok=True)
    R.OUT.mkdir(parents=True, exist_ok=True)
    for src in sorted(R.DIAG.glob("*.drawio")):
        tmp = R.render(src, escala="3")
        destino = FIGS / f"{src.stem}.png"
        destino.write_bytes(tmp.read_bytes())
        w, h = recortar(destino)
        kb = destino.stat().st_size // 1024
        print(f"✓ {destino.name}  {w}×{h} px  {kb} KB")
