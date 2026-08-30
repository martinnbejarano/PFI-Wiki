---
titulo: Análisis de las defensas del 22/08/2026
tipo: análisis
tags: [presentacion, entrega-50, defensa]
fuentes: [PFI-SA10.docx, PFI-SA13.docx, PFI-SA16.docx, PFI-SA34.docx, PFI-SA35.docx]
actualizado: 2026-08-29
---

# Qué pasó en las cinco defensas del 22/08

Transcripciones de Teams de cinco grupos que defendieron el 50 % el sábado anterior.
Evalúa **Castiñeiras, José Ramón** acompañado de un segundo docente. Las transcripciones
son automáticas y tienen errores de reconocimiento; lo que sigue está reconstruido, no
citado al pie de la letra.

| Grupo | Proyecto | Duración total |
|---|---|---|
| SA34 | Predicción de ausentismo en comercios con agenda | 25 min |
| SA10 | Phishar — detección de phishing con educación contextual | 24 min |
| SA13 | Atlas — trazabilidad de trámites documentales | 22 min |
| SA16 | Lupa — análisis multimodal de siniestros de seguros | 25 min |
| SA35 | Cycross — cruce de calle asistido para personas ciegas | 30 min |

## El dato que más cambia la preparación

**La exposición es de 10 minutos y las preguntas duran entre 12 y 20.** Las sesiones
completas van de 22 a 30 minutos. Castiñeiras arranca diciendo «presenten en 10 minutos,
les aviso cuando falten 2» y después conversa largo. **La mitad de la instancia es Q&A**,
así que la hoja de preguntas pesa tanto como el deck.

## La estructura que siguieron los cinco

Sorprendentemente uniforme. Ninguno se salió de este orden:

1. Nombre, nombre del proyecto y una frase de qué es
2. **Una escena o una pregunta**, no una estadística: «¿qué ocurre cuando un cliente no
   asiste a su turno?», «la pregunta que pasa por la cabeza de estas personas al cruzar la
   calle», un mail de un proveedor que llega un martes cualquiera
3. Números que dimensionan el problema
4. Competencia — breve, dos o tres actores, dónde está el hueco
5. *User research*: encuesta con porcentajes + entrevistas con hallazgos
6. La solución y sus componentes
7. Arquitectura y tecnologías — **una lámina, muy por encima**
8. **Demo** — los cinco hicieron demo, y es el centro de gravedad
9. Estado actual y próximos pasos
10. Gracias

Nuestro deck sigue este orden. La única diferencia es que ponemos el modelo de negocio
antes de la demo en vez de dejarlo para el final, y eso juega a favor: es lo que él más
pregunta.

## Qué tan técnico hablaron

**Mucho menos de lo que uno esperaría.** El techo fue nombrar la técnica y dar una frase:
«YOLOv11 en versión nano», «un modelo de gran escala con instrucciones, de pesos abiertos,
que podemos instalar en servidores propios», «React con Vite, FastAPI, PostgreSQL con
pgvector». Nadie explicó una arquitectura en profundidad. El que más bajó (SA16, con un
*pipeline* NLP de tres pasos y dos modelos de visión) igual recibió únicamente preguntas
de negocio.

Confirma el recorte que ya hicimos: la lámina 7 con cuatro módulos y una técnica cada uno
está en el nivel correcto.

## Cuánto pesó el negocio

Es **el eje de la evaluación**. En los cinco casos preguntó por el modelo de negocio, y en
tres de los cinco dio el mismo discurso, que conviene tener presente casi textual:

> Ser ingeniero en sistemas implica que, más allá de conocer todas las soluciones posibles,
> tenés que estar alineado al negocio, entender el negocio. No es solamente hacer, es hacer
> bien, y hacer bien implica entender quién podría necesitar esto. A mí, que soy el de la
> compañía de seguros, me importa poco cómo está hecho: me tenés que vender técnicamente el
> proyecto **y** me tenés que vender el negocio, y dónde me voy a beneficiar yo.

Acepta «todavía no llegamos, va para el 75 %» sin enojarse —SA13 y SA16 contestaron eso—
pero es justo la respuesta que dispara el discurso. **Tener el número listo evita el
sermón.**

## Cuánto pesó la encuesta

Menos de lo que temíamos. Nadie fue interrogado sobre el tamaño de la muestra ni sobre
metodología. Los que la usaron bien la usaron como *munición*: dos o tres porcentajes que
justifican una decisión de diseño. SA34 lo hizo explícito —«el 63 % aceptaría pagar una
seña si es baja; el 24 % buscaría cómo evitarla, **esto indica que la mitigación tiene que
ser dirigida y no masiva**»— y fue el mejor recibido de los cinco.

Es exactamente lo que hace nuestra lámina 3 con el 4,06 contra 3,57.

## Preguntas, ordenadas por frecuencia

| # | Pregunta | Grupos | Nota |
|---|---|---|---|
| 1 | ¿Cuál es el modelo de negocio? ¿Quién es el cliente ideal? | 5/5 | Universal, sin excepción |
| 2 | ¿Cuánto cuesta? Dame una franja de precio | 4/5 | Quiere un número, no un «lo estamos viendo» |
| 3 | ¿Por qué te elegirían a vos y no a lo que ya existe? | 4/5 | La hace él en el Q&A, no quiere oírla en el deck |
| 4 | ¿Hasta dónde llega el alcance? ¿Qué queda afuera? | 3/5 | Premia que esté delimitado de entrada |
| 5 | ¿Qué pasa si falla / caso borde X? | 3/5 | Inventa el caso raro en el momento |
| 6 | ¿Cómo entrenaste el modelo? ¿Con qué datos? | 2/5 | |
| 7 | ¿Nube u *on premise*? ¿Qué requiere? | 1/5 | Ligado al costo |
| 8 | ¿La parte legal? | 2/5 | Le gusta que se haya consultado a alguien |
| 9 | ¿Cómo venís con la planificación? | 1/5 | Cierre de cortesía |
| 10 | ¿Qué te inspiró el tema? | 1/5 | **Se la hizo al único que expone solo** |

## Lo que corrigió del formato

- **«Eviten las pantallas negras.»** Lo dijo dos veces, sin que nadie preguntara, en SA16 y
  en SA35: «para el que quiera leer, para el que quiera ver qué está diciendo». Es su
  cantinela.
- **Tildes.** A SA34, que fue el mejor de los cinco: «noté por lo menos dos tildes que
  faltan; son detalles, pero alguno se va a fijar».
- **Cronometrar el video y anunciar cuánto dura.** A SA16: «¿cuánto dura el video? Tres
  minutos. Entonces yo ya sé, meto el video y sé que en tres minutos no me va a fallar
  nada».
- **Tener láminas guardadas para las preguntas.** A SA35: poder decir «sí, lo pensamos» y
  mostrarla «en vez de improvisar en el momento viendo cómo salen».
- **Ritmo.** A SA35: «tiene que ser lento, legible».

## El elogio, para saber a qué apuntar

A SA34, que expone solo y con un tema de *machine learning*:

> Muy sólido, me gustó mucho. Muy bien explicado y me gustó la presentación: **no está
> sobrecargada, no leíste, confianza, conocés lo que estás haciendo.** Así que yo estoy
> feliz.

Cuatro cosas, y ninguna es sobre el contenido: no sobrecargar, no leer, transmitir
confianza, dominar el tema.

## Referencias cruzadas

- [[GUION]]
- [[PREGUNTAS]]
