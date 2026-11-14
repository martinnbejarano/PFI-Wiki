"""Una base PostgreSQL descartable para que una medición no deje rastros en la real.

`CREATE DATABASE ... TEMPLATE` copia la base entera (con el índice) en el servidor;
sin plantilla, la base arranca vacía y el servicio crea su esquema al abrirla. Se
borra al salir con `WITH (FORCE)`, que corta las conexiones que hayan quedado
abiertas. La plantilla no puede tener otras sesiones: con el servicio de
desarrollo andando sobre ella, `CREATE DATABASE` falla.
"""
import uuid
from contextlib import contextmanager

import psycopg
from psycopg.conninfo import conninfo_to_dict, make_conninfo


@contextmanager
def base_temporal(url: str, copiar: bool = False):
    nombre = "medicion_" + uuid.uuid4().hex[:8]
    administracion = make_conninfo(url, dbname="postgres")
    plantilla = f' TEMPLATE "{conninfo_to_dict(url)["dbname"]}"' if copiar else ""
    with psycopg.connect(administracion, autocommit=True) as c:
        c.execute(f'CREATE DATABASE "{nombre}"{plantilla}')
    try:
        yield make_conninfo(url, dbname=nombre)
    finally:
        with psycopg.connect(administracion, autocommit=True) as c:
            c.execute(f'DROP DATABASE "{nombre}" WITH (FORCE)')


def sin_clave(url: str) -> str:
    """`host:puerto/base`, para imprimir en una medición sin la contraseña."""
    partes = conninfo_to_dict(url)
    return f"{partes.get('host')}:{partes.get('port', 5432)}/{partes.get('dbname')}"
