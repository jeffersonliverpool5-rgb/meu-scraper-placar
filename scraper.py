import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_ceramica_cleopatra_ao_vivo():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Link do Ceramica Cleopatra FC
        driver.get("https://www.aiscore.com/team-ceramica-cleopatra-fc/ndkz6i99r6teq3z")
        time.sleep(45) 

        elementos = driver.find_elements(By.CLASS_NAME, "match-item")
        jogo_ao_vivo = ""

        for el in elementos:
            texto = el.text.strip()
            # Filtro: Nome do time + Indicador de tempo real (85', HT, etc)
            if "Ceramica" in texto and re.search(r"\d+'|HT", texto):
                limpo = texto.replace("Egypt Premier League", "").replace("\n", " ").strip()
                limpo = re.sub(r'\d+\s+[a-zA-Z]+\s+\d{2}:\d{2}', '', limpo)
                jogo_ao_vivo = " ".join(limpo.split())
                break 

        with open("placares.txt", "w", encoding="utf-8") as f:
            if jogo_ao_vivo:
                f.write(f"AO VIVO: {jogo_ao_vivo}\n")
            else:
                f.write("Nenhum jogo do Ceramica Cleopatra ao vivo no momento.\n")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_ceramica_cleopatra_ao_vivo()
