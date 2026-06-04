---
tipo: dataset
nombre: "MultiFC"
autores: [Augenstein, Isabelle, Lioma, Christina, Wang, Dongsheng, Lima, Lucas Chaves, Hansen, Casper, Hansen, Christian, Simonsen, Jakob Grue]
año: 2019
fuente: "26 sitios web de fact-checking en inglés"
paper: "Augenstein et al. 2019 — EMNLP-IJCNLP 2019 — arXiv:1909.03242"
url-paper: "https://aclanthology.org/D19-1475/"
url-dataset: "https://copenlu.github.io/publication/2019_emnlp_augenstein/"
idioma: inglés
tamaño: 34918
clases: "variable (2–38 según la fuente)"
tarea: fact-checking-multi-dominio
dominio: multi-dominio
relevancia: media
---

# MultiFC (Multi-Domain Fact-Checking)

## Descripción

Dataset de 34.918 claims reales provenientes de 26 sitios web de fact-checking en inglés, con metadatos ricos y fuentes textuales de evidencia. Cada claim tiene la etiqueta de veracidad del sitio original, texto de justificación y link a evidencias.

## Fuentes (muestra)

PolitiFact, Snopes, FactCheck.org, The Washington Post Fact Checker, AFP Fact Check, etc.

## Estructura

| Campo | Descripción |
|---|---|
| Claim | Afirmación textual |
| Etiqueta | Veracidad según el fact-checker (multi-clase) |
| Fuente | Sitio web de origin |
| Evidencia | Links a artículos de evidencia |
| Metadata | Fecha, autor, temática |

## Desafío

Las etiquetas son heterogéneas entre fuentes (PolitiFact usa 6 clases, Snopes usa "true/false/mixture/unproven", etc.). Normalizar a 2 clases reduce información; mantener las originales genera problema de 38 clases.

## Limitaciones

- Solo inglés
- Las etiquetas no son consistentes entre fuentes
- Requiere normalización para experimentos comparables

## Relevancia para el PFI

Evidencia de que el fact-checking multi-dominio y multi-clase es un problema abierto. Si el sistema del PFI incorpora múltiples fuentes de fact-checking (Chequeado + La Nación Verificación + otros), MultiFC es el referente de cómo manejar etiquetas heterogéneas.

**Clave paper biblio:** `AugensteinEtAl2019`
