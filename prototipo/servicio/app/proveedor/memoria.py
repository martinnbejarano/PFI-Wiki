"""Memoria semántica de evidencia del Módulo 3 (ticket #101, PRD #100).

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
"""

from __future__ import annotations

import http.client
import json
import logging
import sqlite3
import threading
import urllib.request
from datetime import datetime, timezone
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
    ) -> None:
        self.llm = llm
        self.embebedor = embebedor
        self.umbral_similitud = umbral_similitud
        # Una conexión propia sobre el archivo del histórico, con el mismo
        # candado global que `Historial` y por el mismo motivo.
        self._conexion = sqlite3.connect(ruta, check_same_thread=False)
        self._conexion.enable_load_extension(True)
        sqlite_vec.load(self._conexion)
        self._conexion.enable_load_extension(False)
        self._candado = threading.Lock()
        with self._candado, self._conexion:
            self._conexion.executescript(ESQUEMA)

    def extraer_afirmacion(self, texto: str) -> AfirmacionExtraida:
        return self.llm.extraer_afirmacion(texto)

    def extraer_y_recuperar(
        self, texto: str
    ) -> tuple[AfirmacionExtraida, list[Fuente]]:
        vector = sqlite_vec.serialize_float32(self.embebedor.embeber(texto))
        with self._candado:
            fila = self._conexion.execute(
                """
                SELECT m.afirmacion, m.tipo, m.fuentes, v.distance
                FROM memoria_vector v JOIN memoria_evidencia m ON m.id = v.rowid
                WHERE v.embedding MATCH ? AND k = 1
                """,
                (vector,),
            ).fetchone()

        if fila is None:
            registro.info("memoria | fallo | similitud=- | motivo=vacia")
        else:
            afirmacion, tipo, fuentes, distancia = fila
            similitud = 1.0 - distancia
            if similitud >= self.umbral_similitud:
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
            registro.info("memoria | fallo | similitud=%.3f | motivo=umbral", similitud)

        extraida, fuentes = self.llm.extraer_y_recuperar(texto)
        admisibles = filtrar_por_jerarquia(fuentes)
        # Solo se recuerda evidencia de verdad: sin afirmación o sin fuentes
        # admisibles no hay nada que valga la pena reutilizar.
        if extraida.hay_afirmacion_verificable and admisibles:
            self._guardar(texto, extraida, admisibles, vector)
        return extraida, fuentes

    def emitir_veredicto(
        self, afirmacion: str, fuentes: list[Fuente], veredicto: Veredicto
    ) -> VeredictoEmitido:
        return self.llm.emitir_veredicto(afirmacion, fuentes, veredicto)

    def _guardar(
        self, texto: str, extraida: AfirmacionExtraida, fuentes: list[Fuente], vector: bytes
    ) -> None:
        with self._candado, self._conexion:
            cursor = self._conexion.execute(
                "INSERT INTO memoria_evidencia "
                "(texto, afirmacion, tipo, fuentes, fecha_recuperacion) VALUES (?, ?, ?, ?, ?)",
                (
                    texto,
                    extraida.afirmacion,
                    extraida.tipo.value,
                    _FUENTES.dump_json(fuentes).decode(),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            self._conexion.execute(
                "INSERT INTO memoria_vector (rowid, embedding) VALUES (?, ?)",
                (cursor.lastrowid, vector),
            )
