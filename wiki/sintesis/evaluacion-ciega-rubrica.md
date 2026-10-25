---
titulo: Evaluación ciega del documento con la rúbrica v1.3
tipo: análisis
tags: [rubrica, evaluacion, documento, entrega-90]
fuentes: [evaluacion-rubrica-90-final.md]
actualizado: 2026-10-24
---

# Evaluación ciega del documento con la rúbrica v1.3

Cinco evaluadores sin contexto (`claude -p`, una solapa de la rúbrica cada uno, solo con acceso de lectura al PDF) calificaron `documento/main.pdf`. El puntaje se calcula como en [[evaluacion-rubrica-90-final]]: CUMPLE = 100 %, CUMPLE PARCIALMENTE = 30 %, NO CUMPLE = 0, con el peso propio de cada ítem, sobre 97,5.

## Resultado por ronda

| Solapa | Ronda 1 | Ronda 2 | Ronda 3 | Cambios |
|---|---|---|---|---|
| Calidad técnica | 20,6 | 20,6 | 20,6 | Producto entregado sigue en P en las tres rondas |
| Formalidades | 10,5 | 12,25 | 15,75 | R2: redacción impersonal pasa a C. R3: formato y citas pasan a C; idiomáticos sigue en P |
| Funcional | 13,25 | 13,25 | 13,25 | R2: UX pasa a C y resultados de las pruebas baja a P |
| Investigación | 30 | 30 | 27,0 | R3: marco teórico baja a P (frases valorativas, temas sin teoría) |
| Negocio | 10 | 10 | 10 | Todo C |
| **Total** | **84,4** | **86,1** | **86,6** | Aceptado con cambios de forma (70 a 99) |

La ronda 1 dio origen al plan de correcciones de la rama `fix/correcciones-evaluadores` (PR #106). La ronda 2 se corrió sobre el PDF con esas correcciones.

## Defectos de la ronda 2 y corrección aplicada

| Defecto | Corrección |
|---|---|
| Cap. 4, 4.2.5: la memoria «todavía no» desplegada y la ingesta «no se construyó», en contradicción con el resto del documento (lo marcaron tres evaluadores) | La oración se reemplazó por la descripción del índice local con su ingesta programada |
| Anexo E: claves `ConvencionConstituyente1994` y `Railway2026` sin resolver y ruta del script en la tabla de supuestos | Entrada nueva de la Constitución en `biblio.bib`, `RailwayPrecios2026` en el generador y ruta quitada. Planilla regenerada y validada, sin cambios en las cifras |
| Tabla 4.XXIII desbordada sobre el pie, con RNF-16 cortado y RNF-17 oculto | Pasó a `longtable` |
| Tabla 4.XXIII: costo «medido con dos llamadas» frente a una sola llamada en el resto del documento | «Como máximo 0,0044 dólares», igual que en 4.2.7 |
| Fig. 4.12 rotulada «Probabilidad de desinformación» | «Veredicto y puntaje de confianza con evidencia enlazada» |
| Sueldo convertido con el tipo implícito de Sysarmy y el resto con el del BCRA, sin explicación | Oración en 3.3.5 que justifica la excepción. No cambia ninguna cifra |
| Alícuota de ganancias con fuente «indicada por la cátedra» | Alícuota máxima de la escala de la Ley 27.630 (`CongresoNacion2021`) |
| Párrafo repetido sobre los *embeddings* estáticos en 2.1.2 | Se quitó la oración repetida |
| Tabla 2.III sin las obras de las que salen sus datos | Fuente con LIAR, FakeNewsNet, Fakeddit y el *Spanish Fake News Corpus* |
| Fig. 2.3 con las curvas de los competidores en gris indistinguible | Colores Okabe-Ito y marcadores rellenos |
| Síntesis 4.3.6 con cifras repetidas y una oración suelta | Reescrita en tres párrafos que remiten a las secciones de resultados |

## Defectos de la ronda 3 y corrección aplicada

| Defecto | Corrección |
|---|---|
| 4.2.5 remite a «Despliegue de los módulos» para la ingesta | Remite a la sección «Ingesta de fuentes oficiales» |
| Tabla 4.IX justifica la extensión vectorial con `pgvector` | La fila justifica `sqlite-vec` y deja `pgvector` como camino al migrar a PostgreSQL |
| Fig. 4.10 citada antes que la 4.9 | Se invirtió el orden de las dos figuras |
| CP1 afirma que la señal del texto queda registrada y cubre RF-16 | Se corrigió el resultado esperado y RF-16 queda cubierto por CP2 |
| CP5 aprobado sin seguir el paso 1 | El paso describe la apertura del panel con el identificador de la instalación |
| CP6 y CP7 aprobados «en la segunda ejecución» sin explicar la primera | Cada caso y la síntesis 4.3.6 explican que la primera ejecución no tenía la credencial del LLM |
| Marco teórico con frases que valoran o anticipan decisiones | Se quitaron (2.1.1, 2.1.2, Tabla 2.II y métricas) |
| Términos que se alternan | Un solo término por concepto: combinador, tasa de bajas, período de recuperación, informe, ajuste fino y ajustado, señal del texto, desplazamiento de dominio, conjunto de referencia, ordenamiento, desarrollador |
| Cap. 1 no avisa que la meta del objetivo 2 se reformuló | El objetivo se partió en oraciones cortas y remite a las conclusiones para la reformulación |

## Observaciones de criterio no aplicadas

Quedan como preguntas posibles en la defensa:
- RNF-15 se da por cumplido a título de indicio con tres participantes.
- No hubo cambios en la interfaz derivados de la prueba de usabilidad.
- El corpus de reserva se reutilizó después de adaptar el clasificador.
- Chequeado aparece como fuente en 78 de los 94 análisis.
- No hay una segunda anotación humana ni medida de acuerdo entre anotadores.
- No se justifica GossipCop dentro de FakeNewsNet.
- El marco teórico no trata la credibilidad de la fuente ni la detección de cuentas automatizadas, la seudonimización con HMAC y las extensiones de navegador (decisión del autor: no agregar subsecciones).

## Referencias cruzadas
- [[evaluacion-rubrica-90-final]]
- [[experimentos-overview]]
- [[analisis-financiero]]
