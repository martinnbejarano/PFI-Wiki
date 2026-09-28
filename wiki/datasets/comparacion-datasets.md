---
titulo: Comparación de Datasets — Selección para el PFI
tipo: análisis
tags: [datasets, comparacion, seleccion, liar, fakenewsnet, pheme, fakeddit, multifc, spanish]
fuentes: []
actualizado: 2026-09-28
---

# Comparación de Datasets — Selección para el PFI

Esta página consolida el análisis comparativo de los datasets disponibles para detección de desinformación y la justificación de la estrategia de datos del PFI.

## Tabla comparativa completa

| Dataset | Idioma | Tamaño | Clases | Contexto social | Multimodal | Disponibilidad | Relevancia PFI |
|---|---|---|---|---|---|---|---|
| **LIAR** | Inglés | 12.836 | 6 | No | No | Libre | Alta (benchmark) |
| **FakeNewsNet** | Inglés | ~23.000 | 2 | Sí (Twitter) | Sí | GitHub | Alta (grafos) |
| **PHEME** | Inglés | ~6.500 | 3 | Sí (hilos Twitter) | No | Libre | Media |
| **Fakeddit** | Inglés | 1.063.106 | 2/3/6 | Sí (Reddit) | Sí | GitHub | Media (multimodal) |
| **MultiFC** | Inglés | 34.918 | 2–38 | No | No | Libre | Media (multi-fuente) |
| **CREDBANK** | Inglés | 60M+ tweets | 5 | Sí (streaming) | No | Restricto | Baja |
| **Spanish Fake News** | Español | 971 | 2 | No | No | Libre | **Crítica (gap)** |

## Análisis del gap en español

El gap de datos en español es el hallazgo estructural más importante:

```
Inglés: LIAR (12.836) + FakeNewsNet (~23.000) + Fakeddit (1M+)
             vs.
Español: Spanish Fake News (971 muestras)
```

Wang et al. (2024) documentan que el **83% de la investigación en fake news es en inglés**, con cobertura mínima en español y prácticamente nula para variedades latinoamericanas.

## Estrategia de datos del PFI

### Tier 1 — Entrenamiento inicial (transfer learning desde inglés)

**LIAR + FakeNewsNet** → Fine-tuning inicial del modelo base (XLM-RoBERTa aprovecha el inglés para inicializar representaciones).

**Justificación**: permite arrancar con 40.000+ ejemplos antes de tener datos propios en español.

### Tier 2 — Adaptación al español

**Spanish Fake News Corpus (FakeDeS)** → Fine-tuning de segundo nivel sobre datos en español.

**Justificación**: los 971 ejemplos son insuficientes solos, pero suficientes como segundo fine-tuning sobre un modelo ya adaptado al inglés.

### Tier 3 — Corpus argentino de prueba (fuente de datos primaria)

> Reescrito el 2026-09-28 (spec #28). La versión del 2026-08-19 lo acumulaba como subproducto de la operación, con un subconjunto de adaptación (2.000 a 5.000) y un test doblemente anotado con kappa. Ambas cosas se eliminaron. Detalle en [[datasets-overview]].

- **Solo prueba**: 200 a 300 tuits, cerca de 50/50 entre `verdadero` y `falso`. *Holdout* estricto: no entrena, no ajusta, no elige modelo.
- **Etiquetas desde verificaciones publicadas**: falsos de notas de Chequeado; verdaderos de notas «Verdadero» de Chequeado y de tuits que citan un dato del INDEC o del BCRA comprobable en la fuente. Un único anotador (el autor) confirma cada fila; sin segundo anotador ni kappa.
- **Acceso a Chequeado**: vuelve como fuente de *etiquetas*, no como fuente scrapeada. Su sitio bloquea clientes no navegador, así que la consulta tiene que respetar RNF-17 y no eludir ese bloqueo (ver [[restricciones-legales-eticas]]).
- **Encuadre legal**: art. 5 inc. 2 ap. a) de la Ley 25.326 para la recolección, art. 4 inc. 1 para la proporcionalidad de los campos, art. 16 para la supresión. El corpus no se distribuye durante el PFI (Ley 11.723).

## Decisión de evaluación

Para comparabilidad con la literatura, el sistema se evalúa en:
1. **FakeDeS** (español, partición oficial de prueba): comparabilidad con papers de español
2. **Corpus argentino de prueba** (evaluación final del sistema, una sola vez)

LIAR deja de ser conjunto de evaluación: solo lo ve la variante de XLM-T con etapa en inglés, como entrenamiento.

## Observaciones sobre MultiFC y CREDBANK

- **MultiFC** (34.918 claims de 26 sitios): útil para un sistema que incorpora múltiples fact-checkers. Si Chequeado + AFP + La Nación Verificación se usan como fuentes, MultiFC es el referente metodológico.
- **CREDBANK** (60M+ tweets): relevante solo si se implementa un pipeline de streaming de Twitter en tiempo real. No prioritario para MVP.

## Referencias cruzadas
- [[liar-dataset]]
- [[fakenewsnet]]
- [[pheme-dataset]]
- [[fakeddit]]
- [[spanish-fake-news-corpus]]
- [[wiki/estado-del-arte/brechas-espanol-latam]]
- [[wiki/datasets/dataset-recomendacion]]
