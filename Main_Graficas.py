#Graficas por variable
from Estadisticas.graficas_titulo import medir_tiempos_ordenamiento
from Estadisticas.graficas_year import medir_tiempos_ordenamiento_year
from  Estadisticas.graficas_autores import medir_tiempos_ordenamiento_autores
from  Estadisticas.graficas_abstract import medir_tiempos_ordenamiento_abstract
#Agrupador jerarquico
from  Estadisticas.agrupador_jerarquico import AgrupadorJerarquico
#Estadisticas con condiciones
from  Estadisticas.Estadisticas_Autores import estadisticas_autores
from  Estadisticas.Estadisticas_AnioTipo import estadisticas_aniotipo
from  Estadisticas.Estadisticas_Producto import estadisticas_producto
from  Estadisticas.Estadisticas_journals import estadisticas_journals
from  Estadisticas.Estadisticas_Publisher import estadisticas_publisher
from convertidor_ris_csv import risACsv
import time
import csv

#---------------------------- LEYENDO Y VERIFICANDO ---------------------------------------
computational_thinking_terms = [
    "Abstraction", "Motivation", "Algorithm", "Persistence", "Coding", "Block",
    "Creativity", "Mobile application", "Logic", "Programming", "Conditionals", 
    "Robotic", "Loops", "Scratch"
]

risACsv("referencias.csv", "Proyecto_Analisis\\Articulos\\articulos_unicos.ris")

time.sleep(10)

with open("referencias.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader) 

key = "abstract"  

if not data:
    print(" El archivo CSV está vacío o no tiene datos válidos.")
elif key not in data[0]:  
    print(f" No existe la llave '{key}' en el CSV.")
else:
    total = len(data)  
    print(f" Ordenando más de {total} registros por '{key}'...")
    

#--------------------------------LLAMANDO FUNCION ------------------------------------------
# medir_tiempos_ordenamiento(data, key)

#medir_tiempos_ordenamiento_year(data, key)

# medir_tiempos_ordenamiento_abstract(data, computational_thinking_terms)

# --------------------------------- AGRUPAMIENTO JERÁRQUICO ----------------------------------
print("\n[INFO] Iniciando Agrupamiento Jerárquico...")

agrupador = AgrupadorJerarquico('referencias.csv') 
agrupador.cargar_datos()
agrupador.vectorizar_textos()

# Usar método que ya compara y grafica
agrupador.comparar_metodos()

#-----------------------------------------------------------------------------------------------------------------
#estadisticas_autores(data, key)
#estadisticas_aniotipo(data, key)
#estadisticas_producto(data, key)
#estadisticas_journals(data, key)
#estadisticas_publisher(data, key)