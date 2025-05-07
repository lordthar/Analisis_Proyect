import csv
import rispy
import os

def risACsv(nombrecsv, *ris_files):
    all_entries = [] 

    for file_name in ris_files:
        if not os.path.exists(file_name):
            print(f" Error: El archivo '{file_name}' no existe.")
            continue 

        try:
            
            with open(file_name, "r", encoding="utf-8") as file:
                content = file.read()

            if not content.strip():
                print(f" El archivo '{file_name}' está vacío.")
                continue  
            
            
            with open(file_name, "r", encoding="utf-8") as file:
                entries = rispy.load(file) 
                
                if not entries:
                    print(f" No se encontraron referencias válidas en '{file_name}'.")
                else:
                    all_entries.extend(entries)  
                    print(f" Archivo procesado: {file_name}")

        except Exception as e:
            print(f" No se pudo procesar '{file_name}': {e}")

    
    if all_entries:
        with open(nombrecsv, "w", encoding="utf-8", newline="") as file:
            fieldnames = ["type_of_reference", "primary_title", "authors", "year", "doi", "journal", "urls", "abstract", "publisher", "keywords"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for ref in all_entries:
                writer.writerow({
                    "type_of_reference": ref.get("type_of_reference", ""),
                    "primary_title": ref.get("primary_title", ""),
                    "authors": ", ".join(ref.get("authors", [])),
                    "year": ref.get("year", ""),
                    "doi": ref.get("doi", ""),
                    "journal": ref.get("secondary_title", ""),
                    "urls": ", ".join(ref.get("urls", [])),
                    "abstract": ref.get("abstract", ""),
                    "publisher": ref.get("publisher", ""),
                     "keywords": ", ".join(ref.get("keywords", [])) 
                })

        print(f" Archivo CSV guardado como '{nombrecsv}'")
    else:
        print(" No se encontraron referencias válidas en los archivos.")
