import time
import matplotlib.pyplot as plt
import heapq

def medir_tiempos_ordenamiento(data, key):
    
   
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
        i = 1
        while i < len(arr):
            if arr[i - 1][key] <= arr[i][key]:
                i += 1
            else:
                arr[i - 1], arr[i] = arr[i], arr[i - 1] 
                if i > 1:
                    i -= 1
                else:
                    i += 1
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
                arr.append(root.data)
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

    def pigeonhole_sort(arr, key):
        min_val = int(min(arr, key =lambda x: x[key])[key])
        max_val = int(max(arr, key =lambda x: x[key])[key])
    
        size = max_val - min_val + 1
        holes = [[] for _ in range(size)]

        # Distribuir los elementos en los agujeros correspondientes
        for item in arr:
            index = item[key] - min_val  # Calcular la posición en los agujeros
            holes[index].append(item) # inserta el elemento
        # Extraer los elementos ordenados desde los agujeros
        result = []
        for bucket in holes:
            result.extend(bucket)
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

    #-------------------------------- MIDIENDO TIEMPOS -----------------------------------------------------------------------

    tiempos = {}
        # Medir tiempo de Timsort
    data_copy1 = data.copy()
    start_time = time.time()
    timsort(data_copy1, key)
    #for item in data_copy1:
    #    print(item[key])
    tiempos["TimSort"] = tiempo_timsort = time.time() - start_time

        # Medir tiempo de CombSort
    data_copy2 = data.copy()
    start_time = time.time()
    comb_sort(data_copy2, key)
    #for item in data_copy2:
    #    print(item[key])
    tiempos["CombSort"] = tiempo_combsort = time.time() - start_time

        # Medir tiempo de SelectionSort
    data_copy3 = data.copy()
    start_time = time.time()
    selection_sort(data_copy3, key)
    #for item in data_copy3:
    #    print(item[key])
    tiempos["SelectionSort"] =tiempo_selection = time.time() - start_time

        # Medir tiempo de TreeSort
    data_copy4 = data.copy()
    start_time = time.time()
    tree_sort(data_copy4, key)
    #for item in data_copy4:
    #    print(item[key])
    tiempos["TreeSort"] =tiempo_tree = time.time() - start_time

        # Medir tiempo de BucketSort
    start_time = time.time()
        # Extraer títulos
    titles = [item[key] for item in data if key in item]
    # Ordenar usando Bucket Sort
    sorted_titles = bucket_sort_strings(titles)
        #Mostrar los títulos ordenados
        #for title in sorted_titles:
        #    print(title)
    tiempos["BucketSort"] = tiempo_bucket = time.time() - start_time

        # Medir tiempo de QuickSort
    data_copy5 = data.copy()
    start_time = time.time()
        # Aplicar Insertion Sort
    sorted_data = quicksort(data_copy5, key)
        #for item in sorted_data:
        #    print(item["primary_title"])
    tiempos["QuickSort"] = tiempo_quickSort = time.time() - start_time

        # Medir tiempo de heap_sort
    data_copy6 = data.copy()
    start_time = time.time()
    sorted_data = heap_sort(data_copy6, key)
    #for item in sorted_data:
    #    print(item["primary_title"])
    tiempos["heap_sort"] = tiempo_heapsort = time.time() - start_time

        # Medir tiempo de Bitonic
    data_copy7 = data.copy()
    start_time = time.time()
    bitonic_sort(data_copy7, key)
    #for title in sorted_titles:
    #    print(title)
    tiempos["Bitonic"] = tiempo_bitonic = time.time() - start_time

        # Medir tiempo de Gnome Sort
    data_copy8 = data.copy()
    start_time = time.time()
    gnome_sort(data_copy8, key)
    #for title in sorted_titles:
    #    print(title)
    tiempos["Gnome_Sort"] = tiempo_gnome = time.time() - start_time

        # Medir tiempo de Binaryinsertion
    data_copy9 = data.copy()
    start_time = time.time()
    binary_insertion_sort(data_copy9, key)
    #for title in sorted_titles:
    #    print(title)
    tiempos["Binaryinsertion"] = tiempo_binary = time.time() - start_time

        # Medir tiempo de Radix
    data_copy10 = data.copy()
    start_time = time.time()
    radix_sort(data_copy10, key)
    #for title in sorted_titles:
    #    print(title)
    tiempos["Radix"] = tiempo_radix = time.time() - start_time


        # resultados
    print(f"Timsort: {tiempo_timsort:.5f} segundos")
    print(f"CombSort: {tiempo_combsort:.5f} segundos")
    print(f"Selection: {tiempo_selection:.5f} segundos")
    print(f"TreeSort: {tiempo_tree:.5f} segundos")
    print(f"BucketSort: {tiempo_bucket:.5f} segundos")
    print(f"QuickSort: {tiempo_quickSort:.5f} segundos")
    print(f"heapsort: {tiempo_heapsort:.5f} segundos")
    print(f"bitonic: {tiempo_bitonic:.5f} segundos")
    print(f"Gnome Sort: {tiempo_gnome:.5f} segundos")
    print(f"binary: {tiempo_binary:.5f} segundos")
    print(f"radix: {tiempo_radix:.5f} segundos")

        # Graficar
    metodos = ["Timsort  ", "CombSort  ", "SelectionSort  ", "TreeSort  ", "BucketSort", "QuickSort  ", "heapsort  ", "Bitonic  ", "Gnome Sort  ", "BinaryInsertion  ", "Radix  "]
    tiempos = [tiempo_timsort, tiempo_combsort, tiempo_selection, tiempo_tree, tiempo_bucket, tiempo_quickSort, tiempo_heapsort, tiempo_bitonic, tiempo_gnome, tiempo_binary, tiempo_radix]

    plt.bar(metodos, tiempos, color=["#e85069", "#79e850", "#9a50e8", "#e850c1", "#e6e850", "#e8a850", "#50e8c3", "#5087e8", "#50d8e8", "#e85050", "#e8a850"])
    plt.ylabel("Tiempo (segundos)")
    plt.title("Tiempo de Ordenamiento por titulo")
    plt.xticks(metodos,  rotation=45, ha="right")
    plt.gcf().subplots_adjust(bottom=0.2) 
    plt.show()
    return tiempos
