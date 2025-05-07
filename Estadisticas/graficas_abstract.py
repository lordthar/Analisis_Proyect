import matplotlib.pyplot as plt
import numpy as np
import time
import heapq
import tabulate
from copy import deepcopy


 #------------------------------------------------- METODOS ------------------------------------------------------------
# Función de ordenamiento (Insertion Sort)
def insertion_sort(arr, left, right, key):
    for i in range(left + 1, right + 1):
        temp = arr[i]
        j = i - 1
        while j >= left and arr[j][key] > temp[key]:  # Ordenar por clave
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = temp
#-------------------------------------------------------------------------------------
# Gnome Sort
def gnome_sort(arr, key):
        sorted_arr = [{**item, key: int(item[key])} for item in arr]  # Convertir claves a enteros sin modificar original
        i = 1
        while i < len(sorted_arr):
            if sorted_arr[i - 1][key] <= sorted_arr[i][key]:  
                i += 1
            else:
                sorted_arr[i - 1], sorted_arr[i] = sorted_arr[i], sorted_arr[i - 1]  # Intercambio
                if i > 1:
                    i -= 1
                else:
                    i += 1
        return sorted_arr
#------------------------------------------------------------
# Merge
def merge(arr, left, mid, right, key):
    L = arr[left:mid + 1]
    R = arr[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(L) and j < len(R):
        if L[i][key] <= R[j][key]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1
    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1
# TimSort
def timsort(arr, key):
    min_run = 32
    n = len(arr)
    for i in range(0, n, min_run):
        insertion_sort(arr, i, min((i + min_run - 1), n - 1), key)
    size = min_run
    while size < n:
        for start in range(0, n, size * 2):
            mid = min(n - 1, start + size - 1)
            end = min((start + size * 2 - 1), (n - 1))
            if mid < end:
                merge(arr, start, mid, end, key)
        size = size * 2
    return arr
#-----------------------------------------------------------------------------
# CombSort
def comb_sort(arr, key):
    gap = len(arr)
    swapped = True
    while gap > 1 or swapped:
        gap = max(1, int(gap / 1.3))  # Reduce el gap usando el factor 1.3
        swapped = False
        for i in range(len(arr) - gap):
            if arr[i][key] > arr[i + gap][key]:  # Comparar usando la clave
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
    return arr
#----------------------------------------------------------------------------------------------
# Selection Sort
def selection_sort(arr, key):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j][key] < arr[min_idx][key]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
#------------------------------------------------------------------------------------------------
# Tree
# se le agrega data para que almacene todo el diccionario y no solo un valor
def tree_sort(arr, key):
    class TreeNode:
        def __init__(self, data):
            self.data = data
            self.left = None
            self.right = None

    def insert(root, data):
        if root is None:
            return TreeNode(data)
        if data[key] < root.data[key]:
            root.left = insert(root.left, data) # compara usando la clave
        else:
            root.right = insert(root.right, data)
        return root

    def inorder(root, result):
        if root is not None:
            inorder(root.left, result)
            result.append(root.data)
            inorder(root.right, result)

    if not arr:
        return arr

    root = TreeNode(arr[0])
    for i in range(1, len(arr)):
        root = insert(root, arr[i])

    result = []
    inorder(root, result)
    return result
#-------------------------------------------------------------------------------------------
#Pigeonhole NO SIRVE PARA CADENAS

def pigeonhole_sort(arr, key_term):
    """Pigeonhole sort aplicado a abstracts basado en la presencia de un término clave."""
    if not arr:
        return arr  # Si la lista está vacía, simplemente retorna la lista vacía.

    # Inicializar los "agujeros" basados en el rango de valores posibles
    min_value = min(arr, key=lambda x: key_term.lower() in x.get("abstract", "").lower())
    max_value = max(arr, key=lambda x: key_term.lower() in x.get("abstract", "").lower())
    
    range_of_values = max_value - min_value + 1
    holes = [[] for _ in range(range_of_values)]  # Crear "agujeros"

    # Colocar cada artículo en su "agujero" correspondiente
    for item in arr:
        index = key_term.lower() in item.get("abstract", "").lower()
        holes[index].append(item)

    # Reconstruir la lista a partir de los "agujeros"
    result = []
    for hole in holes:
        result.extend(hole)
    
    return result

#--------------------------------------------------------------------
#bucket_sort
def bucket_sort_strings(strings):
    # Crear diccionario de buckets para cada letra (a-z)
    buckets = {chr(i): [] for i in range(ord('a'), ord('z') + 1)}

    # Colocar las cadenas en el bucket correspondiente según la primera letra
    for string in strings:
        if string:  # Evitar cadenas vacías
            first_char = string[0].lower()
            if first_char in buckets:
                buckets[first_char].append(string)
            else:
                buckets.setdefault(first_char, []).append(string)

    # Ordenar cada bucket y combinar los resultados
    sorted_strings = []
    for key in sorted(buckets):
        sorted_strings.extend(sorted(buckets[key]))

    return sorted_strings


#--------------------------------------------------------------------------------------
#QuickSort
def quicksort(arr, key):
    if len(arr) <= 1:
        return arr

    # Verificamos que cada elemento en 'arr' sea un diccionario con la clave proporcionada
    if not all(isinstance(x, dict) and key in x for x in arr):
        raise ValueError("Todos los elementos deben ser diccionarios con la clave proporcionada")

    pivot = arr[len(arr) // 2]  # Elegimos pivote
    pivot_value = str(pivot[key]).strip().lower()
    left = [x for x in arr if str(x[key]).strip().lower() < pivot_value]
    middle = [x for x in arr if str(x[key]).strip().lower() == pivot_value]
    right = [x for x in arr if str(x[key]).strip().lower() > pivot_value]

    return quicksort(left, key) + middle + quicksort(right, key)
#----------------------------------------------------------------------------------------
#heap_sort

def heap_sort(arr, key):
    try:
        # Convertimos la lista en una lista de tuplas (clave de orden, objeto completo)
        heap = [(str(x.get(key, "")).lower(), x) for x in arr]
        heapq.heapify(heap)  # Convertimos en heap

        # Extraemos los elementos ordenados
        sorted_arr = [heapq.heappop(heap)[1] for _ in range(len(heap))]
        return sorted_arr
    except Exception as e:
        print(f"Error en heap_sort: {e}")
    return []
#----------------------------------------------------------------------------------------
#bitonic
def bitonic_sort(arr, key):
    def compare_and_swap(arr, i, j, direction):
        if (arr[i][key] > arr[j][key] and direction == 1) or (arr[i][key] < arr[j][key] and direction == 0):
            arr[i], arr[j] = arr[j], arr[i]

    def bitonic_merge(arr, low, length, direction):
        if length > 1:
            k = length // 2
            for i in range(low, low + k):
                compare_and_swap(arr, i, i + k, direction)
            bitonic_merge(arr, low, k, direction)
            bitonic_merge(arr, low + k, k, direction)

    def bitonic_sort_recursive(arr, low, length, direction):
        if length > 1:
            k = length // 2
            bitonic_sort_recursive(arr, low, k, 1)  # Ascending order
            bitonic_sort_recursive(arr, low + k, k, 0)  # Descending order
            bitonic_merge(arr, low, length, direction)

    bitonic_sort_recursive(arr, 0, len(arr), 1)
    return arr
#------------------------------------------------------------------------------------------
# Binaryinsertion
def binary_insertion_sort(arr, key):
    def binary_search(arr, val, low, high):
        while low <= high:
            mid = (low + high) // 2
            if val[key] < arr[mid][key]:
                high = mid - 1
            else:
                low = mid + 1
        return low

    for i in range(1, len(arr)):
        val = arr[i]
        j = binary_search(arr, val, 0, i - 1)
        arr = arr[:j] + [val] + arr[j:i] + arr[i + 1:]
    
    return arr
#-----------------------------------------------------------------------------------------
# Radix
def radix_sort(arr, key):
    max_length = max(len(item[key]) for item in arr)  # Longitud máxima del texto

    for pos in range(max_length - 1, -1, -1):  # Recorrer de derecha a izquierda
        buckets = {}  # Diccionario para manejar cualquier carácter Unicode

        for item in arr:
            char = item[key][pos] if pos < len(item[key]) else ""  # Tomar carácter o vacío
            if char not in buckets:
                buckets[char] = []  # Crear bucket si no existe
            buckets[char].append(item)

        # Reconstruir la lista en orden
        arr = [item for char in sorted(buckets.keys()) for item in buckets[char]]

    return arr

def bubble_sort(arr, key):
    """Bubble sort aplicado a abstracts basado en la presencia de un término clave"""
    n = len(arr)
    arr_copy = deepcopy(arr)  # Hacemos una copia del arreglo para no modificar el original
    
    for i in range(n):
        # Se utiliza una bandera (swapped) para optimizar el algoritmo, si no hubo intercambio, terminamos antes
        swapped = False
        for j in range(0, n - i - 1):
            # Evaluamos si el término está presente en los abstracts
            term_in_j = key.lower() in arr_copy[j].get("abstract", "").lower()
            term_in_j1 = key.lower() in arr_copy[j + 1].get("abstract", "").lower()
            
            # Si el término está en j+1 pero no en j, intercambiamos
            if term_in_j1 and not term_in_j:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
        
        # Si no hubo intercambios, podemos salir temprano (la lista ya está ordenada)
        if not swapped:
            break
    
    return arr_copy

def burbuja_doble_keywords(arr, key):
    n = len(arr)
    arr_copy = deepcopy(arr)  # Hacemos una copia del arreglo para no modificar el original
    
    swapped = True
    start = 0
    end = n - 1

    while swapped:
        # Resetear la bandera de intercambio al iniciar cada iteración
        swapped = False
        
        # Recorrido de izquierda a derecha
        for i in range(start, end):
            # Evaluamos si el término está presente en los abstracts
            term_in_i = key.lower() in arr_copy[i].get("abstract", "").lower()
            term_in_i1 = key.lower() in arr_copy[i + 1].get("abstract", "").lower()
            
            # Si el término está en i+1 pero no en i, intercambiamos
            if term_in_i1 and not term_in_i:
                arr_copy[i], arr_copy[i + 1] = arr_copy[i + 1], arr_copy[i]
                swapped = True
        
        # Si no hubo intercambios, el arreglo está ordenado
        if not swapped:
            break
        
        # Decrementar el límite superior
        end -= 1
        
        # Resetear la bandera de intercambio para el recorrido de derecha a izquierda
        swapped = False
        
        # Recorrido de derecha a izquierda
        for i in range(end - 1, start - 1, -1):
            # Evaluamos si el término está presente en los abstracts
            term_in_i = key.lower() in arr_copy[i].get("abstract", "").lower()
            term_in_i1 = key.lower() in arr_copy[i + 1].get("abstract", "").lower()
            
            # Si el término está en i pero no en i+1, intercambiamos
            if term_in_i and not term_in_i1:
                arr_copy[i], arr_copy[i + 1] = arr_copy[i + 1], arr_copy[i]
                swapped = True
        
        # Incrementar el límite inferior
        start += 1

    return arr_copy

#----------------------------------------------------------------------
def shell_sort(arr, key):
    n = len(arr)
    # Comenzamos con un gap grande y lo vamos reduciendo
    gap = n // 2
    # Mientras el gap sea mayor que 0
    while gap > 0:
        # Hacemos una inserción con gap para cada elemento desde gap hasta n
        for i in range(gap, n):
            # Guardamos el valor actual para comparaciones
            temp = arr[i]
            j = i
            
            # Mientras j sea mayor o igual que gap y el elemento en j-gap sea mayor que temp
            while j >= gap and arr[j - gap][key] > temp[key]:
                # Movemos el elemento j-gap a la posición j
                arr[j] = arr[j - gap]
                j -= gap
                
            # Colocamos temp en su posición correcta
            arr[j] = temp
            
        # Reducimos el gap
        gap //= 2
        
    return arr

def merge_sort(arr, key):

    # Caso base: una lista con 0 o 1 elemento ya está ordenada
    if len(arr) <= 1:
        return arr
    
    # Dividir la lista en dos mitades
    medio = len(arr) // 2
    izquierda = arr[:medio]
    derecha = arr[medio:]
    
    # Llamada recursiva para ordenar ambas mitades
    izquierda = merge_sort(izquierda, key)
    derecha = merge_sort(derecha, key)
    
    # Combinar las mitades ordenadas (implementación interna de merge)
    resultado = []
    i = j = 0
    
    # Mientras haya elementos en ambas listas
    while i < len(izquierda) and j < len(derecha):
        # Comparar elementos usando la key proporcionada
        if izquierda[i][key] <= derecha[j][key]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    
    # Agregar los elementos restantes
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    
    return resultado

class NodoEntero:
    """
    Clase para representar un nodo en una lista enlazada.
    Contiene un valor y un puntero al siguiente nodo.
    """
    def __init__(self, valor=0):
        self.valor = valor
        self.siguiente = None

class ColaEnlazada:

    def __init__(self):
        self.inicio = None
        self.fin = None
        self.tamano = 0
    
    def encolar(self, num):
        self.tamano += 1
        temp = NodoEntero(num)
        if self.inicio is None:
            self.inicio = temp
            self.fin = self.inicio
        else:
            self.fin.siguiente = temp
            self.fin = temp
    
    def decolar(self):
        if self.inicio is None:
            return None
        
        self.tamano -= 1
        temp = self.inicio.valor
        nodo_temp = self.inicio
        self.inicio = self.inicio.siguiente
        nodo_temp = None  # Ayuda al recolector de basura
        return temp
    
    def esta_vacia(self):
        """Verifica si la cola está vacía."""
        return self.tamano == 0

class RadixSort:

    def __init__(self):
        # Crear un arreglo de 10 colas (una para cada dígito 0-9)
        self.Q = [ColaEnlazada() for _ in range(10)]
    
    def obtener_radical(self, numero, radical):
        """Obtiene el dígito en la posición especificada."""
        return (numero // (10 ** (radical - 1))) % 10
    
    def sort(self, arr, key=None):
        # Si la lista está vacía, retornarla directamente
        if not arr:
            return arr
        
        # Función para obtener el valor numérico a ordenar
        def get_value(item):
            if key is not None:
                if callable(key):
                    return key(item)
                else:
                    return item[key]
            return item
        
        # Crear una copia de trabajo del arreglo
        a = arr.copy()
        
        # Encontrar el valor máximo y determinar el número de dígitos
        max_val = float('-inf')
        for item in a:
            val = get_value(item)
            if val > max_val:
                max_val = val
        
        numero_digitos = len(str(max_val))
        
        # Ordenar para cada posición de dígito
        for i in range(1, numero_digitos + 1):
            # Distribuir los elementos en las colas según el dígito actual
            for item in a:
                val = get_value(item)
                indice = self.obtener_radical(val, i)
                self.Q[indice].encolar(item)
            
            # Reconstruir el arreglo extrayendo elementos de las colas
            pos_arreglo = 0
            for j in range(10):
                while not self.Q[j].esta_vacia():
                    a[pos_arreglo] = self.Q[j].decolar()
                    pos_arreglo += 1
        
        return a

def medir_tiempos_ordenamiento_abstract(data, terminos):
    # Verificar si hay abstracts para analizar
    articulos_con_abstract = [a for a in data if a.get("abstract")]
    if not articulos_con_abstract:
        print("No hay abstracts disponibles para analizar.")
        return
    
    print("\n===== ANÁLISIS DE ORDENAMIENTO POR TÉRMINOS EN ABSTRACTS =====")
    
    # Definir los algoritmos a utilizar
    algoritmos = {
        "Bubble Sort": bubble_sort,
        "Shaker_Sort": burbuja_doble_keywords,
        "Shell_Sort": shell_sort,
        "Seleccion_Sort" :selection_sort,
        "Merge_sort": merge_sort,
        "Radix_Sort_Node": RadixSort().sort
    }
    
    resultados = {termino: {} for termino in terminos}
    frecuencias = {termino: {} for termino in terminos}
    
    for termino in terminos:
        print(f"\nOrdenando artículos por frecuencia del término: {termino}")
        
        for nombre, algoritmo in algoritmos.items():
            
            def count_term_occurrences(article):
                abstract = article.get("abstract", "").lower()
                return abstract.count(termino.lower())
            
            data_copy = deepcopy(data)
            
            inicio = time.time()
            
            try:
                if nombre in ["Tim Sort", "Comb Sort", "Selection Sort", "Bitonic Sort", "Gnome Sort"]:
                    for article in data_copy:
                        # Guardamos el número de ocurrencias como clave temporal
                        article["_temp_key"] = count_term_occurrences(article)
                    
                    algoritmo(data_copy, "_temp_key")
                    
                    for article in data_copy:
                        if "_temp_key" in article:
                            del article["_temp_key"]
                    
                    ordenados = data_copy
                    
                elif nombre == "Tree Sort":
                    for article in data_copy:
                        article["_temp_key"] = count_term_occurrences(article)
                    
                    temp = data_copy.copy()
                    data_copy.clear()
                    tree_sort(temp, "_temp_key")
                    data_copy = temp
                    
                    for article in data_copy:
                        if "_temp_key" in article:
                            del article["_temp_key"]
                    
                    ordenados = data_copy
                    
                else:
                    for article in data_copy:
                        article["_temp_key"] = count_term_occurrences(article)
                    
                    ordenados = algoritmo(data_copy, "_temp_key")
                    
                    for article in ordenados:
                        if "_temp_key" in article:
                            del article["_temp_key"]
                
                fin = time.time()
                tiempo = fin - inicio
                resultados[termino][nombre] = tiempo
                
                # Calcular el número total de ocurrencias del término en todos los abstracts
                total_occurrences = sum(count_term_occurrences(a) for a in ordenados)
                frecuencias[termino][nombre] = total_occurrences
                print(f"  • {nombre}: {tiempo:.4f} segundos - {total_occurrences} ocurrencias totales del término")
                
            except Exception as e:
                print(f"Error en {nombre} para el término '{termino}': {e}")
                resultados[termino][nombre] = None
                frecuencias[termino][nombre] = None
    
    # Generar tabla resumen de frecuencias
    print("\n===== RESUMEN DE FRECUENCIAS TOTALES DE TÉRMINOS =====")
    resumen_data = []
    for termino in terminos:
        resumen_data.append([termino] + [frecuencias[termino].get(nombre, "N/A") for nombre in algoritmos.keys()])
    
    resumen_tabla = tabulate.tabulate(
        resumen_data,
        headers=["Termino"," "," "," ", " ", "Algoritmos De Ordenmiento","Frecuencia Total"],
        tablefmt="grid"
    )
    print(resumen_tabla)
    
    # Generar gráfica de tiempo por algoritmo para cada término
    for termino in terminos:
        nombres = []
        tiempos = []
        
        for nombre in algoritmos.keys():
            if resultados[termino][nombre] is not None:
                nombres.append(nombre)
                tiempos.append(resultados[termino][nombre])
        
        if nombres:  # Solo generar la gráfica si hay resultados
            plt.figure(figsize=(10, 6))
            bars = plt.bar(nombres, tiempos, color='skyblue')
            
            # Añadir valor sobre cada barra
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.0005,
                        f'{height:.4f}s', ha='center', va='bottom')
            
            plt.title(f'Tiempos de ordenamiento para término "{termino}"')
            plt.xlabel('Algoritmo')
            plt.ylabel('Tiempo (segundos)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.close()
    
    # Generar gráfica comparativa para todos los términos
    plt.figure(figsize=(12, 8))
    
    valid_algoritmos = set()
    for termino in terminos:
        for nombre in algoritmos.keys():
            if resultados[termino].get(nombre) is not None:
                valid_algoritmos.add(nombre)
    
    valid_nombres = sorted(list(valid_algoritmos))
    
    if valid_nombres: 
        bar_width = 0.15
        index = np.arange(len(valid_nombres))
        
        for i, termino in enumerate(terminos):
            tiempos = [resultados[termino].get(nombre, "N/A") for nombre in valid_nombres]
            offset = i * bar_width
            print(f'index: {index}, offset: {offset}, tiempos: {tiempos}')
            # Verifica si alguno de estos es None
            if any(v is None for v in tiempos):
                print("Hay valores None en los datos.")
            else:
                plt.bar(index + offset, tiempos, bar_width, label=termino)
            
        
        plt.xlabel('Algoritmo de ordenamiento')
        plt.ylabel('Tiempo (segundos)')
        plt.title('Comparativa de algoritmos por término')
        plt.xticks(index + bar_width * (len(terminos) - 1) / 2, valid_nombres, rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig('comparativa_algoritmos_terminos.png')
        plt.close()
    
    return resultados, frecuencias