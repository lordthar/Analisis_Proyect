import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict

plt.rcParams['font.family'] = 'DejaVu Sans'


def estadisticas_aniotipo(data, key):
    anio_key = 'year'
    anio_inicio = 2015
    anio_fin = 2025

    clasificacion = {'JOUR', 'CONF', 'CHAP', 'BOOK'}
    conteo = defaultdict(int)

    for fila in data:
        tipo = fila.get(key, '').strip().upper()
        anio_str = fila.get(anio_key, '').strip()

        if tipo in clasificacion and anio_str.isdigit():
            anio = int(anio_str)
            if anio_inicio <= anio <= anio_fin:
                clave = (tipo, str(anio))
                conteo[clave] += 1

    tipos = sorted(clasificacion)
    anios = [str(a) for a in range(anio_inicio, anio_fin + 1)]

    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    for tipo in tipos:
        valores = [conteo.get((tipo, anio), 0) for anio in anios]
        ax.plot(anios, valores, marker='o', label=tipo)

    ax.set_title(f"Productos por Año ({anio_inicio}-{anio_fin}) y Tipo")
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad de productos")
    ax.legend(title="Tipo")

    plt.xticks(rotation=45)

    return fig
