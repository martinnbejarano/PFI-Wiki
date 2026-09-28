---
titulo: Calibración contra la tesis de referencia (Sparkle 2025)
tipo: análisis
tags: [calibracion, referencia, entrega, 50, 90, alcance, diagramas, requerimientos, estilo]
fuentes: [GR_M15_Feresini_Imbriago-EntregaFinal2025.pdf, Rubrica-EP2-50porciento.pdf]
actualizado: 2026-09-28
---

# Calibración contra la tesis de referencia (Sparkle 2025)

Comparación de los artefactos de este PFI contra **Sparkle: Gamificación en tiempo real para reuniones virtuales en entornos educativos** (Feresini y Imbriago, tutor Monzón, entrega final marzo 2026, 141 páginas). Se compara únicamente lo que entra en la Entrega del 50 %: requerimientos, casos de uso, diagramas, mockups y herramientas de marketing. Quedan fuera el análisis financiero, las pruebas realizadas y las transcripciones, que son de la entrega final.

La tesis de referencia es una **entrega final**, no una del 50 %, así que su volumen total no es el objetivo. Lo que sí es directamente comparable es la **cantidad y la profundidad de cada artefacto de diseño**, porque ese contenido no cambia entre una instancia y la otra.

> **Documento previo al volcado (2026-08).** Las cifras de la columna "Este PFI hoy" son las del wiki *antes* de escribir los capítulos 3 y 4. Las recomendaciones se aplicaron: ver [[#Resultado del volcado]] al final para los números efectivos del documento.

## Tabla comparativa

| Artefacto | Sparkle 2025 | Este PFI hoy | Relación |
|---|---|---|---|
| Requerimientos funcionales | **11** | 29 | 2,6× |
| Requerimientos no funcionales | **7** | 17 | 2,4× |
| Casos de uso | **5** | 7 | 1,4× |
| Diagramas técnicos propios | **9** | 9 | **1,0×** |
| Pantallas de *frontend* | **8** | 4 | 0,5× |
| Herramientas de marketing | **8** | 6 | 0,75× |

## Requerimientos: el formato pesa tanto como la cantidad

Los once requerimientos funcionales de Sparkle son **viñetas de una sola oración, sin tabla y sin columna de prioridad**:

> **RF01.** El sistema debe integrarse con Google Meet, permitiendo la incrustación de su interfaz en la videollamada sin necesidad de utilizar dos sistemas por separado.

Los siete no funcionales tienen el mismo formato. Ocupan **dos páginas entre los dieciocho**, y esa es la referencia real: no solo son menos, sino que están escritos de la forma más compacta posible. Este PFI tiene veintinueve funcionales repartidos en cinco tablas con columna de prioridad MoSCoW, más párrafos de justificación entre tabla y tabla — unas seis páginas para el mismo apartado.

El único lugar donde este PFI está por encima y conviene que lo esté es la **prioridad MoSCoW**, que Sparkle no tiene: es información real sobre qué entra en el prototipo y qué no, y cabe en una columna. La conclusión de la comparación es que hay que bajar la cantidad **y** compactar el formato: una sola tabla de funcionales y una de no funcionales.

## Casos de uso: la profundidad es menor de la que se escribió

Los cinco casos de uso de Sparkle tienen esta estructura fija, y ocupan unas tres cuartas partes de página cada uno:

- Actor principal / Actores secundarios
- Descripción (un párrafo)
- Flujo de eventos: entre cuatro y seis pasos numerados
- Flujos alternativos: **una o dos viñetas, sin identificador de paso**
- Precondición / Postcondición

Los de este PFI tienen hasta **seis flujos alternativos identificados por el paso donde se bifurcan** (*3a*, *5b*, *3a-7a*). Esa notación es más rigurosa que la de la referencia, pero es la que hace que la sección se duplique en extensión. Bajando a un máximo de tres alternativos por caso y sin identificador de paso, **los siete casos entran en el mismo espacio en que la referencia pone cinco**.

## Diagramas: la cantidad está bien, la densidad no

Sparkle tiene nueve diagramas técnicos propios. Este PFI tiene nueve. **La cantidad no es el problema, y la recomendación previa de bajar a cinco era incorrecta.** Sparkle incluso desarrolla los tres niveles del modelo C4, que es exactamente lo que se había puesto en duda.

| Sparkle | Este PFI |
|---|---|
| 3.7 Casos de uso | `casos-de-uso` |
| 3.8 Secuencia del flujo principal (uno) | `secuencia-cu01` y `secuencia-cu02` (dos) |
| 3.22 Arquitectura AWS simplificada | `despliegue-red` |
| 3.23 Arquitectura AWS completa | — |
| 3.24 Esquema NoSQL | `der` |
| 3.25 Estructuras clave en Redis | — |
| 3.26 C4 Nivel 1 — contexto | `c4-contexto` |
| 3.27 C4 Nivel 2 — contenedores | `c4-contenedores` |
| 3.28 C4 Nivel 3 — componentes | `c4-componentes` |
| — | `flujo-informacion` |

Lo que sí difiere es **cuánto entra en cada dibujo**:

| Diagrama | Sparkle | Este PFI | Relación |
|---|---|---|---|
| C4 Nivel 1 — contexto | 6 cajas, 7 aristas | 12 cajas, 9 aristas | 2× |
| C4 Nivel 2 — contenedores | 9 cajas, 9 aristas | 15 cajas, 11 aristas | 1,7× |
| **C4 Nivel 3 — componentes** | **5 cajas, 6 aristas** | **22 cajas, 25 aristas** | **4,4×** |
| Flujo de información | (no tiene) | 39 cajas, 32 aristas | — |

El nivel 3 de Sparkle son cinco cajas dentro de un contenedor rotulado *Backend Node.js*: módulo de transcripción externa, módulo de IA, módulo de lógica de gamificación, capa de persistencia y manejador de WebSockets. Nada más. El de este PFI abre el Módulo 3 en cinco componentes internos, suma tres puntos de entrada, el orquestador y la capa de repositorios.

**Ahí es donde este proyecto se pasó de profundidad**, y es un diagrama, no nueve. El de flujo de información es el segundo candidato: treinta y nueve nodos es mucho para un diagrama de actividad, aunque la naturaleza del artefacto justifica más nodos que un C4.

Un patrón que Sparkle aplica y conviene copiar: **cada diagrama va seguido de una lista de viñetas que nombra y describe cada elemento, más un párrafo de flujo general**. El dibujo queda simple y la densidad se traslada al texto, donde no arruina la legibilidad.

## Mockups: este PFI está por debajo

Sparkle presenta ocho pantallas, una por figura: inicio, carga de archivo de contexto, panel principal, registro de estudiante, validación, pregunta activa, respuesta y retroalimentación. Este PFI presenta cuatro, aunque cada una muestra varios estados a la vez —los cuatro estados del indicador, el detalle en su versión completa y en su versión degradada—.

Cuatro es defendible por densidad, pero **la comparación deja de sostener el argumento de recortar acá**. Si hay una pantalla que conviene sumar es la del reporte de veredicto incorrecto, que hoy deja a CU-04 sin respaldo visual.

## Herramientas de marketing

| Herramienta | Sparkle | Este PFI |
|---|---|---|
| Océano azul | Sí | Sí |
| Matriz ERIC | Sí (como figura) | Sí (como tabla) |
| **Diccionario de variables** | **Sí** | **No** |
| **Curva de valor** | **Sí** | **No** |
| Tabla comparativa de atributos | Sí | Sí |
| Cruz de Porter | Sí (como figura) | Sí (en prosa) |
| Análisis FODA | Sí (como figura) | Sí (como tabla) |
| Business Model Canvas | Sí (como figura) | Sí (como tabla) |
| Mix de marketing (4P) | No | No |
| Matriz Boston Consulting | No | No |

Ninguna de las dos usa las 4P ni la Matriz Boston Consulting, pese a que la rúbrica las nombra. Lo que Sparkle tiene y este PFI no es la **curva de valor** con su **diccionario de variables**, que es el cierre natural del análisis de océano azul: el diccionario define los atributos que se comparan y la curva los grafica contra los competidores. Es la adición de mayor valor del apartado, porque completa una herramienta ya empezada en lugar de agregar una suelta.

Sparkle además dibuja la Cruz de Porter, el FODA y el BMC **como figuras y no como tablas**. Es una decisión de presentación que hace el capítulo más visual.

## Metodología de desarrollo

Sparkle declara un enfoque ágil con *sprints*, reuniones semanales, retrospectivas antes de cada entrega parcial y **una tabla de Product Backlog** (Tabla 4.I). Su capítulo 4 tiene cinco secciones cortas: planificación y definición de requisitos, iteraciones y dinámica de trabajo, diseño del sistema y arquitectura, implementación, y pruebas y validación. Ocupa tres páginas.

Es un molde directamente reutilizable. La diferencia honesta es que este proyecto trabaja con un tablero de *issues* y no con *sprints* de duración fija, así que corresponde declarar Kanban y no Scrum, con la tabla de trabajo pendiente cumpliendo el rol del Product Backlog.

## Conclusiones para el volcado

1. **Requerimientos: bajar de 29 a unos 13, en una sola tabla.** La referencia tiene 11 en viñetas sin prioridad.
2. **No funcionales: 17 sigue siendo 2,4× la referencia**, aunque al vivir en una sola tabla ocupan una página. Es la decisión con más margen de criterio.
3. **Casos de uso: los siete, pero al formato de la referencia** — máximo tres flujos alternativos, sin identificador de paso.
4. **Diagramas: los nueve quedan.** La cantidad coincide exactamente con la referencia.
5. **Simplificar `c4-componentes`**, que es 4,4 veces la densidad de su equivalente. Colapsar el Módulo 3 en una caja y trasladar el detalle a las viñetas del texto.
6. **Sumar la curva de valor con su diccionario de variables**, que es lo único del apartado de marketing donde la referencia está por encima.
7. **Los mockups no se recortan.** Este PFI ya está por debajo de la referencia.

## Calibración para la entrega del 90 % (2026-09-28)

La primera parte de esta página cubre solo lo del 50 %. Esta sección compara las partes que entran al 90 %: Resumen, competencia, lo legal, metodología, pruebas, discusión y conclusión, más el tono y la profundidad del texto. Sirve de **ejemplo de cuánto profundizar, cómo escribir y cómo estructurar**.

### Estructura de Sparkle

| Cap. | Contenido | Nota |
|---|---|---|
| 1 | Introducción: objetivo, alcance, descripción | — |
| 2 | Antecedentes: 2.1 Marco Teórico · 2.2 Estado del arte (cierra con **2.2.4 Conclusión**) · **2.3 Competencia** | La competencia es hermana del EdA, no parte de él |
| 3 | Descripción: 3.1 User Research · 3.2 Solución (requerimientos, casos de uso, producto/*branding*, pantallas, tecnologías, arquitectura) · 3.3 Modelo de negocio · 3.4 Análisis financiero · **3.5 Análisis legal** | Lo legal va al final del cap. 3 |
| 4 | Metodología de Desarrollo: 5 secciones cortas | 3 páginas |
| 5 | **Pruebas realizadas**: casos de prueba funcionales, usabilidad en entorno real, validación complementaria, síntesis | Capítulo propio |
| 6 | **Discusión**: líneas de evolución (trabajo futuro) | 1 página |
| 7 | **Conclusión** | 1 página |

No tiene marco normativo, porque la pauta de 2025 no lo pedía. La pauta del 75 % de 2026 sí lo pide, y también pide *Validación del sistema* dentro del cap. 4. En esos dos puntos manda la pauta y no la referencia.

### Extensión, en palabras aproximadas

| Sección | Sparkle | Este PFI | Relación |
|---|---:|---:|---|
| Marco teórico | ~3 600 | ~3 050 | 0,85× |
| Estado del arte | ~1 550 | ~2 900 | 1,9× |
| Competencia | ~2 200 | ~1 650 (+ soluciones comerciales, que se mudan) | ~1× |
| **Análisis legal** | **~550** | **~2 500** | **4,5×** |
| Metodología (cap. 4 propiamente dicho) | ~1 000 | — | — |
| Pruebas / validación | ~3 300, con 5 tablas de casos de prueba | ~1 250, solo protocolo | 0,4× |
| Discusión | ~370 | — | — |
| Conclusión | ~330 | «Completar.» | — |
| Resumen | **~130 palabras, sin palabras clave** | «Completar.» | — |

### Cómo se escribe cada parte

- **Resumen:** dos párrafos cortos con el problema, qué se desarrolló, qué usa, qué busca y cómo se implementó (MVP integrado a Google Meet). No da números de resultados ni palabras clave. El Abstract es la traducción literal.
- **Apertura de sección:** siempre un párrafo que anuncia qué viene. «En esta sección se presentan…», y después el recorrido: «En primer lugar… A continuación… Luego… Finalmente…».
- **Marco teórico:** cada concepto se define con dos o tres autores que se contrastan, y cierra con «para este proyecto interesa…», que ata la definición al producto. Usa viñetas en negrita para las taxonomías.
- **Estado del arte:** cierra con una **subsección «Conclusión»** de dos párrafos que resume los hallazgos con citas agrupadas y enuncia la oportunidad que justifica el producto.
- **Competencia:**
  - Abre con un párrafo de propósito.
  - Sigue con «Plataformas competitivas»: un párrafo por competidor, citando su sitio web (`(Kahoot!, 2025)`).
  - Después vienen Océano azul, ERIC como figura, diccionario de variables en viñetas, curva de valor y tabla comparativa Sí/No/Limitada.
  - Cierra con **«Síntesis del análisis competitivo»** (unos 4 párrafos).
- **Análisis legal:** tres subsecciones (datos personales, propiedad intelectual, términos y condiciones), cada una de 1 o 2 párrafos, con la ley y los artículos concretos. Los términos y condiciones son una lista numerada de 5 ítems. No tiene análisis de riesgos, cesión ni honor.
- **Metodología:** enfoque ágil sin *sprints* fijos, revisión semanal y Product Backlog en tabla (con una columna **«Entrega»**, que la pauta 2026 ya no admite).
- **Pruebas:**
  - Un párrafo introductorio con las tres etapas.
  - Cinco casos de prueba en tabla (objetivo, RF cubiertos, precondiciones, entradas, pasos, resultado esperado, resultado real y resultado de la prueba).
  - Una prueba de usabilidad narrada con fotos del uso real, una tabla de mediciones de latencia contra el RNF y cuestionarios cualitativos en tabla (pregunta → respuesta textual).
  - Cierra con una síntesis que da números (100 % de RF cubiertos, latencia media de 3,17 s).
- **Discusión:** trabajo futuro en prosa, por ejes (tecnológico, pedagógico, investigación), y cierra con «En síntesis, … cuatro ejes».
- **Conclusión:** cuatro párrafos en prosa general (problema → innovación → resultados de la validación → aporte). **No va objetivo por objetivo ni tiene sección de limitaciones.**

### Citas

- Las leyes van como recurso online con URL de InfoLEG y fecha de consulta: `CONGRESO DE LA NACIÓN ARGENTINA, 2000. Ley N.º 25.326…`.
- Los competidores y la documentación de Google (*vendors*) se citan como web. La pauta 2026 prohíbe los *vendors*, pero no dice nada de las leyes.

### Qué tomar y qué no

- **Tomar:** los párrafos de apertura con el recorrido, la conclusión al cierre del EdA, la síntesis al cierre de la competencia, las tablas de casos de prueba con resultado real, las fotos y mediciones de la prueba de usabilidad, un Resumen corto y la conclusión en prosa.
- **No tomar:** la columna «Entrega» del backlog, las citas a documentación de *vendors* y frases que el estilo de este PFI prohíbe y Sparkle usa («En este sentido», «resulta de especial importancia»).

## Referencias cruzadas

- [[wiki/proyecto/plan-volcado-documento]]
- [[wiki/proyecto/entrega-50-alcance]]
- [[wiki/solucion/requerimientos]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/mockups]]
- [[wiki/competencia/analisis-competitivo]]
- [[wiki/proyecto/entrega-90-alcance]]

## Fuentes

- [[raw/clases/GR_M15_Feresini_Imbriago-EntregaFinal2025.pdf]]
- [[raw/clases/Rubrica-EP2-50porciento.pdf]]

## Resultado del volcado

Estado efectivo del documento al 2026-08-22, después de aplicar las conclusiones de arriba.

| Artefacto | Sparkle 2025 | Recomendado aquí | **Documento final** | Relación |
|---|---|---|---:|---|
| Requerimientos funcionales | 11 | ~13 | **16** | 1,5× |
| Requerimientos no funcionales | 7 | 17 (sin cambio) | **17** | 2,4× |
| Casos de uso | 5 | 7 | **7** | 1,4× |
| Diagramas técnicos propios | 9 | 9 | **9** | 1,0× |
| Pantallas de *frontend* | 8 | 4 | **4** | 0,5× |
| Herramientas de marketing | 8 | +curva de valor | **5** (ERIC, curva de valor, FODA, 5 fuerzas, 4P) | 0,63× |

Los requerimientos funcionales bajaron de 29 a **16**, algo por encima de los 13 sugeridos pero dentro del orden de magnitud de la referencia. Los no funcionales quedaron en 17, como estaba previsto. La curva de valor se construyó con su diccionario de variables. **Los números autoritativos son los del documento**; el wiki `solucion/requerimientos.md` está alineado con ellos.
