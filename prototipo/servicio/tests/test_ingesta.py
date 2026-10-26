"""Ingesta del índice de fuentes oficiales (ticket #109, PRD #107), por su función de entrada.

Lo simulado es la red: un `MockTransport` de httpx sirve un INDEC falso con la
forma del real (`robots.txt`, un `sitemap.xml` sin `lastmod` que lista las
páginas de tema, la vista parcial de cada tema con sus informes técnicos y los
PDF). El reloj y la espera son inyectados, y el embebedor es el falso de las
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
    sitio: SitioFalso, indice: IndiceDeFuentes, fuentes=FUENTES, **opciones: object
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
