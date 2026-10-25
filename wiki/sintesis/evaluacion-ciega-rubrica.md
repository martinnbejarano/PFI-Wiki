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

| Solapa | Ronda 1 | Ronda 2 | Ronda 3 | Ronda 4 | Cambios |
|---|---|---|---|---|---|
| Calidad técnica | 20,6 | 20,6 | 20,6 | 20,6 | Producto entregado sigue en P en las tres rondas |
| Formalidades | 10,5 | 12,25 | 15,75 | 14,0 | R2: redacción impersonal pasa a C. R3: formato y citas pasan a C. R4: citas vuelve a P (marcos sin citar); idiomáticos y hilo siguen en P |
| Funcional | 13,25 | 13,25 | 13,25 | 11,5 | R2: UX pasa a C y resultados de las pruebas baja a P. R4: UX vuelve a P (Fig. 4.2) |
| Investigación | 30 | 30 | 27,0 | 30 | R3: marco teórico baja a P (frases valorativas, temas sin teoría) |
| Negocio | 10 | 10 | 10 | 10 | Todo C |
| **Total** | **84,4** | **86,1** | **86,6** | **86,1** | Aceptado con cambios de forma (70 a 99) |

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
| Términos que se alternan | Un solo término por concepto: combinador, tasa de bajas, período de recuperación, informe, señal del texto, desplazamiento de dominio, ordenamiento y desarrollador. Por decisión del autor se mantienen en inglés *fine-tuning*, *fine-tuned*, *benchmark* y *screening*, usados siempre igual |
| Cap. 1 no avisa que la meta del objetivo 2 se reformuló | El objetivo se partió en oraciones cortas y remite a las conclusiones para la reformulación |

## Defectos de la ronda 4 y corrección aplicada

| Defecto | Corrección |
|---|---|
| Cap. 2 dice que la veracidad no es binaria y las conclusiones que la verdad no admite grados | Cap. 2: un contenido puede combinar elementos verdaderos y falsos. Conclusiones: la verdad de una afirmación simple no admite grados |
| «Cuatro decisiones permanecen abiertas», con la expiración de la caché ya definida | Tres parámetros de operación, sin la caché |
| La partición de datos omite las 2.107 afirmaciones de Chequeado | Cinco conjuntos, con el de adaptación y su uso (segunda etapa, época y umbral) |
| El protocolo se presenta como fijado de antemano pese a cambios posteriores | 4.3.3 y conclusiones declaran las tres modificaciones con su cronología |
| Marcos sin citar | Aaker (personalidad de marca), WCAG 2.2, C4, MoSCoW, Scrum Guide (Scrum y definición de terminado), Kotler y Keller (FODA y mezcla de *marketing*), Henderson (matriz BCG), Skok (CAC y LTV) |
| «Trama» registrada en el INPI, sin respaldo | Solicitud en trámite en la clase 9 (acta 4671495), con cita a la consulta de marcas del INPI |
| LIAR «el benchmark más utilizado» y cita textual de Drchal sin página | Afirmación atenuada; la cita pasa a paráfrasis |
| «RF07» y «RF06» en la Tabla 4.VII | Corte de línea en el guion; se impide con `\mbox` |
| Cobertura del 52 % de la extensión anterior al flujo automático | Medida de nuevo: 70 % de las sentencias (24/10/2026) |
| Remisiones genéricas a la Sección 4.3 | Remiten a 4.3.4 (mediciones) y 4.3.3.3 (resultados del SFNC) |

Sin aplicar: la cita para TAM/SAM/SOM (no se encontró una fuente verificable) y el nombre del producto en el panel web («Detector de desinformación» frente a «Factum»), que requiere cambiar el código y volver a capturar las Figs. 4.7 y 4.8. La Fig. 4.2 queda pendiente por decisión del autor.

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
