"""LLM *zero-shot* del prototipo sobre las mismas particiones (ticket #34, *spec* #28).

Mismo modelo, esfuerzo, tope de fichas e instrucción de puntaje que
`prototipo/servicio/app/proveedor/openai.py` (copiados el 2026-09-28), con la
instrucción adaptada a dos clases. El puntaje que devuelve el LLM es la
probabilidad de «falso»; el umbral puntaje → clase se elige maximizando F1 macro
en la validación de FakeDeS y se aplica sin cambios a las pruebas.

Uso, desde esta carpeta, con `OPENAI_API_KEY` en el entorno o en `../servicio/.env`:

    .venv/bin/python llm_zero_shot.py --limite 5          # prueba de humo
    .venv/bin/python llm_zero_shot.py                      # validación + prueba de FakeDeS
    .venv/bin/python llm_zero_shot.py --argentino datos/corpus_argentino/candidatos.csv

Las respuestas quedan en `cache_llm/` (fuera de git): repetir una corrida no se
vuelve a pagar, y el costo y la latencia del JSON son los de la llamada original.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from pathlib import Path

import pandas as pd
from pydantic import BaseModel

from datos import cargar_fakedes
from resultados import construir_resultado, guardar, metricas

MODELO = "gpt-5.6-luna"
ESFUERZO = "low"
MAX_FICHAS = 900
# Dólares por millón de fichas (entrada, entrada en caché, salida) de gpt-5.6-luna,
# contexto corto. Fuente: https://developers.openai.com/api/docs/pricing (consultada 2026-09-28).
PRECIO_ENTRADA, PRECIO_ENTRADA_CACHE, PRECIO_SALIDA = 0.20, 0.02, 1.20
HASH_PARTICIONES = "ec1895196bff859f0bc311f275be97fb61afb2d8e1779987d8a74cb020a88c65"
CACHE = Path("cache_llm")

# `INSTRUCCIONES_EXTRACCION` del servicio, adaptada a dos clases: se quita
# `sin_verificar` (puntos 2 y 5) y el resto queda igual.
INSTRUCCIONES = """\
Sos el módulo de extracción y clasificación de un sistema de detección de \
desinformación en publicaciones de la red social X, orientado al contexto \
argentino.

Recibís el texto de una publicación. Tenés que devolver cuatro cosas: la \
afirmación verificable que contiene, su tipo, un puntaje y una clase.

1. **La afirmación.** Es el hecho contrastable que la publicación sostiene, \
reescrito como un enunciado autónomo, en una sola oración, entendible sin \
haber leído el tuit. Sacá los emojis, los hashtags, las mayúsculas de grito y \
las apelaciones a compartir. No agregues ningún dato que el texto no diga: si \
la publicación no aclara la fecha, el lugar ni el organismo, la afirmación \
tampoco los aclara. Si la publicación sostiene varias, quedate con la más \
verificable y la más central.

2. **Cuando no hay ninguna afirmación verificable**, devolvé `afirmacion` como \
cadena vacía y `tipo` en `otro`. El puntaje y la clase se asignan igual, \
según el texto.

3. **El tipo.** Uno de estos cinco, exactamente: `normativa` para leyes, \
decretos, resoluciones y medidas de gobierno; `dato_economico` para \
inflación, precios, tipo de cambio, empleo, salarios y estadísticas \
oficiales; `salud` para enfermedades, vacunas, tratamientos y sistema \
sanitario; `educacion` para escuelas, universidades, docentes y calendario \
escolar; `otro` para todo lo demás.

4. **El puntaje.** Un número entre 0 y 1 que estima qué tan probable es que la \
publicación sea desinformación, juzgada **únicamente por su texto** y sin \
ninguna evidencia externa. Suben el puntaje el lenguaje de urgencia y de \
alarma, las mayúsculas de grito, las afirmaciones absolutas sin fuente citada, \
la apelación a compartir antes de que \"lo bajen\", la atribución a fuentes \
anónimas y la incoherencia interna. Lo bajan el tono descriptivo, la mención \
de la fuente y el enunciado acotado. No uses lo que sepas del mundo para \
decidir si el hecho ocurrió: eso lo resuelve el módulo de contraste con \
fuentes, no vos.

5. **La clase.** `falso` si el texto tiene señales de desinformación y \
`verdadero` si se lee como una descripción sobria de un hecho. Elegí siempre \
una de las dos.

Escribí la afirmación en castellano rioplatense, sin tecnicismos.
"""


class Tipo(str, Enum):
    NORMATIVA = "normativa"
    DATO_ECONOMICO = "dato_economico"
    SALUD = "salud"
    EDUCACION = "educacion"
    OTRO = "otro"


class Clase(str, Enum):
    VERDADERO = "verdadero"
    FALSO = "falso"


class Salida(BaseModel):
    afirmacion: str
    tipo: Tipo
    puntaje: float
    clase: Clase


def cliente():
    from openai import OpenAI

    clave = os.environ.get("OPENAI_API_KEY")
    env = Path(__file__).parent.parent / "servicio" / ".env"
    if not clave and env.exists():
        clave = next((l.split("=", 1)[1].strip() for l in env.read_text().splitlines() if l.startswith("OPENAI_API_KEY=")), None)
    # max_retries: el SDK reintenta con espera exponencial ante 429, 5xx y cortes de red.
    return OpenAI(api_key=clave, timeout=60, max_retries=6)


def consultar(api, texto: str) -> dict:
    """Una respuesta por texto, cacheada en disco por modelo + instrucción + texto."""
    clave = hashlib.sha256(json.dumps([MODELO, ESFUERZO, MAX_FICHAS, INSTRUCCIONES, texto]).encode()).hexdigest()
    ruta = CACHE / f"{clave}.json"
    if ruta.exists():
        return json.loads(ruta.read_text())
    for intento in range(3):  # salida que no se ajusta al esquema: se reintenta
        comenzo = time.perf_counter()
        respuesta = api.responses.parse(
            model=MODELO,
            instructions=INSTRUCCIONES,
            input=f"Publicación analizada:\n{texto}",
            text_format=Salida,
            max_output_tokens=MAX_FICHAS,
            reasoning={"effort": ESFUERZO},
        )
        latencia = time.perf_counter() - comenzo
        if respuesta.output_parsed is not None:
            break
    else:
        raise RuntimeError(f"Salida fuera de esquema tras 3 intentos (estado: {respuesta.status}): {texto[:80]!r}")
    uso = respuesta.usage
    en_cache = uso.input_tokens_details.cached_tokens or 0
    registro = {
        **respuesta.output_parsed.model_dump(mode="json"),
        "puntaje": min(max(respuesta.output_parsed.puntaje, 0.0), 1.0),
        "fichas_entrada": uso.input_tokens,
        "fichas_entrada_cache": en_cache,
        "fichas_salida": uso.output_tokens,
        "costo_usd": ((uso.input_tokens - en_cache) * PRECIO_ENTRADA + en_cache * PRECIO_ENTRADA_CACHE + uso.output_tokens * PRECIO_SALIDA) / 1e6,
        "latencia_s": latencia,
    }
    CACHE.mkdir(exist_ok=True)
    ruta.write_text(json.dumps(registro, ensure_ascii=False))
    return registro


def mejor_umbral(etiquetas: list[str], puntajes: list[float]) -> float:
    """El umbral (entre los puntajes observados) de mayor F1 macro; ante empate, el menor."""
    return max(sorted(set(puntajes)), key=lambda u: metricas(etiquetas, puntajes, u)["f1_macro"])


def conjuntos(argentino: str | None, limite: int | None) -> dict[str, pd.DataFrame]:
    congeladas = pd.read_csv("particiones.csv.gz").query("dataset == 'fakedes'")
    fakedes = cargar_fakedes("datos").drop(columns="particion").merge(congeladas[["id", "particion"]], on="id")
    salida = {f"fakedes/{p}": fakedes[fakedes["particion"] == p] for p in ("validacion", "prueba")}
    if argentino:
        # Planilla de `wiki/datasets/guia-etiquetado-corpus-argentino.md`: vale la etiqueta del autor.
        corpus = pd.read_csv(argentino).rename(columns={"etiqueta_confirmada": "etiqueta"})
        salida["argentino/prueba"] = corpus[corpus["etiqueta"].isin(["verdadero", "falso"])]
    return {k: (v.head(limite) if limite else v)[["texto", "etiqueta"]] for k, v in salida.items()}


def main() -> None:
    argumentos = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    argumentos.add_argument("--argentino", help="CSV del corpus argentino (texto, etiqueta_confirmada)")
    argumentos.add_argument("--limite", type=int, help="solo los primeros N de cada conjunto (prueba de humo; no guarda JSON)")
    argumentos.add_argument("--hilos", type=int, default=8)
    opciones = argumentos.parse_args()

    api = cliente()
    respuestas = {}
    with ThreadPoolExecutor(opciones.hilos) as grupo:
        for nombre, datos in conjuntos(opciones.argentino, opciones.limite).items():
            respuestas[nombre] = (datos["etiqueta"].tolist(), list(grupo.map(lambda t: consultar(api, t), datos["texto"])))
            print(nombre, len(datos), "ejemplos")

    etiquetas, filas = respuestas["fakedes/validacion"]
    umbral = mejor_umbral(etiquetas, [f["puntaje"] for f in filas])
    evaluaciones = {}
    for nombre, (etiquetas, filas) in respuestas.items():
        evaluaciones[nombre] = {
            **metricas(etiquetas, [f["puntaje"] for f in filas], umbral),
            "costo_usd": sum(f["costo_usd"] for f in filas),
            "latencia_media_s": sum(f["latencia_s"] for f in filas) / len(filas),
            # Acuerdo entre la clase que el LLM eligió y la que sale del umbral.
            "acuerdo_clase_llm": sum((f["puntaje"] >= umbral) == (f["clase"] == "falso") for f in filas) / len(filas),
        }
        print(nombre, {k: round(evaluaciones[nombre][k], 4) for k in ("f1_macro", "auc_roc", "costo_usd", "latencia_media_s")})
    todas = [f for _, filas in respuestas.values() for f in filas]
    consumo = {"costo_usd": sum(f["costo_usd"] for f in todas), "latencia_media_s": sum(f["latencia_s"] for f in todas) / len(todas), "n": len(todas)}
    print("umbral", umbral, "consumo", consumo)
    if opciones.limite:
        return

    resultado = construir_resultado(
        id_corrida=f"llm-zero-shot_{MODELO}",
        modelo="llm-zero-shot",
        entrenado_en="ninguno",
        hiperparametros={
            "proveedor": "openai",
            "modelo": MODELO,
            "esfuerzo_de_razonamiento": ESFUERZO,
            "max_output_tokens": MAX_FICHAS,
            "instrucciones": INSTRUCCIONES,
            "umbral_elegido_en": "fakedes/validacion (máximo F1 macro)",
            "precios_usd_por_millon": {"entrada": PRECIO_ENTRADA, "entrada_cache": PRECIO_ENTRADA_CACHE, "salida": PRECIO_SALIDA},
            "hilos": opciones.hilos,
        },
        evaluaciones=evaluaciones,
        semilla=None,  # el LLM no admite semilla
        hash_particiones=HASH_PARTICIONES,
        consumo=consumo,
    )
    print(guardar(resultado, "resultados"))


if __name__ == "__main__":
    main()
