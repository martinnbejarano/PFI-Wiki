# Clasificador del Módulo 1

Clasificador binario propio (verdadero / falso). Contexto: *spec* [#28](https://github.com/martinnbejarano/PFI-Wiki/issues/28),
ticket [#29](https://github.com/martinnbejarano/PFI-Wiki/issues/29). Tiene sus propias
dependencias; el servicio no las hereda.

| Archivo | Qué es |
|---|---|
| `datos.py` | Descarga, carga a un esquema único, mapeo de etiquetas, preprocesamiento, deduplicación, partición y congelado |
| `resultados.py` | Formato del JSON de resultados (`metricas`, `construir_resultado`, `guardar`) |
| `linea_base.ipynb` | Notebook de Colab: datos + TF-IDF + regresión logística |
| `llm_zero_shot.py` | *Script* local: el LLM *zero-shot* del prototipo sobre las mismas particiones |
| `fine_tuning.ipynb` | Notebook de GPU, para Colab o Kaggle (detecta cuál): XLM-T (1 y 2 etapas), RoBERTuito y BETO |
| `figuras/` | Curvas de entrenamiento por corrida, PNG y PDF (versionadas) |
| `particiones.csv.gz` | Particiones congeladas (versionadas) |
| `resultados/` | Un JSON por corrida (versionados) |
| `space/` | Servicio de inferencia (Hugging Face Space, Docker + FastAPI) |
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
| Chequeado | `datos/corpus_argentino/afirmaciones_chequeado.csv` (versionado; lo arma `recolectar_chequeado.py afirmaciones`) | afirmación del título de la nota | calificación de Chequeado → 2 clases (guía del corpus argentino) | propia: 85/15 estratificada, semilla 42, sin prueba |

Chequeado no entra en `cargar_todos` ni en `particiones.csv.gz`: se carga con `cargar_chequeado()`
y su huella es el SHA-256 del CSV (`hash_chequeado` en el JSON). Excluye las notas del corpus
argentino de prueba y toda afirmación parecida a uno de sus tuits (lo verifica `tests/`).

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

## *Fine-tuning* (ticket #33)

`fine_tuning.ipynb` ajusta cuatro corridas sobre las mismas particiones congeladas:

| `CORRIDAS` | Checkpoint | Entrena en | `max_length` | `id_corrida` |
|---|---|---|---|---|
| `xlmt` | `cardiffnlp/twitter-xlm-roberta-base` | FakeDeS | 512 | `xlm-t_fakedes_s42` |
| `xlmt-2etapas` | ídem | LIAR + FakeNewsNet (128), después FakeDeS | 512 | `xlm-t_liar-fakenewsnet-fakedes_s42` |
| `robertuito` | `pysentimiento/robertuito-base-uncased` | FakeDeS, texto con `preprocess_tweet(lang="es")` | 128 (tiene 130 posiciones) | `robertuito_fakedes_s42` |
| `beto` | `dccuchile/bert-base-spanish-wwm-cased` | FakeDeS | 512 | `beto_fakedes_s42` |

Hiperparámetros comunes (celda de parámetros): AdamW, tasa 2e-5, lote efectivo 16 (8 × 2),
10 % de calentamiento, *weight decay* 0,01, fp16, 5 épocas en FakeDeS y 2 en la etapa previa.
Se evalúa por época y se queda la de mejor F1 macro en la validación de FakeDeS; con ese
modelo se evalúan validación y prueba. El JSON lleva `epocas` (con `etapa`, pérdidas y
F1/AUC de validación), `hiperparametros.epoca_elegida` y las versiones de torch y
transformers en `entorno`. La mitad de las noticias de FakeDeS pasa los 500 *tokens*: se
trunca por la derecha (quedan el titular y el comienzo). RoBERTuito trunca el 97 %.

**En Colab:** abrir el notebook desde GitHub, *Cambiar tipo de entorno → GPU T4*, elegir
`GUARDAR_PESOS` (`"drive"` monta Drive y copia a `CARPETA_DRIVE/<id_corrida>/`; `"hub"`
sube a un repo privado `USUARIO_HUB/pfi-<id_corrida>` y necesita el secreto `HF_TOKEN` con
permiso de escritura) y *Ejecutar todas*. Al final descarga `fine_tuning.zip` con
`resultados/` y `figuras/`, que se descomprime acá y se versiona. Los pesos van con
`save_pretrained` más el JSON de la corrida: el Space carga el modelo con
`AutoModelForSequenceClassification`, aplica el `preprocesamiento` que dice el JSON y toma
la probabilidad de la etiqueta 1 («falso»).

**Humo local** (CPU, modelo diminuto, 8 filas por clase y partición, una época; escribe en
una carpeta temporal, nunca en `resultados/`): instalar `torch transformers accelerate
matplotlib datasets` y `pip install --no-deps pysentimiento emoji` en el `.venv`, poner
`HUMO = True` y ejecutar con `jupyter nbconvert --to notebook --execute --stdout fine_tuning.ipynb > /dev/null`.

## Space (servicio de inferencia, ticket #32)

`space/app.py` expone un único punto: `POST /clasificar` con `{"texto": "..."}` →
`{"puntaje", "clase", "version_modelo"}`. El puntaje es la probabilidad de «falso»; la
clase usa el umbral 0,5 de los JSON; la versión es el `id_corrida`. El modelo servido se
elige con la variable `MODELO` (por defecto `tfidf-lr_fakedes_s42`), que tiene que
coincidir con el nombre del `.joblib` subido. `space/requirements.txt` fija las versiones
del entrenamiento (`entorno` del JSON): un `.joblib` no se garantiza entre versiones.

El `.joblib` y `datos.py` no viven en `space/`: se suben al publicar (el `Pipeline`
referencia `datos.preprocesar`, así que `datos.py` tiene que quedar al lado de `app.py`).

**Estado:** sin publicar. En esta máquina no hay credenciales de Hugging Face. Además,
según la documentación de Hugging Face (consultada el 2026-09-28), crear un Space Docker
o Gradio exige un plan pago (PRO en cuentas personales), aunque el *hardware* CPU Basic
no se cobre por hora; la excepción gratuita son hasta 2 Spaces Gradio en ZeroGPU. Eso
pega en RNF-14 y hay que decidirlo antes de publicar.

### Probarlo local

```bash
cd prototipo/clasificador
mkdir -p /tmp/space && cp space/* datos.py modelos/tfidf-lr_fakedes_s42.joblib /tmp/space/
cd /tmp/space && python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m uvicorn app:app --port 7860
curl -s -X POST localhost:7860/clasificar -H 'Content-Type: application/json' \
  -d '{"texto": "El INDEC informó que la inflación de agosto fue 2,1 %."}'
```

(o `docker build -t pfi-clasificador /tmp/space && docker run -p 7860:7860 pfi-clasificador`).

### Publicar el Space

Con cuenta de Hugging Face con plan que admita Spaces Docker:

```bash
pip install -U huggingface_hub           # trae la CLI `hf`
hf auth login                            # token con permiso de escritura
hf auth whoami                           # anotar el usuario: <usuario>

cd prototipo/clasificador
hf repos create <usuario>/pfi-clasificador --type space --space-sdk docker --flavor cpu-basic --public
hf upload <usuario>/pfi-clasificador space . --type space
hf upload <usuario>/pfi-clasificador datos.py datos.py --type space
hf upload <usuario>/pfi-clasificador modelos/tfidf-lr_fakedes_s42.joblib tfidf-lr_fakedes_s42.joblib --type space
```

El Space se construye solo (ver la pestaña *Logs* en `huggingface.co/spaces/<usuario>/pfi-clasificador`).
La dirección de la API es `https://<usuario>-pfi-clasificador.hf.space`:

```bash
curl -s -X POST https://<usuario>-pfi-clasificador.hf.space/clasificar \
  -H 'Content-Type: application/json' -d '{"texto": "Hola"}'
```

Para servir otro modelo: subir su `.joblib` y poner la variable `MODELO` en
*Settings → Variables* del Space (los modelos que no sean de scikit-learn necesitan
otro `app.py`).

### Conectarlo al servicio

En `prototipo/servicio/.env`:

```
ADAPTADOR=compuesto
URL_CLASIFICADOR=https://<usuario>-pfi-clasificador.hf.space
#TIEMPO_LIMITE_CLASIFICADOR_S=5
#INTERVALO_DESPERTAR_CLASIFICADOR_S=3600   # 0 desactiva la llamada periódica
```

Al arrancar, el servicio llama al Space una vez (lo despierta si dormía) y después cada
hora. Si el Space no responde a tiempo, el análisis sale parcial y no hay un 500.

### Prueba manual con la extensión

1. `cd prototipo && make dev` con el `.env` de arriba y `OPENAI_API_KEY`.
2. En el registro del servicio no tiene que aparecer `la llamada periódica falló`.
3. Cargar `prototipo/extension/dist` en Chrome y analizar un tuit con una afirmación.
4. En el desglose, el puntaje del Módulo 1 tiene que coincidir con el `curl` al Space
   sobre el mismo texto del tuit.
5. Con las herramientas de red del *service worker*, la respuesta de `/analizar` trae
   `puntajes.clasificador.clase` en `verdadero` o `falso` (ya no `sin_verificar`) y
   `version_modelo: "tfidf-lr_fakedes_s42"`.
6. Parcial: poner `URL_CLASIFICADOR=http://127.0.0.1:9`, reiniciar y analizar otro
   tuit: la interfaz muestra el aviso de análisis parcial.

## LLM *zero-shot* (ticket #34)

`llm_zero_shot.py` corre local (no en Colab) con `OPENAI_API_KEY` en el entorno o en
`../servicio/.env`. Usa el modelo (`gpt-5.6-luna`), el esfuerzo de razonamiento (`low`), el
tope de fichas (900) y la instrucción de extracción de `servicio/app/proveedor/openai.py`,
copiados el 2026-09-28 y adaptados a dos clases (se quita `sin_verificar`). La entrada es
el texto crudo, como en el servicio. El puntaje del LLM es la probabilidad de «falso»; el
umbral se elige por F1 macro en la validación de FakeDeS y se aplica igual a las pruebas.

```bash
.venv/bin/pip install -r requirements.txt                   # trae openai
.venv/bin/python llm_zero_shot.py --limite 5                # humo: no guarda JSON
.venv/bin/python llm_zero_shot.py                           # validación + prueba de FakeDeS
.venv/bin/python llm_zero_shot.py --argentino datos/corpus_argentino/candidatos.csv
```

Con `--argentino` agrega `argentino/prueba` con las filas cuya `etiqueta_confirmada` sea
`verdadero` o `falso`, con el mismo umbral. Cada respuesta queda en `cache_llm/` (fuera de
git), así que repetir no se paga; el reintento ante 429/5xx lo hace el SDK. El JSON lleva
además `consumo` (costo total en USD y latencia media por ejemplo) y, por evaluación,
`costo_usd`, `latencia_media_s` y `acuerdo_clase_llm`. La latencia se mide con 8 llamadas
en paralelo.

