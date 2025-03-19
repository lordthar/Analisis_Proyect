from graficas_titulo import medir_tiempos_ordenamiento
from graficas_year import medir_tiempos_ordenamiento_year
from graficas_autores import medir_tiempos_ordenamiento_autores
from convertidor_ris_csv import risACsv
import time
import csv

#---------------------------- LEYENDO Y VERIFICANDO ---------------------------------------
risACsv("referencias.csv", "articulos_unicos.ris")

time.sleep(10)

with open("referencias.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader) 

key = "authors"  

if not data:
    print(" El archivo CSV está vacío o no tiene datos válidos.")
elif key not in data[0]:  
    print(f" No existe la llave '{key}' en el CSV.")
else:
    total = len(data)  
    print(f" Ordenando más de {total} registros por '{key}'...")
#--------------------------------LLAMANDO FUNCION ------------------------------------------
# medir_tiempos_ordenamiento(data, key)

# medir_tiempos_ordenamiento_year(data, key)

medir_tiempos_ordenamiento_autores(data, key)