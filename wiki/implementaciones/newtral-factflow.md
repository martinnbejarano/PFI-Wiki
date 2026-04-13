---
titulo: Newtral FactFlow — Fact-checking automatizado en español con LLM
tipo: entidad
tags: [implementacion, competencia, espanol, fact-checking, telegram, llm, qwen, latam, profesional]
fuentes: []
actualizado: 2026-04-13
---

# Newtral FactFlow

## Qué es

Herramienta de **detección automática de desinformación en Telegram**, desarrollada por Newtral (empresa española especializada en fact-checking con contratos de verificación con La Sexta, Antena 3, etc.). Actualmente disponible solo para académicos y fact-checkers de Newtral, con planes de expansión a otras redacciones y plataformas.

- Organización: Newtral Media Audiovisual (España)
- HuggingFace: https://huggingface.co/Newtral
- Financiamiento: Horizonte 2020 (Comisión Europea), proyecto CORDIS ID 855556
- Tipo: cerrado / profesional (no open-source)

## Qué hace

| Capacidad | Descripción |
|---|---|
| Monitoreo de Telegram | Analiza en tiempo real miles de canales y cuentas sospechosas |
| Detección de patrones de desinformación | Identifica "linguistic cues" (señales lingüísticas) asociadas a desinformación |
| Dashboard de verificación | Muestra narrativas relevantes, contenido ya verificado, alertas |
| Multimodal | Detecta desinformación en texto, audio, video e imágenes |
| Personalización | Los fact-checkers pueden definir qué canales monitorear |

## Modelo y datos de entrenamiento

- **Modelo base**: Qwen (LLM open-source)
- **Entrenamiento**: 1 millón+ de mensajes recolectados por fact-checkers de Newtral desde 2.000+ cuentas y canales sospechosos de Telegram
- **Idioma**: ~70% del contenido procesado está en español
- **Escala**: 10 millones de registros procesados, 125.000+ mensajes flaggeados

## Impacto medido

- Reduce a **segundos** el tiempo que los fact-checkers dedican a monitorear desinformación viral
- Ha procesado más de 10 millones de registros en Telegram
- Flaggeó 125.000+ mensajes con indicios de desinformación

## Expansión planeada

- Integración con **TikTok** y **X (Twitter)** — hoy solo cubre Telegram
- Escalar a otras redacciones fuera de Newtral

## Relevancia para el PFI

### Es el competidor más directo en español

FactFlow hace exactamente lo que el PFI apunta a hacer: detección automática de desinformación en redes sociales, en español, con IA. La diferencia es que está limitado a Telegram y a organizaciones profesionales (no es un producto de consumo masivo).

**Espacio diferencial del PFI**: plataformas más masivas (Twitter/X, Instagram, Facebook), accesible a usuarios comunes (no solo fact-checkers profesionales), contexto latinoamericano específico (Argentina, región).

### Uso de Qwen como LLM base

Qwen es un LLM de Alibaba, open-source. El hecho de que Newtral lo haya elegido frente a GPT-4 u otros modelos de OpenAI sugiere:
1. Puede ser más eficiente para español con fine-tuning adecuado
2. Es reproducible y no depende de APIs de pago
3. Se puede hostear en servidores propios (importante para privacidad)

**Para el PFI**: explorar Qwen como alternativa a BERT/RoBERTa para el módulo de análisis de texto.

### Señal lingüística vs. verificación factual

FactFlow detecta "patrones lingüísticos de desinformación" — señales en el lenguaje que correlacionan con contenido falso (urgencia artificial, apelaciones emocionales, afirmaciones sin fuente, etc.). No verifica contra bases de hechos externas.

Esto es similar al enfoque de clasificación supervisada del PFI: aprender del lenguaje de la desinformación, no buscar cada claim en una base de hechos.

### Dataset implícito valioso

Los 1 millón+ de mensajes de Telegram etiquetados por fact-checkers de Newtral son un dataset en español de alta calidad. **No está disponible públicamente**, pero demuestra que construir datasets en español con fact-checkers locales es el camino correcto.

**Para el PFI**: considerar si existe algo similar para Argentina (Chequeado.com podría ser el equivalente local).

## Diferencias con el PFI

| Dimensión | Newtral FactFlow | PFI (tentativo) |
|---|---|---|
| Plataforma | Telegram únicamente | Twitter/X, Instagram, otras (TBD) |
| Audiencia | Fact-checkers profesionales | Usuarios finales (ciudadanos) |
| Acceso | Cerrado, solo por invitación | Abierto (MVP académico) |
| Idioma | Español (principalmente España) | Español (foco LATAM/Argentina) |
| Financiamiento | EU Horizon 2020 + empresa | Proyecto académico UADE |
| Modelo | Qwen fine-tuned | Por definir (BERT/RoBERTa/LLM) |

## Limitaciones observadas

- Código no público — no hay nada que estudiar técnicamente
- Foco en Telegram limita el alcance actual
- Orientado a redacciones profesionales, no a usuarios finales
- No está claro si los modelos de HuggingFace de Newtral son los usados en FactFlow

## Recurso adicional

Newtral tiene una presencia activa en HuggingFace (https://huggingface.co/Newtral) con modelos para NLP en español que podrían ser útiles para el PFI, independientemente de FactFlow.

## Referencias cruzadas

- [[wiki/implementaciones/implementaciones-overview]]
- [[wiki/competencia/analisis-competitivo]]
- [[wiki/modelos/modelos-overview]]
- [[wiki/investigacion/user-research]]
