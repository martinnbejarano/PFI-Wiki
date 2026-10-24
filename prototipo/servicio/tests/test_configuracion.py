"""RNF-16: umbrales, pesos y parámetros de la memoria se leen del entorno."""

from app.combinador import nivel_de_veredicto
from app.configuracion import Configuracion
from app.contrato import Veredicto


def test_el_entorno_cambia_umbral_pesos_y_memoria_sin_tocar_el_codigo(monkeypatch):
    por_defecto = Configuracion(_env_file=None)
    assert nivel_de_veredicto(0.45, por_defecto) == Veredicto.INFORMACION_SOSPECHOSA

    monkeypatch.setenv("UMBRAL_INFORMACION_SOSPECHOSA", "0.50")
    monkeypatch.setenv("PESO_CONTRASTE", "0.70")
    monkeypatch.setenv("UMBRAL_SIMILITUD_MEMORIA", "0.90")
    monkeypatch.setenv("VIGENCIA_MEMORIA_DIAS", "3")
    monkeypatch.setenv("ETIQUETA_CONFIGURACION_PESOS", "pesos-prueba")
    desde_el_entorno = Configuracion(_env_file=None)

    assert nivel_de_veredicto(0.45, desde_el_entorno) == Veredicto.PARECE_VERIFICADO
    assert desde_el_entorno.peso_contraste == 0.70
    assert desde_el_entorno.umbral_similitud_memoria == 0.90
    assert desde_el_entorno.vigencia_memoria_dias == 3
    assert desde_el_entorno.etiqueta_configuracion_pesos == "pesos-prueba"
