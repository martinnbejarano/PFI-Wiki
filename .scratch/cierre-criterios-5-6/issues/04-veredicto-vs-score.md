# 04 · Veredicto de tres niveles frente a «score, no veredicto»

Type: grilling
Status: open
Blocked by: —

## Question

El archivo legal, en sus líneas 74 a 77, prescribe como mitigación de la difamación: «presentar como probabilidad», «*score*, no veredicto», «0-1, no Verdadero/Falso». El diseño hace justo lo contrario: hay tres niveles con umbrales en 0,40 y 0,75, y el *badge* del mockup dice literalmente **probablemente falso**.

La contradicción es real y toca un riesgo real: marcar públicamente el contenido de una cuenta identificable como falso, equivocándose, es el escenario de los arts. 109-115 del Código Penal.

Hay que decidir qué mitiga ese riesgo **con el diseño que efectivamente existe**:

1. ¿Se mantienen los tres niveles, o se vuelve a un *score* desnudo? Los mockups y el diagrama de secuencia ya están hechos con tres niveles.
2. ¿La evidencia enlazada obligatoria (RF-13) alcanza como mitigación? Es el argumento más fuerte disponible: el sistema no afirma, muestra qué dice la fuente oficial.
3. ¿El *badge* es visible solo para quien instaló la extensión, o hay alguna superficie donde el juicio se vuelva público? Si nunca es público, el hecho difamatorio no se configura y buena parte del riesgo desaparece.
4. ¿Dónde vive el *disclaimer*: en el *popup*, en la tienda, en ambos?
5. ¿El veredicto recae sobre la **afirmación** o sobre la **cuenta**? El Módulo 2 puntúa credibilidad de fuente, que apunta a la persona y no al contenido — es el punto más expuesto y hoy no está escrito en ninguna parte.

**Recomendación de partida.** Mantener los tres niveles y apoyar la defensa en tres patas: el juicio nunca es público, siempre viene con la fuente enlazada, y el veredicto se enuncia sobre la afirmación y no sobre la cuenta. El punto 5 probablemente obligue a reformular cómo se presenta el Módulo 2.
