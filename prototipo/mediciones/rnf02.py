"""RNF-02: latencia de extremo a extremo de /analizar sin caché (tweet_id nuevo)."""
import json, statistics, sys, time, urllib.request, uuid
TUITS = [
 "El INDEC informó que la inflación de septiembre fue del 2,1 % mensual.",
 "Confirman que desde enero el subte de Buenos Aires va a costar 3000 pesos el viaje.",
 "La Corte Suprema declaró inconstitucional la reforma laboral completa.",
 "Argentina exportó más litio que Chile en 2025, según datos oficiales.",
 "El Banco Central eliminó el cepo cambiario para personas físicas.",
 "Messi anunció que se retira de la selección después del Mundial 2026.",
 "La pobreza bajó al 31 % en el primer semestre según el INDEC.",
 "El gobierno cerró el CONICET por decreto esta mañana.",
 "Desde mañana es obligatorio llevar la VTV impresa en todo el país.",
 "El dengue ya causó más de 500 muertes en Argentina en lo que va del año.",
 "Aprobaron en el Senado la baja de la edad de imputabilidad a 14 años.",
 "La AFIP dejó de existir y fue reemplazada por ARCA.",
 "En Mendoza nevó en pleno enero por primera vez en la historia.",
 "El salario mínimo quedó por encima de los 300 mil pesos.",
 "YPF descubrió un nuevo yacimiento en Vaca Muerta que duplica las reservas del país.",
 "La vacuna contra el COVID altera el ADN, lo confirmó un estudio del Malbrán.",
 "El desempleo en Argentina subió al 7,6 % en el segundo trimestre.",
 "Aerolíneas Argentinas fue privatizada y vendida a una empresa chilena.",
 "La ciudad de Buenos Aires prohibió los monopatines eléctricos en la calle.",
 "El Congreso aprobó el presupuesto 2026 con déficit cero.",
]
URL = "http://localhost:8000/analizar"
res = []
for t in TUITS:
    cuerpo = {"tweet_id": "rnf02-" + uuid.uuid4().hex[:12], "texto": t, "handle": "@medicion",
              "verificada": False, "metricas": {}}
    pedido = urllib.request.Request(URL, json.dumps(cuerpo).encode(), {"Content-Type": "application/json"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(pedido, timeout=120) as r:
        d = json.load(r)
    s = time.perf_counter() - t0
    res.append(s)
    print(f"{s:6.2f} s  {d.get('veredicto')}  parcial={d.get('parcial', d.get('es_parcial'))}  {t[:50]}", flush=True)
res.sort()
p95 = res[min(len(res)-1, int(round(0.95*len(res)+0.5))-1)]
print(f"n={len(res)} mediana={statistics.median(res):.2f} p95={p95:.2f} max={res[-1]:.2f}")
