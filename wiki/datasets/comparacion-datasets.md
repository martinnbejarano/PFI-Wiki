---
titulo: Comparación de Datasets — Selección para el PFI
tipo: análisis
tags: [datasets, comparacion, seleccion, liar, fakenewsnet, pheme, fakeddit, multifc, spanish]
fuentes: []
actualizado: 2026-08-19
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

### Tier 3 — Corpus argentino (contribución del PFI)

> Reescrito el 2026-08-19. La versión anterior proponía scraping de medios y etiquetas de Chequeado. Chequeado quedó fuera del alcance por su bloqueo deliberado a clientes no navegador (ver [[restricciones-legales-eticas]]), y el corpus pasó a construirse como subproducto de la operación del sistema.

El corpus no se recolecta por separado: se acumula con las publicaciones que el propio sistema analiza y persiste (RF-16). Cada publicación analizada deja texto, metadatos públicos de la cuenta, veredicto y evidencia recuperada, que es exactamente la estructura que necesita un ejemplo de entrenamiento.

- **Adaptación**: 2.000 a 5.000 publicaciones acumuladas por operación, con etiqueta derivada del veredicto del sistema y revisión humana de los casos de baja confianza.
- **Test**: 300 a 500 publicaciones anotadas a mano, doblemente anotadas y con acuerdo medido por el coeficiente Kappa de Cohen. Es *holdout* estricto: no participa de ningún ajuste.
- **Encuadre legal**: art. 5 inc. 2 ap. a) de la Ley 25.326 para la recolección, art. 4 inc. 1 para la proporcionalidad de los campos, art. 16 para la supresión. El corpus no se distribuye durante el PFI (Ley 11.723).

**Meta**: entre 2.000 y 5.000 ejemplos en español rioplatense como contribución académica del PFI, con un conjunto de test anotado de 300 a 500.

## Decisión de evaluación

Para comparabilidad con la literatura, el sistema se evalúa en:
1. **LIAR** (inglés): comparabilidad con el 90% de los papers del campo
2. **FakeDeS** (español): comparabilidad con papers de español
3. **Dataset argentino propio** (evaluación final del sistema)

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
