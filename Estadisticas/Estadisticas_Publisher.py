from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DejaVu Sans'


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
    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
    ax.bar(nombres, cantidades)
    ax.set_title("Top 15 Editoriales (Publishers)")
    ax.set_xlabel("Editorial")
    ax.set_ylabel("Cantidad de productos")
    plt.xticks(rotation=45, ha='right')
    

    return fig 