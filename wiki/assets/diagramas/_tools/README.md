# Herramientas de los diagramas

Los ocho `.drawio` de `wiki/assets/diagramas/` **son la fuente de verdad**. Se editan en [draw.io](https://app.diagrams.net) como cualquier diagrama; estos scripts solo los validan y los exportan.

## Uso

```bash
python3 _tools/validar.py                 # XML bien formado y sin aristas huérfanas
python3 _tools/render.py [nombre ...]     # PNG de revisión en un directorio temporal
python3 _tools/exportar.py                # PNG recortado en documento/chapters/figures/
```

Sin argumentos, `render.py` procesa los ocho.

## Cómo funciona el render

No hace falta draw.io de escritorio. Los scripts abren el visor web en Chrome *headless* y sacan una captura. El XML viaja en el **fragmento** de la URL —después del `#`—, que el navegador no envía al servidor: el contenido del diagrama nunca sale de la máquina.

Requisitos: Google Chrome instalado y `pillow` para el recorte (`pip install pillow`).

## Qué valida `validar.py`

Que cada `source` y cada `target` de cada arista resuelva a un vértice existente. Es el error que este formato produce con más frecuencia y que en draw.io se ve como una línea suelta flotando: el XML sigue siendo válido, así que ningún parser lo detecta.

## Advertencia

Cuatro de los ocho (`flujo-informacion`, `secuencia-cu01`, `secuencia-cu02`, `despliegue-red`) y también `c4-componentes` se generaron originalmente con un script de layout que **no está versionado acá**. Fue andamiaje de un solo uso: a partir de ahora las correcciones se hacen sobre el `.drawio`, no regenerando. Volver a correr aquel generador pisaría cualquier ajuste manual.
