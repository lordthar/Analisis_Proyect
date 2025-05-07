import time
import matplotlib.pyplot as plt
import heapq

def medir_tiempos_ordenamiento_year(data, key):
    
    #------------------------------------------------- METODOS ------------------------------------------------------------
    # Función de ordenamiento (Insertion Sort)
    def insertion_sort(arr, left, right, key):
        for i in range(left + 1, right + 1):
            temp = arr[i]
            j = i - 1
            while j >= left and int(arr[j][key]) > int(temp[key]):  # Convertir a entero antes de comparar
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
            if int(L[i][key]) <= int(R[j][key]):  # Convertir a int para comparación correcta
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

        # Aplicar Insertion Sort en sublistas pequeñas
        for i in range(0, n, min_run):
            insertion_sort(arr, i, min((i + min_run - 1), n - 1), key)

        # Fusionar las sublistas ordenadas
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
                if int(arr[i][key]) > int(arr[i + gap][key]):  # Conversión a int
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]  # Intercambio
                    swapped = True


    #----------------------------------------------------------------------------------------------
    # Selection Sort
    def selection_sort(arr, key):
        gap = len(arr)
        swapped = True
        while gap > 1 or swapped:
            gap = max(1, int(gap / 1.3))  # Reduce el gap usando el factor 1.3
            swapped = False
            for i in range(len(arr) - gap):
                try:
                    a = int(arr[i][key])  
                    b = int(arr[i + gap][key])  
                except ValueError:
                    a, b = arr[i][key], arr[i + gap][key]  # En caso de error, comparar como strings
                    
                if a > b:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]  # Intercambio
                    swapped = True

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

            # Convertimos el valor de la clave a entero para comparación
            if int(data[key]) < int(root.data[key]):
                root.left = insert(root.left, data)
            else:
                root.right = insert(root.right, data)

            return root

        def inorder(root, result):
            if root is not None:
                inorder(root.left, result)
                result.append(root.data)  # Agregar nodo ordenado a la lista
                inorder(root.right, result)

        if not arr:
            return []  # Retornar lista vacía si la entrada está vacía
        
          # Convertir explícitamente el valor de 'key' a entero en cada diccionario
        for item in arr:
            item[key] = int(item[key])

        root = TreeNode(arr[0])  # Raíz con el primer elemento
        for i in range(1, len(arr)):
            insert(root, arr[i])  # Insertar cada elemento en el árbol

        result = []
        inorder(root, result)  # Obtener elementos ordenados en `result`
        return result 

    #-------------------------------------------------------------------------------------------
    #Pigeonhole NO SIRVE PARA CADENAS

    def pigeonhole_sort(arr, key):
        if not arr:
            return arr  # Retorna vacío si la lista está vacía
        
        min_val = min(arr, key=lambda x: int(x[key]))[key]
        max_val = max(arr, key=lambda x: int(x[key]))[key]
        
        min_val, max_val = int(min_val), int(max_val)  # Asegurar conversión a enteros
        size = max_val - min_val + 1
        
        holes = [[] for _ in range(size)]  # Crear "agujeros" vacíos

        # Distribuir los elementos en los agujeros correspondientes
        for item in arr:
            index = int(item[key]) - min_val  # Calcular la posición en los agujeros
            holes[index].append(item)  # Insertar el elemento en su agujero

        # Extraer los elementos ordenados desde los agujeros
        result = []
        for bucket in holes:
            result.extend(bucket)  # Agregar elementos ordenados

        return result

    #--------------------------------------------------------------------
    #bucket_sort
    def bucket_sort(arr, key):
        if not arr:
            return arr

        # Convertir los valores de la clave a enteros
        min_val = min(arr, key=lambda x: int(x[key]))[key]
        max_val = max(arr, key=lambda x: int(x[key]))[key]

        min_val, max_val = int(min_val), int(max_val)

        bucket_count = 10
        bucket_size = (max_val - min_val) / bucket_count if (max_val - min_val) >= bucket_count else 1
        buckets = [[] for _ in range(bucket_count)]

        # Distribuir los elementos en los buckets
        for item in arr:
            index = int((int(item[key]) - min_val) / bucket_size)
            index = min(index, bucket_count - 1)  # Asegurar que no se pase del rango
            buckets[index].append(item)

        # Ordenar cada bucket y combinarlos
        result = []
        for bucket in buckets:
            result.extend(sorted(bucket, key=lambda x: int(x[key])))

        return result


    #--------------------------------------------------------------------------------------
    #QuickSort
    def quicksort(arr, key):
        if len(arr) <= 1:
            return arr

        # Verificamos que cada elemento sea un diccionario con la clave proporcionada
        if not all(isinstance(x, dict) and key in x for x in arr):
            raise ValueError("Todos los elementos deben ser diccionarios con la clave proporcionada")

        # Convertir los valores de la clave a enteros si es necesario
        try:
            pivot = arr[len(arr) // 2]
            pivot_value = int(pivot[key])  # Convertir a int
            left = [x for x in arr if int(x[key]) < pivot_value]
            middle = [x for x in arr if int(x[key]) == pivot_value]
            right = [x for x in arr if int(x[key]) > pivot_value]
        except ValueError:
            raise ValueError("Los valores de la clave deben ser convertibles a enteros para ordenarse correctamente")

        return quicksort(left, key) + middle + quicksort(right, key)

    #----------------------------------------------------------------------------------------
    #heap_sort
    def heap_sort_dicts(data, key="year"):
        """ Ordena una lista de diccionarios por el valor de 'key' usando heapq """
        try:
            # Filtrar y convertir valores de 'key' a enteros
            valid_data = [item for item in data if key in item and str(item[key]).isdigit()]
            
            # Ordenar usando heapq.nsmallest (evita el error de TypeError)
            sorted_data = heapq.nsmallest(len(valid_data), valid_data, key=lambda x: int(x[key]))

            return sorted_data
        except Exception as e:
            print(f"Error en heap_sort_dicts: {e}")
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
                bitonic_sort_recursive(arr, low, k, 1)  # Ascendente
                bitonic_sort_recursive(arr, low + k, k, 0)  # Descendente
                bitonic_merge(arr, low, length, direction)

        # Verificar si `arr` está vacío
        if not arr:
            return arr

        # Convertir los valores de la clave a enteros sin modificar el original
        arr = [{**item, key: int(item[key])} for item in arr]

        # Ajustar el tamaño de la lista a la potencia de 2 más cercana
        import math
        n = len(arr)
        next_power_of_2 = 2 ** math.ceil(math.log2(n))
        extra_items = [{"dummy": True, key: float('inf')}] * (next_power_of_2 - n)
        arr.extend(extra_items)  # Rellenar con valores grandes

        # Ordenar con Bitonic Sort
        bitonic_sort_recursive(arr, 0, len(arr), 1)

        # Remover los elementos ficticios antes de retornar
        return [item for item in arr if "dummy" not in item]


    #------------------------------------------------------------------------------------------
    # Binaryinsertion
    def binary_insertion_sort(arr, key):
        def binary_search(arr, val, low, high):
            while low <= high:
                mid = (low + high) // 2
                if int(val[key]) < int(arr[mid][key]):  # Convertir a int antes de comparar
                    high = mid - 1
                else:
                    low = mid + 1
            return low

        for i in range(1, len(arr)):
            val = arr[i]
            j = binary_search(arr, val, 0, i - 1)

            # Desplazar elementos manualmente en lugar de usar slicing
            for k in range(i, j, -1):
                arr[k] = arr[k - 1]
            arr[j] = val  # Insertar en la posición correcta

        return arr  

    #-----------------------------------------------------------------------------------------
    # Radix
    def radix_sort(arr, key):
        if not arr:
            return arr
        
        # Obtener el valor máximo como entero (para determinar el número de dígitos)
        max_value = max(int(item[key]) for item in arr)
        exp = 1  # Empezamos con la unidad

        while max_value // exp > 0:
            buckets = [[] for _ in range(10)]  # Dígitos 0-9

            # Distribuir elementos en los buckets según el dígito actual
            for item in arr:
                num = int(item[key])  # Convertir a entero
                digit = (num // exp) % 10  # Extraer el dígito en la posición actual
                buckets[digit].append(item)

            # Concatenar los elementos en el orden de los buckets
            arr.clear()  # Vaciar lista original
            for bucket in buckets:
                arr.extend(bucket)  # Agregar elementos ordenados

            exp *= 10  # Moverse al siguiente dígito

        return arr
    #-------------------------------- MIDIENDO TIEMPOS -----------------------------------------------------------------------

    tiempos = {}
        # Medir tiempo de Timsort
    data_copy1 = data.copy()
    start_time = time.time()
    timsort(data_copy1, key)
    tiempos["TimSort"] = tiempo_timsort = time.time() - start_time

        # Medir tiempo de CombSort
    data_copy2 = data.copy()
    start_time = time.time()
    comb_sort(data_copy2, key)
    for item in data_copy2:
        print(item[key])
    tiempos["CombSort"] = tiempo_combsort = time.time() - start_time

        # Medir tiempo de SelectionSort
    data_copy3 = data.copy()
    start_time = time.time()
    selection_sort(data_copy3, key)
    tiempos["SelectionSort"] =tiempo_selection = time.time() - start_time

        # Medir tiempo de TreeSort
    data_copy4 = data.copy()
    start_time = time.time()
    sorted_data=tree_sort(data_copy4, key)
    tiempos["TreeSort"] =tiempo_tree = time.time() - start_time

    data_copy12 = data.copy()
    start_time = time.time()
    sorted_data=pigeonhole_sort(data_copy12, key)
    tiempos["pigeonhole"] =tiempo_pigenonhole = time.time() - start_time

        # Medir tiempo de BucketSort
    data_copy11 = data.copy()
    start_time = time.time()
    # Ordenar usando Bucket Sort
    sorted_data = bucket_sort(data_copy11, key)
        #Mostrar los títulos ordenados
    tiempos["BucketSort"] = tiempo_bucket = time.time() - start_time

        # Medir tiempo de QuickSort
    data_copy5 = data.copy()
    start_time = time.time()
        # Aplicar Insertion Sort
    sorted_data = quicksort(data_copy5, key)
    tiempos["QuickSort"] = tiempo_quickSort = time.time() - start_time

        # Medir tiempo de heap_sort
    data_copy6 = data.copy()
    start_time = time.time()
    sorted_data = heap_sort_dicts(data_copy6, key)
        #Mostrar los títulos ordenados
    tiempos["heap_sort"] = tiempo_heapsort = time.time() - start_time

        # Medir tiempo de Bitonic
    data_copy7 = data.copy()
    start_time = time.time()
    sorted_data=bitonic_sort(data_copy7, key)
    tiempos["Bitonic"] = tiempo_bitonic = time.time() - start_time

        # Medir tiempo de Gnome Sort
    data_copy8 = data.copy()
    start_time = time.time()
    sorted_data=gnome_sort(data_copy8, key)
    tiempos["Gnome_Sort"] = tiempo_gnome = time.time() - start_time

        # Medir tiempo de Binaryinsertion
    data_copy9 = data.copy()
    start_time = time.time()
    binary_insertion_sort(data_copy9, key)
    tiempos["Binaryinsertion"] = tiempo_binary = time.time() - start_time

        # Medir tiempo de Radix
    data_copy10 = data.copy()
    start_time = time.time()
    sorted_data=radix_sort(data_copy10, key)
    tiempos["Radix"] = tiempo_radix = time.time() - start_time


        # resultados
    print(f"Timsort: {tiempo_timsort:.5f} segundos")
    print(f"CombSort: {tiempo_combsort:.5f} segundos")
    print(f"Selection: {tiempo_selection:.5f} segundos")
    print(f"TreeSort: {tiempo_tree:.5f} segundos")
    print(f"Pigenonhole: {tiempo_pigenonhole:.5f} segundos")
    print(f"BucketSort: {tiempo_bucket:.5f} segundos")
    print(f"QuickSort: {tiempo_quickSort:.5f} segundos")
    print(f"heapsort: {tiempo_heapsort:.5f} segundos")
    print(f"bitonic: {tiempo_bitonic:.5f} segundos")
    print(f"Gnome Sort: {tiempo_gnome:.5f} segundos")
    print(f"binary: {tiempo_binary:.5f} segundos")
    print(f"radix: {tiempo_radix:.5f} segundos")

        # Graficar
    metodos = ["Timsort  ", "CombSort  ", "SelectionSort  ", "TreeSort  ", "Pigeonhole  ", "BucketSort", "QuickSort  ", "heapsort  ", "Bitonic  ", "Gnome Sort  ", "BinaryInsertion  ", "Radix  "]
    tiempos = [tiempo_timsort, tiempo_combsort, tiempo_selection, tiempo_tree, tiempo_pigenonhole, tiempo_bucket, tiempo_quickSort, tiempo_heapsort, tiempo_bitonic, tiempo_gnome, tiempo_binary, tiempo_radix]

    plt.bar(metodos, tiempos, color=["#e85069", "#79e850", "#9a50e8", "#e850c1", "#5079e8", "#e6e850", "#e8a850", "#50e8c3", "#5087e8", "#50d8e8", "#e85050", "#e8a850"])
    plt.ylabel("Tiempo (segundos)")
    plt.title("Tiempo de Ordenamiento por años")
    plt.xticks(metodos,  rotation=45, ha="right")
    plt.gcf().subplots_adjust(bottom=0.2) 
    plt.show()
    return tiempos
