---
titulo: Validación del Sistema
tipo: análisis
tags: [validacion, pruebas, metricas, baseline, kappa]
fuentes: []
actualizado: 2026-08-19
---

# Validación del Sistema

> **Alcance de esta página.** Define el **protocolo de evaluación del modelo**: partición, métricas, línea base y calidad de las etiquetas. Las pruebas de usabilidad y la validación con usuarios reales requieren un prototipo funcionando y se planifican para la Entrega 5.

## Partición de los datos

| Conjunto | Origen | Rol |
|---|---|---|
| Entrenamiento | Nivel 1 (LIAR + FakeNewsNet), Nivel 2 (FakeDeS), Nivel 3a (corpus argentino, adaptación) | Ajuste de parámetros |
| Validación | Partición estratificada del Nivel 2 y del Nivel 3a | Selección de hiperparámetros y criterio de parada |
| Test académico | Partición oficial de LIAR y de FakeDeS | Comparabilidad con la literatura |
| Test real | Nivel 3b (300 a 500, anotado a mano) | Evaluación en contexto real |

Reglas del protocolo:

1. **El test real es *holdout* estricto.** No participa de ningún ajuste, ni de parámetros ni de hiperparámetros. Se toca una sola vez, al final.
2. **Se respetan las particiones oficiales** de LIAR y FakeDeS donde existan, para que los números sean comparables con los papers.
3. **Estratificación por clase** en todas las particiones propias. `sin_verificar` es la clase minoritaria y una partición aleatoria puede dejarla mal representada.
4. **Sin fuga entre niveles.** Una publicación del corpus argentino no puede aparecer en dos subconjuntos, y el `id_nativo` es la clave de deduplicación.

## Métricas

**Métrica principal: F1 macro.**

No se usa *accuracy* como métrica principal por una razón concreta: las clases están desbalanceadas y `sin_verificar` es minoritaria. Un modelo que nunca predijera esa clase podría tener buena exactitud global y ser inútil justo en el caso que más importa, que es el contenido reciente sin verificación disponible. El F1 macro promedia por clase sin ponderar por frecuencia, así que penaliza exactamente ese fallo.

**Métricas secundarias:**

| Métrica | Para qué |
|---|---|
| Precisión y exhaustividad por clase | Ver dónde falla. Un falso positivo sobre contenido verdadero cuesta más que un falso negativo, por el riesgo reputacional y legal |
| AUC-ROC (una contra el resto) | Independiente del umbral; permite comparar modelos sin fijar el punto de corte |
| Matriz de confusión | Distinguir si el error es `verdadero` ↔ `falso` (grave) o `X` ↔ `sin_verificar` (menos grave) |

## Línea base y modelos de contraste

| Modelo | Rol |
|---|---|
| TF-IDF + regresión logística | **Línea base.** Referencia clásica, sin redes neuronales |
| XLM-T | **Modelo principal.** Ver [[modelos-overview]] |
| RoBERTuito | Contraste: monolingüe en español, entrenado sobre tuits |
| BETO | Contraste: monolingüe en español, dominio general |

**Criterio de RNF-05:** el clasificador debe alcanzar **F1 macro ≥ 0,80** y superar a la línea base **por al menos 10 puntos porcentuales**.

Los dos números cumplen funciones distintas y conviene no confundirlas. El umbral absoluto de 0,80 sale de la literatura ([[toapanta-2024-latam]] reporta F1 de 0,934 con RoBERTuito, [[modelos-espanol]] recoge 96 % de MarIA sobre FakeDeS) y se fija por debajo de esos valores porque el corpus argentino es más chico y más ruidoso. La mejora relativa sobre la línea base es la que realmente demuestra que el modelo aporta: un F1 de 0,80 contra una línea base de 0,78 no justificaría el costo del *transformer*.

> ⚠️ RNF-05 es el único número del documento que compromete un resultado experimental que todavía no se corrió. Se declara con número, y no con adjetivo, justamente para que sea verificable en la Entrega 5.

## Calidad de las etiquetas

El conjunto de test real se anota a mano, y una anotación de un solo anotador no es verificable.

1. El autor anota las 300 a 500 publicaciones del conjunto de test.
2. Un segundo anotador anota de forma independiente un subconjunto de al menos 50.
3. Se calcula el **coeficiente Kappa de Cohen** sobre ese subconjunto.

**Umbral de aceptación: κ ≥ 0,60** (acuerdo sustancial en la escala de Landis y Koch). Por debajo de ese valor el problema no es el modelo sino el esquema de etiquetas, y corresponde revisar la guía de anotación antes de seguir.

Los desacuerdos se resuelven por discusión, no por promedio, y se documenta el criterio con el que se resolvieron.

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
