---
titulo: Validación del Sistema
tipo: análisis
tags: [validacion, pruebas, metricas, baseline]
fuentes: []
actualizado: 2026-09-28
---

# Validación del Sistema

> **Alcance de esta página.** Define el **protocolo de evaluación del modelo**: partición, métricas, línea base y calidad de las etiquetas. Las pruebas de usabilidad y la validación con usuarios reales requieren un prototipo funcionando y se planifican para la Entrega 5.

## Partición de los datos

El clasificador es **binario: `verdadero` / `falso`**. La clase `sin_verificar` se eliminó el 2026-09-28 (ver [[datasets-overview]]): ningún dataset externo la trae, y esa situación la resuelve el sistema con el estado `SIN_CONTRASTE_EXTERNO` cuando no encuentra evidencia.

| Conjunto | Origen | Rol |
|---|---|---|
| Entrenamiento | Nivel 2 (FakeDeS, partición de entrenamiento). La variante de XLM-T con etapa en inglés pasa antes por el Nivel 1 (LIAR + FakeNewsNet) | Ajuste de parámetros |
| Validación | Partición estratificada de FakeDeS | Hiperparámetros, criterio de parada y **selección del modelo que se sirve** |
| Test académico | Partición oficial de prueba de FakeDeS | Comparabilidad con la literatura |
| Test real | Nivel 3: corpus argentino de prueba (108 tuits, 44/56) | Evaluación final en contexto real |

Reglas del protocolo:

1. **El test real es *holdout* estricto.** No participa de ningún ajuste, ni de parámetros, ni de hiperparámetros, ni de la elección del modelo. Se toca una sola vez, al final.
2. **Se respetan las particiones oficiales** de LIAR y FakeDeS donde existan, para que los números sean comparables con los papers.
3. **Estratificación por clase y semilla fija** en todas las particiones propias. Con 971 ejemplos, una partición aleatoria puede mover la proporción de clases lo suficiente como para mover la métrica.
4. **Sin fuga entre conjuntos.** Ningún ejemplo aparece en dos particiones; se deduplica por identificador de origen o, si no hay, por texto normalizado. Las particiones se congelan en archivos versionados.

## Métricas

**Métrica principal: F1 macro.**

No se usa *accuracy* como métrica principal porque los datasets tienen proporciones de clase desiguales: un modelo que favorezca a la clase mayoritaria puede tener buena exactitud global sin detectar el contenido falso. El F1 macro promedia las dos clases sin ponderar por frecuencia, y además es comparable entre el test académico y el corpus argentino, que tienen proporciones distintas.

**Métricas secundarias:**

| Métrica | Para qué |
|---|---|
| Precisión y exhaustividad por clase | Ver dónde falla. Un falso positivo (verdadero marcado como falso) cuesta más que un falso negativo, por el riesgo reputacional y legal |
| AUC-ROC (sobre la probabilidad de `falso`) | Independiente del umbral; permite comparar modelos sin fijar el punto de corte |
| Matriz de confusión + análisis de errores | Separar falsos positivos de falsos negativos y mirar ejemplos concretos de dónde falla |

La situación «no hay evidencia para pronunciarse» no se mide acá: no es salida del clasificador sino del ensamblado.

## Comparación de modelos

| Modelo | Rol |
|---|---|
| TF-IDF + regresión logística | **Línea base.** Referencia clásica, sin redes neuronales |
| XLM-T, solo FakeDeS | Multilingüe, pre-entrenado sobre tuits. Ver [[modelos-overview]] |
| XLM-T, LIAR + FakeNewsNet → FakeDeS | Mide si la etapa en inglés aporta |
| RoBERTuito | Monolingüe en español, entrenado sobre tuits, con su propio preprocesamiento |
| BETO | Monolingüe en español, dominio general |
| LLM *zero-shot* | Costo de oportunidad: si iguala sin entrenar, hay que revisar el enfoque. Se compara también latencia y costo por consulta |

**Selección:** gana el mejor F1 macro en la validación de FakeDeS, nunca mirando el corpus argentino. Si hay empate, el más liviano por latencia. Cada corrida registra hiperparámetros, curvas de pérdida y métricas por época.

**Criterio de RNF-05:** el clasificador debe alcanzar **F1 macro ≥ 0,80** y superar a la línea base **por al menos 10 puntos porcentuales**.

Los dos números cumplen funciones distintas y conviene no confundirlas. El umbral absoluto de 0,80 sale de la literatura ([[toapanta-2024-latam]] reporta F1 de 0,934 con RoBERTuito, [[modelos-espanol]] recoge 96 % de MarIA sobre FakeDeS) y se fija por debajo de esos valores porque el corpus argentino es más chico y más ruidoso. La mejora relativa sobre la línea base es la que realmente demuestra que el modelo aporta: un F1 de 0,80 contra una línea base de 0,78 no justificaría el costo del *transformer*.

> ⚠️ RNF-05 es el único número del documento que compromete un resultado experimental que todavía no se corrió. Se declara con número, y no con adjetivo, justamente para que sea verificable en la Entrega 5.

## Calidad de las etiquetas

El test real **no se etiqueta por juicio propio**: la etiqueta sale de una verificación publicada de Chequeado o de la fuente oficial que el tuit cita (INDEC, BCRA). La guía de etiquetado define cómo cada calificación de Chequeado pasa a `verdadero` / `falso` y qué casos se descartan.

- **Un único anotador, el autor**, que confirma o corrige cada fila de la planilla de candidatos.
- **No hay segundo anotador ni kappa** (decisión del 2026-09-28). La subjetividad se desplaza a la fuente: cada tuit guarda el enlace a la nota o al dato oficial que sustenta su etiqueta, así que cualquiera puede auditarla.
- **Limitación a declarar:** sesgo de selección. El corpus solo contiene afirmaciones que alguien ya verificó o que citan un dato oficial.

## Criterios de aceptación por requerimiento

| RNF | Umbral | Cómo se verifica |
|---|---|---|
| RNF-01 | 2 s, p95 | Instrumentación en la extensión, medición sobre una sesión de navegación real |
| RNF-02 | 8 s, p95 | Traza del servicio, medida de extremo a extremo |
| RNF-03 | 300 ms | Prueba de carga sobre publicaciones ya analizadas |
| RNF-04 | 50 ms | Perfilador de rendimiento del navegador sobre el hilo principal |
| RNF-05 | F1 ≥ 0,80 y +10 pp | Evaluación sobre el conjunto de test real |
| RNF-12 | HTTPS y claves resumidas | Inspección del tráfico y del esquema de la base |
| RNF-13 | Chrome MV3 en tres sistemas | Matriz de compatibilidad ejecutada a mano |
| RNF-14 | 14 USD/mes | Panel de facturación de los proveedores |

## Fuera de esta instancia

- **Prueba de usabilidad de RNF-15** (el indicador debe ser interpretable sin instrucción previa). Requiere el prototipo instalado y participantes reales.
- **Validación con usuarios reales.** Prevista para la Entrega 5, es requisito de la entrega final.
- **Pruebas funcionales de integración** sobre los siete casos de uso. Se diseñan cuando exista implementación contra la cual ejecutarlas.

## Referencias cruzadas
- [[requerimientos]]
- [[datasets-overview]]
- [[modelos-overview]]
- [[experimentos-overview]]
- [[metodologia]]
