from collections import Counter
import matplotlib.pyplot as plt

def estadisticas_producto(data, key):

    tipos = [fila.get(key, '').strip().upper() for fila in data if fila.get(key)]
    conteo = Counter(tipos)

    tipos = list(conteo.keys())
    cantidades = list(conteo.values())

    plt.figure(figsize=(8, 5))
    plt.bar(tipos, cantidades)
    plt.title('Cantidad de productos por tipo')
    plt.xlabel('Tipo de producto')
    plt.ylabel('Cantidad')
    plt.tight_layout()
    plt.show()