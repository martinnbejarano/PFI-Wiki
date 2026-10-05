"""Preparación de datos del clasificador (punto 2 de la *spec* #28).

Se prueba por las funciones públicas de `datos`: qué etiqueta sale, en qué
partición cae cada ejemplo. No cómo se calcula.
"""

from __future__ import annotations

import pandas as pd
import pytest

from datos import etiqueta_liar, preparar, preprocesar

# La tabla de mapeo del capítulo 4 (`tab:mapeo-etiquetas`), a dos clases.
TABLA_LIAR = {
    "pants-fire": "falso",
    "false": "falso",
    "barely-true": "falso",
    "half-true": "verdadero",
    "mostly-true": "verdadero",
    "true": "verdadero",
}


@pytest.mark.parametrize("categoria, clase", TABLA_LIAR.items())
def test_cada_categoria_de_liar_cae_en_la_clase_de_la_tabla(categoria, clase) -> None:
    assert etiqueta_liar(categoria) == clase


def test_una_categoria_desconocida_de_liar_no_se_asigna_en_silencio() -> None:
    with pytest.raises(KeyError):
        etiqueta_liar("unverified")


def test_el_preprocesamiento_conserva_numeros_y_emojis_y_normaliza_urls_y_menciones() -> None:
    texto = "😱 El dólar sube a $5.000!!! @MinEconomia #Argentina https://t.co/xyz"
    assert preprocesar(texto) == "😱 El dólar sube a $5.000!!! @usuario Argentina http"


def _corpus(n: int = 1000, proporcion_falso: float = 0.3) -> pd.DataFrame:
    """Un conjunto sin particiones oficiales, desbalanceado a propósito."""
    n_falso = int(n * proporcion_falso)
    return pd.DataFrame(
        {
            "dataset": "sintetico",
            "id": [f"s{i}" for i in range(n)],
            "texto": [f"publicación número {i}" for i in range(n)],
            "etiqueta": ["falso"] * n_falso + ["verdadero"] * (n - n_falso),
            "particion": None,
        }
    )


def test_ningun_ejemplo_aparece_en_dos_particiones() -> None:
    oficiales = pd.DataFrame(
        {
            "dataset": "oficial",
            "id": ["a", "b", "c"],
            # El mismo texto en prueba y en entrenamiento, con otro formato.
            "texto": ["El dólar a $5000 https://t.co/1", "el  DÓLAR a $5000 http://x.y", "otro"],
            "etiqueta": ["falso", "falso", "verdadero"],
            "particion": ["prueba", "entrenamiento", "entrenamiento"],
        }
    )
    # Y el mismo texto otra vez en un conjunto sin partición oficial, más un id repetido.
    sin_particion = _corpus(50)
    sin_particion.loc[0, "texto"] = "El dólar a $5000 https://otro.link"
    sin_particion.loc[1, "id"] = "s2"

    resultado = preparar(pd.concat([oficiales, sin_particion]), semilla=42)

    normalizado = resultado["texto"].map(lambda t: preprocesar(t).casefold())
    assert not normalizado.duplicated().any()
    assert not resultado.duplicated(["dataset", "id"]).any()
    # La copia que sobrevive es la de prueba: el conjunto de prueba no pierde ejemplos.
    assert resultado.loc[normalizado == "el dólar a $5000 http", "particion"].tolist() == ["prueba"]


def test_se_respetan_las_particiones_oficiales() -> None:
    oficiales = _corpus(30)
    oficiales["particion"] = ["prueba"] * 10 + ["entrenamiento"] * 20
    resultado = preparar(oficiales, semilla=1)
    assert resultado.set_index("id")["particion"].sort_index().equals(oficiales.set_index("id")["particion"].sort_index())


def test_la_misma_semilla_da_la_misma_particion() -> None:
    corpus = _corpus()
    uno = preparar(corpus, semilla=7).set_index("id")["particion"]
    otro = preparar(corpus.sample(frac=1, random_state=3), semilla=7).set_index("id")["particion"]
    assert uno.sort_index().equals(otro.sort_index())
    assert not uno.sort_index().equals(preparar(corpus, semilla=8).set_index("id")["particion"].sort_index())


def test_la_estratificacion_mantiene_la_proporcion_de_clases() -> None:
    resultado = preparar(_corpus(1000, proporcion_falso=0.3), semilla=42)
    proporciones = resultado.groupby("particion")["etiqueta"].apply(lambda e: (e == "falso").mean())
    assert (proporciones - 0.3).abs().max() <= 0.02
