---
titulo: Metodología Técnica — Arquitectura ML/DL
tipo: solucion
tags: [arquitectura, ml, dl, transformers, metodologia]
fuentes: []
actualizado: 2026-04-18
---

# Metodología Técnica: Arquitectura ML/DL de 4 Módulos

## Visión general del pipeline

```
INPUT: post de Twitter/X/Facebook/Instagram
  ↓
[MÓDULO 1: Clasificador NLP] → score_nlp
  ↓
[MÓDULO 2: Credibilidad de Fuente] → score_source
  ↓
[MÓDULO 3: Contraste Semántico + Web Search] → score_similarity + linked_sources
  ↓
[MÓDULO 4: Combinator/Ensemble] → final_score + confidence + reasoning
  ↓
OUTPUT: { score, confidence, reason, sources }
```

---

## MÓDULO 1: Clasificador NLP (Deep Learning — Transformers)

### Para qué se usa
**Analizar el CONTENIDO textual en sí**: ¿El texto tiene características lingüísticas típicas de desinformación?**

### Qué detecta
- Lenguaje emotivo/sensacionalista (señal de clickbait)
- Estructura lógica quebrada (falso razonamiento)
- Lenguaje manipulador (imperativo, absoluto, sin matices)
- Consistencia interna (¿se contradice?)
- Contexto temporal (claims sobre hechos pasados vs. futuros)

### Implementación
```
Modelo: Fine-tune BETO/XLM-RoBERTa
Entrada: texto del post (máx 512 tokens)
Output: logits → softmax → [prob_real, prob_falso, prob_sin_verificar]
Técnica: Transfer Learning (pre-entrenado en MLM, fine-tuned en clasificación)
Dataset: LIAR (multiidioma) + FakeNewsNet (traducido) + data augmentation
```

### Caso de uso
```
INPUT:  "¡¡URGENTE!! El gobierno acaba de anunciar que cerrarán TODOS 
         los bancos mañana. Saca tu dinero YA. No esperes."

[MÓDULO 1 análisis]
- Uso de mayúsculas exagerado ❌
- Lenguaje de urgencia artificial ("YA", "URGENTE") ❌
- Afirmación absoluta sin fuente ❌
- Emotivo, sin verificación ❌

OUTPUT: score_nlp = 0.85 (muy probable que sea desinformación)
```

### Limitaciones que corrige el resto del pipeline
- ⚠️ Puede marcar como falso contenido satírico/irónico legítimo
- ⚠️ No verifica si el contenido es factualmente correcto
- ⚠️ No evalúa credibilidad de la fuente

---

## MÓDULO 2: Credibilidad de Fuente (Machine Learning tradicional)

### Para qué se usa
**Evaluar QUIÉN está diciendo esto**: ¿La fuente (cuenta/medio) es confiable?**

### Qué detecta
- Patrones de comportamiento de bots o cuentas falsas
- Historial de la cuenta (antigüedad, consistencia)
- Verificación oficial (¿está verified en la plataforma?)
- Engagement típico (¿sus posts se comparten realmente?)
- Presencia en bases de datos de medios confiables

### Implementación (Opción A: ML tradicional)
```
Entrada: metadatos de la cuenta
  ├─ age_days: antigüedad de cuenta
  ├─ followers: número de seguidores
  ├─ retweet_rate: % de tweets retuiteados
  ├─ is_verified: está verificada en plataforma
  ├─ in_trusted_db: ¿está en base de medios confiables?
  ├─ language_entropy: diversidad de idiomas (bots suelen usar 1 idioma)
  ├─ tweet_frequency: tweets por día (bots: muy altos)
  └─ ...

[Logistic Regression]
score = sigmoid(w1*age + w2*followers + w3*retweet_rate + ... + b)

Output: score_source ∈ [0, 1]
  0 = fuente no confiable (bot, fake account)
  1 = fuente muy confiable (medio verificado, periodista oficial)
```

### Caso de uso
```
INPUT: Tweet de cuenta @pepe_random_xyz
  - age_days: 15 (cuenta muy nueva) ❌
  - followers: 23 (casi ninguno) ❌
  - retweet_rate: 2% (baja) ❌
  - is_verified: False ❌
  - in_trusted_db: False ❌
  
[MÓDULO 2]
score_source = 0.15 (fuente poco confiable)

vs.

INPUT: Tweet de @clarincom (Clarín oficial)
  - age_days: 5000+ (cuenta antigua) ✅
  - followers: 2.3M ✅
  - retweet_rate: 45% (alto) ✅
  - is_verified: True ✅
  - in_trusted_db: True ✅
  
[MÓDULO 2]
score_source = 0.92 (fuente muy confiable)
```

### Limitaciones
- ⚠️ No evalúa si el CONTENIDO es verdadero
- ⚠️ Un medio confiable puede publicar desinformación ocasionalmente
- ⚠️ No diferencia entre sesgo político y falsedad factual

---

## MÓDULO 3: Contraste contra Fuentes Confiables (Deep Learning + Information Retrieval)

### Para qué se usa
**Comparar el claim contra EVIDENCIA REAL**: ¿Qué dicen medios confiables y fuentes oficiales sobre este tema?**

### Qué detecta
- Cobertura en medios confiables (Infobae, Clarín, La Nación)
- Datos en fuentes oficiales (leyes, datos governamentales, estadísticas públicas)
- Consenso entre medios (¿todos dicen lo mismo o hay desacuerdo?)
- Presencia de evidencia contradictoria
- Documentación oficial que refuta o corrobora el claim

### Implementación

```
PASO 1: Extraer los CLAIMS principales del post
  INPUT: "El gobierno cerró 500 escuelas en Buenos Aires"
  TÉCNICA: NER (Named Entity Recognition) + relaciones semánticas
  OUTPUT: { claim: "cerrar escuelas", location: "Buenos Aires", 
            number: 500, entity: "gobierno" }

PASO 2: WEB SEARCH en medios confiables
  INPUT: claims extraído
  TÉCNICA: BM25 (búsqueda) + keyword search en URLs confiables
  SEARCH en: Infobae, Clarín, La Nación, Página/12, Telam
  FILTER: artículos de últimos 30 días (relevancia temporal)
  OUTPUT:
    ├─ "Clarín: Gobierno anuncia cierre de 50 escuelas" 
    │  └─ contradice el número de 500 ❌
    ├─ "Infobae: Crisis en educación — análisis de cierres" 
    │  └─ menciona problema real pero otros números ❌
    ├─ "La Nación: Ministerio de Educación responde..." 
    │  └─ declara falsedad del número ❌
    └─ consensus_score: 0.92 (alto consenso de que es falso)

PASO 3: BUSCAR EN FUENTES OFICIALES
  INPUT: claim + metadatos (tipo: ley, dato económico, educación, salud, etc.)
  
  [Detección automática de tipo de claim]
  SI claim_type == "ley o decreto":
    → Buscar en: infoleg.gob.ar (sistema legislativo argentino)
    → Output: documento legislativo oficial + fecha de promulgación
    
  SI claim_type == "dato económico":
    → Buscar en: indec.gob.ar (estadísticas), bcra.gob.ar (banco central)
    → Output: dato oficial + series históricas
    
  SI claim_type == "educación":
    → Buscar en: minedu.gob.ar (ministerio), digesto de resoluciones
    → Output: resolución oficial + comuniquées
    
  SI claim_type == "salud":
    → Buscar en: msal.gob.ar (ministerio de salud)
    → Output: boletín oficial, datos epidemiológicos
    
  SI claim_type == "cierres/suspensión":
    → Buscar en: boletín oficial (boletin.gob.ar)
    → Output: decreto presidencial o resolución ministerial

  EJEMPLO — Claim: "Nueva ley de educación online"
    → Search: infoleg.gob.ar
    → Result: "Ley 27.779 — Educación online en universidades" 
              (promulgada 2023-03-15, art. 5 especifica...)
    → Verdict: SI existe ley, mostrar texto oficial
    
  EXAMPLE — Claim: "El dólar está a $800"
    → Search: bcra.gob.ar/cotizaciones
    → Result: dólar oficial HOY = $850, ayer = $845
    → Verdict: claim es incorrecto (número desactualizado)

PASO 4: Combinar WEB SEARCH + FUENTES OFICIALES
  ├─ media_consensus: 3/3 medios contradicen claim (0.92)
  ├─ official_source: Decreto oficial dice "50 escuelas", no 500 (0.98)
  ├─ temporal_relevance: decreto de ayer (0.95)
  └─ combined_score_similarity = max(media_consensus, official_source) = 0.98

OUTPUT:
  ├─ score_similarity: 0.98 (confirmado como falso por fuentes oficiales)
  ├─ linked_sources: [
  │    { type: "official", source: "Decreto PEN", url: "boletín oficial", text: "50 escuelas" },
  │    { type: "news", source: "Clarín", url: "...", excerpt: "..." },
  │    { type: "news", source: "La Nación", url: "...", excerpt: "..." }
  │  ]
  └─ confidence: "Fuente oficial + 3 medios confirman número diferente"
```

### Arquitectura detallada

```
┌─ WEB SEARCH PATH (Medios confiables)
│  ├─ Trusted news sources: {infobea.com, clarin.com, lanacion.com.ar, 
│  │                         pagina12.com.ar, telam.gov.ar}
│  ├─ Search API: Google Search API O Serpapi O búsqueda local
│  ├─ Query: auto-generated keywords from post
│  ├─ Reranking: usar BETO para rankear resultados por relevancia
│  └─ Filtering: solo últimos 30 días + high-quality domains
│
└─ OFFICIAL SOURCES PATH (Fuentes governamentales)
   ├─ Legislación: infoleg.gob.ar (API disponible)
   │  └─ Search: leyes, decretos, resoluciones
   │
   ├─ Datos económicos: indec.gob.ar, bcra.gob.ar (APIs disponibles)
   │  └─ Search: inflación, desempleo, cotizaciones, PBI
   │
   ├─ Educación: minedu.gob.ar (boletines, resoluciones)
   │  └─ Search: programas, resoluciones, comunicados
   │
   ├─ Salud: msal.gob.ar (boletines epidemiológicos)
   │  └─ Search: estadísticas, programas, alertas
   │
   └─ Boletín Oficial: boletin.gob.ar (decretos, resoluciones)
      └─ Search: cualquier acto oficial del gobierno
```

### Ejemplo detallado: Claim sobre nueva ley

```
CLAIM: "Acaban de sancionar una nueva ley que prohíbe usar TikTok en escuelas"

[PASO 1] Extrae: { claim_type: "ley", entity: "TikTok", location: "escuelas" }

[PASO 2] Web search en medios
  - Clarín: "¿Prohibirán TikTok en escuelas? Debate en Senado"
  - La Nación: "Diputados debaten proyecto sobre redes en educación"
  - Infobea: "Educación estudia restricciones para menores en redes"
  → Consenso: hay DEBATE pero NO se sancionó ley aún

[PASO 3] Buscar fuentes oficiales
  → infoleg.gob.ar: search "TikTok escuelas"
    ├─ Resultado 1: Proyecto presentado por diputado X (sin sancionar)
    ├─ Resultado 2: Comunicado MINEDU (estudia regulación, sin medida oficial)
    └─ Resultado 3: NINGUNA LEY SANCIONADA
  
  → boletin.gob.ar: search "ley TikTok"
    └─ NINGÚN DECRETO PRESIDENCIAL

[PASO 4] Síntesis
  score_similarity = 0.15 (contenido es FALSO — no hay ley sancionada)
  
  REASONING:
  - Medios reportan DEBATE, no sanción
  - infoleg.gob.ar: ninguna ley sancionada
  - Boletín oficial: sin decreto
  - Conclusión: es DESINFORMACIÓN (confunde proyecto con ley)
  
  LINKED SOURCES:
  - ✓ Clarín: "¿Prohibirán TikTok? Debate en Senado" [debate, no ley]
  - ✓ infoleg.gob.ar: proyecto sin sancionar [fuente oficial]
  - ✓ MINEDU: comunicado sobre estudio [sin medida oficial]
```

### Ejemplo 2: Claim sobre dato económico

```
CLAIM: "La inflación en Argentina es del 5% anual"

[PASO 1] Extrae: { claim_type: "dato_económico", metric: "inflación", value: "5%" }

[PASO 2] Web search
  - BCRA: "La inflación de marzo fue 2.7%" [actual]
  - Clarín: "Inflación acelera en primer trimestre" [2.8% en marzo]
  - La Nación: "Índice de precios al consumidor..." [datos INDEC]

[PASO 3] Buscar fuentes oficiales
  → indec.gob.ar (API): 
    └─ Inflación acumulada 2025: 45.3%
    └─ Inflación últimos 12 meses: 187%
    └─ Inflación mes pasado: 2.7%
    └─ "5% anual" es FALSO, está extremadamente subestimado
  
  → bcra.gob.ar:
    └─ Confirma datos INDEC

[PASO 4] Síntesis
  score_similarity = 0.95 (es DESINFORMACIÓN — datos falsos)
  
  VERDICT: "FALSO — Inflación oficial es 187% anual, no 5%"
  
  LINKED_SOURCES:
  - ✓ INDEC: Índice de precios — 187% anual [fuente oficial]
  - ✓ BCRA: Datos de inflación [fuente oficial]
  - ✓ Clarín: "Inflación acelera..." [cobertura media]
```

### Casos de uso

**Caso A: Desinformación con fact-check explícito**
```
post: "El presidente dijo que Argentina nunca fue en déficit"
→ Chequeado.com: "Desmentida — Argentina estuvo en déficit histórico"
→ score_similarity: 0.95 (muy similar a falsedad verificada)
```

**Caso B: Desinformación sin fact-check, pero contradicha por medios**
```
post: "Robaron 100 millones de la Tesorería anoche"
→ Chequeado.com: sin match
→ Web search: Clarín/Infobae/La Nación = "no hay reportes de robo"
→ consensus_score: 0.88 (consenso de que es falso)
→ score_similarity: 0.88
```

**Caso C: Claim verificado como correcto**
```
post: "Argentina está en recesión económica"
→ Chequeado.com: "Verificado — datos del BCRA confirman..."
→ Web search: todos los medios lo reportan
→ score_similarity: 0.05 (muy diferente a desinformación)
```

### Limitaciones
- ⚠️ Requiere acceso a web search (Google API O Serpapi) — costo $
- ⚠️ Medios confiables pueden tener sesgos políticos
- ⚠️ No detecta desinformación "nueva" (sin cobertura aún)
- ⚠️ Lag temporal (toma 1-2 horas que los medios cubran algo)

### Ventajas
- ✅ Fuentes oficiales son "verdad de campo" — no hay sesgo editorial
- ✅ Detecta desinformación nueva (si hay decreto/ley que la contradice)
- ✅ Muy preciso para claims sobre leyes, datos económicos, salud, educación
- ✅ Links a documentos originales (no filtrados por medio)
- ✅ Consenso triple: medios + fuentes oficiales + Módulo 1 (NLP)

---

## MÓDULO 4: Combinator/Ensemble (Machine Learning)

### Para qué se usa
**Sintetizar los 3 módulos en una DECISIÓN FINAL**: ¿Es desinformación o no?**

### Cómo funciona

```
INPUT: 
  ├─ score_nlp: 0.75 (contenido textualmente sospechoso)
  ├─ score_source: 0.30 (fuente poco confiable)
  └─ score_similarity: 0.85 (muy similar a falsedad verificada)

[WEIGHTED ENSEMBLE]
final_score = 0.4 * score_nlp 
            + 0.2 * (1 - score_source)  ← inverso: si fuente es mala, suma
            + 0.4 * score_similarity

final_score = 0.4 * 0.75 + 0.2 * (1 - 0.30) + 0.4 * 0.85
            = 0.30 + 0.14 + 0.34
            = 0.78

OUTPUT:
  ├─ final_score: 0.78
  ├─ confidence: 0.82 (promedio de los 3 scores)
  ├─ verdict: "PROBABLEMENTE FALSO"
  └─ reasoning: [
       "Contenido textualmente sospechoso (75%)",
       "Fuente poco confiable (cuenta nueva, sin verificación)",
       "Similar a desmentidas verificadas (85%)",
       "3 medios contradicen la afirmación"
     ]
```

### Pesos y threshold

**Calibración (ajustar vía validación con usuarios):**
- `score_nlp`: 40% — el contenido textual es importante
- `(1 - score_source)`: 20% — si la fuente es confiable, baja la sospecha
- `score_similarity`: 40% — si hay evidencia contradictoria, es clave

**Threshold:**
- `final_score > 0.75` → **"PROBABLEMENTE FALSO"** (flag al usuario)
- `0.40 < final_score <= 0.75` → **"INFORMACIÓN SOSPECHOSA"** (verifica antes de compartir)
- `final_score <= 0.40` → **"PARECE VERIFICADO"** (bajo riesgo)

### Limitaciones
- ⚠️ Los pesos son heurísticos, pueden ser subóptimos
- ⚠️ No todos los módulos tienen igual confianza
- ⚠️ Casos edge: contradicciones entre módulos (Ej: fuente confiable pero contenido sospechoso)

### Mejora opcional: Pequeña Red Neuronal
Si con weighted ensemble hay muchos errores, entrenar una pequeña NN en ejemplos reales:
```
INPUT: [score_nlp, score_source, score_similarity]
  ↓
Dense(32) → ReLU → Dense(16) → ReLU → Dense(1) → Sigmoid
  ↓
OUTPUT: final_score (weights aprendidos, no heurísticos)
```

---

## Tabla resumen: Para qué cada módulo

| Módulo | Pregunta | Input | Técnica | Output | Caso de uso |
|---|---|---|---|---|---|
| **1. NLP** | ¿El TEXT es sospechoso? | Texto del post | Transformer (BETO) | score_nlp ∈ [0,1] | "¿Tiene señales lingüísticas de desinformación?" |
| **2. Source** | ¿La FUENTE es confiable? | Metadatos de cuenta | Logistic Regression | score_source ∈ [0,1] | "¿Es una cuenta real, verificada, con historial?" |
| **3. Contrast** | ¿Qué dicen OTROS sobre esto? | Claims extraído | Vector similarity + Web Search | score_similarity ∈ [0,1] | "¿Medios confiables y fact-checkers qué dicen?" |
| **4. Ensemble** | ¿CONCLUSIÓN final? | [score_nlp, score_source, score_similarity] | Weighted combine | final_score + reasoning | "Sintetizar todo → decisión final" |

---

## Flujo end-to-end: ejemplo real

```
USER: Lee un post en Twitter: 
"¡¡¡El gobierno acaba de CERRAR TODAS las escuelas de CABA!!! 
 Mi hijo no puede ir mañana. COMPARTAN ESTO 🚨"

SISTEMA:
┌─ Módulo 1 (NLP)
│  Input: "¡¡¡El gobierno acaba de CERRAR TODAS las escuelas..."
│  Analysis:
│    - Mayúsculas exageradas ❌
│    - Lenguaje emotivo/urgencia artificial ❌
│    - Afirmación absoluta sin fuentes ❌
│    - Emojis de alerta ❌
│  Output: score_nlp = 0.82
│
├─ Módulo 2 (Source Credibility)
│  Input: Cuenta @pepe_xyz_123
│  Analysis:
│    - Account age: 2 meses ❌
│    - Followers: 145 ❌
│    - Verified: No ❌
│    - In trusted DB: No ❌
│  Output: score_source = 0.18
│
├─ Módulo 3 (Contrast + Web Search)
│  Input: claim "gobierno cerró todas las escuelas CABA"
│  Chequeado.com: "Desmentida — Gobierno cerró 50 escuelas, no todas"
│  Web Search:
│    - Clarín: "Anuncian cierre temporal de 50 escuelas"
│    - La Nación: "Ministerio aclara: no hay cierre total"
│    - Infobae: "Crisis educativa: qué hay de verdad en viral"
│  Analysis:
│    - Fact-check encontrado: match 0.88
│    - Consenso web: 3/3 medios contradicen
│    - Claim es FALSO
│  Output: score_similarity = 0.89
│
└─ Módulo 4 (Ensemble)
   final_score = 0.4*0.82 + 0.2*(1-0.18) + 0.4*0.89
               = 0.328 + 0.164 + 0.356
               = 0.848
   
   VERDICT: ⚠️ PROBABLEMENTE FALSO (84.8%)
   
   REASONING:
   - "Contenido con lenguaje sensacionalista y emotivo (82%)"
   - "Fuente no confiable: cuenta nueva, sin verificación"
   - "Chequeado.com tiene desmentida similar: 'No, fueron 50, no todas'"
   - "Clarín, La Nación e Infobae contradicen esta versión"
   - "Score final: 84.8% — probablemente desinformación"
   
   LINKED SOURCES:
   - ✓ Chequeado.com: "Desmentida — gobierno cerró 50, no todas las escuelas"
   - ✓ Clarín: "Anuncian cierre temporal de 50 escuelas"
   - ✓ La Nación: "Ministerio aclara: no hay cierre total"

OUTPUT to user (extensión Chrome):
  ┌─────────────────────────────────────┐
  │ ⚠️ INFORMACIÓN SOSPECHOSA            │
  │ 85% probable que sea falso           │
  │                                       │
  │ 🔍 Razones:                          │
  │ • Lenguaje sensacionalista           │
  │ • Fuente poco confiable              │
  │ • Contradice fact-checks             │
  │ • 3 medios dicen lo contrario        │
  │                                       │
  │ 📰 Qué dicen medios confiables:      │
  │ • Clarín: "50 escuelas, no todas"   │
  │ • La Nación: "Sin cierre total"      │
  │ • Chequeado: "Desmentida"            │
  │                                       │
  │ [Ver fuentes completas]              │
  └─────────────────────────────────────┘
```

---

## Referencias cruzadas
- [[wiki/proyecto/propuesta]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/tecnologias]]
