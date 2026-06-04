---
titulo: Recomendaciones del Profesor — Marco Teórico, Estado del Arte, User Research
tipo: proyecto
tags: [metodologia, marco-teorico, estado-del-arte, user-research, guia]
actualizado: 2026-06-04
---

# Recomendaciones del Profesor

Guía extraída de la clase "Marco Teórico, Estado del Arte, User Research" (PFI Sábados 2026). Priorizar estas instrucciones al redactar el capítulo 2 (Antecedentes) y el capítulo 3 (Descripción).

---

## 1. Marco Teórico

### Qué es

El Marco Teórico reúne los **conceptos, teorías y modelos** que sustentan la investigación. Su propósito es contextualizar el problema dentro del conocimiento existente y proporcionar una base conceptual que oriente el análisis.

> **Idea clave: no es una acumulación de definiciones, es una construcción argumentativa.**

Responde a la pregunta: *¿con qué conceptos y teorías voy a trabajar?*

### Funciones

1. Define los conceptos centrales del proyecto.
2. Justifica las decisiones técnicas y metodológicas.
3. Establece relaciones entre variables o componentes.
4. Permite interpretar los resultados a la luz de teorías reconocidas.
5. Ayuda a evitar reinventar lo ya resuelto.

### Estructura sugerida (de general a específico)

1. Concepto principal del dominio del problema.
2. Tecnologías o enfoques asociados.
3. Modelos, arquitecturas o frameworks aplicables.
4. Métricas, normas o estándares relevantes.

Cada subtema debe responder a una pregunta concreta vinculada a los objetivos del proyecto.

### Tres preguntas para identificar subtemas

1. ¿Qué conceptos necesito definir para que un lector externo entienda el proyecto?
2. ¿Qué teorías o modelos sustentan las decisiones técnicas?
3. ¿Qué estándares o normas son relevantes para validar el resultado?

### Cómo construirlo

1. Búsqueda sistemática de fuentes confiables.
2. Lectura crítica y selección de las pertinentes.
3. Organización por subtemas, **no por autores**.
4. Redacción argumentada, con citas correctamente referenciadas.
5. Revisión final de coherencia con el problema y los objetivos.

### Errores frecuentes a evitar

1. Copiar definiciones sin integrarlas al argumento.
2. Acumular autores sin discutirlos.
3. Incluir conceptos que después no se usan en el proyecto.
4. Citar páginas web no académicas como fuente principal.
5. Confundir Marco Teórico con manual técnico.

---

## 2. Estado del Arte

### Qué es

El Estado del Arte es la sistematización de lo que se ha investigado, desarrollado y publicado sobre un problema específico hasta la fecha.

> **No describe conceptos generales — describe trabajos concretos: qué hicieron, cómo lo hicieron, qué resultados obtuvieron y qué quedó pendiente.**

Responde a la pregunta: *¿qué se hizo y qué se está haciendo sobre este problema?*

**Diferencia con el Marco Teórico:**
- Marco Teórico: habla de ideas. *¿qué dicen las teorías sobre X?*
- Estado del Arte: habla de proyectos, papers, productos y prototipos. *¿quién hizo qué con X y con qué resultado?*

### Por qué es indispensable

1. Evita duplicar soluciones ya existentes.
2. Identifica brechas reales que el proyecto puede llenar.
3. Sirve como referencia comparativa de los resultados propios.
4. Aporta justificación técnica al alcance definido.
5. Demuestra rigor y honestidad académica.

### Qué cubrir

Un Estado del Arte sólido incluye:
1. Soluciones comerciales o de mercado vigentes.
2. Trabajos académicos recientes (idealmente últimos 5 años).
3. Tecnologías o enfoques alternativos al elegido.
4. Limitaciones reportadas por otros autores.
5. Tendencias emergentes en el área.

### Cómo hacer la revisión sistemática

Adaptado de Kitchenham y Charters (2007) y Webster y Watson (2002):

1. **Definir preguntas** de investigación que guíen la búsqueda.
2. **Seleccionar fuentes**: IEEE Xplore, ACM, Springer, ScienceDirect, Semantic Scholar.
3. **Estrategia de búsqueda**: palabras clave en inglés y español, operadores booleanos (AND, OR, NOT), comillas para frases exactas, filtrar por año/tipo/idioma.
4. **Filtrado**: aplicar criterios de inclusión y exclusión.
5. **Extracción**: extraer datos de cada trabajo seleccionado.
6. **Síntesis**: sintetizar hallazgos y vacíos detectados.

### Conclusiones del Estado del Arte

Las conclusiones deben responder:
1. ¿Qué se sabe sobre el problema?
2. ¿Qué soluciones existen y qué limitaciones tienen?
3. ¿Qué brecha justifica el proyecto propio?

### Matriz de antecedentes (opcional pero recomendada)

Herramienta para sistematizar los trabajos relevados. Columnas sugeridas:

| Columna | Pregunta guía |
|---|---|
| Autor y año, Título | ¿Quién lo publicó y cuándo? ¿En qué revista/conferencia? |
| Objetivo del trabajo | ¿Qué problema buscaron resolver? ¿Qué se propusieron demostrar? |
| Enfoque o metodología | ¿Fue empírico, teórico, prototipo, revisión sistemática? ¿Qué muestra/dataset usaron? |
| Tecnologías utilizadas | ¿Qué stack, frameworks, modelos o algoritmos aplicaron? |
| Resultados principales | ¿Qué encontraron concretamente? ¿Qué métricas reportan? |
| Limitaciones reconocidas | ¿Qué reconocen los propios autores que no pudieron resolver? |
| Aporte para el proyecto propio | ¿Qué de este trabajo puedo reutilizar, adaptar o tomar como referencia? ¿En qué se diferencia mi proyecto? |

---

## 3. User Research

### Qué es

El User Research es el proceso sistemático de comprender a los usuarios, sus necesidades, comportamientos y contextos, mediante técnicas empíricas.

> **Aporta evidencia para tomar decisiones de diseño y desarrollo, en lugar de basarlas en supuestos.**

### Cuándo incluirlo

Es **obligatorio** para este PFI: el proyecto tiene usuarios finales identificables, resuelve una necesidad humana directa e implica decisiones de interfaz y experiencia.

### Técnicas a usar en este PFI

1. **Encuestas** — alcance amplio, datos cuantitativos.
2. **Entrevistas** — profundidad, datos cualitativos.
3. **User Persona** — síntesis arquetípica de usuarios.

### Encuestas

**Útiles para:** estimar frecuencia/magnitud, validar hipótesis con muestra amplia, detectar patrones generales.

**Diseño de una encuesta:**
1. Definir el objetivo específico.
2. Identificar variables a medir.
3. Redactar preguntas claras, neutrales y sin ambigüedad.
4. Combinar tipos: cerradas, escala Likert, abiertas acotadas.
5. Probar con un grupo piloto pequeño.
6. Ajustar y aplicar.

**Análisis:** visualización de distribuciones + cruces entre variables si la muestra lo permite.

### Entrevistas

**Útiles para:** motivaciones, percepciones y dolores; explorar temas poco conocidos; capturar el lenguaje real del usuario.

**Modalidad recomendada:** semiestructurada (guión con preguntas guía + libertad para repreguntar).

**Diseño de la guía:**
1. Empezar con preguntas de contexto, fáciles de responder.
2. Avanzar hacia preguntas específicas del problema.
3. Cerrar con preguntas abiertas de validación.
4. Evitar preguntas que sugieran la respuesta esperada.
5. Prever entre 6 y 10 preguntas guía para entrevistas de 30 a 45 minutos.

**En el documento:** la transcripción va en ANEXO. El cuerpo del capítulo tiene la síntesis en hallazgos accionables.

### User Persona

Una User Persona es la representación arquetípica de un usuario, construida a partir de evidencia recolectada en el User Research.

> **No es un usuario inventado — es una síntesis basada en datos.**

**Componentes de cada persona:**
1. Nombre ficticio y datos demográficos relevantes.
2. Contexto y rol respecto al producto o sistema.
3. Objetivos al usar el producto.
4. Frustraciones y obstáculos actuales.
5. Comportamientos y hábitos relevantes.
6. Cita representativa que sintetice su perspectiva.

**Cantidad recomendada:** 2 a 3 personas por proyecto.

---

## Criterios de calidad transversales

Toda la sección de Antecedentes y Descripción debe respetar:

| Criterio | Descripción |
|---|---|
| **Validez** | Se describe o mide lo que efectivamente importa para el problema. |
| **Confiabilidad** | El proceso es reproducible y consistente. |
| **Trazabilidad** | Cada afirmación se sostiene con una fuente o un dato. |
| **Coherencia** | Cada componente se vincula con los objetivos definidos. |

---

## Checklist antes de entregar Antecedentes + Descripción

- [ ] Los subtemas del Marco Teórico cubren todos los conceptos críticos del proyecto.
- [ ] El Estado del Arte incluye trabajos recientes y relevantes (últimos 5 años prioritariamente).
- [ ] Los instrumentos de User Research están alineados con los objetivos.
- [ ] Las fuentes están correctamente citadas siguiendo ISO 690-2010.
- [ ] Ningún concepto del Marco Teórico queda sin usar en el resto del documento.
- [ ] Las conclusiones del Estado del Arte identifican la brecha que justifica el proyecto.

## Referencias cruzadas

- [[wiki/proyecto/propuesta]]
- [[wiki/marco-teorico/enfoques-deteccion]]
- [[wiki/estado-del-arte/kwon-jang-2025-survey-fake-text]]
- [[wiki/investigacion/user-research]]
