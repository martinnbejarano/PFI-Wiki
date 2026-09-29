"""Histórico por instalación (RF-10) e informes de veredicto incorrecto (RF-11).

Es la primera persistencia del prototipo, y la mínima: SQLite por la biblioteca
estándar, un archivo local y dos tablas que toman los nombres del modelo de
datos (`wiki/solucion/modelo-datos.md`), recortadas a lo que CU-04 y CU-05 usan.

- `analisis` guarda la respuesta del contrato **entera, como JSON**, asociada al
  identificador anónimo de la instalación. No es el esquema normalizado de
  RF-16 —`razon`, `evidencia`, `documento`— sino lo que alcanza para volver a
  mostrar el detalle y su evidencia en el panel. Una fila por instalación, tuit
  y versión de modelo: volver a pedir el mismo tuit actualiza la fila y su
  fecha, en lugar de duplicarla.
- `reporte` guarda el informe con la fila de análisis, la instalación y la
  versión de modelo que produjo el veredicto informado, que es lo que CU-04
  pide para distinguir después un error corregido de uno vigente.

No se guarda el texto del tuit: el enlace a la publicación se reconstruye a
partir del identificador nativo, como decide el modelo de datos.

Se omite la tabla `usuario_extension`: su única columna además del UUID es la
fecha de instalación, que el servicio no conoce. El UUID vive como columna.

CU-06 agrega en la misma base las tres tablas de la plataforma para
organizaciones (RF-13): `organizacion` con su cuota mensual, `api_key` con el
prefijo en claro y la clave **solo resumida** (RNF-12), y `consumo_api`, una
fila por llamada aceptada. Se omite `usuario_b2b`: los analistas llegan con
CU-07 y el proveedor de identidad.

CU-07 agrega `cuenta` —el *handle* y su `id_cuenta`, que es el seudónimo del
panel de tendencias (RF-14, RNF-10)— y `tuit`, que vincula el identificador
nativo con su cuenta. El *handle* no sale de la base: las tendencias se
agregan por `id_cuenta`. Se omite `usuario_b2b`: el analista entra con la
clave de su organización.
"""

from __future__ import annotations

import hashlib
import re
import secrets
import sqlite3
import threading
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any

from .configuracion import obtener_configuracion
from .contrato import RespuestaAnalisis

ESQUEMA = """
CREATE TABLE IF NOT EXISTS analisis (
    id_analisis    INTEGER PRIMARY KEY,
    uuid_usuario   TEXT NOT NULL,
    tweet_id       TEXT NOT NULL,
    version_modelo TEXT NOT NULL,
    fecha_analisis TEXT NOT NULL,
    respuesta      TEXT NOT NULL,
    UNIQUE (uuid_usuario, tweet_id, version_modelo)
);
CREATE TABLE IF NOT EXISTS reporte (
    id_reporte     INTEGER PRIMARY KEY,
    id_analisis    INTEGER NOT NULL REFERENCES analisis (id_analisis),
    uuid           TEXT NOT NULL,
    tipo           TEXT NOT NULL CHECK (tipo IN ('falso_positivo', 'falso_negativo')),
    motivo         TEXT,
    version_modelo TEXT NOT NULL,
    fecha          TEXT NOT NULL,
    UNIQUE (id_analisis, uuid)
);
CREATE TABLE IF NOT EXISTS organizacion (
    id_organizacion INTEGER PRIMARY KEY,
    nombre          TEXT NOT NULL,
    cuota_mensual   INTEGER NOT NULL CHECK (cuota_mensual >= 0),
    fecha_alta      TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS api_key (
    id_api_key       INTEGER PRIMARY KEY,
    id_organizacion  INTEGER NOT NULL REFERENCES organizacion (id_organizacion),
    prefijo          TEXT NOT NULL UNIQUE,
    hash_clave       TEXT NOT NULL UNIQUE,
    fecha_emision    TEXT NOT NULL,
    fecha_revocacion TEXT
);
CREATE TABLE IF NOT EXISTS consumo_api (
    id_consumo      INTEGER PRIMARY KEY,
    id_organizacion INTEGER NOT NULL REFERENCES organizacion (id_organizacion),
    id_api_key      INTEGER NOT NULL REFERENCES api_key (id_api_key),
    fecha           TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS cuenta (
    id_cuenta INTEGER PRIMARY KEY,
    handle    TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS tuit (
    id_nativo TEXT PRIMARY KEY,
    id_cuenta INTEGER NOT NULL REFERENCES cuenta (id_cuenta)
);
"""

VEREDICTOS_MARCADOS = ("contradicho_por_fuentes_oficiales", "informacion_sospechosa")
_MENCION = re.compile(r"@\w+")


def resumir_clave(clave: str) -> str:
    """SHA-256 de la clave (RNF-12). Alcanza sin sal ni estiramiento porque la
    clave la genera el servicio con 256 bits de azar: no hay diccionario que
    probar, a diferencia de una contraseña."""
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()


def _inicio_del_mes(momento: datetime) -> datetime:
    return momento.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _renovacion(momento: datetime) -> str:
    """Primer día del mes siguiente, en UTC: cuando la cuota vuelve a cero."""
    inicio = _inicio_del_mes(momento)
    siguiente = inicio.replace(year=inicio.year + 1, month=1) if inicio.month == 12 \
        else inicio.replace(month=inicio.month + 1)
    return siguiente.date().isoformat()


def _ahora() -> str:
    return datetime.now(timezone.utc).isoformat()


class Historial:
    """Acceso a las dos tablas. `":memory:"` es la base de cada test."""

    def __init__(self, ruta: str) -> None:
        # FastAPI atiende los puntos de entrada síncronos desde varios hilos.
        # ponytail: una conexión y un candado global; alcanza para un prototipo local.
        self._conexion = sqlite3.connect(ruta, check_same_thread=False)
        self._conexion.row_factory = sqlite3.Row
        self._candado = threading.Lock()
        with self._candado:
            self._conexion.executescript(ESQUEMA)

    def registrar_analisis(self, uuid: str, analisis: RespuestaAnalisis, handle: str) -> None:
        with self._candado, self._conexion:
            self._conexion.execute(
                "INSERT OR IGNORE INTO cuenta (handle) VALUES (?)", (handle,)
            )
            self._conexion.execute(
                "INSERT OR IGNORE INTO tuit (id_nativo, id_cuenta) "
                "SELECT ?, id_cuenta FROM cuenta WHERE handle = ?",
                (analisis.tweet_id, handle),
            )
            self._conexion.execute(
                """
                INSERT INTO analisis
                    (uuid_usuario, tweet_id, version_modelo, fecha_analisis, respuesta)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT (uuid_usuario, tweet_id, version_modelo)
                DO UPDATE SET fecha_analisis = excluded.fecha_analisis,
                              respuesta = excluded.respuesta
                """,
                (uuid, analisis.tweet_id, analisis.version_modelo, _ahora(),
                 analisis.model_dump_json()),
            )

    def listar(self, uuid: str) -> list[dict[str, Any]]:
        """Los análisis de la instalación, del más reciente al más viejo."""
        with self._candado:
            filas = self._conexion.execute(
                """
                SELECT a.tweet_id, a.fecha_analisis, a.respuesta,
                       r.tipo AS reporte_tipo, r.motivo AS reporte_motivo
                FROM analisis a
                LEFT JOIN reporte r ON r.id_analisis = a.id_analisis
                WHERE a.uuid_usuario = ?
                ORDER BY a.fecha_analisis DESC, a.id_analisis DESC
                """,
                (uuid,),
            ).fetchall()
        return [
            {
                "tweet_id": fila["tweet_id"],
                "fecha": fila["fecha_analisis"],
                "analisis": RespuestaAnalisis.model_validate_json(fila["respuesta"]),
                "reporte_tipo": fila["reporte_tipo"],
                "reporte_motivo": fila["reporte_motivo"],
            }
            for fila in filas
        ]

    def registrar_reporte(
        self, uuid: str, tweet_id: str, tipo: str, motivo: str
    ) -> dict[str, Any] | None:
        """Registra el informe sobre el último análisis de ese tuit en esa instalación.

        Devuelve `None` si la instalación nunca pidió ese análisis. Un segundo
        informe sobre el mismo análisis no pisa el primero y devuelve el
        registrado, de modo que reenviar sea inofensivo.
        """
        with self._candado, self._conexion:
            analisis = self._conexion.execute(
                """
                SELECT id_analisis, version_modelo FROM analisis
                WHERE uuid_usuario = ? AND tweet_id = ?
                ORDER BY fecha_analisis DESC LIMIT 1
                """,
                (uuid, tweet_id),
            ).fetchone()
            if analisis is None:
                return None
            self._conexion.execute(
                """
                INSERT OR IGNORE INTO reporte
                    (id_analisis, uuid, tipo, motivo, version_modelo, fecha)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (analisis["id_analisis"], uuid, tipo, motivo or None,
                 analisis["version_modelo"], _ahora()),
            )
            fila = self._conexion.execute(
                "SELECT * FROM reporte WHERE id_analisis = ? AND uuid = ?",
                (analisis["id_analisis"], uuid),
            ).fetchone()
        return {**dict(fila), "tweet_id": tweet_id}

    # --- Organizaciones cliente (RF-13) -------------------------------------

    def alta_organizacion(self, nombre: str, cuota_mensual: int) -> dict[str, Any]:
        with self._candado, self._conexion:
            cursor = self._conexion.execute(
                "INSERT INTO organizacion (nombre, cuota_mensual, fecha_alta) VALUES (?, ?, ?)",
                (nombre, cuota_mensual, _ahora()),
            )
        return {"id_organizacion": cursor.lastrowid, "nombre": nombre,
                "cuota_mensual": cuota_mensual}

    def emitir_clave(self, id_organizacion: int) -> dict[str, str] | None:
        """Genera una clave y guarda solo su prefijo y su resumen. La clave en
        claro se devuelve acá y nunca más. `None` si la organización no existe."""
        prefijo = "pfi_" + secrets.token_hex(4)
        clave = f"{prefijo}_{secrets.token_urlsafe(32)}"
        with self._candado, self._conexion:
            if self._conexion.execute(
                "SELECT 1 FROM organizacion WHERE id_organizacion = ?", (id_organizacion,)
            ).fetchone() is None:
                return None
            self._conexion.execute(
                "INSERT INTO api_key (id_organizacion, prefijo, hash_clave, fecha_emision) "
                "VALUES (?, ?, ?, ?)",
                (id_organizacion, prefijo, resumir_clave(clave), _ahora()),
            )
        return {"prefijo": prefijo, "clave": clave}

    def revocar_clave(self, id_organizacion: int, prefijo: str) -> bool:
        with self._candado, self._conexion:
            cursor = self._conexion.execute(
                "UPDATE api_key SET fecha_revocacion = ? "
                "WHERE id_organizacion = ? AND prefijo = ? AND fecha_revocacion IS NULL",
                (_ahora(), id_organizacion, prefijo),
            )
        return cursor.rowcount == 1

    def clave_activa(self, clave: str) -> dict[str, Any] | None:
        """La clave activa y su organización, o `None` si es inválida o fue revocada."""
        with self._candado:
            fila = self._conexion.execute(
                """
                SELECT k.id_api_key, o.id_organizacion, o.nombre, o.cuota_mensual
                FROM api_key k JOIN organizacion o USING (id_organizacion)
                WHERE k.hash_clave = ? AND k.fecha_revocacion IS NULL
                """,
                (resumir_clave(clave),),
            ).fetchone()
        return dict(fila) if fila else None

    def consumo(self, id_organizacion: int, cuota_mensual: int) -> dict[str, Any]:
        """Llamadas del mes calendario en curso (UTC) contra la cuota."""
        ahora = datetime.now(timezone.utc)
        with self._candado:
            (usado,) = self._conexion.execute(
                "SELECT COUNT(*) FROM consumo_api WHERE id_organizacion = ? AND fecha >= ?",
                (id_organizacion, _inicio_del_mes(ahora).isoformat()),
            ).fetchone()
        return {"cuota_mensual": cuota_mensual, "consumo_del_mes": usado,
                "renovacion": _renovacion(ahora)}

    def registrar_consumo(self, id_organizacion: int, id_api_key: int) -> None:
        with self._candado, self._conexion:
            self._conexion.execute(
                "INSERT INTO consumo_api (id_organizacion, id_api_key, fecha) VALUES (?, ?, ?)",
                (id_organizacion, id_api_key, _ahora()),
            )

    # --- Panel de tendencias (RF-14, CU-07) ----------------------------------

    def tendencias(self, desde: str, hasta: str) -> dict[str, list[tuple[str, int, int]]]:
        """Publicaciones y marcadas por tema, por día y por cuenta seudonimizada,
        entre dos fechas ISO inclusive. Cada publicación cuenta una vez, con su
        análisis más reciente, aunque la hayan pedido varias instalaciones.

        El tema es la afirmación extraída, normalizada: el modelo de datos no
        tiene entidad `tema` y lo resuelve agregando los *claims* del período."""
        with self._candado:
            filas = self._conexion.execute(
                """
                SELECT a.tweet_id, a.fecha_analisis, a.respuesta, t.id_cuenta
                FROM analisis a LEFT JOIN tuit t ON t.id_nativo = a.tweet_id
                WHERE substr(a.fecha_analisis, 1, 10) BETWEEN ? AND ?
                ORDER BY a.fecha_analisis
                """,
                (desde, hasta),
            ).fetchall()
        # ponytail: se agrega en memoria; con volumen real va a SQL sobre columnas normalizadas.
        ultimas = {fila["tweet_id"]: fila for fila in filas}
        conteos: dict[str, dict[str, list[int]]] = {"tema": {}, "dia": {}, "cuenta": {}}
        for fila in ultimas.values():
            analisis = RespuestaAnalisis.model_validate_json(fila["respuesta"])
            marcada = int(analisis.veredicto.value in VEREDICTOS_MARCADOS)
            claves = {
                # La afirmación puede nombrar cuentas: no salen en claro (RF-15).
                "tema": " ".join(_MENCION.sub("@usuario", analisis.afirmacion).casefold().split()),
                "dia": fila["fecha_analisis"][:10],
                "cuenta": f"cuenta-{fila['id_cuenta']}" if fila["id_cuenta"] else "",
            }
            for seccion, clave in claves.items():
                if clave:
                    total = conteos[seccion].setdefault(clave, [0, 0])
                    total[0] += 1
                    total[1] += marcada
        # Los días en orden cronológico; temas y cuentas, los diez de mayor
        # volumen marcado y, a igualdad, de mayor volumen analizado.
        return {
            seccion: sorted(
                ((clave, p, m) for clave, (p, m) in conteo.items()),
                key=(lambda f: f[0]) if seccion == "dia" else (lambda f: (-f[2], -f[1], f[0])),
            )[: None if seccion == "dia" else 10]
            for seccion, conteo in conteos.items()
        }


@lru_cache
def obtener_historial() -> Historial:
    """El histórico del proceso, en `RUTA_BASE_DE_DATOS`. Los tests lo sustituyen."""
    return Historial(obtener_configuracion().ruta_base_de_datos)
