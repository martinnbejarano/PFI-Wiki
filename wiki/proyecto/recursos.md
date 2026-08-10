---
titulo: Recursos — Presupuesto estimado
tipo: proyecto
tags: [presupuesto, infraestructura, cloud, recursos]
fuentes: []
actualizado: 2026-08-13
---

# Recursos — Presupuesto estimado

Los recursos financieros del proyecto se dividen en dos categorías: costos fijos (pagos únicos, no recurrentes) y costos mensuales (servicios de infraestructura en la nube). Los gastos estarán a cargo del autor del proyecto. No se incluyen licencias de software ya que todos los servicios utilizados cuentan con plan gratuito o código abierto compatible con un prototipo académico.

---

## Costos fijos (pagos únicos)

| Ítem | Descripción | Costo (USD) |
|---|---|---|
| Publicación extensión Chrome | Registro de cuenta de desarrollador en la tienda oficial de extensiones — habilitación para publicar en la store pública | $5 |
| Dominio web (opcional) | Dominio personalizado para el panel web. Reemplazable por subdominio gratuito durante el PFI | $15/año |
| **TOTAL FIJO OBLIGATORIO** | | **$5** |
| **TOTAL FIJO (con dominio)** | | **$20** |

---

## Costos mensuales (servicios recurrentes)

| Ítem | Descripción | Costo/mes (USD) |
|---|---|---|
| Hosting servidor web y base de datos | Servidor de la API always-on + base de datos PostgreSQL gestionada en la nube. Cubre el cómputo del servidor, no la inferencia del modelo de IA | $5 |
| Hosting módulo clasificador NLP | Cómputo en la nube para ejecutar el módulo de clasificación de lenguaje natural (XLM-T fine-tuneado) | $9 |
| Hosting panel web | Dashboard web para visualización de análisis históricos y reportes | $0 |
| Servicio de búsqueda web (Tavily) | Consultas a medios de noticias para el módulo de contraste semántico — 1.000 queries/mes en plan gratuito. Complementado con scraping directo de fuentes gubernamentales argentinas (Infoleg, INDEC, etc.) sin costo adicional | $0 |
| **TOTAL MENSUAL** | | **$14** |

**Proyección para el período del PFI (~12 meses):**
- Costo fijo obligatorio: **$5**
- Costo mensual × 12: **$168**
- **Total estimado período PFI: $173 USD**

> Si se requiere el dominio propio: **$188 USD** total para el período del PFI.

---

## Justificación por servicio

### Backend + Base de datos — Railway ($5/mes)

Railway es una plataforma de hosting que permite desplegar servicios en contenedores Docker con PostgreSQL gestionado incluido en el plan Hobby. Es la opción elegida por las siguientes razones:

- **Always-on**: a diferencia de alternativas gratuitas como Render o Fly.io en plan free, los servicios en Railway no se duermen por inactividad — crítico para una extensión Chrome que realiza llamadas en tiempo real mientras el usuario navega.
- **PostgreSQL incluido**: evita contratar una base de datos por separado.
- **FastAPI nativo**: compatibilidad directa con el stack del proyecto (Python + FastAPI).
- **$5/mes** es el costo del plan Hobby con 512 MB RAM, 1 GB de disco y 100 GB de ancho de banda — suficiente para un prototipo académico con carga baja.

Alternativas consideradas: Render Starter ($7/mes, sin PostgreSQL incluido), Fly.io Hobby ($0 base pero sin DB, más compleja de configurar).

---

### Frontend / panel web — Vercel (plan gratuito)

Vercel ofrece hosting gratuito para aplicaciones web estáticas y serverless, con integración directa con GitHub. El plan Free incluye:

- Despliegues ilimitados desde repositorio.
- 100 GB de ancho de banda mensual.
- Subdominio gratuito (`proyecto.vercel.app`) — suficiente para el MVP académico, elimina la necesidad del dominio propio durante el PFI.
- SSL automático.

El panel web del sistema (histórico de análisis, tendencias) no requiere procesamiento intensivo y puede servirse completamente desde Vercel, separado del backend en Railway.

---

### Cómputo de inferencia NLP — Hugging Face Pro ($9/mes)

La arquitectura propone un modelo XLM-T fine-tuneado sobre LIAR y FakeNewsNet en inglés —por transferencia cross-lingual, sin traducir—, FakeDeS en español y el corpus argentino propio, con RoBERTuito y BETO como líneas de comparación. El cómputo de inferencia **no puede correr en el mismo servidor que el backend**: Railway Hobby incluye 512 MB RAM, suficiente para FastAPI pero no para cargar un modelo transformer de ~125M parámetros (ocupa ~500 MB en memoria). Son dos costos de cómputo separados con funciones distintas.

**Por qué no alcanza el plan gratuito de HF**

El plan gratuito de Hugging Face Serverless tiene dos problemas para un prototipo que necesita funcionar en una demo presencial:

- **Cold starts**: la primera llamada al modelo puede tardar 20–60 segundos porque HF necesita cargar los pesos desde disco. En uso de desarrollo es tolerable; en una presentación académica es un problema.
- **Rate limiting no publicado**: HF no expone los límites exactos del free tier — puede cortarse en horarios pico sin aviso.

**Opciones evaluadas:**

| Servicio | Costo fijo | Notas |
|---|---|---|
| **Hugging Face Pro** ← elegido | $9/mes | Inferencia prioritaria, sin cold starts problemáticos, sin infraestructura que gestionar |
| Modal.com | $0 (primeros $30/mes en créditos) | GPU on-demand, pago por segundo, Python-nativo — agrega complejidad de setup |
| HF Dedicated Endpoint (auto-scale a 0) | ~$5–10/mes según uso | Más control, se apaga cuando no hay tráfico — opción de escalado si HF Pro no alcanza |
| Replicate | $0 fijo + pago por predicción | Sin costo mensual, pero latencia variable |

**Opción elegida: Hugging Face Pro ($9/mes)**

El plan Pro garantiza mayor prioridad en la cola de inferencia compartida, warm-up más rápido y límites de uso mucho más generosos. Para un prototipo académico con carga baja (el análisis lo dispara el usuario manualmente, no en batch) es el punto óptimo entre costo y confiabilidad.

**Opción alternativa si se necesita control total: Dedicated Endpoint (auto-scale a 0)**

| Configuración | Costo estimado |
|---|---|
| CPU (m4.xlarge) con auto-scale a 0 | ~$0.06/hora → **~$5–10/mes** si solo se usa en demos/testing |
| GPU T4 con auto-scale a 0 | ~$0.60/hora → solo necesario en producción real con alta carga |

El auto-scale a 0 apaga el endpoint cuando no hay tráfico, pagando solo por los minutos de inferencia efectiva. Viable si el plan Pro resulta insuficiente.

**Alternativa considerada: Modal.com** — plataforma serverless con GPU bajo demanda, primeros $30/mes gratis, Python-native. Viable si HF Pro tiene problemas, pero agrega complejidad de setup.

---

### Servicio de búsqueda web — arquitectura híbrida: Tavily + scraping directo

El módulo de contraste semántico utiliza dos estrategias complementarias para obtener fuentes que corroboren o contradigan el contenido analizado:

**Estrategia 1 — Tavily API (búsqueda general en medios)**

Tavily es una API de búsqueda diseñada específicamente para agentes de IA y pipelines de RAG. A diferencia de APIs de búsqueda genéricas, devuelve el contenido del artículo directamente (no solo el link y el snippet), lo que simplifica el pipeline de extracción. Plan gratuito: 1.000 queries/mes — suficiente para el MVP considerando que el scraping directo cubre las fuentes de mayor frecuencia de uso.

| Servicio | Plan gratuito | Costo si se supera | Notas |
|---|---|---|---|
| **Tavily** ← elegido | 1.000 queries/mes | $30/mes (10k queries) | Diseñado para IA/RAG, devuelve contenido completo, no solo links |
| Serper.dev | 2.500 queries/mes | $50/mes (50k queries) | Mayor volumen gratuito, resultados de Google, integración simple |
| Brave Search API | 2.000 queries/mes | $3/1.000 queries extra | Índice propio, más barato en escala |
| Google Custom Search | 100 queries/día | $5/1.000 queries extra | Límite diario muy restrictivo |

**Estrategia 2 — Scraping directo de fuentes gubernamentales argentinas (sin costo adicional)**

Para fuentes de autoridad institucional — que son las más relevantes para fact-checking en el contexto argentino — se implementa scraping directo. Estas fuentes son datos públicos del estado, sin restricciones de ToS para uso académico/investigación, y no requieren API externa. El scraping corre en el mismo servidor del backend sin costo adicional.

Fuentes a scrapear directamente:

| Fuente | URL | Contenido relevante |
|---|---|---|
| Infoleg | infoleg.gob.ar | Legislación argentina vigente — para verificar afirmaciones sobre leyes |
| INDEC | indec.gob.ar | Estadísticas oficiales (inflación, pobreza, empleo) — dato económico verificable |
| Casa Rosada | casarosada.gob.ar | Comunicados oficiales del Poder Ejecutivo |
| ANMAT | anmat.gov.ar | Aprobaciones de medicamentos, alertas sanitarias |
| BCRA | bcra.gob.ar | Datos monetarios y cambiarios oficiales |
| Chequeado | chequeado.com | Base de fact-checks existentes en español |

La combinación de Tavily (medios) + scraping gubernamental reduce el consumo de queries de API y mejora la calidad del contraste para el contexto argentino, que es el foco del sistema.

---

### Chrome Web Store — $5 (único)

Publicar la extensión en la Chrome Web Store requiere registrarse como desarrollador con un pago único de **$5 USD**. Esta cuenta es vitalicia y permite publicar extensiones ilimitadas. El fee no aplica si la extensión se distribuye solo de forma local (instalación desde repositorio para evaluación académica), pero se incluye en el presupuesto para habilitar la publicación pública como parte de la demostración del MVP.

---

## Resumen final

| Categoría | Concepto | Costo |
|---|---|---|
| **Fijo** | Publicación extensión Chrome | $5 USD |
| **Fijo (opcional)** | Dominio web | $15 USD/año |
| **Mensual** | Hosting servidor web y base de datos | $5 USD/mes |
| **Mensual** | Hosting panel web | $0 |
| **Mensual** | Hosting módulo clasificador NLP | $9 USD/mes |
| **Mensual** | Servicio de búsqueda web | $0 |
| | **Total mensual** | **$14 USD/mes** |
| | **Total período PFI (~12 meses)** | **$173 USD** |

## Referencias cruzadas
- [[wiki/proyecto/propuesta]]
- [[wiki/negocio/modelo-de-negocio]]
- [[wiki/negocio/analisis-financiero]]
- [[wiki/solucion/tecnologias]]
