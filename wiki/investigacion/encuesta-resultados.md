---
titulo: Encuesta de user research — resultados
tipo: análisis
tags: [user-research, encuesta, resultados, validacion]
fuentes: [encuesta-desinformacion.xlsx]
actualizado: 2026-08-22
---

# Encuesta de user research — resultados

Resultados del trabajo de campo cuantitativo diseñado en [[wiki/investigacion/user-research]]. La encuesta buscaba validar cuatro cosas antes de comprometer el desarrollo: que el segmento se topa con desinformación en Twitter/X, que le cuesta detectarla por su cuenta, que hoy verifica de forma insuficiente, y que instalaría y confiaría en una extensión que le devuelva un puntaje con evidencia.

## Ficha técnica

| | |
|---|---|
| **Población objetivo** | Personas de 18 a 40 años, residentes en Argentina, usuarias de Twitter/X que siguen noticias de política o economía |
| **Respuestas recibidas** | **140** |
| **Respuestas dentro del segmento** | **107** (76,4 %) |
| **Período de campo** | 2026-07-04 a 2026-08-18 |
| **Instrumento** | Cuestionario autoadministrado de 14 preguntas (perfil, exposición, capacidad y comportamiento, apetito y confianza) |
| **Distribución** | Digital y presencial, por muestreo no probabilístico por conveniencia y bola de nieve |
| **Preguntas abiertas respondidas** | 34 de 140 |
| **Fuente de datos** | `raw/investigacion/encuesta-desinformacion.xlsx` |
| **Script de análisis** | `scripts/analizar_encuesta.py` |

**Criterio de segmento.** Las preguntas 1 a 3 se computan sobre las 140 respuestas porque son las que definen el filtro. De la 4 en adelante la base es n = 107: quedan fuera quienes declararon tener menos de 18 o más de 40 años (10), no usar Twitter/X (4) o no seguir noticias de política ni economía en la plataforma (20). Todos los porcentajes de este documento indican su base.

**Alcance de la muestra.** El muestreo es no probabilístico, de modo que los resultados describen a las personas alcanzadas y no son extrapolables al conjunto de usuarios argentinos de Twitter/X. La franja 18-25 concentra el 59,3 % de las respuestas, lo que sesga la muestra hacia el extremo joven del segmento. Ver [[#Limitaciones]].

---

## Bloque A — Perfil y filtro (n = 140)

**Edad.** 18-25: 59,3 % (83) · 26-33: 27,9 % (39) · 34-40: 5,7 % (8) · Más de 40: 5,0 % (7) · Menos de 18: 2,1 % (3). El **92,9 %** cae dentro de la franja objetivo de 18 a 40 años.

**Uso de Twitter/X.** Varias veces al día: 34,3 % (48) · Una vez al día: 27,1 % (38) · Algunas veces por semana: 27,1 % (38) · Rara vez: 8,6 % (12) · No la uso: 2,9 % (4). El **61,4 %** entra a la plataforma al menos una vez por día, que es la frecuencia sobre la que una extensión de navegador tiene sentido.

**Seguimiento de noticias de política o economía.** Sí, frecuentemente: 38,6 % (54) · A veces: 47,1 % (66) · No: 14,3 % (20).

## Bloque B — Exposición al problema (n = 107)

**Frecuencia con que se cruzan contenido falso, engañoso o no verificable:**

| Respuesta | n | % |
|---|---:|---:|
| Muy frecuentemente | 45 | 42,1 % |
| Frecuentemente | 34 | 31,8 % |
| A veces | 15 | 14,0 % |
| Rara vez | 7 | 6,5 % |
| Nunca | 6 | 5,6 % |

El **73,9 %** se cruza con desinformación de forma frecuente o muy frecuente. Es el dato que sostiene la premisa del proyecto: el problema no es marginal ni percibido como lejano por el segmento.

**Contacto personal con el problema.** El 35,5 % (38) reconoce haber compartido contenido que después resultó falso o dudoso y otro 26,2 % (28) estuvo a punto de hacerlo. Sumados, **el 61,7 % pasó por la situación que el sistema busca prevenir**. Solo el 26,2 % lo descarta y un 12,1 % no sabe.

**Preocupación** (escala 1 a 5, media **4,20**): 5 → 43,0 % · 4 → 37,4 % · 3 → 15,9 % · 2 → 3,7 % · 1 → 0 %. El **80,4 %** se ubica en los dos valores más altos y **ninguna respuesta marcó el mínimo**.

> La preocupación se sostiene incluso entre quienes declaran poca exposición: el cruce exposición × preocupación da media 4,40 en "muy frecuentemente" y no baja de 3,67 en ninguna categoría. La inquietud es transversal, no un efecto de quienes más contenido dudoso ven.

## Bloque C — Capacidad y comportamiento actual (n = 107)

**Capacidad autopercibida de distinguir una noticia falsa** (1 a 5, media **3,58**): 5 → 22,4 % · 4 → 33,6 % · 3 → 26,2 % · 2 → 15,0 % · 1 → 2,8 %.

> **Hallazgo — la brecha preocupación/capacidad.** La preocupación promedia 4,20 y la capacidad autopercibida 3,58. El segmento está más preocupado de lo que se siente equipado: un 44,0 % se ubica en el punto medio o por debajo al evaluar su propia capacidad. Ese diferencial es, exactamente, el espacio que la herramienta ocupa.

**Qué hace ante una publicación dudosa** (opción múltiple):

| Acción | n | % |
|---|---:|---:|
| Busco en Google | 89 | 83,2 % |
| Miro la cuenta que lo publicó | 76 | 71,0 % |
| Comparo con medios que conozco | 51 | 47,7 % |
| Le pregunto a alguien | 45 | 42,1 % |
| Nada, sigo de largo | 7 | 6,5 % |
| Leo los comentarios o las notas de la comunidad | 1 | 0,9 % |
| Lo busco en X con otras palabras | 1 | 0,9 % |

Las dos conductas dominantes **replican lo que hacen dos de los cuatro módulos del sistema**: buscar en Google equivale al módulo de contraste con evidencia web y mirar la cuenta autora equivale al módulo de credibilidad de la fuente. El diseño de la solución automatiza el comportamiento que el usuario ya intenta hacer a mano, en lugar de proponerle uno nuevo.

**Tiempo dedicado a verificar:** Menos de 1 minuto: 35,5 % (38) · 1-3 minutos: 40,2 % (43) · Más de 3 minutos: 16,8 % (18) · No verifico: 7,5 % (8).

> **Hallazgo — la ventana es de segundos.** El **75,7 % resuelve la duda en menos de tres minutos** y más de un tercio en menos de uno. La verificación existe pero es superficial, y define un requerimiento no funcional duro: si el veredicto no llega en pocos segundos, el usuario ya siguió scrolleando. Alimenta el presupuesto de latencia de [[wiki/solucion/requerimientos]].

## Bloque D — Apetito y confianza (n = 107)

**Intención de instalar y usar la extensión** (1 a 5, media **4,06**): 5 → 42,1 % · 4 → 33,6 % · 3 → 15,0 % · 2 → 6,5 % · 1 → 2,8 %. El **75,7 %** se declara probable o muy probablemente usuario.

**Confianza en un puntaje generado automáticamente** (1 a 5, media **3,57**): 5 → 25,2 % · 4 → 32,7 % · 3 → 22,4 % · 2 → 13,1 % · 1 → 6,5 %. El **57,9 %** en los dos valores altos.

> **Hallazgo principal — la brecha intención/confianza.** La intención de uso (4,06) supera a la confianza en el resultado automático (3,57) en casi medio punto de escala. El segmento **quiere la herramienta pero no le cree del todo al número**. La consecuencia de diseño es directa: el producto no puede entregar un puntaje solo. La evidencia y la explicación no son una mejora opcional de la interfaz, son la condición para que el puntaje sea utilizable.

El cruce con la capacidad autopercibida refuerza la lectura:

| Capacidad autopercibida | n | Confianza media | Intención media |
|---|---:|---:|---:|
| 1 | 3 | 4,00 | 3,33 |
| 2 | 16 | 3,75 | 4,50 |
| 3 | 28 | 3,61 | 4,18 |
| 4 | 36 | 3,50 | 4,06 |
| 5 | 24 | 3,46 | 3,71 |

La confianza en el puntaje **desciende de forma monótona a medida que sube la capacidad autopercibida** (4,00 → 3,46). Quien se cree bueno detectando desinformación es quien menos delega el juicio en el sistema. La intención de uso, en cambio, es máxima en el escalón 2 (4,50) y cae en los extremos. El usuario que mejor calza con el producto no es ni el que se siente indefenso ni el experto: es el que duda de sí mismo lo suficiente como para querer una segunda opinión.

**Qué generaría más confianza** (opción múltiple):

| Driver | n | % |
|---|---:|---:|
| Que no tenga sesgo político | 90 | 84,1 % |
| Que muestre las fuentes/evidencia | 71 | 66,4 % |
| Que explique por qué llega a ese resultado | 54 | 50,5 % |
| Que sea transparente sobre su margen de error | 41 | 38,3 % |
| Que la respalde una institución reconocida | 34 | 31,8 % |
| Que sea *open source* | 4 | 3,7 % |

**Mayor preocupación** (opción múltiple):

| Preocupación | n | % |
|---|---:|---:|
| Que se equivoque (falsos positivos) | 71 | 66,4 % |
| Que censure opiniones o sátira | 61 | 57,0 % |
| Sesgo político | 52 | 48,6 % |
| Privacidad de mis datos | 38 | 35,5 % |
| Ninguna | 3 | 2,8 % |
| Que se vuelva paga | 3 | 2,8 % |
| Que ande lento | 1 | 0,9 % |

> **Hallazgo — la neutralidad política domina todo lo demás.** El sesgo político aparece como el principal driver de confianza (84,1 %, veinte puntos por encima del segundo) y a la vez como la tercera preocupación (48,6 %). Sumado al 57,0 % que teme la censura de opiniones o sátira, el mensaje del segmento es que **el riesgo percibido no es que la herramienta falle, sino que tome partido**. Esto tiene consecuencias de producto verificables: obliga a que el sistema clasifique afirmaciones fácticas y no opiniones, a exponer siempre la evidencia que sostiene el veredicto, y a que la comunicación del resultado use lenguaje probabilístico y no sentencias.

**Respuestas abiertas.** De las 34 recibidas, los pedidos recurrentes fueron: detección de imágenes generadas con IA, distinguir opinión de dato falso, avisar cuando se recircula contenido viejo como nuevo, mostrar el contexto que falta en el tuit, y no saturar la pantalla con carteles. Las dos primeras confirman los hallazgos cuantitativos; las tres restantes son insumo de diseño que **excede el alcance del prototipo** y se registra como línea futura.

---

## Insights y su traducción a decisiones

| # | Insight | Evidencia | Consecuencia en el proyecto |
|---|---|---|---|
| 1 | El problema existe y es percibido | 73,9 % de exposición frecuente; 61,7 % compartió o casi compartió contenido falso | Valida la premisa de [[wiki/proyecto/contexto-problema]] con datos locales propios |
| 2 | Hay brecha entre preocupación (4,20) y capacidad (3,58) | Bloques B y C | Justifica la existencia del producto: asiste donde el usuario se siente corto |
| 3 | La verificación actual es superficial | 75,7 % verifica en menos de 3 minutos | RNF de latencia: el veredicto debe llegar en segundos |
| 4 | El usuario ya busca en Google y mira la cuenta | 83,2 % y 71,0 % | Confirma los módulos de contraste web y de credibilidad de la fuente |
| 5 | Quieren la herramienta pero desconfían del puntaje | Intención 4,06 vs. confianza 3,57 | El puntaje nunca va solo: evidencia + explicación son obligatorias |
| 6 | La neutralidad política es la condición de aceptación | 84,1 % driver; 48,6 % + 57,0 % preocupación | Clasificar hechos y no opiniones; excluir sátira; lenguaje probabilístico |
| 7 | El falso positivo es el modo de falla que más pesa | 66,4 % | Priorizar precisión sobre exhaustividad en el umbral de decisión; alimenta [[wiki/solucion/pruebas]] |
| 8 | La gratuidad no es un diferencial percibido | Solo 2,8 % teme que se vuelva paga | El modelo *freemium* de [[wiki/negocio/modelo-de-negocio]] no encuentra resistencia en el segmento |

## Limitaciones

1. **Muestreo no probabilístico.** Por conveniencia y bola de nieve, sin marco muestral. Los resultados describen a las personas alcanzadas y no admiten inferencia al universo de usuarios argentinos de Twitter/X.
2. **Sesgo etario dentro del segmento.** El 59,3 % de la muestra total tiene entre 18 y 25 años y solo 8 respuestas caen en 34-40, lo que impide leer esa franja por separado con solvencia. El cruce edad × intención se reporta a título descriptivo.
3. **Intención declarada, no conducta.** El 75,7 % de intención de uso mide disposición manifestada ante una descripción, no instalación efectiva. La literatura de adopción documenta la distancia entre ambas.
4. **Autopercepción en la capacidad de detección.** La pregunta 7 mide lo que la persona cree sobre sí misma, no su desempeño real, que suele estar sobreestimado.
5. **Deseabilidad social.** Reconocer haber compartido contenido falso tiene costo reputacional, por lo que el 35,5 % es probablemente un piso.
6. **Baja tasa de respuesta abierta.** 34 de 140 (24,3 %) respondieron la pregunta 14, lo que limita el peso del análisis cualitativo derivado de ella.

## Referencias cruzadas

- [[wiki/investigacion/user-research]] — diseño del instrumento y metodología
- [[wiki/proyecto/contexto-problema]] — estadísticas que esta encuesta valida localmente
- [[wiki/solucion/requerimientos]] — RNF de latencia y requerimientos de evidencia y explicabilidad
- [[wiki/solucion/pruebas]] — el peso del falso positivo en los criterios de aceptación
- [[wiki/solucion/mockups]] — la evidencia visible en pantalla responde al insight 5
- [[wiki/negocio/modelo-de-negocio]] — apetito y ausencia de resistencia al esquema gratuito
- [[wiki/competencia/analisis-competitivo]] — océano azul y matriz ERIC

## Fuentes

- [[raw/investigacion/encuesta-desinformacion.xlsx]] — planilla de respuestas
