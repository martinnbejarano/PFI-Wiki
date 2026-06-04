---
tipo: dataset
nombre: "CREDBANK"
autores: [Mitra, Tanushree, Gilbert, Eric]
año: 2015
fuente: "Twitter (streaming, oct 2014 – feb 2015)"
paper: "Mitra & Gilbert 2015 — ICWSM 2015"
url-paper: "https://ojs.aaai.org/index.php/ICWSM/article/view/14625"
idioma: inglés
tamaño: "60M+ tweets, 1049 eventos"
clases: "escala de credibilidad (5 niveles)"
tarea: credibilidad-de-tweets
dominio: eventos-noticias-tiempo-real
relevancia: baja
---

# CREDBANK

## Descripción

Corpus de más de 60 millones de tweets agrupados en 1.049 eventos del mundo real, cada uno anotado con credibilidad por 30 anotadores humanos usando crowdsourcing. Recolectado durante 5 meses mediante streaming de Twitter.

## Estructura

- **1.049 eventos** identificados automáticamente a partir del stream
- Cada evento: ~60.000 tweets promedio
- Cada evento anotado por 30 anotadores en escala de credibilidad de 5 niveles

## Escala de credibilidad

1. Muy improbable que sea verdad
2. Improbable que sea verdad
3. No se puede determinar
4. Probable que sea verdad
5. Muy probable que sea verdad

## Limitaciones

- Muy antiguo (2015): el ecosistema de Twitter/X cambió significativamente
- Escala de credibilidad subjetiva, no verificación factual
- No disponible para descarga directa (restricciones de Twitter)

## Relevancia para el PFI

Baja prioridad para el PFI actual. Útil como referencia metodológica para el diseño del pipeline de captura de datos en streaming de Twitter/X. La anotación por crowdsourcing (Amazon Mechanical Turk) puede replicarse para construir el dataset argentino.

**Clave paper biblio:** `MitraGilbert2015`
