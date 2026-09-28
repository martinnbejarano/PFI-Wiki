# Clasificador del Módulo 1

Clasificador binario propio (verdadero / falso). Contexto: *spec* [#28](https://github.com/martinnbejarano/PFI-Wiki/issues/28),
ticket [#29](https://github.com/martinnbejarano/PFI-Wiki/issues/29). Tiene sus propias
dependencias; el servicio no las hereda.

| Archivo | Qué es |
|---|---|
| `datos.py` | Descarga, carga a un esquema único, mapeo de etiquetas, preprocesamiento, deduplicación, partición y congelado |
| `resultados.py` | Formato del JSON de resultados (`metricas`, `construir_resultado`, `guardar`) |
| `linea_base.ipynb` | Notebook de Colab: datos + TF-IDF + regresión logística |
| `particiones.csv.gz` | Particiones congeladas (versionadas) |
| `resultados/` | Un JSON por corrida (versionados) |
| `modelos/`, `datos/` | Modelos exportados y descargas (no se versionan) |

## Pruebas

```bash
cd prototipo/clasificador
python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

## Datos

| Dataset | Fuente | Texto | Etiqueta | Partición |
|---|---|---|---|---|
| LIAR | `sites.cs.ucsb.edu/~william/data/liar_dataset.zip` | afirmación | 6 niveles → 2 (tabla del cap. 4) | oficial (train/valid/test) |
| FakeNewsNet | CSV mínimo de `KaiDMML/FakeNewsNet` (PolitiFact + GossipCop) | solo el título | binaria de origen | propia: 80/10/10 estratificada, semilla 42 |
| FakeDeS | `jpposadas/FakeNewsCorpusSpanish` | titular + cuerpo | binaria de origen | oficial IberLEF 2021 (train / development / test) |

Se deduplica por identificador y por texto normalizado sobre todo el corpus; ante un
repetido sobrevive la copia de prueba. Las particiones quedan en `particiones.csv.gz`
(`dataset, id, etiqueta, particion`). Huella SHA-256 del CSV sin comprimir:

```
ec1895196bff859f0bc311f275be97fb61afb2d8e1779987d8a74cb020a88c65
```

`congelar` falla si una corrida nueva no reproduce ese archivo (se verificó igual con
pandas 3.0 / scikit-learn 1.9 y pandas 2.2 / scikit-learn 1.6).

## Formato del JSON de resultados

Uno por corrida (un modelo entrenado), en `resultados/<id_corrida>.json`. El puntaje es
siempre la probabilidad de la clase «falso»; la clase predicha es `puntaje >= umbral`.

```jsonc
{
  "id_corrida": "tfidf-lr_fakedes_s42",   // también es la versión del modelo que devuelve el Space
  "modelo": "tfidf-lr",
  "fecha": "2026-09-28T22:30:45+00:00",
  "entrenado_en": "fakedes",              // fakedes | completo | ...
  "semilla": 42,
  "hash_particiones": "ec18…",            // la huella de arriba
  "clases": ["verdadero", "falso"],       // orden de la matriz de confusión
  "hiperparametros": { … },               // libre, lo que haga falta para reproducir
  "evaluaciones": {                       // clave: "<dataset>/<particion>"
    "fakedes/prueba": {
      "n": 572, "umbral": 0.5, "f1_macro": 0.73, "auc_roc": 0.80,
      "por_clase": {"verdadero": {"precision": …, "exhaustividad": …, "f1": …, "soporte": …}, "falso": {…}},
      "matriz_confusion": [[vv, vf], [fv, ff]]   // filas: real; columnas: predicha
    }
  },
  "epocas": [],                           // opcional: [{"epoca": 1, "perdida_entrenamiento": …, "perdida_validacion": …, "f1_macro_validacion": …}]
  "entorno": {"python": …, "scikit_learn": …, "pandas": …}
}
```

Para otro modelo: `metricas(etiquetas, puntajes)` por cada partición evaluada,
`construir_resultado(...)` y `guardar(resultado, "resultados")`.

## Línea base

`linea_base.ipynb` corre en Colab con *Ejecutar todas* (CPU, un par de minutos) y al final
descarga un `.zip` con `resultados/`, `modelos/` y `particiones.csv.gz`. Localmente, desde
esta carpeta: `jupyter nbconvert --to notebook --execute linea_base.ipynb`.

El modelo exportado (`modelos/<id_corrida>.joblib`) es un `Pipeline` de scikit-learn que
recibe texto crudo: el preprocesamiento va adentro. Para cargarlo, el Space necesita
`datos.py` importable como `datos` y la misma versión de scikit-learn que figura en
`entorno`.
