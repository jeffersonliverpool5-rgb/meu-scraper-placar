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
    # User-agent mais real para evitar bloqueio
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        # Espera 15 segundos para garantir o carregamento do conteúdo dinâmico
        time.sleep(15) 
        
        # Tentativa 1: Seletores por Classe de Placar
        try:
            # Buscando o container principal do placar
            placar_casa = driver.find_element(By.XPATH, "//div[contains(@class, 'home-score')] | //span[contains(@class, 'home-score')]").text
            placar_fora = driver.find_element(By.XPATH, "//div[contains(@class, 'away-score')] | //span[contains(@class, 'away-score')]").text
            cronometro = driver.find_element(By.XPATH, "//div[contains(@class, 'match-status')] | //span[contains(@class, 'status')]").text
        except:
            # Tentativa 2: Busca por estrutura de posição (mais genérica)
            placar_casa = driver.find_element(By.XPATH, "(//div[contains(@class, 'score')])[1]").text
            placar_fora = driver.find_element(By.XPATH, "(//div[contains(@class, 'score')])[2]").text
            cronometro = "Em andamento"

        info = f"{time.strftime('%d/%m/%Y %H:%M:%S')} - [{cronometro}] Casa {placar_casa} x {placar_fora} Fora"
        print(f"Capturado: {info}")

        with open("placares.txt", "a", encoding="utf-8") as f:
            f.write(info + "\n")

    except Exception as e:
        print(f"Erro: {e}")
        # Log de erro para o arquivo para você saber o que falhou
        with open("placares.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%d/%m/%Y %H:%M:%S')} - Erro ao localizar elementos\n")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar()
