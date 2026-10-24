"""El adaptador de OpenAI en lo que no necesita red: la redacción sin llamada
al proveedor, que es la que sacó una de las dos llamadas del análisis (RNF-02)."""

from app.configuracion import Configuracion
from app.contrato import Fuente, Postura, TipoFuente, Veredicto
from app.proveedor.openai import ProveedorOpenAI


def _fuente(url: str, postura: Postura, tipo: TipoFuente, razon: str = "") -> Fuente:
    return Fuente(titulo="t", url=url, tipo=tipo, postura=postura, razon=razon)


def _proveedor() -> ProveedorOpenAI:
    return ProveedorOpenAI(Configuracion())


def test_la_justificacion_nombra_cada_dominio_una_vez_y_las_razones_llevan_su_enlace() -> None:
    fuentes = [
        _fuente("https://www.indec.gob.ar/a", Postura.CORROBORA, TipoFuente.FUENTE_OFICIAL, "El INDEC publica 1,9 %."),
        _fuente("https://www.indec.gob.ar/b", Postura.CORROBORA, TipoFuente.FUENTE_OFICIAL, "El informe repite el dato."),
        _fuente("https://www.lanacion.com.ar/c", Postura.NEUTRAL, TipoFuente.MEDIO_DE_REFERENCIA),
    ]

    emitido = _proveedor().emitir_veredicto("a", fuentes, Veredicto.PARECE_VERIFICADO)

    assert emitido.justificacion.count("indec.gob.ar") == 1
    assert [r.fuente_url for r in emitido.razones] == [
        "https://www.indec.gob.ar/a", "https://www.indec.gob.ar/b",
    ]


def test_el_desmentido_se_atribuye_a_la_fuente_oficial() -> None:
    fuentes = [
        _fuente("https://www.clarin.com/x", Postura.CONTRADICE, TipoFuente.MEDIO_DE_REFERENCIA),
        _fuente("https://www.boletinoficial.gob.ar/y", Postura.CONTRADICE, TipoFuente.FUENTE_OFICIAL),
    ]

    emitido = _proveedor().emitir_veredicto(
        "a", fuentes, Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES
    )

    assert emitido.justificacion.startswith("Lo que publica boletinoficial.gob.ar")
