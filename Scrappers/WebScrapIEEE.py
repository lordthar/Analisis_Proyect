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


class ScraperIEEE:
    def __init__(self, unique_file_path, duplicate_file_path ):
        self.download_path = "C:\\Users\\lanth\\Desktop\\Proyecto_Analisis\\articulos_descargados"
        self.unique_file_path = unique_file_path  
        self.duplicate_file_path = duplicate_file_path 
        self.brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        
        chrome_options = Options()
        chrome_options.binary_location = self.brave_path
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
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
                    identifier = entry.get("doi", None) or entry.get("UR", None)

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

        ieee_link = WebDriverWait(self.driver, 70).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "IEEE (Institute of Electrical and Electronics Engineers) - (DESCUBRIDOR)"))
        )
        ieee_link.click()

        google_button = WebDriverWait(self.driver, 40).until(
            EC.element_to_be_clickable((By.ID, "btn-google"))
        )
        google_button.click()

        email_field = WebDriverWait(self.driver, 70).until(
            EC.element_to_be_clickable((By.ID, "identifierId"))
        )
        email_field.send_keys(config('CORREO_INSTITUCIONAL'))
        email_field.send_keys(Keys.ENTER)

        password_field = WebDriverWait(self.driver, 70).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        )
        password_field.send_keys(config('PASSWORD_INSTITUCIONAL'))
        password_field.send_keys(Keys.ENTER)

        ieee_box = WebDriverWait(self.driver, 40).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input.Typeahead-input"))
        )

        ieee_box = self.driver.find_element(By.CSS_SELECTOR, "input.Typeahead-input")
        ieee_box.send_keys("computational thinking")
        ieee_box.send_keys(Keys.ENTER)

        dropdown_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, "dropdownPerPageLabel"))
        )
        dropdown_button.click()

        items_per_page_100 = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item filter-popover-option' and contains(text(), '100')]"))
        )
        ActionChains(self.driver).move_to_element(items_per_page_100).click().perform()
        pagina_actual= 1
        num_paginas = 4

        while pagina_actual <= num_paginas:
            label_checkbox = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "results-actions-selectall"))
            )
            if label_checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", label_checkbox)
            self.driver.execute_script("arguments[0].click();", label_checkbox)

            export_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'myproject-export')]//button[contains(@class, 'xpl-btn-primary') and text()='Export']"))
            )
            export_button.click()
            time.sleep(2)
            citations_link = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'nav-link') and text()='Citations']"))
            )
            citations_link.click()
            self.driver.execute_script("arguments[0].click();", citations_link)

            time.sleep(2)

            label_for_radio = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//label[@for='download-ris']/input[@name='download-format' and @type='radio']"))
            )
            label_for_radio.click()

            download_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='stats-SearchResults_Citation_Download xpl-btn-primary' and not(@disabled)]"))
            )
            download_button.click()
            while not self.is_download_complete(self.download_path):
                    print("Esperando a que la descarga termine...")
            time.sleep(5)
            close_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'cursor-pointer') and contains(@class, 'd-flex')]//i[contains(@class, 'fa-times')]"))
            )
            close_button.click()

            next_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li.next-page-set button"))
            )
            next_button.click()
            time.sleep(5)
            pagina_actual += 1

        self.process_ris_file()
            
        

