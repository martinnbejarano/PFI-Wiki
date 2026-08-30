---
titulo: Feedback de la exposición del 50 % — qué pidió el evaluador
tipo: análisis
tags: [presentacion, entrega-50, defensa, feedback, entrega-final]
fuentes: [wiki/presentacion/e50/transcripcion.md]
actualizado: 2026-08-30
---

# Feedback de la exposición del 50 %

Lectura del feedback que dejó **Castiñeiras, José Ramón** al cierre de la exposición
del 29/08/2026. La fuente es [[wiki/presentacion/e50/transcripcion]], que es una
transcripción automática y está rota en varios tramos: los puntos marcados con
`[interpretado]` son reconstrucción del sentido, no cita textual.

---

## Lo que funcionó

| Aspecto | Qué dijo |
|---|---|
| La herramienta | Le gustó, y volvió sobre eso tres veces. «Son esas aplicaciones que ayudan sobre todo al que no tiene la capacidad de darse cuenta de que algo es *fake*.» |
| El tiempo | 10:14. Lo dio por bien resuelto y recomendó seguir ensayando para sostener ese control. |
| El planteo del problema | «Súper claro.» |
| La presentación | «Muy ordenada, muy equilibrada, muy linda.» |
| La demo | Valoró que a esta altura ya hubiera un prototipo funcionando. |

Su síntesis final: la herramienta es valiosa y **por eso mismo** es atacable, así que
prepararse para defenderla es lo que la termina de hacer valiosa.

---

## Lo que pidió corregir

### 1. Falta un diferencial — lo marcó como lo más importante

Sostiene que herramientas parecidas circulan desde hace unos cuatro años. Mencionó dos
referencias, ambas mal transcriptas: un equipo interno de una farmacéutica dedicado a
esto, y una herramienta reciente de verificación en vivo de declaraciones de políticos
contra sus fuentes. `[interpretado]`

> «Hay que encontrar un distintivo más. Eso para mí es clave.»

El riesgo que planteó es concreto: que en la defensa final alguien diga *esto ya existe*
y no haya respuesta preparada.

**Pendiente:** identificar y documentar el diferencial defendible. El candidato que ya
está en el proyecto —entregar el camino a la evidencia y no solo la conclusión— hay que
contrastarlo contra esas herramientas antes de apoyarse en él.
Ver [[wiki/competencia/analisis-competitivo]].

### 2. El problema del *ex falso* — el reparo conceptual de fondo

Le hace ruido que el veredicto se reduzca a un porcentaje. Su argumento: si una fuente
oficial trae un dato erróneo, por *ex falso quodlibet* se puede terminar derivando
cualquier cosa como falsa, y la verdad o falsedad de una afirmación no es una cuestión
de grado.

Propuso contemplar el camino de **descomponer la afirmación en predicados lógicos** y
evaluar la implicación, en lugar de agregar puntajes. No pidió implementarlo: dijo que
alcanza con declarar que esto es un MVP y mostrar que el escenario está contemplado.

**Pendiente:** decidir si entra como limitación declarada, como trabajo futuro, o ambas.
Ver [[wiki/solucion/metodologia-tecnica]].

### 3. Probabilidad contra *chances* — corrección de vocabulario

En la demo se dijo «79 % de probabilidades». La probabilidad se expresa entre cero y
uno; en porcentaje son *chances*. Aceptó la respuesta dada en el momento —que en la
interfaz conviene el lenguaje llano porque el público general no procesa la distinción—
pero dejó fijada la regla:

> En la app puede quedar como está. **En la exposición hay que usar el término técnico
> de la carrera.**

### 4. «¿Quién verifica al verificador?» — la pregunta que anticipó

La formuló explícitamente como entrenamiento, aclarando dos veces que no era una
crítica:

> «Si hay gente que puede hacer un posteo *fake*, ¿no puede haber alguien que haga un
> análisis *fake*? ¿Cómo defendés que tu análisis está bien?»

Lo que pidió tener preparado para la próxima:

- Un **disclaimer visible** en la interfaz sobre cómo se analiza.
- Un **listado público y enlazable de todas las fuentes** que se consultan.
- Usar **todas** las fuentes disponibles y no una selección. Mencionó algo parecido a la
  cámara argentina de diarios como criterio de exhaustividad. `[interpretado]`

Su razonamiento: la exhaustividad declarada te limpia frente al mal pensado, que siempre
va a existir y tiene derecho a existir. Y agregó que si el usuario llega a confiar en el
botón, el valor del producto sube muchísimo.

Esto toca directamente la política de fuentes actual, que es una **lista cerrada y
ponderada por peso** (oficiales 1,0 · medios 0,6 · verificaciones previas 0,4). La
lista cerrada tiene su propia justificación —trazabilidad y control de calidad— pero
hay que poder defenderla contra la acusación de selección sesgada, o abrirla.
Ver [[wiki/solucion/arquitectura]].

### 5. Trabajo futuro con ideas propias — para la próxima presentación

Observó que la mayoría llega al capítulo de conclusiones y escribe lo obvio
(«escalarlo a Latinoamérica»), y que lo que demuestra dominio real del tema es llegar
con ideas propias. Dejó dos, concretas:

**Mentir con datos verdaderos.** Publicaciones que dan un dato real pero omiten el
contexto que lo contradice. Nada de lo afirmado es falso, pero la intención es engañar
y queda una idea equivocada en la cabeza del lector. Requiere un análisis más profundo
que el actual.

**Mentir con gráficos.** Un gráfico de barras con el eje recortado exagera una
diferencia. El dato es real, la sugerencia visual es falsa. Implica análisis de
imágenes, que él mismo calificó de costoso, y por eso lo propuso como trabajo futuro.

Fue específico con el *cuándo*: **en esta exposición no hacía falta; en la próxima de
este estilo, sí.** Y explicó por qué lo levantaba ahora: los evaluadores de esta mesa no
están en la entrega final, así que prefería dejarlo dicho mientras podía.

---

## Pendientes que abre este feedback

| # | Pendiente | Origen | Destino |
|---|---|---|---|
| 1 | Definir y documentar el diferencial frente a las herramientas ya existentes | Punto 1 | [[wiki/competencia/analisis-competitivo]] |
| 2 | Declarar el límite del enfoque por puntaje y evaluar la vía lógico-proposicional | Punto 2 | [[wiki/solucion/metodologia-tecnica]] |
| 3 | Corregir «probabilidad» por «chances» en el guion de la defensa | Punto 3 | `presentacion/GUION.md` |
| 4 | Preparar la defensa de imparcialidad: disclaimer, fuentes públicas, criterio de exhaustividad | Punto 4 | [[wiki/presentacion/e50/analisis-feedback]] → `PREGUNTAS.md` |
| 5 | Lámina de trabajo futuro con las dos ideas propias | Punto 5 | Deck de la Entrega 4 |

Quedó además una pregunta cortada por el final de la grabación sobre los modelos usados
en la demo y cuáles se reemplazan de acá a la entrega final, y el ofrecimiento de que se
le mande material por su cuenta.

---

## Referencias cruzadas

- [[wiki/presentacion/e50/transcripcion]]
- [[wiki/proyecto/reuniones]]
- [[wiki/competencia/analisis-competitivo]]
- [[wiki/solucion/metodologia-tecnica]]
- [[wiki/solucion/arquitectura]]

## Fuentes

- [[wiki/presentacion/e50/transcripcion]] — transcripción automática de Teams del 29/08/2026
