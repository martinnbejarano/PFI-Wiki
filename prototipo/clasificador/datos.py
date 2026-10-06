"""Preparación de datos del clasificador del Módulo 1 (ticket #29, *spec* #28).

Deja LIAR, FakeNewsNet y FakeDeS en un único esquema:

    dataset | id | texto | etiqueta ("verdadero" / "falso") | particion

`particion` toma "entrenamiento", "validacion" o "prueba". LIAR y FakeDeS traen
particiones oficiales y se respetan; FakeNewsNet no, y se parte de forma
estratificada con semilla fija (80/10/10).

El texto se guarda **crudo**. `preprocesar` se aplica dentro del modelo, para
que entrenamiento e inferencia vean exactamente el mismo texto.
"""

from __future__ import annotations

import gzip
import hashlib
import re
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

FUENTES = {
    "liar.zip": "https://www.cs.ucsb.edu/~william/data/liar_dataset.zip",
    **{
        f"{nombre}.csv": f"https://raw.githubusercontent.com/KaiDMML/FakeNewsNet/master/dataset/{nombre}.csv"
        for nombre in ("politifact_fake", "politifact_real", "gossipcop_fake", "gossipcop_real")
    },
    # FakeDeS (IberLEF 2021): train + development son la versión 1.0 del corpus
    # (971 noticias); test.xlsx es el conjunto de prueba de la versión 2.0.
    **{
        f"fakedes_{nombre}.xlsx": f"https://raw.githubusercontent.com/jpposadas/FakeNewsCorpusSpanish/master/{nombre}.xlsx"
        for nombre in ("train", "development", "test")
    },
}

# Tabla de mapeo del capítulo 4 (`tab:mapeo-etiquetas`), a dos clases.
MAPEO_LIAR = {
    "pants-fire": "falso",
    "false": "falso",
    "barely-true": "falso",
    "half-true": "verdadero",
    "mostly-true": "verdadero",
    "true": "verdadero",
}

PARTICIONES = ("entrenamiento", "validacion", "prueba")


def etiqueta_liar(categoria: str) -> str:
    return MAPEO_LIAR[categoria]


def preprocesar(texto: str) -> str:
    """El *pipeline* de `wiki/solucion/pipeline-preprocesamiento.md`.

    Conserva números, emojis, mayúsculas y signos repetidos: son la señal.
    """
    texto = re.sub(r"https?://\S+|www\.\S+", "http", texto)
    texto = re.sub(r"@\w+", "@usuario", texto)
    texto = re.sub(r"#(\w+)", r"\1", texto)
    texto = texto.translate(str.maketrans("“”«»‘’", "\"\"\"\"''"))
    return re.sub(r"\s+", " ", texto).strip()


def descargar(carpeta: str | Path) -> Path:
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    for nombre, url in FUENTES.items():
        if not (carpeta / nombre).exists():
            urllib.request.urlretrieve(url, carpeta / nombre)
    with zipfile.ZipFile(carpeta / "liar.zip") as zip_liar:
        zip_liar.extractall(carpeta / "liar")
    return carpeta


def cargar_liar(carpeta: str | Path) -> pd.DataFrame:
    partes = []
    for archivo, particion in (("train", "entrenamiento"), ("valid", "validacion"), ("test", "prueba")):
        # Sin comillas: el TSV de LIAR trae comillas sueltas dentro de las afirmaciones.
        crudo = pd.read_csv(Path(carpeta) / "liar" / f"{archivo}.tsv", sep="\t", header=None, quoting=3)
        partes.append(
            pd.DataFrame(
                {"id": crudo[0], "texto": crudo[2], "etiqueta": crudo[1].map(etiqueta_liar), "particion": particion}
            )
        )
    return pd.concat(partes).assign(dataset="liar")


def cargar_fakenewsnet(carpeta: str | Path) -> pd.DataFrame:
    """El CSV mínimo de FakeNewsNet trae solo el título: ese es el texto."""
    partes = []
    for fuente in ("politifact", "gossipcop"):
        for sufijo, etiqueta in (("fake", "falso"), ("real", "verdadero")):
            crudo = pd.read_csv(Path(carpeta) / f"{fuente}_{sufijo}.csv")
            partes.append(pd.DataFrame({"id": crudo["id"], "texto": crudo["title"], "etiqueta": etiqueta}))
    return pd.concat(partes).assign(dataset="fakenewsnet", particion=None)


def cargar_fakedes(carpeta: str | Path) -> pd.DataFrame:
    partes = []
    for archivo, particion in (("train", "entrenamiento"), ("development", "validacion"), ("test", "prueba")):
        crudo = pd.read_excel(Path(carpeta) / f"fakedes_{archivo}.xlsx")
        crudo.columns = crudo.columns.str.lower()  # test.xlsx trae las columnas en mayúscula
        # train/development usan "True"/"Fake"; test.xlsx, booleanos (False = falsa).
        etiqueta = crudo["category"].astype(str).str.lower().map({"true": "verdadero", "fake": "falso", "false": "falso"})
        titular = crudo["headline"].fillna("").astype(str)
        partes.append(
            pd.DataFrame(
                {
                    "id": f"{archivo}-" + crudo["id"].astype(str),
                    "texto": (titular + "\n" + crudo["text"].astype(str)).str.strip(),
                    "etiqueta": etiqueta,
                    "particion": particion,
                }
            )
        )
    return pd.concat(partes).assign(dataset="fakedes")


AFIRMACIONES_CHEQUEADO = Path(__file__).parent / "datos/corpus_argentino/afirmaciones_chequeado.csv"


def cargar_chequeado(ruta: str | Path = AFIRMACIONES_CHEQUEADO) -> pd.DataFrame:
    """Afirmaciones calificadas por Chequeado (entrenamiento y validación, sin prueba).

    Las arma `recolectar_chequeado.py afirmaciones`, con su propia partición 85/15. Queda
    fuera de `cargar_todos` para no mover `particiones.csv.gz`: la prueba es el corpus argentino.
    """
    crudo = pd.read_csv(ruta, dtype=str)
    return crudo[["id", "texto", "etiqueta", "particion"]].assign(dataset="chequeado")


def cargar_todos(carpeta: str | Path) -> pd.DataFrame:
    return pd.concat([cargar_liar(carpeta), cargar_fakenewsnet(carpeta), cargar_fakedes(carpeta)], ignore_index=True)


def deduplicar(datos: pd.DataFrame) -> pd.DataFrame:
    """Un ejemplo por identificador y por texto normalizado, en todo el corpus.

    Ante un repetido sobrevive la copia de la partición más restrictiva
    (prueba > validación > entrenamiento > sin partición): el conjunto de prueba
    oficial no pierde ejemplos y ninguno de sus textos queda en entrenamiento.
    """
    # ponytail: ante etiquetas en conflicto también gana la copia de prueba; descartar el par si aparecen muchos.
    datos = datos.dropna(subset=["texto", "etiqueta"])
    datos = datos[datos["texto"].astype(str).str.strip() != ""]
    prioridad = datos["particion"].map({"prueba": 0, "validacion": 1, "entrenamiento": 2}).fillna(3)
    normalizado = datos["texto"].astype(str).map(lambda t: preprocesar(t).casefold())
    datos = datos.assign(_prioridad=prioridad, _normalizado=normalizado).sort_values(
        ["_prioridad", "dataset", "id"], kind="stable"
    )
    datos = datos.drop_duplicates(["dataset", "id"]).drop_duplicates("_normalizado")
    return datos.drop(columns=["_prioridad", "_normalizado"])


def particionar(datos: pd.DataFrame, semilla: int) -> pd.DataFrame:
    """Asigna 80/10/10 estratificado a lo que no trae partición oficial."""
    datos = datos.sort_values(["dataset", "id"]).reset_index(drop=True)  # el orden de entrada no influye
    sin_particion = datos[datos["particion"].isna()]
    for _, grupo in sin_particion.groupby("dataset"):
        entrenamiento, resto = train_test_split(
            grupo.index, test_size=0.2, stratify=grupo["etiqueta"], random_state=semilla
        )
        validacion, prueba = train_test_split(
            resto, test_size=0.5, stratify=grupo.loc[resto, "etiqueta"], random_state=semilla
        )
        datos.loc[entrenamiento, "particion"] = "entrenamiento"
        datos.loc[validacion, "particion"] = "validacion"
        datos.loc[prueba, "particion"] = "prueba"
    return datos


def preparar(datos: pd.DataFrame, semilla: int) -> pd.DataFrame:
    return particionar(deduplicar(datos), semilla)


def congelar(datos: pd.DataFrame, ruta: str | Path) -> str:
    """Guarda qué ejemplo va a qué partición y devuelve su huella SHA-256.

    Si el archivo ya existe y no coincide, falla: las fuentes cambiaron y los
    resultados dejarían de ser comparables.
    """
    ruta = Path(ruta)
    tabla = datos[["dataset", "id", "etiqueta", "particion"]].astype(str).sort_values(["dataset", "id"])
    contenido = tabla.to_csv(index=False, lineterminator="\n")
    huella = hashlib.sha256(contenido.encode()).hexdigest()
    if ruta.exists():
        congelado = gzip.decompress(ruta.read_bytes()).decode()
        if congelado != contenido:
            raise ValueError(f"Las particiones no coinciden con {ruta}: revisar las fuentes descargadas.")
    else:
        ruta.write_bytes(gzip.compress(contenido.encode(), mtime=0))
    return huella
