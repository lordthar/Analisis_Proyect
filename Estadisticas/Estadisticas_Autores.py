import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter

plt.rcParams['font.family'] = 'DejaVu Sans'

def estadisticas_autores(data, key):

    def obtener_primer_autor(authors_str):
        if not authors_str:
            return None
        partes = [a.strip() for a in authors_str.split(',')]
        if len(partes) >= 2:
            apellido = partes[0]
            nombre = partes[1]
            return f"{nombre} {apellido}"
        return None


    primeros_autores = []

    for fila in data:
        autores = fila.get(key, "")
        primer_autor = obtener_primer_autor(autores)
        if primer_autor:
            primeros_autores.append(primer_autor)

    # Contar frecuencia de autores
    conteo = Counter(primeros_autores).most_common(15)

    nombres = [nombre for nombre, _ in conteo]
    valores = [cantidad for _, cantidad in conteo]

    # Graficar
    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
    ax.bar(nombres, valores)
    ax.set_title('Top 15 primeros autores por cantidad de productos')
    ax.set_xlabel('Primer autor')
    ax.set_ylabel('Cantidad de productos')
    plt.xticks(rotation=45, ha='right')

    return fig