from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re
from google.cloud import bigquery
from google.oauth2 import service_account
import os
import base64
import json
from dotenv import load_dotenv

load_dotenv()

# === Carga las credenciales desde la variable de entorno ===
credentials_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")

if not credentials_json:
    raise ValueError("Falta la variable de entorno GOOGLE_APPLICATION_CREDENTIALS_JSON")

credentials_dict = json.loads(base64.b64decode(credentials_json))
credentials = service_account.Credentials.from_service_account_info(credentials_dict)

# === Configura Selenium para entornos tipo Docker / Cloud Run ===
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)

# === Scraping de Yogonet ===
url = "https://www.yogonet.com/international/"
driver.get(url)
time.sleep(5)

data = []
articles = driver.find_elements(By.CSS_SELECTOR, "h2.titulo.fuente_roboto_slab")

for article in articles:
    try:
        link_element = article.find_element(By.TAG_NAME, "a")
        title = link_element.text.strip()
        link = link_element.get_attribute("href")

        # Volanta
        try:
            volanta_element = article.find_element(By.XPATH, "./preceding-sibling::div[contains(@class, 'volanta')]")
            volanta = volanta_element.text.strip()
        except:
            volanta = "N/A"

        # Imagen
        try:
            image_element = article.find_element(By.XPATH, "./following::div[contains(@class, 'imagen')]//img")
            image_url = image_element.get_attribute("src")
        except:
            image_url = "No Image"

        data.append({
            "volanta": volanta,
            "title": title,
            "image": image_url,
            "link": link
        })

    except Exception as e:
        print(f"Error al extraer datos: {e}")

driver.quit()

# === Convierte a DataFrame y agrega columnas ===
df = pd.DataFrame(data)
if not df.empty:
    df["title_word_count"] = df["title"].apply(lambda x: len(x.split()))
    df["title_char_count"] = df["title"].apply(len)
    df["capital_words"] = df["title"].apply(lambda x: [word for word in x.split() if re.match(r"^[A-Z][a-z]+$", word)])

    # === Sube a BigQuery ===
    project_id = os.environ.get("PROJECT_ID", "default-project-id")
    dataset_id = os.environ.get("DATASET_ID", "default_dataset")
    table_id = os.environ.get("TABLE_ID", "default_table")
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    df.to_gbq(full_table_id, project_id=project_id, if_exists="replace", credentials=credentials)
    print("Datos subidos")
else:
    print("Sin datos")
