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
        # Tempo de espera para o carregamento do live score
        time.sleep(25) 
        
        # 1. Captura o Tempo de Jogo (Cronômetro)
        try:
            # Tenta encontrar o elemento que contém o minuto atual
            cronometro = driver.find_element(By.XPATH, "//div[contains(@class, 'match-status')]//span[contains(text(), \"'\")] | //span[contains(@class, 'status-time')] | //div[contains(@class, 'time-box')]").text
            if not cronometro:
                cronometro = driver.find_element(By.CSS_SELECTOR, ".match-status").text
        except:
            cronometro = "Live"

        # 2. Captura os Placares
        try:
            placar_casa = driver.find_element(By.CSS_SELECTOR, ".home-score, .score-item.home").text
            placar_fora = driver.find_element(By.CSS_SELECTOR, ".away-score, .score-item.away").text
        except:
            placar_casa = "0"
            placar_fora = "0"

        # Formatação Final: Data/Hora - [Tempo] Placar
        # Exemplo: 23/01/2026 13:05:00 - [32'] 0 x 0
        resultado = f"{time.strftime('%d/%m/%Y %H:%M:%S')} - [{cronometro}] {placar_casa} x {placar_fora}"
        print(f"Atualizando: {resultado}")

        # Sobrescreve o arquivo (modo 'w') para manter apenas a última linha
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar()
