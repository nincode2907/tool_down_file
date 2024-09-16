from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

link_page = "https://nhasachmienphi.com/dac-nhan-tam.html"

driver = webdriver.Chrome()
driver.get(link_page)

time.sleep(5)

pdf_link = driver.find_element(By.XPATH, "//a[contains(@href, '.pdf')]").get_attribute('href')
print(f"URL của file PDF: {pdf_link}")

response = requests.get(pdf_link)
pdf_file_name = pdf_link.split('/')[-1] 
with open(pdf_file_name, 'wb') as file:
    file.write(response.content)

print(f"Đã tải file PDF: {pdf_file_name}")
driver.quit()
