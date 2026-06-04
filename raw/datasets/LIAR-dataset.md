---
tipo: dataset
nombre: "LIAR"
autores: [Wang, William Yang]
año: 2017
fuente: "PolitiFact.com (2007–2016)"
paper: "Wang 2017 — ACL 2017 — DOI: 10.18653/v1/P17-2067"
url-descarga: "https://www.cs.ucsb.edu/~william/data/liar_dataset.zip"
url-paper: "https://aclanthology.org/P17-2067/"
idioma: inglés
tamaño: 12836
clases: 6
tarea: clasificacion-veracidad
dominio: politica
relevancia: alta
---

# LIAR Dataset

## Descripción

Benchmark de referencia para fake news detection. Contiene 12.836 declaraciones cortas extraídas de PolitiFact.com durante una década. Cada declaración está anotada con una de 6 etiquetas de veracidad y acompañada de 12 features de metadata sobre el hablante.

## Estructura

| Campo | Descripción |
|---|---|
| Etiqueta de veracidad | pants-fire / false / barely-true / half-true / mostly-true / true |
| Declaración | Texto corto de la afirmación (promedio ~20 palabras) |
| Sujeto | Tema de la declaración (economía, salud, etc.) |
| Hablante | Nombre del político o figura pública |
| Cargo | Cargo actual del hablante |
| Partido | Partido político del hablante |
| Estado | Estado de EEUU del hablante |
| Contexto | Dónde se hizo la declaración (debate, entrevista, etc.) |
| Historial | Conteo histórico de declaraciones verdaderas, falsas, etc. del mismo hablante |

## Distribución de etiquetas

| Etiqueta | Proporción |
|---|---|
| true | ~18% |
| mostly-true | ~21% |
| half-true | ~21% |
| barely-true | ~17% |
| false | ~19% |
| pants-fire | ~4% |

## Splits

- Train: 10.269 ejemplos
- Validation: 1.284 ejemplos
- Test: 1.267 ejemplos

## Resultados de referencia en la literatura

| Modelo | Accuracy (6 clases) |
|---|---|
| CNN híbrida (baseline Wang 2017) | 27.4% |
| SVM lineal (Hasan 2025) | 62.4% |
| RoBERTa (Hasan 2025) | 62.0% |
| RoBERTa+BiGRU (binario simplificado) | 99.04% |

El techo real para 6 clases con modelos puros es ~62%. Superar esto requiere conocimiento externo.

## Limitaciones

- Solo inglés; fuente única (PolitiFact → sesgo político US)
- Declaraciones cortas sin contexto adicional
- No incluye datos de propagación en redes sociales
- Desbalance entre clases (pants-fire es raro)

## Relevancia para el PFI

Benchmark de referencia obligatorio. Los resultados del PFI deben compararse contra este dataset (aunque sea en cross-lingual) para tener posición en la literatura internacional. El techo bajo en 6 clases (62%) justifica la arquitectura con evidence retrieval.

**Clave paper biblio:** `Wang2017`
