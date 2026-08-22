---
titulo: User Research
tipo: análisis
tags: [user-research, entrevistas, encuestas, user-persona]
fuentes: [PFI_MarcoTeorico_EstadoDelArte_UserResearch-Sabados.pdf, GR_M15_Feresini_Imbriago-EntregaFinal2025.pdf, WhatsApp-Chat-PFI-2026.zip, encuesta-desinformacion.xlsx]
actualizado: 2026-08-22
---

# User Research

> Estado: **encuesta ejecutada (140 respuestas, campo cerrado el 2026-08-18) — entrevistas pendientes**. Esta página contiene el diseño de los instrumentos; los resultados de la encuesta están en [[wiki/investigacion/encuesta-resultados]].

## Objetivo general del user research

Reunir evidencia empírica que **valide la viabilidad del problema y el apetito por la solución** antes de invertir en el desarrollo: confirmar que el segmento objetivo se topa con desinformación en Twitter/X, que percibe una dificultad real para detectarla por su cuenta, y que instalaría y confiaría en una extensión que le asista con un score + evidencia. Los instrumentos están alineados a los objetivos específicos del proyecto (clasificación en español, señales de la cuenta autora, contraste semántico, integración en extensión).

## Metodología

Se emplean los tres instrumentos que indica la cátedra (diapositivas de User Research), respetando los criterios transversales de **validez, confiabilidad, trazabilidad y coherencia**:

| Instrumento | Tipo | Objetivo | A quién |
|---|---|---|---|
| **Encuesta** ✅ | Cuantitativo, alcance amplio | Validar exposición al problema, capacidad de detección, comportamiento de verificación actual y apetito/confianza en la solución | Ciudadanos de **18-40 años** que siguen política/economía en **Twitter/X**. Meta: 120+ respuestas → **140 obtenidas, 107 en segmento**. Resultados: [[wiki/investigacion/encuesta-resultados]] |
| **Entrevistas** (2, semiestructuradas) | Cualitativo, profundidad | Comprender el flujo de verificación real, dolores y qué haría creíble la herramienta desde "personas de peso" | 1 periodista/editor + 1 fact-checker o académico de desinformación |
| **User Personas** (2-3) | Síntesis | Representación arquetípica de los usuarios, construida sobre la evidencia recolectada | Ciudadano común (primario), periodista/editor (secundario), fact-checker (opcional) |

> ⚠️ Nota de consigna (del chat de alumnos PFI 2026): **no hubo un acuerdo común único entre comisiones**. Las notas de la clase de **Monzón** piden "dos herramientas como base — encuestas, entrevistas y océano azul; encuestas mínimo 120 resultados; no hacer FODA" y "no pegar screenshots de Google Form". Las **diapositivas de los sábados** piden encuestas + entrevistas + user persona (sin número fijo). El tutor de este PFI es **Giro Uribazo**, cuya consigna exacta aún no se confirmó → **pendiente validar con él** el mínimo de muestra y si quiere océano azul en esta sección. El **océano azul ya está desarrollado** en [[wiki/competencia/analisis-competitivo]] (es análisis de competencia, no user research), por lo que no se duplica aquí.

---

## 1. Encuesta

**Objetivo específico:** medir, sobre el segmento primario, (a) exposición al problema, (b) capacidad autopercibida de detección, (c) comportamiento de verificación actual, y (d) apetito y confianza frente a la solución propuesta.

**Población objetivo:** personas de 18 a 40 años, residentes en Argentina, que usan Twitter/X y siguen noticias de política o economía.

**Meta de muestra:** 120+ respuestas válidas (estándar de la cátedra; el PFI de ejemplo alcanzó 160). **Resultado: 140 respuestas recibidas, 107 dentro del segmento objetivo.** Campo: 2026-07-04 a 2026-08-18.

**Variables a medir:** perfil/segmento (filtro), frecuencia de exposición a desinformación, preocupación, capacidad autopercibida, comportamiento de verificación, tiempo de verificación, intención de uso, confianza en un score automático, drivers de confianza, preocupaciones.

### Cuestionario aplicado

> El instrumento efectivamente aplicado tiene **14 preguntas**: la pregunta 10 del borrador original (*"¿Conocés o usás herramientas o sitios de verificación?"*) **no se incluyó** en la versión final, para acortar el cuestionario y sostener la tasa de finalización. La numeración de abajo conserva el orden aplicado.

**Bloque A — Perfil y filtro de segmento**

1. ¿Qué edad tenés? — *(opción única)* Menos de 18 · 18-25 · 26-33 · 34-40 · Más de 40
   *(filtro: fuera de 18-40 se etiqueta "fuera de segmento" para el análisis)*
2. ¿Con qué frecuencia usás Twitter/X? — *(única)* Varias veces al día · Una vez al día · Algunas veces por semana · Rara vez · No la uso
3. ¿Seguís noticias de política o economía en Twitter/X? — *(única)* Sí, frecuentemente · A veces · No

**Bloque B — Exposición al problema**

4. ¿Con qué frecuencia sentís que te cruzás con noticias o afirmaciones falsas, engañosas o no verificables en Twitter/X? — *(Likert)* Muy frecuentemente · Frecuentemente · A veces · Rara vez · Nunca
5. ¿Alguna vez compartiste, o estuviste a punto de compartir, contenido que después resultó falso o dudoso? — *(única)* Sí, lo compartí · Estuve a punto pero no lo hice · No · No sé
6. ¿Qué tan preocupado/a estás por la desinformación en las redes sociales en Argentina? — *(Likert 1-5)* Nada preocupado/a → Muy preocupado/a

**Bloque C — Capacidad y comportamiento actual**

7. ¿Qué tan capaz te sentís de distinguir por tu cuenta una noticia falsa de una verdadera en Twitter/X? — *(Likert 1-5)* Nada capaz → Muy capaz
8. Cuando dudás de una publicación, ¿qué hacés habitualmente? — *(opción múltiple)* Busco en Google · Comparo con medios que conozco · Consulto un verificador (Chequeado u otro) · Miro la cuenta que lo publicó · Le pregunto a alguien · Nada, sigo de largo · Otro
9. En promedio, ¿cuánto tiempo le dedicás a verificar una publicación que te genera dudas? — *(única)* Menos de 1 minuto · 1-3 minutos · Más de 3 minutos · No verifico

**Bloque D — Apetito y confianza en la solución**

10. Si existiera una extensión **gratuita** de Chrome que, al leer un tuit, te muestra un **puntaje de probabilidad** de que sea desinformación junto con **enlaces a fuentes** que lo corroboran o contradicen, ¿qué tan probable es que la instales y uses? — *(Likert 1-5)* Nada probable → Muy probable
11. ¿Qué tanto confiarías en un puntaje generado automáticamente por un sistema de IA para esto? — *(Likert 1-5)* No confiaría → Confiaría plenamente
12. ¿Qué te haría confiar **más** en una herramienta así? — *(opción múltiple)* Que muestre las fuentes/evidencia · Que explique por qué llega a ese resultado · Que sea transparente sobre su margen de error · Que la respalde una institución reconocida · Que no tenga sesgo político · Otro
13. ¿Cuál sería tu **mayor preocupación** con una herramienta así? — *(opción múltiple)* Que se equivoque (falsos positivos) · Sesgo político · Privacidad de mis datos · Que censure opiniones o sátira · Ninguna · Otro
14. *(abierta acotada, opcional)* En una frase: ¿qué te resultaría más útil de una herramienta que te ayude a detectar desinformación en Twitter/X?

### Aplicación (ejecutada)

1. **Piloto** con un grupo reducido del segmento → se detectó que el cuestionario era largo y se quitó la pregunta sobre conocimiento de verificadores.
2. **Distribución** digital y presencial, por conveniencia y bola de nieve: grupo de WhatsApp PFI 2026 (reciprocidad de respuestas, práctica del curso), redes personales y reparto presencial. Se priorizó la llegada al segmento 18-40 consumidor de noticias en X.
3. **Recolección** entre el 2026-07-04 y el 2026-08-18 → **140 respuestas**, de las cuales **107 caen dentro del segmento objetivo** (18-40 años, usa X, sigue política o economía).
4. **Análisis** con `scripts/analizar_encuesta.py`, que lee la planilla y emite tanto las tablas del wiki como las figuras `pgfplots` del documento. Gráficos propios — **sin screenshots del Google Form**, según la recomendación de la cátedra. Resultados completos en [[wiki/investigacion/encuesta-resultados]].
5. El **cuestionario y las tablas de frecuencia completas** se incluyen como anexo del documento (`chapters/appendix/surveys.tex`).

---

## 2. Entrevistas

**Modalidad:** semiestructurada (guión con preguntas guía + libertad para repreguntar). 6-10 preguntas, 30-45 minutos. Transcripción completa **va en anexo** (`chapters/appendix/interviews.tex`).

**Perfiles objetivo (el rol importa — la cátedra valora "personas de peso"):**
- **Entrevista 1 — Periodista o editor de medios** (segmento secundario): cómo verifica hoy, dolores del proceso, rol de X.
- **Entrevista 2 — Fact-checker (idealmente Chequeado) o académico de desinformación**: metodología de verificación, viabilidad de automatizar, riesgos en el contexto argentino.

### Guía de entrevista (periodista / fact-checker)

1. *(Contexto)* Contame sobre tu rol y cómo aparece la desinformación en tu trabajo día a día.
2. ¿Cómo es hoy tu proceso para verificar una afirmación o una publicación dudosa? ¿Qué herramientas usás?
3. ¿Cuáles son los mayores dolores o cuellos de botella de ese proceso? ¿Dónde perdés más tiempo?
4. ¿Qué rol juega Twitter/X, como fuente y como lugar donde se origina o amplifica la desinformación?
5. ¿Qué tan factible ves automatizar parte de la verificación? ¿Qué parte le confiarías a un sistema y qué parte no?
6. Si tuvieras una herramienta que da un puntaje de probabilidad acompañado de evidencia, ¿cómo la usarías? ¿Qué la haría confiable para vos?
7. ¿Qué riesgos o límites le ves a un sistema automático de detección en el contexto argentino (sesgo, polarización, sátira)?
8. *(Validación abierta)* ¿Qué les falta a las soluciones actuales que vos necesitarías?
9. *(Cierre)* ¿Algo que no te haya preguntado y creas importante?

### Estrategia de captación (no hay contactos confirmados aún)

- **Chequeado**: contacto directo por su formulario/mail institucional o LinkedIn; es el interlocutor de mayor peso posible.
- **Periodistas/editores**: LinkedIn, red personal, docentes de UADE con perfil periodístico o de comunicación.
- **Académicos**: investigadores de desinformación/NLP en universidades argentinas (UBA, UADE, CONICET).
- **Grupo PFI 2026**: preguntar si algún compañero tiene contacto.

**Plan B (si no se consigue un rol de peso a tiempo):** entrevistar a 2 *power-users* del segmento primario — consumidores intensivos de noticias en X — con una guía adaptada (más corta, centrada en su experiencia como lector: cómo consume, cómo detecta, qué verifica, si usaría la extensión y qué la haría creíble). Es un plan de contingencia, no el preferido: la cátedra valora entrevistados con rol relevante.

---

## 3. User Personas

Se elaborarán **2-3 personas** una vez recolectada la evidencia (encuesta + entrevistas). No son usuarios inventados: son una síntesis basada en datos. Cada una lleva los componentes que pide la cátedra: nombre ficticio + demografía, contexto/rol, objetivos, frustraciones, comportamientos/hábitos y una cita representativa. Se presentan como figuras en el documento.

### Persona 1 — Ciudadano/a consumidor/a de noticias en X *(primario)*

> Construida sobre las 107 respuestas del segmento. Cada atributo se apoya en la moda o la media de la variable correspondiente; el dato de respaldo va entre paréntesis.

- **Nombre y demografía:** Nicolás, 24 años, AMBA. Estudiante universitario que trabaja *(franja 18-25, 59,3 % de la muestra total)*.
- **Contexto y rol:** entra a Twitter/X al menos una vez por día *(61,4 %)* y sigue noticias de política y economía en la plataforma *(85,7 % entre "frecuentemente" y "a veces")*. No es periodista ni verificador: es lector.
- **Objetivos:** enterarse rápido de lo que pasa sin comerse una noticia falsa, y no quedar expuesto por compartir algo que después resulta ser mentira.
- **Frustraciones:** se cruza con contenido dudoso de forma frecuente o muy frecuente *(73,9 %)* y ya pasó por compartir o estar a punto de compartir algo falso *(61,7 %)*. Está muy preocupado por el tema *(media 4,20 sobre 5)* pero no se siente del todo equipado para resolverlo solo *(capacidad autopercibida 3,58)*. Desconfía de que cualquier herramienta del tema termine tomando partido político *(84,1 % pide neutralidad)*.
- **Comportamientos:** ante la duda googlea *(83,2 %)* y mira quién publicó el tuit *(71,0 %)*, pero cierra el asunto en menos de tres minutos *(75,7 %)* y muchas veces en menos de uno *(35,5 %)*. Rara vez llega a un verificador profesional.
- **Relación con la solución:** instalaría la extensión *(intención media 4,06)*, pero le creería al puntaje bastante menos de lo que la usaría *(confianza media 3,57)*. Le teme sobre todo al falso positivo *(66,4 %)* y a que se censure una opinión o una sátira *(57,0 %)*.
- **Cita representativa:** *"Que me muestre las fuentes en el momento, no que me diga si es verdad o mentira y listo."* — síntesis de las respuestas abiertas, donde el pedido recurrente es evidencia visible y explicación del resultado.

### Persona 2 — Periodista / editor *(secundario)*
- **Nombre y demografía:** [a completar]
- **Contexto y rol:** verifica fuentes antes de publicar; usa la herramienta como screening.
- **Objetivos / Frustraciones / Comportamientos:** [a completar con datos de la entrevista]
- **Cita representativa:** "[a completar]"

### Persona 3 — Fact-checker *(opcional, según evidencia)*
- [a completar si se realiza la entrevista al verificador]

---

## Insights clave

Los ocho insights derivados de la encuesta, con su evidencia y su consecuencia sobre el proyecto, están consolidados en [[wiki/investigacion/encuesta-resultados]]. Los tres que más pesan sobre el diseño:

1. **Existe una brecha entre preocupación (4,20) y capacidad autopercibida (3,58).** Es el espacio que ocupa el producto: el segmento quiere resolver el problema y no se siente equipado para hacerlo solo.
2. **La intención de uso (4,06) supera a la confianza en el puntaje (3,57).** El sistema no puede devolver un número solo; la evidencia y la explicación son condición de uso, no un adorno de la interfaz.
3. **La neutralidad política es el driver dominante (84,1 %), veinte puntos por encima del segundo.** Obliga a clasificar afirmaciones fácticas y no opiniones, a excluir la sátira y a comunicar el resultado en términos probabilísticos.

Falta incorporar los insights cualitativos de las entrevistas, todavía pendientes.

## Referencias cruzadas

- [[wiki/proyecto/propuesta]] — segmentos objetivo (primario 18-40 en X, secundario periodistas)
- [[wiki/proyecto/contexto-problema]] — estadísticas que la encuesta busca validar localmente
- [[wiki/competencia/analisis-competitivo]] — océano azul y matriz ERIC (ya desarrollados)
- [[wiki/solucion/requerimientos]] — los insights alimentan los requerimientos
- [[wiki/investigacion/encuesta-resultados]] — resultados, hallazgos y limitaciones de la encuesta
- [[wiki/negocio/modelo-de-negocio]] — apetito y disposición validan el modelo

## Fuentes

- [[raw/clases/PFI_MarcoTeorico_EstadoDelArte_UserResearch-Sabados.pdf]] — método de la cátedra
- PFI de ejemplo Feresini/Imbriago 2025 (Sparkle) — estructura de referencia de la sección
- Chat WhatsApp PFI 2026 — consigna de Monzón (mín. 120, sin FODA, sin screenshots) y práctica del curso
- [[raw/investigacion/encuesta-desinformacion.xlsx]] — respuestas de la encuesta (140)
