---
titulo: Entrega del 90 % — alcance, estado y plan de acción
tipo: proyecto
tags: [entrega, e75, e90, rubrica, plan]
fuentes: [Pautas-E75-Monzon-2026.pdf, Rubrica-PFI-2026-v1.3.xlsx, Cronograma-PFI-Informatica-2026.pdf, GR_M15_Feresini_Imbriago-EntregaFinal2025.pdf]
actualizado: 2026-09-28
---

# Entrega del 90 % — alcance, estado y plan de acción

La cátedra la llama Entrega Preliminar 3 (75 %). **Para defender en diciembre, el avance tiene que ser del 90 %**, y ese es el camino elegido. En la práctica, se entrega el informe final: el evaluador externo lo corrige con la rúbrica del 100 %, y la fecha de defensa se fija después de su devolución.

## Fechas (cronograma oficial 2026)

| Hito | Fecha |
|---|---|
| **Entrega del documento al 90 %** | **sábado 24/10/2026, 23:59** |
| Exposición de avance (10 a 15 min, con demo) | 24/10, 31/10 o 7/11. La presentación se sube el día anterior |
| Feedback y consultas | 14/11 |
| Recuperatorio del 75 % / 90 % | 28/11 |
| Defensas, llamado regular | 9/12 al 14/12 |

La entrega la envía el tutor, así que la fecha real de corte es **antes del 24/10**, la que acuerde Fidel.

## Qué acompaña al documento

1. **Tres videos de 5 minutos** que explican la tesis.
2. Un **informe de avance**.
3. La **rúbrica del 75 % como autoevaluación**, que completa y avala el tutor.
4. Una **demo productiva**: el proyecto aplicado a un escenario real, y documentado.

## Qué exige el documento (novedades del 75 %)

- Marco normativo dentro del Marco Teórico.
- Metodología de desarrollo con su estructura oficial: *Metodología* / *Arquitectura y tecnologías utilizadas* / *Validación del sistema*. Se cierra al final.
- Los aspectos legales, si son extensos, van en una sección propia.
- Resumen, Abstract (traducción del Resumen) y capítulo de Conclusiones generales.
- Siguen vigentes todas las exigencias del 25 % y del 50 %, más la lista de formato y redacción de las pautas (unas 90 viñetas; ver la fuente).

## Estado frente a la rúbrica del 100 %

Leyenda: ✅ se cumple · 🟡 parcial · 🔴 falta.

| Solapa (pts) | Criterio | Estado | Qué falta |
|---|---|---|---|
| Calidad técnica (25) | Modelo de datos y arquitectura | ✅ | Pasar la arquitectura a calidad «nivel AWS» si no lo es |
| | Justificación tecnológica | ✅ | — |
| | Tendencias en informática | 🟡 | Hoy toda la inferencia es un LLM de terceros. La pauta dice que **no puede ser solo un *wrapper* de un LLM**: hace falta el clasificador propio entrenado |
| | Producto entregado | 🟡 | Los objetivos específicos prometen un módulo de credibilidad (pesa 0) y un clasificador propio. Implementarlos o recortar los objetivos |
| | Uso de datasets | 🟡 | Documentado, pero sin usar: se usa recién cuando haya entrenamiento. Declarar el corpus propio como fuente primaria |
| Formalidades (20) | Estructura | 🔴 | Reordenar el cap. 4 en tres secciones, sacar lo legal a una sección propia, agregar el marco normativo, Conclusiones, Resumen y Abstract |
| | Formato, índice, redacción, idioma | 🟡 | Pasada completa contra la lista de las pautas: *Title Case* en títulos, «no debe» en requerimientos, lenguaje de trabajo en progreso («Trabajo previsto», «Alcance diferido», «Decisiones diferidas»), menciones a entregas |
| | Citas y bibliografía | 🟡 | Las pautas prohíben citar páginas web y documentación de *vendors*; hay 14 entradas `@online` que revisar. Pasar los *preprints* de arXiv a su versión publicada |
| | Hilo conductor | ✅ | Revisar después de reestructurar |
| Desarrollo funcional (15) | Requerimientos, diagramas, mockups, metodología | ✅ | Diagramas UML con sintaxis estándar completa |
| | **Pruebas funcionales** | 🔴 | Hay 61 tests del servicio (cobertura 88 %) y 16 de la extensión (cobertura sin medir). **Faltan las pruebas con usuarios** (usabilidad) |
| | **Resultados de las pruebas** | 🔴 | No hay resultados ni decisiones tomadas a partir de ellos. La validación del sistema está escrita como protocolo, sin números |
| Investigación (30) | Marco teórico | 🟡 | Falta el marco normativo |
| | Estado del arte y conclusión | ✅ | La pauta pide la competencia *dentro* del Estado del Arte; hoy está en el cap. 3 (ver contradicción) |
| | **User research** | 🔴 | **Encuesta: 140 respuestas; el mínimo nuevo es 160.** **Entrevistas: 2; se esperan 5**, 3 como mínimo si se combina con encuesta. **Personas: 2; se piden 3**, y en formato gráfico |
| | Viabilidad legal | ✅ | Hay un análisis extenso; pasarlo a sección propia |
| | Viabilidad técnica | ✅ | No aplica (no hay hardware) |
| | Dominio conceptual | ✅ | — |
| | **Conclusiones generales** | 🔴 | El capítulo no existe (`conclusion.tex` tiene «Completar.») |
| Negocio (10) | Modelo de negocio | ✅ | — |
| | **Viabilidad económico-financiera** | 🔴 | `analisis-financiero.md` es una plantilla vacía. Se piden dos escenarios (optimista y pesimista) y VAN, TIR o *payback* |
| | **Branding y logotipo** | 🔴 | No hay nombre ni logo: la extensión se llama «Detector de desinformación — prototipo» |

Además, fuera de la rúbrica pero en las pautas:

- **Mitigación de *prompt injection*** (se le pasa el texto del tuit a un LLM): no está documentada.
- **Proceso de entrenamiento documentado** (variables y métricas), si se usa ML.
- **Escenario real:** hoy el servicio corre en local. Hay que desplegarlo y publicar la extensión, aunque sea sin listar.

> ⚠️ CONTRADICCION: las pautas del 75 % dicen «Competencia dentro del Estado del Arte», pero el template y el mapa de `CLAUDE.md` ponen el análisis competitivo en el cap. 3 (Descripción), y así se aprobó el 50 %. Consultar a Fidel antes de mover algo.

## Riesgos

1. **El clasificador propio es la ruta crítica.** Sin él, el producto es un *wrapper* de un LLM (criterio eliminatorio de las pautas), la validación no tiene números y las conclusiones no tienen de qué concluir. Salida mínima viable: *fine-tuning* de XLM-T o BETO sobre FakeDeS, que ya está en español y etiquetado, con la línea base TF-IDF + regresión logística. Es trabajo de días en Colab, no de semanas. El corpus argentino anotado a mano (300 a 500 casos) va solo como test real, y si no llega se recorta.
2. **El trabajo de campo depende de terceros**: 20 respuestas más a la encuesta, 3 entrevistas y usuarios para la prueba de usabilidad. Hay que arrancarlo esta semana.
3. **El tutor envía la entrega**: su fecha de corte y la autoevaluación restan días al plan.

## Plan de acción (28/09 → 24/10)

### Semana 1 · 28/09 a 04/10 — arrancar lo que depende de otros

- [ ] Preguntar a Fidel su fecha de corte, cómo quiere la autoevaluación y lo de la competencia dentro del Estado del Arte.
- [ ] Reabrir la encuesta hasta pasar las 160 respuestas.
- [ ] Coordinar 3 entrevistas nuevas. Prioridad: una organización de verificación (pendiente desde el 50 %), un usuario del segmento y alguien de un medio socio de ADEPA.
- [ ] Clasificador: preparar FakeDeS, entrenar la línea base TF-IDF + LR y lanzar el primer *fine-tuning*.
- [ ] Nombre del producto y logo (hay clase de modelo de negocio el 03/10).

### Semana 2 · 05/10 a 11/10 — cerrar el producto

- [ ] Integrar el clasificador al servicio en reemplazo del puntaje del LLM, con métricas contra la línea base.
- [ ] Decidir el módulo 2 (credibilidad): implementar las señales públicas mínimas o recortarlo de los objetivos.
- [ ] Mitigación de *prompt injection*, implementada y documentada.
- [ ] Desplegar el servicio y publicar la extensión (escenario real).
- [ ] Análisis financiero: supuestos, costos, dos escenarios, VAN, TIR y *payback*.

### Semana 3 · 12/10 a 18/10 — validar y escribir

- [ ] Prueba de usabilidad con 5 a 8 usuarios (tareas + cuestionario SUS) y registro de los resultados.
- [ ] Validación del sistema con números: métricas del clasificador y del sistema completo sobre el test real.
- [ ] Reestructurar el documento: el cap. 4 en tres secciones, lo legal en sección propia y el marco normativo en el Marco Teórico.
- [ ] Volcar las entrevistas nuevas (un anexo por entrevista), la tercera persona y la encuesta actualizada.
- [ ] Conclusiones generales atadas a cada objetivo específico, y después Resumen y Abstract.

### Semana 4 · 19/10 a 24/10 — pulir y entregar

- [ ] Pasada de formato y redacción contra la lista completa de las pautas.
- [ ] Bibliografía: sacar las citas web y de *vendors*, pasar los *preprints* a su versión publicada y cargar las claves del trabajo futuro (FActScore, ProgramFC y ClaimDecomp).
- [ ] Grabar los 3 videos de 5 minutos.
- [ ] Informe de avance y autoevaluación con la rúbrica.
- [ ] Deck y guion de 10 a 15 minutos con demo, aplicando lo pendiente del feedback del 50 %.
- [ ] Compilar, checklist de entrega y enviar al tutor.

## Plan detallado — puntos 1, 4 y 5

Contiene solo lo que falta. Las decisiones abiertas de cada punto se resuelven en otra sesión, antes de ejecutarlo.

### 1. Clasificador propio

Lo que ya está decidido y escrito en el cap. 4:
- **Modelo:** comparación de cinco —TF-IDF + regresión logística (línea base), XLM-T con y sin la etapa en inglés, RoBERTuito, BETO y un LLM *zero-shot*—; se sirve el mejor por F1 macro en la validación de FakeDeS, en un Hugging Face Space en CPU. El LLM queda para extraer la afirmación, recuperar evidencia y redactar la justificación.
- **Datos (actualizado 2026-09-28, spec #28):** dos clases (verdadero y falso); LIAR + FakeNewsNet (unos 36 000 ejemplos, solo en la variante de XLM-T con etapa en inglés), FakeDeS (971, entrenamiento común) y un corpus argentino **solo de prueba** (114 tuits, 44/56; el objetivo era 200 a 300), declarado fuente de datos primaria. Se eliminó el 3a.
- **Meta (RNF-05):** F1 macro de 0,80 y 10 puntos por encima de la línea base.
- **Integración:** en el combinador, el clasificador pesa 0,35 del puntaje final.

Lo que falta:

1. **Preparar los datos**
   - [ ] Descargar LIAR, FakeNewsNet y FakeDeS, y mapear sus etiquetas según la Tabla `tab:mapeo-etiquetas`.
   - [ ] Preprocesar como indica `pipeline-preprocesamiento.md`: conservar números y emojis, y normalizar URLs y menciones.
   - [ ] Partir en entrenamiento, validación y prueba, estratificado, y congelar las particiones con una semilla fija.
2. **Entrenar la línea base**
   - [ ] TF-IDF + regresión logística sobre FakeDeS y sobre el conjunto completo, y registrar F1 macro, precisión y exhaustividad por clase.
3. ***Fine-tuning***
   - [ ] XLM-T en dos etapas: primero el nivel 1 (inglés) y después el nivel 2 (FakeDeS).
   - [ ] Registrar hiperparámetros, curvas y métricas por época (las pautas piden documentar variables y métricas del entrenamiento).
   - [ ] Repetir con RoBERTuito (con su propio preprocesamiento) y con BETO, solo sobre el nivel 2.
   - [ ] Correr el LLM *zero-shot* sobre la misma partición de prueba.
4. **Corpus argentino**
   - [ ] Armar la planilla de candidatos desde notas de Chequeado (falsos y «Verdadero») y tuits que citan datos del INDEC o del BCRA.
   - [ ] Confirmar cada fila (único anotador, el autor; sin segundo anotador ni kappa).
5. **Integrar al servicio**
   - [ ] Exportar el modelo y agregar un adaptador en el puerto del proveedor, para que el puntaje del módulo 1 salga del modelo propio y no del LLM.
   - [ ] Medir la latencia contra RNF-02.
   - [ ] Agregar los tests que sean necesarios.
6. **Volcar al documento**
   - [ ] Reescribir la validación del sistema con los números.
   - [ ] Tabla comparativa de los cinco modelos, matriz de confusión y análisis de errores.
   - [x] Declarar el corpus propio como fuente de datos primaria (cap. 4, 2026-09-28).

**Decisiones abiertas:**
Resueltas el 2026-09-28 (spec #28): se entrena en Colab; se sirve en un Hugging Face Space en CPU; dos clases, y «sin verificar» pasa a ser `SIN_CONTRASTE_EXTERNO` del sistema; el 3a se elimina y el conjunto de prueba queda en 200 a 300; no hay segundo anotador; la comparación entra completa (cinco modelos). RNF-05 no se modifica: si no se llega a 0,80 se avisa y se decide en ese momento.

### 4. Documento incompleto

1. **Marco normativo, dentro del Marco Teórico (cap. 2)**
   - [ ] Una subsección que presente las normas sin analizarlas: Ley 25.326 de protección de datos personales, Ley 11.723 de propiedad intelectual, delitos contra el honor del Código Penal, términos de servicio de X y políticas de Chrome Web Store.
   - [ ] Cargar cada ley en `biblio.bib` como norma, no como página web.
2. **Aspectos legales como sección propia**
   - [ ] Sacar «Restricciones legales del diseño» del cap. 4 y convertirla en sección propia. La ubicación está a definir.
   - [ ] Revisar las referencias cruzadas a `sec:legal`.
3. **Reestructurar el cap. 4** en las tres secciones oficiales:
   - *Metodología*: metodología de trabajo y herramientas.
   - *Arquitectura y tecnologías utilizadas*: requerimientos, casos de uso, interfaz, arquitectura, modelo de datos, tecnologías, estrategia de datos y entrenamiento.
   - *Validación del sistema*: tests automatizados con cobertura, métricas del clasificador, prueba de usabilidad y resultados, con las decisiones que se tomaron a partir de ellos.
   - [ ] Eliminar el lenguaje de trabajo en progreso: «Trabajo previsto», «Alcance diferido», «Decisiones diferidas», la columna «Entrega» de las tablas y toda mención a entregas.
   - [ ] Revisar que no queden niveles con un solo hijo ni títulos pegados sin texto.
4. **Conclusiones generales** (`conclusion.tex`, descomentarlo en `main.tex`)
   - [ ] Un párrafo por objetivo específico: qué se cumplió y con qué evidencia (métricas, prueba de usabilidad, encuesta).
   - [ ] Limitaciones: *ex falso*, una afirmación por tuit, fuente oficial errónea y sesgo de la muestra.
   - [ ] Trabajo futuro: los tres engaños de la lámina 10, citando FActScore, ClaimDecomp y ProgramFC.
5. **Resumen y Abstract** (se escriben al final)
   - [ ] Resumen de 250 a 300 palabras con palabras clave: problema, propuesta, método, resultados y conclusión.
   - [ ] Abstract como traducción fiel del Resumen.
   - [ ] Descomentarlos en `main.tex`.
6. **Pasada de formato y redacción** contra la lista de las pautas, en `raw/clases/Pautas-E75-Monzon-2026.pdf`
   - [ ] Títulos en mayúscula de oración («Marco teórico», «Modelo de negocio»).
   - [ ] Requerimientos redactados siempre como «El sistema debe…».
   - [ ] Revisar las 14 entradas `@online`: sacar vendors y noticias, y pasar los *preprints* de arXiv a su versión publicada.
   - [ ] Unificar términos (IA/AI, *backend*, *frontend*).
   - [ ] Captions de tablas arriba, fuente en cada caption, sin *overfull hbox*, sin «Completar.».
   - [ ] Pasar el checklist de entrega de `CLAUDE.md`.

**Decisiones abiertas:**
- Dónde va la sección legal: dentro del cap. 4 como sección hermana o como capítulo aparte.
- Si la competencia se mueve al Estado del Arte (consultar a Fidel).
- Cuánto del cap. 4 actual pasa a anexos: casos de uso completos o tablas de requerimientos largas.
- Si «Descripción» (cap. 3) queda como está.

### 5. Negocio

1. **Análisis económico-financiero** (`analisis-financiero.md` está vacío; el cap. 3 no tiene sección)
   - [ ] **Supuestos:** horizonte de 3 años, moneda en USD, tasa de descuento, instalaciones de la extensión y conversión a clientes pagos por segmento, a partir de los cinco segmentos y la estructura de precios del cap. 3 (200 USD por mes a un medio chico y 2 500 a un cliente *enterprise*).
   - [ ] **Inversión inicial y costos:** desarrollo (horas por tarifa), infraestructura (14 USD por mes al principio, escalando con el volumen), llamadas al LLM por análisis, *hosting* del modelo, dominio, Chrome Web Store, marketing y costos legales.
   - [ ] **Ingresos:** suscripciones de reportes más API por volumen, mes a mes.
   - [ ] **Dos escenarios, optimista y pesimista** (y uno base si suma), que varíen adopción, conversión y *churn*.
   - [ ] **Indicadores:** flujo de fondos, VAN, TIR, *payback* y punto de equilibrio en clientes.
   - [ ] Una planilla como fuente de los números y tablas en LaTeX, sin captura de Excel.
   - [ ] Volcar como sección del cap. 3, después del modelo de negocio, y citar el método desde un libro.
2. **Branding y logotipo**
   - [ ] **Nombre del producto:** que no sea «Detector de desinformación — prototipo». Verificar que no esté tomado en Chrome Web Store ni como marca en el INPI.
   - [ ] **Logo:** versión color, monocromo y ícono de la extensión en 16, 48 y 128 px, coherente con el *badge* (verde, ámbar y rojo).
   - [ ] **Identidad mínima:** paleta, tipografía, tono de voz (neutral, sin tomar partido) y *tagline*.
   - [ ] Una subsección en el cap. 3 que explique el porqué del nombre, del logo y de los colores. La rúbrica pide explicar las razones y usar otros conceptos de *branding*.
   - [ ] Aplicar el nombre y el logo a la extensión, el deck, los videos y la carátula.
3. **Clase del 03/10** (modelo de negocio y herramientas de apoyo visual): llevar el borrador de nombre, logo y supuestos, y ajustar con lo que digan.

**Decisiones abiertas:**
- Nombre y concepto del logo.
- Tasa de descuento y horizonte.
- Si el costo de desarrollo incluye las horas propias.
- Cuántos clientes por segmento suponer en cada escenario, y de dónde se justifica.
- Si el ciudadano gratuito tiene algún costo variable que haya que modelar (llamadas al LLM por tuit analizado).

## Referencias cruzadas

- [[wiki/proyecto/cronograma]]
- [[wiki/proyecto/entrega-50-alcance]]
- [[wiki/proyecto/calibracion-tesis-referencia]]
- [[wiki/presentacion/e50/analisis-feedback]]
- [[wiki/negocio/analisis-financiero]]
- [[wiki/solucion/pruebas]]

## Fuentes

- [[raw/clases/Pautas-E75-Monzon-2026.pdf]]
- [[raw/clases/Rubrica-PFI-2026-v1.3.xlsx]]
- [[raw/clases/Cronograma-PFI-Informatica-2026.pdf]]
