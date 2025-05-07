import time
import os
import rispy 
from selenium import webdriver
from decouple import config
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

class ScraperSD:
    def __init__(self, unique_file_path, duplicate_file_path):
        self.download_path = "C:\\Users\\lanth\\Desktop\\Proyecto_Analisis\\articulos_descargados"
        self.unique_file_path = unique_file_path  
        self.duplicate_file_path = duplicate_file_path 
        self.brave_path = "C:\Program Files\BraveSoftware\Brave-Browser\Application/brave.exe"
        
        chrome_options = Options()
        chrome_options.binary_location = self.brave_path
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disabled-gpu")
        chrome_options.add_argument(f'--download-default-directory={self.download_path}')
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        })
        
        self.driver = webdriver.Chrome(options=chrome_options)

    def is_download_complete(self, directory):
        files = os.listdir(directory)
        for f in files:
            if f.endswith('.crdownload'): 
                return False
        return True

    def process_ris_file(self):
        all_files = [f for f in os.listdir(self.download_path) if f.endswith(".ris")]

        if not all_files:
            print("No se encontraron archivos RIS para procesar.")
            return

        unique_articles = {}
        duplicate_articles = {}

        for file in all_files:
            file_path = os.path.join(self.download_path, file)

            if os.path.getsize(file_path) == 0:
                print(f"El archivo {file} está vacío.")
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                entries = rispy.load(f) 

                for entry in entries:
                    identifier = entry.get("doi", None)

                    if identifier:
                        if identifier in unique_articles:
                            duplicate_articles[identifier] = entry
                        else:
                            unique_articles[identifier] = entry
                    else:
                        unique_articles[f"no_identifier_{len(unique_articles)}"] = entry

        if unique_articles:
            with open(self.unique_file_path, 'w', encoding="utf-8") as unique_file:
                rispy.dump(list(unique_articles.values()), unique_file)
            print("Artículos únicos añadidos al archivo.")
        else:
            print("No se encontraron artículos únicos.")

        if duplicate_articles:
            with open(self.duplicate_file_path, 'w', encoding="utf-8") as duplicate_file:
                rispy.dump(list(duplicate_articles.values()), duplicate_file)
            print("Artículos repetidos añadidos al archivo.")
        else:
            print("No se encontraron artículos duplicados.")

    def run(self):
        self.driver.get("https://library.uniquindio.edu.co/databases")

        WebDriverWait(self.driver, 60).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.onload-background"))
        )

        fac_ingenieria_access = WebDriverWait(self.driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//summary[@role='button'][contains(., 'Fac. Ingeniería')]"))
        )
        fac_ingenieria_access.click()

        scienceD_link = WebDriverWait(self.driver, 70).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "SCIENCEDIRECT - Consorcio Colombia - (DESCUBRIDOR)"))
        )
        scienceD_link.click()

        google_button = WebDriverWait(self.driver, 40).until(
            EC.element_to_be_clickable((By.ID, "btn-google"))
        )
        google_button.click()

        email_field = WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_field.send_keys(config('CORREO_INSTITUCIONAL'))
        email_field.send_keys(Keys.ENTER)

        password_field = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        )
        password_field.send_keys(config('PASSWORD_INSTITUCIONAL'))
        password_field.send_keys(Keys.ENTER)

        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "qs"))
        )
        search_box = self.driver.find_element(By.ID, "qs")
        search_box.send_keys("computational thinking")
        search_box.send_keys(Keys.ENTER)

        onehundred_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[span[text()='100']]"))
        )
        onehundred_button.click()
        time.sleep(2)
        pagina_actual = 1
        numero_pagina = 25
        while pagina_actual <= numero_pagina:
            time.sleep(5)
            try:
                checkbox = WebDriverWait(self.driver, 500).until(
                    EC.presence_of_element_located((By.ID, "select-all-results"))
                )
                if checkbox.is_selected():
                    self.driver.execute_script("arguments[0].click();", checkbox)
                self.driver.execute_script("arguments[0].click();", checkbox)

                export_citations_button = WebDriverWait(self.driver, 100).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "export-all-link-text"))
                )
                export_citations_button.click()

                WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "ReactModal__Content"))
                )
                export_ris_button = WebDriverWait(self.driver, 40).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export citation to RIS')]"))
                )
                ActionChains(self.driver).move_to_element(export_ris_button).click().perform()

                while not self.is_download_complete(self.download_path):
                    print("Esperando a que la descarga termine...")

                time.sleep(4)

                self.driver.execute_script(""" 
                    var feedback_button = document.getElementById("_pendo-badge_9BcFvkCLLiElWp6hocDK3ZG6Z4E");
                    if (feedback_button) {
                        feedback_button.style.display = 'none';
                    }
                """)

                next_button = WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li.pagination-link.next-link a"))
                )

                if "disabled" not in next_button.get_attribute("class") and next_button.is_displayed():
                    ActionChains(self.driver).move_to_element(next_button).click().perform()
                    print("Cargando siguiente página...")

                    WebDriverWait(self.driver, 2000).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.result-item-content"))
                    )
                    print("Página siguiente cargada.")
                    time.sleep(5)
               
             
            except Exception as e:
                print("Error al cargar la siguiente página o no hay más páginas.")
                self.driver.quit()
                break
            pagina_actual +=1
        
        self.process_ris_file() 
