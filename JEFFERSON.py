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
        
        # Espera forçada para o JavaScript carregar os números
        time.sleep(20) 
        
        # Rola um pouco a página para ativar o carregamento de dados dinâmicos
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(2)

        # Seletores via XPATH baseados na estrutura visual do AiScore (Placar central)
        try:
            # O tempo geralmente fica no centro, em cima ou embaixo do placar
            cronometro = driver.find_element(By.XPATH, "//div[contains(@class, 'match-status')]//span | //div[contains(@class, 'time-box')]").text
        except:
            cronometro = "Em jogo"

        try:
            # Busca o placar da esquerda (Casa) e direita (Fora)
            # No AiScore, os placares grandes ficam em spans dentro de containers de score
            placar_casa = driver.find_element(By.XPATH, "(//span[contains(@class, 'score')])[1]").text
            placar_fora = driver.find_element(By.XPATH, "(//span[contains(@class, 'score')])[2]").text
            
            # Se o placar vier vazio, tenta outro seletor de fallback
            if not placar_casa:
                placar_casa = driver.find_element(By.CLASS_NAME, "home-score").text
            if not placar_fora:
                placar_fora = driver.find_element(By.CLASS_NAME, "away-score").text
        except:
            placar_casa = "0"
            placar_fora = "0"

        resultado = f"{time.strftime('%d/%m/%Y %H:%M:%S')} - [{cronometro}] Casa {placar_casa} x {placar_fora} Fora"
        print(f"Resultado: {resultado}")

        # Gravação no arquivo
        with open("placares.txt", "a", encoding="utf-8") as f:
            f.write(resultado + "\n")

    except Exception as e:
        print(f"Erro Geral: {e}")
        with open("placares.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%d/%m/%Y %H:%M:%S')} - Falha técnica no carregamento\n")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar()
