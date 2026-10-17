---
titulo: Entrega del 90 % — alcance, estado y plan de acción
tipo: proyecto
tags: [entrega, e75, e90, rubrica, plan]
fuentes: [Pautas-E75-Monzon-2026.pdf, Rubrica-PFI-2026-v1.3.xlsx, Cronograma-PFI-Informatica-2026.pdf, GR_M15_Feresini_Imbriago-EntregaFinal2025.pdf]
actualizado: 2026-10-17
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

## Estado frente a la rúbrica del 100 % (al 2026-10-17)

Leyenda: ✅ se cumple · 🟡 parcial · 🔴 falta.

| Solapa (pts) | Criterio | Estado | Detalle |
|---|---|---|---|
| Calidad técnica (25) | Modelo de datos y arquitectura | ✅ | — |
| | Justificación tecnológica | ✅ | — |
| | Tendencias en informática | ✅ | El Módulo 1 es BETO propio, ajustado en dos etapas (FakeDeS + 2107 afirmaciones de Chequeado) y servido en local con `make dev`. El LLM extrae, busca y redacta, pero no decide el veredicto |
| | Producto entregado | 🟡 | Los 4 módulos andan. Falta la clasificación automática de tuits nuevos: un tuit ya analizado muestra el veredicto sin clic; uno nuevo necesita el clic. Declarado en `sec:alcance-implementado` |
| | Uso de datasets | ✅ | FakeDeS, LIAR, FakeNewsNet, Chequeado y el corpus argentino de 108 tuits como prueba real |
| Formalidades (20) | Estructura | ✅ | Cap. 4 en *Metodología* / *Arquitectura y tecnologías utilizadas* / *Validación del sistema*; marco normativo en el cap. 2; viabilidad legal como sección propia; Resumen, Abstract y Conclusión escritos |
| | Formato, índice, redacción, idioma | ✅ | Pasada del 2026-10-17: 0 errores, 0 referencias indefinidas, 0 *overfull hbox*, 0 frases prohibidas, toda sección abre con recorrido. Solo queda «Completar.» en Agradecimientos |
| | Citas y bibliografía | ✅ | biber sin advertencias. Los dos *preprints* de arXiv (WangEtAl2024survey, HasanEtAl2025) no tienen versión publicada al 2026-10-17 |
| | Hilo conductor | ✅ | — |
| Desarrollo funcional (15) | Requerimientos, diagramas, mockups, metodología | ✅ | — |
| | Pruebas funcionales | ✅ | 7 casos de prueba ejecutados (3 con observaciones, 2 tras corrección); 111 pruebas del servicio (93 %) y 18 de la extensión |
| | Resultados de las pruebas | ✅ | F1 del sistema 0,654 (RNF-05 no se cumple); SUS 74,2 con 3 participantes; RNF-02 a 04 y 12 a 15 medidos (ver [[wiki/experimentos/mediciones-rnf]]) |
| Investigación (30) | Marco teórico | ✅ | Incluye el marco normativo |
| | Estado del arte y conclusión | ✅ | Competencia como sección hermana del EdA en el cap. 2 |
| | User research | 🟡 | Se deja así por decisión del 2026-10-17: encuesta 140 (piden 160), 2 entrevistas (3 a 5), 2 personas (3) |
| | Viabilidad legal | ✅ | — |
| | Viabilidad técnica | ✅ | No aplica |
| | Dominio conceptual | ✅ | — |
| | Conclusiones generales | ✅ | Por objetivo, con los datos medidos y sin marcas pendientes |
| Negocio (10) | Modelo de negocio | ✅ | — |
| | Viabilidad económico-financiera | ✅ | Dos escenarios con VAN y TIR |
| | Branding y logotipo | ✅ | Factum |

Fuera de la rúbrica, en las pautas:

- **Mitigación de *prompt injection*:** ✅ documentada en el cap. 4, con la instrucción en el paso de extracción y tres intentos en vivo que no lograron nada (ver `prototipo/mediciones/inyeccion.py`).
- **Proceso de entrenamiento documentado:** ✅
- **Escenario real:** 🟡 el servicio y BETO corren en local; la extensión se carga sin empaquetar. HTTPS de RNF-12 queda sin verificar por eso.

## Lo que falta (al 2026-10-17)

- [ ] Preguntar a Fidel su fecha de corte (él envía la entrega) y cómo quiere la autoevaluación.
- [ ] Agradecimientos (los escribe el autor).
- [ ] Informe de avance y autoevaluación con la rúbrica.
- [ ] Deck y guion de 10 a 15 minutos con demo.
- [ ] Checklist de entrega de `CLAUDE.md`: enlaces en negro (`hidelinks`), sacar el cronograma del anexo, `\today` en la portada.
- [ ] Grabar los 3 videos de 5 minutos (al final).

El plan semanal del 28/09 quedó superado y se reemplaza por esta lista.

## Plan detallado

Los planes detallados del clasificador, el documento y el Módulo 2 quedaron cumplidos o superados entre el 28/09 y el 17/10; el detalle está en `log.md` y en el historial de git. El Resumen sigue el formato de la tesis de referencia (unas 130 palabras, dos párrafos, sin palabras clave ni números) y no el de 250 a 300 palabras que preveía este plan.

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
