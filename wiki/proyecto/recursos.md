---
titulo: Recursos — Presupuesto estimado
tipo: proyecto
tags: [presupuesto, infraestructura, cloud, recursos]
fuentes: []
actualizado: 2026-04-22
---

# Recursos — Presupuesto estimado

Los recursos financieros del proyecto se dividen en dos categorías: costos fijos (pagos únicos, no recurrentes) y costos mensuales (servicios de infraestructura en la nube). Los gastos estarán a cargo del autor del proyecto. No se incluyen licencias de software ya que todos los servicios utilizados cuentan con plan gratuito o código abierto compatible con un prototipo académico.

---

## Costos fijos (pagos únicos)

| Ítem | Servicio | Descripción | Costo (USD) |
|---|---|---|---|
| Publicación extensión Chrome | Google Chrome Web Store | Registro de cuenta de desarrollador — habilitación para publicar en la store pública | $5 |
| Dominio web (opcional) | Namecheap / similar | Dominio personalizado para el panel web (ej. `infoverify.ar`). Reemplazable por subdominio gratuito de Vercel durante el PFI | $15/año |
| **TOTAL FIJO OBLIGATORIO** | | | **$5** |
| **TOTAL FIJO (con dominio)** | | | **$20** |

---

## Costos mensuales (servicios recurrentes)

| Ítem | Servicio | Descripción | Costo/mes (USD) |
|---|---|---|---|
| Hosting backend + base de datos | Railway (plan Hobby) | Servidor FastAPI siempre activo + PostgreSQL gestionado | $5 |
| Hosting frontend / panel web | Vercel (plan Free) | Dashboard web (React/Next.js), 100 GB de ancho de banda incluidos | $0 |
| Inferencia modelo NLP | Hugging Face Inference API (serverless) | Inferencia del modelo BETO/XLM-RoBERTa fine-tuneado, plan gratuito con rate limiting | $0 |
| API de búsqueda web | Serper.dev (plan Free) | Consultas a Google Search para el módulo de contraste semántico — 2.500 queries/mes incluidas | $0 |
| **TOTAL MENSUAL** | | | **$5** |

**Proyección para el período del PFI (~12 meses):**
- Costo fijo obligatorio: **$5**
- Costo mensual × 12: **$60**
- **Total estimado período PFI: $65 USD**

> Si se requiere el dominio propio: **$80 USD** total para el período del PFI.

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

### Inferencia modelo NLP — Hugging Face Inference API

La arquitectura propone un modelo BETO o XLM-RoBERTa fine-tuneado sobre datasets en español (LIAR + FakeNewsNet + datos argentinos). Para la inferencia en producción se utiliza la plataforma Hugging Face.

**Opción elegida para el MVP: Hugging Face Serverless Inference API (gratuito)**

Hugging Face provee inferencia serverless sobre modelos alojados en su Hub sin costo para modelos públicos, con rate limiting generoso para uso de baja frecuencia. Para un prototipo académico donde las inferencias son puntuales (el usuario activa el análisis manualmente desde la extensión), este plan es suficiente durante todo el período del PFI.

**Opción de escalado si el plan gratuito resulta insuficiente: Dedicated Endpoints**

Si el rate limiting del plan gratuito impide el uso normal del prototipo, Hugging Face ofrece endpoints dedicados:

| Configuración | Costo estimado |
|---|---|
| CPU (m4.xlarge) con auto-scale a 0 | ~$0.06/hora → **~$10–20/mes** según uso |
| GPU T4 con auto-scale a 0 | ~$0.60/hora → **~$30–60/mes** según uso |

El auto-scale a 0 significa que el endpoint se apaga cuando no recibe tráfico, pagando solo por los minutos de inferencia efectiva — ideal para un prototipo con uso esporádico.

**Alternativa considerada: Modal.com** — plataforma serverless con GPU bajo demanda. Incluye $30/mes gratis, Python-native, más fácil de integrar con código propio. Viable como alternativa si HF Serverless muestra limitaciones.

---

### API de búsqueda web — Serper.dev (plan gratuito)

El módulo de contraste semántico necesita consultar Google Search en tiempo real para obtener artículos de medios confiables que corroboren o contradigan el contenido analizado. Para esto se require una API de búsqueda estructurada.

**Opciones evaluadas:**

| Servicio | Plan gratuito | Costo si se supera | Notas |
|---|---|---|---|
| **Serper.dev** ← elegido | 2.500 queries/mes | $50/mes (50k queries) | Resultados de Google, REST simple, muy usado con Python/LangChain |
| Brave Search API | 2.000 queries/mes | $3/1.000 queries extra | Privacidad, buena calidad, alternativa viable |
| Google Custom Search API | 100 queries/día (3.000/mes) | $5/1.000 queries extra | Oficial de Google pero más burocrático de configurar |
| Scraping directo | — | — | ❌ Viola ToS de Google, frágil, no recomendado |

**Justificación de Serper.dev:** ofrece el mayor volumen gratuito (2.500 queries/mes), integración REST directa con FastAPI/Python, y devuelve resultados de Google en formato JSON estructurado — el mismo que se necesita para extraer snippets y URLs de medios confiables. Para el MVP académico con carga baja, el plan gratuito es suficiente sin incurrir en costos adicionales.

---

### Chrome Web Store — $5 (único)

Publicar la extensión en la Chrome Web Store requiere registrarse como desarrollador con un pago único de **$5 USD**. Esta cuenta es vitalicia y permite publicar extensiones ilimitadas. El fee no aplica si la extensión se distribuye solo de forma local (instalación desde repositorio para evaluación académica), pero se incluye en el presupuesto para habilitar la publicación pública como parte de la demostración del MVP.

---

## Resumen final

| Categoría | Concepto | Costo |
|---|---|---|
| **Fijo** | Chrome Web Store developer fee | $5 USD |
| **Fijo (opcional)** | Dominio web | $15 USD/año |
| **Mensual** | Railway (backend + PostgreSQL) | $5 USD/mes |
| **Mensual** | Vercel (frontend) | $0 |
| **Mensual** | Hugging Face Inference API | $0 (plan gratuito) |
| **Mensual** | Serper.dev (web search) | $0 (plan gratuito) |
| | **Total mensual** | **$5 USD/mes** |
| | **Total período PFI (~12 meses)** | **$65 USD** |

## Referencias cruzadas
- [[wiki/proyecto/propuesta]]
- [[wiki/negocio/modelo-de-negocio]]
- [[wiki/negocio/analisis-financiero]]
- [[wiki/solucion/tecnologias]]
