---
titulo: Mockups del frontend
tipo: análisis
tags: [mockups, wireframes, ui, extension, dashboard, diseño]
fuentes: [Rubrica-EP2-50porciento.pdf]
actualizado: 2026-08-11
---

# Mockups del frontend

Cubre el **criterio 2** de la rúbrica de EP2, que pide pantallas del *frontend* claras y significativas. Cuatro pantallas, no más: la rúbrica premia que se entiendan, no que sean muchas.

**Fuente:** `wiki/assets/mockups/mockups.html`. Capturas en `wiki/assets/mockups/*.png`, copiadas a `documento/chapters/figures/` para el LaTeX.

Están construidas en HTML y CSS reales en lugar de dibujadas en una herramienta de diseño, por una razón práctica: la extensión del Bloque 3 hereda este marcado. El indicador que se inyecta sobre el tuit en la demo es el mismo componente que se ve acá, no una reimplementación.

Todo el contenido es **ficticio**. Las cuentas, los tuits, los titulares y las verificaciones fueron inventados sobre temas argentinos verosímiles. Cada pantalla lleva un rótulo visible que lo aclara, para que el documento no señale a ninguna cuenta identificable como fuente de desinformación —que sería contradecir el apartado ético dos capítulos antes.

## Cómo se abren

Abrir `wiki/assets/mockups/mockups.html` en Chrome. Se navega con las flechas ← y →, o directamente con `?pantalla=badge|popup|evidencia|dashboard`. La tecla `C` esconde la barra de navegación; `&captura=1` hace lo mismo desde la URL, que es como se generaron las imágenes del documento.

Las capturas se regeneran con Chrome en modo *headless*, a doble resolución:

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=900,1010 --screenshot=badge.png \
  "file://.../mockups.html?pantalla=badge&captura=1"
```

---

## 1. Indicador sobre el tuit

**Realiza:** RF-10 · **Caso de uso:** CU-01 · **Captura:** `badge.png`

Cuatro tuits del *timeline*, uno por cada estado posible: probablemente falso, información sospechosa, parece verificado y el estado transitorio de análisis en curso. Es la pantalla más importante del producto, porque es la única que el usuario ve sin haber pedido nada.

Dos decisiones de diseño que no son cosméticas:

**El estado se comunica por tres canales a la vez** —color, forma del ícono y texto—. Un usuario que no distingue rojo de verde lee "Probablemente falso" y ve un triángulo en lugar de un tilde. Es lo que sostiene RNF-15, que exige que el indicador sea interpretable sin instrucción previa.

**Ningún indicador afirma que el contenido sea falso.** El más severo dice *probablemente* y expone el porcentaje. Es la traducción visual de RNF-07 y la respuesta al riesgo de falsos positivos ante sátira e ironía que la propuesta reconoce: el error no se puede eliminar, pero sí se puede evitar presentarlo con una autoridad que el sistema no tiene.

El indicador incluye además una línea de motivo —"Contradice a 3 medios y a una verificación de Chequeado"— que adelanta la evidencia sin obligar a abrir nada. Es lo que hace que el badge sea informativo y no solo un semáforo.

---

## 2. Detalle del veredicto

**Realiza:** RF-11 y RF-13 · **Caso de uso:** CU-02 · **Captura:** `popup.png`

Dos estados en la misma captura, a propósito.

**A la izquierda, el flujo principal.** El *score* final, el desglose de los tres *scores* parciales con su barra, y las razones en lenguaje natural que produce el Módulo 4. El desglose es lo que convierte al sistema en algo auditable: el usuario puede ver que el texto puntuó 0,82 pero que lo que realmente movió el veredicto fue el contraste con fuentes en 0,89.

**A la derecha, el flujo alternativo 6a de CU-02**, cuando la búsqueda web no responde. No hay porcentaje: hay un guión. La barra del módulo faltante aparece rayada y la etiqueta dice *sin dato*, y un aviso explica qué pasó.

Esta segunda pantalla es la traducción visual de RNF-11 y vale la pena defenderla en la exposición. Un sistema que calcula el promedio ponderado con un módulo caído devuelve un número que parece igual de confiable que los demás y no lo es. La decisión de diseño es que la ausencia de un módulo se muestre como ausencia, no que se disimule con aritmética.

---

## 3. Panel de evidencia

**Realiza:** RF-12 · **Caso de uso:** CU-03 · **Captura:** `evidencia.png`

Las seis fuentes consultadas, agrupadas por tipo —verificaciones previas, medios de referencia, fuentes oficiales— y etiquetadas por postura: contradice, corrobora parcialmente, neutral. Cada una con la cita y el enlace al documento original.

Arriba de todo aparece la afirmación verificable que el Módulo 3 extrajo del tuit, con su tipo. Es un detalle que importa: muestra que el sistema no compara el tuit entero contra internet, sino una afirmación acotada, y explicita cuál. Si el sistema extrajo mal la afirmación, el usuario lo ve en la primera línea y entiende por qué el veredicto no le cierra.

La fila del Boletín Oficial es la que mejor ilustra la propuesta de valor. La cita dice que el anexo enumera 50 establecimientos; el usuario puede abrir la resolución y contarlos. Eso es lo que sostiene RNF-06 y lo que ningún competidor de la matriz comparativa entrega al ciudadano: no un veredicto, sino el camino para no depender del veredicto.

Se incluyó a propósito una fuente que **corrobora parcialmente** y otra **neutral**. Un panel donde todas las fuentes apuntan en la misma dirección sería un panel de confirmación, no de evidencia.

---

## 4. Panel de tendencias B2B

**Realiza:** RF-23 y RF-24 · **Caso de uso:** CU-07 · **Captura:** `dashboard.png`

El producto que se le vende a los segmentos B2B del modelo de negocio: volumen analizado, tasa de contenido marcado y su variación, evolución diaria, temas con mayor circulación, cuentas con mayor volumen marcado, y el consumo de la clave de API contra la cuota del plan.

Es la pantalla que conecta el capítulo de negocio con el de solución. Sin ella, el modelo *freemium* con monetización B2B queda declarado en el capítulo 3 y no aparece nunca en el producto.

**La columna de cuentas aparece hasheada a propósito.** RF-24 y RNF-10 exigen que toda exportación hacia terceros salga agregada o con la cuenta autora anonimizada, porque vender el dataset con los *handles* en claro es una cesión de datos personales bajo el art. 11 de la Ley 25.326. Un *mockup* que mostrara los `@` en esta pantalla estaría contradiciendo el apartado legal del propio documento. Los dos botones del pie —"Exportar CSV agregado" y "Exportar JSON anonimizado"— dicen lo mismo con otras palabras.

---

## Lo que estas pantallas dejan pendiente

No hay pantalla de instalación ni de configuración, y no hay pantalla del formulario de reporte de falso positivo. Las tres corresponden a requerimientos de prioridad *importante* o *deseable* (RF-15, RF-16, RF-18) y su ausencia no afecta a ninguno de los ocho criterios de la rúbrica. Si sobra tiempo en el bloque de escritura, la del reporte es la que más conviene sumar, porque CU-04 hoy no tiene respaldo visual.

Tampoco hay estados de error del lado del usuario más allá del análisis parcial: qué se muestra si la extensión no puede leer el DOM, o si el usuario no tiene conexión. Son estados reales que van a aparecer en la implementación del Bloque 3.

## Referencias cruzadas

- [[wiki/solucion/requerimientos]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/metodologia-tecnica]]
- [[wiki/proyecto/plan-bloque-diseno]]
- [[wiki/proyecto/restricciones-legales-eticas]]
- [[wiki/negocio/modelo-de-negocio]]
- [[wiki/competencia/analisis-competitivo]]
