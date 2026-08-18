---
titulo: Recursos — Presupuesto estimado
tipo: proyecto
tags: [presupuesto, infraestructura, cloud, recursos]
fuentes: []
actualizado: 2026-08-11
---

# Recursos — Presupuesto estimado

Los recursos financieros del proyecto se dividen en dos categorías: costos fijos (pagos únicos, no recurrentes) y costos mensuales (servicios de infraestructura en la nube). Los gastos estarán a cargo del autor del proyecto. No se incluyen licencias de software ya que todos los servicios utilizados cuentan con plan gratuito o código abierto compatible con un prototipo académico.

---

## Costos fijos (pagos únicos)

| Ítem | Descripción | Costo (USD) | Se ejecuta durante el PFI |
|---|---|---|---|
| Dominio web (opcional) | Dominio personalizado para el panel web. Reemplazable por subdominio gratuito durante el PFI | $15/año | No |
| Registro de desarrollador en la Chrome Web Store | Cargo único de habilitación para publicar. **No se ejecuta:** la extensión se distribuye sin empaquetar, en modo desarrollador | `[sin verificar]` | No |
| **TOTAL FIJO OBLIGATORIO** | | **$0** | |

**No hay costo fijo obligatorio durante el PFI.** La extensión no se publica en la tienda: se distribuye sin empaquetar, en modo desarrollador, para la demostración y la defensa, que es funcionalmente idéntico a una extensión publicada a los fines de una exposición y no exige cargo, ni revisión, ni política de privacidad. El razonamiento completo está en [[wiki/proyecto/restricciones-legales-eticas]].

**El monto del cargo de registro queda `[sin verificar]` a propósito.** Ninguna página de documentación de Google lo publica: el acuerdo lo describe como un cargo único «por un monto determinado a exclusivo criterio de Google», y la cifra solo se ve en la pantalla de registro de la consola de desarrollador. La cifra de USD 5 que este archivo afirmaba circula en foros y no tiene fuente oficial. O se verifica entrando a la consola, o el documento dice «cargo único, monto según la tienda» sin número — un monto sin fuente en una tabla de presupuesto es exactamente lo que un evaluador comprueba.

Se reclasifica como **costo fijo y único de lanzamiento**, diferido fuera del período del PFI. RNF-14 limita solo el gasto **mensual**, así que un fijo diferido no lo compromete, y el análisis financiero conserva el costo real de salida al mercado.

---

## Costos mensuales (servicios recurrentes)

| Ítem | Descripción | Costo/mes (USD) |
|---|---|---|
| Hosting servidor web y base de datos | Servidor de la API always-on + base de datos PostgreSQL gestionada en la nube. Cubre el cómputo del servidor, no la inferencia del modelo de IA | $5 |
| Hosting módulo clasificador NLP | Cómputo en la nube para ejecutar el módulo de clasificación de lenguaje natural (XLM-T fine-tuneado) | $9 |
| Hosting panel web | Dashboard web para visualización de análisis históricos y reportes | $0 |
| Servicio de búsqueda web (Tavily) | Consultas a medios de noticias para el módulo de contraste semántico — 1.000 queries/mes en plan gratuito. Complementado con el índice propio de fuentes oficiales, que mantiene una tarea programada sin costo mensual adicional | $0 |
| **TOTAL MENSUAL** | | **$14** |

**Proyección para el período del PFI (~12 meses):**
- Costo fijo obligatorio: **$0**
- Costo mensual × 12: **$168**
- **Total estimado período PFI: $168 USD**

> Si se requiere el dominio propio: **$183 USD** total para el período del PFI.

---

## Justificación por servicio

### Backend + Base de datos — Railway ($5/mes)

Railway es una plataforma de hosting que permite desplegar servicios en contenedores Docker con PostgreSQL gestionado incluido en el plan Hobby. Es la opción elegida por las siguientes razones:

- **Always-on**: a diferencia de alternativas gratuitas como Render o Fly.io en plan free, los servicios en Railway no se duermen por inactividad — crítico para una extensión Chrome que realiza llamadas en tiempo real mientras el usuario navega.
- **PostgreSQL incluido**: evita contratar una base de datos por separado.
- **FastAPI nativo**: compatibilidad directa con el stack del proyecto (Python + FastAPI).
- **$5/mes** es el costo del plan Hobby, que incluye USD 5 de crédito de uso con facturación por consumo. No impone un techo de memoria: el límite efectivo para un prototipo académico con carga baja es ese crédito, no una cifra de RAM.

Alternativas consideradas: Render Starter ($7/mes, sin PostgreSQL incluido), Fly.io Hobby ($0 base pero sin DB, más compleja de configurar).

---

### Frontend / panel web — Vercel (plan gratuito)

Vercel ofrece hosting gratuito para aplicaciones web estáticas y serverless, con integración directa con GitHub. El plan Hobby incluye:

- Despliegues ilimitados desde repositorio.
- 100 GB de ancho de banda mensual.
- Subdominio gratuito (`proyecto.vercel.app`) — suficiente para el MVP académico, elimina la necesidad del dominio propio durante el PFI.
- SSL automático.

El panel web del sistema (histórico de análisis, tendencias) no requiere procesamiento intensivo y puede servirse completamente desde Vercel, separado del backend en Railway.

**El plan Hobby restringe el uso a fines personales y no comerciales, y ese cero necesita su cláusula.** El panel es donde vive RF-14, la vista de tendencias para organizaciones con plan y cuota, así que la restricción es pertinente y conviene enunciarla antes que esconderla. Se aplica el mismo corte que el proyecto usa para la publicación en la tienda: **durante el PFI el panel no presta servicio comercial**, porque no hay cliente, no hay facturación y no hay suscripción vigente. El plan Pro, a USD 20 mensuales por usuario, corresponde a la explotación comercial, que está fuera del alcance del prototipo y entra en el análisis financiero como costo de producto y no de PFI. Presupuestarlo ahora rompería el techo de RNF-14 por un beneficio nulo: no hay clientes a los que servir.

---

### Cómputo de inferencia NLP — Hugging Face Pro ($9/mes)

La arquitectura propone un modelo XLM-T fine-tuneado sobre LIAR y FakeNewsNet en inglés —por transferencia cross-lingual, sin traducir—, FakeDeS en español y el corpus argentino propio, con RoBERTuito y BETO como líneas de comparación. El cómputo de inferencia **no conviene que corra en el mismo servidor que el backend, y el motivo es de presupuesto y no de memoria**: el plan Hobby de Railway factura por consumo sobre un crédito mensual de USD 5, y un contenedor con un transformer de ~125M parámetros residente consume memoria de forma continua y quema ese crédito en cuestión de días. La inferencia bajo demanda, en cambio, se paga por invocación. Son dos costos de cómputo separados con funciones distintas, y el techo que decide es RNF-14.

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

### Servicio de búsqueda web — arquitectura híbrida: Tavily + índice propio

El módulo de contraste semántico utiliza dos estrategias complementarias para obtener fuentes que corroboren o contradigan el contenido analizado:

**Estrategia 1 — Tavily API (búsqueda general en medios)**

Tavily es una API de búsqueda diseñada específicamente para agentes de IA y pipelines de RAG. A diferencia de APIs de búsqueda genéricas, devuelve el contenido del artículo directamente (no solo el link y el snippet), lo que simplifica el pipeline de extracción. Plan gratuito: 1.000 queries/mes — suficiente para el MVP considerando que el índice propio de fuentes oficiales cubre, sin consumir consultas, las fuentes de mayor frecuencia de uso.

| Servicio | Plan gratuito | Costo si se supera | Notas |
|---|---|---|---|
| **Tavily** ← elegido | 1.000 queries/mes | $30/mes (10k queries) | Diseñado para IA/RAG, devuelve contenido completo, no solo links |
| Serper.dev | 2.500 queries/mes | $50/mes (50k queries) | Mayor volumen gratuito, resultados de Google, integración simple |
| Brave Search API | 2.000 queries/mes | $3/1.000 queries extra | Índice propio, más barato en escala |
| Google Custom Search | 100 queries/día | $5/1.000 queries extra | Límite diario muy restrictivo |

**Estrategia 2 — Ingesta programada de las fuentes oficiales argentinas (sin costo adicional)**

Para las fuentes de autoridad institucional —las más relevantes para la verificación en el contexto argentino— el sistema mantiene un índice local propio (RF-05). **No se consultan en vivo dentro de la petición del usuario**: una tarea programada las recorre cada tanto, respeta el `crawl-delay` declarado por cada sitio y vuelca los documentos al índice. El motivo y sus consecuencias están en [[wiki/solucion/arquitectura]].

Corre como tarea programada de Railway, que se factura por tiempo de ejecución y no como un servicio siempre encendido: **no agrega costo mensual al presupuesto**. La afirmación anterior de este archivo —que el *scraping* corría en el mismo servidor del backend— dejó de ser cierta con esa decisión.

Las seis fuentes son las mismas que enumera RF-05, y esta tabla dejó de listar otras:

| Fuente | Dominio | Tipo de afirmación que cubre |
|---|---|---|
| InfoLEG | `infoleg.gob.ar` | Normativa — legislación argentina vigente |
| INDEC | `indec.gob.ar` | Dato económico — inflación, pobreza, empleo |
| BCRA | `bcra.gob.ar` | Dato económico — datos monetarios y cambiarios |
| Boletín Oficial | `boletinoficial.gob.ar` | Normativa — primera sección |
| Ministerio de Salud | `argentina.gob.ar` | Salud |
| Ministerio de Educación | `argentina.gob.ar` | Educación |

**Chequeado sale de esta tabla.** El sitio responde 403 a todo cliente que no sea un navegador, incluido el pedido de su propio `robots.txt`: el bloqueo es de infraestructura y es deliberado. RF-05 se cubre igual, con lo que el servicio de búsqueda ya tiene indexado y con la cita enlazada al artículo original. Eludir el bloqueo se evaluó y se descartó, por los motivos que desarrolla [[wiki/proyecto/restricciones-legales-eticas]].

**Casa Rosada y ANMAT también salen.** Estaban en esta tabla y no en RF-05, que es la lista autoritativa: sus contenidos quedan cubiertos por el Boletín Oficial y por el Ministerio de Salud respectivamente, y sostener dos listas distintas de fuentes oficiales en dos páginas era una contradicción esperando a que alguien la encontrara.

La combinación de Tavily para los medios y del índice propio para las fuentes oficiales reduce el consumo de consultas de la API de búsqueda y mejora la calidad del contraste para el contexto argentino, que es el foco del sistema.

---

### Chrome Web Store — costo diferido, fuera del período del PFI

Publicar la extensión requiere registrarse como desarrollador con un cargo único, que habilita publicaciones ilimitadas. **Durante el PFI no se publica**, así que ese cargo no se ejecuta: la extensión se distribuye sin empaquetar, en modo desarrollador, que en una demostración se ve idéntica a una publicada.

La decisión no es de presupuesto sino legal y de calendario. Publicar habría traído, sin salida posible, una política de privacidad y una pantalla de consentimiento —Google cuenta como *user data* el contenido de los sitios con los que el usuario interactúa, y aclara que el tratamiento local no exime—, y las tres variantes de visibilidad pagan el mismo cargo y pasan la misma revisión. Esa revisión declara una ventana de «unos días, hasta algunas semanas», con umbral de escalamiento a las tres semanas, y una extensión de desarrollador nuevo que lee contenido de una red social y lo envía a un servidor propio cae en varios de los factores agravantes que Google enumera. La fecha de aprobación no la controla el proyecto.

Queda registrado como **costo fijo y único de lanzamiento**, con su monto `[sin verificar]` por las razones de la tabla de costos fijos.

---

## Resumen final

| Categoría | Concepto | Costo |
|---|---|---|
| **Mensual** | Hosting servidor web, base de datos e ingesta programada | $5 USD/mes |
| **Mensual** | Hosting panel web (plan Hobby, uso no comercial) | $0 |
| **Mensual** | Hosting módulo clasificador NLP y codificador de *embeddings* | $9 USD/mes |
| **Mensual** | Servicio de búsqueda web | $0 |
| | **Total mensual** | **$14 USD/mes** |
| | **Total período PFI (~12 meses)** | **$168 USD** |
| **Diferido** | Registro de desarrollador en la Chrome Web Store | `[sin verificar]`, fuera del PFI |
| **Diferido (opcional)** | Dominio web | $15 USD/año |

## Referencias cruzadas
- [[wiki/proyecto/propuesta]]
- [[wiki/negocio/modelo-de-negocio]]
- [[wiki/negocio/analisis-financiero]]
- [[wiki/solucion/tecnologias]]
