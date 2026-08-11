---
titulo: Decisiones pendientes — resolución del health-check 2026-08-08
tipo: análisis
tags: [decisiones, modelo, pipeline, entrega-50, lint]
fuentes: []
actualizado: 2026-08-13
---

# Decisiones pendientes — resolución del health-check 2026-08-08

Esta página traduce las contradicciones del lint del 2026-08-08 en decisiones concretas con opciones y costo de cada una. Se escribe a 20 días de la **Entrega 3 (50%) — 28 de agosto de 2026**.

## Regla de priorización

La Entrega 3 cubre **User Research + competencia + modelo de negocio** (`chapters/chapter03.tex`). Las decisiones de modelo y pipeline pertenecen a la Entrega 4 (octubre). Por lo tanto: las decisiones 1 a 3 de esta página **no bloquean el 28 de agosto** y no deben consumir el tiempo de estas semanas. Se documentan ahora para que estén cerradas antes de escribir código.

---

## Decisión 1 — Modelo principal del clasificador ✅ RESUELTA el 2026-08-13

**Se ratificó la Opción C: XLM-T (`cardiffnlp/twitter-xlm-roberta-base`) como modelo principal**, con RoBERTuito y BETO como líneas de comparación y TF-IDF con regresión logística como *baseline*. La Opción D se adopta como marco: la ratificación fija el modelo con el que se construye el prototipo, pero la comparación experimental sigue en pie y su tabla de resultados es el contenido del capítulo 4 en la Entrega 4. Si la comparación contradice la elección, la elección se revierte.

**Qué destrabó la decisión.** No fue el rendimiento sino los datos. El Tier 1 —unos 40.000 ejemplos anotados en inglés— solo existe con un modelo multilingüe, y XLM-T es el único candidato que conserva esa transferencia sin renunciar al registro de Twitter.

**Contra conocida, declarada.** Gouliev et al. (2025) reportan entre 8 y 12 puntos de caída de los multilingües frente a los nativos del idioma. Se asume porque esa medición es sobre multilingües genéricos y XLM-T está adaptado al dominio, pero es un argumento de plausibilidad, no una demostración: por eso la comparación contra RoBERTuito existe.

**Propagado a:** `modelos-overview`, `metodologia-tecnica`, `propuesta`, `recursos`, `enfoques-deteccion`, `transformers-bert`, `modelos-espanol` (ficha nueva), `comparativa-llms-2024-2025`, `brechas-espanol-latam`, `arquitectura` (ya lo decía), más `chapter02.tex` y la entrada `BarbieriEtAl2022` en `biblio.bib`.

**No se tocó** lo que reporta resultados de terceros: las mediciones de Toapanta et al. (2024) en `toapanta-2024-latam` y en `chapter02.tex` quedan como están.

### El hecho que reduce el costo de cambiar

`documento/chapters/chapter01.tex:23` —los objetivos específicos, la parte formalmente presentada— ya está redactado de forma **agnóstica**: "arquitecturas Transformer pre-entrenadas en español —BETO, XLM-RoBERTa o RoBERTuito—". Solo el capítulo 2 se inclina por RoBERTuito, y lo hace en **tres oraciones**: L50, L214 y L301. Cambiar de modelo principal cuesta tres oraciones, no un capítulo.

### Sobre la confiabilidad de RoBERTuito

La duda no se sostiene. RoBERTuito se publicó en **LREC 2022** (Pérez, Furman, Alonso Alemany y Luque, pp. 7235–7243, ACL Anthology), que es el mismo tipo de venue que XLM-RoBERTa (Conneau et al., ACL 2020). Además ya fue evaluado en la tarea exacta del PFI por Toapanta et al. (2024): 93,53 % de exactitud y F1 0,934, empatado con BETO (93,53 %, F1 0,935) y por debajo de MarIA (96,01 %). Que sea de la UBA y el CONICET es un argumento **a favor** en un PFI argentino, no en contra: implica que el corpus contiene variedad rioplatense.

### El trade-off real (no es prestigio, es datos)

| | RoBERTuito | XLM-RoBERTa |
|---|---|---|
| Ajuste al dominio (tweets informales) | Alto — pre-entrenado sobre 500M de tweets en español | Bajo — corpus web genérico |
| Transferencia desde inglés | **No** (monolingüe) | **Sí** |
| Consecuencia sobre el Tier 1 de datos | LIAR y FakeNewsNet quedan inutilizables | LIAR y FakeNewsNet siguen en juego |

Esta es la raíz de la contradicción: el Tier 1 de `comparacion-datasets` (40.000 ejemplos en inglés) **solo existe si el modelo es multilingüe**. Con RoBERTuito, el conjunto de entrenamiento se reduce a FakeDeS (971 ejemplos) más el corpus argentino que se construya.

### Opciones

**Opción A — XLM-RoBERTa como principal.**
Habilita el Tier 1 y unifica la estrategia de datos. Costo: reescribir las tres oraciones del capítulo 2. Cuidado: L214 usa a Albtoush et al. (2025) para argumentar que los modelos específicos del idioma superan a los multilingüe; hay que reformular esa oración para no quedar en auto-contradicción.

**Opción B — RoBERTuito como principal (estado actual).**
Cero cambios en el documento y mejor ajuste al dominio, pero obliga a descartar LIAR y FakeNewsNet y a que el corpus argentino esté listo antes y sea grande (2.000–5.000). Aumenta el riesgo de la Entrega 4.

**Opción C — XLM-T (`cardiffnlp/twitter-xlm-roberta-base`) — recomendada.**
Es **XLM-RoBERTa de Meta re-pre-entrenado sobre ~198M de tweets en más de 30 idiomas** por Cardiff NLP. Publicado como Barbieri et al., *XLM-T: Multilingual Language Models in Twitter for Sentiment Analysis and Beyond*, LREC 2022, pp. 258–266. Combina las dos propiedades que están en tensión: el linaje y la arquitectura de XLM-RoBERTa —con transferencia desde el inglés intacta— y la adaptación al dominio de Twitter. Costo: las mismas tres oraciones más una entrada nueva en `biblio.bib` (`BarbieriEtAl2022`).

**Opción D — no decidir por decreto: declararlo comparación experimental — recomendada como marco, compatible con A, B o C.**
`chapter01.tex:23` ya compromete que "la elección del modelo y los resultados experimentales se documentarán con métricas estándar". Convertir eso en una comparación explícita de cuatro modelos —el principal elegido, RoBERTuito, BETO y TF-IDF con regresión logística como *baseline*— es lo que hizo Toapanta et al. y es la razón por la que ese trabajo es publicable. Ventajas: elimina la necesidad de acertar hoy, da contenido real al capítulo 4 (una tabla de resultados en vez de `Completar.`) y convierte la contradicción en metodología. El "modelo principal" pasa a ser el que gane la comparación.

---

## Decisión 2 — Ensemble de dos modelos en `modelos-espanol.md` ✅ RESUELTA el 2026-08-13

**Se aplicó la Opción A:** eliminada la recomendación de *ensemble*, un solo clasificador. Cayó sola con la Decisión 1, porque XLM-T cubre por sí mismo las dos propiedades que motivaban usar dos modelos. Además de alinear el wiki, hacerlo con un modelo en lugar de dos elimina un servicio de inferencia del despliegue y su costo.



`modelos-espanol.md:106-112` recomienda usar dos modelos en paralelo: RoBERTuito para publicaciones de redes y XLM-RoBERTa para artículos periodísticos. Es un resto del alcance anterior al 2026-06-13, cuando el sistema todavía clasificaba notas de Infobae y Clarín. Hoy los medios son **fuente de evidencia**, no objetos de clasificación: no hay artículos periodísticos que clasificar, así que el segundo modelo no tiene entrada.

**Opción A (recomendada):** eliminar la recomendación de ensemble y dejar un único clasificador, alineado con `modelos-overview`. Sin impacto en el documento.
**Opción B:** conservarla explícitamente etiquetada como línea futura para cuando el alcance incluya medios digitales.

---

## Decisión 3 — `pipeline-preprocesamiento.md` en BETO ✅ RESUELTA el 2026-08-13

**Se aplicó la Opción B:** reescrita la etapa de limpieza hacia XLM-T. Se optó por reescribir y no por poner un aviso porque, ratificada la Decisión 1, el riesgo de rehacerlo desapareció.

La reescritura invirtió el principio de la página: preprocesar es **adaptarse al pre-entrenamiento del modelo**, no "limpiar" el texto. Se conservan emojis, mayúsculas, signos repetidos y números; se normalizan URLs a `http` y menciones a `@usuario`; se segmentan los hashtags. La función de limpieza pasó de doce líneas a cinco.

**Lo más importante que apareció al reescribir, y que no estaba en el diagnóstico original:** la recomendación de reemplazar los números por un token `<NUM>` es un error grave en este dominio, no una optimización menor. Con `<NUM>`, «cerró 500 escuelas» y «cerró 50 escuelas» son la misma entrada para el modelo — y esa diferencia es exactamente la afirmación que el sistema tiene que detectar, el ejemplo que recorre toda la metodología técnica. Los números se conservan.

Se agregó además la advertencia de que RoBERTuito, al ser *uncased*, necesita su propio preprocesamiento (`pysentimiento.preprocessing`) al evaluarlo: aplicarle el de XLM-T arruinaría la comparación de forma silenciosa. Corregida la errata `dcc-uchile` → `dccuchile`.



El problema serio no es el nombre del modelo sino la **etapa de limpieza**: la página remueve emojis, *mentions* y hashtags y pasa todo a minúsculas. Eso es correcto para BETO —entrenado sobre Wikipedia— y es lo peor posible para cualquier modelo pre-entrenado sobre tweets. Tanto RoBERTuito (vía `pysentimiento.preprocessing`) como XLM-T esperan que los emojis se conserven o se conviertan a texto, que los hashtags se segmenten en lugar de borrarse, y que las menciones se reemplacen por un token especial (`@usuario`) en vez de eliminarse. Aplicar el pipeline tal como está anula la ventaja de dominio que justifica elegir un modelo social.

Errata adicional: el identificador `dcc-uchile/bert-base-spanish-wwm-uncased` no existe; el correcto es `dccuchile/bert-base-spanish-wwm-uncased`.

**Opción A (recomendada si se adopta la Decisión 1-D):** dejar la página como está y agregarle un aviso al inicio de que describe la variante BETO y que la limpieza se redefine cuando la comparación experimental fije el modelo. Cinco minutos.
**Opción B:** reescribir ahora la sección de limpieza hacia el modelo elegido (conservar emojis y hashtags, `@usuario` como token). Medio día, y hay que rehacerlo si la comparación da otro ganador.
**Opción C:** documentar las dos variantes de limpieza en paralelo. Más trabajo del que el PFI necesita.

---

## Decisión 4 — Tamaño del corpus argentino

`dataset-recomendacion.md` pide 200–500 publicaciones anotadas; `comparacion-datasets.md:58` fija 2.000–5.000 como contribución académica. Son dos cosas distintas mezcladas: 200–500 alcanza para un **conjunto de test** de validación en contexto real, pero no para entrenar.

**Opción A (recomendada):** conservar los dos números pero con roles explícitos — 2.000–5.000 para entrenamiento y adaptación, 300–500 para el conjunto de test argentino anotado con acuerdo inter-anotador. Elimina la contradicción sin bajar la ambición.
**Opción B:** bajar la meta a 200–500 y renunciar al corpus como contribución académica. Debilita el aporte del PFI, que el capítulo 2 ya declara como una de sus tres contribuciones.

---

## Decisión 5 — Número de clases

Conviven tres definiciones: binario (`dataset-recomendacion.md:34`, colapsando las 6 clases de LIAR), tres etiquetas en el esquema de anotación (0 verdadero / 1 falso / 2 mixto) y tres clases en la salida del módulo 1 (`metodologia-tecnica.md:45`).

**Opción A (recomendada):** tres clases —verdadero, falso, no verificable— en todo el sistema. Es coherente con la definición operativa del capítulo 1 ("potencialmente falso, engañoso **o no verificable**") y con la salida del módulo 1; la clase "no verificable" es la que justifica el módulo de contraste con evidencia.
**Opción B:** binario. Más simple de entrenar y más comparable con la literatura, pero contradice la definición operativa ya escrita en el documento.

---

## Correcciones mecánicas (sin decisión, solo aplicar)

| # | Qué | Dónde |
|---|---|---|
| 1 | Tutor: Monzón → Giro Uribazo | `cronograma.md:39`, `pruebas.md:24`, `fake-news-detector-br.md:78` |
| 2 ✅ | Serper.dev → Tavily como servicio del PFI | Aplicado el 2026-08-10 en los cuatro archivos. Se conservó «Serper/Google» donde nombra el montaje del paper citado y no el del PFI |
| 3 ✅ | Costo del período PFI: ~USD 65 → **USD 168** | Aplicado el 2026-08-10 en `modelo-de-negocio.md`. No son 173: el cargo de la Chrome Web Store pasó a costo diferido al decidirse que la extensión no se publica |
| 4 | Alcance Twitter/X únicamente | `newtral-factflow.md:54,81`, `toapanta-2024-latam.md:54` |
| 5 | Chequeado ya no es corpus de contraste ni de entrenamiento | `enfoques-deteccion.md:179`, `analisis-competitivo.md:35` |
| 6 | Tamaño de FakeNewsNet: unificar en ~23.000 (PolitiFact 1.056 + GossipCop 22.140) | `dataset-recomendacion.md:42`, `comparacion-datasets.md:18` |
| 7 | Completar el cronograma con las fechas reales | `cronograma.md` |
| 8 | Salir de `[POR DEFINIR]` remitiendo a las páginas que ya lo resuelven | `datasets-overview.md` |
| 9 | Links a carpeta y residuos de template | `implementaciones-overview.md`, `datasets-overview.md` |

## Referencias cruzadas

- [[wiki/modelos/modelos-overview]]
- [[wiki/marco-teorico/modelos-espanol]]
- [[wiki/solucion/pipeline-preprocesamiento]]
- [[wiki/datasets/comparacion-datasets]]
- [[wiki/proyecto/cronograma]]
