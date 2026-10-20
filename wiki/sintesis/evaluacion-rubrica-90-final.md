---
titulo: Revaluación del documento contra la rúbrica del 90 %
tipo: análisis
tags: [rubrica, entrega-90, evaluacion, documento]
fuentes: [raw/clases/Rubrica-PFI-2026-v1.3.xlsx, documento/main.pdf, handoff-pfi-evaluacion-rubrica-90.md]
actualizado: 2026-10-20
---

# Revaluación del documento contra la rúbrica del 90 %

Issue #90. Se recompiló `documento/main.pdf` desde cero (rama `feat/rubrica-90`) y se evaluó contra `Rubrica-PFI-2026-v1.3.xlsx` con la misma metodología del diagnóstico de partida: solapa por solapa, veredicto por ítem, observación con página y puntaje con el peso propio de cada ítem. Las páginas citadas son las del pie («Página X de 206»); en el visor del PDF son X + 2.

## Compilación

- 208 páginas de PDF, sin errores, sin referencias ni citas indefinidas; `biber` sin *warnings*.
- Dos `Overfull \hbox` de más de 10 pt corregidos: Tabla 4.II de herramientas (33,7 pt; primera columna pasa a `p{4.3cm}`) y mapa de navegación de la extensión (15,2 pt; separación horizontal de nodos 1,3 → 0,9 cm). Queda uno de 4,9 pt.
- No quedan `\Martin{}` ni `\Fidel{}`. «Completar.» solo aparece en `acknowledgments.tex`, que no se incluye.
- Checklist de entrega: `hidelinks` activo, cronograma comentado en el anexo, portada con `\the\year`.

## Pesos y cálculo

| Solapa | Peso por ítem | Ítems que suman | No suma |
|---|---|---|---|
| Calidad Técnica | 6,25 | 4 | Datasets |
| Formalidades | 2,5 | 7 | Hilo conductor |
| Funcional | 2,5 | 6 | — |
| Investigación | 30/7 ≈ 4,286 | 7 | Dominio conceptual |
| Negocio | 3,333 | 3 | — |

CUMPLE = 100 %, CUMPLE PARCIALMENTE = 30 %, NO CUMPLE = 0. Total = suma / 0,975. El Excel tiene fórmulas con errores (Investigación F7/F8 toman F4 y F10 toma F6; Formalidades I7–I9 toman I6; Funcional F5 tiene 2,5 fijo; Carátula B108 da `#REF!`), así que el puntaje se calcula con el peso propio de cada ítem.

## Veredictos por ítem

C = CUMPLE, P = CUMPLE PARCIALMENTE, NC = NO CUMPLE, (ns) = no suma.

### Calidad Técnica

| Ítem | Antes | Después | Observación |
|---|---|---|---|
| Modelo de datos y arquitectura | C | C | DER con PK/FK (p. 129), modelo C4 en tres niveles (pp. 107–112), despliegue (p. 136). |
| Justificación tecnológica | P | **C** | Python, FastAPI, SQLite, Railway, el LLM y TypeScript justificados contra alternativas (pp. 132–134); la Tabla 4.XI separa diseño y construido. |
| Tendencias | C | C | — |
| Producto entregado | P | P | Funciona de punta a punta, pero RNF-05 (F1 0,654 < 0,75) y RNF-02 (p95 14,9 s > 8 s) no se cumplen; la señal automática está apagada por defecto; el índice local, la ingesta programada, el historial de cuenta y RF-17 no están construidos. Las conclusiones lo reconocen (objetivo general «se cumple en parte», p. 162). |
| Datasets (ns) | P | C | Resultados del nivel 1 en la Tabla 4.XIX, 2.107 publicaciones de Chequeado (Tabla 4.IV, p. 149), fuga 87/108 declarada. |

### Formalidades

| Ítem | Antes | Después | Observación |
|---|---|---|---|
| Estructura | P | **C** | Alineada con el instructivo (#77/#78). Falta la sección de Agradecimientos (opcional; el archivo existe pero está comentado). |
| Formato | C | C | — |
| Índice | C | C | — |
| Voz impersonal | C | C | Sin primera persona fuera de las transcripciones. |
| Errores idiomáticos | P | P | Mejoró mucho con #79, pero quedan: el párrafo de 4.2.5.5 (pp. 116–117) mezcla cinco temas en un bloque; «Por esa razón» repetido en párrafos cercanos; p. 101 anuncia que «tres pantallas quedan fuera» y enseguida presenta la Figura 4.6. |
| Citas ISO 690 | P | **C** | #80 aplicado; `\parencite` en todo el texto. |
| Bibliografía | C | C | — |
| Hilo conductor (ns) | C | C | Problema → encuesta/entrevistas → requerimientos → arquitectura → resultados → conclusiones por objetivo. |

### Funcional

| Ítem | Antes | Después | Observación |
|---|---|---|---|
| Requerimientos | C | C | — |
| Diagramas | C | C | La Figura 4.14 muestra la secuencia tal como está construida. |
| UX | P | CUMPLE | (Revaluado tras c966a43.) Capturas reales de la señal de BETO en X y del formulario de CU-04 (Fig. 4.3), del detalle (4.4), del panel de tendencias por tema y del histórico de CU-05 (4.7), del aviso, de la ventana y mapa de navegación. Las maquetas que quedan (indicador y panel de evidencia) se rotulan como diseño y se contrastan con la versión construida. |
| Metodología | P | **C** | Kanban del desarrollo con correspondencia estado ↔ señal del repositorio, DoD, 20 *issues*, CI (p. 87 en adelante). |
| Pruebas | C | C | — |
| Resultados de pruebas | P | P | SUS 74,2 con n = 3, escala 1–10 convertida y sobre una versión previa a la señal automática y al aviso de primer uso; CP-6/7 ya se repitieron con la credencial del LLM el 2026-10-20 y quedan aprobados. La prueba del flujo automático pasa a «Aprobado»: la señal del texto se verificó el 2026-10-20 en una sesión real de X (edición del agente principal en paralelo). |

### Investigación

| Ítem | Antes | Después | Observación |
|---|---|---|---|
| Marco teórico | P | **C** | Agregados RAG, búsqueda vectorial, LLM, postura, *ensembles*, calibración y TF-IDF + LR. |
| Estado del arte | P | **C** | Tabla 2.VII con la propuesta; Notas de la Comunidad, Grok, NewsGuard. |
| Conclusión del EdA | P | **C** | Relevancia y aporte social explícitos (pp. 43–44). |
| User research | C | C | Encuesta n = 152 (116 en el segmento), entrevistas, personas; cifras consistentes en todo el documento. |
| Competencia | C | C | — |
| Legal | P | **C** | Sección 3.4: Ley 25.326 (arts. 7 y 12), aviso de uso de seis puntos, inscripción de la base, ToS de X, Chrome Web Store. |
| Conclusiones | C | C | Cierra los seis objetivos por número. Riesgo: el objetivo 1 «se cumple», pero prometía exactitud, precisión, cobertura, F1 ponderado y matriz de confusión, y la Tabla 4.XIX solo informa F1 macro y AUC. |
| Dominio conceptual (ns) | C | C | Observación: «ex falso quodlibet» está mal aplicado en p. 163. |

### Negocio

| Ítem | Antes | Después | Observación |
|---|---|---|---|
| Modelo de negocio | P | **C** | Cuotas de API (5.000/40.000), CAC 741 y LTV, comparación de mercado (Tabla 3.V), TAM/SAM/SOM. La disposición a pagar no está validada con clientes, y el documento lo declara. |
| Análisis financiero | C | C | VAN neutral 63.935,76; TIR 72,55 %; *payback* 2,93/3,46 años; escenarios optimista (833.353,48) y pesimista (−94.161,07). |
| Branding | C | C | — |

## Puntaje

| Solapa | Antes | Después |
|---|---|---|
| Calidad Técnica (25) | 16,25 | 20,625 |
| Formalidades (17,5) | 12,25 | 15,75 |
| Funcional (15) | 9,75 | 11,5 |
| Investigación (30) | 18,0 | 30,0 |
| Negocio (10) | 7,667 | 10,0 |
| **Suma** | 63,92 | 87,875 |
| **Total (/0,975)** | **65,6** (61,6 con las fórmulas del Excel) | **90,1** |

Con UX en CUMPLE tras c966a43, el total sube a **91,9**.

## Consistencia verificada

F1 0,654 (IC 0,56–0,74), línea base 0,527, clasificador solo 0,540; p95 14,9 s (mediana 11,1; inicial 18,0); SUS 74,2; encuesta n = 152 / 116, 38 / 29 respuestas abiertas; VAN 63.936; seis objetivos cerrados por número. El Resumen y el Abstract son coherentes con las conclusiones; no mencionan que la señal automática está apagada por defecto (menor).

## Pendientes priorizados (no CUMPLE y riesgos)

1. **Resultados de pruebas (P).** Repetir el SUS con al menos cinco participantes en la escala original 1–5 sobre la versión actual (con señal automática y aviso de primer uso). (CP-1, CP-6 y CP-7 ya se repitieron y quedan aprobados.) Actualizar la tabla de casos y el 74,2.
2. **UX (CUMPLE tras c966a43).** Se agregaron capturas de la señal, de CU-04, del panel construido y del histórico web. Mejora opcional: reemplazar las maquetas del indicador (4.2) y del panel de evidencia (4.5) por capturas.
3. **Producto entregado (P).** Lo que más pesa (6,25 pts). No se resuelve con texto: requiere bajar el p95 por debajo de 8 s (p. ej., paralelizar las dos llamadas al LLM o hacer *streaming* del veredicto) o reformular RNF-02/RNF-05 como metas no alcanzadas con su análisis. Construir RF-17 o sacarlo del alcance de forma explícita en la Tabla 4.XI.
4. **Errores idiomáticos (P).** Partir el párrafo de 4.2.5.5 (pp. 116–117) en uno por tema; variar «Por esa razón»; reescribir la frase de p. 101 sobre las «tres pantallas que quedan fuera» para que no contradiga la Figura 4.6.
5. **Riesgo en Conclusiones / objetivo 1.** Agregar a la Tabla 4.XIX la exactitud, la precisión, la cobertura, el F1 ponderado y la matriz de confusión del clasificador, o ajustar el enunciado del objetivo 1 a las métricas que se informan.
6. **Riesgo menor.** Corregir el uso de «ex falso quodlibet» (p. 163); mencionar en el Resumen que la señal automática queda apagada por defecto; agregar a la Tabla 4.III el mapeo de etiquetas de las 2.107 publicaciones de Chequeado; decidir si se incluyen los Agradecimientos.

## Errores chicos corregidos en esta pasada

- **Cap. 4, 4.2.1.5 (p. 90):** decía que las tres fuentes se almacenan en un índice de 768 dimensiones «según se detalla en 4.2.6», que dice que el prototipo no tiene vectores. Ahora remite al diseño lógico y aclara que el prototipo usa búsqueda web restringida (4.2.5.5).
- **Cap. 1 (p. 12):** afirmaba que los análisis se hacen «localmente en el navegador» sin persistencia. Ahora dice que se hacen mediante la API del servicio, con un identificador anónimo por instalación.
- **Cap. 3, 3.1.2 (p. 48):** «el guion se elaboró después de cerrar el campo de la encuesta» → «sobre los resultados de una primera versión de la encuesta».
- **Anexo B:** nota aclarando que las cifras que cita el entrevistador (4,06; 3,57; 84,1 %) son de la versión 1 (140 respuestas) y que las definitivas (152) están en la Sección 3.1.1. La transcripción no se tocó.
- **Cap. 3 (p. 67):** «las tres llamadas que componen un análisis» → «las llamadas» (el prototipo hace dos llamadas al LLM, Fig. 4.14).
- **Cap. 3, 3.4.4 (p. 82):** la ingesta programada de 4.2.7 aparecía como construida; ahora dice que la prevé el diseño y que no está en el prototipo.
- **Cap. 4:** los dos `Overfull \hbox` de más de 10 pt (Tabla 4.II y mapa de navegación).

## Referencias cruzadas
- [[wiki/proyecto/entrega-90-alcance]]
- [[wiki/sintesis/decisiones-pendientes-2026-08]]

## Fuentes
- [[raw/clases/Rubrica-PFI-2026-v1.3.xlsx]]
- `documento/main.pdf` (compilado el 2026-10-20)
