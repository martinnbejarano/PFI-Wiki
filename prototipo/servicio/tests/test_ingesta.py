"""Ingesta del índice de fuentes oficiales (ticket #109, PRD #107), por su función de entrada.

Lo simulado es la red: un `MockTransport` de httpx sirve un INDEC falso con la
forma del real (`robots.txt`, un `sitemap.xml` sin `lastmod` que lista las
páginas de tema, la vista parcial de cada tema con sus informes técnicos y los
PDF); las demás fuentes (#110), una `RedFalsa` con el sitemap índice del BCRA
y de argentina.gob.ar y los listados por día del Boletín Oficial. El reloj y la
espera son inyectados, y el embebedor es el falso de las
pruebas de la memoria. Ningún test mira tablas: se observa lo que se pidió por
HTTP, lo que devuelve una consulta al índice y el registro.
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone

import httpx2 as httpx
import pytest

from app.configuracion import Configuracion
from app.ingesta import FUENTES, Candidato, FuenteOficial, ingerir
from app.proveedor.indice import IndiceDeFuentes

from .test_memoria import EmbebedorFalso

INDEC = "https://www.indec.gob.ar"
HOY = datetime(2026, 10, 25, 3, 0, tzinfo=timezone.utc)

IPC = "Índice de precios al consumidor"
TEXTO_IPC = "El nivel general del IPC registro en septiembre una variacion de 1,9% mensual."


def pdf_con(*lineas: str) -> bytes:
    """Un PDF mínimo y válido con una línea de texto por argumento."""
    flujo = "BT /F1 10 Tf 50 750 Td 12 TL " + " ".join(f"({l}) Tj T*" for l in lineas) + " ET"
    objetos = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        "/Resources << /Font << /F1 5 0 R >> >> >>",
        f"<< /Length {len(flujo)} >>\nstream\n{flujo}\nendstream",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    salida, posiciones = "%PDF-1.4\n", []
    for numero, objeto in enumerate(objetos, 1):
        posiciones.append(len(salida))
        salida += f"{numero} 0 obj\n{objeto}\nendobj\n"
    xref = len(salida)
    salida += f"xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n"
    salida += "".join(f"{p:010d} 00000 n \n" for p in posiciones)
    salida += f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    return salida.encode("latin-1")


def informe(dias_atras: int, titulo: str, ruta: str) -> str:
    """Un informe técnico como lo lista la vista parcial de un tema del INDEC."""
    fecha = (HOY - timedelta(days=dias_atras)).strftime("%d/%m/%y")
    return (
        '<div class="item-n3"><div class="row"><div class="col-md-9">'
        f'<div class="card-titulo3 mb-3">{fecha}. {titulo}</div></div></div>'
        '<div class="card-texto3"><p>Resumen.</p></div>'
        f'<a class="btn btn-outline-success w-100 btn-sm max-w" href="{ruta}" '
        "target=&#39;_blank&#39;>Leer informe</a></div>"
    )


class SitioFalso:
    """El INDEC falso. Cada pedido queda anotado con la hora del reloj."""

    def __init__(self, reloj: Reloj, robots: str = "User-agent: *\nDisallow:\n") -> None:
        self.reloj = reloj
        self.temas: dict[str, list[str]] = {}
        self.archivos: dict[str, httpx.Response] = {"/robots.txt": httpx.Response(200, text=robots)}
        self.pedidos: list[tuple[datetime, str]] = []

    def tema(self, codigo: str, *informes: str) -> None:
        self.temas[codigo] = list(informes)

    def pdf(self, ruta: str, *lineas: str) -> None:
        self.archivos[ruta] = httpx.Response(
            200, content=pdf_con(*lineas), headers={"Content-Type": "application/pdf"}
        )

    def __call__(self, pedido: httpx.Request) -> httpx.Response:
        ruta = pedido.url.path
        self.pedidos.append((self.reloj(), ruta))
        if ruta == "/sitemap.xml":
            locs = "".join(
                f"<url><loc>{INDEC}/indec/web/Nivel4-Tema-{c.replace('/', '-')}</loc>"
                "<changefreq>monthly</changefreq></url>"
                for c in ["Institucional", *self.temas]
            )
            return httpx.Response(200, text=f'<urlset xmlns="x">{locs}</urlset>')
        codigo = ruta.removeprefix("/Nivel4/Tema/")
        if codigo in self.temas:
            return httpx.Response(200, text="<div>" + "".join(self.temas[codigo]) + "</div>")
        return self.archivos.get(ruta, httpx.Response(404))

    def bajados(self) -> list[str]:
        return [r for _, r in self.pedidos if r.startswith("/uploads/")]


class Reloj:
    """Un reloj que solo avanza cuando la ingesta espera."""

    def __init__(self, ahora: datetime = HOY) -> None:
        self.ahora = ahora

    def __call__(self) -> datetime:
        return self.ahora

    def esperar(self, segundos: float) -> None:
        self.ahora += timedelta(seconds=segundos)


def configuracion(**cambios: object) -> Configuracion:
    return Configuracion(_env_file=None, **cambios)


def correr(
    sitio: SitioFalso, indice: IndiceDeFuentes, fuentes=FUENTES[:1], **opciones: object
) -> None:
    with httpx.Client(transport=httpx.MockTransport(sitio)) as cliente:
        ingerir(
            indice, cliente, configuracion(**opciones),
            reloj=sitio.reloj, espera=sitio.reloj.esperar, fuentes=fuentes,
        )


@pytest.fixture
def indice() -> IndiceDeFuentes:
    return IndiceDeFuentes(":memory:", EmbebedorFalso())


@pytest.fixture
def sitio() -> SitioFalso:
    sitio = SitioFalso(Reloj())
    sitio.tema("3/5/31", informe(12, IPC, "/uploads/informesdeprensa/ipc_10_26AAAA.pdf"))
    sitio.pdf("/uploads/informesdeprensa/ipc_10_26AAAA.pdf", TEXTO_IPC)
    return sitio


def lineas_de_ingesta(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [r.getMessage() for r in caplog.records if r.name == "app.ingesta"]


def test_el_texto_de_un_pdf_entra_al_indice_con_su_url_titulo_y_fecha(sitio, indice) -> None:
    correr(sitio, indice)

    fragmento, similitud = indice.buscar(TEXTO_IPC, 1)[0]
    assert similitud > 0.99
    assert fragmento.url == f"{INDEC}/uploads/informesdeprensa/ipc_10_26AAAA.pdf"
    assert (fragmento.titulo, fragmento.fuente) == (IPC, "INDEC")
    assert fragmento.fecha_publicacion == "2026-10-13"


def test_ningun_fragmento_supera_el_largo_maximo(sitio, indice) -> None:
    largas = [" ".join(f"palabra{n}{m}" for m in range(30)) for n in range(12)]
    sitio.tema("3/9/48", informe(5, "EMAE", "/uploads/informesdeprensa/emae.pdf"))
    sitio.pdf("/uploads/informesdeprensa/emae.pdf", *largas)

    correr(sitio, indice)

    fragmentos = [f for f, _ in indice.buscar("palabra00", 50) if f.titulo == "EMAE"]
    palabras = sum(len(f.texto.split()) for f in fragmentos)
    assert palabras == 360
    assert all(len(f.texto.split()) <= 100 for f in fragmentos)


def test_las_urls_excluidas_por_robots_no_se_bajan(indice, caplog) -> None:
    sitio = SitioFalso(Reloj(), robots="User-agent: *\nDisallow: /uploads/informesdeprensa/priv\n")
    sitio.tema(
        "3/5/31",
        informe(3, "Privado", "/uploads/informesdeprensa/privado.pdf"),
        informe(3, IPC, "/uploads/informesdeprensa/ipc.pdf"),
    )
    sitio.pdf("/uploads/informesdeprensa/privado.pdf", "Secreto.")
    sitio.pdf("/uploads/informesdeprensa/ipc.pdf", TEXTO_IPC)

    with caplog.at_level(logging.INFO, logger="app.ingesta"):
        correr(sitio, indice)

    assert sitio.bajados() == ["/uploads/informesdeprensa/ipc.pdf"]
    assert "omitidos=1" in lineas_de_ingesta(caplog)[-1]


@pytest.mark.parametrize(
    ("robots", "minima", "esperada"),
    [
        pytest.param("User-agent: *\nCrawl-delay: 10\n", 1.0, 10.0, id="declarada"),
        pytest.param("User-agent: *\nDisallow:\n", 2.0, 2.0, id="minima"),
    ],
)
def test_entre_pedidos_al_mismo_sitio_se_espera_la_demora(
    robots, minima, esperada, indice
) -> None:
    sitio = SitioFalso(Reloj(), robots=robots)
    sitio.tema("3/5/31", informe(3, IPC, "/uploads/informesdeprensa/ipc.pdf"))
    sitio.tema("3/9/48", informe(3, "EMAE", "/uploads/informesdeprensa/emae.pdf"))
    sitio.pdf("/uploads/informesdeprensa/ipc.pdf", TEXTO_IPC)
    sitio.pdf("/uploads/informesdeprensa/emae.pdf", "Actividad.")

    correr(sitio, indice, demora_minima_rastreo_s=minima)

    horas = [hora for hora, _ in sitio.pedidos]
    assert len(horas) == 6
    assert all((b - a).total_seconds() >= esperada for a, b in zip(horas, horas[1:]))


def test_fuera_de_la_ventana_no_se_baja_y_se_respeta_el_tope(indice) -> None:
    sitio = SitioFalso(Reloj())
    sitio.tema(
        "3/5/31",
        informe(100, "Viejo", "/uploads/informesdeprensa/viejo.pdf"),
        informe(20, "Anterior", "/uploads/informesdeprensa/anterior.pdf"),
        informe(2, "Nuevo", "/uploads/informesdeprensa/nuevo.pdf"),
    )
    for nombre in ("viejo", "anterior", "nuevo"):
        sitio.pdf(f"/uploads/informesdeprensa/{nombre}.pdf", f"Informe {nombre}.")

    correr(sitio, indice, tope_documentos_por_fuente=1)

    assert sitio.bajados() == ["/uploads/informesdeprensa/nuevo.pdf"]

    sitio.pedidos.clear()
    correr(sitio, indice, tope_documentos_por_fuente=5, ventana_indice_dias=90)

    assert sitio.bajados() == ["/uploads/informesdeprensa/anterior.pdf"]


def test_una_segunda_corrida_no_vuelve_a_bajar_ni_duplica(sitio, indice) -> None:
    correr(sitio, indice)
    sitio.pedidos.clear()

    correr(sitio, indice)

    assert sitio.bajados() == []
    assert len(indice.buscar(TEXTO_IPC, 10)) == 1


def test_lo_vencido_se_purga(sitio, indice) -> None:
    correr(sitio, indice)
    sitio.reloj.ahora = HOY + timedelta(days=85)

    correr(sitio, indice)

    assert indice.buscar(TEXTO_IPC, 10) == []


def test_un_documento_roto_no_aborta_la_corrida(indice, caplog) -> None:
    sitio = SitioFalso(Reloj())
    sitio.tema(
        "3/5/31",
        informe(3, "Caido", "/uploads/informesdeprensa/caido.pdf"),
        informe(3, "Corrupto", "/uploads/informesdeprensa/corrupto.pdf"),
        informe(3, IPC, "/uploads/informesdeprensa/ipc.pdf"),
    )
    sitio.archivos["/uploads/informesdeprensa/caido.pdf"] = httpx.Response(500)
    sitio.archivos["/uploads/informesdeprensa/corrupto.pdf"] = httpx.Response(
        200, content=b"%PDF-1.4\nbasura", headers={"Content-Type": "application/pdf"}
    )
    sitio.pdf("/uploads/informesdeprensa/ipc.pdf", TEXTO_IPC)

    with caplog.at_level(logging.INFO, logger="app.ingesta"):
        correr(sitio, indice)

    assert indice.buscar(TEXTO_IPC, 1)[0][0].titulo == IPC
    assert lineas_de_ingesta(caplog)[-1].endswith("fallados=2")


def test_la_fuente_registra_la_ultima_corrida_y_el_resumen(sitio, indice, caplog) -> None:
    assert indice.ultima_corrida("INDEC") is None

    with caplog.at_level(logging.INFO, logger="app.ingesta"):
        correr(sitio, indice)

    assert indice.ultima_corrida("INDEC") == sitio.reloj().isoformat(timespec="seconds")
    assert lineas_de_ingesta(caplog)[-1] == (
        "ingesta | INDEC | descubiertos=1 | bajados=1 | omitidos=0 | fallados=0"
    )


def test_el_texto_de_un_html_entra_al_indice_por_parrafos(indice) -> None:
    """Las demás fuentes (#110) son un descubridor más; acá, uno de prueba."""
    sitio = SitioFalso(Reloj())
    sitio.archivos["/comunicado"] = httpx.Response(200, text=(
        "<html><head><title>Comunicado</title><script>alert(1)</script></head>"
        "<body><nav>Inicio Contacto</nav><p>El BCRA mantuvo la tasa.</p>"
        "<p>La decisión rige &amp; desde hoy.</p></body></html>"
    ))
    fuente = FuenteOficial(
        "BCRA", INDEC,
        lambda rastreador, desde: [Candidato(f"{INDEC}/comunicado", "", date(2026, 10, 20))],
    )

    correr(sitio, indice, fuentes=[fuente])

    fragmento = indice.buscar("El BCRA mantuvo la tasa.", 1)[0][0]
    assert fragmento.texto == "El BCRA mantuvo la tasa. La decisión rige & desde hoy."
    assert (fragmento.titulo, fragmento.fuente) == ("Comunicado", "BCRA")


def test_la_ventana_y_el_tope_son_configuracion() -> None:
    por_defecto = configuracion()
    assert (por_defecto.ventana_indice_dias, por_defecto.tope_documentos_por_fuente) == (90, 200)


def test_una_fecha_futura_cuenta_como_hoy(indice) -> None:
    sitio = SitioFalso(Reloj())
    sitio.tema("3/1/34", informe(-28, "Supermercados", "/uploads/informesdeprensa/super.pdf"))
    sitio.pdf("/uploads/informesdeprensa/super.pdf", "Ventas en supermercados.")

    correr(sitio, indice)

    assert indice.buscar("Ventas en supermercados.", 1)[0][0].fecha_publicacion == "2026-10-25"


# -- Las demás fuentes (#110) ------------------------------------------------

BCRA = "https://www.bcra.gob.ar"
ARGENTINA = "https://www.argentina.gob.ar"
BOLETIN = "https://www.boletinoficial.gob.ar"


class RedFalsa:
    """Varios sitios falsos a la vez, por URL completa. Sin `robots.txt` propio,
    cada sitio permite todo."""

    def __init__(self, reloj: Reloj) -> None:
        self.reloj = reloj
        self.respuestas: dict[str, httpx.Response] = {}
        self.pedidos: list[tuple[datetime, str]] = []

    def servir(self, url: str, texto: str, estado: int = 200) -> None:
        self.respuestas[url] = httpx.Response(estado, text=texto)

    def __call__(self, pedido: httpx.Request) -> httpx.Response:
        url = str(pedido.url)
        self.pedidos.append((self.reloj(), url))
        if url.endswith("/robots.txt") and url not in self.respuestas:
            return httpx.Response(200, text="User-agent: *\nDisallow:\n")
        return self.respuestas.get(url, httpx.Response(404))

    def pedidas(self, prefijo: str) -> list[str]:
        return [u for _, u in self.pedidos if u.startswith(prefijo)]


def indice_de_sitemaps(*locs: str) -> str:
    """Un `sitemapindex` como los del BCRA y argentina.gob.ar."""
    hijos = "".join(f"<sitemap><loc>{l}</loc><lastmod>2026-07-22T15:06:38+00:00</lastmod></sitemap>"
                    for l in locs)
    return f'<?xml version="1.0"?><sitemapindex xmlns="x">{hijos}</sitemapindex>'


def urlset(*urls: tuple[str, int]) -> str:
    """Un `urlset` con la fecha de modificación de cada URL, a tantos días de HOY."""
    entradas = "".join(
        f"<url><loc>{u}</loc><lastmod>{(HOY - timedelta(days=d)).strftime('%Y-%m-%dT%H:%MZ')}"
        "</lastmod><changefreq>never</changefreq></url>"
        for u, d in urls
    )
    return f'<?xml version="1.0"?><urlset xmlns="x"><url><loc>https://raiz/</loc></url>{entradas}</urlset>'


def pagina(titulo: str, texto: str) -> str:
    return f"<html><head><title>{titulo}</title></head><body><p>{texto}</p></body></html>"


def aviso(seccion: str, id_aviso: int, dias_atras: int, organismo: str, norma: str) -> str:
    """Un renglón del listado de una sección del Boletín Oficial."""
    ruta = f"/detalleAviso/{seccion}/{id_aviso}/{(HOY - timedelta(days=dias_atras)):%Y%m%d}"
    return (
        f'<a href="{ruta}?anexos=1" title="Ver anexos"><i class="fa"></i></a>'
        f'<a href="{ruta}" onclick="sendDetalleEvent()"><div class="linea-aviso">'
        f'<p class="item">{organismo} </p><p class="item-detalle"><small>{norma}</small></p>'
        '<p class="item-detalle" ><small>RESOL-2026-1-APN</small></p></div></a>'
    )


def correr_en(red: RedFalsa, indice: IndiceDeFuentes, nombres: list[str], **opciones) -> None:
    fuentes = [f for f in FUENTES if f.nombre in nombres]
    assert [f.nombre for f in fuentes] == nombres
    with httpx.Client(transport=httpx.MockTransport(red)) as cliente:
        ingerir(indice, cliente, configuracion(**opciones),
                reloj=red.reloj, espera=red.reloj.esperar, fuentes=fuentes)


def test_el_bcra_agrega_lo_publicado_en_la_ventana_de_su_sitemap(indice) -> None:
    red = RedFalsa(Reloj())
    red.servir(f"{BCRA}/sitemap_index.xml", indice_de_sitemaps(
        f"{BCRA}/post-sitemap.xml", f"{BCRA}/publicaciones-sitemap.xml"))
    red.servir(f"{BCRA}/publicaciones-sitemap.xml", "Gateway Timeout", 504)
    red.servir(f"{BCRA}/post-sitemap.xml", urlset(
        (f"{BCRA}/noticias/tasa/", 3),
        (f"{BCRA}/en/noticias/rate/", 3),
        (f"{BCRA}/noticias/vieja/", 200),
    ))
    red.servir(f"{BCRA}/noticias/tasa/", pagina("Tasa | BCRA", "El BCRA mantuvo la tasa."))

    correr_en(red, indice, ["BCRA"])

    fragmento = indice.buscar("El BCRA mantuvo la tasa.", 1)[0][0]
    assert (fragmento.url, fragmento.fuente) == (f"{BCRA}/noticias/tasa/", "BCRA")
    assert fragmento.fecha_publicacion == "2026-10-22"
    assert red.pedidas(f"{BCRA}/noticias") == [f"{BCRA}/noticias/tasa/"]
    assert red.pedidas(f"{BCRA}/en/") == []


def test_de_argentina_gob_ar_solo_entran_salud_y_educacion_con_su_demora(indice) -> None:
    red = RedFalsa(Reloj())
    red.servir(f"{ARGENTINA}/robots.txt", "User-agent: *\nCrawl-delay: 10\nDisallow: /search/\n")
    red.servir(f"{ARGENTINA}/sitemap.xml", indice_de_sitemaps(
        f"{ARGENTINA}/sitemap.xml?page=1", f"{ARGENTINA}/sitemap.xml?page=2"))
    red.servir(f"{ARGENTINA}/sitemap.xml?page=1", urlset(
        (f"{ARGENTINA}/noticias/vacunacion", 1),
        (f"{ARGENTINA}/salud/vacunas", 2),
        (f"{ARGENTINA}/saludables", 2),
    ))
    red.servir(f"{ARGENTINA}/sitemap.xml?page=2", urlset(
        (f"{ARGENTINA}/educacion/becas", 4),
        (f"{ARGENTINA}/transporte/sube", 1),
        (f"{ARGENTINA}/educacion-tecnico-profesional", 1),
    ))
    red.servir(f"{ARGENTINA}/salud/vacunas", pagina("Vacunas", "El calendario de vacunacion."))
    red.servir(f"{ARGENTINA}/educacion/becas", pagina("Becas", "Las becas Progresar."))

    correr_en(red, indice, ["Ministerio de Salud", "Ministerio de Educación"])

    documentos = [u for u in red.pedidas(ARGENTINA)
                  if "/robots.txt" not in u and "/sitemap.xml" not in u]
    assert documentos == [f"{ARGENTINA}/salud/vacunas", f"{ARGENTINA}/educacion/becas"]
    assert indice.buscar("El calendario de vacunacion.", 1)[0][0].fuente == "Ministerio de Salud"
    assert indice.buscar("Las becas Progresar.", 1)[0][0].fuente == "Ministerio de Educación"
    horas = [hora for hora, _ in red.pedidos]
    assert all((b - a).total_seconds() >= 10 for a, b in zip(horas, horas[1:]))


def test_del_boletin_oficial_entra_la_primera_seccion_de_cada_dia_y_nunca_la_segunda(
    indice,
) -> None:
    red = RedFalsa(Reloj())
    red.servir(f"{BOLETIN}/robots.txt", (
        "User-agent: *\nDisallow: /detalleAviso/segunda/*\n"
        "Disallow: /seccion/segunda/*\nDisallow: /seccion/segunda\n"
    ))
    for dias in (2, 30):
        red.servir(f"{BOLETIN}/seccion/primera/{(HOY - timedelta(days=dias)):%Y%m%d}", (
            "<html><body>"
            + aviso("primera", 1000 + dias, dias, "MINISTERIO DE ECONOMÍA", f"Resolución {dias}/2026")
            + aviso("segunda", 2000 + dias, dias, "SOCIEDAD ANÓNIMA", "Constitución")
            + "</body></html>"
        ))
        ruta = f"/detalleAviso/primera/{1000 + dias}/{(HOY - timedelta(days=dias)):%Y%m%d}"
        red.servir(f"{BOLETIN}{ruta}", pagina("BOLETIN OFICIAL", f"Se fija el valor numero {dias}."))

    correr_en(red, indice, ["Boletín Oficial"])

    fragmento = indice.buscar("Se fija el valor numero 2.", 1)[0][0]
    assert fragmento.titulo == "MINISTERIO DE ECONOMÍA - Resolución 2/2026"
    assert (fragmento.fuente, fragmento.fecha_publicacion) == ("Boletín Oficial", "2026-10-23")
    assert indice.buscar("Se fija el valor numero 30.", 1)[0][0].fecha_publicacion == "2026-09-25"
    listados = red.pedidas(f"{BOLETIN}/seccion/")
    assert len(listados) == 91 and all("/seccion/primera/" in u for u in listados)
    assert red.pedidas(f"{BOLETIN}/detalleAviso/segunda") == []


def test_una_fuente_caida_no_impide_que_las_demas_completen_la_corrida(indice, caplog) -> None:
    red = RedFalsa(Reloj())
    red.servir(f"{BCRA}/robots.txt", "Service Unavailable", 503)
    red.servir(f"{BCRA}/sitemap_index.xml", "Service Unavailable", 503)
    dia = f"{(HOY - timedelta(days=1)):%Y%m%d}"
    red.servir(f"{BOLETIN}/seccion/primera/{dia}",
               aviso("primera", 7, 1, "BANCO CENTRAL", "Comunicación A 1"))
    red.servir(f"{BOLETIN}/detalleAviso/primera/7/{dia}", pagina("BO", "La comunicacion rige."))

    with caplog.at_level(logging.INFO, logger="app.ingesta"):
        correr_en(red, indice, [f.nombre for f in FUENTES])

    assert indice.buscar("La comunicacion rige.", 1)[0][0].fuente == "Boletín Oficial"
    lineas = lineas_de_ingesta(caplog)
    assert any(l.startswith("ingesta | BCRA | abortada") for l in lineas)
    assert any(l.startswith("ingesta | Boletín Oficial | descubiertos=1 | bajados=1") for l in lineas)
