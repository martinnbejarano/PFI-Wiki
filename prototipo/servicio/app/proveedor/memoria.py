"""Memoria semántica de evidencia del Módulo 3 (tickets #101 y #102, PRD #100).

La búsqueda web del LLM es casi todo el costo y la latencia de un análisis
(RNF-02), y una misma afirmación viral llega escrita con otras palabras y desde
otras cuentas. La caché de RF-07 no la reconoce porque va por identificador de
tuit. Esta memoria sí: compara el texto de la publicación por similitud con las
que ya tienen evidencia y, si hay una equivalente, devuelve su afirmación y sus
fuentes con su postura sin llamar al LLM.

Dos piezas:

- `ClienteEmbebedor`: habla con `POST /embeber` del contenedor del
  clasificador, que calcula el vector con un modelo propio. Igual que el
  cliente del clasificador, cualquier falla sale como `ErrorDelProveedor`.
- `MemoriaDeEvidencia`: implementa `ProveedorDeAnalisis` envolviendo al LLM y
  se arma **dentro** del proveedor compuesto. Así el clasificador sigue
  puntuando la publicación nueva en un acierto, y la credibilidad, el
  combinador y la justificación se recalculan en el orquestador como siempre.

Se compara el texto de la publicación y no la afirmación extraída: extraer la
afirmación ya es la llamada al LLM que un acierto se ahorra.

El almacén es `sqlite-vec` sobre el mismo archivo SQLite del histórico (sin
motor nuevo ni migración): una tabla vectorial de 384 dimensiones con distancia
coseno y, con el mismo `rowid`, una tabla con el texto, la afirmación, su tipo,
las fuentes en JSON y la fecha de recuperación.

Guardas (#102): un acierto exige similitud sobre el umbral, las mismas cifras
en los dos textos y evidencia dentro de la vigencia; el registro dice cuál
falló (`umbral`, `numeros`, `vencida`). Solo se guarda un análisis completo
con afirmación y fuentes admisibles. Si el embebedor o el almacén fallan, la
memoria se hace a un lado y el análisis sigue por la búsqueda web.
"""

from __future__ import annotations

import http.client
import json
import logging
import re
import sqlite3
import threading
import urllib.request
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from typing import Protocol

import sqlite_vec
from pydantic import BaseModel, Field, TypeAdapter

from ..contrato import Fuente, TipoAfirmacion, Veredicto
from ..jerarquia import filtrar_por_jerarquia
from .puerto import (
    AfirmacionExtraida,
    ErrorDelProveedor,
    ProveedorDeAnalisis,
    VeredictoEmitido,
)

registro = logging.getLogger("app.proveedor.memoria")

DIMENSIONES = 384
"""Las de `paraphrase-multilingual-MiniLM-L12-v2`, el modelo de `/embeber`."""

ESQUEMA = f"""
CREATE TABLE IF NOT EXISTS memoria_evidencia (
    id                 INTEGER PRIMARY KEY,
    texto              TEXT NOT NULL,
    afirmacion         TEXT NOT NULL,
    tipo               TEXT NOT NULL,
    fuentes            TEXT NOT NULL,
    fecha_recuperacion TEXT NOT NULL
);
CREATE VIRTUAL TABLE IF NOT EXISTS memoria_vector USING vec0(
    embedding float[{DIMENSIONES}] distance_metric=cosine
);
"""

_FUENTES = TypeAdapter(list[Fuente])

_NUMERO = re.compile(r"\d+(?:[.,]\d+)*")
"""Números, porcentajes y fechas, todos por sus cifras: «1,9 %» da `1,9`,
«24/10/2026» da `24`, `10` y `2026`. El separador decimal o de miles queda
dentro del número, así que «1,9» y «19» no se confunden."""


def _numeros(texto: str) -> set[str]:
    """Los datos de una publicación que la similitud no ve (PRD #100).

    Dos publicaciones sobre la inflación de septiembre quedan casi idénticas
    para el *embedding* aunque una diga 1,9 % y la otra 2,3 %, y la evidencia
    de una no sirve para contrastar la otra. Por eso un acierto exige además
    el mismo conjunto de cifras en los dos textos.
    """
    # ponytail: solo cifras; una fecha escrita con palabras («el lunes») o
    # «1.000» frente a «1000» no se comparan. El error va hacia el lado
    # barato: una búsqueda de más, nunca un falso acierto por eso.
    return set(_NUMERO.findall(texto))


class Embedding(BaseModel):
    """Lo que devuelve `/embeber`: el vector ya normalizado."""

    vector: list[float] = Field(min_length=DIMENSIONES, max_length=DIMENSIONES)


class Embebedor(Protocol):
    def embeber(self, texto: str) -> list[float]: ...


class ClienteEmbebedor:
    """Cliente HTTP de `POST {url}/embeber` con `{"texto": ...}`.

    Es el gemelo de `ClienteClasificador`: mismo tiempo límite, misma
    traducción de fallas a `ErrorDelProveedor`.
    """

    def __init__(self, url: str, tiempo_limite_s: float) -> None:
        self.url = url.rstrip("/")
        self.tiempo_limite_s = tiempo_limite_s

    def embeber(self, texto: str) -> list[float]:
        if not self.url:
            raise ErrorDelProveedor("embebedor | falta URL_EMBEBEDOR")
        pedido = urllib.request.Request(
            f"{self.url}/embeber",
            data=json.dumps({"texto": texto}).encode(),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(pedido, timeout=self.tiempo_limite_s) as respuesta:
                return Embedding.model_validate_json(respuesta.read()).vector
        except (OSError, ValueError, http.client.HTTPException) as error:
            raise ErrorDelProveedor(f"embebedor | {error}") from error


class MemoriaDeEvidencia:
    """El LLM, con una memoria de la evidencia que ya recuperó delante."""

    def __init__(
        self,
        llm: ProveedorDeAnalisis,
        embebedor: Embebedor,
        ruta: str,
        umbral_similitud: float,
        vigencia_dias: int = 7,
        reloj: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self.llm = llm
        self.embebedor = embebedor
        self.umbral_similitud = umbral_similitud
        self.vigencia = timedelta(days=vigencia_dias)
        # Inyectable para que un test venza evidencia sin esperar una semana.
        self.reloj = reloj
        # Una conexión propia sobre el archivo del histórico, con el mismo
        # candado global que `Historial` y por el mismo motivo.
        self._conexion = sqlite3.connect(ruta, check_same_thread=False)
        self._conexion.enable_load_extension(True)
        sqlite_vec.load(self._conexion)
        self._conexion.enable_load_extension(False)
        self._candado = threading.Lock()
        # Evidencia recuperada que espera a que el análisis termine entero
        # para guardarse. Por hilo: cada petición de `/analizar` corre su
        # análisis completo en un solo hilo del *pool* de FastAPI.
        self._pendiente = threading.local()
        with self._candado, self._conexion:
            self._conexion.executescript(ESQUEMA)

    def extraer_afirmacion(self, texto: str) -> AfirmacionExtraida:
        return self.llm.extraer_afirmacion(texto)

    def extraer_y_recuperar(
        self, texto: str
    ) -> tuple[AfirmacionExtraida, list[Fuente]]:
        self._pendiente.evidencia = None
        try:
            vector = sqlite_vec.serialize_float32(self.embebedor.embeber(texto))
            with self._candado:
                fila = self._conexion.execute(
                    """
                    SELECT m.id, m.texto, m.afirmacion, m.tipo, m.fuentes,
                           m.fecha_recuperacion, v.distance
                    FROM memoria_vector v JOIN memoria_evidencia m ON m.id = v.rowid
                    WHERE v.embedding MATCH ? AND k = 1
                    """,
                    (vector,),
                ).fetchone()
        except (ErrorDelProveedor, sqlite3.Error) as error:
            # La memoria es un atajo, no un módulo del análisis: si el
            # embebedor o el almacén fallan, no se pronuncia y delega en la
            # búsqueda web. Es un fallo de memoria y no un análisis parcial
            # (RNF-11), así que la pieza nueva nunca empeora el servicio.
            registro.warning("memoria | fallo | similitud=- | motivo=no_disponible | %s", error)
            return self.llm.extraer_y_recuperar(texto)

        vencida = None
        if fila is None:
            registro.info("memoria | fallo | similitud=- | motivo=vacia")
        else:
            id_fila, guardado, afirmacion, tipo, fuentes, fecha, distancia = fila
            similitud = 1.0 - distancia
            if similitud < self.umbral_similitud:
                motivo = "umbral"
            elif _numeros(guardado) != _numeros(texto):
                motivo = "numeros"
            elif self.reloj() - datetime.fromisoformat(fecha) > self.vigencia:
                # La evidencia de hace más de una semana puede haber cambiado
                # (PRD #100): se vuelve a buscar y la búsqueda nueva renueva
                # esta misma fila, para que la vieja no quede como la más
                # cercana de las publicaciones que vengan.
                motivo = "vencida"
                vencida = id_fila
            else:
                registro.info("memoria | acierto | similitud=%.3f", similitud)
                # El puntaje y la clase son de relleno: el proveedor compuesto
                # los reemplaza por los del clasificador sobre el texto nuevo.
                extraida = AfirmacionExtraida(
                    afirmacion=afirmacion,
                    tipo=TipoAfirmacion(tipo),
                    puntaje=0.5,
                    clase="sin_verificar",
                )
                return extraida, _FUENTES.validate_json(fuentes)
            registro.info("memoria | fallo | similitud=%.3f | motivo=%s", similitud, motivo)

        extraida, fuentes = self.llm.extraer_y_recuperar(texto)
        admisibles = filtrar_por_jerarquia(fuentes)
        # Solo se recuerda evidencia de verdad: sin afirmación o sin fuentes
        # admisibles no hay nada que valga la pena reutilizar, y un «no se
        # encontró evidencia» no debe propagarse a otras publicaciones.
        if extraida.hay_afirmacion_verificable and admisibles:
            self._pendiente.evidencia = (texto, extraida, admisibles, vector, vencida)
        return extraida, fuentes

    def emitir_veredicto(
        self, afirmacion: str, fuentes: list[Fuente], veredicto: Veredicto
    ) -> VeredictoEmitido:
        """Redacta y, si el análisis llegó entero hasta acá, guarda la evidencia.

        La redacción es el último paso que puede marcar el análisis como
        parcial (RNF-11): si falla, o si el presupuesto de tiempo se agotó y
        este método ni se llama, la evidencia pendiente se descarta. Un
        parcial no alimenta la memoria, igual que no entra en la caché de
        RF-07: una falla puntual no debe contaminar análisis futuros.
        """
        pendiente = getattr(self._pendiente, "evidencia", None)
        self._pendiente.evidencia = None
        emitido = self.llm.emitir_veredicto(afirmacion, fuentes, veredicto)
        if pendiente is not None and pendiente[1].afirmacion == afirmacion:
            try:
                self._guardar(*pendiente)
            except sqlite3.Error as error:
                # El análisis ya está completo: perder el guardado solo
                # cuesta una búsqueda la próxima vez.
                registro.warning("memoria | no se guardó la evidencia: %s", error)
        return emitido

    def _guardar(
        self,
        texto: str,
        extraida: AfirmacionExtraida,
        fuentes: list[Fuente],
        vector: bytes,
        vencida: int | None,
    ) -> None:
        datos = (
            texto,
            extraida.afirmacion,
            extraida.tipo.value,
            _FUENTES.dump_json(fuentes).decode(),
            self.reloj().isoformat(),
        )
        with self._candado, self._conexion:
            if vencida is None:
                cursor = self._conexion.execute(
                    "INSERT INTO memoria_evidencia "
                    "(texto, afirmacion, tipo, fuentes, fecha_recuperacion) VALUES (?, ?, ?, ?, ?)",
                    datos,
                )
                self._conexion.execute(
                    "INSERT INTO memoria_vector (rowid, embedding) VALUES (?, ?)",
                    (cursor.lastrowid, vector),
                )
            else:
                self._conexion.execute(
                    "UPDATE memoria_evidencia SET texto = ?, afirmacion = ?, tipo = ?, "
                    "fuentes = ?, fecha_recuperacion = ? WHERE id = ?",
                    (*datos, vencida),
                )
                self._conexion.execute(
                    "UPDATE memoria_vector SET embedding = ? WHERE rowid = ?",
                    (vector, vencida),
                )
