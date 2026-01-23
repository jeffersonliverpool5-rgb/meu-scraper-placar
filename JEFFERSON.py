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
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        # Espera o carregamento total dos dados dinâmicos
        wait = WebDriverWait(driver, 20)
        
        # 1. Extrair o Cronômetro (Tempo de jogo)
        try:
            # No AiScore, o tempo fica geralmente em uma classe 'status' ou 'time'
            cronometro = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'match-status')] | //div[contains(@class, 'time-box')]"))).text
        except:
            cronometro = "Tempo N/A"

        # 2. Extrair os Placares (Usando seletores específicos de pontuação)
        try:
            # Buscando o valor numérico do placar
            placar_casa = driver.find_element(By.XPATH, "//div[contains(@class, 'home-team')]//span[contains(@class, 'score')] | (//span[contains(@class, 'score')])[1]").text
            placar_fora = driver.find_element(By.XPATH, "//div[contains(@class, 'away-team')]//span[contains(@class, 'score')] | (//span[contains(@class, 'score')])[2]").text
        except:
            placar_casa = "0"
            placar_fora = "0"

        # Formata a string final
        # Exemplo: 23/01/2026 12:45:00 - [25'] Casa 1 x 0 Fora
        resultado = f"{time.strftime('%d/%m/%Y %H:%M:%S')} - [{cronometro}] Casa {placar_casa} x {placar_fora} Fora"
        print(f"Capturado: {resultado}")

        # Salva no arquivo
        with open("placares.txt", "a", encoding="utf-8") as f:
            f.write(resultado + "\n")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar()
