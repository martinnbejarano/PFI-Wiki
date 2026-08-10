# 06 · Las catorce entidades: traza a RF, atributos, tipos y cardinalidades

Type: grilling
Status: open
Blocked by: 01, 02

## Question

`plan-bloque-diseno.md` nombra catorce entidades en cuatro dominios. Falta convertirlas en un modelo lógico y, antes de eso, pasarlas por la regla de corte del propio plan: **toda entidad tiene que ser trazable a un RF**.

**Contenido analizado** — `tuit`, `cuenta`, `medio_confiable`
**Análisis** — `analisis`, `claim`, `evidencia`, `desmentida`
**Uso ciudadano** — `usuario_extension`, `reporte_falso_positivo`, `modelo_version`
**Plataforma B2B** — `organizacion`, `usuario_b2b`, `api_key`, `consumo_api`

Lo que hay que resolver:

1. **La traza, entidad por entidad.** `medio_confiable` es la más dudosa: ¿es una tabla o es configuración de la aplicación? La lista de medios de referencia es fija y corta. `cuenta` se sostiene en RF-26, pero conviene verificar que el Módulo 2 necesite historial agregado persistido y no calculado al vuelo.
2. **`modelo_version` está en el dominio equivocado.** El plan la ubica en «uso ciudadano» y no tiene nada que ver: es trazabilidad del modelo (RF-27). ¿Se mueve a «análisis», o se abre un quinto dominio?
3. **Atributos, tipos y nulabilidad** de cada entidad, con las columnas que salgan de los tickets 01 y 02.
4. **Cardinalidades**, con dos casos que no son obvios: un `claim` puede aparecer en muchos `tuit` —es el punto de la búsqueda vectorial—, y una `evidencia` puede sostener más de un `analisis`.
5. **Las columnas `vector`** de `claim` y `desmentida`: dimensión del *embedding* y qué modelo la produce. Tiene que ser coherente con XLM-T, que no es el mismo espacio vectorial que un modelo de similitud semántica.
6. **El origen automático o a demanda** de `analisis` (decisión 1): ¿un análisis automático y uno profundo del mismo tuit son dos filas o una que se enriquece? Cambia el diagrama de secuencia si es lo segundo.

**Por qué está bloqueado.** El ticket 01 define columnas de retención y de supresión; el 02 define si `usuario_extension` existe. Dibujar antes es dibujar dos veces.
