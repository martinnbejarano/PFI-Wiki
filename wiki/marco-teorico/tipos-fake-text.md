---
titulo: Taxonomía de Fake Text — Tipos y Definiciones
tipo: concepto
tags: [marco-teorico, fake-news, misinformacion, desinformacion, taxonomia]
fuentes: ["A Comprehensive Survey of Fake Text Detection on Misinformation and LM-Generated Texts.md", "Fake news detection state-of-the-art review and advances with attention to Arabic language aspects.md"]
actualizado: 2026-04-16
---

# Taxonomía de Fake Text — Tipos y Definiciones

## Clasificación de alto nivel

El "fake text" abarca dos grandes categorías con naturalezas distintas:

```
Fake Text
├── Misinformación (contenido falso, creado por humanos)
└── Texto generado por LM (contenido artificial, creado por IA)
```

La distinción es importante: **la misinformación es falsa en su contenido**; el **texto generado por LM puede ser factualmente correcto pero inauténtico en su origen**.

---

## Misinformación

### Definiciones

| Concepto | Definición | Intencional |
|---|---|---|
| **Misinformación** | Información falsa o imprecisa, diseminada intencional o no intencionalmente (Wu et al.) | No necesariamente |
| **Desinformación** | Información falsa creada deliberadamente para engañar (Hernon & Peter) | Sí |
| **Fake news** | Contenido creado con intención sospechosa o engañosa con potencial de daño social | Sí |
| **Rumores** | Información no verificada que puede ser verdadera, falsa o incierta (Wu et al.) | No necesariamente |
| **Hate speech** | Lenguaje que ataca o denigra a un grupo por características identitarias (Fortuna et al.) | Variable |
| **Reviews falsos** | Reseñas fabricadas para influir en decisiones de compra | Sí |

**Distinción clave misinformación vs. desinformación:**
- Misinformación = falso, puede ser involuntario
- Desinformación = falso + **intención de engañar**

### Tipos por contenido (Albtoush et al.)

| Tipo | Descripción | Ejemplo |
|---|---|---|
| Sátira / parodia | Humor, no intención de engañar | The Onion, Satirewire |
| Clickbait | Titulares exagerados para generar tráfico | "Yellow journalism" |
| Propaganda | Manipulación política/ideológica | Framing selectivo de noticias |
| Hoax | Contenido fabricado que se difunde como verdad | HoaxSlayer |
| Rumores | Afirmaciones no verificadas | Rumores en WhatsApp |

---

## Texto generado por LM

Texto producido por modelos de lenguaje (ChatGPT, Gemini, etc.) que puede **parecer escrito por humanos**.

### Tipos de desafío

| Tipo | Descripción |
|---|---|
| **Spam / Phishing** | Generación masiva de contenido malicioso automatizado |
| **Sesgos múltiples** | El modelo hereda sesgos del corpus de entrenamiento (social, racial, de género) |
| **Deshonestidad académica** | Entregas generadas por IA en contextos educativos |
| **Alucinaciones** | El modelo genera afirmaciones convincentes pero incorrectas |

---

## Dominios de propagación

Fake news aparece en todos los dominios pero con diferente impacto:

| Dominio | Eventos representativos |
|---|---|
| Política | Elecciones (EEUU 2016, Brasil, India), conflictos geopolíticos |
| Salud | COVID-19, crisis nucleares, tratamientos falsos |
| Economía | Crash de acciones (United Airlines), Brexit |
| Desastres naturales | Terremotos en Chile 2010, Turquía-Siria |

**Relevante para el PFI**: el foco es política, economía y sociedad argentina — los tres dominios con mayor impacto de desinformación local.

---

## Ciclo de vida del fake news

```
1. Creación → 2. Diseminación → 3. Detección temprana → 4. Propagación
```

- La **detección temprana** (fase 3) es la más valiosa: evitar la propagación antes de que sea viral
- Una vez en fase 4, el daño es difícil de revertir (studies muestran que las correcciones tienen menos alcance que la noticia falsa original)

---

## Implicancias para el PFI

- El sistema del PFI ataca principalmente **misinformación** (fake news, rumores, desinformación) — no texto generado por LM
- Los dominios objetivo (política, economía, sociedad argentina) son los de mayor riesgo
- La detección temprana en redes sociales es el escenario central del sistema
- La distinción intencionalidad (desinformación vs. misinformación) es relevante pero **el sistema no necesita inferirla** — basta con clasificar si el contenido es verdadero/falso

---

## Referencias cruzadas

- [[wiki/marco-teorico/enfoques-deteccion]]
- [[wiki/estado-del-arte/kwon-jang-2025-survey-fake-text]]
- [[wiki/estado-del-arte/albtoush-2025-arabic-fake-news]]
- [[wiki/proyecto/propuesta]]

## Fuentes

- [[raw/A Comprehensive Survey of Fake Text Detection on Misinformation and LM-Generated Texts.md]]
- [[raw/Fake news detection state-of-the-art review and advances with attention to Arabic language aspects.md]]
