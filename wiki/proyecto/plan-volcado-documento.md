---
titulo: Plan de volcado al documento — Entrega 50%
tipo: proyecto
tags: [plan, entrega, 50, volcado, latex, rubrica]
fuentes: [Rubrica-EP2-50porciento.pdf]
actualizado: 2026-08-18
---

# Plan de volcado al documento — Entrega 50%

Estado de cada artefacto de diseño producido entre el 09 y el 11 de agosto, y cómo se traduce al documento LaTeX. **Nada de esto se vuelca hasta que el plan tenga el visto bueno.**

Faltan cuatro días para el 22/08. La distinción que organiza todo lo que sigue:

- **Criterios 5 y 6 (tecnologías, arquitectura de red, modelo de datos): ya están en el documento.** Se volcaron el 11/08 y el capítulo compila. Acá solo se revisan.
- **Criterios 1, 2, 3 y 4 (requerimientos, mockups, diagramas, competencia): están escritos en el wiki y no están en el documento.** Es el trabajo de volcado propiamente dicho.

---

## Criterio 1 — Requerimientos y casos de uso

**Origen:** [[wiki/solucion/requerimientos]] (313 líneas). **Destino:** `chapter04.tex`, sección nueva antes de *Modelo de datos*.

### Qué se hizo

Veintinueve requerimientos funcionales agrupados en cinco bloques temáticos —detección y análisis, presentación al usuario, retroalimentación y configuración, plataforma para organizaciones, persistencia y trazabilidad— cada uno con prioridad MoSCoW. Diecisiete requerimientos no funcionales en siete categorías (rendimiento, calidad del modelo, explicabilidad, privacidad, disponibilidad, seguridad, compatibilidad, costo, usabilidad, mantenibilidad, legalidad), **cada uno con un número comprometido en lugar de un adjetivo**: 2 segundos en el percentil 95, F1 macro de 0,80, 14 dólares mensuales, 50 milisegundos en el hilo principal.

Siete casos de uso con actor, precondición, flujo principal numerado, flujos alternativos identificados por paso (*3a*, *5b*) y postcondición. Cuatro actores: Ciudadano, Extensión (actor de sistema), Analista B2B y Sistema cliente (actor de sistema). Matriz de trazabilidad caso de uso → requerimientos, con la justificación explícita de los cuatro requerimientos que no tienen caso de uso asociado.

### Cómo se hizo

Los requerimientos no se listaron: se derivaron de las ocho decisiones de producto de [[wiki/proyecto/plan-bloque-diseno]] y del alcance de [[wiki/proyecto/propuesta]]. Tres decisiones estructurales atraviesan la lista entera y son las que hay que poder defender en la exposición:

1. **El análisis ocurre en dos flujos, no en uno.** El Módulo 1 corre automático sobre los tuits visibles; los Módulos 2, 3 y 4 solo a pedido. De ahí salen dos requerimientos de latencia distintos (RNF-01 y RNF-02) en lugar de uno solo que tendría que ser el peor de los dos.
2. **Dos tipos de usuario con necesidades opuestas.** Ciudadano anónimo y gratuito; cliente organizacional autenticado y pago. El modelo de negocio depende de que ambos existan.
3. **La evidencia tiene jerarquía**: fuente oficial, medios de referencia, verificadores profesionales, en ese orden.

La numeración no se recicla: RF-28 y RF-29 aparecen al final de sus tablas aunque pertenezcan temáticamente a bloques anteriores, para que «RF-08» signifique lo mismo en agosto y en noviembre.

### Qué falta o necesita validación

- **Ningún requerimiento está validado con usuarios.** Los RNF con número son objetivos de diseño, no mediciones; el documento debe decirlo con esas palabras. Se validan experimentalmente en la Entrega 5.
- **El F1 macro de 0,80 de RNF-05 no tiene respaldo experimental propio.** Es un objetivo tomado de la literatura ([[wiki/estado-del-arte/toapanta-2024-latam]] reporta 96 % en FakeDeS, [[wiki/estado-del-arte/brechas-espanol-latam]] documenta una degradación de ~26 pp fuera de dominio). Hay que decidir si se declara como objetivo o se rebaja.
- **RF-16, RF-17 y RF-19 no tienen mockup.** No afecta a la rúbrica, pero CU-04 queda sin respaldo visual.
- **La numeración salteada va a leerse como error** si no se explica. Se agrega un párrafo que enuncie la regla.

### Cómo se vuelca

Sección `\section{Requerimientos}` con dos subsecciones y una tercera para los casos de uso.

- **Seis tablas** en el formato ya usado en el capítulo (`\begin{table}[t]`, `\small`, `\caption` con «Fuente: elaboración propia», `\label{tab:...}`): cinco de funcionales por bloque y una de no funcionales. Columna de descripción con `p{}` de ancho fijo, como `tab:entidades`.
- **Los siete casos de uso en prosa estructurada**, no en tabla: actor y precondición en un párrafo introductorio, flujo principal como `\begin{enumerate}`, flujos alternativos como `\begin{itemize}` con el identificador de paso en negrita.
- **Matriz de trazabilidad** como séptima tabla, más el párrafo que justifica los cuatro requerimientos huérfanos.
- **Figura `casos-de-uso.png`** (ya exportada) con su pie explicando las dos relaciones `<<include>>`.
- **Adaptación de tono:** los comentarios del wiki que empiezan con «Es el caso de uso que más veces se ejecuta» se convierten en prosa impersonal o se eliminan. Las notas de por qué cambió un requerimiento respecto de su versión anterior —RNF-06, RNF-07, RNF-08— **no van al documento**: son historial de trabajo, no contenido académico. Van a `documento/history/`.
- **Castellanización:** *score* → puntaje, *timeline* → *timeline* (en cursiva, no tiene equivalente usable), B2B → «plataforma para organizaciones» en los títulos y «B2B» en las tablas, como ya se resolvió en la sección de modelo de datos.

**Extensión estimada:** 9 a 11 páginas. Es la sección más larga del capítulo.

---

## Criterio 2 — Mockups

**Origen:** [[wiki/solucion/mockups]] + `wiki/assets/mockups/mockups.html`. **Destino:** `chapter04.tex`, subsección dentro de la sección de requerimientos o sección propia.

### Qué se hizo

Cuatro pantallas: indicador sobre el tuit en sus cuatro estados visibles, detalle del veredicto con su variante de análisis parcial, panel de evidencia con siete fuentes, y panel de tendencias para organizaciones. Capturas en `documento/chapters/figures/`: `badge.png`, `popup.png`, `evidencia.png`, `dashboard.png`.

### Cómo se hizo

**En HTML y CSS reales, no dibujadas en una herramienta de diseño.** La razón es práctica: la extensión de la demo hereda este marcado, así que el indicador del *mockup* y el de la demo son el mismo componente. Las capturas se generan con Chrome en modo *headless* a doble resolución, con un parámetro de URL que esconde la barra de navegación.

Tres decisiones de diseño que sostienen requerimientos y no son cosméticas:

- **El estado se comunica por tres canales a la vez** —color, forma del ícono y texto—, que es lo que hace cumplible RNF-15 para un usuario que no distingue rojo de verde.
- **Ningún indicador afirma por sí mismo que el contenido sea falso.** El nivel severo atribuye el juicio a las fuentes: «Contradicho por fuentes oficiales». Es la traducción visual de RNF-07 y lo que hace entrar el enunciado en la eximente del art. 113 del Código Penal.
- **La ausencia de un módulo se muestra como ausencia**, con barra rayada y la etiqueta *sin dato*, en lugar de disimularse promediando sobre lo que haya.

### Qué falta o necesita validación

- **Todo el contenido es ficticio** —cuentas, tuits, titulares y verificaciones inventados sobre temas argentinos verosímiles—. Cada pantalla lleva un rótulo que lo aclara. **Ese rótulo tiene que sobrevivir al pie de figura del documento**: si el PDF muestra un `@` que parece real señalado como fuente de desinformación, contradice el apartado ético dos secciones antes.
- **No hay validación con usuarios.** Ningún usuario vio estas pantallas. La rúbrica no lo pide en esta instancia, pero es la pregunta obvia del tutor.
- **Faltan tres pantallas** (instalación/configuración, formulario de reporte, estados de error de red). Ninguna afecta a la rúbrica.

### Cómo se vuelca

Cuatro figuras con pie extenso. El pie hace el trabajo pesado, porque una captura sin explicación no muestra decisiones de diseño: cada uno nombra el requerimiento que realiza, el caso de uso al que pertenece y la decisión de diseño que la pantalla materializa, y **el de las cuatro aclara que el contenido es ficticio**.

Cuestión de tamaño: `badge.png` y `popup.png` son verticales y entran a `0.6\linewidth`; `evidencia.png` y `dashboard.png` son anchas y probablemente necesiten `landscape`, como ya se hizo con el DER y el diagrama de despliegue.

**Extensión estimada:** 3 a 4 páginas, casi todo figura.

---

## Criterio 3 — Diagramas y arquitectura

**Origen:** [[wiki/solucion/arquitectura]] (165 líneas). **Destino:** `chapter04.tex`, sección *Arquitectura del sistema*, que hoy dice `Completar.`

### Qué se hizo

Nueve diagramas en draw.io, revisados uno por uno y exportados a PNG a 3× recortado al contenido (entre 2.700 y 4.100 px de ancho):

| Diagrama | Qué muestra | ¿En el documento? |
|---|---|---|
| `c4-contexto` | Dos personas, siete sistemas externos, jerarquía de evidencia dibujada | No |
| `c4-contenedores` | Seis contenedores con su tecnología y responsabilidad | No |
| `c4-componentes` | Tres puntos de entrada, orquestador, Módulo 3 abierto en cinco componentes | No |
| `flujo-informacion` | Actividad UML, cinco calles, bifurcación de los dos flujos, M2 y M3 en paralelo | No |
| `secuencia-cu01` | Flujo automático, seis líneas de vida, `alt` de caché y `opt` de fallo | No |
| `secuencia-cu02` | Flujo a demanda, diez líneas de vida, `opt` de verificadores, `alt` de degradación | No |
| `casos-de-uso` | Cuatro actores, siete casos de uso, dos `<<include>>` | No |
| `despliegue-red` | Cinco zonas por grado de control, cruces de frontera con el dato que sale | **Sí** |
| `der` | Diecisiete entidades, veinte relaciones, cinco dominios por color | **Sí** |

Además de los diagramas, la página contiene el texto que los explica: la descripción de los tres niveles C4, la ingesta de fuentes oficiales, el flujo de información, las dos secuencias, el despliegue con la tabla de zonas y la tabla de dependencias externas con su modo de falla, y **nueve decisiones de arquitectura con las alternativas evaluadas y el motivo del descarte**.

### Cómo se hizo

La revisión encontró defectos en siete de los ocho diagramas que existían entonces. Dos no eran cosméticos:

- **El diagrama de flujo tenía un error de modelado**: mostraba los Módulos 2 y 3 en cadena, como si el segundo esperara al primero. Son independientes. Ahora van como bifurcación paralela.
- **Los mensajes del actor en los diagramas de secuencia salían en diagonal**, lo que en un diagrama de secuencia sugiere que el mensaje ocurre en un instante distinto en cada extremo.

Las nueve decisiones de arquitectura están escritas con su alternativa descartada. La que más se va a preguntar en la exposición: **la inferencia vive fuera del contenedor de la API por presupuesto y no por memoria**. El plan Hobby de Railway no impone techo de RAM; lo que decide es RNF-14.

### Qué falta o necesita validación

- **Nada de esto está implementado.** La arquitectura es de diseño; el documento tiene que enunciarla en futuro o en voz de propuesta, no como si el sistema existiera.
- **Cuatro decisiones quedan abiertas y la página lo dice**: reintentos y *timeouts* por servicio externo, política de expiración del caché, periodicidad exacta de la ingesta por fuente, y versionado del contrato de la API. Van al documento como decisiones diferidas, igual que se hizo en la sección de modelo de datos.
- **Ninguna latencia está medida.** Los 2 y 8 segundos son presupuesto de diseño repartido entre módulos, no una medición.

### Cómo se vuelca

Sección `\section{Arquitectura del sistema}` con seis subsecciones: descripción general y las dos restricciones que le dan forma; los tres niveles C4; la ingesta de fuentes oficiales; el flujo de información; las dos secuencias; y las decisiones de arquitectura.

- **Siete figuras nuevas.** Los tres C4 y el de casos de uso entran verticales; `flujo-informacion` y las dos secuencias casi seguro necesitan `landscape`.
- **Dos tablas**: dependencias externas con su modo de falla, y las nueve decisiones de arquitectura con sus alternativas. La segunda es la que más puntúa: muestra que hubo evaluación y no elección por defecto.
- **La tabla de zonas de despliegue ya está** en la sección de tecnologías (arquitectura de red). No se repite: se referencia.
- **El diagrama de despliegue ya está en el documento.** Al escribir la sección de arquitectura hay que reordenar para que la figura quede cerca de la primera mención, o dejar la referencia cruzada.

**Extensión estimada:** 8 a 10 páginas.

> ⚠️ Riesgo de volumen: entre requerimientos, mockups y arquitectura, el capítulo 4 pasa de 5.229 palabras a unas 12.000 y de 2 figuras a 13. Es mucho, pero son los criterios que la rúbrica puntúa. La alternativa —mandar diagramas al anexo— resta puntos, porque el evaluador los busca en el capítulo.

---

## Criterio 4 — Competencia y herramientas de marketing

**Origen:** [[wiki/competencia/analisis-competitivo]] y [[wiki/negocio/modelo-de-negocio]]. **Destino:** `chapter03.tex`, **que hoy está comentado en `main.tex`**.

### Qué se hizo

Seis competidores relevados con fortalezas y debilidades (Information Tracer, Diggity, Newtral FactFlow, Cyabra, Blackbird.AI, Botometer), matriz comparativa de once variables, análisis de océano azul con el nicho no ocupado, matriz ERIC de diez atributos, y tabla de ventajas y brechas frente a cada competidor.

Del lado de negocio: Business Model Canvas completo, cinco segmentos de clientes organizacionales, FODA, Cruz de Porter, modelo de *pricing* por producto y análisis del activo de datos.

### Qué falta o necesita validación

Esto es lo que más atención necesita antes de volcarse, porque **el material de competencia y negocio es de abril y no se actualizó con las decisiones de agosto**. Hay cuatro contradicciones que un evaluador que lea el documento entero va a encontrar:

1. **La cobertura de WhatsApp.** `modelo-de-negocio.md` afirma que el sistema cubre WhatsApp «si el usuario abre un link en el navegador» y que el sensor cubre «cualquier sitio donde el usuario navegue». **Contradice el alcance del capítulo 1**, que declara Twitter/X como única plataforma de detección, y contradice RNF-08. Es la contradicción más grave de las cuatro, porque está en la parte del argumento que sostiene el modelo de negocio.
2. **El dataset de entrenamiento en la matriz comparativa** dice «LIAR, FakeNewsNet + Chequeado». Chequeado salió del alcance en agosto —responde 403 y RNF-17 prohíbe eludir bloqueos— y el modelo elegido es XLM-T.
3. **La matriz ERIC dice «reducir a español rioplatense»** como si el modelo fuera monolingüe. XLM-T es multilingüe; lo que se reduce es el dominio de datos, no la capacidad del modelo.
4. **Chequeado figura como socio clave del BMC** mientras el apartado legal explica que se lo excluye del acceso automatizado. Las dos cosas pueden convivir —un socio comercial no es una fuente de la que se extraen datos— pero hay que escribirlo, porque leído en crudo parece incoherente.

Además, dos cosas de encuadre:

- **La matriz comparativa de competidores ya está en el capítulo 2** (`tab:competidores`, sección *Soluciones comerciales y de mercado*). El capítulo 3 **no debe repetirla**: la referencia y aporta lo que el capítulo 2 no tiene, que son las herramientas de marketing.
- **La rúbrica nombra cuatro herramientas** (triple P, FODA, Cruz de Porter, Matriz Boston Consulting) y tenemos FODA, Porter, ERIC y océano azul. ERIC y océano azul no están en la lista de la rúbrica aunque son herramientas legítimas de estrategia. Conviene sumar una de las nombradas.

### Cómo se vuelca

Sección `\section{Análisis de Competencia}` de `chapter03.tex`, con subsecciones para el panorama de soluciones (breve, remitiendo al capítulo 2), océano azul, matriz ERIC y FODA; y `\section{Modelo de Negocio}` con el BMC, los segmentos, la Cruz de Porter y el *pricing*.

**Descomentar `chapter03` en `main.tex` arrastra la sección de User Research**, que hoy son tres `Completar.`. Ver la decisión 2 más abajo.

**Extensión estimada:** 6 a 8 páginas, de las cuales 4 son tablas.

---

## Criterio 5 — Tecnologías y arquitectura de red *(ya volcado)*

**Estado: en el documento desde el 11/08**, `chapter04.tex` líneas 111-186.

Contiene la tabla de componentes por capa con versiones fijadas y verificadas contra el registro de paquetes el 10/08, ocho decisiones con su alternativa descartada, y la arquitectura de red completa: cinco zonas con su grado de control, TLS 1.3 en todo cruce, red privada sin puerto público para API, ingesta y base, y la autenticación por frontera.

**Lo que hay que revisar antes de la entrega:** las versiones se verificaron el 10/08 y el documento las presenta como vigentes. Si alguna cambió, o se actualiza o se agrega la fecha de verificación al pie de la tabla. Es lo que un evaluador técnico puede comprobar en un minuto.

---

## Criterio 6 — Modelo de datos *(ya volcado)*

**Estado: en el documento desde el 11/08**, `chapter04.tex` líneas 16-110, con el DER como figura apaisada.

Diecisiete entidades en cinco dominios, con atributos, tipos, cardinalidades y la matriz de trazabilidad entidad → requerimiento funcional, que es lo que hace verificable la regla de corte: toda entidad se traza hasta un requerimiento.

La revisión del 11/08 ya corrigió el error de conteo de relaciones que estaba impreso. **No queda trabajo pendiente sobre este criterio**, más allá de que la sección de requerimientos, cuando se escriba, quede antes que esta para que las referencias a RF-xx aparezcan después de su definición y no antes.

---

## Orden de ejecución propuesto

El orden importa porque la sección de requerimientos define los RF-xx que las otras tres secciones referencian.

| # | Trabajo | Dónde | Estimación |
|---|---|---|---|
| 1 | Corregir las cuatro contradicciones del material de competencia y negocio | wiki | 1 h |
| 2 | Requerimientos y casos de uso | `chapter04.tex` | media jornada |
| 3 | Mockups | `chapter04.tex` | 2 h |
| 4 | Arquitectura y diagramas | `chapter04.tex` | media jornada |
| 5 | Competencia, marketing y modelo de negocio | `chapter03.tex` | 3 h |
| 6 | Cerrar las cuatro secciones `Completar.` restantes del capítulo 4 | `chapter04.tex` | 2 h |

El punto 6 son *Metodología* (de [[wiki/proyecto/metodologia]]), *Datasets* (de [[wiki/datasets/comparacion-datasets]]), *Arquitectura del sistema* —que la absorbe el punto 4— y *Validación del sistema* (de [[wiki/solucion/pruebas]], que hoy tiene 35 líneas y es la más floja de las cuatro).

---

## Decisiones que necesito antes de empezar

1. **Casos de uso: ¿los siete completos, o dos completos y cinco abreviados?** Los siete con todos sus flujos alternativos son unas 5 páginas de las 9-11 de la sección. Recomiendo CU-01 y CU-02 completos —son los que tienen los flujos interesantes— y CU-03 a CU-07 con flujo principal y solo los alternativos que aportan una decisión.
2. **`chapter03` y el User Research.** Descomentarlo para el criterio 4 deja tres `Completar.` visibles hasta que haya campo. ¿Se escribe la sección de user research el 20/08 con lo que haya, o se reordena el capítulo para que la ausencia no quede como un hueco?
3. **La herramienta de marketing que falta.** Recomiendo sumar el mix de marketing (4P), que se escribe en media hora y está en la lista de la rúbrica. La Matriz Boston Consulting no aplica bien: exige una cartera de productos y acá hay uno solo.
4. **RNF-05, el F1 macro de 0,80.** ¿Se sostiene como objetivo declarado, o se baja? Es el único número del documento que compromete un resultado experimental que todavía no se corrió.
5. **Las contradicciones 1 a 4 del criterio 4.** La de WhatsApp es la que hay que resolver sí o sí: o se saca del argumento, o se reformula como línea futura fuera del alcance del prototipo. Las otras tres son correcciones mecánicas si estás de acuerdo.
6. **Volumen del capítulo 4.** ¿Van las trece figuras al cuerpo, o alguna al anexo? Mi recomendación es todas al cuerpo.

---

## Referencias cruzadas

- [[wiki/proyecto/entrega-50-alcance]]
- [[wiki/proyecto/plan-entrega-50]]
- [[wiki/proyecto/plan-bloque-diseno]]
- [[wiki/solucion/requerimientos]]
- [[wiki/solucion/mockups]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/modelo-datos]]
- [[wiki/solucion/tecnologias]]
- [[wiki/competencia/analisis-competitivo]]
- [[wiki/negocio/modelo-de-negocio]]
