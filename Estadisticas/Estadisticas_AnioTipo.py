import matplotlib.pyplot as plt
from collections import defaultdict

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
    
    # Preparar para graficar
    tipos = sorted(clasificacion)
    anios = [str(a) for a in range(anio_inicio, anio_fin + 1)]

    for tipo in tipos:
        valores = [conteo.get((tipo, anio), 0) for anio in anios]
        plt.plot(anios, valores, marker='o', label=tipo)

    plt.title(f'Productos por Año ({anio_inicio}-{anio_fin}) y Tipo')
    plt.xlabel('Año')
    plt.ylabel('Cantidad de productos')
    plt.legend(title='Tipo')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()