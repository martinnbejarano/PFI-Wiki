# Documentación de dominio

Cómo deben consumir las *skills* de ingeniería la documentación de dominio de este repositorio.

Layout: **contexto único**.

## Antes de explorar, leer

- **`CONTEXT.md`** en la raíz.
- **`docs/adr/`** — los ADR que toquen el área en la que se va a trabajar.

Si alguno no existe, **seguir en silencio**. No señalar su ausencia ni proponer crearlos por adelantado. La *skill* `/domain-modeling` —a la que se llega desde `/grill-with-docs` y `/improve-codebase-architecture`— los crea de forma perezosa, cuando efectivamente se resuelve un término o una decisión.

## Estructura de archivos

```
/
├── CONTEXT.md          ← glosario del dominio
├── docs/
│   ├── adr/            ← decisiones difíciles de revertir
│   └── agents/         ← esta configuración
├── wiki/               ← investigación y borrador
├── documento/          ← documento final en LaTeX
└── raw/                ← fuentes originales, inmutables
```

## Particularidad de este repositorio

No es una base de código: es un wiki de investigación más un documento LaTeX. Eso cambia dos cosas.

**El glosario ya existe, repartido.** El dominio —desinformación, misinformación, verificación automática, jerarquía de evidencia, los cuatro módulos— está definido en `wiki/marco-teorico/` y en `wiki/solucion/`. `CONTEXT.md` no debe duplicarlo: sirve para los términos que se usan de forma transversal y cuya deriva rompe el documento, apuntando a la página del wiki que los desarrolla. La regla de terminología consistente del `CLAUDE.md` —una vez establecido un término, usarlo siempre igual— es exactamente el problema que `CONTEXT.md` existe para vigilar.

**Los ADR y el wiki se reparten distinto trabajo.** `wiki/sintesis/decisiones-pendientes-*.md` registra decisiones **abiertas** del proyecto, con sus opciones evaluadas. `docs/adr/` es para decisiones **cerradas y difíciles de revertir** que condicionan cómo se trabaja: elección de modelo, motor de base de datos, postura legal. Cuando una decisión de `decisiones-pendientes` se cierra y condiciona el resto, se le escribe su ADR.

`documento/history/considerations.tex` cumple un rol parecido para las decisiones de formato del documento LaTeX y sigue siendo el lugar de esas.

## Usar el vocabulario del glosario

Cuando una salida nombre un concepto del dominio —el título de un *issue*, una propuesta, una hipótesis—, usar el término tal como está definido, sin derivar a sinónimos que el glosario evita.

Si el concepto que se necesita todavía no está, es una señal: o se está inventando lenguaje que el proyecto no usa —conviene reconsiderar— o hay un hueco real, y se anota para `/domain-modeling`.

## Señalar conflictos con un ADR

Si una salida contradice un ADR existente, hay que decirlo en lugar de pisarlo en silencio:

> _Contradice el ADR-0007 (persistencia del `@` en claro), pero vale reabrirlo porque…_
