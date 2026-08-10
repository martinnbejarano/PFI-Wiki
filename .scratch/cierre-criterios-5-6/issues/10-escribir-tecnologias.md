# 10 · Escribir `tecnologias.md`

Type: task
Status: open
Blocked by: 09

## Question

Reescribir `wiki/solucion/tecnologias.md`, hoy un *stub* de abril con cuatro `[POR DEFINIR]`, como página **técnica pura**: lenguajes, *frameworks*, versiones, librerías y el porqué de cada elección. `recursos.md` sigue siendo la página de costos; se enlazan y no se duplican. Alcance fijado el 2026-08-10.

Contenido:

1. Tabla por capa —extensión, panel web, API, base de datos, inferencia— con tecnología, versión fijada y justificación en una línea.
2. Un apartado por decisión disputada, con las alternativas evaluadas y el criterio de corte. Solo donde hubo alternativa real.
3. La parte de **arquitectura de red** que el criterio 5 exige, apoyada en `despliegue-red.drawio`, que ya está dibujado y exportado: protocolos, TLS, red privada de Railway y los cruces de frontera de confianza.
4. Librerías del pipeline de NLP —`transformers`, `tokenizers`, lo que use el preprocesamiento— coherentes con `pipeline-preprocesamiento.md`.
5. Enlaces a `recursos.md` para todo lo que sea costo, sin repetir cifras. Las que hoy están mal en el wiki —USD 65 en lugar de 173, y Serper en lugar de Tavily en seis archivos— no se propagan acá.

**Verificación.** Que no quede ningún `[POR DEFINIR]` en el archivo, y que el criterio 5 se pueda señalar entero desde una sola página. Actualizar `index.md` y `log.md`.
