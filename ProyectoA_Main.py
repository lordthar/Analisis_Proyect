from WebScrapScienceD import ScraperSD
from WebScrapSAGE import ScraperSage
from WebScrapIEEE import ScraperIEEE
import os


def main():

    download_path = "C:\\Users\\lanth\\Desktop\\Analisis_De_Algortimos_Proyecto"

    unique_file_path = os.path.join(download_path, "articulos_unicos.ris")

    duplicate_file_path = os.path.join(download_path, "articulos_repetidos.ris")

    if not os.path.exists(unique_file_path):
        with open(unique_file_path, 'w', encoding='utf-8') as unique_file:
            unique_file.write('') 

    if not os.path.exists(duplicate_file_path):
        with open(duplicate_file_path, 'w', encoding='utf-8') as duplicate_file:
            duplicate_file.write('')

    scraper = ScraperIEEE(unique_file_path , duplicate_file_path)
    scraper.run()
if __name__ == "__main__":
    main()
