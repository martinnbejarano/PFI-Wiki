---
titulo: PHEME Dataset — Rumores en Twitter por Eventos
tipo: dataset
tags: [dataset, pheme, twitter, rumores, veracidad, eventos, ingles]
fuentes: [PHEME-dataset.md]
actualizado: 2026-06-04
---

# PHEME Dataset

PHEME es el dataset estándar para detección de rumores en Twitter organizado por eventos de noticias en tiempo real. A diferencia de LIAR (política americana) o FakeNewsNet (artículos periodísticos), PHEME trabaja con **conversaciones de Twitter** surgidas durante eventos noticiosos.

## Descripción

| Atributo | Valor |
|---|---|
| Año | 2016–2019 (múltiples versiones) |
| Fuente | Twitter + anotación manual |
| Tamaño | ~6.500 tweets fuente (source tweets) |
| Idioma | Inglés |
| Clases | 3: verdadero / falso / no verificado |
| Disponibilidad | Libre (requiere aceptar ToS) |

## Estructura

PHEME está organizado por **9 eventos de noticias** reales:
- Ottawa shooting
- Ferguson unrest
- Sydney siege
- Germanwings crash
- Charlie Hebdo
- Prince Toronto
- Ebola Essien
- Putin missing
- Gurlitt

Para cada evento: tweets fuente + respuestas + hilos de conversación.

## Diferencia con LIAR/FakeNewsNet

| Dataset | Granularidad | Temporalidad | Contexto |
|---|---|---|---|
| LIAR | Claim política | Estática | Perfil del hablante |
| FakeNewsNet | Artículo periodístico | Estática | Red de difusión |
| PHEME | Tweet individual | Dinámica (hilo) | Conversación de respuestas |

La temporalidad dinámica de PHEME permite estudiar **cómo evoluciona la veracidad de un rumor** a medida que se desarrolla el evento.

## Limitaciones

- Solo 9 eventos: cobertura temática limitada
- Solo inglés
- El esquema de 3 clases incluye "no verificado" (ambigüedad difícil de manejar en clasificación)
- Antigüedad: eventos de 2014–2016

## Relevancia para el PFI

Relevancia media. PHEME es útil si el PFI incluye análisis de conversaciones de Twitter (hilos de respuestas como señal de veracidad). El patrón "cómo responden los usuarios a una noticia sospechosa" es una señal complementaria al análisis del texto de la noticia misma.

Limitado por no tener datos en español.

**Clave biblio**: `Zubiaga2016` (paper principal del dataset)

## Referencias cruzadas
- [[comparacion-datasets]]
- [[fakenewsnet]]

## Fuentes
- [[raw/datasets/PHEME-dataset.md]]
