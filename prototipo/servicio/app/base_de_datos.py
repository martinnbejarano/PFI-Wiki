"""La base del servicio: PostgreSQL con la extensión `pgvector` (#121).

Histórico, memoria de evidencia e índice de fuentes oficiales viven en la misma
base, la de `DATABASE_URL`, y comparten un *pool* de conexiones por proceso. El
*pool* es lo que permite atender las peticiones desde los hilos de FastAPI sin
un candado global y reponer una conexión que el servidor cortó.

Cada módulo trae su esquema y lo crea al arrancar con `CREATE ... IF NOT
EXISTS`: no hay herramienta de migraciones. Un bloque `with
pool.connection()` es una transacción: confirma al salir y deshace si hubo una
excepción, igual que el `with conexion:` de SQLite que reemplaza.
"""

from __future__ import annotations

import atexit
import json
from functools import lru_cache

import psycopg
from psycopg_pool import ConnectionPool


def abrir(url: str, esquema: str) -> ConnectionPool:
    """Crea el esquema si falta y devuelve el *pool* del proceso para esa base.

    El esquema va por una conexión directa con tiempo límite, para que una base
    caída falle acá con `psycopg.Error` y no al primer pedido."""
    with psycopg.connect(url, connect_timeout=5) as conexion:
        conexion.execute(esquema)
    return _pool(url)


@lru_cache
def _pool(url: str) -> ConnectionPool:
    pool = ConnectionPool(
        url, min_size=1, max_size=8, check=ConnectionPool.check_connection, open=True
    )
    # Sin cerrarlo, el intérprete espera a sus hilos varios segundos al salir.
    atexit.register(pool.close)
    return pool


def vector(valores: list[float]) -> str:
    """El literal de `pgvector`, `[0.1,0.2,...]`. Se manda como texto y se
    convierte en la consulta (`%s::vector`): el servicio nunca lee vectores."""
    return json.dumps(valores)
