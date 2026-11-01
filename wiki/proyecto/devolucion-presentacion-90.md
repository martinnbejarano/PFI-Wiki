---
titulo: Devolución de la exposición del 90 %
tipo: proyecto
tags: [entrega-90, devolucion, jurado, defensa-final]
fuentes: [SA25.vtt (transcripción de la exposición del 31/10/2026)]
actualizado: 2026-11-01
---

# Devolución de la exposición del 90 % (31/10/2026)

Jurado: **Monzón, Nicolás Alberto** (presencial) y **Castiñeiras, José Ramón** (remoto). La transcripción automática atribuye casi todo a Monzón porque usaba el micrófono de la sala, así que también le asigna lo que dijo Martín. Lo de abajo se reconstruyó por contexto.

Valoración general: «bastante bien, me gusta mucho» (Monzón); «la presentación está sólida, la solución es muy interesante» (Castiñeiras). Ninguno objetó el problema, la arquitectura de módulos, la demo ni las limitaciones.

## 1. Observaciones del jurado

| # | Quién | Observación | Tipo |
|---|---|---|---|
| J1 | Monzón | Faltó decir unas palabras de cierre al final | Forma |
| J2 | Monzón | Si el user research dice que la gente quiere esto, ¿por qué hay un escenario que pierde plata? | Pregunta |
| J3 | Monzón | El modelo quizás debería apuntar también al individuo: «yo no soy una organización y me gustaría usarlo; me estás perdiendo como cliente» | Sugerencia de negocio |
| J4 | Monzón | Si X ya tiene los datos y se ahorra los viajes de red, ¿qué hace que tu sistema sea más rápido que el interno (Notas de la Comunidad)? | Pregunta |
| J5 | Monzón | ¿Cuál es la parte legal de manejar los datos de quien publicó? | Pregunta |
| J6 | Castiñeiras | La inversión inicial (~USD 1.700) es «flaca». Sumar costos operativos: registro de sociedad, de marca, contables e impositivos, **horas propias**. Algo como USD 8.000 para bancar los primeros meses y después el inversor ángel | **Corrección** |
| J7 | Monzón | Railway (como Heroku o Render) encarece y está pensado para quien no sabe de infraestructura. Para una tesis «te pueden matar con alguna pregunta en diciembre». Cambiar la arquitectura en el mes que queda, **en la implementación y en el documento** | **Corrección** |
| J8 | Monzón + Castiñeiras | Ni un VPS a mano (demasiado manual; hacerlo robusto lleva meses) ni Railway: un punto intermedio en AWS, GCP o Azure con servicios gestionados (Cloud Run o similar). Evaluar un par de alternativas y justificar | Sugerencia |

## 2. Cómo se respondió cada pregunta

**J2 · Escenario pesimista — parcial.** Se respondió que el ingreso depende de la adopción masiva. Faltaron dos cosas que están en el cap. 3: (a) la intención de uso de la encuesta no es adopción, y el pesimista es justamente el caso en que la adopción queda por debajo; (b) el financiamiento por tramos acota la pérdida, porque el segundo tramo solo se pide si se alcanza la adopción del neutral.

**J3 · Monetizar al individuo — respuesta que no está en el documento.** Se habló de un plan de USD 20 por mes con 500 análisis. **Ese plan no figura en la Tabla de precios (`tab:pricing`), ni en el modelo financiero, ni en las láminas.** En diciembre el jurado lo va a buscar en el documento.

**J4 · Velocidad frente a las Notas — bien encaminada, sin datos.** El argumento correcto se dijo: la demora de las Notas es humana (consenso), no de cómputo, y cubre solo lo viral. Faltaron los datos que ya estaban preparados (`presentacion/PREGUNTAS.md` §6): solo el 16,9 % de las publicaciones con nota propuesta llega a mostrarla, la mitad con más de 23 horas de demora. Y del lado de Factum: la señal de BETO en lote sobre todo lo visible (RNF-01: ≤ 2 s p95), análisis profundo con mediana de 8,5 s y caché instantánea. Convenía admitir que X podría hacerlo técnicamente (§16) y que la defensa es el criterio argentino de fuentes.

**J5 · Legal — floja.** Se dijo «guardamos el nombre y la información pública; la afirmación, anonimizada». La respuesta preparada (§14) es más sólida y conviene usarla: excepción de fuentes de acceso público de la Ley 25.326; la cuenta autora se **seudonimiza con HMAC**; no se agregan resultados por cuenta (art. 7, perfilado); el texto viaja al LLM sin el usuario y hay consentimiento de primer uso por la transferencia; el nivel severo se enuncia «contradicho por fuentes oficiales» por el art. 113 del Código Penal. Decir «guardamos el nombre» contradice al cap. 4.

**J6 · Inversión inicial — respuesta incompleta e incorrecta.** Se dijo «solo consideramos infraestructura». En realidad los USD 1.716 incluyen dominio, solicitud de marca en el INPI y USD 1.500 de asesoría legal que **ya contempla la constitución de la sociedad**. Parte de lo que pidió Castiñeiras ya estaba y no se dijo. Lo que sí falta: honorarios contables e impositivos y las horas del tesista en el año 0, que se excluyeron a propósito (decisión del 18/10 a partir de la clase del 03/10).

**J7/J8 · Railway — se defendió con «servicios independientes y fácil de integrar».** Las cuatro razones del cap. 4 (región UE por el art. 12 de la Ley 25.326, red privada, despliegue por CLI, cobro por uso) no se dijeron, y aun así el jurado pide cambiarlo.

## 3. Correcciones a la exposición (forma)

1. **Cierre:** se omitió la frase de memoria («El objetivo no es que el usuario le crea al veredicto, sino que pueda prescindir de él…»). Monzón lo notó (J1).
2. **Cifras dichas mal:** «fondos propios de 1.300 dólares» (son 1.716); «TIR del 74 %» (es 72,6 %).
3. **Pesimista:** no se nombró en la lámina de negocio y por eso llegó como pregunta. El guion lo trae: decirlo con el corte por tramos.
4. **No improvisar productos** que no están en el documento (plan de USD 20).
5. Se omitió «el precio de la API todavía no está validado con clientes» y las dos palancas de costo (tope y caché).
6. Persona: alterna «estoy construyendo», «nosotros» y «le damos». Elegir una sola (primera persona singular, porque el trabajo es individual).
7. Notas de la Comunidad: dar el 16,9 % y las 23 h en la exposición, no solo «varias horas».

## 4. Correcciones al documento

| # | Dónde | Qué cambiar | Origen |
|---|---|---|---|
| D1 | cap. 3, Tabla de supuestos e inversión del año 0 | Reabrir la decisión de no imputar horas. Sumar honorarios contables e impositivos (mensuales, desde la constitución) y un costo de horas del fundador para los meses previos al ingreso. Llevar la inversión al orden de USD 8.000 y recalcular VAN, TIR, *payback* y plan de financiamiento | J6 |
| D2 | cap. 3, Tabla `tab:pricing` y modelo financiero | Agregar un plan individual pago (p. ej., USD 20 por mes con 500 análisis). Costo a cuota llena: 500 × 0,0246 ≈ USD 12,3 por mes; el margen es positivo pero chico, así que conviene revisar la cuota o el precio. Modelar una tasa de conversión de gratuito a pago. Sube el pesimista | J3 + respuesta dada |
| D3 | cap. 4, despliegue (§ tecnologías y diagrama de despliegue) | Reemplazar Railway o, como mínimo, agregar una evaluación comparada (Railway, Cloud Run/AWS/Azure gestionado, VPS) con costo, operación, seguridad y región, y el plan de migración al escalar | J7, J8 |
| D4 | cap. 3, viabilidad legal | Verificar que diga explícitamente qué se guarda de la cuenta autora (HMAC) y qué no, para que coincida con lo que se dirá en la defensa | J5 |
| D5 | cap. 3, escenarios | Una oración que vincule el pesimista con la brecha entre intención (encuesta) y adopción real | J2 |
| D6 | cap. 3/4 | Las menciones a Railway Pro en los costos fijos (`financiero-supuestos.tex`, filas 46, 51, 52; `RailwayPrecios2026`) cambian si cambia el proveedor | D3 |

## 5. Correcciones al código (si se migra la infraestructura)

Restricciones que la migración debe respetar:

- **Región:** tiene que seguir en un país con legislación adecuada para el art. 12 de la Ley 25.326 (UE): GCP `europe-west4` (Países Bajos), AWS `eu-west-1` o Azure West Europe. São Paulo **no** sirve.
- **SQLite en volumen:** Cloud Run no tiene disco persistente para SQLite con escritura. O Cloud SQL (PostgreSQL + `pgvector`, migración que el cap. 4 ya anuncia para escalar) o una VM gestionada. Es el cambio más grande.
- **Red privada API → clasificador:** en Cloud Run, clasificador con *ingress* interno y autenticación IAM.
- **Cron de ingesta:** Cloud Scheduler en lugar del servicio `curlimages/curl` de Railway.
- **Costo:** con la API siempre encendida (min-instances 1) y el clasificador con 1,2 GB, Cloud Run puede costar **más** que los USD 13 actuales. Medirlo antes de afirmar que es más barato; el argumento a favor es la robustez y la defendibilidad, no necesariamente el precio.
- Archivos afectados: `prototipo/servicio/Procfile`, `prototipo/Makefile` (`make desplegar`), configuración de la base en `prototipo/servicio/app/`, URL del servicio en `prototipo/extension/`.

## 6. Respuestas listas para diciembre

- **«¿Por qué pierde el pesimista?»** La encuesta mide intención, no adopción. El pesimista supone una adopción menor: las ventas B2B arrancan recién al llegar a 5.000 usuarios activos (año 3), y hasta entonces corren sueldo e infraestructura sin ingresos. Por eso el financiamiento va en dos tramos: si no hay adopción, el segundo no se pide y la pérdida queda acotada.
- **«La inversión es muy baja.»** (Según lo que se decida en D1.)
- **«¿Por qué este proveedor de nube?»** (Según lo que se decida en D3: región adecuada, red privada, servicio gestionado sin administrar el sistema operativo, costo medido.)

## Referencias cruzadas
- [[wiki/proyecto/entrega-90-alcance]]
- [[wiki/negocio/analisis-financiero]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/tecnologias]]
- [[wiki/sintesis/feedback-exposiciones-90-otros-grupos]]

## Fuentes
- Transcripción `SA25.vtt` (fuera del repositorio)
- `presentacion/GUION.md`, `presentacion/PREGUNTAS.md`
