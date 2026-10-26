"""Ingesta del índice de fuentes oficiales del Módulo 3 (tickets #109 y #110, PRD #107).

Recorre cada fuente del catálogo `FUENTES`, baja lo publicado dentro de la
ventana que todavía no está indexado, lo corta en fragmentos y los agrega al
índice (`proveedor/indice.py`). Al final purga lo vencido, anota la última
corrida de cada fuente y registra su resumen:

    ingesta | INDEC | descubiertos=12 | bajados=10 | omitidos=0 | fallados=2

`descubiertos` son los documentos que listó la fuente, `omitidos` los que
`robots.txt` excluye y `fallados` los que no se pudieron bajar o leer. Un
documento roto se anota y la corrida sigue; una fuente rota no frena a las
demás.

**Rastreo (RNF-17).** Se aplican las reglas del grupo `*` de `robots.txt`, con
los comodines `*` y `$` y la regla más larga como ganadora (RFC 9309), a todo
pedido y no solo a los documentos, y entre dos pedidos al mismo sitio se espera
la demora declarada o el mínimo configurado, la mayor de las dos. Las
redirecciones se siguen a mano para que cada salto pase por lo mismo; a otro
sitio no se siguen. El User-Agent es de navegador: algunos sitios del Estado
rechazan los genéricos.

**Sumar una fuente** es sumar una `FuenteOficial` a `FUENTES` con su
descubridor: una función que recibe el `Rastreador` y la fecha desde la que
vale la ventana y devuelve los `Candidato`, cada uno con su URL, su título y su
fecha de publicación. El resto (ventana, tope, robots, demora, extracción,
fragmentos, purga y registro) es común.

Se ejecuta desde la línea de comandos sobre la base local configurada:

    python -m app.ingesta

o con `POST /ingesta` (#111), que la lanza así en un subproceso. **Una corrida
a la vez:** la corrida toma un candado de archivo (`flock`) junto a la base y,
si ya está tomado, termina sin rastrear. El candado lo suelta el sistema
operativo cuando el proceso termina, aunque muera o se reinicie el servidor.
"""

from __future__ import annotations

import fcntl
import html
import io
import logging
import re
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from typing import IO
from urllib.parse import unquote, urljoin, urlsplit
from urllib.robotparser import RobotFileParser

import httpx2 as httpx
from pypdf import PdfReader

from .configuracion import Configuracion, obtener_configuracion
from .proveedor.indice import Fragmento, IndiceDeFuentes
from .proveedor.memoria import ClienteEmbebedor

registro = logging.getLogger("app.ingesta")

AGENTE = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
)

PALABRAS_POR_FRAGMENTO = 45
"""Para quedar debajo de los 128 *tokens* del modelo de *embeddings* (PRD #107).

Medido el 2026-10-25 con el tokenizador de
`paraphrase-multilingual-MiniLM-L12-v2` (el de `/embeber`) sobre los informes
del INDEC de IPC, EMAE y mercado de trabajo, con `extraer` y `fragmentar`:
100 palabras dan 174 *tokens* de mediana (206 de 208 fragmentos pasan 128); 60,
104 de mediana y 141 en el p95; 45, 80 de mediana y 112 en el p95. Los pocos que
pasan con 45 son ejes de gráficos (`2T1T4T3T...`), que el modelo trunca.
"""

SALTOS_MAXIMOS = 10


class Excluida(Exception):
    """La URL está excluida por `robots.txt` para el grupo `*`."""


class Limitada(Exception):
    """El sitio respondió 429: no se le pide nada más en esta corrida."""


@dataclass(frozen=True)
class Candidato:
    """Un documento que lista una fuente. Sin título, se usa el del documento."""

    url: str
    titulo: str
    fecha: date


class Rastreador:
    """Pedidos a un sitio respetando su `robots.txt` y su demora de rastreo."""

    def __init__(
        self,
        cliente: httpx.Client,
        dominio: str,
        demora_minima_s: float,
        reloj: Callable[[], datetime],
        espera: Callable[[float], None],
    ) -> None:
        self.cliente, self.dominio, self.reloj, self.espera = cliente, dominio, reloj, espera
        self._ultimo: datetime | None = None
        self.demora_s = demora_minima_s
        self.robots = RobotFileParser()
        self.robots.allow_all = True  # mientras se baja el propio robots.txt
        respuesta = self._seguir(f"{dominio}/robots.txt")
        self.robots.allow_all = False
        # Lo mismo que hace `RobotFileParser.read()`.
        if respuesta.status_code in (401, 403):
            self.robots.disallow_all = True
        elif respuesta.status_code >= 400:
            self.robots.allow_all = True
        else:
            self.robots.parse(respuesta.text.splitlines())
        self.demora_s = max(float(self.robots.crawl_delay("*") or 0), demora_minima_s)

    def get(self, url: str) -> httpx.Response:
        respuesta = self._seguir(url)
        respuesta.raise_for_status()
        return respuesta

    def _seguir(self, url: str) -> httpx.Response:
        """El pedido y sus redirecciones, cada salto con robots y demora."""
        for _ in range(SALTOS_MAXIMOS + 1):
            if not self.permitida(url):
                raise Excluida(url)
            respuesta = self._pedir(url)
            if not respuesta.is_redirect:
                return respuesta
            url = urljoin(url, respuesta.headers["Location"])
            if not url.startswith(f"{self.dominio}/"):
                raise httpx.HTTPError(f"redirige a otro sitio: {url}")
        raise httpx.TooManyRedirects(f"más de {SALTOS_MAXIMOS} redirecciones: {url}")

    def permitida(self, url: str) -> bool:
        """Las reglas del grupo `*` con `*` y `$`: gana la que coincide más
        largo y, en empate, Allow. `robotparser` las parsea pero no entiende
        los comodines (y las guarda con `quote`)."""
        if self.robots.disallow_all:
            return False
        entrada = self.robots.default_entry
        if self.robots.allow_all or entrada is None:
            return True
        partes = urlsplit(url)
        ruta = (partes.path or "/") + (f"?{partes.query}" if partes.query else "")
        ganadora = (-1, True)
        for regla in entrada.rulelines:
            patron = unquote(regla.path)
            expresion = re.escape(patron.removesuffix("$")).replace(r"\*", ".*")
            if re.match(expresion + (r"\Z" if patron.endswith("$") else ""), ruta):
                ganadora = max(ganadora, (len(patron), regla.allowance))
        return ganadora[1]

    def _pedir(self, url: str) -> httpx.Response:
        if self._ultimo is not None:
            faltan = self.demora_s - (self.reloj() - self._ultimo).total_seconds()
            if faltan > 0:
                self.espera(faltan)
        try:
            respuesta = self.cliente.get(url)
        finally:
            self._ultimo = self.reloj()
        if respuesta.status_code == 429:
            raise Limitada(url)
        return respuesta


@dataclass(frozen=True)
class FuenteOficial:
    nombre: str
    dominio: str
    descubrir: Callable[[Rastreador, date], Iterable[Candidato]]


# -- Descubridores ----------------------------------------------------------

INDEC = "https://www.indec.gob.ar"

_TEMA = re.compile(r"/indec/web/Nivel4-Tema-(\d+)-(\d+)-(\d+)$")
_INFORME_TITULO = re.compile(r'card-titulo3[^>]*>\s*(\d\d)/(\d\d)/(\d\d)\.\s*([^<]+?)\s*<')
_INFORME_PDF = re.compile(r'href="(/uploads/informesdeprensa/[^"]+\.pdf)"')


def _locs(sitemap: str) -> list[str]:
    return [html.unescape(loc) for loc in re.findall(r"<loc>\s*(.*?)\s*</loc>", sitemap)]


def descubrir_indec(rastreador: Rastreador, desde: date) -> Iterable[Candidato]:
    """Los informes técnicos vigentes de cada tema del INDEC.

    El `sitemap.xml` del INDEC (al 2026-10-25) es un `urlset` fijo de páginas
    de tema, sin `lastmod` salvo la portada, así que la ventana no sale de ahí.
    Cada página `/indec/web/Nivel4-Tema-A-B-C` es una cáscara que carga la
    vista `/Nivel4/Tema/A/B/C`, y esa vista lista los informes técnicos, cada
    uno con su fecha y su título (`13/10/26. Índice de precios al consumidor`)
    y el enlace al PDF.
    """
    for loc in _locs(rastreador.get(f"{INDEC}/sitemap.xml").text):
        tema = _TEMA.search(loc)
        if tema is None:
            continue
        try:
            vista = rastreador.get(f"{INDEC}/Nivel4/Tema/{'/'.join(tema.groups())}").text
        except (Excluida, httpx.HTTPError) as error:
            registro.warning("ingesta | INDEC | tema %s | %s", loc, error)
            continue
        for item in vista.split('class="item-n3"')[1:]:
            titulo, pdf = _INFORME_TITULO.search(item), _INFORME_PDF.search(item)
            if titulo and pdf:
                dia, mes, anio, nombre = titulo.groups()
                yield Candidato(
                    urljoin(INDEC, pdf.group(1)),
                    html.unescape(nombre),
                    date(2000 + int(anio), int(mes), int(dia)),
                )


BCRA = "https://www.bcra.gob.ar"
ARGENTINA = "https://www.argentina.gob.ar"
BOLETIN = "https://www.boletinoficial.gob.ar"

_URL = re.compile(r"<url>\s*<loc>\s*([^<]*?)\s*</loc>\s*<lastmod>\s*(\d{4})-(\d\d)-(\d\d)")
_AVISO = re.compile(
    r'href="(/detalleAviso/primera/\d+/(\d{4})(\d\d)(\d\d))"[^>]*>\s*<div class="linea-aviso">'
    r'\s*<p class="item">\s*(.*?)\s*</p>\s*(?:<p class="item-detalle">\s*<small>\s*(.*?)\s*</small>)?',
    re.S,
)


@lru_cache(maxsize=1)
def _sitemap(rastreador: Rastreador, url: str) -> tuple[tuple[str, date], ...]:
    """Las URL con `lastmod` de un sitemap y, si es un índice, las de sus hijos.

    Un hijo caído se anota y se sigue. Las fechas del índice no se usan: el del
    BCRA (al 2026-10-25) fecha `post-sitemap.xml` en julio y trae notas de
    octubre. La última lectura queda en memoria para que Salud y Educación, que
    comparten el sitemap de argentina.gob.ar y el rastreador, lo bajen una vez.
    """
    texto = rastreador.get(url).text
    textos = [texto]
    if "<sitemapindex" in texto:
        textos = []
        for hijo in _locs(texto):
            try:
                textos.append(rastreador.get(hijo).text)
            except (Excluida, httpx.HTTPError) as error:
                registro.warning("ingesta | sitemap %s | %s", hijo, error)
    return tuple(
        (html.unescape(loc), date(int(a), int(m), int(d)))
        for t in textos for loc, a, m, d in _URL.findall(t)
    )


def descubrir_bcra(rastreador: Rastreador, desde: date) -> Iterable[Candidato]:
    """Las páginas del sitemap del BCRA, un índice de Rank Math con un hijo por
    tipo de contenido (notas, publicaciones, sumarios...), menos las traducciones
    al inglés de `/en/`. El título sale de la página."""
    for url, fecha in _sitemap(rastreador, f"{BCRA}/sitemap_index.xml"):
        if "/en/" not in url:
            yield Candidato(url, "", fecha)


def _ministerio(ruta: str) -> Callable[[Rastreador, date], Iterable[Candidato]]:
    """Las páginas bajo `ruta` del sitemap de argentina.gob.ar, un índice de
    cuatro páginas (`sitemap.xml?page=N`) de unas 50 000 URL cada una. Las
    noticias de cada ministerio viven en `/noticias/`, sin ruta propia, y no
    entran."""

    def descubrir(rastreador: Rastreador, desde: date) -> Iterable[Candidato]:
        for url, fecha in _sitemap(rastreador, f"{ARGENTINA}/sitemap.xml"):
            if url == ARGENTINA + ruta or url.startswith(f"{ARGENTINA}{ruta}/"):
                yield Candidato(url, "", fecha)

    return descubrir


def descubrir_boletin(rastreador: Rastreador, desde: date) -> Iterable[Candidato]:
    """Los avisos del listado de la primera sección de cada día de la ventana.

    El Boletín Oficial no publica sitemap. `/seccion/primera/AAAAMMDD` lista los
    avisos de ese día en una sola página (el resto que carga al desplazarse
    viene vacío), cada uno con el organismo y la norma; un día sin edición
    redirige a la portada. La segunda sección no se pide nunca.
    """
    dia, hoy = desde, rastreador.reloj().date()
    while dia <= hoy:
        try:
            listado = rastreador.get(f"{BOLETIN}/seccion/primera/{dia:%Y%m%d}").text
        except (Excluida, httpx.HTTPError) as error:
            registro.warning("ingesta | Boletín Oficial | día %s | %s", dia, error)
        else:
            for ruta, a, m, d, organismo, norma in _AVISO.findall(listado):
                titulo = " - ".join(t for t in (organismo, norma) if t)
                yield Candidato(urljoin(BOLETIN, ruta), html.unescape(titulo),
                                date(int(a), int(m), int(d)))
        dia += timedelta(days=1)


FUENTES: list[FuenteOficial] = [
    FuenteOficial("INDEC", INDEC, descubrir_indec),
    FuenteOficial("BCRA", BCRA, descubrir_bcra),
    # Seguidas, para que la segunda use el sitemap que bajó la primera.
    FuenteOficial("Ministerio de Salud", ARGENTINA, _ministerio("/salud")),
    FuenteOficial("Ministerio de Educación", ARGENTINA, _ministerio("/educacion")),
    FuenteOficial("Boletín Oficial", BOLETIN, descubrir_boletin),
]


# -- Texto y fragmentos -----------------------------------------------------

_BLOQUES = {"p", "div", "li", "br", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6",
            "section", "article", "blockquote", "pre", "table", "ul", "ol"}
_IGNORADOS = {"script", "style", "noscript", "nav", "header", "footer", "head"}


class _TextoDeHtml(HTMLParser):
    """Párrafos y título de un HTML, sin scripts ni navegación."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parrafos: list[str] = [""]
        self.titulo = ""
        self._ignorando = 0
        self._en_titulo = False

    def handle_starttag(self, etiqueta: str, _: object) -> None:
        if etiqueta == "title":
            self._en_titulo = True
        elif etiqueta in _IGNORADOS:
            self._ignorando += 1
        elif etiqueta in _BLOQUES:
            self.parrafos.append("")

    def handle_endtag(self, etiqueta: str) -> None:
        if etiqueta == "title":
            self._en_titulo = False
        elif etiqueta in _IGNORADOS:
            self._ignorando = max(0, self._ignorando - 1)
        elif etiqueta in _BLOQUES:
            self.parrafos.append("")

    def handle_data(self, datos: str) -> None:
        if self._en_titulo:
            self.titulo += datos
        elif not self._ignorando:
            self.parrafos[-1] += datos


def extraer(contenido: bytes, texto: str) -> tuple[str, list[str]]:
    """El título y los párrafos de un PDF o de un HTML."""
    if contenido.startswith(b"%PDF"):
        lector = PdfReader(io.BytesIO(contenido))
        # pypdf devuelve una línea por renglón; cada renglón cuenta como párrafo
        # y `fragmentar` los junta.
        lineas = [l for p in lector.pages for l in (p.extract_text() or "").splitlines()]
        return str((lector.metadata or {}).get("/Title") or ""), lineas
    extractor = _TextoDeHtml()
    extractor.feed(texto)
    return extractor.titulo.strip(), extractor.parrafos


def fragmentar(parrafos: Iterable[str]) -> list[str]:
    """Junta los párrafos cortos y parte los largos, hasta
    `PALABRAS_POR_FRAGMENTO` palabras por fragmento."""
    fragmentos: list[list[str]] = []
    actual: list[str] = []
    for parrafo in parrafos:
        palabras = parrafo.split()
        if actual and len(actual) + len(palabras) > PALABRAS_POR_FRAGMENTO:
            fragmentos.append(actual)
            actual = []
        actual += palabras
        while len(actual) > PALABRAS_POR_FRAGMENTO:
            fragmentos.append(actual[:PALABRAS_POR_FRAGMENTO])
            actual = actual[PALABRAS_POR_FRAGMENTO:]
    if actual:
        fragmentos.append(actual)
    return [" ".join(f) for f in fragmentos]


# -- Corrida ----------------------------------------------------------------


def ingerir(
    indice: IndiceDeFuentes,
    cliente: httpx.Client,
    configuracion: Configuracion,
    reloj: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    espera: Callable[[float], None] = time.sleep,
    fuentes: list[FuenteOficial] = FUENTES,
) -> None:
    """Una corrida de la ingesta sobre todas las fuentes. El embebedor es el
    del índice."""
    desde = (reloj() - timedelta(days=configuracion.ventana_indice_dias)).date()
    # Uno por sitio: Salud y Educación comparten argentina.gob.ar y su demora.
    rastreadores: dict[str, Rastreador] = {}
    for fuente in fuentes:
        try:
            if fuente.dominio not in rastreadores:
                rastreadores[fuente.dominio] = Rastreador(
                    cliente, fuente.dominio, configuracion.demora_minima_rastreo_s, reloj, espera
                )
            _ingerir_fuente(
                fuente, rastreadores[fuente.dominio], indice, configuracion, reloj, desde
            )
        except Exception as error:  # una fuente rota no frena a las demás
            registro.error("ingesta | %s | abortada | %s", fuente.nombre, error)
        # También si falló: el catálogo tiene siempre todas; el fallo, en el registro.
        rastreador = rastreadores.get(fuente.dominio)
        try:
            indice.registrar_corrida(
                fuente.nombre, fuente.dominio,
                rastreador.demora_s if rastreador else configuracion.demora_minima_rastreo_s,
                reloj().isoformat(timespec="seconds"),
            )
        except Exception as error:
            registro.error("ingesta | %s | sin registrar la corrida | %s", fuente.nombre, error)
    indice.purgar(desde.isoformat())


def _ingerir_fuente(
    fuente: FuenteOficial,
    rastreador: Rastreador,
    indice: IndiceDeFuentes,
    configuracion: Configuracion,
    reloj: Callable[[], datetime],
    desde: date,
) -> None:
    # Uno por URL y del más nuevo al más viejo: si el tope corta, corta lo viejo.
    candidatos = {c.url: c for c in fuente.descubrir(rastreador, desde)}
    pendientes = sorted(candidatos.values(), key=lambda c: c.fecha, reverse=True)
    hoy = reloj().date()
    bajados = omitidos = fallados = 0
    for candidato in pendientes:
        if bajados >= configuracion.tope_documentos_por_fuente:
            break
        if candidato.fecha < desde or indice.indexada(candidato.url):
            continue
        try:
            respuesta = rastreador.get(candidato.url)
        except Excluida:
            omitidos += 1
            continue
        except Limitada:
            # RNF-17: el sitio pidió bajar el ritmo; lo que falta, en la próxima corrida.
            registro.warning("ingesta | %s | 429 en %s: se corta la fuente", fuente.nombre,
                             candidato.url)
            fallados += 1
            break
        except httpx.HTTPError as error:
            registro.warning("ingesta | %s | %s | %s", fuente.nombre, candidato.url, error)
            fallados += 1
            continue
        bajados += 1
        try:
            titulo, parrafos = extraer(respuesta.content, respuesta.text)
            textos = fragmentar(parrafos)
            # ponytail: un documento sin texto (PDF escaneado, página vacía)
            # no queda indexado y se vuelve a bajar en cada corrida, ocupando
            # el tope; recordar esas URL si llegan a comerse el tope de una fuente.
            if not textos:
                raise ValueError("sin texto")
            indice.agregar([
                Fragmento(
                    texto, candidato.url, candidato.titulo or titulo or candidato.url,
                    # Una fecha futura es un error del sitio (el INDEC lista
                    # un informe de octubre como 22/11/26): cuenta como hoy.
                    min(candidato.fecha, hoy).isoformat(), fuente.nombre,
                )
                for texto in textos
            ])
        except Exception as error:  # un documento roto no aborta la corrida
            registro.warning("ingesta | %s | %s | %s", fuente.nombre, candidato.url, error)
            fallados += 1
    registro.info(
        "ingesta | %s | descubiertos=%d | bajados=%d | omitidos=%d | fallados=%d",
        fuente.nombre, len(candidatos), bajados, omitidos, fallados,
    )


def ruta_del_candado(configuracion: Configuracion) -> Path:
    return Path(f"{configuracion.ruta_base_de_datos}.ingesta")


def tomar_candado(ruta: Path) -> IO[str] | None:
    """El candado de la corrida, o `None` si otra lo tiene. Se suelta al
    cerrar el archivo o al terminar el proceso."""
    archivo = open(ruta, "a")
    try:
        fcntl.flock(archivo, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        archivo.close()
        return None
    return archivo


def principal() -> None:
    """La corrida sobre la base local configurada, con el embebedor de la memoria."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    # Un renglón por pedido y un aviso por fuente tipográfica de cada PDF tapan el resumen.
    logging.getLogger("httpx2").setLevel(logging.WARNING)
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    configuracion = obtener_configuracion()
    candado = tomar_candado(ruta_del_candado(configuracion))
    if candado is None:
        registro.warning("ingesta | ya hay una corrida en curso")
        return
    embebedor = ClienteEmbebedor(
        configuracion.url_embebedor or configuracion.url_clasificador,
        configuracion.tiempo_limite_clasificador_s,
    )
    indice = IndiceDeFuentes(configuracion.ruta_base_de_datos, embebedor)
    with httpx.Client(
        headers={"User-Agent": AGENTE}, timeout=60
    ) as cliente:
        ingerir(indice, cliente, configuracion)
    candado.close()


if __name__ == "__main__":
    principal()
