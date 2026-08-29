# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

**Primario: el ciudadano argentino que usa X.** Está leyendo su *timeline*, en escritorio, sin haber pedido nada. Se cruza con una publicación que afirma algo verificable —una medida de gobierno, un dato económico, una noticia de salud o de educación— y no tiene forma de saber si es cierta sin abandonar lo que estaba haciendo. Su trabajo no es investigar: es decidir, en segundos, cuánto crédito darle a lo que acaba de leer.

No tiene conocimiento técnico y no va a leer instrucciones. Si la señal no se interpreta sola, no existe.

**Secundario: quien evalúa el proyecto.** Tribunal y tutor de la Facultad de Ingeniería y Ciencias Exactas de la UADE. Su trabajo es verificar que lo que el documento describe está efectivamente construido y que los recortes declarados son metodológicos y no improvisados.

## Product Purpose

Detección automática de desinformación en X. El sistema lee una publicación, extrae la afirmación verificable que contiene, la contrasta contra fuentes oficiales argentinas y medios de referencia, y emite un veredicto acompañado de las fuentes que lo sostienen, cada una enlazada a su documento original.

El éxito no es que el usuario crea el veredicto. Es que pueda **prescindir de él**: el sistema entrega el camino hacia la evidencia, no sólo la conclusión.

## Positioning

Lo que un producto vecino no puede copiar de buena fe: **el veredicto llega siempre con su evidencia enlazada, y cuando no hay evidencia el sistema lo dice en lugar de opinar.**

La ausencia de fuentes se muestra como ausencia —el estado *sin contraste externo*— y no se disfraza de veredicto. La jerarquía de evidencia es explícita y está restringida a fuentes oficiales argentinas, cinco medios de referencia de orientación editorial diversa, y verificaciones previas, en ese orden de precedencia.

El sistema se enuncia **sobre la afirmación y nunca sobre la persona que la publicó**. El nivel más severo atribuye el juicio a la fuente que lo sostiene en lugar de afirmarlo por su cuenta.

## Operating Context

La superficie de uso es **el *timeline* de x.com, en Chrome de escritorio**, con la interfaz de X ocupando toda la pantalla. La extensión no tiene lienzo propio: inyecta su interfaz dentro de una página ajena, que no controla y que puede cambiar sin aviso.

Eso define la restricción central del producto: **todo lo que se dibuje convive con la interfaz de X, compitiendo por la misma atención y el mismo espacio, sin poder ocultarla ni reemplazarla.**

El análisis es **a demanda**: se dispara por clic del usuario sobre el indicador, nunca automáticamente. Tarda del orden de veinte segundos, medidos, de modo que el estado transitorio no es un detalle sino una parte sustancial de la experiencia.

## Capabilities and Constraints

**Lo que hace hoy**

- Inyecta un indicador sobre cada publicación del *timeline*.
- Extrae la afirmación verificable y la clasifica por tipo: normativa, dato económico, salud, educación u otro.
- Recupera evidencia restringida a la jerarquía declarada y determina, para cada fuente, si corrobora, contradice o es neutral.
- Emite un veredicto en tres niveles —contradicho por fuentes oficiales, información sospechosa, parece verificado— o el estado *sin contraste externo*.
- Muestra el desglose de los tres puntajes parciales y el panel de evidencia con las fuentes enlazadas.
- Ante el fallo de cualquier módulo devuelve un análisis parcial identificado como tal, nunca un error opaco.

**Estados que la interfaz tiene que saber dibujar**

Inicial · transitorio · tres niveles de veredicto · sin contraste externo · análisis parcial · falla.

**Restricciones**

- Chrome de escritorio bajo Manifest V3, en Windows, macOS y Linux. Sin soporte móvil ni otros navegadores.
- La interfaz vive en un *shadow DOM* y **no puede alterar los estilos ni el comportamiento de X**.
- La política de contenido de X prohíbe guiones en línea y `eval`.
- El marcado de X no está versionado y puede cambiar sin aviso; la lectura del DOM es defensiva.
- Recortes declarados: el módulo de credibilidad de cuenta no está implementado y su valor es arbitrario; debe aparecer marcado como tal y no ponderar en el resultado.

**Terminología fijada**

*Afirmación verificable*, *jerarquía de evidencia*, *postura* (corrobora / contradice / neutral), *análisis parcial*, *sin contraste externo*. Los tres niveles se nombran siempre igual y nunca se abrevian.

## Brand Commitments

**El lenguaje visual de X, en modo oscuro exclusivamente.** La extensión debe leerse como una función integrada de X y no como un artefacto externo pegado encima. Es una restricción binaria del usuario: no hay modo claro.

**Marca propia discreta y siempre visible.** Se adopta el lenguaje visual de X, pero el indicador lleva permanentemente una marca mínima propia. El producto parece integrado sin hacerse pasar por X: un ciudadano no debe poder concluir que el veredicto lo emite la plataforma.

Esa tensión —integrarse sin suplantar— es la decisión de diseño más cargada del producto, y sostiene directamente la atribución que el marco legal y ético del proyecto exige.

## Evidence on Hand

- Código andando: `prototipo/` (servicio y extensión), verificado con 60 y 14 pruebas.
- Requerimientos, arquitectura, modelo de datos y metodología técnica: `wiki/solucion/`.
- Documento académico en LaTeX: `documento/`.
- Diseño previo de las pantallas: `wiki/assets/mockups/`.
- **Latencia medida** el 2026-08-28 sobre una afirmación de dato económico, tres pasos y seis fuentes: 20,2 s de extremo a extremo.

**Lo que no existe y no debe fabricarse:** no hay usuarios reales, ni métricas de uso, ni resultados de evaluación del clasificador, ni testimonios, ni acuerdos con medios o con organismos. La jerarquía de evidencia es una decisión de diseño del proyecto, no un convenio con esas instituciones.

## Product Principles

1. **La ausencia se muestra como ausencia.** Ningún vacío se rellena con aritmética ni con un número que aparente ser una medición. Un módulo que no corrió se dibuja faltante.
2. **El veredicto nunca viaja solo.** Toda afirmación del sistema llega con la evidencia que la sostiene, enlazada y abrible. Lo que el sistema *encontró* se distingue visualmente de lo que *infirió*.
3. **Se juzga la afirmación, nunca a la persona.** Ninguna superficie puede leerse como un señalamiento sobre quien publicó.
4. **Interpretable sin instrucción previa.** El estado se comunica por más de un canal a la vez, de modo que no dependa de distinguir colores. Un usuario sin conocimiento técnico entiende la señal al verla.
5. **Invitada en casa ajena.** La interfaz se integra en X sin degradarla, sin competir con ella y sin suplantarla.

## Accessibility & Inclusion

El indicador debe ser interpretable sin instrucción previa por un usuario sin conocimiento técnico (RNF-15). El estado se comunica por **tres canales simultáneos —color, forma del ícono y texto—**, de modo que quien no distingue rojo de verde lea el estado igual.

Los enlaces a las fuentes son navegables y el contraste tiene que sostenerse sobre el fondo oscuro de X.
