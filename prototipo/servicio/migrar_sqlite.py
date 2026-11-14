"""Copia una base SQLite del prototipo (anterior a #121) a la PostgreSQL de `DATABASE_URL`.

Uso, desde `prototipo/` (lo arma `make migrar-sqlite SQLITE=ruta.sqlite3`):

    servicio/.venv/bin/python servicio/migrar_sqlite.py RUTA.sqlite3

Copia las tablas que existan en el archivo —histórico, organizaciones, memoria
de evidencia, índice de fuentes oficiales— conservando los identificadores, y
los vectores de `sqlite-vec` pasan a la columna `embedding` de `pgvector`. Una
fila que ya está en la base (misma clave) se saltea, así que correrlo dos veces
no duplica nada. `sqlite-vec` no es dependencia del servicio: el target lo
agrega solo para esta corrida.
"""

from __future__ import annotations

import sqlite3
import sys

import psycopg
import sqlite_vec

from app.configuracion import obtener_configuracion
from app.historial import ESQUEMA as ESQUEMA_HISTORIAL
from app.proveedor.indice import ESQUEMA as ESQUEMA_INDICE
from app.proveedor.memoria import ESQUEMA as ESQUEMA_MEMORIA

# En orden de claves foráneas. SQLite no las hacía cumplir, así que una fila
# huérfana (un reporte sin su análisis) se deja afuera. Las tablas con vector
# traen el suyo en JSON, que es el literal que acepta `pgvector`.
TABLAS = {
    "analisis": "SELECT * FROM analisis",
    "reporte": "SELECT * FROM reporte WHERE id_analisis IN (SELECT id_analisis FROM analisis)",
    "organizacion": "SELECT * FROM organizacion",
    "api_key": "SELECT * FROM api_key "
    "WHERE id_organizacion IN (SELECT id_organizacion FROM organizacion)",
    "consumo_api": "SELECT * FROM consumo_api WHERE id_api_key IN (SELECT id_api_key FROM api_key) "
    "AND id_organizacion IN (SELECT id_organizacion FROM organizacion)",
    "cuenta": "SELECT * FROM cuenta",
    "tuit": "SELECT * FROM tuit WHERE id_cuenta IN (SELECT id_cuenta FROM cuenta)",
    "analisis_nuevo": "SELECT * FROM analisis_nuevo",
    "memoria_evidencia": "SELECT m.*, vec_to_json(v.embedding) AS embedding "
    "FROM memoria_evidencia m JOIN memoria_vector v ON v.rowid = m.id",
    "fuente_oficial": "SELECT * FROM fuente_oficial",
    "documento": "SELECT d.*, vec_to_json(v.embedding) AS embedding "
    "FROM documento d JOIN documento_vector v ON v.rowid = d.id",
}


def migrar(ruta: str, url: str) -> None:
    origen = sqlite3.connect(f"file:{ruta}?mode=ro", uri=True)
    origen.enable_load_extension(True)
    sqlite_vec.load(origen)
    existentes = {f[0] for f in origen.execute("SELECT name FROM sqlite_master")}
    with psycopg.connect(url) as destino:
        for esquema in (ESQUEMA_HISTORIAL, ESQUEMA_MEMORIA, ESQUEMA_INDICE):
            destino.execute(esquema)
        for tabla, consulta in TABLAS.items():
            if tabla not in existentes:
                continue
            cursor = origen.execute(consulta)
            columnas = [d[0] for d in cursor.description]
            filas = cursor.fetchall()
            insertadas = 0
            if filas:
                with destino.cursor() as escritura:
                    escritura.executemany(
                        f"INSERT INTO {tabla} ({', '.join(columnas)}) "
                        f"VALUES ({', '.join(['%s'] * len(columnas))}) ON CONFLICT DO NOTHING",
                        filas,
                    )
                    insertadas = escritura.rowcount
            # Las filas llegan con su identificador: la secuencia sigue desde el mayor.
            identidad = destino.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = %s AND is_identity = 'YES'",
                (tabla,),
            ).fetchone()
            if identidad:
                columna = identidad[0]
                destino.execute(
                    f"SELECT setval(pg_get_serial_sequence('{tabla}', '{columna}'), "
                    f"COALESCE((SELECT MAX({columna}) FROM {tabla}), 0) + 1, false)"
                )
            (total,) = origen.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()
            print(f"{tabla}: {total} en SQLite, {total - len(filas)} huérfanas, "
                  f"{insertadas} nuevas en PostgreSQL")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    migrar(sys.argv[1], obtener_configuracion().database_url)
