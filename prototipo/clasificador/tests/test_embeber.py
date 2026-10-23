"""`POST /embeber` del Space (ticket #101): el vector de la memoria de evidencia.

Necesita torch y transformers, que viven en el venv del Space y no en el del
entrenamiento; desde `prototipo/`, tras `make instalar-clasificador`:

    clasificador/space/.venv/bin/python -m pytest -q clasificador/tests/test_embeber.py

La primera corrida baja el modelo de Hugging Face (≈ 470 MB).
"""

from __future__ import annotations

import importlib
import math
import sys
from pathlib import Path

import pytest

pytest.importorskip("transformers")
joblib = pytest.importorskip("joblib")
from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture(scope="module")
def cliente(tmp_path_factory: pytest.TempPathFactory):
    # `app.py` carga el clasificador al importarse; acá no se usa, así que
    # alcanza con un `.joblib` cualquiera.
    nulo = tmp_path_factory.mktemp("modelo") / "nulo"
    joblib.dump(None, f"{nulo}.joblib")
    with pytest.MonkeyPatch.context() as parche:
        parche.setenv("MODELO", str(nulo))
        parche.syspath_prepend(str(Path(__file__).parents[1] / "space"))
        sys.modules.pop("app", None)
        app = importlib.import_module("app")
        yield TestClient(app.app)
        sys.modules.pop("app", None)


def embeber(cliente: TestClient, texto: str) -> list[float]:
    respuesta = cliente.post("/embeber", json={"texto": texto})
    assert respuesta.status_code == 200
    return respuesta.json()["vector"]


def test_devuelve_un_vector_normalizado_de_384_dimensiones(cliente: TestClient) -> None:
    vector = embeber(cliente, "A partir del lunes cierran todas las escuelas de la Provincia.")

    assert len(vector) == 384
    assert math.sqrt(sum(x * x for x in vector)) == pytest.approx(1.0, abs=1e-4)


def test_dos_parafrasis_quedan_mas_cerca_que_dos_textos_no_relacionados(
    cliente: TestClient,
) -> None:
    original = embeber(cliente, "A partir del lunes cierran todas las escuelas de la Provincia.")
    parafrasis = embeber(cliente, "Desde el lunes no habrá clases en ningún colegio bonaerense.")
    ajeno = embeber(cliente, "El dólar blue cerró hoy en alza en la City porteña.")

    def coseno(a: list[float], b: list[float]) -> float:
        return sum(x * y for x, y in zip(a, b))  # ya vienen normalizados

    assert coseno(original, parafrasis) > coseno(original, ajeno)
