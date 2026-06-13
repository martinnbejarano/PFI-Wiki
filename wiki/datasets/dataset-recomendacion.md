---
titulo: Selección, Recolección y Validación de Datasets
tipo: desarrollo
tags: [dataset, entrenamiento, validación, anotación, español]
actualizado: 2026-04-19
---

# Selección, Recolección y Validación de Datasets

## Resumen ejecutivo

Para entrenar el modelo NLP de detección de desinformación necesitas:
1. **Dataset de ENTRENAMIENTO** (12k-20k samples etiquetados: verdadero/falso/mixto)
2. **Dataset de VALIDACIÓN** (500-1000 samples, anotados manualmente, reales de Argentina)

La estrategia recomendada es: **LIAR + FakeNewsNet (traducidos/multilingües) + data augmentation + validación con datos reales argentinos**.

---

## 1. DATASET DE ENTRENAMIENTO

### 1.1 LIAR Dataset (12.8k claims)

**Descripción:**
- Fuente: politifact.com (fact-checking manual)
- Tamaño: 12,800 claims en inglés
- Labels: 6 clases (pants-fire, false, barely-true, half-true, mostly-true, true)
- Disponible: https://www.cs.ucsb.edu/~william/data/liar_dataset.zip

**Para el PFI:**
- ✅ **Usar para entrenamiento inicial**
- Traducción: Usar modelo multilingüe (XLM-RoBERTa) — acepta múltiples idiomas
- O traducir automáticamente al español con Google Translate / DeepL
- Colapsar 6 clases en 2: {falso: pants-fire+false+barely-true} vs {verdadero: mostly-true+true}

**Comando de descarga:**
```bash
wget https://www.cs.ucsb.edu/~william/data/liar_dataset.zip
unzip liar_dataset.zip
```

### 1.2 FakeNewsNet (11.8k samples)

**Descripción:**
- Fuente: GossipCop (5.4k) + PolitiFact (6.4k)
- Tamaño: ~11,800 articles con grafos de propagación
- Labels: Verdadero/Falso + metadatos (followers, engagement, hora publicación)
- Disponible: https://github.com/KaiDMML/FakeNewsNet

**Para el PFI:**
- ✅ **Usar para entrenamiento + features de fuente**
- Incluye metadata (autor, followers, likes, replies) — útil para Módulo 2 (credibilidad de fuente)
- Combinar con LIAR para ~24k samples totales

**Comando:**
```bash
git clone https://github.com/KaiDMML/FakeNewsNet.git
```

### 1.3 Datasets en español (BUSCADOR)

**A investigar:**
- Kaggle: buscar "fake news spanish" o "desinformación español"
- GitHub: buscar repos de PFIs o papers hispanohablantes
- Universidad de Chile / Colombia / UNAM: proyectos de fake news en español
- Chequeado.com: contactar equipo, pedir acceso a dataset de afirmaciones verificadas

**Recomendación:** Hacer búsqueda específica en semana 1 del desarrollo.

### 1.4 Data Augmentation (aumentar volumen)

**Si los datos son insuficientes (<10k en español):**

| Técnica | Cómo | Riesgo |
|---|---|---|
| **Traducción automática** | Traducir LIAR al español con DeepL/Google | Pérdida de significado, cambios idiomáticos |
| **Paráfrasis** | Reescribir afirmaciones manteniendo sentido | Manual (lento); o automática con T5/GPT (costo) |
| **Back-translation** | Traducir a otro idioma y volver al español | Genera variantes del mismo contenido |
| **Mixup / Interpolación** | Mezclar features de samples similares | Requiere embeddings, más complejo |

**Recomendación para PFI:** Usar **traducción automática** + **paráfrasis manual** en ~500 samples críticos.

---

## 2. DATASET DE VALIDACIÓN (Datos reales argentinos)

### ¿Por qué necesitas validación en datos reales?

Los datasets académicos (LIAR, FakeNewsNet) son en inglés / genéricos. Tu modelo necesita ser validado en **datos reales del contexto argentino** para saber si funciona en la práctica.

### 2.1 Recolección de datos de validación

**Cantidad:** 200-500 posts/artículos reales de Argentina

**Fuentes:**

| Fuente | Cómo | Tamaño aprox |
|---|---|---|
| **Twitter/X API** | Buscar tweets sobre política/economía, 2025-2026 | 200-300 tweets |
| **Clarín.com** | Articulos últimos 3 meses, sección política | 50-100 artículos |
| **Infobae.com** | Articulos últimos 3 meses, sección economía | 50-100 artículos |
| **Página/12** | Articulos sobre elecciones 2025 | 30-50 artículos |
| **Telam** | Noticias de agencia oficial (confiable) | 50-100 artículos |

**Herramienta de recolección (si usas Twitter API):**
```python
# Pseudocódigo
import tweepy
client = tweepy.Client(bearer_token="YOUR_TOKEN")
tweets = client.search_recent_tweets(
    query="(dólar OR inflación OR elecciones) lang:es",
    max_results=100,
    tweet_fields=["created_at", "author_id"]
)
```

**Comando simplificado (sin API):**
- Descargar manualmente posts/artículos
- Guardar en CSV: `[texto, plataforma, fecha, etiqueta_real]`

### 2.2 Anotación manual (etiquetar verdadero/falso)

**Proceso:**
1. **Tú anotas** todos los 200-500 posts (esfuerzo: 5-10 horas)
2. **1-2 personas externas anotan** ~50 posts (verificación de consenso)
3. **Calcular Cohen's Kappa** (acuerdo entre anotadores)

**Labels:**
```
0 = Verdadero (afirmación corroborada por fuentes confiables)
1 = Falso (afirmación contradice datos verificados)
2 = Mixto/Incierto (parcialmente verdadero o imposible verificar)
```

**Ejemplo de anotación:**
```csv
texto,plataforma,fecha,label,nota
"El dólar cerró a 1000 pesos",twitter,2026-04-19,0,"BCRA confirmó en comunicado"
"La inflación es 5% anual",twitter,2026-04-19,1,"INDEC reporta 187% anual"
"El Ministro X renunció",twitter,2026-04-19,2,"Ministro desmintió pero hay incertidumbre"
```

**Herramienta recomendada para anotación:**
- **Taiga.io** (gratuito, colaborativo): https://taiga.io/
- **Prodigy** (pago, especial para ML): https://prodi.gy/
- O simplemente: **Google Sheets + consenso manual**

### 2.3 Métrica de acuerdo inter-anotador

Si 2+ personas anotan los mismos 50 posts:

**Cohen's Kappa:**
```
κ = (observed agreement - expected agreement) / (1 - expected agreement)
κ > 0.8 = Excelente acuerdo
κ 0.6-0.8 = Bueno
κ < 0.6 = Revisar etiquetas
```

**Herramienta Python:**
```python
from sklearn.metrics import cohen_kappa_score
kappa = cohen_kappa_score(anotador1, anotador2)
```

---

## 3. DISTRIBUCIÓN DE DATOS RECOMENDADA

Para modelo robusto:

| Conjunto | Tamaño | Fuente | Propósito |
|---|---|---|---|
| **Training** | 15,000-20,000 | LIAR + FakeNewsNet | Entrenar modelo |
| **Validation** | 1,000 | LIAR + FakeNewsNet | Tuning de hiperparámetros |
| **Test (académico)** | 2,000 | LIAR + FakeNewsNet | Reportar accuracy en paper |
| **Test (real Argentina)** | 200-500 | Recolección manual + anotación | Validar en contexto real |

**Split típico:** 70-20-10 (entrenamiento - validación - test)

---

## 4. CHECKLIST DE RECOLECCIÓN Y VALIDACIÓN

- [ ] Descargar LIAR dataset
- [ ] Descargar FakeNewsNet
- [ ] Investigar datasets en español (Kaggle, GitHub, académicos)
- [ ] Contactar Chequeado.com para pedir dataset
- [ ] Obtener Twitter API v2 (aplicación académica gratuita)
- [ ] Recolectar 200-500 posts reales de Argentina
- [ ] Crear CSV con columnas: [texto, plataforma, fecha, label]
- [ ] Anotar manualmente (o con 2+ anotadores)
- [ ] Calcular Cohen's Kappa (si 2+ anotadores)
- [ ] Documentar proceso de anotación en wiki
- [ ] Guardar datos anonymizados (sin ID usuario)
- [ ] Verificar distribución de clases (balance verdadero/falso)

---

## 5. Gestión de datos

### Estructura de carpetas (raw/)
```
raw/
├── datasets/
│   ├── liar_dataset/           # LIAR descargado
│   ├── fakenewsnet/            # FakeNewsNet descargado
│   ├── spanish_datasets/       # Cualquier dataset en español encontrado
│   └── validation_argentina/   # Posts recolectados + anotaciones
└── README.md                    # Documentación de cada dataset
```

### Privacidad
- ✅ Guardar: texto del post, fecha, plataforma, label
- ❌ NO guardar: ID usuario, username, email, IP, ubicación
- ✅ Si publicas dataset: anonymizar completamente

---

## 6. Timelines estimadas

| Tarea | Tiempo | Notas |
|---|---|---|
| Descargar LIAR + FakeNewsNet | 30 min | Descarga + unzip |
| Explorar datasets (EDA) | 2-3 horas | Entender estructura, distribución |
| Traducir/preparar datos | 5-10 horas | Si traducés LIAR al español |
| Investigar datasets en español | 3-5 horas | Búsqueda + evaluación |
| Recolectar datos reales (Argentina) | 5-10 horas | Descargas + cleanup |
| Anotar manualmente | 5-10 horas | 200-500 posts a mano |
| Preparar splits train/val/test | 1-2 horas | Scripts Python |
| **TOTAL** | **25-45 horas** | Distribuir en primeras 4-5 semanas |

---

## Referencias cruzadas

- [[wiki/solucion/pipeline-preprocesamiento]]
- [[wiki/proyecto/restricciones-legales-eticas]]
- [[wiki/estado-del-arte/kwon-jang-2025-survey-fake-text]]

## Enlaces útiles

- LIAR: https://www.cs.ucsb.edu/~william/data/liar_dataset.zip
- FakeNewsNet: https://github.com/KaiDMML/FakeNewsNet
- Twitter API v2: https://developer.twitter.com/en/docs/twitter-api
- Kaggle Fake News: https://www.kaggle.com/search?q=fake+news
- Cohen's Kappa: https://en.wikipedia.org/wiki/Cohen%27s_kappa

