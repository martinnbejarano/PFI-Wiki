"""Índice local de fuentes oficiales del Módulo 3 (ticket #108, PRD #107).

La evidencia oficial es la de mayor peso de la jerarquía, y por la búsqueda web
llega con la misma latencia y la misma caja negra que los medios. Este índice
guarda fragmentos de documentos oficiales recientes y devuelve los más cercanos
al texto de la publicación, que el adaptador del LLM le entrega a su única
llamada como un bloque de documentos.

El esquema es el del modelo de datos del capítulo 4, en el mismo archivo SQLite
del histórico y de la memoria, con `sqlite-vec`:

- `fuente_oficial`: el catálogo, con su dominio, su demora de rastreo y la
  fecha de la última corrida. Lo llena la ingesta (#109, `app/ingesta.py`).
- `documento`: un fragmento por fila, con su texto, la URL de origen, el título
  del documento, la fecha de publicación y la fuente.
- `documento_vector`: el *embedding* de cada fragmento, con el mismo `rowid`.

Los fragmentos se embeben con el mismo embebedor que la memoria, que memoriza el
último texto: la memoria y el índice comparten un solo pedido a `/embeber` por
análisis. Cualquier falla sale como `ErrorDelProveedor`, igual que en el
embebedor, para que quien consulta tenga una sola excepción que atajar.
"""

from __future__ import annotations

import sqlite3
import threading
from dataclasses import dataclass

import sqlite_vec

from .memoria import DIMENSIONES, Embebedor
from .puerto import ErrorDelProveedor

ESQUEMA = f"""
CREATE TABLE IF NOT EXISTS fuente_oficial (
    nombre           TEXT PRIMARY KEY,
    dominio          TEXT NOT NULL,
    demora_rastreo_s REAL NOT NULL,
    ultima_corrida   TEXT
);
CREATE TABLE IF NOT EXISTS documento (
    id                INTEGER PRIMARY KEY,
    fuente            TEXT NOT NULL REFERENCES fuente_oficial(nombre),
    url               TEXT NOT NULL,
    titulo            TEXT NOT NULL,
    fecha_publicacion TEXT NOT NULL,
    texto             TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS documento_url ON documento(url);
CREATE VIRTUAL TABLE IF NOT EXISTS documento_vector USING vec0(
    embedding float[{DIMENSIONES}] distance_metric=cosine
);
"""


@dataclass(frozen=True)
class Fragmento:
    """Un fragmento de un documento oficial. `fecha_publicacion` va en ISO
    (`AAAA-MM-DD`) y `fuente` es el nombre de la fila de `fuente_oficial`."""

    texto: str
    url: str
    titulo: str
    fecha_publicacion: str
    fuente: str


class IndiceDeFuentes:
    """Fragmentos oficiales con su *embedding*, consultables por similitud."""

    def __init__(self, ruta: str, embebedor: Embebedor) -> None:
        self.embebedor = embebedor
        # Mismo candado y mismo motivo que la memoria: una conexión compartida
        # entre los hilos del *pool* de FastAPI.
        self._candado = threading.Lock()
        # Si el almacén no se abre, el índice queda inactivo: cada consulta
        # falla y el análisis sigue sin el bloque. El servicio arranca igual.
        self._conexion: sqlite3.Connection | None = None
        self._error_al_abrir = ""
        try:
            conexion = sqlite3.connect(ruta, check_same_thread=False)
            conexion.enable_load_extension(True)
            sqlite_vec.load(conexion)
            conexion.enable_load_extension(False)
            with conexion:
                conexion.executescript(ESQUEMA)
            self._conexion = conexion
        except (sqlite3.Error, AttributeError) as error:
            self._error_al_abrir = str(error)

    def agregar(self, fragmentos: list[Fragmento]) -> None:
        """Embebe y guarda los fragmentos. Lo usa la ingesta (#109)."""
        conexion = self._activa()
        vectores = [
            sqlite_vec.serialize_float32(self.embebedor.embeber(f.texto)) for f in fragmentos
        ]
        try:
            with self._candado, conexion:
                for fragmento, vector in zip(fragmentos, vectores):
                    cursor = conexion.execute(
                        "INSERT INTO documento (fuente, url, titulo, fecha_publicacion, texto) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (fragmento.fuente, fragmento.url, fragmento.titulo,
                         fragmento.fecha_publicacion, fragmento.texto),
                    )
                    conexion.execute(
                        "INSERT INTO documento_vector (rowid, embedding) VALUES (?, ?)",
                        (cursor.lastrowid, vector),
                    )
        except sqlite3.Error as error:
            raise ErrorDelProveedor(f"indice | {error}") from error

    def buscar(self, texto: str, k: int) -> list[tuple[Fragmento, float]]:
        """Los `k` fragmentos más cercanos al texto, con su similitud coseno,
        del más cercano al más lejano. El umbral lo aplica quien consulta."""
        conexion = self._activa()
        vector = sqlite_vec.serialize_float32(self.embebedor.embeber(texto))
        try:
            with self._candado:
                filas = conexion.execute(
                    """
                    SELECT d.texto, d.url, d.titulo, d.fecha_publicacion, d.fuente, v.distance
                    FROM documento_vector v JOIN documento d ON d.id = v.rowid
                    WHERE v.embedding MATCH ? AND k = ?
                    ORDER BY v.distance
                    """,
                    (vector, k),
                ).fetchall()
        except sqlite3.Error as error:
            raise ErrorDelProveedor(f"indice | {error}") from error
        return [(Fragmento(*fila[:5]), 1.0 - fila[5]) for fila in filas]

    # -- Lo que usa la ingesta (#109) --------------------------------------

    def indexada(self, url: str) -> bool:
        """Si ya hay fragmentos de esa URL: la ingesta no la vuelve a bajar."""
        return self._consultar(
            "SELECT 1 FROM documento WHERE url = ? LIMIT 1", (url,)
        ) is not None

    def purgar(self, antes_de: str) -> None:
        """Borra los fragmentos publicados antes de la fecha ISO, con su vector."""
        self._escribir(
            "DELETE FROM documento_vector WHERE rowid IN "
            "(SELECT id FROM documento WHERE fecha_publicacion < ?)",
            "DELETE FROM documento WHERE fecha_publicacion < ?",
            parametros=(antes_de,),
        )

    def registrar_corrida(
        self, nombre: str, dominio: str, demora_rastreo_s: float, fecha: str
    ) -> None:
        """Da de alta la fuente en el catálogo o la actualiza con su corrida."""
        self._escribir(
            "INSERT INTO fuente_oficial (nombre, dominio, demora_rastreo_s, ultima_corrida) "
            "VALUES (?, ?, ?, ?) ON CONFLICT (nombre) DO UPDATE SET "
            "dominio = excluded.dominio, demora_rastreo_s = excluded.demora_rastreo_s, "
            "ultima_corrida = excluded.ultima_corrida",
            parametros=(nombre, dominio, demora_rastreo_s, fecha),
        )

    def ultima_corrida(self, nombre: str) -> str | None:
        fila = self._consultar(
            "SELECT ultima_corrida FROM fuente_oficial WHERE nombre = ?", (nombre,)
        )
        return fila[0] if fila else None

    def _consultar(self, sql: str, parametros: tuple) -> tuple | None:
        conexion = self._activa()
        try:
            with self._candado:
                return conexion.execute(sql, parametros).fetchone()
        except sqlite3.Error as error:
            raise ErrorDelProveedor(f"indice | {error}") from error

    def _escribir(self, *sentencias: str, parametros: tuple) -> None:
        conexion = self._activa()
        try:
            with self._candado, conexion:
                for sql in sentencias:
                    conexion.execute(sql, parametros)
        except sqlite3.Error as error:
            raise ErrorDelProveedor(f"indice | {error}") from error

    def _activa(self) -> sqlite3.Connection:
        if self._conexion is None:
            raise ErrorDelProveedor(f"indice | inactivo | {self._error_al_abrir}")
        return self._conexion
