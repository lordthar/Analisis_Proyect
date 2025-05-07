from collections import Counter
import matplotlib.pyplot as plt

def estadisticas_publisher(data, key):

    # Obtener todos los publishers no vacíos
    publishers = [fila.get(key, '').strip() for fila in data if fila.get(key, '').strip()]
    
    if not publishers:
        print("No hay editoriales válidas en los datos.")
        return

    conteo = Counter(publishers).most_common(15)

    # Preparar datos para gráfico
    nombres = [nombre for nombre, _ in conteo]
    cantidades = [int(cantidad) for _, cantidad in conteo]

    # Mostrar gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(nombres, cantidades)
    plt.title("Top 15 Editoriales (Publishers)")
    plt.xlabel("Editorial")
    plt.ylabel("Cantidad de productos")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()