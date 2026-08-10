#!/usr/bin/env python3
"""Valida los .drawio del wiki: XML bien formado y sin aristas huérfanas."""
import glob
import os
import pathlib
import sys
import xml.etree.ElementTree as ET

D = str(pathlib.Path(__file__).resolve().parent.parent)
fallas = 0

for path in sorted(glob.glob(os.path.join(D, "*.drawio"))):
    nombre = os.path.basename(path)
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        print(f"✗ {nombre}: XML mal formado — {exc}")
        fallas += 1
        continue

    celdas = root.findall(".//mxCell")
    ids = {c.get("id") for c in celdas}
    vertices = [c for c in celdas if c.get("vertex") == "1"]
    aristas = [c for c in celdas if c.get("edge") == "1"]
    vids = {c.get("id") for c in vertices}

    problemas = []
    vistos = set()
    for c in celdas:
        cid = c.get("id")
        if cid in vistos:
            problemas.append(f"id duplicado: {cid}")
        vistos.add(cid)

    for a in aristas:
        for extremo in ("source", "target"):
            ref = a.get(extremo)
            if ref is None:
                problemas.append(f"arista {a.get('id')}: sin {extremo}")
            elif ref not in vids:
                problemas.append(f"arista {a.get('id')}: {extremo}='{ref}' no resuelve a un vértice")

    for v in vertices:
        if v.get("parent") not in ids:
            problemas.append(f"vértice {v.get('id')}: parent inexistente")

    estado = "✓" if not problemas else "✗"
    print(f"{estado} {nombre}: {len(vertices)} vértices, {len(aristas)} aristas")
    for p in problemas:
        print(f"    → {p}")
        fallas += 1

print()
print("Todo correcto." if not fallas else f"{fallas} problema(s).")
sys.exit(1 if fallas else 0)
