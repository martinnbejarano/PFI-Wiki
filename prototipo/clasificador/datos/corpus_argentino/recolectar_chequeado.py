"""Recolección reproducible de candidatos del corpus argentino de prueba (ticket #30).

Pasos (cada uno se puede repetir; `bajar` retoma donde quedó):

    python recolectar_chequeado.py urls        # sitemaps de notas -> cache_chequeado/urls.txt
    python recolectar_chequeado.py bajar       # notas -> cache_chequeado/html/*.html.gz
    python recolectar_chequeado.py crudos      # tuits de cada nota -> cache_chequeado/crudos.json
    python recolectar_chequeado.py verificar   # chequea candidatos.csv (columnas, duplicados, proporción)
    python recolectar_chequeado.py afirmaciones  # conjunto de entrenamiento -> afirmaciones_chequeado.csv

Respeta https://chequeado.com/robots.txt (grupo `User-agent: *`, regla más larga gana, con
comodines) y espera PAUSA segundos entre consultas. Se identifica con un agente propio; no
simula un navegador. Solo baja notas públicas; no consulta X/Twitter.

`crudos.json` NO es la planilla: lista cada tuit embebido o citado en una nota, con la
calificación de la nota y una etiqueta propuesta según wiki/datasets/guia-etiquetado-corpus-argentino.md.
Las filas de `candidatos.csv` salen de revisar esos crudos a mano: queda solo el tuit que es
el contenido calificado por la nota.

`afirmaciones` arma un conjunto de **entrenamiento** con los títulos de las demás notas (ver
`paso_afirmaciones`). Nunca toma una nota del corpus de prueba ni una afirmación parecida a uno
de sus tuits.
"""
import csv, glob, gzip, html, json, os, re, sys, time, unicodedata, urllib.parse, urllib.request

UA = "PFI-UADE-research/1.0 (tesis academica, recoleccion espaciada)"
PAUSA = 1.2
AQUI = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(AQUI, "cache_chequeado")  # fuera de git
SECCIONES = ("verificacionfb", "ultimas-noticias", "quien-lo-dijo", "mitos-y-enganos", "promesas-chequeadas")  # explicadores y análisis no califican tuits
MAPEO = {"verdadero": "verdadero", "verdadero pero": "verdadero", "falso": "falso", "enganoso": "falso"}
COLUMNAS = ["enlace_tuit", "texto", "calificacion_original_o_dato_oficial", "enlace_nota_o_fuente",
            "etiqueta_propuesta", "etiqueta_confirmada"]


def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def reglas_robots(txt):
    reglas, grupo = [], False
    for linea in txt.splitlines():
        linea = linea.split("#")[0].strip()
        if ":" not in linea:
            continue
        k, v = (x.strip() for x in linea.split(":", 1))
        if k.lower() == "user-agent":
            grupo = v == "*"
        elif grupo and k.lower() in ("allow", "disallow") and v:
            patron = re.escape(v).replace(r"\*", ".*").replace(r"\$", "$")
            reglas.append((len(v), k.lower() == "allow", re.compile(patron)))
    return reglas


def permitido(u, reglas):
    p = urllib.parse.urlsplit(u)
    ruta = p.path + ("?" + p.query if p.query else "")
    hits = [(n, a) for n, a, r in reglas if r.match(ruta)]
    return max(hits)[1] if hits else True


def limpiar(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"https?://\S+|pic\.twitter\.com/\S+|@\w+", " ", s)
    return re.sub(r"\s+", " ", re.sub(r"[^\w%]", " ", s)).strip()


TW = re.compile(r'https?://(?:www\.|mobile\.)?(?:x|twitter)\.com/([A-Za-z0-9_]+)/status(?:es)?/(\d+)')


def extraer(u, h):
    cab = h[h.find("o-single__header"):h.find("o-single__content-wrapper")]
    m = (re.search(r'class="c-tax__item c-tax__item--([a-z0-9-]+)">([^<]+)<', cab)
         or re.search(r'class="c-nota__featured-image-calificacion c-nota__featured-image-calificacion--(?!card)'
                      r'([a-z0-9-]+)\s*">\s*([^<]+)<', h))
    cal = limpiar(m.group(2)) if m else None
    t = re.search(r'<meta property="og:title" content="([^"]*)"', h)
    titulo = html.unescape(t.group(1)) if t else ""
    if not cal:  # notas viejas sin calificación marcada: Chequeado la pone en el título
        n = norm(titulo)
        cal = next((c + " (título)" for p, c in (("es falso", "Falso"), ("falso", "Falso"),
                    ("es enganoso", "Engañoso"), ("es verdadero", "Verdadero")) if n.startswith(p)), None)
    ini, fin = h.find("c-bullets"), h.find("c-meta-tags")
    cuerpo = h[max(ini, 0): fin if fin > 0 else len(h)]
    tuits = []
    for b in re.finditer(r'<blockquote[^>]*class="[^"]*twitter-tweet[^"]*"[^>]*>(.*?)</blockquote>', cuerpo, re.S):
        ids = TW.findall(b.group(0))
        lang = re.search(r'lang="([a-z-]+)"', b.group(0))
        texto = re.split(r"\n?\s*[—-]{1,2}\s*[^\n]*\(@\w+\)[^\n]*$", limpiar(b.group(1)))[0].strip()
        if ids:
            tuits.append({"tipo": "embebido", "lang": lang.group(1) if lang else None,
                          "usuario": ids[-1][0], "id": ids[-1][1], "texto": texto})
    for p in re.finditer(r"<p[^>]*>(.*?)</p>", cuerpo, re.S):
        for usuario, i in TW.findall(p.group(1)):
            for cita in re.findall(r"[“\"]([^”\"]{25,})[”\"]", limpiar(p.group(1))):
                tuits.append({"tipo": "cita", "lang": None, "usuario": usuario, "id": i, "texto": cita})
    clave = norm((cal or "").replace("(título)", ""))
    return {"url": u, "titulo": titulo, "calificacion": cal, "etiqueta_propuesta": MAPEO.get(clave),
            "tuits": tuits}


def paso_urls():
    os.makedirs(CACHE, exist_ok=True)
    reglas = reglas_robots(get("https://chequeado.com/robots.txt"))
    indice = get("https://chequeado.com/sitemap_index.xml")
    urls = []
    for sm in re.findall(r"<loc>([^<]*nota-sitemap\d*\.xml)</loc>", indice):
        time.sleep(PAUSA)
        urls += re.findall(r"<loc>([^<]+)</loc>", get(sm))
    urls = sorted({u for u in urls if urllib.parse.urlsplit(u).path.split("/")[1] in SECCIONES
                   and permitido(u, reglas)})
    open(os.path.join(CACHE, "urls.txt"), "w").write("\n".join(urls) + "\n")
    print(len(urls), "notas")


def archivo(u):
    return os.path.join(CACHE, "html", re.sub(r"\W+", "_", u)[-180:] + ".html.gz")


def paso_bajar():
    os.makedirs(os.path.join(CACHE, "html"), exist_ok=True)
    reglas = reglas_robots(get("https://chequeado.com/robots.txt"))
    for u in open(os.path.join(CACHE, "urls.txt")).read().split():
        if os.path.exists(archivo(u)) or not permitido(u, reglas):
            continue
        try:
            h = get(u)
            with gzip.open(archivo(u), "wt") as f:
                f.write(h)
        except Exception as e:  # una nota caída no frena la corrida
            print("error", u, e, file=sys.stderr)
        time.sleep(PAUSA)


def paso_crudos():
    salida = []
    for f in sorted(glob.glob(os.path.join(CACHE, "html", "*.html.gz"))):
        h = gzip.open(f, "rt").read()
        c = re.search(r'<link rel="canonical" href="([^"]+)"', h)
        r = extraer(c.group(1) if c else f, h)
        if r["tuits"]:
            salida.append(r)
    json.dump(salida, open(os.path.join(CACHE, "crudos.json"), "w"), ensure_ascii=False, indent=1)
    print(len(salida), "notas con tuits")


def verificar(ruta=os.path.join(AQUI, "candidatos.csv")):
    filas = list(csv.DictReader(open(ruta, encoding="utf-8")))
    assert filas and list(filas[0]) == COLUMNAS, "columnas distintas de las acordadas"
    ids = [TW.search(f["enlace_tuit"]).group(2) for f in filas]
    textos = [norm(f["texto"]) for f in filas]
    assert len(set(ids)) == len(ids), "tuit repetido"
    assert len(set(textos)) == len(textos), "texto normalizado repetido"
    assert all(f["etiqueta_propuesta"] in ("verdadero", "falso") for f in filas)
    assert all(f["enlace_nota_o_fuente"].startswith("https://") for f in filas)
    assert all(f["etiqueta_confirmada"] in ("", "verdadero", "falso", "descartar") for f in filas)
    columna = "etiqueta_propuesta"
    if any(f["etiqueta_confirmada"] for f in filas):  # con confirmaciones, cuenta solo el corpus final
        assert all(f["etiqueta_confirmada"] for f in filas), "hay filas sin confirmar"
        filas, columna = [f for f in filas if f["etiqueta_confirmada"] != "descartar"], "etiqueta_confirmada"
    v = sum(f[columna] == "verdadero" for f in filas)
    print(f"{len(filas)} filas ({columna}) · verdadero {v} ({v / len(filas):.0%}) · falso {len(filas) - v}")
    assert 0.4 <= v / len(filas) <= 0.6, "proporción fuera de 40/60"
    return len(filas), v


# «Quién: “afirmación”» (discurso público) y «Es falso que afirmación» (desinformación viral).
DICHO = re.compile(r'^(?P<quien>[^:“"«]{2,120}):\s*[“"«](?P<texto>[^”"»]+)[”"»]\s*\.?\s*$')
VIRAL = re.compile(r'^\s*es\s+(?:falso|verdadero|engañoso)\s+que\s+(?P<texto>[^“"«]+)$', re.I)
PARECIDO_MAXIMO = 0.6  # fracción de las palabras de la afirmación presentes en un tuit de prueba


def afirmacion(titulo):
    """La afirmación calificada, sin las palabras de la nota que anticipan la etiqueta."""
    m = DICHO.match(titulo.strip())
    # «Es falso que X dijo: “…”» califica la atribución, no el contenido de la cita.
    if m and not re.match(r"(es (falso|verdadero|enganoso)|no)\b", norm(m["quien"])):
        return m["texto"].strip()
    m = VIRAL.match(titulo.strip())
    # El subjuntivo («haya») y el «pero» de la nota delatan la etiqueta.
    if m and not re.search(r"\b(haya|hayan|pero)\b", norm(m["texto"])):
        return m["texto"].strip()
    return None


def paso_afirmaciones(salida=os.path.join(AQUI, "afirmaciones_chequeado.csv")):
    from sklearn.model_selection import train_test_split

    prueba = list(csv.DictReader(open(os.path.join(AQUI, "candidatos.csv"), encoding="utf-8")))
    notas_prueba = {f["enlace_nota_o_fuente"] for f in prueba}
    palabras = lambda s: {w for w in norm(s).split() if len(w) > 3}
    tuits = [palabras(f["texto"]) for f in prueba]
    grupos, descartes = {}, {"nota de prueba": 0, "parecida a un tuit de prueba": 0}
    for f in sorted(glob.glob(os.path.join(CACHE, "html", "*.html.gz"))):
        h = gzip.open(f, "rt").read()
        c = re.search(r'<link rel="canonical" href="([^"]+)"', h)
        r = extraer(c.group(1) if c else f, h)
        texto = afirmacion(r["titulo"])
        if not r["etiqueta_propuesta"] or not texto or len(texto.split()) < 5:
            continue
        if r["url"] in notas_prueba:
            descartes["nota de prueba"] += 1
            continue
        a = palabras(texto)
        if any(len(a & t) >= PARECIDO_MAXIMO * len(a) for t in tuits):
            descartes["parecida a un tuit de prueba"] += 1
            continue
        grupos.setdefault(norm(texto), []).append({
            "id": urllib.parse.urlsplit(r["url"]).path.strip("/").split("/")[-1], "texto": texto,
            "etiqueta": r["etiqueta_propuesta"], "calificacion": r["calificacion"], "enlace_nota": r["url"]})
    # Un texto repetido queda una vez; si dos notas lo califican distinto, se descarta.
    filas = sorted((g[0] for g in grupos.values() if len({x["etiqueta"] for x in g}) == 1), key=lambda x: x["id"])
    entrenamiento, _ = train_test_split(range(len(filas)), test_size=0.15, random_state=42,
                                        stratify=[x["etiqueta"] for x in filas])
    entrenamiento = set(entrenamiento)
    for i, x in enumerate(filas):
        x["particion"] = "entrenamiento" if i in entrenamiento else "validacion"
    with open(salida, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, ["id", "texto", "etiqueta", "particion", "calificacion", "enlace_nota"], lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    print(len(filas), "afirmaciones", {e: sum(x["etiqueta"] == e for x in filas) for e in ("verdadero", "falso")},
          "descartadas:", descartes)


if __name__ == "__main__":
    {"urls": paso_urls, "bajar": paso_bajar, "crudos": paso_crudos, "verificar": verificar,
     "afirmaciones": paso_afirmaciones}[sys.argv[1]]()
