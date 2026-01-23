import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_completo():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        # Espera generosa para garantir que o script do cronômetro carregue
        time.sleep(30) 
        
        # 1. Capturar Nomes dos Times
        try:
            nome_casa = driver.find_element(By.CSS_SELECTOR, ".home-team-name, .home-name").text
            nome_fora = driver.find_element(By.CSS_SELECTOR, ".away-team-name, .away-name").text
        except:
            nome_casa = "BSRC"
            nome_fora = "Indera FC"

        # 2. Capturar o Tempo (Cronômetro)
        # Tentando localizar o span que contém o caractere de minutos (')
        try:
            # Seletor focado na div de status que contém o tempo real
            cronometro = driver.find_element(By.XPATH, "//div[contains(@class, 'match-status')]//span[contains(text(), \"'\")]").text
            if not cronometro:
                # Fallback para qualquer texto dentro da caixa de tempo
                cronometro = driver.find_element(By.CSS_SELECTOR, ".status-info, .time").text
        except:
            cronometro = "Em jogo"

        # 3. Capturar Placares
        try:
            placar_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text
            placar_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text
        except:
            placar_casa = "0"
            placar_fora = "0"

        # Montagem da linha: Data - [Tempo] TimeCasa 0 x 0 TimeFora
        resultado = f"{time.strftime('%d/%m/%Y %H:%M:%S')} - [{cronometro}] {nome_casa} {placar_casa} x {placar_fora} {nome_fora}"
        print(f"Resultado: {resultado}")

        # Salva limpando o anterior
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar_completo()
