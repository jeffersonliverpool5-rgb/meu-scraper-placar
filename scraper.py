import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_jogos_espn():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Acessando ESPN Resultados...")
        # Link da Champions League que você pediu
        driver.get("https://www.espn.com.br/futebol/resultados?liga=UEFA.CHAMPIONS")
        
        # Espera para carregar os resultados dinâmicos
        time.sleep(30) 

        # Na ESPN, os blocos de jogos geralmente estão em 'Table__TR' ou seções de placar
        # Usaremos um XPATH largo que pega as linhas de jogos
        elementos = driver.find_elements(By.XPATH, "//section[contains(@class, 'Card')]//tr | //div[contains(@class, 'Schedule')]")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not elementos:
                print("Tentando captura por texto bruto...")
                texto_pagina = driver.find_element(By.TAG_NAME, "body").text
                f.write(texto_pagina)
            else:
                for el in elementos:
                    txt = el.text.strip().replace("\n", " ")
                    # Filtro para pegar apenas linhas que tenham o placar (ex: 2 - 1) ou horário (ex: 17:00)
                    if len(txt) > 10 and ("-" in txt or ":" in txt):
                        f.write(txt + "\n")

        print("Processo finalizado. Verifique o arquivo placares.txt!")

    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_jogos_espn()
