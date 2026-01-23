import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Captura o Placar (tentando seletores comuns de placar ao vivo)
        # O AiScore costuma usar classes como 'score' ou 'home-score'/'away-score'
        try:
            placar_casa = wait.until(EC.presence_of_element_located((By.CSS_NAME, ".home-score, .score-item.home"))).text
            placar_fora = driver.find_element(By.CSS_NAME, ".away-score, .score-item.away").text
            cronometro = driver.find_element(By.CSS_NAME, ".match-status, .time-box").text
        except:
            # Fallback caso o site mude a estrutura
            placar_casa = "N/A"
            placar_fora = "N/A"
            cronometro = "Não iniciado/Fim"

        info = f"{time.strftime('%d/%m/%Y %H:%M:%S')} - [{cronometro}] Casa {placar_casa} x {placar_fora} Fora"
        print(f"Sucesso: {info}")

        # Escrita no arquivo
        with open("placares.txt", "a", encoding="utf-8") as f:
            f.write(info + "\n")

    except Exception as e:
        print(f"Erro na extração: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar()
