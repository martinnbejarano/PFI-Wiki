---
titulo: Restricciones Legales y Éticas — Contexto Argentino
tipo: proyecto
tags: [legal, ético, privacidad, argentina, compliance, lpdp]
actualizado: 2026-04-19
---

# Restricciones Legales y Éticas — Contexto Argentino

## Resumen ejecutivo

El proyecto trabaja **exclusivamente con datos públicos** (posts públicos de redes sociales, artículos de noticias). No hay riesgo legal significativo si:
- No usamos datos privados (mensajes directos, emails, etc.)
- Anonymizamos metadatos personales (ID usuario, IP, ubicación)
- Usamos datasets académicos autorizados o APIs oficiales (no scraping no autorizado)
- Presentamos resultados como probabilidad, no como veredicto definitivo

---

## 1. LPDP — Ley de Protección de Datos Personales (25.326)

### ¿Qué protege?
Datos personales: nombre, email, teléfono, IP, ubicación geográfica, ID de usuario, cookies, datos biométricos, etc.

### ¿Cómo te afecta?

| Situación                                               | Riesgo                  | Mitigación                                                                               |
| ------------------------------------------------------- | ----------------------- | ---------------------------------------------------------------------------------------- |
| Recolectas posts públicos **sin anonymizar ID usuario** | Alto — es dato personal | Eliminar ID usuario, no guardar IP, solo guardar: texto + fecha publicación + plataforma |
| Usas ID usuario para linking (cruzar datos)             | Medio-Alto              | Usar hash del ID (no reversible) o eliminar directamente                                 |
| Publicas dataset con posts reales identificables        | Alto — viola LPDP       | Si publicas dataset, anonymizar completamente o pedir consentimiento                     |
| Usas datos para investigación académica no comercial    | Bajo — legítimo interés | OK, pero debe ser transparente (por ej., en aclaración legal)                            |

### Recomendación para el PFI
**Anonymizar durante recolección:**
```
ANTES: {user_id: 123456, username: "JuanPerez", tweet: "El dólar sube...", location: "Buenos Aires"}
DESPUÉS: {text: "El dólar sube...", date: "2026-04-19", platform: "twitter"}
```

---

## 2. Derechos de Autor — Ley 11.723

### ¿Qué protege?
Obras intelectuales originales: textos, imágenes, videos, etc. **Posts en Twitter/Instagram SON obras protegidas.**

### ¿Cómo te afecta?

| Situación | Derecho | Permiso necesario |
|---|---|---|
| Usar posts para entrenar modelo ML | Análisis / investigación educativa (fair use) | ✅ No necesitas permiso explícito |
| Publicar dataset con 1000 posts originales | Reproducción / distribución | ❌ Necesitas permiso de autores o de plataforma |
| Citar post en documentación del PFI | Cita / referencia | ✅ OK si citas fuente |
| Usar post para entrenar + vender API con ese contenido | Reproducción / derivación comercial | ❌ Necesitas licencia |

### Recomendación para el PFI
- **Entrenar modelo:** OK, cubre "investigación educativa"
- **Documentar en paper:** OK, cita las fuentes
- **Publicar dataset:** Anonymizar o pedir permisos
- **API comercial B2B:** No redistribuyas posts directamente; solo devuelve scores + links a fuentes (no contenido original)

---

## 3. Responsabilidad por Difamación / Derecho al Honor

### ¿Qué está prohibido?
Acusar falsamente a alguien de desinformación sin evidencia sólida.

### ¿Cómo te afecta?
Si tu modelo marca un post como "DESINFORMACIÓN CONFIRMADA" (veredicto definitivo) y es incorrecto, hay riesgo legal de difamación.

### Recomendación para el PFI
- **Presentar como probabilidad:** "70% prob de ser falso" (no "ES FALSO")
- **Incluir evidencia:** Links a fuentes que corroboran/contradicen (usuario decide)
- **Disclaimer:** "Este sistema es una herramienta de apoyo, no reemplaza verificación profesional"
- **Score, no veredicto:** 0-1 (probabilidad), no "Verdadero/Falso"

---

## 4. Terms of Service (ToS) de Plataformas

### ¿Por qué importa?
Cada plataforma tiene reglas legales que aceptas al usarla:
- Twitter/X: No scraping masivo, no entrenamiento de modelos sin permiso
- Instagram: Acceso API muy restrictivo
- Facebook: Acceso API limitado post-Cambridge Analytica

### Cumplimiento legal según fuente de datos

| Fuente | ToS | Legalidad | Recomendación |
|---|---|---|---|
| **API oficial (Twitter, etc.)** | ✅ Respeta ToS | Legal | ✅ Usar |
| **Dataset académico (LIAR, FakeNewsNet)** | ✅ Datos ya extraídos legalmente | Legal | ✅ Usar |
| **Web scraping sin permiso** | ❌ Viola ToS | Gris legal en Argentina | ⚠️ Evitar |
| **Chequeado.com datos** | Negociar con equipo | Legal si hay permiso | ✅ Contactar |

---

## 5. Ley de Libertad de Expresión vs Restricción de Desinformación

### Contexto actual
Argentina no tiene ley específica sobre "fake news" o desinformación (a diferencia de algunos países europeos). Esto es **favorable para el PFI**.

**Implicancia:** Tu sistema no "censura" — es una herramienta informativa que el usuario usa voluntariamente.

---

## 6. Estrategia recomendada de Compliance para el PFI

### ✅ Haz esto:
1. **Anonymizar datos durante recolección:** Eliminar ID usuario, IP, metadatos sensibles
2. **Usar datasets académicos autorizados:** LIAR, FakeNewsNet, buscar equivalentes en español
3. **Contactar Chequeado.com:** Preguntar si pueden compartir datos de afirmaciones verificadas (para entrenamiento)
4. **API oficial si la necesitas:** Solicitar acceso a Twitter API v2 (disponible en tier académico gratuito)
5. **Documentar fuentes:** Citar todos los datasets y papers usados
6. **Disclaimer legal en la extensión Chrome:** "Herramienta de apoyo. Verificar con fuentes originales. No es veredicto definitivo."
7. **No publicar dataset completo:** Si publicas algo, anonymizar al máximo
8. **Presentar scores no veredictos:** 0.7 = 70% probabilidad, no "ES FALSO"

### ❌ Evita esto:
1. Scraping masivo de Twitter/Instagram sin permiso
2. Guardar ID usuario o metadatos personales
3. Presentar resultado como "VEREDICTO DEFINITIVO"
4. Publicar dataset con posts identificables sin permiso
5. Acceder a datos privados (DMs, privacidad de cuenta)

---

## 7. Disclaimer legal para la extensión

**Propuesta de texto para incluir en la extensión:**

> Este sistema utiliza inteligencia artificial para analizar contenido textual y estimar la probabilidad de que sea desinformativo. 
> - **No es un veredicto legal o definitivo.** Los resultados son una herramienta de apoyo para usuarios.
> - Antes de compartir información importante, verifica con fuentes originales.
> - Los datos utilizados son públicos y se tratan de conformidad con la Ley 25.326 (LPDP).
> - El sistema puede tener falsos positivos, especialmente con contenido satírico o irónico.

---

## 8. Referencia de leyes argentinas clave

| Ley | Código | Tema | Link |
|---|---|---|---|
| LPDP | 25.326 | Protección de datos personales | https://www.argentina.gob.ar/normativa/nacional/ley-25326-1999-9853 |
| Ley de Derechos de Autor | 11.723 | Propiedad intelectual | https://www.argentina.gob.ar/normativa/nacional/ley-11723-1933-16240 |
| Código Penal (Difamación) | Art. 109-115 | Delitos contra honor | https://www.argentina.gob.ar/normativa/nacional/ley-11179-1921-123456 |

---

## Referencias cruzadas

- [[wiki/proyecto/propuesta]]
- [[wiki/datasets/dataset-recomendacion]]
- [[wiki/solucion/pipeline-preprocesamiento]]

