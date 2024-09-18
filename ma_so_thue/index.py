import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from env import url_init, start_date, end_date, tax_codes, init_folder_download

driver = webdriver.Chrome()

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def download_file(url, save_path, filename):
    response = requests.get(url)
    with open(os.path.join(save_path, filename), 'wb') as file:
        file.write(response.content)
    print(f"Downloaded: {filename} in {save_path}")

def process_tax_code(tax_code, start_date, end_date):
    # Truy cập vào website (nhập url website của anh)
    driver.get(url_init)
    
    tax_input = driver.find_element(By.NAME, "MST")
    tax_input.clear()
    tax_input.send_keys(tax_code)
    
    start_date_input = driver.find_element(By.NAME, "from_date")
    end_date_input = driver.find_element(By.NAME, "to_date")
    
    start_date_input.clear()
    start_date_input.send_keys(start_date)
    
    end_date_input.clear()
    end_date_input.send_keys(end_date)
    
    search_button = driver.find_element(By.ID, "btn_search")
    search_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table#result_table"))
    )

    days = driver.find_elements(By.CSS_SELECTOR, "table#result_table tr")

    tax_code_dir = os.path.join(init_folder_download, tax_code)
    create_directory(tax_code_dir)
    
    for day in days[1:]:
        day_text = day.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        day.click()
        
        day_dir = os.path.join(tax_code_dir, day_text)
        create_directory(day_dir)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table#declaration_table"))
        )

        declarations = driver.find_elements(By.CSS_SELECTOR, "table#declaration_table tr")

        for declaration in declarations[1:]:
            download_button = declaration.find_element(By.CSS_SELECTOR, "a.download")
            download_url = download_button.get_attribute('href')
            filename = download_url.split("/")[-1]
            download_file(download_url, day_dir, filename)
        
        driver.back()  

for tax_code in tax_codes:
    process_tax_code(tax_code, start_date, end_date)

driver.quit()
