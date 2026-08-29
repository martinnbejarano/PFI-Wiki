# Preguntas previsibles del tribunal

Doce preguntas con la respuesta preparada y la lámina de respaldo que la acompaña.

**Regla general:** escuchá la pregunta entera, respirá antes de contestar, y si no sabés,
decilo. «No lo sé con certeza, lo verifico y le respondo» es mejor que inventar — y el
tribunal lo nota. No discutas: si te marcan algo, anotalo y agradecé.

**Contexto útil:** en las defensas previas de este curso las preguntas fueron
mayoritariamente **de negocio, no técnicas**. Dos grupos reportaron que casi no hubo
preguntas cuando la exposición dio bien el contexto al principio.

---

## Las tres que ya sabemos que vienen

### 1 · «¿Por qué no entrevistaste a una organización de verificación?»

Está gestionada y no hubo respuesta dentro del plazo. Lo declaro en la lámina de límites en
lugar de omitirlo. La consecuencia real es acotada: el perfil que falta es el del
**verificador profesional**, y la parte del diseño que dependía de él —el proceso manual de
verificación— quedó cubierta por la entrevista a la periodista de Canal 10, que verifica a
diario. Queda para la Entrega 4.

> No ofrezcas más de lo que te preguntan. Si insiste, el plan concreto es sumarla al
> trabajo de campo de la E4 junto con la validación con usuarios.

### 2 · «¿Cómo tratás una afirmación que mezcla un dato verdadero con una interpretación?»

Hoy, mal, y está declarado. El esquema pasó de cuatro clases a tres: se eliminó
«engañoso», que era justamente la categoría de los casos mixtos, y `sin verificar` los
absorbe solo en parte. La razón de eliminarla fue que **ningún dataset disponible la
etiqueta**, así que la clase no se podía entrenar ni evaluar. Es una limitación conocida,
no un descuido, y la advirtió la propia entrevistada.

### 3 · «¿Cómo validás la clase *sin verificar* si no existe en ningún dataset?»

No se puede validar contra un dataset público, y por eso el corpus argentino propio deja de
ser un extra y pasa a ser **una condición del diseño**. Se construye como subproducto de la
operación del sistema, con 300 a 500 ejemplos anotados para test y Kappa de Cohen de 0,60
como umbral de acuerdo entre anotadores. Es trabajo de la Entrega 4.

**Respaldo:** *Estrategia de datos — tres niveles* · *Protocolo de validación*

---

## Negocio

### 4 · «¿Quién paga esto? ¿Cómo se gana plata?»

El ciudadano no paga nunca. Pagan cinco segmentos B2B por el mismo activo: medios
(ventaja editorial), verificadores (priorizar qué chequear), centros de investigación
(dataset en español argentino), organismos públicos (monitoreo electoral) y marcas
(alertas reputacionales). Dos formatos: API por volumen y reportes por suscripción.

**Respaldo:** lámina 6, y *Panel de tendencias* para mostrar el producto que se vende.

### 5 · «¿Y el análisis financiero? ¿VAN, TIR, payback?»

La cátedra dejó la parte económica **fuera del alcance de esta entrega**; corresponde a la
Entrega 4. Lo que sí está medido es el costo de infraestructura: 14 dólares por mes, 168 en
todo el período del PFI.

> Es la respuesta honesta y está respaldada por lo que dijeron en clase el 04/07. No
> improvises un VAN.

**Respaldo:** *Costos de infraestructura*

### 6 · «¿Qué te impide que Google o Twitter lo hagan mañana?»

Nada técnico, y no es ahí donde está la defensa. El activo es el **corpus argentino** que
genera el uso, que no se puede comprar ni scrapear: mide qué se consume, no qué se publica.
Y la ventaja se compone con el tiempo — cuantos más usuarios, mejor el dato. Es un efecto
de red de datos, no una barrera técnica.

### 7 · «¿Por qué solo Twitter/X? WhatsApp es el vector principal en Argentina.»

Correcto, y está declarado en el documento: WhatsApp tiene 93 % de penetración y es el
principal vector. Queda fuera **por su cifrado de extremo a extremo** — no es una decisión
de alcance sino una imposibilidad técnica. Extender el sensor a otras superficies web es
línea futura, y el argumento del activo diferencial se sostiene solo sobre X.

---

## Técnicas

### 8 · «¿Qué modelo usás?»

Hoy el análisis del texto lo resuelve un proveedor externo detrás de un puerto inyectable;
el prototipo demuestra el recorrido completo, no el clasificador definitivo. El clasificador
propio es un modelo multilingüe ajustado al español —la familia XLM— y es el trabajo de la
Entrega 4. **La forma de la respuesta no cambia cuando se sustituye**: por eso el proveedor
está detrás de un puerto y no llamado directamente.

### 9 · «¿Está todo hardcodeado? ¿Es ajustable?»

No. Los pesos del combinador y los umbrales de los veredictos son configuración: se cambian
con una línea y un reinicio, sin tocar código. Cada análisis viaja con la versión de
configuración que lo produjo, y esa versión **se calcula** a partir de los valores, así que
no puede quedar desactualizada. Se puede demostrar en vivo.

**Respaldo:** *Los pesos son configuración, no código*

### 10 · «¿Por qué no está en la nube? / ¿Por qué corre local?»

Es un prototipo para demostrar el recorrido completo, y el despliegue no aporta nada a lo
que esta entrega evalúa. La arquitectura de despliegue está diseñada y documentada —cinco
zonas de confianza, Railway y Vercel, 14 dólares mensuales presupuestados—, y se ejecuta en
la Entrega 4.

> En el curso ya le hicieron este comentario a otro grupo. Tené el diagrama de despliegue a
> mano; que exista el diseño es la respuesta.

**Respaldo:** *Arquitectura de red y despliegue*

### 11 · «¿Cómo evitás sesgar políticamente el resultado?»

Tres decisiones concretas, no una promesa: los cinco medios de la jerarquía son de
**orientación editorial diversa** y elegidos a propósito; el sistema se pronuncia **sobre
la afirmación y nunca sobre la persona** que publicó; y el nivel más severo **atribuye el
juicio a la fuente oficial que lo sostiene** en lugar de afirmarlo por su cuenta. Además,
sin evidencia no hay veredicto. Es el riesgo que el 84 % de los encuestados marcó como su
condición de confianza, así que ordenó el diseño y no al revés.

### 12 · «¿Y si el sistema se equivoca y marca algo verdadero como falso?»

El umbral de decisión está ordenado hacia **precisión antes que exhaustividad**,
exactamente por eso: en la encuesta el falso positivo (66 %) y la censura de sátira (57 %)
pesaron más que el falso negativo. Y el producto no bloquea ni oculta nada: muestra una
señal con su evidencia al lado, y el usuario decide. Es un asistente, no un árbitro.

---

## Si te marcan algo del formato o del documento

Anotá, agradecé, no discutas. En este curso marcan detalles muy chicos —a un grupo le
corrigieron una pronunciación— y **la instancia es un punto de control, no una evaluación
con nota**. Lo dijeron explícitamente: donde sí evalúan la presentación es en el 75 %.

## Lo que no tenés que ofrecer si no te preguntan

- Que el prototipo corre sobre Python 3.13 y el documento declara 3.14.
- Que la caché es en memoria y se pierde al reiniciar.
- Que Télam no respondió la conexión el día que se verificaron los dominios.

Son honestos y están escritos en el repositorio; simplemente no aportan nada en diez
minutos y abren frentes que nadie abrió.
