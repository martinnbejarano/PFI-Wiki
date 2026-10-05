"""Recolección reproducible de candidatos del corpus argentino de prueba (ticket #30).

Pasos (cada uno se puede repetir; `bajar` retoma donde quedó):

    python recolectar_chequeado.py urls        # sitemaps de notas -> cache_chequeado/urls.txt
    python recolectar_chequeado.py bajar       # notas -> cache_chequeado/html/*.html.gz
    python recolectar_chequeado.py crudos      # tuits de cada nota -> cache_chequeado/crudos.json
    python recolectar_chequeado.py verificar   # chequea candidatos.csv (columnas, duplicados, proporción)

Respeta https://chequeado.com/robots.txt (grupo `User-agent: *`, regla más larga gana, con
comodines) y espera PAUSA segundos entre consultas. Se identifica con un agente propio; no
simula un navegador. Solo baja notas públicas; no consulta X/Twitter.

`crudos.json` NO es la planilla: lista cada tuit embebido o citado en una nota, con la
calificación de la nota y una etiqueta propuesta según wiki/datasets/guia-etiquetado-corpus-argentino.md.
Las filas de `candidatos.csv` salen de revisar esos crudos a mano: queda solo el tuit que es
el contenido calificado por la nota.
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
    v = sum(f["etiqueta_propuesta"] == "verdadero" for f in filas)
    print(f"{len(filas)} filas · verdadero {v} ({v / len(filas):.0%}) · falso {len(filas) - v}")
    return len(filas), v


if __name__ == "__main__":
    {"urls": paso_urls, "bajar": paso_bajar, "crudos": paso_crudos, "verificar": verificar}[sys.argv[1]]()
