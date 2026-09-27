"""La jerarquía de evidencia de RF-05, hecha configuración y hecha filtro.

Dos cosas viven acá y no repartidas por el servicio:

1. **La lista de dominios admisibles con su escalón.** Es configuración: el
   ticket #24 y la Entrega 4 la van a tocar —sumar fuentes oficiales, cambiar el
   conjunto de verificadores— y ninguna de esas dos cosas debería obligar a
   abrir el adaptador del proveedor.
2. **El filtro que la hace valer.** Es código propio y observable, y es lo que
   la batería de pruebas ejercita a través de `POST /analizar`.

La jerarquía tiene tres escalones y el orden entre ellos no es indistinto —
fuentes oficiales, medios de referencia, verificaciones previas—, tal como lo
fija `wiki/solucion/metodologia-tecnica.md` y lo dibuja la tercera pantalla del
*mockup*. `JERARQUIA_DE_EVIDENCIA` está declarada en ese orden y de ahí sale
tanto la prioridad como el orden en que el panel de evidencia agrupa las
fuentes.


Verificación de la restricción de dominios del proveedor de búsqueda
--------------------------------------------------------------------

La *spec* (issue #18) dejó esta capacidad marcada como **sin verificar** y pidió
confirmarla antes de escribir el paso de búsqueda. Queda anotado acá el
resultado, que es lo que el criterio de aceptación del ticket #23 exige.

**Consultado el 2026-08-25** en la guía de la herramienta de búsqueda web,
https://developers.openai.com/api/docs/guides/tools-web-search.md, y
contrastado contra los tipos del SDK instalado (`openai==3.3.1`), en
`openai/types/responses/web_search_tool_param.py`.

**La capacidad existe.** La herramienta `web_search` de la API de respuestas
acepta un objeto `filters` con `allowed_domains`. Lo que la verificación
encontró sobre sus límites:

- **Hasta 100 dominios** en `allowed_domains`. Con el padrón de ADEPA la
  jerarquía declara 111, así que al proveedor se le declara un recorte; ver
  `DOMINIOS_PARA_EL_PROVEEDOR`.
- Los dominios se escriben **sin el esquema**: `clarin.com`, y no
  `https://clarin.com/`.
- **Los subdominios del dominio declarado quedan incluidos.** Lo dice la guía y
  lo repite la documentación del propio tipo del SDK: «Subdomains of the
  provided domains are allowed as well». Es lo que hace que declarar
  `argentina.gob.ar` alcance para los contenidos del Ministerio de Salud y del
  de Educación, que es como los aloja ese sitio.
- Solo está disponible en **la API de respuestas con la herramienta
  `web_search`**. Ni las terminaciones de conversación con modelos de búsqueda
  ni `web_search_preview` la admiten.

Dos hallazgos laterales de la verificación que conviene dejar escritos:

1. La guía documenta también `blocked_domains`, y **el SDK instalado no lo
   declara**: `Filters` en `openai==3.3.1` tiene un solo campo,
   `allowed_domains`. Acá no hace falta —la jerarquía es una lista blanca— pero
   quien vaya a usarlo tiene que saber que no está en el tipado de esta versión.
2. La documentación presenta el filtro como una restricción y no como una
   preferencia, pero **no publica ninguna garantía de que sea duro**, y desde el
   servicio no hay forma de comprobarlo: la búsqueda ocurre dentro del
   proveedor, sobre una superficie que no se puede probar ni observar.

**Por eso el filtro propio se aplica igual, y no es redundancia inútil.** El
filtro del proveedor es una caja negra que no controlamos; el de este módulo
corre sobre las URLs que efectivamente volvieron, está escrito acá y es lo que
los tests ejercitan. Si el proveedor cambiara el comportamiento de su filtro sin
avisar, la restricción de RF-05 seguiría en pie. Los dos actúan: el del
proveedor evita gastar la búsqueda fuera de la jerarquía, el propio hace valer
la regla.


Cómo se compara un dominio
--------------------------

`clasificar_dominio` compara el **anfitrión** de la URL contra cada dominio
declarado, exigiendo igualdad o sufijo con punto. Nunca una subcadena. Es la
diferencia entre un filtro y un colador:

- `www.clarin.com` y `servicios.infoleg.gob.ar` **entran**: son subdominios.
- `no-es-clarin.com` **no entra**: contiene `clarin.com` como sufijo de cadena
  pero no es un subdominio suyo. Un `in` sobre el texto lo dejaría pasar, y es
  exactamente la forma que toma la suplantación de un medio.
- `clarin.com.desinformacion.test` **no entra**: el dominio registrable es otro.
- Las mayúsculas y el punto final del anfitrión absoluto no cambian nada.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import NamedTuple
from urllib.parse import urlsplit

from .contrato import Fuente, TipoFuente


class EscalonDeEvidencia(NamedTuple):
    """Un escalón de la jerarquía: su tipo y los dominios que lo componen."""

    tipo: TipoFuente
    dominios: tuple[str, ...]


# El orden de esta tupla ES la jerarquía. Cambiarlo cambia la prioridad del
# contraste y el orden de los grupos del panel de evidencia.
JERARQUIA_DE_EVIDENCIA: tuple[EscalonDeEvidencia, ...] = (
    # Escalón 1 — fuentes oficiales. Las seis que enumera RF-05, sobre cinco
    # dominios: `argentina.gob.ar` aloja los contenidos del Ministerio de Salud
    # y del de Educación, tal como lo registra `wiki/proyecto/recursos.md`, así
    # que no son dos dominios sino uno.
    EscalonDeEvidencia(
        TipoFuente.FUENTE_OFICIAL,
        (
            "infoleg.gob.ar",
            "indec.gob.ar",
            "bcra.gob.ar",
            "boletinoficial.gob.ar",
            "argentina.gob.ar",
        ),
    ),
    # Escalón 2 — los medios socios activos de ADEPA (Asociación de Entidades
    # Periodísticas Argentinas), **todos**, no una selección propia.
    #
    # Es la respuesta a «¿quién verifica al verificador?» de la exposición del
    # 50 %: el criterio de qué medio entra no lo fija el proyecto sino la entidad
    # que nuclea a la prensa argentina, y su padrón es público. Se toma de
    # https://adepa.org.ar/asociados/socios-activos/ al 2026-09-27: 130 socios,
    # de los cuales 103 declaran sitio web. Van en el orden del padrón.
    # Reemplaza a los cinco medios elegidos a mano (Télam, además, dejó de
    # operar como agencia en 2024).
    EscalonDeEvidencia(
        TipoFuente.MEDIO_DE_REFERENCIA,
        (
            "0221.com.ar",
            "a24.com",
            "diarioactualidad.com",
            "adnsur.com.ar",
            "ahora.com.ar",
            "ambito.com",
            "bigbangnews.com",
            "canal12web.com",
            "diariocastellanos.net",
            "cenital.com",
            "chacabucoenred.com",
            "ciudadano.news",
            "clarin.com",
            "daia.org.ar",
            "contexto.com.ar",
            "grupocronica.com.ar",
            "diariodemocracia.com",
            "multimedioscanning.com",
            "diarioellibertador.com.ar",
            "diarioformosa.net",
            "diariohuarpe.com",
            "diariolavozdelchaco.com",
            "diarionucleo.com",
            "diariouno.com.ar",
            "unoentrerios.com.ar",
            "ecosdiarios.com.ar",
            "perfil.com.ar",
            "diarioel9dejulio.com.ar",
            "elancasti.com.ar",
            "diarioelargentino.com.ar",
            "elciudadano.com.ar",
            "elcoeditores.com",
            "cronista.com.ar",
            "eldiarioar.com",
            "eldiariodelapampa.com.ar",
            "eleco.com.ar",
            "eleconomista.com.ar",
            "elesquiu.com",
            "elheraldo.com.ar",
            "elliberal.com.ar",
            "corrientes.com.ar",
            "semanarioelmundo.com.ar",
            "diarioelnorte.com.ar",
            "elsolonline.com.ar",
            "territoriodigital.com",
            "eltiempo.com.ar",
            "eltribuno.com.ar",
            "gazetanorte.com.ar",
            "hola.com.ar",
            "relacionespublicas.com",
            "infonegocios.info",
            "infobae.com",
            "infocielo.com",
            "inforama.com.ar",
            "jornadaonline.com",
            "jujuyalmomento.com.ar",
            "laarena.com.ar",
            "lacapitalmdp.com",
            "lacapital.com.ar",
            "lagaceta.com.ar",
            "lmneuquen.com.ar",
            "lanacion.com.ar",
            "lanueva.com.ar",
            "laopinionaustral.com.ar",
            "laopinionsemanario.com.ar",
            "lapalabradeberazategui.com.ar",
            "lapoliticaonline.com",
            "laprensa.com.ar",
            "laverdadonline.com",
            "lavozdesanjusto.com.ar",
            "lavozdelinterior.com.ar",
            "letrap.com.ar",
            "losandes.com.ar",
            "mendozatoday.com.ar",
            "miradorprovincial.com",
            "misionesonline.net",
            "centrogalicia-bsas.org",
            "diarionorte.com.ar",
            "norteonline.com.ar",
            "notife.com",
            "periodiconuevaepoca.com.ar",
            "nuevarioja.com.ar",
            "nuevospapeles.com",
            "ole.com.ar",
            "opisantacruz.com.ar",
            "pagina12.com.ar",
            "paralelo32.com.ar",
            "pilaradiario.com",
            "portalmisiones.com",
            "continental.com.ar",
            "radiopopularsanluis.com.ar",
            "rivadavia.com.ar",
            "diarioresumen.com",
            "rionegro.com.ar",
            "rosarionuestro.com",
            "santafe.com.ar",
            "seccionciudad.com.ar",
            "tiemposur.com.ar",
            "tn.com.ar",
            "todojujuy.com",
            "tranqueradigital.com.ar",
            "tsnnecochea.com.ar",
            "turismocero.com",
        ),
    ),
    # Escalón 3 — verificaciones previas. Chequeado y los dos equivalentes que
    # nombra `wiki/solucion/metodologia-tecnica.md`: Reverso y AFP Factual.
    #
    # Que estén acá no contradice que `wiki/proyecto/recursos.md` haya sacado a
    # Chequeado de la tabla de ingesta: esa tabla es la de los sitios que el
    # sistema completo **recorre por su cuenta**, y Chequeado responde 403 a
    # todo cliente que no sea un navegador. Acá no se recorre nada: se consulta
    # un índice de búsqueda ajeno y se enlaza el artículo original, que es
    # exactamente la salida que esa misma página deja anotada.
    EscalonDeEvidencia(
        TipoFuente.VERIFICACION_PREVIA,
        (
            "chequeado.com",
            "reversoar.com",
            "factual.afp.com",
        ),
    ),
)

# Aplanado, en el orden de la jerarquía. Es lo que admite el filtro propio.
DOMINIOS_ADMISIBLES: tuple[str, ...] = tuple(
    dominio for escalon in JERARQUIA_DE_EVIDENCIA for dominio in escalon.dominios
)

# Lo que se le declara al proveedor en `filters.allowed_domains`, que acepta
# hasta 100. Con ADEPA la jerarquía pasa de 111: van primero los escalones
# chicos —oficiales y verificaciones— y después los medios hasta llenar.
# ponytail: los últimos medios del padrón quedan fuera del filtro del proveedor
# (el propio los admite igual); si pesa, partir la búsqueda en dos llamadas.
TOPE_DEL_PROVEEDOR = 100
DOMINIOS_PARA_EL_PROVEEDOR: tuple[str, ...] = tuple(
    dominio
    for escalon in sorted(JERARQUIA_DE_EVIDENCIA, key=lambda e: len(e.dominios))
    for dominio in escalon.dominios
)[:TOPE_DEL_PROVEEDOR]

# Precedencia de cada tipo, derivada del orden de la tupla en lugar de repetida
# a mano: agregar un escalón no obliga a acordarse de tocar dos sitios.
_PRECEDENCIA: dict[TipoFuente, int] = {
    escalon.tipo: indice for indice, escalon in enumerate(JERARQUIA_DE_EVIDENCIA)
}


def clasificar_dominio(url: str) -> TipoFuente | None:
    """Devuelve el escalón al que pertenece una URL, o `None` si no pertenece.

    `None` significa «fuera de la jerarquía de evidencia» y es la respuesta
    correcta para la enorme mayoría de internet. No es una falla.
    """
    anfitrion = _anfitrion(url)
    if not anfitrion:
        return None

    for escalon in JERARQUIA_DE_EVIDENCIA:
        for dominio in escalon.dominios:
            if anfitrion == dominio or anfitrion.endswith(f".{dominio}"):
                return escalon.tipo
    return None


def filtrar_por_jerarquia(fuentes: Iterable[Fuente]) -> list[Fuente]:
    """Deja solo las fuentes de la jerarquía, con su tipo real y en su orden.

    Hace tres cosas, y las tres importan:

    1. **Descarta** toda fuente cuya URL caiga fuera de los dominios
       declarados. Es la forma en que RF-05 se hace valer del lado del servicio,
       sin depender de que el proveedor de búsqueda haya respetado el filtro que
       se le declaró.
    2. **Corrige el tipo** con el que cada fuente viaja, derivándolo del
       dominio. El tipo no es una opinión de quien produjo la fuente: es una
       propiedad del dominio, y hacerlo así impide que una fuente llegue
       etiquetada como oficial sin serlo.
    3. **Ordena** por la precedencia de la jerarquía, de forma estable: dentro
       de un mismo escalón se conserva el orden en que llegaron. Es lo que el
       panel de evidencia dibuja y, según `wiki/solucion/mockups.md`, la
       decisión de fondo de esa pantalla.

    De paso descarta repetidos por URL, que es lo que evita que la misma nota
    aparezca dos veces cuando la búsqueda la encuentra por dos caminos.
    """
    admisibles: list[Fuente] = []
    vistas: set[str] = set()

    for fuente in fuentes:
        tipo = clasificar_dominio(fuente.url)
        if tipo is None:
            continue
        clave = fuente.url.strip().rstrip("/").casefold()
        if clave in vistas:
            continue
        vistas.add(clave)
        admisibles.append(fuente.model_copy(update={"tipo": tipo}))

    return sorted(admisibles, key=lambda fuente: _PRECEDENCIA[fuente.tipo])


def _anfitrion(url: str) -> str:
    """Extrae el anfitrión de una URL, normalizado para comparar.

    Tolera lo que llega de verdad: mayúsculas, espacios alrededor, el punto
    final del nombre absoluto, un puerto explícito y una URL sin esquema. Una
    URL que no se pueda descomponer devuelve la cadena vacía, que
    `clasificar_dominio` traduce en «fuera de la jerarquía»: ante una URL
    ilegible, el filtro descarta en lugar de arriesgar.
    """
    texto = url.strip()
    if not texto:
        return ""
    if "://" not in texto:
        # Sin esquema, `urlsplit` mete todo en el camino y el anfitrión queda
        # vacío. Se le antepone uno para poder descomponerla.
        texto = f"https://{texto}"

    try:
        partes = urlsplit(texto)
    except ValueError:
        return ""

    anfitrion = (partes.hostname or "").strip().rstrip(".")
    return anfitrion.casefold()


__all__ = [
    "DOMINIOS_ADMISIBLES",
    "DOMINIOS_PARA_EL_PROVEEDOR",
    "JERARQUIA_DE_EVIDENCIA",
    "EscalonDeEvidencia",
    "clasificar_dominio",
    "filtrar_por_jerarquia",
]
