from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DejaVu Sans'

def estadisticas_journals(data, key):

    def abreviar_nombre(nombre, max_palabras=7, max_chars=40):
        palabras = nombre.split()
        if len(palabras) > max_palabras or len(nombre) > max_chars:
            return ' '.join(palabras[:max_palabras])[:max_chars].rstrip() + '...'
        return nombre

    # Filtra y limpia los valores no vacíos
    valores = [fila.get(key, '').strip() for fila in data if fila.get(key, '').strip()]
    if not valores:
        print(f"No se encontraron datos válidos en la columna '{key}'.")
        return

    # Cuenta los valores más comunes
    conteo = Counter(valores).most_common(15)
    conteo = [(nombre, int(cantidad)) for nombre, cantidad in conteo]
    
    # Abrevia nombres si son largos
    nombres_abreviados = [abreviar_nombre(nombre) for nombre, _ in conteo]
    cantidades = [cantidad for _, cantidad in conteo]

    # Gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
    ax.bar(nombres_abreviados, cantidades)
    ax.set_title(f'Top 15 más frecuentes en: {key}')
    ax.set_xlabel(key.capitalize())
    ax.set_ylabel('Cantidad de productos')
    plt.xticks(rotation=45, ha='right')
    

    return fig