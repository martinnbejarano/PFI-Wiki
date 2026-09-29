"""Panel web mínimo del ciudadano: histórico personal (RF-10, CU-05) y RF-12.

La arquitectura prevé el panel como aplicación estática aparte (React con
Vite). El prototipo lo sirve el propio servicio como HTML armado en el
servidor, sin JavaScript: son una lista y un detalle, y así se prueban por el
mismo contrato HTTP que el resto de la batería.

Todo lo que viene del análisis pasa por `html.escape`: la afirmación sale del
texto de un tuit, que escribe cualquiera.
"""

from __future__ import annotations

from html import escape
from typing import Any
from urllib.parse import urlencode

from .contrato import RespuestaAnalisis, TipoFuente

VEREDICTOS = {
    "contradicho_por_fuentes_oficiales": "Contradicho por fuentes oficiales",
    "informacion_sospechosa": "Información sospechosa",
    "parece_verificado": "Parece verificado",
    "sin_contraste_externo": "Sin contraste externo",
}
TIPOS_DE_FUENTE = {
    "fuente_oficial": "Fuente oficial",
    "medio_de_referencia": "Medio de referencia",
    "verificacion_previa": "Verificación previa",
}
TIPOS_DE_ERROR = {"falso_positivo": "falso positivo", "falso_negativo": "falso negativo"}

# RF-12. La finalidad repite la que declara el apartado legal (cap. 3 del
# documento). El canal concreto de supresión no está definido en ningún lado.
FINALIDAD_Y_SUPRESION = """
<section class="legal">
  <h2>Finalidad y supresión de datos</h2>
  <p><strong>Finalidad declarada del tratamiento.</strong> El contenido público
  analizado se usa para emitir el veredicto, para investigación, para entrenar
  y corregir el clasificador —incluidos los informes de error— y para el
  historial agregado por cuenta. Tu histórico se asocia a un identificador
  anónimo generado por la extensión en este navegador, no a una persona: no se
  piden nombre, correo ni cuenta.</p>
  <p><strong>Derecho de supresión.</strong> Quien sea titular de los datos
  puede pedir su supresión según el artículo 16 de la Ley 25.326; el pedido se
  atiende dentro de los cinco días hábiles. Canal de contacto: pendiente de
  definir en el prototipo.</p>
</section>
"""

ESTILOS = """
body { max-width: 760px; margin: 0 auto; padding: 16px; font: 15px/1.5 -apple-system,
  BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #15202b; background: #fff; }
h1 { font-size: 20px; } h2 { font-size: 16px; margin-top: 28px; }
ol.historial { padding: 0; list-style: none; }
ol.historial li { padding: 10px 0; border-bottom: 1px solid #e1e8ed; }
.meta { color: #5b6570; font-size: 13px; }
.veredicto { font-weight: 700; }
.legal { margin-top: 32px; padding-top: 8px; border-top: 1px solid #e1e8ed;
  color: #5b6570; font-size: 13.5px; }
a { color: #1d6fb8; }
"""


def _pagina(cuerpo: str) -> str:
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Detector de desinformación — panel</title><style>{ESTILOS}</style></head>
<body><h1>Detector de desinformación</h1>{cuerpo}{FINALIDAD_Y_SUPRESION}</body></html>"""


def _veredicto(analisis: RespuestaAnalisis) -> str:
    texto = VEREDICTOS[analisis.veredicto.value]
    if analisis.analisis_parcial.es_parcial:
        return f"{texto} (análisis parcial)"
    if analisis.veredicto.value != "sin_contraste_externo":
        # La misma inversión que la extensión (`veracidad.ts`).
        return f"{texto} · {round((1 - analisis.puntaje_final) * 100)}% de probabilidad de ser verdadera"
    return texto


def _afirmacion(analisis: RespuestaAnalisis) -> str:
    return escape(analisis.afirmacion) or "Sin afirmación verificable"


def renderizar_institucional() -> str:
    """Flujo alternativo de CU-05: sin instalación no hay histórico que asociar."""
    return _pagina(
        "<p>Este panel muestra el histórico de los análisis que pediste. Para "
        "verlo, abrilo desde la extensión, que es la que conoce el identificador "
        "anónimo de tu navegador.</p>"
    )


def renderizar_lista(uuid: str, entradas: list[dict[str, Any]]) -> str:
    if not entradas:
        return _pagina("<p>Todavía no hay análisis pedidos desde esta instalación.</p>")
    filas = []
    for entrada in entradas:
        analisis: RespuestaAnalisis = entrada["analisis"]
        enlace = "?" + urlencode({"instalacion": uuid, "tuit": entrada["tweet_id"]})
        filas.append(
            f'<li><a href="{escape(enlace)}">{_afirmacion(analisis)}</a><br>'
            f'<span class="veredicto">{escape(_veredicto(analisis))}</span> '
            f'<span class="meta">· {escape(entrada["fecha"][:16].replace("T", " "))} UTC</span></li>'
        )
    return _pagina(
        "<h2>Tu histórico</h2><p class=\"meta\">Asociado a este navegador, sin "
        "sincronización entre dispositivos.</p>"
        f'<ol class="historial">{"".join(filas)}</ol>'
    )


def renderizar_detalle(uuid: str, entrada: dict[str, Any]) -> str:
    analisis: RespuestaAnalisis = entrada["analisis"]
    partes = [
        f'<p><a href="?{escape(urlencode({"instalacion": uuid}))}">← Volver al histórico</a></p>',
        f'<h2>{_afirmacion(analisis)}</h2>',
        f'<p class="meta">Tipo: {escape(analisis.tipo_afirmacion.value)} · '
        f'<a href="https://x.com/i/status/{escape(analisis.tweet_id)}">ver la publicación</a></p>',
        f'<p class="veredicto">{escape(_veredicto(analisis))}</p>',
        f"<p>{escape(analisis.justificacion)}</p>",
    ]
    if analisis.analisis_parcial.es_parcial:
        ausentes = ", ".join(analisis.analisis_parcial.modulos_ausentes)
        partes.append(f'<p class="meta">Módulos ausentes: {escape(ausentes)}</p>')
    if analisis.razones:
        razones = "".join(
            f'<li>{escape(r.texto)}'
            + (f' (<a href="{escape(r.fuente_url)}">fuente</a>)'
               if (r.fuente_url or "").startswith("https://") else "")
            + "</li>"
            for r in analisis.razones
        )
        partes.append(f"<h2>Por qué</h2><ul>{razones}</ul>")

    orden = list(TipoFuente)
    fuentes = sorted(analisis.fuentes, key=lambda f: orden.index(f.tipo))
    if fuentes:
        items = "".join(
            f'<li><a href="{escape(f.url)}">{escape(f.titulo)}</a> '
            f'<span class="meta">· {TIPOS_DE_FUENTE[f.tipo.value]} · {escape(f.postura.value)}</span></li>'
            for f in fuentes
        )
        partes.append(f"<h2>Evidencia</h2><ul>{items}</ul>")
    else:
        partes.append("<p class=\"meta\">Sin fuentes vinculadas: sin contraste externo.</p>")

    if entrada["reporte_tipo"]:
        motivo = escape(entrada["reporte_motivo"] or "")
        partes.append(
            f'<p class="meta">Informaste este veredicto como '
            f'{TIPOS_DE_ERROR[entrada["reporte_tipo"]]}. {motivo}</p>'
        )
    return _pagina("".join(partes))
