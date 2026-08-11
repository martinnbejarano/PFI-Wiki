---
titulo: Comparativa BERT vs. LLMs para Detección (2024–2025)
tipo: análisis
tags: [estado-del-arte, bert, llms, gpt, comparativa, 2024, 2025, raza, srba, web-retrieval]
fuentes: [Fake News Detection Comparative BERT LLMs - Raza 2024.md, Survey Automatic Credibility Assessment Textual Signals LLMs - Srba 2025.md, Web Retrieval Agents Evidence-Based Misinformation Detection - Tian 2024.md, PolyTruth Multilingual Disinformation Detection - Gouliev 2025.md]
actualizado: 2026-06-04
---

# Comparativa BERT vs. LLMs para Detección de Fake News (2024–2025)

La explosión de LLMs (GPT-4, Claude, Gemini, LLaMA) generó expectativas de que estos modelos resolverían el problema de detección de desinformación. La evidencia empírica de 2024–2025 matiza estas expectativas.

## Conclusión adelantada

**BERT fine-tuned supera a LLMs para clasificación de fake news**, cuando se evalúa en el mismo dominio con métricas estándar. Los LLMs aportan valor en tareas de generación (explicaciones, síntesis de evidencia), no en clasificación binaria.

## BERT fine-tuned vs. LLMs — Raza et al. (2024)

Raza et al. (2024) — evaluación comparativa sistemática en LIAR y FakeNewsNet:

| Modelo | Tipo | Accuracy LIAR | F1 FakeNewsNet |
|---|---|---|---|
| BERT fine-tuned | Pre-train + fine-tune | **68%** | **89%** |
| RoBERTa fine-tuned | Pre-train + fine-tune | 67% | 88% |
| GPT-3.5 (zero-shot) | LLM sin fine-tune | 59% | 72% |
| GPT-4 (zero-shot) | LLM sin fine-tune | 63% | 78% |
| GPT-4 (few-shot, 5 ejemplos) | LLM con contexto | 65% | 81% |

**Hallazgo clave**: BERT fine-tuned supera a GPT-4 zero-shot en 5–10 puntos en accuracy. GPT-4 con few-shot se acerca pero no iguala.

**Por qué BERT gana**: el fine-tuning especializado permite al modelo aprender señales específicas del dominio que los LLMs generales no capturan en zero/few-shot.

## LLMs como señal de credibilidad textual — Srba et al. (2025)

Srba et al. (2025) — ACM TIST — examinan cómo los LLMs pueden usarse para **extracción de señales de credibilidad**:

### LLMs como herramientas de análisis (no clasificadores)

Los LLMs son útiles para:
- **Explicar** por qué un contenido parece sospechoso (evidencia generada)
- **Identificar características textuales** de desinformación (estilo sensacionalista, ausencia de fuentes, inconsistencias)
- **Generar preguntas de verificación** para el fact-checker humano

### Señales textuales de credibilidad identificadas

El survey identifica las señales más discriminativas:
1. Presencia/ausencia de fuentes citadas
2. Lenguaje sensacionalista / palabras de alta carga emocional
3. Consistencia interna del artículo
4. Comparación con cobertura de otros medios sobre el mismo evento
5. Historial del dominio/publicación

### Sistema híbrido recomendado

Srba et al. (2025) recomiendan un pipeline híbrido:
```
Clasificador base (BERT fine-tuned)
        +
LLM para extracción de señales / explicación
        +
Búsqueda web para evidencia factual
```

## Web retrieval agéntico — Tian et al. (2024)

Tian et al. (2024) implementaron un sistema que combina clasificación BERT con recuperación web en tiempo real:

| Configuración | F1 |
|---|---|
| Solo BERT (sin evidencia) | 0.72 |
| BERT + evidencia de Wikipedia | 0.81 |
| BERT + evidencia web (Serper/Google) | **0.92** |

**+20 puntos de F1** con búsqueda web. Este es el hallazgo que más directamente justifica la decisión de arquitectura del PFI de incluir un módulo de búsqueda web (Tavily, en este proyecto).

**Cómo funciona**: dado un claim, el agente busca en Google, recupera los primeros 5–10 resultados, los procesa con un LLM para extraer evidencia relevante, y luego el clasificador re-evalúa el claim con la evidencia.

## PolyTruth — Multilingüe 2025 (Gouliev et al., 2025)

Para el escenario multilingüe con español:

| Modelo | Inglés | Español | Promedio 25 langs |
|---|---|---|---|
| RemBERT | 89% | 81% | 82% |
| XLM-RoBERTa-large | 87% | 79% | 80% |
| GPT-4 zero-shot | 80% | 72% | 70% |
| mBERT | 78% | 68% | 66% |

**RemBERT y XLM-RoBERTa son superiores a GPT-4** incluso en escenario multilingüe, con español como uno de los idiomas evaluados.

## Decisión de diseño del PFI

Basándose en la evidencia de 2024–2025, el sistema del PFI adopta:

1. **Clasificador base**: XLM-T fine-tuned — resuelve en un solo modelo el español informal y la transferencia desde el inglés
2. **Búsqueda web**: módulo de búsqueda —Tavily— para recuperación de evidencia (+20pp F1)
3. **LLM como re-ranker**: OpenAI GPT-4 o Claude para síntesis de evidencia y generación de explicaciones
4. **No LLM como clasificador principal**: la evidencia muestra que BERT fine-tuned es superior

## Referencias cruzadas
- [[fakebert-kaliyar-2021]]
- [[wiki/marco-teorico/transformers-bert]]
- [[wiki/marco-teorico/modelos-espanol]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/metodologia-tecnica]]

## Fuentes
- [[raw/papers/Fake News Detection Comparative BERT LLMs - Raza 2024.md]]
- [[raw/papers/Survey Automatic Credibility Assessment Textual Signals LLMs - Srba 2025.md]]
- [[raw/papers/Web Retrieval Agents Evidence-Based Misinformation Detection - Tian 2024.md]]
- [[raw/papers/PolyTruth Multilingual Disinformation Detection - Gouliev 2025.md]]
