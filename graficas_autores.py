import time
import matplotlib.pyplot as plt
import heapq

def medir_tiempos_ordenamiento_autores(data, key):
    
   
    #------------------------------------------------- METODOS ------------------------------------------------------------
    # Función de ordenamiento (Insertion Sort)
    def insertion_sort(arr, left, right, key):
        for i in range(left + 1, right + 1):
            temp = arr[i]
            j = i - 1

            # Obtener el primer autor para comparación (o una cadena vacía si no hay autores)
            temp_author = temp[key][0] if temp[key] else ""

            while j >= left:
                current_author = arr[j][key][0] if arr[j][key] else ""

                if current_author > temp_author:  # Comparar nombres de autores
                    arr[j + 1] = arr[j]
                    j -= 1
                else:
                    break

            arr[j + 1] = temp  # Insertar en la posición correcta

    #-------------------------------------------------------------------------------------
    # Gnome Sort
    def gnome_sort(arr, key):
        i = 1
        while i < len(arr):
            # Obtener el primer autor o una cadena vacía si la lista está vacía
            prev_author = arr[i - 1][key][0] if arr[i - 1][key] else ""
            curr_author = arr[i][key][0] if arr[i][key] else ""

            if prev_author <= curr_author:
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
        # Copiamos las mitades del array
        L = arr[left:mid + 1]
        R = arr[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(L) and j < len(R):
            # Obtener el primer autor o cadena vacía si la lista está vacía
            left_author = L[i][key][0] if L[i][key] else ""
            right_author = R[j][key][0] if R[j][key] else ""

            if left_author <= right_author:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Agregar elementos restantes
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

        # Aplicar Insertion Sort en fragmentos pequeños
        for i in range(0, n, min_run):
            insertion_sort(arr, i, min((i + min_run - 1), n - 1), key)

        size = min_run
        while size < n:
            for start in range(0, n, size * 2):
                mid = min(n - 1, start + size - 1)
                end = min((start + size * 2 - 1), (n - 1))
                if mid < end:
                    merge(arr, start, mid, end, key)
            size *= 2

    #-----------------------------------------------------------------------------
    # CombSort
    def comb_sort(arr, key):
        gap = len(arr)
        swapped = True

        while gap > 1 or swapped:
            gap = max(1, int(gap / 1.3))  # Reducir el gap usando el factor 1.3
            swapped = False

            for i in range(len(arr) - gap):
                # Obtener el primer autor o una cadena vacía si la lista está vacía
                author_i = arr[i][key][0] if arr[i][key] else ""
                author_j = arr[i + gap][key][0] if arr[i + gap][key] else ""

                if author_i > author_j:  # Comparar los primeros autores
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    swapped = True


    #----------------------------------------------------------------------------------------------
    # Selection Sort
    def selection_sort(arr, key):
        n = len(arr)

        for i in range(n):
            min_idx = i

            for j in range(i + 1, n):
                # Obtener el primer autor o una cadena vacía si no hay autores
                author_j = arr[j][key][0] if arr[j][key] else ""
                author_min = arr[min_idx][key][0] if arr[min_idx][key] else ""

                if author_j < author_min:
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

            # Obtener el primer autor o una cadena vacía si no hay autores
            author_data = data[key][0] if data[key] else ""
            author_root = root.data[key][0] if root.data[key] else ""

            if author_data < author_root:
                root.left = insert(root.left, data)
            else:
                root.right = insert(root.right, data)
            return root

        def inorder(root, result):
            if root is not None:
                inorder(root.left, result)
                result.append(root.data)  # Agregar elemento ordenado
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
    def bucket_sort_strings(arr, key):
        # Crear diccionario de buckets para cada carácter imprimible (A-Z, a-z, 0-9, etc.)
        import string
        valid_chars = string.ascii_letters + string.digits  # Letras y números
        buckets = {ch: [] for ch in valid_chars}
        buckets["others"] = []  # Para caracteres no alfanuméricos

        # Distribuir elementos en buckets según la primera letra
        for item in arr:
            first_char = str(item.get(key, "")).strip().lower()[:1]  # Tomar el primer carácter
            if first_char in buckets:
                buckets[first_char].append(item)
            else:
                buckets["others"].append(item)  # Para caracteres como #, @, etc.

        # Ordenar cada bucket y reconstruir la lista
        sorted_data = []
        for bucket in sorted(buckets.keys()):  # Asegurar orden lexicográfico
            sorted_data.extend(sorted(buckets[bucket], key=lambda x: x.get(key, "")))

        return sorted_data


    #--------------------------------------------------------------------------------------
    #QuickSort
    def quicksort_authors(arr, key):
        if len(arr) <= 1:
            return arr

        # Verificamos que cada elemento sea un diccionario con la clave proporcionada
        if not all(isinstance(x, dict) and key in x for x in arr):
            raise ValueError("Todos los elementos deben ser diccionarios con la clave proporcionada")

        def get_first_author(item):
            """ Devuelve el primer autor en minúsculas, o una cadena vacía si no hay autores """
            return str(item[key][0]).strip().lower() if item[key] else ""

        pivot = arr[len(arr) // 2]  # Elegimos el pivote
        pivot_value = get_first_author(pivot)

        left = [x for x in arr if get_first_author(x) < pivot_value]
        middle = [x for x in arr if get_first_author(x) == pivot_value]
        right = [x for x in arr if get_first_author(x) > pivot_value]

        return quicksort_authors(left, key) + middle + quicksort_authors(right, key)

    #----------------------------------------------------------------------------------------

    def heap_sort(arr, key):
        # Función para extraer la clave de ordenamiento
        def key_func(x):
            return str(x.get(key, "")).lower()  # Convertir a string para comparación segura

        # Crear una lista de tuplas con (clave de orden, índice original, diccionario completo)
        heap = [(key_func(x), i, x) for i, x in enumerate(arr)]

        # Convertir en heap
        heapq.heapify(heap)

        # Extraer los elementos ordenados
        sorted_arr = [heapq.heappop(heap)[2] for _ in range(len(heap))]

        return sorted_arr

    #----------------------------------------------------------------------------------------
    #bitonic
    def bitonic_sort(arr, key):
        def key_func(x):
            return str(x.get(key, "")).lower()  # Convertir a string para comparación segura

        def compare_and_swap(arr, i, j, direction):
            if (key_func(arr[i]) > key_func(arr[j]) and direction == 1) or \
            (key_func(arr[i]) < key_func(arr[j]) and direction == 0):
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
        def key_func(x):
            return str(x.get(key, "")).lower()  # Asegurar que el valor es string y evitar errores

        def binary_search(arr, val, low, high):
            while low <= high:
                mid = (low + high) // 2
                if key_func(val) < key_func(arr[mid]):  # Uso correcto de key_func
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
        def key_func(x):
            return str(x.get(key, "")).lower()  # Asegura que el valor sea un string

        if not arr:
            return arr

        max_length = max(len(key_func(item)) for item in arr)  # Evitar TypeError

        for pos in range(max_length - 1, -1, -1):  # Recorrer de derecha a izquierda
            buckets = {}  # Diccionario para manejar cualquier carácter Unicode

            for item in arr:
                char = key_func(item)[pos] if pos < len(key_func(item)) else ""  # Evita errores de índice
                if char not in buckets:
                    buckets[char] = []
                buckets[char].append(item)

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
    sorted_data=tree_sort(data_copy4, key)
    #for item in sorted_data:
    #    print(item[key])
    tiempos["TreeSort"] =tiempo_tree = time.time() - start_time

        # Medir tiempo de BucketSort
    data_copy11 = data.copy()
    start_time = time.time()
        # Extraer títulos
    # Ordenar usando Bucket Sort
    sorted_titles = bucket_sort_strings(data_copy11, key)
        #Mostrar los títulos ordenados
    #for title in sorted_titles:
    #    print(title[key])
    tiempos["BucketSort"] = tiempo_bucket = time.time() - start_time

        # Medir tiempo de QuickSort
    data_copy5 = data.copy()
    start_time = time.time()
        # Aplicar Insertion Sort
    sorted_data = quicksort_authors(data_copy5, key)
    #for item in sorted_data:
    #    print(item[key])
    tiempos["QuickSort"] = tiempo_quickSort = time.time() - start_time

        # Medir tiempo de heap_sort
    data_copy6 = data.copy()
    start_time = time.time()
    sorted_data = heap_sort(data_copy6, key)
    #for item in sorted_data:
    #    print(item[key])
    tiempos["heap_sort"] = tiempo_heapsort = time.time() - start_time

        # Medir tiempo de Bitonic
    data_copy7 = data.copy()
    start_time = time.time()
    bitonic_sort(data_copy7, key)
    #for item in data_copy7:
    #    print(item[key])
    tiempos["Bitonic"] = tiempo_bitonic = time.time() - start_time

        # Medir tiempo de Gnome Sort
    data_copy8 = data.copy()
    start_time = time.time()
    gnome_sort(data_copy8, key)
    #for item in data_copy8:
    #    print(item[key])
    tiempos["Gnome_Sort"] = tiempo_gnome = time.time() - start_time

        # Medir tiempo de Binaryinsertion
    data_copy9 = data.copy()
    start_time = time.time()
    sorted_data=binary_insertion_sort(data_copy9, key)
    #for item in sorted_data:
    #    print(item[key])
    tiempos["Binaryinsertion"] = tiempo_binary = time.time() - start_time

        # Medir tiempo de Radix
    data_copy10 = data.copy()
    start_time = time.time()
    sorted_data=radix_sort(data_copy10, key)
    #for item in sorted_data:
    #    print(item[key])
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
    plt.title("Tiempo de Ordenamiento por autor")
    plt.xticks(metodos,  rotation=45, ha="right")
    plt.gcf().subplots_adjust(bottom=0.2) 
    plt.show()
    return tiempos
