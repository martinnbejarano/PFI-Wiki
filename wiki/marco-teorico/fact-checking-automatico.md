---
titulo: Fact-Checking Automático — Pipeline Canónico
tipo: concepto
tags: [fact-checking, claim-detection, evidence-retrieval, verdict-prediction, pipeline, nlp]
fuentes: [A Survey on Automated Fact-Checking - Guo 2022.md, Claim Detection Automated Fact-checking Survey - Panchendrarajan 2024.md, ClaimBuster Automated Fact-Checking - Hassan 2017.md, Web Retrieval Agents Evidence-Based Misinformation Detection - Tian 2024.md]
actualizado: 2026-08-11
---

# Fact-Checking Automático — Pipeline Canónico

El fact-checking automatizado es el proceso computacional de verificar si una afirmación (*claim*) es verdadera, falsa o indeterminada, sin intervención humana directa. Este campo constituye el núcleo técnico del sistema del PFI.

## Pipeline canónico (Guo et al., 2022)

La revisión de Guo et al. (2022) en *Transactions of the Association for Computational Linguistics* establece el pipeline estándar del campo, adoptado por la literatura posterior:

```
Texto de entrada
     ↓
[1] DETECCIÓN DE CLAIM
     ↓
[2] IDENTIFICACIÓN DE EVIDENCIA
     ↓
[3] VERIFICACIÓN DE CLAIM (veredicto)
     ↓
Etiqueta de veracidad + justificación
```

Cada módulo puede implementarse de forma independiente y combinarse en un sistema end-to-end.

## Módulo 1: Detección de Claim

### Definición

Una *claim* (afirmación verificable) es una oración que hace una asserción factual sobre el mundo real que puede ser evaluada como verdadera o falsa. No toda oración es una claim: las preguntas, opiniones, expresiones de emoción o declaraciones hipotéticas no lo son.

**Ejemplos de claims**: "El gobierno argentino gastó $500M en publicidad oficial en 2024."  
**No-claims**: "¿Cuánto gastó el gobierno?", "Creo que la deuda es enorme", "Si hubiera mejores precios..."

### Estado del arte (Panchendrarajan & Zubiaga, 2024)

La revisión de Panchendrarajan & Zubiaga (2024) categoriza los métodos:

| Enfoque | Descripción | Performance |
|---|---|---|
| Basado en features | TF-IDF, POS tags, características sintácticas | F1 ~0.65–0.75 |
| Deep learning | BiLSTM, CNN sobre embeddings | F1 ~0.75–0.82 |
| Transformers (BERT) | Clasificación con fine-tuning | F1 ~0.85–0.92 |
| Zero-shot LLMs | GPT-4, Claude sin fine-tuning | F1 ~0.70–0.80 |

### ClaimBuster (Hassan et al., 2017)

La herramienta ClaimBuster fue el primer sistema práctico de detección automática de claims. Desarrollado por la University of Texas Arlington, clasifica oraciones en tres categorías:
- *Non-factual sentence* (NFS): opinión, pregunta, etc.
- *Unimportant factual sentence* (UFS): hecho sin relevancia pública
- *Check-worthy factual sentence* (CFS): claim que merece verificación

Disponible como API pública; relevante como componente del pipeline del PFI.

## Módulo 2: Identificación de Evidencia

### Categorías de evidencia

La evidencia para verificar una claim puede provenir de:
1. **Base de conocimiento estructurada**: Wikidata, DBpedia, Wikipedia (acceso eficiente, cobertura limitada)
2. **Documentos no estructurados**: corpus de noticias, artículos periodísticos (alta cobertura, recuperación compleja)
3. **Búsqueda web en tiempo real**: evidencia fresca, cobertura máxima (mayor latencia)

### Web retrieval agéntico (Tian et al., 2024)

Tian et al. (2024) implementaron agentes de recuperación web para evidencia (*evidence-based misinformation detection*), integrando búsqueda con Serper/Google Search API + razonamiento con LLM.

**Resultado clave**: la incorporación de evidencia web mejora el F1 en **+20 puntos porcentuales** versus modelos que solo analizan el texto de la claim. Este es el hallazgo más relevante para la arquitectura del PFI, que incluye un módulo de búsqueda web (Tavily, en este proyecto).

## Módulo 3: Verificación de Claim (Veredicto)

### Esquemas de labels

| Dataset | Esquema de labels |
|---|---|
| LIAR | 6 clases (pants-fire, false, barely-true, half-true, mostly-true, true) |
| FakeNewsNet | Binario (real/fake) |
| MultiFC | Variable (2–38 clases según el fact-checker) |
| PFI (propuesto) | 4 clases: verdadero / falso / misleading / indeterminado |

### Desafío principal: generalización entre dominios

Un modelo entrenado en noticias políticas de EE.UU. (LIAR) degrada significativamente al aplicarse a:
- Noticias en español (dominio lingüístico diferente)
- Noticias argentinas (dominio temático/cultural diferente)
- Redes sociales vs. artículos periodísticos (dominio de canal diferente)

Yenikent et al. (2024) reportan la caída de 97–98% (in-domain) a 71% (datos reales), ilustrando el problema. Ver [[wiki/estado-del-arte/comparativa-llms-2024-2025]].

## Encuesta integral (Srba et al., 2025)

La encuesta de Srba et al. (2025) en *ACM Transactions on Intelligent Systems and Technology* agrega el uso de LLMs al pipeline:
- **LLMs como verificadores zero-shot**: ChatGPT puede hacer fact-checking sin fine-tuning, pero con menor accuracy que modelos fine-tuned en el dominio
- **LLMs como generadores de evidencia**: prompting para extraer evidencia interna del modelo
- **Señales textuales de credibilidad**: estilo de escritura, coherencia, fuentes citadas como features adicionales

La recomendación del survey es un **sistema híbrido**: BERT fine-tuned + búsqueda web + LLM como re-ranker.

## Diseño del pipeline del PFI

Basándose en el estado del arte, el sistema del PFI implementa:

```
Input (URL / texto libre)
     ↓
Módulo 1: Extracción y limpieza de texto
          + Tokenización (BETO/WordPiece)
     ↓
Módulo 2: Clasificación base (BERT/BETO fine-tuned)
          → Probabilidades iniciales de veracidad
     ↓
Módulo 3: Búsqueda web (Tavily)
          → Recuperación de evidencia
          → Re-scoring con evidencia
     ↓
Módulo 4: Veredicto final
          → Label + score de confianza + fuentes
```

Ver [[wiki/solucion/arquitectura]] y [[wiki/solucion/metodologia-tecnica]] para detalles de implementación.

## Referencias cruzadas
- [[wiki/marco-teorico/transformers-bert]]
- [[wiki/marco-teorico/nlp-fundacional]]
- [[wiki/estado-del-arte/comparativa-llms-2024-2025]]
- [[wiki/solucion/arquitectura]]

## Fuentes
- [[raw/papers/A Survey on Automated Fact-Checking - Guo 2022.md]]
- [[raw/papers/Claim Detection Automated Fact-checking Survey - Panchendrarajan 2024.md]]
- [[raw/papers/ClaimBuster Automated Fact-Checking - Hassan 2017.md]]
- [[raw/papers/Web Retrieval Agents Evidence-Based Misinformation Detection - Tian 2024.md]]
