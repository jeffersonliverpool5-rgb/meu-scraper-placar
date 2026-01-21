import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_jogos_definitivo():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # User-agent para parecer um PC real
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Acessando AiScore...")
        driver.get("https://www.aiscore.com/team-galatasaray/2ezk96i1ppawkn5")
        
        # Espera longa para carregar os placares do meio
        time.sleep(45) 

        # Tenta capturar TODOS os elementos que podem ser jogos
        elementos = driver.find_elements(By.XPATH, "//div[contains(@class, 'match')] | //div[contains(@class, 'item')]")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not elementos:
                # Se não achou nada por classe, pega o TEXTO PURO da página inteira
                print("Tentando captura por texto bruto...")
                texto_pagina = driver.find_element(By.TAG_NAME, "body").text
                f.write(texto_pagina)
            else:
                for el in elementos:
                    txt = el.text.strip().replace("\n", " ")
                    # Filtra apenas o que tem cara de jogo (ex: contém " - " ou " vs ")
                    if len(txt) > 20 and ("-" in txt or "vs" in txt or ":" in txt):
                        f.write(txt + "\n")

        print("Processo finalizado. Verifique o arquivo!")

    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_jogos_definitivo()
