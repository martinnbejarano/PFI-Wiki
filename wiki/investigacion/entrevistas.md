---
titulo: Entrevistas — resultados y análisis
tipo: análisis
tags: [user-research, entrevistas, cualitativo, validacion]
fuentes: [entrevista-maidan-2026-08.md, entrevista-soruco-2026-08.md]
actualizado: 2026-08-22
---

# Entrevistas — resultados y análisis

Dos entrevistas semiestructuradas, agosto de 2026, por videollamada, 30-40 min cada una, grabadas con consentimiento. El guion se escribió **después** de cerrar la encuesta, por lo que varias preguntas confrontan directamente los resultados cuantitativos con la experiencia del entrevistado. Transcripciones completas en `documento/chapters/appendix/interviews.tex` (Anexo C).

| # | Entrevistado | Perfil | Ángulo |
|---|---|---|---|
| 1 | **Federico Maidan** | Fundador de SorbyData, empresa de productos basados en IA | Viabilidad técnica y modelo de negocio — validación experta |
| 2 | **Ximena Soruco** | Periodista de Canal 10 de Salta; también radio y plataformas digitales | Proceso profesional de verificación — segmento secundario |

---

## Entrevista 1 — Federico Maidan (especialista en IA)

**Modelo de negocio: calidad de datos, no volumen de usuarios.** Descarta fijar un umbral de usuarios como objetivo. *"Tener 100.000 usuarios que analizan poco contenido puede ser menos interesante que 20.000 usuarios que son muy activos."* Lo que da valor al activo es la **intensidad de uso** y la capacidad de detectar patrones, no el head count.

**Arranque en frío: secuencia de dos etapas.** Primero un producto con utilidad verificable para el usuario individual; recién después aproximarse a los perfiles con necesidad profesional (periodistas, investigadores, gente muy interesada en política).

**Cómo atacaría el proyecto: distribución y confianza.** No la tecnología. *"La tecnología que vos estás implementando no es algo del otro mundo. Alguna empresa grande establecida podría implementar algo mucho mejor a nivel tecnológico."* Competiría consiguiendo canales de distribución (acuerdos con medios, organizaciones, comunidades) y construyendo una marca percibida como confiable. Cierra con la frase que ordena el capítulo 3: *"El desafío no es solamente hacer la extensión y el sistema, sino construir un ecosistema alrededor de la extensión."*

> **Esto confirma y precisa la tesis del océano azul.** El wiki y el documento ya sostenían que la ventaja no está en la técnica sino en el modelo de negocio. Maidan lo confirma y desagrega "modelo de negocio" en **dos componentes operativos: distribución y confianza percibida**. Se incorporó a [[wiki/competencia/analisis-competitivo]] y a la sección de espacio diferencial del documento.

**Brecha intención/confianza: la confirma desde la práctica.** *"Una cosa es que digan que les parece útil, y otra completamente distinta que digan que confían."* Precisa que la resistencia **se acentúa en usuarios con más conocimiento del dominio**, y menciona espontáneamente al periodista como caso típico. Y da el diagnóstico: *"esto no se resuelve teniendo un modelo más potente o más preciso, sino trabajando mucho en la explicación al usuario."*

**Neutralidad: mostrar fuentes es necesario pero no suficiente.** Su argumento es el que faltaba en el diseño: *"una persona puede considerar que una fuente es neutral y otra persona puede considerar que esa misma fuente es partidaria."* Propuesta concreta: exhibir **varias fuentes de orientación editorial diversa** y explicitar qué evidencia respalda cada dato.

**XLM-T vs. LLM.** Valida el fine-tuning para presupuesto limitado, y señala que un LLM en zero-shot clasifica bien pero con costo de operación mucho mayor. Recomienda **comparar contra un LLM antes de cerrar la decisión**, porque salen alternativas potentes y baratas todas las semanas.

**Recorte a dos meses: tirar el módulo de credibilidad de cuenta.** Es el módulo *"donde es más fácil introducir sesgo y más difícil de justificar"*: atribuir credibilidad por seguidores o por verificación es arbitrario **y manipulable**, porque ambas cosas se compran. Prioriza clasificador + contraste web, que se relacionan con la afirmación misma. *"Prefiero dos módulos funcionando muy bien y bien medidos, antes que cuatro módulos funcionando a medias."*

**No respondida:** la pregunta sobre la clase `sin_verificar` (que no existe en ningún dataset público y solo se puede aprender del corpus propio) **quedó sin respuesta registrada**. Sigue siendo un riesgo de diseño sin validación externa → llevarlo a la próxima entrevista.

---

## Entrevista 2 — Ximena Soruco (periodista, Canal 10 Salta)

**El proceso real de verificación: primero el emisor, después el contenido.** Ante una publicación dudosa mira, en este orden: si es cuenta oficial de gobierno, si es cuenta verificada, si es un periodista o político reconocido. Menciona explícitamente **el tilde gris que X asigna a cuentas gubernamentales** y la composición del conjunto de seguidores. Si el emisor no es reconocible, pasa a corroboración externa: *"veo si hay otro medio de comunicación que levantó esa noticia."*

> Ese flujo **reproduce la secuencia de dos módulos del sistema** y coincide con lo que la encuesta relevó en el segmento primario (83,2 % busca en Google, 71,0 % mira la cuenta). Que un profesional y un lector común converjan en la misma secuencia es evidencia de que la arquitectura automatiza un proceso que existe.

**El cuello de botella no es el que se esperaba.** No está en encontrar corroboración sino en **validar la fuente de segundo orden**: *"tenemos que validar que esas fuentes sean confiables y tengan cierto respaldo."* Matiza el módulo de contraste web: recuperar una fuente que corrobore resuelve la mitad del problema si el sistema no informa qué respaldo tiene esa fuente.

**Encaje del producto: primer filtro, no veredicto.** *"La usaría como una herramienta de primer filtro. No sé si la tomaría como una verdad absoluta."* Sirve para triar qué publicaciones merecen investigación y ahorrar tiempo. Coincide exactamente con el posicionamiento del segmento secundario en [[wiki/proyecto/propuesta]].

**Condición de abandono.** Dejaría de usarla si se equivoca seguido o *"si no me permite acceder a la fuente que usó para armar la respuesta."* La evidencia no es un plus: es condición de permanencia.

**Riesgo en el contexto argentino.** *"El principal riesgo es que el sistema termine siendo percibido como un árbitro de la verdad, cuando en realidad puede cometer errores y tener sesgos."* Y agrega el problema que el esquema de clases no resuelve del todo: hay afirmaciones con **datos verdaderos mezclados con interpretación, opinión o información incompleta**.

**Cierre: el contexto importa tanto como el veredicto.** *"Verificar no es solamente ver si es verdadero o falso. Importa el contexto: cuándo ocurrió, quién lo dijo, de dónde salió y si existen otras fuentes independientes."* Y el límite: la herramienta como asistente, *"no creo que termine reemplazando el criterio periodístico."*

---

## Convergencias entre los tres instrumentos

Tres hallazgos aparecen de forma **independiente** en la encuesta y en ambas entrevistas. Es la triangulación que hace fuerte al user research.

| Hallazgo | Encuesta (n=107) | Maidan (IA) | Soruco (periodismo) |
|---|---|---|---|
| **La evidencia es obligatoria** | 66,4 % la pide; 50,5 % pide explicación | "No se resuelve con un modelo más potente, sino trabajando la explicación" | "Si no me permite acceder a la fuente, dejaría de utilizarla" |
| **El riesgo es el sesgo, no el error técnico** | 84,1 % pone neutralidad primero | Fuentes de orientación diversa; una sola fuente no alcanza | "Percibido como un árbitro de la verdad" |
| **Asistente, no oráculo** | Intención 4,06 > confianza 3,57 | La resistencia sube con el conocimiento del usuario | "Primer filtro"; "no reemplaza el criterio periodístico" |

Un cuarto punto aparece en la encuesta y en la entrevista 2, pero no en la 1: **el contexto temporal**. En las respuestas abiertas apareció espontáneamente *"que me diga cuando algo es viejo y lo están recirculando como nuevo"*, y Soruco cierra pidiendo "cuándo ocurrió". No está contemplado en el diseño actual.

## La divergencia: el módulo de credibilidad de cuenta

Es el hallazgo más productivo, porque **las dos entrevistas se contradicen y las dos tienen razón**.

- **Maidan dice tirarlo.** Es el punto más fácil de sesgar y más difícil de justificar; seguidores y verificación se compran, así que la señal es manipulable.
- **Soruco lo usa primero.** Verificación, tilde gubernamental y seguidores son literalmente su primer paso, todos los días.

**Resolución adoptada — separar valor de uso de validez probatoria:**

| Dimensión | Evaluación |
|---|---|
| Valor informativo para el usuario | **Alto** — el profesional lo consulta primero; el 71,0 % del segmento primario también |
| Validez probatoria | **Baja** — adquirible y arbitraria (Maidan) |

→ **El módulo se conserva como señal exhibida al usuario, con peso reducido en el cálculo del puntaje.** El puntaje se apoya en clasificador + contraste externo. Así se atiende la advertencia de sesgo sin quitar una funcionalidad que ambos segmentos usan.

## Consecuencias sobre el proyecto

| # | Consecuencia | Origen | Dónde impacta |
|---|---|---|---|
| 1 | Panel de evidencia con **varias fuentes de orientación editorial diversa**, no una sola, informando el respaldo de cada una | Maidan + Soruco | [[wiki/solucion/requerimientos]], [[wiki/solucion/mockups]] |
| 2 | Exhibir el **contexto temporal**: fecha de origen y si el contenido está recirculando | Soruco + abiertas de la encuesta | [[wiki/solucion/requerimientos]] — **no está en la especificación vigente**; queda para la próxima iteración (E4) |
| 3 | Agregar una **línea base con LLM en zero-shot** al protocolo de evaluación, junto a TF-IDF + LR | Maidan | [[wiki/solucion/pruebas]] — ✅ ya incorporado a `chapter04.tex`, comparando desempeño, latencia y costo por consulta |
| 4 | Módulo de credibilidad: **señal exhibida, peso reducido** en el puntaje | Divergencia Maidan/Soruco | [[wiki/solucion/arquitectura]] — ✅ ya incorporado a `chapter04.tex` en la descripción del ensamblado |
| 5 | La ventaja competitiva se desagrega en **distribución + confianza percibida** | Maidan | [[wiki/competencia/analisis-competitivo]], [[wiki/negocio/modelo-de-negocio]] |
| 6 | Métrica de éxito del activo: **intensidad de uso**, no cantidad de usuarios | Maidan | [[wiki/negocio/modelo-de-negocio]] |

## Tensiones abiertas

1. **Afirmaciones mixtas.** Soruco advierte sobre declaraciones que mezclan datos verdaderos con interpretación u omisión. El esquema pasó de cuatro clases a tres eliminando "engañoso" (ver `documento/history/05.tex`), y `sin_verificar` absorbe esos casos solo parcialmente. **Es una pregunta previsible del tutor** — conviene llegar con la respuesta armada.
2. **La clase `sin_verificar` sigue sin validación externa.** La pregunta no obtuvo respuesta en la entrevista 1.
3. **Falta el perfil de verificación profesional.** Ninguna de las dos entrevistas cubre a una organización de fact-checking. Gestionar para E4.

## Limitaciones

- **Dos casos.** Permiten profundizar, no saturar. Los hallazgos son hipótesis fundamentadas, no regularidades establecidas.
- **Selección por conveniencia**, sobre la red de contactos del autor. No garantiza la diversidad de posiciones de un muestreo intencional por criterios.
- **Ningún entrevistado pertenece a una organización de verificación**, que era el perfil de mayor peso previsto en el diseño original.

## Referencias cruzadas

- [[wiki/investigacion/user-research]] — diseño de los instrumentos
- [[wiki/investigacion/encuesta-resultados]] — los datos que las entrevistas explican
- [[wiki/competencia/analisis-competitivo]] — océano azul, precisado con la entrevista 1
- [[wiki/solucion/requerimientos]] — consecuencias 1 y 2
- [[wiki/solucion/pruebas]] — consecuencia 3
- [[wiki/solucion/arquitectura]] — consecuencia 4
- [[wiki/negocio/modelo-de-negocio]] — consecuencias 5 y 6

## Fuentes

- Entrevista a Federico Maidan, agosto de 2026 — Anexo C del documento
- Entrevista a Ximena Soruco, agosto de 2026 — Anexo C del documento
