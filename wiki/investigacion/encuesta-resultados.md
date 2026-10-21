---
titulo: Encuesta de user research — resultados
tipo: análisis
tags: [user-research, encuesta, resultados, validacion]
fuentes: [encuesta-desinformacion-v2.xlsx]
actualizado: 2026-10-20
---

# Encuesta de user research — resultados

Resultados de la encuesta diseñada en [[wiki/investigacion/user-research]]. Buscaba validar cuatro cosas antes de comprometer el desarrollo: que el segmento se topa con desinformación en Twitter/X, que le cuesta detectarla por su cuenta, que hoy verifica de forma insuficiente, y que instalaría y confiaría en una extensión que le devuelva un puntaje con evidencia.

> Desde 2026-10-20 la fuente es la planilla v2 (152 respuestas), que reemplaza a la primera versión (140). Por pedido del tutor, en el documento la sección quedó breve: ficha mínima, hallazgos y figuras, sin la descripción del método de recolección.

## Ficha

| | |
|---|---|
| **Respuestas** | **152** |
| **Dentro del segmento** | **116** (76,3 %): 18 a 40 años, usa Twitter/X y sigue política o economía en la plataforma |
| **Preguntas** | 14 (perfil, exposición, capacidad y comportamiento, apetito y confianza) |
| **Pregunta abierta respondida** | 38 de 152 (29 del segmento) |
| **Fuente de datos** | `raw/investigacion/encuesta-desinformacion-v2.xlsx` |
| **Script** | `scripts/analizar_encuesta.py` (genera figuras, tablas del anexo y cifras derivadas) |

**Base.** Las preguntas 1 a 3 se computan sobre las 152 respuestas porque definen el filtro. De la 4 en adelante la base es n = 116: quedan fuera quienes tienen menos de 18 o más de 40 años (11), no usan Twitter/X o no siguen noticias de política ni economía.

---

## Bloque A — Perfil y filtro (n = 152)

**Edad.** 18-25: 58,6 % (89) · 26-33: 27,6 % (42) · 34-40: 6,6 % (10) · Más de 40: 5,3 % (8) · Menos de 18: 2,0 % (3). El **92,8 %** cae en la franja de 18 a 40.

**Uso de Twitter/X.** Varias veces al día: 34,2 % (52) · Una vez al día: 27,6 % (42) · Algunas veces por semana: 27,0 % (41) · Rara vez: 8,6 % (13) · No la uso: 2,6 % (4). El **61,8 %** entra al menos una vez por día.

**Sigue política o economía.** Sí, frecuentemente: 39,5 % (60) · A veces: 46,1 % (70) · No: 14,5 % (22). En total, **85,5 %**.

## Bloque B — Exposición al problema (n = 116)

| Frecuencia de exposición | n | % |
|---|---:|---:|
| Muy frecuentemente | 50 | 43,1 % |
| Frecuentemente | 37 | 31,9 % |
| A veces | 16 | 13,8 % |
| Rara vez | 7 | 6,0 % |
| Nunca | 6 | 5,2 % |

El **75,0 %** se cruza con desinformación de forma frecuente o muy frecuente.

**Contacto personal.** 35,3 % (41) compartió contenido que resultó falso o dudoso y 26,7 % (31) estuvo a punto. Sumados, **62,1 %**. No: 25,9 % · No sé: 12,1 %.

**Preocupación** (1 a 5, media **4,22**): 5 → 44,0 % · 4 → 37,9 % · 3 → 14,7 % · 2 → 3,4 % · 1 → 0 %. El **81,9 %** en los dos valores altos. Por exposición, la media va de 4,44 ("muy frecuentemente") a 3,69 ("a veces"): la inquietud es transversal.

## Bloque C — Capacidad y comportamiento (n = 116)

**Capacidad autopercibida** (1 a 5, media **3,57**): 5 → 21,6 % · 4 → 33,6 % · 3 → 27,6 % · 2 → 14,7 % · 1 → 2,6 %. El 44,8 % se ubica en el punto medio o por debajo.

> **Brecha preocupación/capacidad:** 4,22 contra 3,57. El segmento está más preocupado de lo que se siente equipado.

| Qué hace ante una publicación dudosa | n | % |
|---|---:|---:|
| Busco en Google | 95 | 81,9 % |
| Miro la cuenta que lo publicó | 81 | 69,8 % |
| Comparo con medios que conozco | 55 | 47,4 % |
| Le pregunto a alguien | 46 | 39,7 % |
| Nada, sigo de largo | 7 | 6,0 % |
| Leo los comentarios o las notas de la comunidad | 1 | 0,9 % |
| Lo busco en X con otras palabras | 1 | 0,9 % |

Las dos conductas dominantes replican dos módulos del sistema (contraste web y credibilidad de la fuente).

**Tiempo de verificación.** Menos de 1 minuto: 35,3 % (41) · 1-3 minutos: 40,5 % (47) · Más de 3 minutos: 17,2 % (20) · No verifico: 6,9 % (8). El **75,9 %** resuelve en menos de tres minutos → RNF de latencia en [[wiki/solucion/requerimientos]].

## Bloque D — Apetito y confianza (n = 116)

**Intención de uso** (media **4,09**): 5 → 42,2 % · 4 → 35,3 % · 3 → 13,8 % · 2 → 6,0 % · 1 → 2,6 %. **77,6 %** en los dos valores altos.

**Confianza en el puntaje automático** (media **3,58**): 5 → 24,1 % · 4 → 33,6 % · 3 → 24,1 % · 2 → 12,1 % · 1 → 6,0 %. **57,8 %** en los dos valores altos.

> **Hallazgo principal — brecha intención/confianza (0,51 puntos).** Quieren la herramienta pero no le creen del todo al número: el puntaje nunca va solo, la evidencia y la explicación son obligatorias.

| Capacidad autopercibida | n | Confianza media | Intención media |
|---|---:|---:|---:|
| 1 | 3 | 4,00 | 3,33 |
| 2 | 17 | 3,76 | 4,47 |
| 3 | 32 | 3,62 | 4,22 |
| 4 | 39 | 3,51 | 4,10 |
| 5 | 25 | 3,44 | 3,72 |

La confianza baja de forma monótona con la capacidad autopercibida (4,00 → 3,44); la intención es máxima en el escalón 2 (4,47). Los extremos tienen pocos casos.

| Qué generaría más confianza | n | % |
|---|---:|---:|
| Que no tenga sesgo político | 96 | 82,8 % |
| Que muestre las fuentes/evidencia | 77 | 66,4 % |
| Que explique por qué llega a ese resultado | 57 | 49,1 % |
| Que sea transparente sobre su margen de error | 43 | 37,1 % |
| Que la respalde una institución reconocida | 35 | 30,2 % |
| Que sea *open source* | 4 | 3,4 % |

| Mayor preocupación | n | % |
|---|---:|---:|
| Que se equivoque (falsos positivos) | 75 | 64,7 % |
| Que censure opiniones o sátira | 65 | 56,0 % |
| Sesgo político | 57 | 49,1 % |
| Privacidad de mis datos | 39 | 33,6 % |
| Ninguna | 3 | 2,6 % |
| Que se vuelva paga | 3 | 2,6 % |
| Que ande lento | 1 | 0,9 % |

> **Neutralidad política:** primer atributo de confianza (82,8 %, 16,4 puntos sobre el segundo) y tercera preocupación (49,1 %). Consecuencias: clasificar afirmaciones fácticas y no opiniones, exponer siempre la evidencia y comunicar en términos probabilísticos.

## Pregunta abierta

38 respuestas sobre 152 (29 del segmento). Los temas se agrupan por texto idéntico o por igual pedido; el script lista qué respuestas entran en cada uno, así que el conteo es verificable.

| Tema | Total (38) | Segmento (29) |
|---|---:|---:|
| Detectar imágenes generadas con IA | 4 | 3 |
| Avisar si un contenido viejo recircula como nuevo | 3 | 3 |
| Mostrar las fuentes o la evidencia | 3 | 2 |
| No recargar la pantalla | 3 | 1 |
| Contrastar más de una fuente o postura | 2 | 2 |
| Distinguir opinión o sátira de un dato falso | 2 | 2 |
| Ahorrar el tiempo de buscar en Google | 2 | 2 |
| Avisar de títulos *clickbait* | 2 | 2 |
| Efectividad | 2 | 2 |
| Facilidad de uso | 2 | 1 |
| Otras (una mención cada una) | 7 | 3 |
| Sin un pedido concreto | 6 | 6 |

Ningún pedido pasa de cuatro menciones, así que no conviene llamar «recurrente» a nada. La cita de la persona 1 es textual: «Que me muestre las fuentes en el momento» (la respuesta no pertenece al segmento).

---

## Insights y su traducción a decisiones

| # | Insight | Evidencia | Consecuencia |
|---|---|---|---|
| 1 | El problema existe y es percibido | 75,0 % de exposición frecuente; 62,1 % compartió o casi | Valida [[wiki/proyecto/contexto-problema]] con datos propios |
| 2 | Brecha preocupación (4,22) / capacidad (3,57) | Bloques B y C | Justifica el producto |
| 3 | Verificación superficial | 75,9 % en menos de 3 minutos | RNF de latencia |
| 4 | Ya googlean y miran la cuenta | 81,9 % y 69,8 % | Confirma los módulos de contraste web y credibilidad de la fuente |
| 5 | Quieren la herramienta pero desconfían del puntaje | Intención 4,09 vs. confianza 3,58 | Evidencia + explicación obligatorias |
| 6 | Neutralidad política como condición de aceptación | 82,8 % driver; 49,1 % + 56,0 % preocupación | Hechos y no opiniones; lenguaje probabilístico |
| 7 | El falso positivo es la falla que más pesa | 64,7 % | Priorizar precisión en el umbral; [[wiki/solucion/pruebas]] |
| 8 | La gratuidad no es un diferencial percibido | 2,6 % teme que se vuelva paga | El *freemium* de [[wiki/negocio/modelo-de-negocio]] no encuentra resistencia |

## Limitaciones

1. **Muestreo no probabilístico**: describe a las personas alcanzadas, no al universo de usuarios argentinos de X.
2. **Sesgo etario**: 58,6 % entre 18 y 25; solo 10 respuestas en 34-40.
3. **Intención declarada, no conducta.**
4. **Capacidad autopercibida**, no medida.
5. **Deseabilidad social**: el 35,3 % que admite haber compartido es probablemente un piso.
6. **Pocas respuestas abiertas**: 38 de 152.

## Referencias cruzadas

- [[wiki/investigacion/user-research]] — diseño del instrumento y personas
- [[wiki/proyecto/contexto-problema]] — estadísticas que esta encuesta valida localmente
- [[wiki/solucion/requerimientos]] — RNF de latencia, evidencia y explicabilidad
- [[wiki/solucion/pruebas]] — peso del falso positivo
- [[wiki/negocio/modelo-de-negocio]] — apetito y esquema gratuito
- [[wiki/competencia/analisis-competitivo]] — océano azul y matriz ERIC

## Fuentes

- [[raw/investigacion/encuesta-desinformacion-v2.xlsx]] — planilla de respuestas (152)
