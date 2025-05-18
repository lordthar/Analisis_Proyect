from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DejaVu Sans'


def estadisticas_producto(data, key):

    tipos = [fila.get(key, '').strip().upper() for fila in data if fila.get(key)]
    conteo = Counter(tipos)

    tipos = list(conteo.keys())
    cantidades = list(conteo.values())

    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    ax.bar(tipos, cantidades)
    ax.set_title('Cantidad de productos por tipo')
    ax.set_xlabel('Tipo de producto')
    ax.set_ylabel('Cantidad')
    

    return fig