---
titulo: Modelo de Negocio
tipo: análisis
tags: [negocio, canvas, propuesta-de-valor, segmentos, b2b, b2c, freemium, datos]
actualizado: 2026-06-13
---

# Modelo de Negocio

## Resumen ejecutivo

El sistema opera bajo un modelo **freemium con monetización B2B**. La extensión de Chrome es gratuita para el ciudadano común, y su uso masivo genera el activo central del negocio: un mapa en tiempo real de qué desinformación circula en Argentina, dónde y con qué intensidad. Ese mapa —que ningún competidor puede construir desde scraping de APIs— se vende como **API de detección** y **reportes de tendencias** a medios, organizaciones de fact-checking, centros de investigación, organismos públicos y marcas.

La lógica del negocio es de tipo **plataforma con efecto de red de datos**: cuanta más gente usa la extensión, más rico es el dataset, más valioso es el producto B2B, más recursos hay para mejorar el producto ciudadano, y así sucesivamente. La parte gratuita no es filantropía ni "loss leader" — es la fuente del dato que hace posible el producto pago.

---

## Qué se vende exactamente

No se vende la extensión. Se vende **información sobre qué desinformación está circulando en Argentina ahora mismo**. Esa información se entrega a los clientes B2B en dos formatos:

1. **API de detección** — endpoint que cualquier sistema externo puede consultar para clasificar un texto. Devuelve score de probabilidad de desinformación + evidencia (links a fuentes que corroboran o contradicen). Pricing por volumen de consultas.
2. **Reportes / dashboards de tendencias** — paneles que muestran qué temas falsos circulan esta semana, en qué plataformas, con qué intensidad, con qué patrones de propagación. Pricing por suscripción mensual.

Ambos productos se nutren del mismo dataset propietario, generado por el uso ciudadano de la extensión.

---

## Segmentos de clientes B2B

### 1. Medios de comunicación (Clarín, Infobae, La Nación, Página/12, Telam)

**Problema que les resuelve:** las redacciones tienen que decidir todos los días qué notas escribir. Si saben que "hoy hay 50.000 personas compartiendo un video falso sobre las elecciones", pueden escribir una nota de fact-check antes de que se descontrole. Hoy lo hacen a ojo o reaccionando tarde, cuando el daño ya ocurrió.

**Por qué pagan:** los reportes en tiempo real les dan ventaja editorial. Pueden anticiparse, captar tráfico SEO sobre el tema antes que la competencia, y posicionarse como referentes verificados.

### 2. Organizaciones de fact-checking (Chequeado.com, Reverso, AFP Factual)

**Problema que les resuelve:** Chequeado verifica manualmente y tiene recursos limitados — solo puede chequear unas pocas afirmaciones por día. El cuello de botella no es verificar, es **decidir qué verificar primero**.

**Por qué pagan:** el mapa les permite priorizar por impacto real. Pasan de elegir por intuición a elegir por dato — chequean lo que más circula, no lo que más les llama la atención. Multiplica su retorno por hora trabajada.

### 3. Centros de investigación / universidades / observatorios

**Problema que les resuelve:** los académicos que estudian desinformación, polarización política o comportamiento electoral necesitan datasets en español argentino. Hoy no existe un dataset bueno de desinformación argentina en tiempo real — usan datasets en inglés o snapshots manuales.

**Por qué pagan:** suscripciones institucionales para acceso histórico al dataset. Lo usan para papers, tesis, observatorios públicos. Mercado pequeño pero estable, y suma legitimidad académica al producto.

### 4. Organismos públicos y ONGs (Cámara Nacional Electoral, Defensoría del Público, Poder Ciudadano)

**Problema que les resuelve:** antes y durante elecciones necesitan monitorear desinformación electoral en vivo. Quieren saber qué narrativas falsas circulan sobre cada candidato, de qué cuentas salen, cuándo arrancó el pico. Hoy no tienen forma sistemática de saberlo.

**Por qué pagan:** contratos puntuales de monitoreo durante ciclos electorales (2025 legislativas, 2027 presidenciales). Volumen alto de revenue concentrado en ventanas cortas.

### 5. Marcas y agencias de comunicación corporativa

**Problema que les resuelve:** si circula una fake news sobre un producto ("este shampoo tiene cáncer", "esta fintech cerró"), la marca necesita detectarlo en horas, no en días. La inacción reputacional cuesta mucho más que la suscripción.

**Por qué pagan:** alertas en tiempo real cuando una narrativa falsa sobre la marca empieza a viralizar. Mercado más amplio que los anteriores, y usa exactamente la misma infraestructura técnica que los demás productos B2B.

---

## El moat: por qué nuestra data es mejor que la de los competidores

Cyabra, Blackbird.AI y Newtral FactFlow ya venden productos parecidos a clientes enterprise. La diferencia central está en **cómo obtienen la data**:

| | Competidores enterprise | Nuestra propuesta |
|---|---|---|
| Fuente de datos | Scraping de APIs públicas (Twitter/X, Facebook) | Sensor distribuido en miles de navegadores reales |
| Cobertura WhatsApp | Imposible (cifrado E2E, sin API) | Sí: si el usuario abre un link de WhatsApp en el navegador, queda registrado |
| Costo de adquisición de datos | Muy alto (Twitter API enterprise: USD 5.000-42.000/mes) | Cero — los usuarios analizan voluntariamente |
| Tipo de señal | Qué se publica | Qué se consume realmente |
| Cobertura de plataformas | Limitada a las que tienen API | Cualquier sitio donde el usuario navegue |

La extensión vive en el navegador del usuario, lo que da una ventaja estructural: registramos **lo que la gente está leyendo y atendiendo de verdad**, no solo lo que se publicó. Un post puede tener millones de impresiones y ser irrelevante; otro puede tener pocas pero estar circulando intensamente en grupos. Nuestro dato lo distingue.

Además, en Argentina **WhatsApp es el principal vector de difusión** (93% de penetración), y los competidores no pueden verlo. Nosotros sí, en la medida que los usuarios abran los links recibidos en su navegador.

---

## El bucle de red de datos

```
Más usuarios ciudadanos
        ↓
Más posts analizados
        ↓
Mapa más completo y en más plataformas
        ↓
Producto B2B más valioso
        ↓
Más revenue
        ↓
Mejor producto ciudadano (más features, más precisión, más plataformas)
        ↓
Más usuarios ciudadanos
        ↺
```

Este bucle es lo que hace **defendible** el negocio frente a competidores que entren después. El primer competidor que logra adopción ciudadana masiva acumula una ventaja de datos que se vuelve cada vez más difícil de igualar — fenómeno conocido como **data network effect**.

---

## Business Model Canvas

| Bloque | Contenido |
|---|---|
| **Propuesta de valor** | Para B2C: detección automática y gratuita de desinformación con evidencia explicable, mientras navegan. Para B2B: dataset propietario de tendencias de desinformación argentinas en tiempo real, accesible vía API y reportes. |
| **Segmentos de clientes** | B2C: usuarios argentinos de Twitter/X que consumen noticias (segmento de validación primario: 18-40 años, política y economía; abierto al público general). B2B: medios de comunicación, fact-checkers, centros de investigación, organismos públicos / ONGs, marcas y agencias corporativas. |
| **Canales** | B2C: Chrome Web Store, sitio web del producto, prensa y redes sociales. B2B: ventas directas (outbound), sitio institucional, alianzas con asociaciones (ADEPA, FOPEA, Chequeado). |
| **Relación con clientes** | B2C: self-service, comunidad, soporte por email. B2B chico: self-service con suscripción mensual. B2B enterprise (medios grandes, gobierno): account manager dedicado, contrato anual, SLAs. |
| **Fuentes de ingreso** | API por volumen de consultas (tiered pricing). Suscripciones mensuales a reportes/dashboards. Contratos enterprise (anual). Contratos puntuales de monitoreo electoral. |
| **Recursos clave** | (1) Dataset propietario de tendencias de desinformación argentinas, (2) modelo NLP entrenado en español rioplatense, (3) base de usuarios ciudadanos que alimenta el dataset, (4) marca y reputación de imparcialidad. |
| **Actividades clave** | Mantener y mejorar el modelo NLP. Mantener la extensión y la API. Generar reportes y dashboards. Ventas B2B. Comunicación con la base ciudadana. Cumplimiento legal (LPDP, ToS de plataformas). |
| **Socios clave** | Chequeado.com (sinergia, posible cliente y partner académico). Medios confiables (fuentes de verificación). HuggingFace (hosting del modelo). Tavily (API de búsqueda web). Universidades (UADE, UBA — investigación y validación). |
| **Estructura de costos** | Infraestructura cloud (Railway backend+DB, Vercel frontend, HF Inference API). Web Search API (Tavily). Ventas y marketing B2B. Desarrollo y mantenimiento. Cumplimiento legal. Costos crecen con volumen, pero margen mejora con escala. |

---

## Modelo de pricing tentativo

Estos números son referenciales y se afinarán con validación de mercado:

| Producto | Segmento | Precio tentativo |
|---|---|---|
| Extensión Chrome | Ciudadano común | Gratuito |
| API de detección — Free tier | Devs, pruebas | 1.000 consultas/mes gratis |
| API de detección — Pro | Medios chicos, fact-checkers | USD 200/mes (50.000 consultas) |
| API de detección — Enterprise | Medios grandes, marcas | USD 1.500-5.000/mes (volumen alto + SLAs) |
| Dashboard de tendencias | Fact-checkers, observatorios | USD 300/mes |
| Reportes electorales | Organismos públicos, ONGs | USD 10.000-50.000 por contrato (3-6 meses) |
| Acceso histórico al dataset | Universidades, investigación | USD 100/mes (suscripción institucional) |

---

## Análisis FODA

| | Positivo | Negativo |
|---|---|---|
| **Interno** | **Fortalezas:** Dataset diferencial imposible de replicar sin adopción ciudadana. Foco local (español rioplatense, fuentes argentinas). Evidencia explicable, no solo veredicto binario. Costos operativos bajos (USD 168 en el período del PFI). | **Debilidades:** Pre-revenue — el modelo depende íntegramente de lograr adopción ciudadana. Riesgo de falsos positivos (sátira, ironía). Equipo chico (1 integrante en PFI). Modelo NLP requiere entrenamiento y validación continua. |
| **Externo** | **Oportunidades:** Ciclos electorales recurrentes (2025, 2027) con alta demanda de monitoreo. IA generativa como vector creciente. Ausencia de competidor local con foco ciudadano. Tendencia regulatoria global hacia transparencia algorítmica favorece productos con evidencia explicable. | **Amenazas:** Regulación (LPDP — manejo de datos de uso). Cambios en APIs de redes sociales que limiten extracción. Competidores establecidos (Cyabra, Blackbird) pivotando hacia segmento ciudadano. Politización del producto — riesgo reputacional si se percibe sesgo. |

---

## Cruz de Porter / 5 Fuerzas

- **Rivalidad entre competidores:** Media. Los competidores enterprise (Cyabra, Blackbird, Newtral FactFlow) operan en segmentos diferentes (gobierno y redacciones grandes). En el segmento ciudadano local prácticamente no hay competencia directa.
- **Poder de negociación de los clientes B2B:** Alto al inicio (somos nuevos, ellos tienen alternativas), bajo a medida que el dataset se vuelve insustituible. Mitigación: contratos anuales, integración profunda en sus workflows.
- **Poder de negociación de los proveedores:** Medio. Dependemos de Chrome Web Store (Google), HuggingFace y APIs de búsqueda. Riesgo de cambios de pricing o políticas. Mitigación: arquitectura modular, opciones de fallback.
- **Amenaza de nuevos entrantes:** Media-baja. La barrera de entrada técnica es baja (modelos open-source disponibles), pero la barrera de **datos** es alta y crece con el tiempo (efecto de red).
- **Amenaza de productos sustitutos:** Alta. Sustitutos directos: chequeo manual (Chequeado), búsqueda en Google, plataformas como Community Notes de X. Sustituto fuerte a futuro: si las plataformas integran detección nativa. Mitigación: foco local + evidencia explicable + cobertura cross-plataforma.

---

## Misión y Visión

**Misión:** Hacer accesible para todo ciudadano argentino una herramienta automática y explicable que le permita identificar desinformación mientras consume contenido digital, y construir sobre esa base el primer mapa en tiempo real de tendencias de desinformación local.

**Visión:** Ser el sensor de referencia del ecosistema informativo argentino — la fuente que medios, fact-checkers, académicos y organismos públicos consultan cuando necesitan saber qué desinformación está circulando, dónde y con qué intensidad.

---

## Riesgos clave del modelo

1. **Riesgo de adopción:** todo el modelo depende de lograr una base ciudadana significativa. Sin usuarios no hay dataset, y sin dataset el producto B2B pierde su diferencial. Mitigación: estrategia de lanzamiento orientada a partners (Chequeado, medios académicos) y campañas de prensa en ciclos electorales.
2. **Riesgo regulatorio:** la LPDP argentina y eventuales regulaciones sobre monitoreo de redes pueden limitar el manejo de datos de uso. Mitigación: anonimización por diseño, transparencia total con el usuario, asesoría legal.
3. **Riesgo reputacional:** un producto que clasifica contenido como "sospechoso" puede ser percibido como sesgado políticamente. Mitigación: evidencia explicable (no veredictos binarios), comité asesor plural, código abierto del modelo.
4. **Riesgo competitivo:** un competidor enterprise (Cyabra) podría lanzar una extensión gratuita y replicar la estrategia. Mitigación: ventaja de primer movimiento + foco local profundo + bucle de red de datos que se acelera con tiempo.

---

## Referencias cruzadas

- [[wiki/proyecto/propuesta]]
- [[wiki/negocio/analisis-financiero]]
- [[wiki/competencia/analisis-competitivo]]
- [[wiki/investigacion/user-research]]
- [[wiki/proyecto/restricciones-legales-eticas]]
