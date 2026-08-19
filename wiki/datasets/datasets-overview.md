---
titulo: Estrategia de Datos del PFI
tipo: análisis
tags: [datasets, estrategia, tres-niveles, corpus-argentino, etiquetas]
fuentes: []
actualizado: 2026-08-19
---

# Estrategia de Datos del PFI

> Esta página reemplaza al panorama general de abril, que quedó desactualizado. El **relevamiento comparativo** de los datasets disponibles está en [[comparacion-datasets]] y en las fichas individuales. Acá se define **la estrategia propia**: qué se usa, en qué orden y para qué.

## Esquema de etiquetas

El clasificador devuelve **tres clases**:

| Clase | Significado |
|---|---|
| `verdadero` | La afirmación se corresponde con la evidencia disponible |
| `falso` | La afirmación es contradicha por la evidencia disponible |
| `sin_verificar` | No hay evidencia suficiente para pronunciarse |

La tercera clase no es un punto intermedio de una escala de veracidad: es la ausencia de evidencia. Se la trata como clase propia y no como un umbral de confianza porque el contenido de circulación reciente, que es el que interesa detectar, casi siempre cae ahí.

> ⚠️ **Distinción importante que se prestaba a confusión.** Las tres clases del clasificador **no son** los cuatro estados del veredicto que ve el usuario. El veredicto lo produce el orquestador combinando la salida del clasificador con el contraste externo y las señales de la cuenta. Ver [[requerimientos]] (RF-06) y [[modelo-datos]].

### Mapeo desde los datasets de origen

| Origen | Esquema original | Mapeo a las tres clases |
|---|---|---|
| LIAR | 6 niveles | `pants-fire`, `false`, `barely-true` → `falso`; `half-true`, `mostly-true`, `true` → `verdadero` |
| FakeNewsNet | 2 clases | Directo |
| FakeDeS | 2 clases | Directo |
| Corpus argentino | 3 clases | Nativo, anotado con el esquema propio |

Ninguno de los tres datasets externos aporta ejemplos de `sin_verificar`: todos etiquetan afirmaciones que **ya fueron verificadas**, que es justamente el sesgo de selección de los corpus de *fact-checking*. Esa clase se aprende únicamente del corpus argentino, y es una de las razones por las que construirlo no es opcional.

## Los tres niveles de datos de entrenamiento

### Nivel 1 — Transferencia desde el inglés

**LIAR** (12.836) + **FakeNewsNet** (~23.000) ≈ 36.000 ejemplos anotados.

Es el único volumen de datos anotados al que el proyecto tiene acceso real, y solo existe porque el modelo elegido es multilingüe. XLM-T procesa el español de forma nativa y aprovecha lo aprendido en inglés por **transferencia *cross-lingual***, sin traducir nada ([[drchal-2024-pipeline-multiidioma]]).

> La traducción automática de LIAR al español se evaluó en abril y se descartó: introduce ruido de traducción sobre un texto que ya es coloquial y breve, y deja de ser necesaria en cuanto el modelo es multilingüe.

### Nivel 2 — Adaptación al español

**FakeDeS / Spanish Fake News Corpus** (971).

971 ejemplos no alcanzan para entrenar un clasificador desde cero, pero sí alcanzan como **segundo ajuste** sobre un modelo que ya resolvió la tarea en inglés: en esa instancia el modelo no aprende qué es desinformación, aprende cómo se expresa en español. Limitación declarada: el corpus es de México y España, no rioplatense.

### Nivel 3 — Corpus argentino (contribución del PFI)

**No se recolecta por separado: se acumula operando el sistema.**

Cada publicación que el sistema analiza queda persistida con su texto, los metadatos públicos de la cuenta, el veredicto y la evidencia recuperada (RF-16). Esa es exactamente la estructura de un ejemplo de entrenamiento, así que el corpus es un subproducto del uso y no un proyecto de recolección aparte.

| Subconjunto | Volumen | Etiquetado | Rol |
|---|---|---|---|
| Adaptación | 2.000 a 5.000 | Derivado del veredicto, con revisión humana de los casos de baja confianza | Tercer ajuste del clasificador |
| Test | 300 a 500 | Anotación manual doble, acuerdo medido con Kappa de Cohen | *Holdout* estricto, no participa de ningún ajuste |

**Encuadre legal** (ver [[restricciones-legales-eticas]]): recolección amparada por el art. 5 inc. 2 ap. a) de la Ley 25.326 (fuentes de acceso público irrestricto); campos acotados por el principio de proporcionalidad del art. 4 inc. 1; supresión a pedido según el art. 16. El corpus **no se distribuye durante el PFI**, porque una fila se borra y un corpus descargado no.

## Datos de evidencia en tiempo de ejecución

No son datos de entrenamiento y conviene no confundirlos. El sistema consulta en línea tres clases de fuente, con la jerarquía definida en [[metodologia-tecnica]]:

- **Seis fuentes oficiales** pre-indexadas por una tarea programada (InfoLEG, INDEC, BCRA, Boletín Oficial, MSal, MinEdu).
- **Cinco medios de referencia** recuperados por API de búsqueda web (Infobae, Clarín, La Nación, Página/12, Télam).
- **Verificaciones previas** ya indexadas, cuando existen.

Las tres poblaciones viven en la misma entidad y sobre **un único índice HNSW de 768 dimensiones**, discriminadas por tipo de fuente. Ver [[arquitectura]] y [[modelo-datos]].

## Tabla resumen

| Nivel | Fuente | Volumen | Rol | Etapa |
|---|---|---|---|---|
| 1 | LIAR + FakeNewsNet (inglés) | ~36.000 | Ajuste inicial por transferencia | E4 |
| 2 | FakeDeS (español) | 971 | Adaptación al idioma | E4 |
| 3a | Corpus argentino, adaptación | 2.000 a 5.000 | Adaptación al dominio local | E4 y E5 |
| 3b | Corpus argentino, test | 300 a 500 | Evaluación en contexto real | E5 |
| — | Fuentes oficiales, medios y verificadores | Variable | Evidencia en tiempo de ejecución | E4 |

## Qué queda pendiente

- Búsqueda de corpus adicionales en español más allá de FakeDeS. Planteada en abril, nunca ejecutada.
- Definición del protocolo de revisión humana sobre el subconjunto de adaptación.

## Referencias cruzadas
- [[comparacion-datasets]]
- [[liar-dataset]] · [[fakenewsnet]] · [[spanish-fake-news-corpus]] · [[pheme-dataset]] · [[fakeddit]]
- [[metodologia-tecnica]] · [[modelo-datos]] · [[arquitectura]]
- [[pruebas]] · [[restricciones-legales-eticas]]
- [[dataset-recomendacion]] (documento histórico de abril)
