---
titulo: Resumen del PFI
tipo: proyecto
tags: [overview, pfi, uade]
actualizado: 2026-04-13
---

# Proyecto Final de Ingeniería — Resumen

## Datos del proyecto

| Campo | Valor |
|---|---|
| Universidad | UADE — Facultad de Ingeniería y Ciencias Exactas |
| Carrera | Ingeniería en Informática |
| Año | 2026 |
| Tutor | Monzón, Nicolás Alberto |
| Tipo | Desarrollo |
| Tema troncal | Inteligencia Artificial |
| Nombre del proyecto | Sistema de Detección Automática de Desinformación en Redes Sociales |
| Integrantes | Juan Martín Bejarano Arce |

## Descripción del proyecto

Sistema que detecta automáticamente contenido desinformativo publicado en redes sociales, combinando técnicas de NLP (procesamiento de lenguaje natural) con modelos de machine learning. El objetivo es clasificar posts/artículos según su veracidad, apuntando a ser un MVP validado con usuarios reales.

## Objetivo general

Desarrollar un servicio que, mediante la aplicación de técnicas de procesamiento del lenguaje natural e inteligencia artificial, facilite a ciudadanos argentinos la identificación de contenido potencialmente desinformativo en redes sociales y medios digitales, permitiéndoles tomar decisiones informadas sobre la veracidad del contenido que consumen y comparten, en Argentina durante el año 2026.

## Objetivos específicos

1. Diseñar e implementar un modelo de clasificación de texto basado en arquitectura Transformer (BETO o XLM-RoBERTa) fine-tuneado para detectar indicadores lingüísticos de desinformación en publicaciones en español.
2. Implementar un módulo que evalúe metadatos de la cuenta o medio publicante (antigüedad, verificación, historial) para complementar el análisis textual con un score de credibilidad de fuente.
3. Implementar un módulo de contraste semántico contra un corpus de fuentes confiables (medios verificados, cuentas oficiales, verificaciones de Chequeado.com) usando búsqueda de similitud vectorial.
4. Desarrollar una extensión de Google Chrome que integre los tres módulos y permita al usuario analizar contenido en tiempo real, mostrando un score de confiabilidad con evidencia asociada.
5. Desarrollar un panel web (dashboard) con historial de análisis y estadísticas por usuario.
6. Construir o adaptar un dataset de entrenamiento en español con foco en contenido argentino/latinoamericano.
7. Evaluar el sistema con métricas estándar (Accuracy, Precision, Recall, F1, AUC-ROC) y validar con usuarios reales.

## Alcance

**Plataformas:** Twitter/X, Instagram, Facebook, Infobae.com, Clarín.com, etc.
**Temática:** Política, economía y sociedad argentina (2026)
**Idioma:** Español (variante rioplatense/argentina)
**Interfaz principal:** Extensión de Google Chrome
**Entregables:** Extensión Chrome + modelo publicado en HuggingFace + dashboard web

**Fuera del alcance:** apps móviles, análisis multimedia (solo texto), grafos de propagación, otros idiomas, otras plataformas, streaming a escala, otros navegadores.

## Estado actual

- [x] Tema elegido
- [ ] Propuesta aprobada por tutor
- [ ] Marco teórico iniciado
- [ ] Estado del arte iniciado
- [ ] Análisis competitivo iniciado
- [ ] User research iniciado
- [ ] Solución definida
- [ ] Arquitectura diseñada
- [ ] MVP implementado
- [ ] Pruebas realizadas
- [ ] Documento final entregado

## Referencias cruzadas

- [[wiki/proyecto/propuesta]]
- [[wiki/proyecto/cronograma]]
- [[wiki/proyecto/reuniones]]
