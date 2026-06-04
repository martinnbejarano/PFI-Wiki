---
tipo: dataset
nombre: "PHEME"
autores: [Zubiaga, Arkaitz, et al.]
año: 2016
actualizacion: 2018
fuente: "Twitter (9 eventos de noticias de última hora)"
paper: "Zubiaga et al. 2016 — figshare"
url-descarga: "https://figshare.com/articles/dataset/PHEME_dataset_for_Rumour_Detection_and_Veracity_Classification/6392078"
url-recursos: "https://www.zubiaga.org/datasets/"
idioma: inglés
tamaño: ~6500-tweets-version-extendida
clases: 3
tarea: deteccion-rumores-veracidad
dominio: noticias-de-ultima-hora
relevancia: media
---

# PHEME Dataset

## Descripción

Colección de rumores y no-rumores de Twitter alrededor de 9 eventos de noticias de última hora. Cada tweet está categorizado como rumor o no-rumor, y los rumores tienen anotación de veracidad. El dataset captura la estructura conversacional (reply threads) de cada rumor.

## Eventos cubiertos (9)

1. Charlie Hebdo shooting (2015)
2. Ferguson unrest (2014)
3. Germanwings crash (2015)
4. Ottawa shooting (2014)
5. Sydney siege (2014)
6. ebola (2014)
7. gurlitt (2013)
8. prince_toronto (2012)
9. putinmissing (2015)

## Etiquetas

| Etiqueta | Descripción |
|---|---|
| True | Rumor verificado como verdadero |
| False | Rumor verificado como falso |
| Unverified | Estado de veracidad no confirmado |

**Anotaciones adicionales por tweet:** soporte (¿el tweet apoya, niega o consulta el rumor?), certeza, evidencialidad.

## Tamaño

- ~6.500 tweets en versión extendida (9 eventos)
- ~1.972 rumores anotados

## Limitaciones

- Solo inglés; eventos mayormente del mundo anglosajón
- Los eventos son específicos de un período (2012–2015)
- La proporción de rumores verificables es baja respecto al total de tweets

## Relevancia para el PFI

Útil como referencia para modelos de detección temprana de rumores (antes de que sean verificados) y para sistemas de stance detection (¿el tweet apoya o niega la afirmación?). Si el PFI incorpora análisis de respuestas/comentarios a noticias en redes sociales, PHEME es el benchmark de referencia.

**Clave paper biblio:** `ZubiagaEtAl2016`
