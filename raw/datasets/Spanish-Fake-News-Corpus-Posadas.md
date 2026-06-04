---
tipo: dataset
nombre: "Spanish Fake News Corpus / FakeDeS"
autores: [Posadas-Durán, Juan Pablo, Gómez-Adorno, Helena, Sidorov, Grigori, Escobar, Juan Jesús Martínez]
año: 2019
actualizacion: "2021 (FakeDeS @ IberLEF)"
fuente: "Sitios web de noticias mexicanos y españoles + sitios de fact-checking"
paper-original: "Posadas-Durán et al. 2019 — J. Intelligent & Fuzzy Systems — DOI: 10.3233/JIFS-179015"
paper-shared-task: "Gómez-Adorno et al. 2021 — IberLEF 2021 — Procesamiento del Lenguaje Natural"
url-github: "https://github.com/jpposadas/FakeNewsCorpusSpanish"
idioma: español
tamaño: 971
clases: 2
tarea: clasificacion-binaria
dominio: multidominio
relevancia: alta
---

# Spanish Fake News Corpus (FakeDeS)

## Descripción

El corpus en español para detección de fake news más utilizado en la literatura académica. Primera versión de 2019 con 971 noticias; extendido para el shared task FakeDeS en IberLEF 2021.

## Estructura

- **491 noticias reales**: extraídas de medios de comunicación verificados
- **480 noticias falsas**: extraídas de sitios de desinformación y redes sociales

## Temáticas cubiertas (9)

Ciencia, Deporte, Economía, Educación, Entretenimiento, Política, Salud, Seguridad, Sociedad.

## Splits (FakeDeS 2021)

| Conjunto | Tamaño |
|---|---|
| Entrenamiento | ~700 noticias |
| Desarrollo | ~100 noticias |
| Test | ~171 noticias |

## Limitaciones críticas

- **971 muestras totales**: extremadamente pequeño vs. LIAR (12.836) o Fakeddit (1M+)
- Contexto México y España: diferencias de vocabulario político y cultural con Argentina
- Sin contexto social (no incluye tweets, propagación ni metadata de redes sociales)
- Las fuentes de noticias falsas no cubren los principales medios argentinos
- Actualizado en 2019–2021: no cubre eventos recientes

## Resultados en FakeDeS 2021 (mejores equipos)

Los mejores sistemas en el shared task usaron transformers (BETO, XLM-RoBERTa) con F1 ~0.80 en el subset más difícil.

## Relevancia para el PFI

**El corpus de referencia más cercano en español.** Evidencia del gap: el dataset más usado en español tiene 971 muestras; esta escasez justifica la construcción de un corpus argentino como contribución del PFI. Los temas cubiertos (política, economía, salud) se superponen con el dominio objetivo del sistema.

**Clave paper biblio:** `PosadasEtAl2019`
