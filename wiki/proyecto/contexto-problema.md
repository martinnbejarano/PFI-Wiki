---
titulo: Contexto del Problema — Desinformación en Argentina
tipo: proyecto
tags: [contexto, problema, argentina, estadisticas, desinformacion, ia-generativa]
fuentes: ["Reuters Institute Digital News Report 2024"]
actualizado: 2026-04-16
---

# Contexto del Problema — Desinformación en Argentina

## Narrativa base (para usar en la Descripción del PFI)

Argentina enfrenta una crisis de desinformación sostenida. Según el **Digital News Report 2024 del Reuters Institute** — relevado para Argentina por La Nación — solo el **30% de la población confía en los medios**, el nivel más bajo de América Latina, y el interés en noticias colapsó del **77% en 2017 al 45% en 2024**. A esto se suma un vector de crecimiento exponencial: el contenido generado por inteligencia artificial. En los últimos años, deepfakes de figuras políticas, imágenes sintéticas y videos manipulados se han consolidado como una de las formas más extendidas y difíciles de detectar de desinformación, con presencia creciente en los ciclos electorales recientes.

---

## Estadísticas verificadas

### Confianza en medios y consumo de noticias

| Indicador | Valor | Fuente |
|---|---|---|
| Confianza en noticias (Argentina) | **30%** — menor de América Latina | Reuters Institute DNR 2024 |
| Confianza en noticias (Brasil, referencia regional) | 45% | Reuters Institute DNR 2024 |
| Interés en noticias (Argentina 2024) | 45% | Reuters Institute DNR 2024 |
| Interés en noticias (Argentina 2017) | 77% | Reuters Institute DNR 2024 |
| Descenso de interés en 7 años | −32 puntos porcentuales | Reuters Institute DNR 2024 |

**Cobertura local:** La Nación — *Digital News Report 2024: un nuevo informe del Instituto Reuters describe el estado de los medios en la Argentina y el mundo* (junio 2024)

### Penetración digital (contexto del problema)

| Indicador | Valor | Fuente |
|---|---|---|
| Usuarios de redes sociales en Argentina | 31.3 millones (68.2% de la población) | We Are Social / Meltwater 2024 |
| Penetración de WhatsApp | 93% de usuarios de internet | We Are Social / Meltwater 2024 |
| Usuarios de Instagram | 27.85 millones | We Are Social / Meltwater 2024 |

WhatsApp es el principal vector de difusión de desinformación en Argentina por su altísima penetración y la naturaleza viral de sus cadenas.

### Desinformación electoral

- **Balotaje 2023**: videos falsos sobre irregularidades en el conteo provisional circularon en redes durante las elecciones presidenciales
- **Elecciones 2025**: deepfakes de figuras políticas (Macri, Lospennato, De Loredo/Llaryora) viralizados durante el silencio electoral — casos documentados y verificados

### IA generativa como nuevo vector (2024-2025)

El surgimiento de herramientas de IA generativa (imágenes, videos, texto) introdujo un vector nuevo de desinformación:
- **Deepfakes de figuras políticas**: video y audio sintético indistinguible, usado en campañas electorales
- **"AI slop"**: contenido masivo de baja calidad generado con IA, diseñado para capturar atención rápida, sin indicar origen sintético
- **Escalabilidad**: la IA permite generar desinformación a una velocidad y volumen imposibles para la verificación manual

Este vector es cualitativamente distinto al fake news textual tradicional y aún no está contemplado en la mayoría de los sistemas de detección existentes.

---

## Por qué Argentina específicamente

1. **Crisis de confianza documentada**: la caída sostenida (2017→2024) indica un problema estructural, no coyuntural
2. **Alta penetración de redes**: 68.2% de la población en redes sociales — el daño de la desinformación es proporcional al alcance
3. **WhatsApp como vector dominante**: difusión privada, cifrada, sin moderación algorítmica — las plataformas no pueden detectarla
4. **Ciclos electorales recurrentes**: 2023 (presidenciales), 2025 (legislativas) — la desinformación electoral es el caso de uso de mayor impacto inmediato
5. **Ausencia de herramientas locales**: no existe un sistema automático gratuito orientado al ciudadano argentino
6. **Idioma**: el español rioplatense no está bien representado en modelos genéricos entrenados en inglés

---

## Limitación de las soluciones actuales

- **Chequeado.com**: fact-checking manual de alta calidad, pero no escala — solo puede verificar un subconjunto pequeño de afirmaciones
- **Soluciones comerciales** (Cyabra, Blackbird.AI, Newtral FactFlow): orientadas a gobiernos y redacciones, no accesibles al ciudadano común
- **Detectores genéricos**: entrenados en inglés, sin contexto local, sin capacidad de citar evidencia

---

## Implicancias para el PFI

- El **contexto del problema justifica el foco en Argentina**: la crisis de confianza + alta penetración de redes + vacío de herramientas locales es el escenario central
- La IA generativa como vector nuevo justifica incluir mención explícita en el alcance futuro (aunque el MVP se enfoca en texto)
- Las **elecciones como caso de uso** son el ejemplo más concreto y documentado del impacto de la desinformación local

---

## Referencias cruzadas

- [[wiki/proyecto/propuesta]]
- [[wiki/competencia/analisis-competitivo]]
- [[wiki/marco-teorico/tipos-fake-text]]
- [[wiki/estado-del-arte/albtoush-2025-arabic-fake-news]]

## Fuentes

- Reuters Institute — Digital News Report 2024: https://reutersinstitute.politics.ox.ac.uk/es/digital-news-report/2024
- La Nación — cobertura DNR 2024: https://www.lanacion.com.ar/sociedad/digital-news-report-2024-un-nuevo-informe-del-instituto-reuters-describe-el-estado-de-los-medios-en-nid16062024/
- We Are Social / Meltwater — Digital 2024 Argentina
