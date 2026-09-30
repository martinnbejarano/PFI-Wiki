#!/usr/bin/env python3
"""Validación y exportación del modelo financiero del PFI.

Lee wiki/negocio/modelo-financiero.xlsx con los valores ya recalculados
(ver scripts/generar_modelo_financiero.py), recalcula por su cuenta los
indicadores de cada hoja de escenario y los compara con los de la planilla.
Si alguno no coincide, termina con código 1 e indica el indicador y el
escenario. Si todo coincide, escribe las tablas LaTeX de cada escenario en
documento/chapters/tables/.

Antes de validar corre un autochequeo con flujos de juguete de resultado
conocido, para que un error del cálculo de referencia no apruebe una
planilla rota.

Uso:  .venv/bin/python scripts/validar_modelo_financiero.py [--autochequeo]
          [--planilla RUTA] [--salida DIRECTORIO]
"""
import argparse, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANILLA = os.path.join(ROOT, 'wiki/negocio/modelo-financiero.xlsx')
SALIDA = os.path.join(ROOT, 'documento/chapters/tables')

NO_TIR = 'no definida'
NO_RECUPERA = 'no se recupera'


# ------------------------------------------------------------- indicadores

def descontar(flujos, tasa):
    return [f / (1 + tasa) ** t for t, f in enumerate(flujos)]


def van(flujos, tasa):
    return sum(descontar(flujos, tasa))


def tir(flujos, lo=-0.99, hi=100.0):
    """Tasa que anula el VAN, por bisección. Sin cambio de signo no hay TIR."""
    if min(flujos) >= 0 or max(flujos) <= 0:
        return None
    f_lo = van(flujos, lo)
    if f_lo * van(flujos, hi) > 0:
        return None
    for _ in range(200):
        medio = (lo + hi) / 2
        f_medio = van(flujos, medio)
        if f_lo * f_medio <= 0:
            hi = medio
        else:
            lo, f_lo = medio, f_medio
    return (lo + hi) / 2


def payback(flujos):
    """a + b/c: a = año anterior al recupero, b = saldo sin recuperar al
    cierre del año a, c = flujo del año del recupero."""
    acumulado = 0.0
    for t, f in enumerate(flujos):
        previo, acumulado = acumulado, acumulado + f
        if t > 0 and previo < 0 <= acumulado:
            return (t - 1) + (-previo) / f
    return NO_RECUPERA


def punto_equilibrio(costos, ingresos, clientes):
    """Clientes B2B necesarios para cubrir los costos del año, al ingreso medio."""
    if not ingresos or not clientes:
        return None
    return math.ceil(costos / (ingresos / clientes) - 1e-9)


def autochequeo():
    # Flujo A al 10 %: VAN = -100 + 54,5455 + 49,5868 = 4,1322.
    # TIR: 60x² + 60x - 100 = 0 => x = (-60 + √27.600)/120 = 0,884437 => 13,0662 %.
    # Acumulado -100, -40, 20 => 1 + 40/60. Descontado -100, -45,4545, 4,1322
    # => 1 + 45,4545/49,5868 = 1 + 60,5/66 = 1,916667.
    a = [-100, 60, 60]
    assert abs(van(a, 0.10) - 4.132231) < 1e-5
    assert abs(tir(a) - 0.130662) < 1e-5
    assert abs(payback(a) - 1.666667) < 1e-5
    assert abs(payback(descontar(a, 0.10)) - 1.916667) < 1e-5
    # Flujo B al 10 %: VAN = -100 + 30 × 2,486852 = -25,3944; no se recupera.
    b = [-100, 30, 30, 30]
    assert abs(van(b, 0.10) + 25.394440) < 1e-5
    assert payback(b) == NO_RECUPERA
    # Flujo C: nunca cambia de signo, no hay TIR.
    assert tir([-100, -10, -5]) is None
    # Flujo D: 110 / 1,10 = 100 => TIR = 10 % y VAN al 10 % = 0.
    assert abs(tir([-100, 110]) - 0.10) < 1e-9
    assert abs(van([-100, 110], 0.10)) < 1e-9
    # Punto de equilibrio: 1.000 / (300 / 4) = 13,33 => 14 clientes.
    assert punto_equilibrio(1000, 300, 4) == 14
    assert punto_equilibrio(1000, 0, 0) is None
    print('autochequeo: ok')


# ---------------------------------------------------------------- lectura

HOJAS_NO_ESCENARIO = {'Supuestos', 'Resumen'}


def leer(planilla):
    import openpyxl
    wb = openpyxl.load_workbook(planilla, data_only=True)
    sup = {f[0]: f[3] for f in wb['Supuestos'].iter_rows(values_only=True) if f[0]}
    escenarios = {}
    for hoja in wb.worksheets:
        if hoja.title in HOJAS_NO_ESCENARIO:
            continue
        filas = {f[0]: list(f[1:7]) for f in hoja.iter_rows(values_only=True) if f[0]}
        escenarios[hoja.title] = filas
    return sup['tasa_descuento'], escenarios


def recalcular(filas, tasa):
    neto = filas['Flujo neto']
    return {
        'VAN (USD)': van(neto, tasa),
        'TIR': tir(neto),
        'Payback simple (años)': payback(neto),
        'Payback descontado (años)': payback(descontar(neto, tasa)),
        'Punto de equilibrio (clientes B2B)': punto_equilibrio(
            filas['Costos totales'][-1], filas['Ingresos totales'][-1],
            filas['Clientes B2B (promedio del año, con contratos)'][-1]),
    }


TEXTO_NULO = {'TIR': NO_TIR, 'Punto de equilibrio (clientes B2B)': 'no definido'}


def coincide(planilla, propio):
    if isinstance(propio, str) or isinstance(planilla, str):
        return planilla == propio
    return abs(planilla - propio) <= 1e-6 * max(1, abs(propio)) + 1e-4


# ----------------------------------------------------------------- salida

CABECERA = '% Generado por scripts/validar_modelo_financiero.py — no editar a mano.\n'
FUENTE = 'Fuente: elaboración propia sobre la planilla del modelo financiero.'
SEGMENTOS = [  # (etiqueta en la planilla, encabezado de la tabla)
    ('Medios de gran porte', 'Medios de gran porte'),
    ('Medios socios de ADEPA (resto)', 'Resto de medios de ADEPA'),
    ('Verificadores', 'Verifica\\-dores'),
    ('Universidades y observatorios', 'Univer\\-sidades'),
    ('Agencias', 'Agencias'),
]


def num(v, dec=2):
    """Coma decimal, punto de miles y negativos entre paréntesis."""
    if abs(v) < 0.5 * 10 ** -dec:
        v = 0
    s = f'{abs(v):,.{dec}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'({s})' if v < 0 else s


def entero(v):
    return int(math.floor((v or 0) + 0.5))


def tabla(slug, clave, titulo, columnas, encabezado, filas):
    cuerpo = '\n'.join('    ' + ' & '.join(f) + r' \\' for f in filas)
    return CABECERA + f"""\\begin{{table}}[t]
  \\centering
  \\small
  \\caption{{{titulo}. {FUENTE}}}
  \\label{{tab:financiero-{slug}{'-' + clave if clave else ''}}}
  \\begin{{tabular}}{{{columnas}}}
    \\hline
    {' & '.join(f'\\textbf{{{e}}}' for e in encabezado)} \\\\
    \\hline
{cuerpo}
    \\hline
  \\end{{tabular}}
\\end{{table}}
"""


def filas_indicadores(filas):
    def valor(etiqueta, formato):
        v = filas[etiqueta][0]
        return v if isinstance(v, str) else formato(v)

    return [
        ['VAN (USD)', valor('VAN (USD)', num)],
        ['TIR (\\%)', valor('TIR', lambda v: num(100 * v))],
        ['\\textit{Payback} (años)', valor('Payback simple (años)', num)],
        ['\\textit{Payback} descontado (años)', valor('Payback descontado (años)', num)],
        ['Punto de equilibrio en el año 5 (clientes B2B)',
         valor('Punto de equilibrio (clientes B2B)', lambda v: num(v, 0))],
        ['Clientes B2B en el año 5 (promedio del año)',
         num(filas['Clientes B2B (promedio del año, con contratos)'][-1], 1)],
    ]


def tabla_comparada(escenarios):
    """Indicadores de todos los escenarios, uno por columna, en el orden de las hojas."""
    columnas = [filas_indicadores(filas) for filas in escenarios.values()]
    filas = [[fila[0][0], *(f[1] for f in fila)] for fila in zip(*columnas)]
    return tabla('comparada', None, 'Indicadores financieros comparados de los escenarios',
                 'l' + ' r' * len(escenarios), ['Indicador', *escenarios], filas)


def tablas_del_escenario(nombre, filas):
    import unicodedata
    slug = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode().lower()
    esc = nombre.lower()
    anios = range(1, 6)

    altas = []
    for t in anios:
        fila = [str(t)]
        for etiqueta, _ in SEGMENTOS:
            a = entero(filas[f'{etiqueta}: altas'][t])
            fila.append(f'{"+" if a > 0 else ""}{a} ({entero(filas[f"{etiqueta}: activos al cierre"][t])})')
        fila.append(str(entero(filas['Organismos y ONG: contratos'][t])))
        altas.append(fila)

    flujo = []
    for t in range(0, 6):
        flujo.append([str(t)] + [num(filas[r][t] or 0) for r in (
            'Ingresos totales', 'Costos totales', 'Flujo neto', 'Flujo descontado',
            'Flujo neto acumulado')])

    indicadores = filas_indicadores(filas)

    return slug, {
        'altas': tabla(slug, 'altas',
                       f'Altas de clientes B2B por año y segmento, escenario {esc}. Cada celda muestra '
                       'las altas del año y, entre paréntesis, los clientes activos al cierre; la '
                       'última columna corresponde a los contratos de monitoreo electoral',
                       'c *{6}{>{\\centering\\arraybackslash}p{1.8cm}}',
                       ['Año', *[e for _, e in SEGMENTOS], 'Contratos electorales'], altas),
        'flujo': tabla(slug, 'flujo', f'Flujo de caja del escenario {esc}, en USD',
                       'c r r r r r',
                       ['Año', 'Ingresos', 'Costos', 'Flujo neto', 'Flujo descontado',
                        'Flujo neto acumulado'], flujo),
        'indicadores': tabla(slug, 'indicadores', f'Indicadores financieros del escenario {esc}',
                             'l r', ['Indicador', 'Valor'], indicadores),
    }


def main(args):
    parser = argparse.ArgumentParser(description='Valida el modelo financiero y exporta sus tablas LaTeX.')
    parser.add_argument('--autochequeo', action='store_true', help='solo corre el autochequeo')
    parser.add_argument('--planilla', default=PLANILLA, help='planilla recalculada a validar')
    parser.add_argument('--salida', default=SALIDA, help='directorio de las tablas .tex')
    opts = parser.parse_args(args)
    autochequeo()
    if opts.autochequeo:
        return 0
    planilla, salida = opts.planilla, opts.salida
    tasa, escenarios = leer(planilla)
    errores = []
    for nombre, filas in escenarios.items():
        for indicador, propio in recalcular(filas, tasa).items():
            if propio is None:
                propio = TEXTO_NULO[indicador]
            en_planilla = filas[indicador][0]
            if not coincide(en_planilla, propio):
                errores.append(f'ERROR: el indicador «{indicador}» no coincide en el escenario '
                               f'{nombre}: planilla = {en_planilla}, recalculado = {propio}')
    if errores:
        print('\n'.join(errores), file=sys.stderr)
        return 1
    os.makedirs(salida, exist_ok=True)
    for nombre, filas in escenarios.items():
        slug, tablas = tablas_del_escenario(nombre, filas)
        for clave, tex in tablas.items():
            ruta = os.path.join(salida, f'financiero-{slug}-{clave}.tex')
            with open(ruta, 'w') as fh:
                fh.write(tex)
            print(f'  escrito  {os.path.relpath(ruta, ROOT)}')
    ruta = os.path.join(salida, 'financiero-comparada.tex')
    with open(ruta, 'w') as fh:
        fh.write(tabla_comparada(escenarios))
    print(f'  escrito  {os.path.relpath(ruta, ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
