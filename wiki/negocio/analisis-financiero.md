---
titulo: Análisis Financiero
tipo: análisis
tags: [financiero, van, tir, payback, costos, supuestos, escenarios, borrador]
fuentes: [prototipo/servicio/app/configuracion.py, prototipo/servicio/app/proveedor/openai.py, prototipo/servicio/app/jerarquia.py, wiki/proyecto/recursos.md, documento/chapters/chapter03.tex]
actualizado: 2026-09-28
---

# Análisis Financiero

> **Estado:** supuestos cerrados como borrador para la clase de modelo de negocio del 03/10/2026 (#49). Los resultados (flujos, VAN, TIR, *payback*, punto de equilibrio) salen de la planilla `.xlsx` y del script de validación de #51, que leen esta página. Spec padre: #45.

## Cómo leer esta página

- Cada supuesto tiene una **clave** (columna `clave`) pensada para ser el nombre de la celda en la hoja *Supuestos* de la planilla.
- Los valores van por escenario: **Opt** (optimista), **Neu** (neutral), **Pes** (pesimista). Si una fila tiene un solo valor, vale para los tres.
- Moneda: **USD nominales**. Los montos en pesos se convierten al tipo de cambio oficial BNA vendedor del 28/09/2026, **ARS 1.545 por USD** (`ElCronista2026`).
- Fecha de consulta de todas las fuentes *online*: **2026-09-28**.
- Marcas: `[sin verificar]` = cifra sin fuente primaria confirmada; **supuesto propio** = decisión del autor sin fuente externa, que se defiende con el razonamiento que la acompaña.

---

## 1. Horizonte y calendario

| clave | Supuesto | Valor | Unidad | Fuente |
|---|---|---|---|---|
| `horizonte` | Horizonte de evaluación | 5 | años | Decisión de #45 (molde Sparkle, 3.4) |
| `anio_0` | Año 0 (inversión: desarrollo del PFI) | 2026 | año calendario | Supuesto propio |
| `anios_operacion` | Años 1 a 5 | 2027 a 2031 | año calendario | — |
| `periodicidad` | Flujo | anual, fin de período | — | (`SapagEtAl2014`) |
| `moneda` | Moneda | USD | — | Decisión de #45 |

### Años con elecciones nacionales en Argentina

La Cámara de Diputados se renueva por mitad cada dos años (art. 50 de la Constitución) (`ConvencionConstituyente1994`) y la próxima presidencial es el domingo 24/10/2027 (`LaNacion2026`). Con año 0 = 2026:

| Año del modelo | Año calendario | Elección nacional | `anio_electoral` |
|---|---|---|---|
| 0 | 2026 | No | 0 |
| 1 | 2027 | Sí: presidencial + legislativa | 1 |
| 2 | 2028 | No | 0 |
| 3 | 2029 | Sí: legislativa de medio término | 1 |
| 4 | 2030 | No | 0 |
| 5 | 2031 | Sí: presidencial + legislativa | 1 |

Los contratos de monitoreo electoral (sección 7) **solo** generan ingreso en los años con `anio_electoral = 1`.

---

## 2. Tasa de descuento: 25 % en USD

Se arma por componentes (*build-up*), como en (`SapagEtAl2014`) y (`RossEtAl2013`):

| clave | Componente | Valor | Fuente y fecha |
|---|---|---|---|
| `tasa_libre_riesgo` | Tasa libre de riesgo de EE. UU.: bono del Tesoro a 10 años (DGS10) | 5,17 % | FRED, dato del 25/09/2026, consultado el 28/09/2026 (`FederalReserve2026`) |
| `riesgo_pais` | Riesgo país de Argentina (EMBI de JP Morgan): 628 pb | 6,28 % | Infobae, 28/09/2026 (`Infobae2026`) |
| `prima_proyecto` | Prima por proyecto nuevo (residual) | 13,55 % | Supuesto propio, acotado por (`Damodaran2010`) |
| `tasa_descuento` | **Total** | **25,00 %** | Suma |

**Por qué la prima es razonable.** (`Damodaran2010`) recoge las tasas que exige el capital de riesgo según la etapa: entre 50 y 70 % para un *startup*, entre 40 y 60 % en la primera etapa y entre 35 y 50 % en la segunda. Un 25 % total queda **por debajo** del piso de esa escala. La prima de 13,55 puntos es más baja que la que exigiría un fondo porque el flujo ya incorpora el sueldo del desarrollador a tarifa de mercado (sección 3): el proyecto no descuenta el costo de oportunidad del trabajo en la tasa, lo paga en el flujo.

**Volatilidad declarada.** El riesgo país se movió mucho en el mes: mínimo del año de 403 pb el 07/07/2026 y máximo de 641 pb el 28/09/2026 (`Infobae2026`). El bono a 10 años tocó 5,23 %, su nivel más alto desde 2007. Con el riesgo país en 641 pb, la prima residual sería 13,42 %. La tasa se fija en 25 % y no se recalcula con cada dato diario: la prima absorbe la diferencia. Sparkle usó 15 %; este trabajo se aparta a propósito, por el riesgo país y por la etapa del proyecto (#45).

---

## 3. Recursos humanos: desarrollador semi senior a tarifa de mercado

| clave | Supuesto | Valor | Unidad | Fuente |
|---|---|---|---|---|
| `sueldo_ars` | Mediana del sueldo bruto mensual, rol *Developer*, semi senior (2 a 5 años de experiencia), sueldo no dolarizado | 2.501.629 | ARS/mes | Encuesta Sysarmy 2026.01, relevada entre diciembre de 2025 y febrero de 2026 y publicada el 04/03/2026 (`Sysarmy2026`) |
| `tc_encuesta` | Tipo de cambio implícito de la encuesta (mediana general ARS 3.253.581 = USD 2.327,51) | 1.397,88 | ARS/USD | (`Sysarmy2026`) |
| `sueldo_usd` | Sueldo bruto mensual en USD | **1.790** | USD/mes | Cálculo: 2.501.629 / 1.397,88 |
| `sueldos_por_anio` | Sueldos por año (12 + aguinaldo) | 13 | sueldos | Supuesto propio (relación de dependencia) |
| `costo_rrhh_anual` | Costo anual base | 23.270 | USD/año | 1.790 × 13 |
| `ajuste_sueldo` | Ajuste anual del sueldo en USD | 5 % | anual | Supuesto propio |
| `dedicacion` | Dedicación | 1 persona a tiempo completo, años 0 a 5 | FTE | Supuesto propio |
| `meses_anio_0` | Meses de desarrollo en el año 0 (marzo a diciembre de 2026) | 10 | meses | Cronograma del PFI |

Serie resultante: año 0: 10 × 1.790 × 13/12 = **19.392**. Año 1: 24.434. Año 2: 25.655. Año 3: 26.938. Año 4: 28.285. Año 5: 29.699 (USD, costo base × 1,05^t, sin redondeos intermedios).

**Notas.**
- La mediana del mismo rol con sueldo dolarizado es ARS 3.200.000 (≈ USD 2.289). Se toma la no dolarizada porque es la del mercado local al que pertenece el proyecto. Usar la dolarizada subiría el costo de RR. HH. un 28 %.
- **Cargas sociales patronales: no incluidas.** Se modela un único fundador que cobra el bruto. Si la cátedra pide costo empleador, hay que sumar las contribuciones patronales (tasa `[sin verificar]`) como un multiplicador sobre `costo_rrhh_anual`. Queda para la clase del 03/10.
- El 5 % de ajuste en USD es un supuesto propio: cubre la inflación en dólares y una recuperación moderada del salario real del sector.

---

## 4. Inversión del año 0

| clave | Concepto | Monto (USD) | Fuente |
|---|---|---|---|
| `inv_desarrollo` | Desarrollo: 10 meses de sueldo semi senior con aguinaldo proporcional | 19.392 | Sección 3 |
| `inv_infraestructura_0` | Infraestructura durante el PFI: 14 USD/mes × 12 | 168 | [[wiki/proyecto/recursos]], RNF-14 |
| `inv_dominio` | Dominio propio, primer año | 15 | [[wiki/proyecto/recursos]] `[sin verificar]` |
| `inv_chrome_web_store` | Alta como desarrollador en Chrome Web Store (cargo único) | 5 | La página oficial confirma que es un cargo único, pero no publica el monto (`Google2026`). Los USD 5 salen de fuentes secundarias `[sin verificar]` |
| `inv_marca_inpi` | Solicitud de marca «Trama» en el INPI, clases 9 y 42: 2 × 100 UMAPI × ARS 405,69 = ARS 81.138 | 53 | 100 UMAPI por clase (`INPI2026`). Valor de la UMAPI a septiembre de 2026 (ARS 405,69) tomado de fuente secundaria `[sin verificar]` |
| `inv_legal` | Asesoría legal: política de privacidad, términos de uso, adecuación a la Ley 25.326 y constitución de la sociedad | 1.500 | Supuesto propio `[sin verificar]` |
| `inversion_total` | **Total año 0** | **21.133** | Suma |

No hay compra de *hardware* ni licencias: todo el *stack* es servicio en la nube o software libre ([[wiki/proyecto/recursos]]).

---

## 5. Costos fijos por año (años 1 a 5)

### 5.1 Infraestructura

Parte de los **14 USD/mes actuales** (Railway Hobby 5 + Hugging Face PRO 9, RNF-14). A partir de la explotación comercial pasa a planes comerciales, porque los planes *hobby* de Railway y de Vercel no admiten uso comercial.

| clave | Concepto | Valor | Unidad | Fuente |
|---|---|---|---|---|
| `infra_railway` | Railway Pro (servicio, base de datos, ingesta programada), incluye USD 20 de uso | 20 | USD/mes | (`Railway2026`) |
| `infra_vercel` | Vercel Pro para el panel (1 asiento de desarrollo); el Hobby es «uso personal, no comercial» | 20 | USD/mes | (`Vercel2026`) |
| `infra_hf_pro` | Hugging Face PRO | 9 | USD/mes | (`HuggingFace2026`) |
| `infra_base` | **Base comercial** | **49** | USD/mes (588/año) | Suma |
| `infra_escalado` | Escalado con el volumen: uso adicional de Railway por cada 10.000 usuarios activos | 10 | USD/mes por 10.000 UA | Supuesto propio `[sin verificar]` |
| `dominio_anual` | Renovación del dominio | 15 | USD/año | [[wiki/proyecto/recursos]] `[sin verificar]` |

Fórmula: `infra_anual(t) = 12 × (infra_base + infra_escalado × UA(t) / 10.000) + dominio_anual`.

### 5.2 *Hosting* del modelo (clasificador propio de la Entrega 4)

Endpoint de inferencia dedicado en Hugging Face, encendido todo el año (8.760 h). El tamaño se elige según el volumen de cada escenario.

| clave | Instancia | Precio | Costo anual |
|---|---|---|---|
| `hosting_cpu` | CPU Intel Sapphire Rapids, 1 vCPU y 2 GB (AWS) | 0,03 USD/h | 262,80 USD |
| `hosting_gpu` | GPU NVIDIA T4, 14 GB (AWS) | 0,50 USD/h | 4.380,00 USD |

Fuente: (`HuggingFace2026`).

| Escenario | Año 1 | Año 2 | Año 3 | Año 4 | Año 5 |
|---|---|---|---|---|---|
| Opt | CPU | T4 | T4 | T4 | T4 |
| Neu | CPU | CPU | T4 | T4 | T4 |
| Pes | CPU | CPU | CPU | CPU | CPU |

### 5.3 Marketing (desde el año 1)

Supuesto propio. El presupuesto crece con la adopción y se concentra en los años electorales (línea 2 de la promoción en [[wiki/negocio/modelo-de-negocio]]).

| clave | Escenario | Año 1 | Año 2 | Año 3 | Año 4 | Año 5 |
|---|---|---|---|---|---|---|
| `marketing` | Opt | 6.000 | 9.000 | 12.000 | 15.000 | 18.000 |
| `marketing` | Neu | 4.000 | 6.000 | 8.000 | 10.000 | 12.000 |
| `marketing` | Pes | 2.000 | 3.000 | 4.000 | 5.000 | 6.000 |

(USD/año)

---

## 6. Costo variable: análisis a pedido

### 6.1 Costo por análisis

**No hay consumo medido.** El adaptador del proveedor (`prototipo/servicio/app/proveedor/openai.py`, `_registrar_consumo`) registra por llamada `fichas_entrada`, `fichas_salida` y `costo_usd`. Se buscaron líneas `proveedor | paso=…` en el repositorio y en los historiales de terminal del autor y no apareció ninguna. La única medición real registrada es la de latencia del 2026-08-28 (20,2 s), y no dejó el consumo de *tokens* anotado. **La cifra de esta sección es una estimación derivada del código y de los *prompts*: `[sin verificar]` hasta correr la prueba de humo que documenta `_registrar_consumo` y reemplazar estos números por los del registro.**

**Precios (verificados el 2026-09-28)** (`OpenAI2026`):

| clave | Concepto | Valor | Fuente |
|---|---|---|---|
| `precio_entrada` | `gpt-5.6-luna`, entrada de contexto corto | 0,20 USD / 1 M *tokens* | `configuracion.py` (consultado el 2026-08-25). La tabla oficial sigue igual al 2026-09-28 |
| `precio_salida` | `gpt-5.6-luna`, salida de contexto corto | 1,20 USD / 1 M *tokens* | Ídem |
| `precio_busqueda` | Herramienta `web_search`: USD 10 cada 1.000 llamadas, y el contenido recuperado se factura como *tokens* de entrada del modelo | 0,01 USD / llamada | (`OpenAI2026`) |

> ⚠️ CONTRADICCION: [[wiki/proyecto/recursos]] y [[wiki/negocio/modelo-de-negocio]] dicen que la búsqueda web es **Tavily**. El prototipo usa la herramienta `web_search` de la API de respuestas de OpenAI (`_herramienta_de_busqueda` en `openai.py`) y no llama a Tavily. El modelo financiero usa el precio de OpenAI, que es el que efectivamente se paga.

**Estructura de un análisis.** Hace tres llamadas a `gpt-5.6-luna` con esfuerzo de razonamiento `low`. Los *tokens* fijos se contaron con `tiktoken` (codificación `o200k_base`) sobre los *prompts* del adaptador:

| Paso | Entrada fija medida | Otros *tokens* de entrada (estimados) | Tope de salida |
|---|---|---|---|
| Extracción | 662 (instrucciones) | Esquema ≈ 150, tuit ≈ 80 | 900 |
| Evidencia (con `web_search`, contexto `medium`) | 672 (instrucciones) + 493 (100 dominios del filtro) | Esquema ≈ 150, afirmación ≈ 40, **contenido de búsqueda: variable** | 2.500 |
| Veredicto | 558 (instrucciones) | Esquema ≈ 150, fuentes y afirmación ≈ 250 | 900 |

La incertidumbre está en el contenido que trae la búsqueda y en la cantidad de búsquedas por análisis: la regla 6 del *prompt* de evidencia pide buscar lo que confirma y lo que desmiente, así que lo esperable son dos. Se arman tres estimaciones, una por escenario. El pesimista es el caro:

| clave | Supuesto | Opt | Neu | Pes |
|---|---|---|---|---|
| `tokens_entrada` | *Tokens* de entrada por análisis (3 pasos) | 6.220 | 11.220 | 18.220 |
| — | de los cuales, contenido de búsqueda | 3.000 | 8.000 | 15.000 |
| `tokens_salida` | *Tokens* de salida por análisis (incluye razonamiento) | 1.250 | 2.000 | 3.600 |
| `busquedas` | Llamadas a `web_search` por análisis | 1 | 2 | 3 |
| — | Costo de *tokens* (USD) | 0,0027 | 0,0046 | 0,0080 |
| — | Costo de búsqueda (USD) | 0,0100 | 0,0200 | 0,0300 |
| `costo_analisis` | **Costo por análisis (USD)** | **0,0127** | **0,0246** | **0,0380** |

Fórmula: `costo_analisis = tokens_entrada × precio_entrada / 1e6 + tokens_salida × precio_salida / 1e6 + busquedas × precio_busqueda`. **Fecha de la cifra: 2026-09-28, estimada y `[sin verificar]`.** Lo que más pesa es la búsqueda web (entre el 79 y el 81 % del costo), no los *tokens*. Una optimización que ahorre búsquedas vale más que cualquier cambio de modelo.

### 6.2 Usuarios activos, uso y tope diario

| clave | Supuesto | Escenario | Año 1 | Año 2 | Año 3 | Año 4 | Año 5 |
|---|---|---|---|---|---|---|---|
| `usuarios_activos` | Usuarios activos mensuales promedio del año (UA) | Opt | 5.000 | 20.000 | 50.000 | 100.000 | 150.000 |
| `usuarios_activos` | | Neu | 2.000 | 8.000 | 20.000 | 40.000 | 60.000 |
| `usuarios_activos` | | Pes | 500 | 2.000 | 5.000 | 8.000 | 10.000 |

| clave | Supuesto | Opt | Neu | Pes | Fuente |
|---|---|---|---|---|---|
| `analisis_por_ua_mes` | Análisis a pedido por usuario activo por mes | 20 | 12 | 6 | Supuesto propio. Referencia: el 61,4 % de la muestra entra a X al menos una vez por día y el 73,9 % se cruza con desinformación con frecuencia ([[wiki/investigacion/encuesta-resultados]]) |
| `tope_diario` | Tope de análisis por usuario gratuito por día | 20 | 20 | 20 | Supuesto propio. Acota el peor caso a 600 análisis por usuario por mes. No está implementado en el servicio (fuera de alcance según #45) |
| `tasa_reuso` | Análisis servidos desde la caché (RF-07: el mismo tuit pedido por otro usuario no se vuelve a pagar) | 30 % | 20 % | 10 % | Supuesto propio. Los tuits virales se piden muchas veces |

Fórmula: `costo_variable_b2c(t) = UA(t) × analisis_por_ua_mes × 12 × (1 − tasa_reuso) × costo_analisis`.

Los UA son un supuesto propio: no hay usuarios reales (PRODUCT.md, «Evidence on Hand»). El neutral del año 5 (60.000) es el 0,2 % de los 31,3 millones de usuarios de redes sociales en Argentina (`DataReportal2024`).

### 6.3 Costo variable del uso B2B de la API

Cada consulta a la API corre el mismo *pipeline*, así que cuesta lo mismo que un análisis ciudadano.

| clave | Supuesto | Opt | Neu | Pes |
|---|---|---|---|---|
| `consultas_pro_mes` | Consultas consumidas por cliente API Pro por mes (cuota de 50.000) | 2.000 | 4.000 | 8.000 |
| `consultas_ent_mes` | Consultas consumidas por cliente API Enterprise por mes | 20.000 | 40.000 | 80.000 |

Fórmula: `costo_variable_b2b(t) = Σ clientes_api × consultas_mes × 12 × (1 − tasa_reuso) × costo_analisis`.

> ⚠️ **Riesgo de precio que conviene llevar a la clase del 03/10.** Con el costo neutral (0,0246 USD), un cliente Pro que use toda su cuota de 50.000 consultas le cuesta al proyecto ≈ USD 1.230 por mes y paga USD 200. La tabla de precios del cap. 3 (`tab:pricing`) no cubre el costo marginal si la API corre la búsqueda web en cada consulta. Hay tres salidas: (a) que la API use solo el clasificador propio, sin búsqueda, cuyo costo es casi cero; (b) bajar la cuota del plan Pro; (c) subir el precio. Mientras no se decida, el modelo supone un uso parcial de la cuota (tabla de arriba).

---

## 7. Clientes B2B: universos, productos, captación y *churn*

### 7.1 Universos contables y producto que compra cada segmento

Los precios salen de la estructura de precios del cap. 3 (`tab:pricing`). Si el precio es un rango, se fija un valor por escenario.

| clave | Segmento | Universo | Fuente del universo | Producto (cap. 3) | Precio Opt | Precio Neu | Precio Pes |
|---|---|---|---|---|---|---|---|
| `u_medios_grandes` | Medios de gran porte (socios de ADEPA de alcance nacional) | 10 | Subconjunto de los 103 de abajo. Corte propio `[sin verificar]` | API, nivel superior | 3.000 | 2.500 | 1.500 USD/mes |
| `u_medios_chicos` | Resto de los medios socios de ADEPA con sitio web | 93 | Padrón de socios activos de ADEPA al 27/09/2026: 130 socios, 103 con sitio web (`ADEPA2026`). 103 − 10 = 93 | API, nivel intermedio | 200 | 200 | 200 USD/mes |
| `u_verificadores` | Organizaciones de verificación argentinas: Chequeado, Reverso, AFP Factual | 3 | Chequeado dirige LatamChequea y Reverso participa como observador (`LatamChequea2026`). Los tres son el escalón de verificaciones previas de `jerarquia.py` | Panel de tendencias + API intermedia | 500 | 500 | 500 USD/mes |
| `u_universidades` | Universidades, institutos universitarios y sus observatorios | 149 | 64 nacionales, 54 privadas con autorización definitiva, 19 privadas con autorización provisoria, 10 provinciales, 1 organismo internacional y 1 universidad extranjera, a mayo de 2026 (`SubsecretariaPoliticasUniversitarias2026`). Los observatorios fuera de universidades no se cuentan `[sin verificar]` | Acceso histórico al conjunto de datos | 100 | 100 | 100 USD/mes |
| `u_organismos` | Organismos públicos electorales y ONG | 32 | Cámara Nacional Electoral y 24 juzgados federales con competencia electoral (`MinisterioInterior2026`), Dirección Nacional Electoral, Defensoría del Público y 5 ONG (Poder Ciudadano, CIPPEC, ACIJ, Transparencia Electoral y Directorio Legislativo) `[sin verificar como compradores]` | Reportes de monitoreo electoral (por contrato) | 30.000 | 20.000 | 10.000 USD/contrato |
| `u_agencias` | Agencias de comunicación que atienden marcas | 120 | «+120 agencias socias, de todo el país» (`AgenciasArgentinas2026`) | API, nivel superior | 3.000 | 2.500 | 1.500 USD/mes |

El nivel inicial de la API (1.000 consultas gratis) no genera ingresos y su costo variable se considera marginal. No se modela.

### 7.2 Inicio de las ventas B2B

Por el efecto de red de datos, primero llega la adopción ciudadana y después se vende el dato.

| clave | Opt | Neu | Pes |
|---|---|---|---|
| `anio_inicio_b2b` | 1 (2027) | 2 (2028) | 3 (2029) |

En consecuencia, los contratos electorales caen en: **Opt:** 2027, 2029 y 2031. **Neu:** 2029 y 2031. **Pes:** 2029 y 2031.

### 7.3 Captación anual por segmento y escenario

Tasa sobre los **no clientes** del universo al inicio del año. Supuesto propio en todos los casos.

| clave | Segmento | Opt | Neu | Pes |
|---|---|---|---|---|
| `capt_medios_grandes` | Medios de gran porte | 20 % | 10 % | 5 % |
| `capt_medios_chicos` | Medios socios de ADEPA (resto) | 10 % | 5 % | 2 % |
| `capt_verificadores` | Verificadores | 40 % | 30 % | 20 % |
| `capt_universidades` | Universidades y observatorios | 8 % | 4 % | 2 % |
| `capt_organismos` | Organismos y ONG: fracción del universo que contrata en un año electoral | 10 % | 6 % | 3 % |
| `capt_agencias` | Agencias | 5 % | 2 % | 1 % |

### 7.4 *Churn* anual por segmento y escenario

Tasa sobre los clientes activos al inicio del año. Supuesto propio.

| clave | Segmento | Opt | Neu | Pes |
|---|---|---|---|---|
| `churn_medios_grandes` | Medios de gran porte | 10 % | 15 % | 25 % |
| `churn_medios_chicos` | Medios socios de ADEPA (resto) | 15 % | 20 % | 30 % |
| `churn_verificadores` | Verificadores | 0 % | 10 % | 20 % |
| `churn_universidades` | Universidades y observatorios | 5 % | 10 % | 15 % |
| `churn_organismos` | Organismos y ONG | n/a: contrato puntual, no hay suscripción | | |
| `churn_agencias` | Agencias | 15 % | 20 % | 30 % |

### 7.5 Reglas de cálculo para la planilla

Para cada segmento con suscripción, escenario y año `t ≥ anio_inicio_b2b`:

```
bajas(t)   = REDONDEAR(churn × activos_inicio(t); 0)
altas(t)   = REDONDEAR(captación × (universo − activos_inicio(t)); 0)
activos_fin(t) = activos_inicio(t) + altas(t) − bajas(t)
ingreso(t) = (activos_inicio(t) + activos_fin(t)) / 2 × precio_mensual × 12
```

- `activos_inicio(1) = 0`. Un cliente dado de baja vuelve al universo y puede recapturarse.
- Se redondea hacia el entero más cercano, con medio punto hacia arriba (`REDONDEAR` de Excel). El script de #51 tiene que redondear igual y **no** usar el `round` de Python, que redondea al par.
- Organismos: `contratos(t) = REDONDEAR(capt_organismos × u_organismos; 0)` si `anio_electoral(t) = 1` y `t ≥ anio_inicio_b2b`; si no, 0. `ingreso(t) = contratos(t) × precio_contrato`.
- El ingreso usa el promedio de clientes al inicio y al cierre (convención de mitad de año): el alta de un cliente no cuenta como doce meses de cobro.

---

## 8. Simplificaciones declaradas

- **Flujo antes de impuestos.** No se modelan ganancias, IVA ni ingresos brutos. Queda como limitación y se decide en la clase.
- **Sin valor residual** al final del año 5.
- **Sin capital de trabajo.** Las suscripciones se cobran por mes adelantado.
- **Precios B2B constantes en USD** durante el horizonte.
- **Un solo integrante.** No se suma personal de ventas: la venta B2B la hace el fundador, apoyado en el presupuesto de marketing.

## 9. Resultados

Pendientes de #51 (planilla `.xlsx` con fórmulas vivas y script de validación que genera las tablas LaTeX). No se transcriben números a mano.

---

## Referencias cruzadas

- [[wiki/negocio/modelo-de-negocio]]: segmentos, estructura de precios, mezcla de marketing
- [[wiki/proyecto/recursos]]: presupuesto del PFI (14 USD/mes), dominio, Chrome Web Store
- [[wiki/proyecto/entrega-90-alcance]]: criterio «Viabilidad económico-financiera»
- [[wiki/investigacion/encuesta-resultados]]: frecuencia de uso de X
- [[wiki/solucion/tecnologias]]

## Fuentes

Claves en `documento/biblio.bib`: `RossEtAl2013`, `SapagEtAl2014`, `Damodaran2010`, `FederalReserve2026`, `Infobae2026`, `Sysarmy2026`, `ElCronista2026`, `OpenAI2026`, `HuggingFace2026`, `Railway2026`, `Vercel2026`, `Google2026`, `INPI2026`, `SubsecretariaPoliticasUniversitarias2026`, `LatamChequea2026`, `AgenciasArgentinas2026`, `MinisterioInterior2026`, `ConvencionConstituyente1994`, `LaNacion2026`, `ADEPA2026`, `DataReportal2024`.

Código del prototipo:
- `prototipo/servicio/app/configuracion.py`: modelo y precios por millón de *tokens*
- `prototipo/servicio/app/proveedor/openai.py`: *prompts*, herramienta `web_search`, `_registrar_consumo`
- `prototipo/servicio/app/jerarquia.py`: padrón de ADEPA y verificadores
