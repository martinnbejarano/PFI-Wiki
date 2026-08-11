---
titulo: Modelo de Datos
tipo: análisis
tags: [modelo-de-datos, der, entidades, postgresql, pgvector, criterio-6]
fuentes: [Rubrica-EP2-50porciento.pdf]
actualizado: 2026-08-11
---

# Modelo de Datos

Cubre la mitad del **criterio 6** de la rúbrica de EP2; la otra mitad es el diagrama de arquitectura de [[wiki/solucion/arquitectura]]. El motor está decidido en [[wiki/proyecto/recursos]] y en [[wiki/solucion/tecnologias]]: PostgreSQL 16 gestionado en Railway, con la extensión `pgvector` para las columnas de *embeddings*.

El modelo se presenta a **nivel lógico**: entidades, atributos, tipos, claves primarias y foráneas, y cardinalidades. No incluye DDL ejecutable ni índices más allá de los que son una decisión de diseño y no de afinamiento. La creación real de la base pertenece al bloque de implementación.

**Regla de corte.** Toda entidad tiene que ser trazable a un requerimiento funcional de [[wiki/solucion/requerimientos]]. La matriz del final de esta página es lo que hace verificable esa regla, y hay una entidad —`medio_confiable`— que se mantiene por normalización y no por requerimiento: la excepción está declarada y argumentada, no escondida.

## Panorama

Diecisiete entidades repartidas en cinco dominios. El número es una consecuencia del recorrido de diseño y no un objetivo: el plan de agosto proyectaba catorce sobre una foto de abril, y desde entonces la ingesta asíncrona sumó su catálogo, la evidencia se partió en dos, la justificación pasó a tener estructura propia y la configuración del ensamblado se independizó de la versión del modelo.

| Dominio | Entidades |
|---|---|
| 1 · Contenido analizado | `tuit`, `cuenta`, `fuente_oficial`, `medio_confiable` |
| 2 · Análisis y evidencia | `analisis`, `razon`, `claim`, `documento`, `evidencia` |
| 3 · Uso ciudadano | `usuario_extension`, `reporte` |
| 4 · Trazabilidad del modelo | `modelo_version`, `configuracion_ensamblado` |
| 5 · Plataforma B2B | `organizacion`, `usuario_b2b`, `api_key`, `consumo_api` |

`analisis` es el centro del esquema: participa de nueve de las veinte relaciones que dibuja el DER, más la relación N:M derivada con `documento`. Es la consecuencia directa de RF-27, que exige que cada análisis quede atado a lo que lo produjo —modelo y configuración de pesos— y de la doble propiedad que introduce la plataforma B2B.

## Diagrama entidad-relación

Fuente: `wiki/assets/diagramas/der.drawio`, exportado a `documento/chapters/figures/der.png`.

El dibujo lleva las diecisiete entidades y las veinte relaciones con su cardinalidad —la tabla de más abajo suma una fila más, la N:M entre `analisis` y `documento`, que no se dibuja porque se deriva de la tabla puente—; los atributos viven en las tablas de esta página. Es una decisión de legibilidad: un DER con atributos dentro de cada caja se vuelve ilegible impreso en A4 a partir de la docena de entidades, y las tablas permiten además declarar el tipo y la nulabilidad de cada columna, que es donde está la mitad de las decisiones de diseño. El dominio se identifica por color, con la referencia en el propio diagrama.

## Dominio 1 — Contenido analizado

Es lo que el sistema observa: el tuit, su autor y los dos catálogos de fuentes contra las que después se contrasta.

### `tuit`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_tuit` | `bigserial` | PK | |
| `id_nativo` | `text` | UNIQUE, NULL | RF-01; se borra en la supresión |
| `texto` | `text` | NOT NULL | RF-26 |
| `fecha_publicacion` | `timestamptz` | NOT NULL | RF-01 |
| `plataforma` | `text` | NOT NULL | RF-01 |
| `m_likes`, `m_retweets`, `m_respuestas`, `m_citas` | `int` | NULL | RF-01, métricas de propagación |
| `fecha_captura` | `timestamptz` | NOT NULL | |
| `id_cuenta` | `bigint` | FK → `cuenta`, NULL | |

**La URL no se persiste.** Se reconstruye siempre como `x.com/i/status/{id_nativo}`, forma que redirige al tuit. Guardar `x.com/usuario/status/123` era guardar el `@` en texto plano en una segunda columna: borrar `cuenta.handle` y dejar esa URL intacta no anonimiza nada.

**`id_nativo` es nulable porque se borra en la supresión.** La fila conserva texto, análisis y evidencia, y pierde el identificador que permitía recuperar el `@` consultando la plataforma. El costo está escrito y no tapado: esa fila puntual deja de ser reproducible para el trabajo experimental de la Entrega 5. Es un costo acotado a las filas efectivamente suprimidas, y es el escenario correcto — quien ejerció el art. 16 de la Ley 25.326 obtuvo lo que pidió.

Se descartó hashear el identificador desde la captura: rompía RF-10 y la deduplicación del caché —los dos se apoyan en el identificador nativo para saber si un tuit ya fue analizado— y volvía irreproducible el corpus entero para resolver un problema de unas pocas filas.

**No hay `fecha_purga` ni columna de política de retención.** La postura de [[wiki/proyecto/restricciones-legales-eticas]] es retención sin plazo con finalidad declarada estrecha, así que no existe un reloj que modelar.

### `cuenta`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_cuenta` | `bigserial` | PK | Seudónimo del panel B2B |
| `handle` | `text` | NULL | Se borra en la supresión |
| `id_nativo_cuenta` | `text` | NULL | Se borra en la supresión |
| `fecha_creacion` | `date` | NULL | RF-03, antigüedad |
| `seguidores`, `seguidos` | `int` | NULL | RF-03 |
| `verificada` | `boolean` | NULL | RF-03 |
| `frecuencia_tuits` | `numeric` | NULL | RF-03 |
| `n_marcados_agregado` | `int` | NULL | RF-03, historial de contenido marcado |
| `suprimida` | `boolean` | NOT NULL, `false` | Marca de supresión |
| `fecha_supresion` | `timestamptz` | NULL | |

`suprimida` no es redundante con vaciar los campos: es lo que impide que el sistema vuelva a enriquecer la fila la próxima vez que aparezca un tuit de esa misma cuenta.

**El seudónimo del panel B2B es `id_cuenta`, el serial que la tabla ya tiene.** RNF-10 exige que ninguna entrega hacia terceros lleve la identidad de la cuenta autora en claro, y la supresión manda borrar el `@`. Agrupar por el serial resuelve las dos cosas a la vez: no deriva del `@`, así que es irreversible por construcción y no por fuerza criptográfica, y sobrevive a la supresión sin comprometerla —la fila queda sin `@` y sin metadatos, o sea disociada— conservando la serie histórica de esa cuenta en el panel.

Se descartó un HMAC del `@` con clave del servidor: habría sido un derivado del dato personal, con gestión de claves y un secreto más que custodiar, para lograr lo que el serial da sin costo. Un SHA-256 pelado quedaba descartado de entrada, porque un `@` es reversible por diccionario en segundos.

### `fuente_oficial`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_fuente` | `bigserial` | PK | |
| `nombre` | `text` | NOT NULL | RF-06 |
| `dominio` | `text` | NOT NULL, UNIQUE | RF-06 |
| `tipos_afirmacion` | `text[]` | NOT NULL | RF-04 y RF-06, ruteo por tipo |
| `crawl_delay_s` | `int` | NULL | Declarado en el `robots.txt` del sitio |
| `fecha_ultima_ingesta` | `timestamptz` | NULL | Estado de la ingesta programada |

Es la entidad que la ingesta asíncrona hizo necesaria. No es un catálogo de constantes: `fecha_ultima_ingesta` y `crawl_delay_s` son estado variable por sitio, y es lo que el proceso programado lee y escribe en cada corrida. Ver [[wiki/solucion/arquitectura]].

### `medio_confiable`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_medio` | `bigserial` | PK | |
| `nombre` | `text` | NOT NULL | RF-05 |
| `dominio` | `text` | NOT NULL, UNIQUE | RF-05 |
| `handle_x` | `text` | NULL | Rasgo `in_trusted_db` del Módulo 2 |

**Esta es la excepción a la regla de corte, y se declara como tal.** Ningún requerimiento pide administrar la lista: los cinco medios están escritos dentro del texto de RF-05 y el conjunto es cerrado. Se mantiene por **normalización**: es el destino de la clave foránea que evita un `documento.medio` de texto libre, le da identidad estable a los cinco medios para el rasgo de medio confiable del Módulo 2 y sostiene el orden jerárquico de RF-13. La regla de corte se lee entonces como «ninguna entidad sin propósito trazable a un RF», y su propósito traza a RF-05 y RF-13.

## Dominio 2 — Análisis y evidencia

Es el resultado del sistema y lo que lo respalda.

### `analisis`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_analisis` | `bigserial` | PK | |
| `id_tuit` | `bigint` | FK → `tuit`, NOT NULL | |
| `score_nlp` | `numeric(4,3)` | NOT NULL | RF-02 |
| `score_source` | `numeric(4,3)` | NULL | RF-03, solo flujo profundo |
| `score_similarity` | `numeric(4,3)` | NULL | RF-05 a RF-07, solo flujo profundo |
| `score_final` | `numeric(4,3)` | NULL | RF-08 |
| `veredicto` | `enum(contradicho, sospechosa, verificado, sin_contraste)` | NULL | RF-08 |
| `parcial` | `boolean` | NOT NULL, `false` | RF-14 |
| `modulos_faltantes` | `text[]` | NULL | RF-14 |
| `profundidad` | `enum(automatico, completo)` | NOT NULL | Decisión 1 de producto |
| `id_modelo_version` | `bigint` | FK, NOT NULL | RF-27 |
| `id_config_ensamblado` | `bigint` | FK, NOT NULL | RF-27 |
| `uuid_usuario` | `uuid` | FK → `usuario_extension`, NULL | RF-15 |
| `id_organizacion` | `bigint` | FK → `organizacion`, NULL | RF-22 |
| `fecha_analisis` | `timestamptz` | NOT NULL | |
| `vigente_hasta` | `timestamptz` | NULL | RF-10, política diferida |

Restricción de tabla: exactamente una de `uuid_usuario` y `id_organizacion` está poblada.

**Una sola fila que se completa, no dos filas.** Una fila por tuit y versión de modelo. Nace en CU-01 con `score_nlp` y se completa con una actualización cuando corre el flujo profundo de CU-02; `profundidad` distingue un estado del otro. Dos filas habrían obligado a decidir cuál de las dos es *el* veredicto del tuit en el histórico de RF-15 y en la agregación por tema de RF-24, y esa pregunta no tiene buena respuesta.

**`veredicto` tiene cuatro valores y no tres.** Los tres niveles de RF-08 más `sin_contraste`, que es el estado que vuelve cumplible a RNF-06: cuando ningún módulo externo encontró fuente, el indicador se emite igual pero como ausencia declarada y sin porcentaje, en lugar de vestirse de veredicto.

**`parcial` y `modulos_faltantes` son ortogonales al veredicto, no parte de él.** Son cosas distintas: `sin_contraste` es que el módulo corrió y no encontró fuente; `parcial` es que el módulo no pudo correr. Pueden darse a la vez, así que necesitan campos separados. Meterlas en el mismo enumerado habría hecho que RF-14 dejara de significar lo que dice.

**El dueño del análisis es explícito.** Dos claves foráneas nulables con la restricción de exclusividad, en lugar de deducir la propiedad recorriendo `consumo_api`. Esa deducción dejaba la pertenencia implícita a dos junturas de distancia y acoplaba la propiedad de un análisis a su facturación, que se rompe el día que un análisis B2B no genere fila de consumo.

### `razon`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_razon` | `bigserial` | PK | |
| `id_analisis` | `bigint` | FK, NOT NULL | RF-09 |
| `texto` | `text` | NOT NULL | RF-09 |
| `orden` | `int` | NOT NULL | RF-09, orden de presentación |
| `id_evidencia` | `bigint` | FK → `evidencia`, NULL | RF-09 |

RF-09 exige que cada razón derivada de evidencia externa lleve el enlace a la fuente que la respalda. La clave foránea nulable es exactamente esa condición: hay razones que salen del análisis lingüístico o de las señales de la cuenta y no derivan de ningún documento, y esas quedan sin enlace de forma legítima.

### `claim`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_claim` | `bigserial` | PK | |
| `id_tuit` | `bigint` | FK, NOT NULL | |
| `texto` | `text` | NOT NULL | RF-04 |
| `tipo` | `enum(normativa, dato_economico, salud, educacion, otro)` | NOT NULL | RF-04 |
| `vector` | `vector(768)` | NULL | RF-07, índice HNSW |

### `documento`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_documento` | `bigserial` | PK | |
| `url` | `text` | UNIQUE, NOT NULL | RF-13 |
| `titulo` | `text` | NULL | RF-13 |
| `texto` | `text` | NULL | RF-05 a RF-07 |
| `tipo_fuente` | `enum(oficial, medio, verificador)` | NOT NULL | RF-13, orden jerárquico |
| `id_fuente_oficial` | `bigint` | FK, NULL | RF-06 |
| `id_medio` | `bigint` | FK, NULL | RF-05 |
| `fecha_publicacion` | `date` | NULL | |
| `fecha_ingesta` | `timestamptz` | NOT NULL | Ingesta programada |
| `vector` | `vector(768)` | NULL | RF-07, índice HNSW |

### `evidencia`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_evidencia` | `bigserial` | PK | |
| `id_analisis` | `bigint` | FK, NOT NULL | |
| `id_documento` | `bigint` | FK, NOT NULL | |
| `postura` | `enum(corrobora, contradice, neutral)` | NOT NULL | RF-05 |
| `similitud` | `numeric(4,3)` | NULL | RF-07 |
| `extracto` | `text` | NULL | RF-13 |

Restricción de tabla: `UNIQUE (id_analisis, id_documento)`.

**Por qué la evidencia son dos entidades y no una.** `documento` guarda lo que es propiedad del documento —su URL única, su texto y su vector—; `evidencia` es la tabla puente y lleva lo que es propiedad del **vínculo** entre ese documento y un análisis concreto: la postura, la similitud y el extracto. La misma nota del Boletín Oficial puede corroborar un análisis y contradecir otro, así que postura y similitud no son atributos del documento.

Tres consecuencias, y son las que decidieron la partición:

1. **Un documento sostiene varios análisis sin duplicar texto.** El artículo que contradice quince tuits se guarda una vez.
2. **Hay un solo índice HNSW en lugar de tres.** `documento` absorbe el índice de fuentes oficiales que exige la ingesta programada y el corpus de verificaciones previas, con `tipo_fuente` como discriminador. Las tres poblaciones se consultan de la misma forma —búsqueda por similitud sobre el texto de una fuente—, así que separarlas era triplicar un índice sin ganar nada.
3. **RF-13 se resuelve con un `ORDER BY`** sobre `tipo_fuente`, en lugar de una unión de tres tablas.

**La dimensión de los vectores es 768**, la del codificador `multilingual-e5-base` fijado en [[wiki/solucion/tecnologias]]. No es un número elegido en el modelo de datos: lo impone el modelo de *embeddings*, y cambiarlo obliga a reindexar.

## Dominio 3 — Uso ciudadano

### `usuario_extension`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `uuid` | `uuid` | PK | RF-15 |
| `fecha_instalacion` | `timestamptz` | NOT NULL | |

**Dos columnas y nada más.** Sin preferencias, sin fecha de última actividad y sin contador de consultas: todo eso engordaría el perfil justo en la tabla que hay que defender. La configuración de RF-16 y de RF-19 no sale del almacenamiento local del navegador, así que no tiene tabla.

La postura legal es que este identificador no constituye dato personal en los términos del art. 2 de la Ley 25.326, por no referirse a persona determinada ni determinable. El argumento, con su flanco declarado, está en [[wiki/proyecto/restricciones-legales-eticas]].

### `reporte`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_reporte` | `bigserial` | PK | |
| `id_analisis` | `bigint` | FK, NOT NULL | RF-17 |
| `uuid` | `uuid` | FK → `usuario_extension`, NOT NULL | RF-17 |
| `tipo` | `enum(falso_positivo, falso_negativo)` | NOT NULL | RF-17 |
| `motivo` | `text` | NULL | RF-17 |
| `id_modelo_version` | `bigint` | FK, NOT NULL | RF-18 |
| `fecha` | `timestamptz` | NOT NULL | |

Restricción de tabla: `UNIQUE (id_analisis, uuid)`, que es lo que evita el envío repetido del mismo usuario sobre el mismo veredicto.

Se llama `reporte` y no `reporte_falso_positivo` porque RF-17 cubre los dos sentidos del error. La clave foránea a `modelo_version` es lo que permite distinguir un error ya corregido de uno vigente cuando se revisen los reportes acumulados, y es el paso 3 de CU-04.

## Dominio 4 — Trazabilidad del modelo

### `modelo_version`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_modelo_version` | `bigserial` | PK | RF-27 |
| `nombre_checkpoint` | `text` | NOT NULL | RF-27 |
| `fecha_entrenamiento` | `date` | NOT NULL | RF-27 |
| `f1_macro` | `numeric(4,3)` | NULL | RNF-05 |
| `dataset` | `text` | NULL | RF-27 |
| `activo` | `boolean` | NOT NULL | |

### `configuracion_ensamblado`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_config` | `bigserial` | PK | RF-27 |
| `peso_nlp`, `peso_source`, `peso_similarity` | `numeric(3,2)` | NOT NULL | RF-27 |
| `umbral_sospechoso` | `numeric(3,2)` | NOT NULL | RF-08 |
| `umbral_contradicho` | `numeric(3,2)` | NOT NULL | RF-08 |
| `vigente_desde` | `timestamptz` | NOT NULL | RNF-16 |

**Por qué los pesos y los umbrales tienen tabla propia.** Los pesos 0,4 / 0,2 / 0,4 y los umbrales 0,40 y 0,75 no tenían dónde vivir, y RF-27 exige asociar cada análisis a la versión del modelo **y** a la configuración de pesos. La tabla resuelve dos cosas de una vez: RF-27 queda cubierto entero —la versión de modelo cubría solo la mitad— y RNF-16 pasa a ser implementable, porque mover un umbral es insertar una fila y no volver a desplegar el servicio.

Se descartó meter pesos y umbrales como columnas de `modelo_version`: ata dos ciclos de vida distintos al mismo número de versión, y cada ajuste de sensibilidad habría generado una versión de modelo falsa, ensuciando el historial de reentrenamientos que la Entrega 5 necesita limpio.

## Dominio 5 — Plataforma B2B

### `organizacion`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_organizacion` | `bigserial` | PK | RF-20 |
| `nombre` | `text` | NOT NULL | RF-20 |
| `plan` | `enum(free, pro, enterprise)` | NOT NULL | RF-23 |
| `cuota_mensual` | `int` | NOT NULL | RF-23 |
| `id_externo_idp` | `text` | NULL | RF-20 |
| `fecha_alta` | `timestamptz` | NOT NULL | |

### `usuario_b2b`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_usuario` | `bigserial` | PK | RF-20 |
| `id_organizacion` | `bigint` | FK, NOT NULL | RF-20 |
| `email` | `text` | NOT NULL | RF-20 |
| `subject_idp` | `text` | UNIQUE, NOT NULL | RF-20 |
| `rol` | `text` | NOT NULL | RF-20 |
| `fecha_alta` | `timestamptz` | NOT NULL | |

### `api_key`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_api_key` | `bigserial` | PK | RF-21 |
| `id_organizacion` | `bigint` | FK, NOT NULL | RF-21 |
| `hash_clave` | `text` | NOT NULL | RNF-12 |
| `prefijo` | `text` | NOT NULL | RF-21, identificación sin revelar la clave |
| `fecha_emision` | `timestamptz` | NOT NULL | RF-21 |
| `fecha_revocacion` | `timestamptz` | NULL | RF-21 |
| `activa` | `boolean` | NOT NULL | RF-21 |

La clave se almacena hasheada, conforme RNF-12. `prefijo` guarda los primeros caracteres en claro, que es lo que permite mostrarla en el panel y revocar la correcta sin conservar el secreto.

### `consumo_api`

| Atributo | Tipo | Restricción | Origen |
|---|---|---|---|
| `id_consumo` | `bigserial` | PK | RF-23 |
| `id_api_key` | `bigint` | FK, NOT NULL | RF-23 |
| `id_analisis` | `bigint` | FK, NULL | RF-23 |
| `fecha` | `timestamptz` | NOT NULL | RF-23 |
| `endpoint` | `text` | NOT NULL | RF-23 |
| `resultado` | `enum(ok, cuota_agotada, clave_invalida)` | NOT NULL | RF-23 |

`id_analisis` es nulable porque las solicitudes rechazadas —clave inválida o cuota agotada, los flujos alternativos *2a* y *2b* de CU-06— consumen registro pero no producen análisis.

## Cardinalidades

| Relación | Cardinalidad | Nota |
|---|---|---|
| `cuenta` — `tuit` | 1 : N | FK nulable: tras la supresión el tuit queda sin autor |
| `tuit` — `analisis` | 1 : N | Una fila por versión de modelo |
| `tuit` — `claim` | 1 : 0..1 | No todo tuit contiene una afirmación verificable |
| `analisis` — `razon` | 1 : N | RF-09 |
| `razon` — `evidencia` | 0..1 : 1 | Nulable: hay razones que no derivan de evidencia externa |
| `analisis` — `evidencia` | 1 : N | |
| `documento` — `evidencia` | 1 : N | Es lo que hace que un documento sostenga varios análisis |
| `analisis` — `documento` | N : M vía `evidencia` | |
| `fuente_oficial` — `documento` | 1 : N | |
| `medio_confiable` — `documento` | 1 : N | |
| `modelo_version` — `analisis` | 1 : N | RF-27 |
| `configuracion_ensamblado` — `analisis` | 1 : N | RF-27, RNF-16 |
| `usuario_extension` — `analisis` | 0..1 : N | FK nulable: los análisis de CU-06 no tienen instalación |
| `usuario_extension` — `reporte` | 1 : N | |
| `analisis` — `reporte` | 1 : N | `UNIQUE (id_analisis, uuid)`: uno por usuario |
| `modelo_version` — `reporte` | 1 : N | RF-18, paso 3 de CU-04 |
| `organizacion` — `analisis` | 0..1 : N | |
| `organizacion` — `usuario_b2b` | 1 : N | |
| `organizacion` — `api_key` | 1 : N | |
| `api_key` — `consumo_api` | 1 : N | |
| `consumo_api` — `analisis` | N : 0..1 | FK nulable: la solicitud rechazada no produce análisis |

## Matriz de trazabilidad entidad → requerimiento

Es lo que hace verificable la regla de corte. Una entidad sin columna derecha sería una entidad que sobra.

| Entidad | Requerimientos que sostiene | Casos de uso |
|---|---|---|
| `tuit` | RF-01, RF-10, RF-26 | CU-01, CU-02 |
| `cuenta` | RF-01, RF-03, RF-26, RNF-10 | CU-01, CU-02, CU-07 |
| `fuente_oficial` | RF-06 | CU-02 |
| `medio_confiable` | RF-05, RF-13 | CU-02, CU-03 |
| `analisis` | RF-02, RF-08, RF-10, RF-14, RF-26, RF-27 | CU-01, CU-02, CU-06 |
| `razon` | RF-09 | CU-02, CU-03 |
| `claim` | RF-04, RF-07 | CU-02 |
| `documento` | RF-05, RF-06, RF-07, RF-13, RF-26 | CU-02, CU-03 |
| `evidencia` | RF-05, RF-09, RF-13 | CU-02, CU-03 |
| `usuario_extension` | RF-15, RF-17 | CU-04, CU-05 |
| `reporte` | RF-17, RF-18 | CU-04 |
| `modelo_version` | RF-18, RF-27 | CU-01, CU-02, CU-04 |
| `configuracion_ensamblado` | RF-27, RNF-16 | CU-01, CU-02 |
| `organizacion` | RF-20, RF-23 | CU-06, CU-07 |
| `usuario_b2b` | RF-20 | CU-07 |
| `api_key` | RF-21, RNF-12 | CU-06 |
| `consumo_api` | RF-23 | CU-06 |

`medio_confiable` es la única fila que no se sostiene sola en un requerimiento que pida administrarla; su justificación de normalización está arriba, en el dominio 1.

## Decisiones diferidas y ausencias deliberadas

**La política de vigencia del caché.** La columna `analisis.vigente_hasta` existe y queda nulable; el criterio que la puebla —cuánto dura vigente un análisis, y si esa duración depende del tipo de afirmación— corresponde a la Entrega 4, como declara [[wiki/solucion/arquitectura]]. Se escribe como decisión diferida y no como olvido: la columna está, el criterio no.

**No hay entidad `tema`.** RF-24 pide «temas con mayor circulación», que no se deriva de `claim.tipo` —que tiene cinco valores fijos y es un ruteador de fuentes, no una taxonomía temática—. Se resuelve por agregación al vuelo sobre los *claims* del período. Queda escrito para que nadie invente esa tabla más adelante.

**No hay tabla de configuración del ciudadano ni de sesión.** Los umbrales de RF-19 y la desactivación por sitio de RF-16 viven en el almacenamiento local del navegador; el ciudadano no se autentica, así que no hay sesión que persistir.

**No hay planificador ni cola en el modelo de datos.** La ingesta programada es un proceso que corre fuera de la petición y deja su estado en `fuente_oficial.fecha_ultima_ingesta`. No necesita tabla propia.

**No hay entidad para verificadores profesionales.** El corpus de verificaciones previas de RF-07 vive en `documento` con `tipo_fuente = verificador`. La decisión de no acceder al sitio de Chequeado está argumentada en [[wiki/proyecto/restricciones-legales-eticas]].

**El DDL ejecutable no es parte de esta página.** Los tipos declarados acá son los de PostgreSQL, pero la creación de la base, los índices de afinamiento y las migraciones pertenecen al bloque de implementación.

## Referencias cruzadas

- [[wiki/solucion/requerimientos]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/tecnologias]]
- [[wiki/solucion/metodologia-tecnica]]
- [[wiki/proyecto/restricciones-legales-eticas]]
- [[wiki/proyecto/recursos]]
- [[wiki/proyecto/plan-bloque-diseno]]

## Fuentes

- [[raw/clases/Rubrica-EP2-50porciento.pdf]]
