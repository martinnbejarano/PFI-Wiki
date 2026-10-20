#!/usr/bin/env python3
"""Análisis de la encuesta de user research del PFI.

Lee raw/investigacion/encuesta-desinformacion-v2.xlsx sin dependencias externas
(parsea el OOXML con la stdlib) y emite:

  - tablas markdown  -> para wiki/investigacion/encuesta-resultados.md
  - figuras pgfplots -> para documento/chapters/figures/
  - tablas del anexo -> documento/chapters/appendix/encuesta-tablas.tex

Uso:  python3 scripts/analizar_encuesta.py
"""
import csv, os, re, sys, zipfile, collections, datetime
from xml.etree import ElementTree as ET

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(ROOT, 'raw/investigacion/encuesta-desinformacion-v2.xlsx')


# ---------------------------------------------------------------- lectura

def leer_xlsx(path):
    z = zipfile.ZipFile(path)
    shared = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall(NS + 'si'):
            shared.append(''.join(t.text or '' for t in si.iter(NS + 't')))

    def col(ref):
        n = 0
        for c in re.match(r'([A-Z]+)', ref).group(1):
            n = n * 26 + ord(c) - 64
        return n - 1

    filas = []
    for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).iter(NS + 'row'):
        celdas = {}
        for c in row.findall(NS + 'c'):
            v, t = c.find(NS + 'v'), c.get('t')
            if t == 'inlineStr':
                nodo = c.find(NS + 'is')
                val = ''.join(x.text or '' for x in nodo.iter(NS + 't')) if nodo is not None else ''
            elif v is None:
                val = ''
            elif t == 's':
                val = shared[int(v.text)]
            else:
                val = v.text
            celdas[col(c.get('r'))] = val
        if celdas:
            filas.append([celdas.get(i, '') for i in range(max(celdas) + 1)])
    # Las filas con celdas finales vacías vienen truncadas: se completan.
    ancho = len(filas[0])
    return filas[0], [f + [''] * (ancho - len(f)) for f in filas[1:]]


def fecha_excel(serial):
    return datetime.datetime(1899, 12, 30) + datetime.timedelta(days=float(serial))


# ------------------------------------------------------------- estructura

# (índice de columna, etiqueta corta, tipo, orden de las categorías)
LIKERT = ['1', '2', '3', '4', '5']
PREGUNTAS = [
    (1,  'edad',        'unica',  ['Menos de 18', '18-25', '26-33', '34-40', 'Más de 40']),
    (2,  'uso_x',       'unica',  ['Varias veces al día', 'Una vez al día', 'Algunas veces por semana', 'Rara vez', 'No la uso']),
    (3,  'sigue_pol',   'unica',  ['Sí, frecuentemente', 'A veces', 'No']),
    (4,  'exposicion',  'unica',  ['Muy frecuentemente', 'Frecuentemente', 'A veces', 'Rara vez', 'Nunca']),
    (5,  'compartio',   'unica',  ['Sí, lo compartí', 'Estuve a punto pero no lo hice', 'No', 'No sé']),
    (6,  'preocupa',    'likert', LIKERT),
    (7,  'capacidad',   'likert', LIKERT),
    (8,  'que_hace',    'multi',  None),
    (9,  'tiempo',      'unica',  ['Menos de 1 minuto', '1-3 minutos', 'Más de 3 minutos', 'No verifico']),
    (10, 'intencion',   'likert', LIKERT),
    (11, 'confianza',   'likert', LIKERT),
    (12, 'drivers',     'multi',  None),
    (13, 'preocupac',   'multi',  None),
]
ABIERTA = 14

# El segmento objetivo declarado en el diseño del instrumento.
EDADES_SEGMENTO = {'18-25', '26-33', '34-40'}


def en_segmento(fila):
    return (fila[1] in EDADES_SEGMENTO
            and fila[2] != 'No la uso'
            and fila[3] != 'No')


def opciones_multi(valor):
    """La opción 'Nada, sigo de largo' lleva una coma propia: se re-une."""
    partes = [p.strip() for p in valor.split(',') if p.strip()]
    salida, i = [], 0
    while i < len(partes):
        if partes[i] == 'Nada' and i + 1 < len(partes) and partes[i + 1] == 'sigo de largo':
            salida.append('Nada, sigo de largo')
            i += 2
        else:
            salida.append(partes[i])
            i += 1
    return salida


def contar(datos, idx, tipo, orden):
    if tipo == 'multi':
        c = collections.Counter()
        for f in datos:
            c.update(opciones_multi(f[idx]))
        return c.most_common()
    c = collections.Counter(f[idx] for f in datos if f[idx])
    if tipo == 'likert':
        # Una escala se lee mal si le faltan puntos: se muestran los cinco.
        return [(k, c.get(k, 0)) for k in orden]
    claves = [k for k in orden if k in c] + sorted(k for k in c if k not in orden)
    return [(k, c[k]) for k in claves]


def media(datos, idx):
    vals = [int(f[idx]) for f in datos if f[idx].isdigit()]
    return sum(vals) / len(vals) if vals else 0.0


# ----------------------------------------------------------------- salida

def tabla_md(pares, total, titulo_col='Respuesta'):
    out = [f'| {titulo_col} | n | % |', '|---|---:|---:|']
    for k, v in pares:
        out.append(f'| {k} | {v} | {100 * v / total:.1f}% |')
    return '\n'.join(out)


ESC = {'%': r'\\%', '&': r'\\&', '#': r'\\#', '_': r'\\_'}


def esc(t):
    for k, v in ESC.items():
        t = t.replace(k, v)
    return t


CABECERA = '% Generado por scripts/analizar_encuesta.py — no editar a mano.\n'


# El eje no admite el texto literal de las opciones sin que las etiquetas se
# pisen entre sí. Se abrevian aquí; el enunciado completo va en el anexo.
ABREVIA = {
    'Que no tenga sesgo político': 'Ausencia de sesgo político',
    'Que muestre las fuentes/evidencia': 'Exhibición de la evidencia',
    'Que explique por qué llega a ese resultado': 'Explicación del resultado',
    'Que sea transparente sobre su margen de error': 'Transparencia sobre el error',
    'Que la respalde una institución reconocida': 'Respaldo institucional',
    'Que sea open source': 'Código abierto',
    'Que se equivoque (falsos positivos)': 'Error de clasificación',
    'Que censure opiniones o sátira': 'Censura de opiniones o sátira',
    'Privacidad de mis datos': 'Privacidad de los datos',
    'Busco en Google': 'Búsqueda web',
    'Miro la cuenta que lo publicó': 'Revisión de la cuenta autora',
    'Comparo con medios que conozco': 'Comparación con medios conocidos',
    'Le pregunto a alguien': 'Consulta a otra persona',
    'Nada, sigo de largo': 'Ninguna acción',
}


def num(v):
    """Coma decimal, como corresponde al castellano del documento."""
    return f'{v:.1f}'.replace('.', ',')


def barras_h(pares, base, ancho=11.8):
    """Barras horizontales con el porcentaje al final de cada barra."""
    etiquetas = [esc(ABREVIA.get(k, k)) for k, _ in pares]
    pct = [100 * v / base for _, v in pares]
    n = len(pares)
    alto = max(3.2, 0.95 * n)
    coords = ' '.join(f'({p:.1f},{i}) [{num(p)}\\%]' for i, p in enumerate(pct))
    return CABECERA + f"""\\begin{{tikzpicture}}
  \\begin{{axis}}[
      xbar, width={ancho}cm, height={alto:.1f}cm,
      xmin=0, xmax={max(pct) * 1.30:.0f},
      bar width=12pt, y dir=reverse,
      enlarge y limits={{abs=0.7}},
      axis lines*=left, axis line style={{draw=black!30}},
      xmajorgrids, grid style={{draw=black!10}},
      tick align=outside, tick style={{draw=black!30}},
      xlabel={{Porcentaje de respuestas}}, xlabel style={{font=\\footnotesize}},
      xticklabel={{\\pgfmathprintnumber{{\\tick}}\\%}},
      ticklabel style={{font=\\footnotesize}},
      ytick={{{','.join(str(i) for i in range(n))}}},
      yticklabels={{{','.join('{' + e + '}' for e in etiquetas)}}},
      yticklabel style={{align=right, text width=4.8cm, font=\\footnotesize}},
      nodes near coords, point meta=explicit symbolic,
      nodes near coords align={{horizontal}},
      every node near coord/.append style={{font=\\scriptsize, color=black!65,
        anchor=west, xshift=2pt}},
  ]
    \\addplot[fill=encuestaBar, draw=none] coordinates {{{coords}}};
  \\end{{axis}}
\\end{{tikzpicture}}
"""


def likert_par(serie_a, serie_b, etiqueta_a, etiqueta_b, base):
    """Dos escalas Likert 1-5 superpuestas, para contrastarlas."""
    def pts(serie):
        return ' '.join(
            f'({i},{100 * serie.get(str(i), 0) / base:.1f}) [{num(100 * serie.get(str(i), 0) / base)}\\%]'
            for i in range(1, 6))
    a, b = pts(serie_a), pts(serie_b)
    tope = max(max(serie_a.values()), max(serie_b.values())) * 100 / base
    return CABECERA + f"""\\begin{{tikzpicture}}
  \\begin{{axis}}[
      ybar, width=13.2cm, height=6.4cm,
      ymin=0, ymax={tope * 1.42:.0f},
      bar width=15pt, enlarge x limits={{abs=0.8}},
      axis lines*=left, axis line style={{draw=black!30}},
      ymajorgrids, grid style={{draw=black!10}},
      tick align=outside, tick style={{draw=black!30}},
      xlabel={{Valoración en escala de 1 a 5}},
      ylabel={{Porcentaje de respuestas}},
      xlabel style={{font=\\footnotesize}}, ylabel style={{font=\\footnotesize}},
      yticklabel={{\\pgfmathprintnumber{{\\tick}}\\%}},
      ticklabel style={{font=\\footnotesize}},
      xtick={{1,2,3,4,5}},
      legend style={{at={{(0.5,-0.22)}}, anchor=north, legend columns=2,
                     draw=black!20, font=\\footnotesize}},
      nodes near coords, point meta=explicit symbolic,
      every node near coord/.append style={{font=\\scriptsize, color=black!65,
        rotate=90, anchor=west, yshift=1pt}},
  ]
    \\addplot[fill=encuestaBar, draw=none] coordinates {{{a}}};
    \\addplot[fill=encuestaBarAlt, draw=none] coordinates {{{b}}};
    \\legend{{{esc(etiqueta_a)}, {esc(etiqueta_b)}}}
  \\end{{axis}}
\\end{{tikzpicture}}
"""


def escribir_figuras(filas, seg):
    dest = os.path.join(ROOT, 'documento/chapters/figures')
    n = len(seg)
    figuras = {}

    figuras['encuesta-exposicion'] = barras_h(
        contar(seg, 4, 'unica', dict(PREGUNTAS_POR_IDX)[4]), n)
    figuras['encuesta-verificacion'] = barras_h(
        contar(seg, 9, 'unica', dict(PREGUNTAS_POR_IDX)[9]), n)
    figuras['encuesta-drivers'] = barras_h(
        [p for p in contar(seg, 12, 'multi', None) if p[1] >= 5], n)
    figuras['encuesta-preocupaciones'] = barras_h(
        [p for p in contar(seg, 13, 'multi', None) if p[1] >= 5], n)

    intencion = collections.Counter(f[10] for f in seg if f[10])
    confianza = collections.Counter(f[11] for f in seg if f[11])
    figuras['encuesta-intencion-confianza'] = likert_par(
        intencion, confianza,
        'Intención de instalar y usar la extensión',
        'Confianza en un puntaje generado automáticamente', n)

    for nombre, cuerpo in figuras.items():
        ruta = os.path.join(dest, nombre + '.tex')
        with open(ruta, 'w') as fh:
            fh.write(cuerpo)
        print(f'  escrito  documento/chapters/figures/{nombre}.tex')


PREGUNTAS_POR_IDX = [(i, orden) for i, _, _, orden in PREGUNTAS]

# Temas de la pregunta abierta. Cada tema lista las respuestas textuales que
# agrupa, de modo que el conteo se pueda verificar contra la planilla. Lo que
# no entra en ningún tema va a «Otras (una mención cada una)».
TEMAS = [
    ('Detectar imágenes generadas con IA', ['detectar imagenes generadas con ia']),
    ('Avisar si un contenido viejo recircula como nuevo',
     ['Que me diga cuando algo es viejo y lo estan recirculando como nuevo']),
    ('Mostrar las fuentes o la evidencia',
     ['Que me muestre las fuentes en el momento',
      'Ver las fuentes al lado del tuit sin salir de X',
      'Que te muestre posts donde se evidencia la verdad sobre la fake news']),
    ('No recargar la pantalla', ['Que no me llene la pantalla de carteles']),
    ('Contrastar más de una fuente o postura',
     ['Que muestre las dos campanas y no una sola',
      'Que no dependa de un solo medio para decidir si algo es falso']),
    ('Distinguir opinión o sátira de un dato falso',
     ['Que distinga entre una opinion y un dato falso',
      'Que distinga sátira de noticia falsa']),
    ('Ahorrar el tiempo de buscar en Google',
     ['Ahorrarme el tiempo de googlear cada cosa',
      'Que me ahorre el tiempo de googlear todo']),
    ('Avisar de títulos \\textit{clickbait}',
     ['Que avise de titulos clickbait aunque la nota no sea falsa']),
    ('Efectividad', ['Efectividad', 'Efectividad y que sea rapida']),
    ('Facilidad de uso', ['Que sea facil de usar, sin tener que configurar nada']),
    ('Sin un pedido concreto',
     ['no lo se', 'La verdad no se, capaz que me sirva para no comerme fake news']),
]
OTRAS = 'Otras (una mención cada una)'


def contar_temas(filas):
    """[(tema, total, segmento)] sobre las respuestas abiertas no vacías."""
    tema_de = {r: t for t, rs in TEMAS for r in rs}
    tot, seg = collections.Counter(), collections.Counter()
    for f in filas:
        r = f[ABIERTA].strip()
        if not r:
            continue
        t = tema_de.get(r, OTRAS)
        tot[t] += 1
        seg[t] += en_segmento(f)
    orden = [t for t, _ in TEMAS] + [OTRAS]
    pares = sorted(((t, tot[t], seg[t]) for t in orden if tot[t]),
                   key=lambda x: (x[0] in (OTRAS, 'Sin un pedido concreto'), -x[1]))
    assert sum(x[1] for x in pares) == sum(1 for f in filas if f[ABIERTA].strip())
    return pares


def pct(a, b):
    return num(100 * a / b)


def tablas_anexo(cab, filas, seg):
    """Tablas compactas de frecuencias para el Anexo A."""
    N, n = len(filas), len(seg)
    out = [CABECERA]

    def bloque(idxs, titulo, etiqueta, nota):
        out.append('\\begin{table}[t]\n  \\centering\\small')
        out.append(f'  \\caption{{{titulo} {nota} Fuente: elaboración propia.}}')
        out.append(f'  \\label{{{etiqueta}}}')
        out.append('  \\begin{tabular}{l >{\\raggedright\\arraybackslash}p{8.4cm} rr}')
        out.append('    \\hline\n    \\textbf{Pregunta} & \\textbf{Respuesta} & \\textbf{Casos} & \\textbf{\\%} \\\\\n    \\hline')
        for idx in idxs:
            _, nombre, tipo, orden = PREGUNTAS[idx - 1]
            base = filas if idx in (1, 2, 3) else seg
            pares = contar(base, idx, tipo, orden)
            for j, (k, v) in enumerate(pares):
                preg = f'P{idx} (n = {len(base)})' if j == 0 else ''
                out.append(f'    {preg} & {esc(k)} & {v} & {pct(v, len(base))} \\\\')
            out.append('    \\hline')
        out.append('  \\end{tabular}\n\\end{table}\n')

    bloque([1, 2, 3, 4, 5, 9], 'Frecuencias de las preguntas de opción única.',
           'tab:enc-unica', f'P1 a P3 sobre las {N} respuestas; P4 en adelante, sobre las {n} del segmento.')
    bloque([8, 12, 13], 'Frecuencias de las preguntas de opción múltiple.',
           'tab:enc-multiple', f'Los porcentajes se calculan sobre las {n} respuestas del segmento y suman más de cien.')

    out.append('\\begin{table}[t]\n  \\centering\\small')
    out.append(f'  \\caption{{Distribución de las escalas de 1 a 5, en porcentaje sobre las {n} respuestas del segmento. Fuente: elaboración propia.}}')
    out.append('  \\label{tab:enc-likert}')
    out.append('  \\begin{tabular}{lrrrrrr}')
    out.append('    \\hline\n    \\textbf{Pregunta} & \\textbf{1} & \\textbf{2} & \\textbf{3} & \\textbf{4} & \\textbf{5} & \\textbf{Media} \\\\\n    \\hline')
    for idx, nombre in [(6, 'P6. Preocupación'), (7, 'P7. Capacidad autopercibida'),
                        (10, 'P10. Intención de uso'), (11, 'P11. Confianza en el puntaje')]:
        c = collections.Counter(f[idx] for f in seg)
        celdas = ' & '.join(pct(c.get(k, 0), n) for k in LIKERT)
        m = f'{media(seg, idx):.2f}'.replace('.', ',')
        out.append(f'    {nombre} & {celdas} & {m} \\\\')
    out.append('    \\hline\n  \\end{tabular}\n\\end{table}\n')

    temas = contar_temas(filas)
    ab_tot = sum(t for _, t, _ in temas)
    ab_seg = sum(s for _, _, s in temas)
    out.append('\\begin{table}[t]\n  \\centering\\small')
    out.append(f'  \\caption{{Temas de la pregunta abierta (P14), agrupados por respuestas de texto idéntico o de igual pedido. Fuente: elaboración propia.}}')
    out.append('  \\label{tab:enc-temas}')
    out.append('  \\begin{tabular}{lrr}')
    out.append(f'    \\hline\n    \\textbf{{Tema}} & \\textbf{{Total (n = {ab_tot})}} & \\textbf{{Segmento (n = {ab_seg})}} \\\\\n    \\hline')
    for t, a, b in temas:
        out.append(f'    {t} & {a} & {b} \\\\')
    out.append('    \\hline\n  \\end{tabular}\n\\end{table}\n')

    ruta = os.path.join(ROOT, 'documento/chapters/appendix/encuesta-tablas.tex')
    with open(ruta, 'w') as fh:
        fh.write('\n'.join(out))
    print('  escrito  documento/chapters/appendix/encuesta-tablas.tex')


def cifras_texto(filas, seg):
    """Cifras derivadas que cita el texto del documento y del wiki."""
    N, n = len(filas), len(seg)
    def cuenta(base, idx, vals):
        return sum(1 for f in base if f[idx] in vals)
    edad = cuenta(filas, 1, EDADES_SEGMENTO)
    multi12 = dict(contar(seg, 12, 'multi', None))
    d = [
        ('respuestas totales', N, ''),
        ('segmento', n, pct(n, N)),
        ('edad 18-40 (sobre N)', edad, pct(edad, N)),
        ('fuera por edad', N - edad, ''),
        ('uso diario (sobre N)', cuenta(filas, 2, {'Varias veces al día', 'Una vez al día'}), pct(cuenta(filas, 2, {'Varias veces al día', 'Una vez al día'}), N)),
        ('sigue política (sobre N)', cuenta(filas, 3, {'Sí, frecuentemente', 'A veces'}), pct(cuenta(filas, 3, {'Sí, frecuentemente', 'A veces'}), N)),
        ('exposición frecuente o muy', cuenta(seg, 4, {'Muy frecuentemente', 'Frecuentemente'}), pct(cuenta(seg, 4, {'Muy frecuentemente', 'Frecuentemente'}), n)),
        ('compartió o casi', cuenta(seg, 5, {'Sí, lo compartí', 'Estuve a punto pero no lo hice'}), pct(cuenta(seg, 5, {'Sí, lo compartí', 'Estuve a punto pero no lo hice'}), n)),
        ('preocupación 4-5', cuenta(seg, 6, {'4', '5'}), pct(cuenta(seg, 6, {'4', '5'}), n)),
        ('capacidad 1-3', cuenta(seg, 7, {'1', '2', '3'}), pct(cuenta(seg, 7, {'1', '2', '3'}), n)),
        ('verifica en menos de 3 min', cuenta(seg, 9, {'Menos de 1 minuto', '1-3 minutos'}), pct(cuenta(seg, 9, {'Menos de 1 minuto', '1-3 minutos'}), n)),
        ('intención 4-5', cuenta(seg, 10, {'4', '5'}), pct(cuenta(seg, 10, {'4', '5'}), n)),
        ('confianza 4-5', cuenta(seg, 11, {'4', '5'}), pct(cuenta(seg, 11, {'4', '5'}), n)),
        ('dif. sesgo - fuentes (puntos)', '', num(100 * (multi12['Que no tenga sesgo político'] - multi12['Que muestre las fuentes/evidencia']) / n)),
        ('dif. sesgo - explicación (puntos)', '', num(100 * (multi12['Que no tenga sesgo político'] - multi12['Que explique por qué llega a ese resultado']) / n)),
        ('dif. intención - confianza (media)', '', f'{media(seg, 10) - media(seg, 11):.2f}'.replace('.', ',')),
        ('abiertas respondidas (sobre N)', sum(1 for f in filas if f[ABIERTA].strip()), ''),
        ('abiertas del segmento', sum(1 for f in seg if f[ABIERTA].strip()), ''),
    ]
    print('## cifras derivadas para el texto')
    for k, a, b in d:
        print(f'   {k:36s} {a!s:>5}  {b}')
    print()
    print('## temas de la pregunta abierta (total, segmento)')
    for t, a, b in contar_temas(filas):
        print(f'   {a:3d} {b:3d}  {t}')
    print()



def main():
    cab, filas = leer_xlsx(XLSX)
    total = len(filas)
    seg = [f for f in filas if en_segmento(f)]
    fechas = [fecha_excel(f[0]) for f in filas if f[0]]

    print(f'# Encuesta — resumen de cómputo')
    print(f'respuestas recibidas : {total}')
    print(f'dentro de segmento   : {len(seg)} ({100*len(seg)/total:.1f}%)')
    print(f'campo                : {min(fechas):%Y-%m-%d} a {max(fechas):%Y-%m-%d}')
    print(f'abiertas respondidas : {sum(1 for f in filas if f[ABIERTA].strip())}')
    print()

    for idx, nombre, tipo, orden in PREGUNTAS:
        base = filas if idx in (1, 2, 3) else seg
        n = len(base)
        print(f'## [{idx}] {nombre} — {cab[idx][:80]}  (base n={n})')
        pares = contar(base, idx, tipo, orden)
        for k, v in pares:
            print(f'   {v:4d}  {100*v/n:5.1f}%  {k}')
        if tipo == 'likert':
            print(f'   media = {media(base, idx):.2f}')
        print()

    # Cruces
    print('## cruce capacidad autopercibida x confianza en el score (segmento)')
    for cap in LIKERT:
        sub = [f for f in seg if f[7] == cap]
        if sub:
            print(f'   capacidad={cap}  n={len(sub):3d}  confianza media={media(sub,11):.2f}  intención media={media(sub,10):.2f}')
    print()
    print('## cruce edad x intención de uso (segmento)')
    for e in ['18-25', '26-33', '34-40']:
        sub = [f for f in seg if f[1] == e]
        if sub:
            print(f'   {e}  n={len(sub):3d}  intención media={media(sub,10):.2f}  confianza media={media(sub,11):.2f}')
    print()
    print('## cruce exposición x preocupación (segmento)')
    for ex in ['Muy frecuentemente', 'Frecuentemente', 'A veces', 'Rara vez', 'Nunca']:
        sub = [f for f in seg if f[4] == ex]
        if sub:
            print(f'   {ex:20s} n={len(sub):3d}  preocupación media={media(sub,6):.2f}')
    print()
    print('## respuestas abiertas (segmento)')
    for f in seg:
        if f[ABIERTA].strip():
            print(f'   - {f[ABIERTA].strip()}')
    print()
    cifras_texto(filas, seg)
    print('## figuras')
    escribir_figuras(filas, seg)
    tablas_anexo(cab, filas, seg)


if __name__ == '__main__':
    main()
