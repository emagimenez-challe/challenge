import os
import time
import re
import pandas as pd
import spacy
from selenium import webdriver
from selenium.webdriver.common.by import By

# === Cargar modelo de NLP ===
nlp = spacy.load("en_core_web_sm")

# === Configurar Selenium ===
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)

# === Acceder al sitio ===
url = "https://www.yogonet.com/international/"
driver.get(url)
time.sleep(5)

data = []
articles = driver.find_elements(By.CSS_SELECTOR, "h2.titulo.fuente_roboto_slab")
print(f"Elementos encontrados: {len(articles)}")

for article in articles:
    try:
        link_element = article.find_element(By.TAG_NAME, "a")
        title = link_element.text.strip()

        # Validar con spaCy si es un posible título
        doc = nlp(title)
        if len(title.split()) < 4 or not any(ent.label_ in ["ORG", "GPE", "EVENT", "WORK_OF_ART"] for ent in doc.ents):
            print(f"Título descartado por AI: {title}")
            continue

        link = link_element.get_attribute("href")

        # Volanta (texto anterior)
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

        print(f"Título aceptado: {title}")

    except Exception as e:
        print(f"Error al procesar: {e}")

driver.quit()

# === Convertir a DataFrame y generar métricas ===
df = pd.DataFrame(data)
if not df.empty:
    df["title_word_count"] = df["title"].apply(lambda x: len(x.split()))
    df["title_char_count"] = df["title"].apply(len)
    df["capital_words"] = df["title"].apply(lambda x: [word for word in x.split() if re.match(r"^[A-Z][a-z]+$", word)])
    df.to_csv("scraped.csv", index=False)
    print("CSV generado")
else:
    print("No se encontraron datos.")
