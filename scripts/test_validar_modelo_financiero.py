"""Tests de scripts/validar_modelo_financiero.py a través de su interfaz de línea de comandos.

Uso:  .venv/bin/python -m unittest scripts/test_validar_modelo_financiero.py
"""
import os, subprocess, sys, tempfile, unittest

import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'scripts/validar_modelo_financiero.py')
PLANILLA = os.path.join(ROOT, 'wiki/negocio/modelo-financiero.xlsx')
SEGMENTOS = ['Medios de gran porte', 'Medios socios de ADEPA (resto)', 'Verificadores',
             'Universidades y observatorios', 'Agencias']


def correr(*args):
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)


def planilla_de_juguete(ruta, van_planilla):
    """Planilla con valores (sin fórmulas) y un flujo de resultado conocido.

    Flujo -100, 60, 60, 0, 0, 0 al 25 %: VAN = -100 + 48 + 38,4 = -13,6;
    acumulado -100, -40, 20 => payback = 1 + 40/60; el descontado no se recupera.
    TIR = 13,0662 % (raíz de 60x² + 60x - 100 = 0, x = 1/(1+TIR)).
    Año 5: costos 1.000, ingresos 1.000 y 4 clientes => 250 por cliente => 4 clientes.
    """
    wb = openpyxl.Workbook()
    sup = wb.active
    sup.title = 'Supuestos'
    sup.append(['clave', 'concepto', 'unidad', 'común', 'Opt', 'Neu', 'Pes'])
    sup.append(['tasa_descuento', 'Tasa de descuento', '%', 0.25])
    esc = wb.create_sheet('Neutral')
    filas = [
        ('Año', [0, 1, 2, 3, 4, 5]),
        ('Ingresos totales', [0, 60, 60, 0, 0, 1000]),
        ('Costos totales', [100, 0, 0, 0, 0, 1000]),
        ('Flujo neto', [-100, 60, 60, 0, 0, 0]),
        ('Flujo descontado', [-100, 48, 38.4, 0, 0, 0]),
        ('Flujo neto acumulado', [-100, -40, 20, 20, 20, 20]),
        ('Clientes B2B (promedio del año, con contratos)', [0, 0, 0, 0, 0, 4]),
        ('Organismos y ONG: contratos', [None, 0, 0, 0, 0, 2]),
    ]
    for segmento in SEGMENTOS:
        filas.append((f'{segmento}: altas', [None, 1, 0, 0, 0, 0]))
        filas.append((f'{segmento}: activos al cierre', [None, 1, 1, 1, 1, 1]))
    for etiqueta, valores in filas:
        esc.append([etiqueta, *valores])
    indicadores = [
        ('VAN (USD)', van_planilla),
        ('TIR', 0.130662),
        ('Payback simple (años)', 1 + 40 / 60),
        ('Payback descontado (años)', 'no se recupera'),
        ('Punto de equilibrio (clientes B2B)', 4),
    ]
    esc.append([])
    for etiqueta, valor in indicadores:
        esc.append([etiqueta, valor])
    wb.save(ruta)


class ValidarModeloFinanciero(unittest.TestCase):

    def test_autochequeo_con_flujos_de_juguete_pasa(self):
        r = correr('--autochequeo')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('autochequeo: ok', r.stdout)

    def test_indicador_que_no_coincide_termina_con_error_y_lo_nombra(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = os.path.join(d, 'm.xlsx')
            planilla_de_juguete(ruta, van_planilla=-13.0)  # el correcto es -13,6
            r = correr('--planilla', ruta, '--salida', d)
            self.assertEqual(r.returncode, 1)
            self.assertIn('VAN', r.stderr)
            self.assertIn('Neutral', r.stderr)
            self.assertFalse(os.path.exists(os.path.join(d, 'financiero-neutral-flujo.tex')))

    def test_planilla_consistente_genera_las_tablas_del_escenario(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = os.path.join(d, 'm.xlsx')
            planilla_de_juguete(ruta, van_planilla=-13.6)
            r = correr('--planilla', ruta, '--salida', d)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            tablas = {}
            for nombre in ('altas', 'flujo', 'indicadores'):
                with open(os.path.join(d, f'financiero-neutral-{nombre}.tex')) as fh:
                    tablas[nombre] = fh.read()
            for tex in tablas.values():
                self.assertIn(r'\begin{table}[t]', tex)
                self.assertLess(tex.index(r'\caption'), tex.index(r'\begin{tabular}'))
                self.assertIn('Fuente: elaboración propia', tex)
            flujo, ind = tablas['flujo'], tablas['indicadores']
            self.assertIn('1.000,00', flujo)        # punto de miles y coma decimal
            self.assertIn('(100,00)', flujo)        # negativos entre paréntesis
            self.assertIn('(13,60)', ind)           # VAN
            self.assertIn('13,07', ind)             # TIR en %
            self.assertIn('1,67', ind)              # payback a mitad de año
            self.assertIn('no se recupera', ind)    # payback descontado
            self.assertIn('+1 (1)', tablas['altas'])

    def test_la_planilla_versionada_valida_contra_el_calculo_independiente(self):
        with tempfile.TemporaryDirectory() as d:
            r = correr('--planilla', PLANILLA, '--salida', d)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertTrue(os.path.exists(os.path.join(d, 'financiero-neutral-indicadores.tex')))


if __name__ == '__main__':
    unittest.main()
