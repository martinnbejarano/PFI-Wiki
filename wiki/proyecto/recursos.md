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
| Hosting módulo clasificador NLP | Cómputo en la nube para ejecutar el módulo de clasificación de lenguaje natural (BETO/XLM-RoBERTa fine-tuneado) | $9 |
| Hosting panel web | Dashboard web para visualización de análisis históricos y reportes | $0 |
| Servicio de búsqueda web | Consultas a buscadores para el módulo de contraste semántico — 2.500 queries/mes incluidas en plan gratuito | $0 |
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

La arquitectura propone un modelo BETO o XLM-RoBERTa fine-tuneado sobre datasets en español (LIAR + FakeNewsNet + datos argentinos). El cómputo de inferencia **no puede correr en el mismo servidor que el backend**: Railway Hobby incluye 512 MB RAM, suficiente para FastAPI pero no para cargar un modelo transformer de ~110M parámetros (BETO pesa ~440 MB solo en memoria). Son dos costos de cómputo separados con funciones distintas.

**Por qué no alcanza el plan gratuito de HF**

El plan gratuito de Hugging Face Serverless tiene dos problemas para un prototipo que necesita funcionar en una demo presencial:

- **Cold starts**: la primera llamada al modelo puede tardar 20–60 segundos porque HF necesita cargar los pesos desde disco. En uso de desarrollo es tolerable; en una presentación académica es un problema.
- **Rate limiting no publicado**: HF no expone los límites exactos del free tier — puede cortarse en horarios pico sin aviso.

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
