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
        # Espera o site carregar completamente
        time.sleep(25) 
        
        # Tenta pegar o tempo (cronômetro)
        try:
            # Procura especificamente pelo texto que contém o minuto (ex: 35')
            cronometro = driver.find_element(By.CSS_SELECTOR, ".match-status .status, .time-box, .status-info").text
        except:
            cronometro = "Ao vivo"

        # Tenta pegar os placares usando seletores mais diretos do cabeçalho
        try:
            # Procura pelos números grandes do placar
            placar_casa = driver.find_element(By.CSS_SELECTOR, ".home-score, .score-item.home").text
            placar_fora = driver.find_element(By.CSS_SELECTOR, ".away-score, .score-item.away").text
            
            # Se ainda vier vazio, tenta via XPath direto no container de placar
            if not placar_casa or not placar_fora:
                placar_casa = driver.find_element(By.XPATH, "//div[contains(@class,'score-number')][1]").text
                placar_fora = driver.find_element(By.XPATH, "//div[contains(@class,'score-number')][2]").text
        except:
            placar_casa = "0"
            placar_fora = "0"

        # Se o cronômetro pegou o placar por erro, limpamos
        if ":" in placar_casa: placar_casa = "0"

        resultado = f"{time.strftime('%d/%m/%Y %H:%M:%S')} - [{cronometro}] Casa {placar_casa} x {placar_fora} Fora"
        print(f"Gravando: {resultado}")

        # MODO 'w' APAGA O ANTERIOR E SALVA O NOVO
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar()
