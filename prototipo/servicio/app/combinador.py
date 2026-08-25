"""Módulo 4 — el combinador: de tres puntajes parciales a un veredicto.

Acá vive lo que convierte el resultado del sistema en **el producto de combinar
evidencia** y no en el juicio suelto de una llamada a un modelo. Tres funciones,
en el orden en que el orquestador las usa:

1. `puntaje_de_contraste` agrega la postura de las fuentes recuperadas,
   pesándolas según la jerarquía de evidencia, y produce el puntaje del
   Módulo 3.
2. `puntaje_combinado` pondera los tres puntajes parciales.
3. `nivel_de_veredicto` traduce el puntaje final en uno de los tres niveles de
   RF-06.

**Ningún número está escrito en este archivo.** Todos los pesos y los dos
umbrales salen de `Configuracion`, que es lo que exige RNF-16: se ajustan sin
volver a desplegar el servicio. Lo que este módulo aporta son las fórmulas.

Ningún test importa este módulo. Se ejercita entero por `POST /analizar`, que es
la costura que la *spec* fija: probar el combinador por separado sería probar
implementación y trabaría el reemplazo del paso de clasificación en la Entrega
4, que es justamente lo que la arquitectura busca habilitar.


Qué son estas fórmulas y qué no son
-----------------------------------

**Son heurísticas de prototipo.** No salen de un ajuste sobre datos etiquetados
ni de la literatura: son un promedio ponderado y dos cortes, elegidos porque son
transparentes, porque se pueden explicar en una oración y porque se pueden mover
en vivo durante la exposición. Decirlo así es más defendible que vestirlas de
método: un tribunal que pregunte de dónde salió el 0,65 tiene derecho a una
respuesta honesta, y la respuesta honesta es «de una decisión de diseño
declarada, no de una medición».

Lo que sí tiene que ser cierto, y lo que la batería de pruebas comprueba a
través del contrato HTTP:

- que la fórmula haga lo que este archivo dice que hace;
- que los tres niveles sean alcanzables;
- que mover un peso en la configuración mueva el puntaje final;
- que la jerarquía pese de verdad: una fuente oficial que contradice mueve el
  puntaje de contraste más que una verificación previa que contradice.

**Todo apunta en el mismo sentido.** Los tres puntajes parciales y el puntaje
final miden lo mismo: cuánto apunta la evidencia disponible a que la afirmación
sea desinformación. Cero es «nada apunta a eso», uno es «todo apunta a eso». Es
lo que la interfaz rotula como «probabilidad estimada de desinformación» en la
tapa del detalle. El puntaje de credibilidad de la cuenta es el único que viene
al revés —mide credibilidad, no sospecha— y por eso entra invertido; ver
`puntaje_combinado`.
"""

from __future__ import annotations

from .configuracion import Configuracion
from .contrato import Fuente, Postura, Puntajes, TipoFuente, Veredicto
from .jerarquia import JERARQUIA_DE_EVIDENCIA

# Cuánto empuja la postura de una fuente, y hacia dónde.
#
# Una fuente que contradice la afirmación empuja el puntaje de contraste hacia
# arriba —hacia «esto es desinformación»—, una que la corrobora lo empuja hacia
# abajo, y una neutral no lo empuja a ningún lado pero **sí cuenta** en el total
# contra el que se normaliza: encontrar cinco fuentes que no se pronuncian no es
# lo mismo que no encontrar ninguna, y la fórmula lo refleja diluyendo el
# resultado hacia el centro en lugar de ignorarlas.
_SENTIDO_DE_LA_POSTURA: dict[Postura, float] = {
    Postura.CONTRADICE: 1.0,
    Postura.CORROBORA: -1.0,
    Postura.NEUTRAL: 0.0,
}

# El punto medio de la escala de contraste: la evidencia recuperada no se
# inclina ni para un lado ni para el otro.
#
# **No es lo mismo que la ausencia de evidencia**, que el orquestador representa
# con 0,0 y con el estado *sin contraste externo*: 0,5 significa que se buscó,
# se encontró y quedó en equilibrio, que es una afirmación sobre el mundo. Ver
# `PUNTAJE_CONTRASTE_SIN_EVIDENCIA` en `pipeline.py` para la otra mitad de esta
# decisión.
CONTRASTE_EN_EQUILIBRIO = 0.5


def _peso_por_escalon(configuracion: Configuracion) -> dict[TipoFuente, float]:
    """Devuelve el peso de cada escalón de la jerarquía, según la configuración.

    La correspondencia entre escalón y campo de configuración se escribe una
    sola vez, acá. Si alguien suma un escalón a `JERARQUIA_DE_EVIDENCIA` sin
    darle un peso, el servicio falla al primer análisis con un mensaje que dice
    exactamente qué falta, en lugar de asignarle un peso por defecto y producir
    en silencio un puntaje que nadie eligió.
    """
    pesos = {
        TipoFuente.FUENTE_OFICIAL: configuracion.peso_fuente_oficial,
        TipoFuente.MEDIO_DE_REFERENCIA: configuracion.peso_medio_de_referencia,
        TipoFuente.VERIFICACION_PREVIA: configuracion.peso_verificacion_previa,
    }
    faltantes = {escalon.tipo for escalon in JERARQUIA_DE_EVIDENCIA} - set(pesos)
    if faltantes:
        nombres = ", ".join(sorted(tipo.value for tipo in faltantes))
        raise ValueError(
            f"La jerarquía de evidencia declara escalones sin peso en el "
            f"combinador: {nombres}. Agregá el campo en `Configuracion` y la "
            f"entrada en `_peso_por_escalon`."
        )
    return pesos


def puntaje_de_contraste(fuentes: list[Fuente], configuracion: Configuracion) -> float:
    """Agrega la postura de las fuentes en el puntaje del Módulo 3 (RF-05).

    **La fórmula.** Cada fuente aporta el peso de su escalón de la jerarquía,
    con el signo de su postura: positivo si contradice la afirmación, negativo
    si la corrobora, cero si es neutral. La suma se normaliza contra el peso
    total de las fuentes recuperadas —neutrales incluidas— y se lleva de la
    escala [-1, 1] a la escala [0, 1] del contrato::

        empuje    = Σ  peso(escalón de f) · sentido(postura de f)
        peso_total = Σ peso(escalón de f)
        contraste  = 0,5 + 0,5 · empuje / peso_total

    Qué produce, leído en casos:

    - Todas las fuentes contradicen → 1,0.
    - Todas corroboran → 0,0.
    - Todas neutrales, o el empuje de unas cancela el de otras → 0,5.
    - Una fuente oficial que contradice y un medio de referencia que corrobora,
      con los pesos por defecto (1,0 y 0,6) → 0,5 + 0,5 · 0,4/1,6 = 0,625. El
      contraste queda del lado de la contradicción, pero moderado por la
      corroboración, que es exactamente lo que la jerarquía dice que tiene que
      pasar.

    **Por qué normalizar por el peso total y no por la cantidad de fuentes.** Es
    lo que hace que la jerarquía pese de verdad. Con los pesos por defecto, una
    sola fuente oficial que contradice (peso 1,0) mueve el puntaje más que dos
    verificaciones previas que corroboran (0,4 cada una), y el resultado sigue
    del lado de la contradicción. Dividir por la cantidad daría el mismo número
    para las tres y la jerarquía sería decorativa.

    **Qué no hace.** No mira cuántas fuentes hay: tres fuentes que contradicen y
    una que contradice dan las dos 1,0. La cantidad de evidencia no entra en el
    puntaje; el ciudadano la ve en el panel de evidencia, donde están las tres
    filas o la única. Meter la cantidad exigiría decidir cuántas fuentes hacen
    una certeza, que es una pregunta que este prototipo no tiene con qué
    responder.

    Con la lista vacía esta función no llega a llamarse: el orquestador usa
    `PUNTAJE_CONTRASTE_SIN_EVIDENCIA`, porque la ausencia de evidencia no es un
    equilibrio. Aun así devuelve el punto medio si la reciben vacía, para no
    dividir por cero.
    """
    if not fuentes:
        return CONTRASTE_EN_EQUILIBRIO

    peso_por_escalon = _peso_por_escalon(configuracion)

    empuje = 0.0
    peso_total = 0.0
    for fuente in fuentes:
        peso = peso_por_escalon[fuente.tipo]
        peso_total += peso
        empuje += peso * _SENTIDO_DE_LA_POSTURA[fuente.postura]

    if peso_total <= 0.0:
        # Todos los escalones configurados en cero. Es una configuración
        # legítima —alguien apagó la jerarquía entera— y la respuesta correcta
        # es que la evidencia no inclina nada, no una división por cero.
        return CONTRASTE_EN_EQUILIBRIO

    return _acotar(CONTRASTE_EN_EQUILIBRIO * (1.0 + empuje / peso_total))


def puntaje_combinado(puntajes: Puntajes, configuracion: Configuracion) -> float:
    """Pondera los tres puntajes parciales en el puntaje final (RF-06).

    **La fórmula.** Un promedio ponderado, normalizado por la suma de los pesos
    para que ninguno tenga que acordarse de sumar uno::

        final = (p_clas · clasificador
                 + p_cred · (1 − credibilidad)
                 + p_contr · contraste) / (p_clas + p_cred + p_contr)

    Con los pesos por defecto —0,35 al clasificador, 0,00 a la credibilidad y
    0,65 al contraste— el término de la credibilidad desaparece del numerador y
    del denominador, y el final queda en 0,35 · clasificador + 0,65 · contraste.

    **Por qué el contraste pesa más que el clasificador.** El clasificador juzga
    el texto y solo el texto: detecta el lenguaje de alarma, las mayúsculas de
    grito y la apelación a compartir. Eso correlaciona con la desinformación
    pero no la establece, y castiga a quien escribe indignado una verdad. El
    contraste, en cambio, se apoya en documentos que el ciudadano puede abrir.
    El sistema entero existe para hacer ese contraste; el reparto lo dice.

    **Por qué la credibilidad entra invertida.** Es el único de los tres que
    mide en sentido contrario: un valor alto significa cuenta creíble, es decir,
    menos sospecha. Sin invertirlo, subir su peso volvería más sospechosa a la
    afirmación de una cuenta más creíble. Con el peso en cero el término no
    cambia ningún resultado, pero la inversión queda escrita para el día en que
    el Módulo 2 mida de verdad.

    **Por qué su peso por defecto es cero.** Ver `Configuracion.peso_credibilidad`:
    el Módulo 2 devuelve un número inventado, y ponderarlo contaminaría con él
    la cifra que la interfaz muestra como probabilidad estimada de
    desinformación. El puntaje sigue viajando en la respuesta, marcado, porque
    la interfaz tiene que dibujar el desglose de los tres módulos y decir cuál
    no midió nada; lo que no hace es entrar en el resultado.
    """
    terminos = (
        (configuracion.peso_clasificador, puntajes.clasificador.valor),
        (configuracion.peso_credibilidad, 1.0 - puntajes.credibilidad.valor),
        (configuracion.peso_contraste, puntajes.contraste.valor),
    )

    peso_total = sum(peso for peso, _ in terminos)
    if peso_total <= 0.0:
        # Los tres pesos en cero. Ningún módulo aporta, así que no hay puntaje
        # que sostener: se devuelve 0,0 en lugar de dividir por cero. Es una
        # configuración absurda, pero configurable quiere decir que se puede
        # escribir, y el servicio no se cae por eso.
        return 0.0

    return _acotar(sum(peso * valor for peso, valor in terminos) / peso_total)


def nivel_de_veredicto(puntaje: float, configuracion: Configuracion) -> Veredicto:
    """Traduce el puntaje final en uno de los tres niveles de RF-06.

    Dos cortes, leídos de mayor a menor: desde
    `umbral_contradicho_por_fuentes_oficiales` el nivel severo, desde
    `umbral_informacion_sospechosa` el intermedio, por debajo *parece
    verificado*. Los dos viven en la configuración por RNF-16.

    **Esta función no emite `sin_contraste_externo`.** Ese estado no es un
    escalón más bajo de la misma escala sino la ausencia de evidencia sobre la
    cual pronunciarse, y no depende de ningún puntaje: lo decide el orquestador
    mirando si hay fuentes admisibles, que es donde esa invariante de RNF-06 se
    hace valer.

    El orquestador también puede rebajar el nivel severo que esta función
    devuelva. El nombre del nivel dice quién sostiene el juicio —*contradicho
    por fuentes oficiales*— y RNF-07 exige que ese juicio se le atribuya a la
    fuente que lo sostiene; si ninguna fuente oficial contradice la afirmación,
    el nivel no se puede emitir aunque el puntaje llegue. Ver
    `_veredicto_admisible` en `pipeline.py`.
    """
    if puntaje >= configuracion.umbral_contradicho_por_fuentes_oficiales:
        return Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES
    if puntaje >= configuracion.umbral_informacion_sospechosa:
        return Veredicto.INFORMACION_SOSPECHOSA
    return Veredicto.PARECE_VERIFICADO


def _acotar(valor: float) -> float:
    """Deja el valor dentro de [0, 1], que es lo que el contrato admite.

    Las fórmulas no se salen del rango con pesos positivos, pero la
    configuración es texto que alguien escribe: un peso negativo en el `.env` no
    tiene que producir un error de validación del contrato a tres capas de
    distancia de su causa.
    """
    return min(max(valor, 0.0), 1.0)


__all__ = [
    "CONTRASTE_EN_EQUILIBRIO",
    "nivel_de_veredicto",
    "puntaje_de_contraste",
    "puntaje_combinado",
]
