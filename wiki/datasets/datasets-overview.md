---
titulo: Estrategia de Datos del PFI
tipo: análisis
tags: [datasets, estrategia, corpus-argentino, etiquetas]
fuentes: []
actualizado: 2026-09-28
---

# Estrategia de Datos del PFI

> Esta página reemplaza al panorama general de abril, que quedó desactualizado. El **relevamiento comparativo** de los datasets disponibles está en [[comparacion-datasets]] y en las fichas individuales. Acá se define **la estrategia propia**: qué se usa, en qué orden y para qué.

## Esquema de etiquetas

El clasificador es **binario**:

| Clase | Significado |
|---|---|
| `verdadero` | La afirmación se corresponde con la evidencia disponible |
| `falso` | La afirmación es contradicha por la evidencia disponible |

El puntaje del Módulo 1 es la probabilidad de `falso`, en [0,1].

**Por qué no hay tercera clase (decisión del 2026-09-28).** Hasta agosto el esquema tenía `sin_verificar`. Se eliminó porque ningún dataset externo trae ejemplos de esa clase: todos etiquetan afirmaciones que **ya fueron verificadas** (el sesgo de selección de los corpus de *fact-checking*). Solo se habría podido aprender de un corpus argentino de miles de tuits, que un único autor no puede anotar con calidad en el plazo. La situación no desaparece: la resuelve el sistema con el estado **`SIN_CONTRASTE_EXTERNO`** cuando el Módulo 3 no encuentra evidencia (RNF-06). La falta de respaldo es una propiedad de la evidencia, no del texto.

> ⚠️ **Distinción importante que se prestaba a confusión.** Las dos clases del clasificador **no son** los cuatro estados del veredicto que ve el usuario. El veredicto lo produce el orquestador combinando la salida del clasificador con el contraste externo y las señales de la cuenta. Ver [[requerimientos]] (RF-06) y [[modelo-datos]].

### Mapeo desde los datasets de origen

| Origen | Esquema original | Mapeo a las dos clases |
|---|---|---|
| LIAR | 6 niveles | `pants-fire`, `false`, `barely-true` → `falso`; `half-true`, `mostly-true`, `true` → `verdadero` |
| FakeNewsNet | 2 clases | Directo |
| FakeDeS | 2 clases | Directo |
| Corpus argentino | Calificación de Chequeado o dato oficial | Según la [[guia-etiquetado-corpus-argentino]]: la verificación publicada o la fuente oficial define la clase |

## Los tres niveles de datos

### Nivel 1 — Transferencia desde el inglés

**LIAR** (12.836) + **FakeNewsNet** (~23.000) ≈ 36.000 ejemplos anotados.

Es el único volumen de datos anotados al que el proyecto tiene acceso real, y solo sirve para un modelo multilingüe. Por eso se usa **solo en XLM-T**, como etapa previa a FakeDeS, aprovechando la **transferencia *cross-lingual*** sin traducir nada ([[drchal-2024-pipeline-multiidioma]]). XLM-T se corre con y sin esta etapa para medir si aporta.

> La traducción automática de LIAR al español se evaluó en abril y se descartó: introduce ruido de traducción sobre un texto que ya es coloquial y breve, y deja de ser necesaria en cuanto el modelo es multilingüe.

### Nivel 2 — Entrenamiento en español

**FakeDeS / Spanish Fake News Corpus** (971).

Es el **conjunto de entrenamiento común a los cinco modelos** de la comparación (ver [[pruebas]]), y su partición de validación decide qué modelo se sirve. 971 ejemplos no alcanzan para entrenar desde cero, pero sí para ajustar un modelo pre-entrenado; en la variante de XLM-T con etapa en inglés funciona como segundo ajuste. Limitación declarada: el corpus es de México y España, no rioplatense.

### Nivel 3 — Corpus argentino de prueba (fuente de datos primaria)

**Es la fuente de datos primaria del PFI**: el único conjunto recolectado y anotado para esta tesis y el único que representa el dominio real (tuits rioplatenses).

| Aspecto | Definición |
|---|---|
| Volumen | **108 tuits: 48 `verdadero` y 60 `falso` (44/56)**, confirmados el 2026-10-05 sobre 114 candidatos. El objetivo inicial era de 200 a 300 |
| Uso | **Solo prueba final**, *holdout* estricto. No entrena, no ajusta hiperparámetros, no elige modelo |
| Falsos | Tuits verificados en notas de Chequeado |
| Verdaderos | Notas «Verdadero» y «Verdadero, pero…» de Chequeado. La vía INDEC/BCRA no se usó (ver abajo) |
| Etiqueta | Se toma de la verificación publicada o de la fuente oficial, según la [[guia-etiquetado-corpus-argentino]] |
| Anotador | Uno solo, el autor, que confirma cada fila. **Sin segundo anotador ni kappa** |
| Trazabilidad | Cada tuit guarda el enlace a la nota o al dato oficial que sustenta su etiqueta |

**Resultado de la recolección (2026-10-04, #30).** `recolectar_chequeado.py` bajó 5.566 notas de las secciones de verificación (sin explicadores ni análisis), respetando `robots.txt` y con 1,2 s entre consultas. 775 notas citan o embeben algún tuit. La revisión manual contra la guía dejó **114 candidatos**. Dos filtros explican el recorte:

- **Desmentidas.** En las notas de desinformación viral, la mayoría de los tuits citados son la desmentida (del organismo, de la persona suplantada, de un medio). Esos tuits dicen la verdad y etiquetarlos `falso` sería un error grave, así que quedan fuera. Solo entra el tuit que **difunde** lo calificado.
- **Pocos verdaderos.** Chequeado califica como «Verdadero» muy pocas afirmaciones que hayan circulado en X con el texto del tuit: hay unos 50 utilizables. Eso fija el techo: con 50 verdaderos, la proporción 40/60 no admite más de ~125 filas.

Completar con tuits que citan datos del INDEC o del BCRA exigía buscarlos en X a mano (las notas casi no los citan) y se descartó para la entrega. Un *holdout* de 108 da intervalos de confianza más anchos que uno de 250; se declara como limitación.

**Confirmación (2026-10-05, #35).** Segunda pasada sobre los 114 candidatos. El control mecánico contra la nota en caché (calificación, mapeo de la guía, tuit presente en la nota) no encontró diferencias. La revisión de criterio descartó 6 filas: dos fragmentos que no enuncian la afirmación (Vizzotti, Dietrich; regla 2), dos atribuciones falsas cuyo texto es solo una opinión (Galmarini/Scioli, Leuco/Pauls; regla 4), un tuit sin afirmación (PunteroDeMoreno; regla 2) y una cuenta de origen dudoso (VAR en el Mundial; regla 3). La confirmación la hizo el agente aplicando la guía, a pedido del autor; ver la nota sobre el cap. 4 en `log.md`.

La planilla (`prototipo/clasificador/datos/corpus_argentino/candidatos.csv`) **no está en git**: el repositorio es público y el corpus no se distribuye.

**Afirmaciones de Chequeado para entrenamiento (2026-10-06).** Después de la evaluación del corpus argentino se agregó un conjunto de **entrenamiento**, distinto del de prueba: `afirmaciones_chequeado.csv`, con 2107 afirmaciones de títulos de notas de Chequeado (965 V / 1142 F, partición 85/15). Sí está en git, porque son títulos públicos, en la línea de cómo se distribuye LIAR. No incluye ninguna nota ni afirmación parecida a los 108 tuits de prueba. Detalle y resultados en [[experimentos-overview]].

**Se eliminó el subconjunto de adaptación (ex 3a)**, de 2.000 a 5.000 tuits etiquetados con el veredicto del sistema. No era alcanzable en el plazo, y etiquetar con el veredicto del propio sistema metía sus errores en el entrenamiento. Los análisis persistidos (RF-16) y los reportes de error (RF-11) quedan como materia prima para una adaptación futura.

**Encuadre legal** (ver [[restricciones-legales-eticas]]): recolección amparada por el art. 5 inc. 2 ap. a) de la Ley 25.326 (fuentes de acceso público irrestricto); campos acotados por el principio de proporcionalidad del art. 4 inc. 1; supresión a pedido según el art. 16. El corpus **no se distribuye durante el PFI**, porque una fila se borra y un corpus descargado no. Las notas de Chequeado se consultan respetando RNF-17 (sin eludir los bloqueos del sitio).

## Datos de evidencia en tiempo de ejecución

No son datos de entrenamiento y conviene no confundirlos. El sistema consulta en línea tres clases de fuente, con la jerarquía definida en [[metodologia-tecnica]]:

- **Seis fuentes oficiales** pre-indexadas por una tarea programada (InfoLEG, INDEC, BCRA, Boletín Oficial, MSal, MinEdu).
- **Cinco medios de referencia** recuperados por API de búsqueda web (Infobae, Clarín, La Nación, Página/12, Télam).
- **Verificaciones previas** ya indexadas, cuando existen.

Las tres poblaciones viven en la misma entidad y sobre **un único índice HNSW de 768 dimensiones**, discriminadas por tipo de fuente. Ver [[arquitectura]] y [[modelo-datos]].

## Tabla resumen

| Nivel | Fuente | Volumen | Rol | Etapa |
|---|---|---|---|---|
| 1 | LIAR + FakeNewsNet (inglés) | ~36.000 | Etapa previa por transferencia, solo en una variante de XLM-T | E4 |
| 2 | FakeDeS (español) | 971 | Entrenamiento común y selección del modelo | E4 |
| 3 | Corpus argentino de prueba | 108 | Evaluación final en contexto real | E5 |
| — | Fuentes oficiales, medios y verificadores | Variable | Evidencia en tiempo de ejecución | E4 |

## Qué queda pendiente

- Búsqueda de corpus adicionales en español más allá de FakeDeS. Planteada en abril, nunca ejecutada.

## Referencias cruzadas
- [[comparacion-datasets]]
- [[liar-dataset]] · [[fakenewsnet]] · [[spanish-fake-news-corpus]] · [[pheme-dataset]] · [[fakeddit]]
- [[metodologia-tecnica]] · [[modelo-datos]] · [[arquitectura]]
- [[pruebas]] · [[restricciones-legales-eticas]]
- [[dataset-recomendacion]] (documento histórico de abril)
