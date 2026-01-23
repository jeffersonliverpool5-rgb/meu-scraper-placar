import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_tudo():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        # Espera 30 segundos para o cronômetro "acordar" no site
        time.sleep(30) 
        
        # 1. Capturar Nomes dos Times
        try:
            nome_casa = driver.find_element(By.CSS_SELECTOR, ".home-team-name, .home-name").text.strip()
            nome_fora = driver.find_element(By.CSS_SELECTOR, ".away-team-name, .away-name").text.strip()
        except:
            nome_casa = "BSRC"
            nome_fora = "Indera FC"

        # 2. Capturar o Tempo (CRONÔMETRO EXATO)
        cronometro = ""
        try:
            # Tenta pegar especificamente o elemento que pisca o minuto
            # O AiScore costuma usar a classe 'status-info' ou 'playing'
            temp_el = driver.find_element(By.XPATH, "//span[contains(@class, 'status-time')] | //div[contains(@class, 'match-status')]//span[contains(text(), \"'\")]")
            cronometro = temp_el.text.strip()
        except:
            # Se falhar, faz uma busca geral por qualquer texto que tenha o sinal '
            try:
                cronometro = driver.find_element(By.XPATH, "//*[contains(text(), \"'\") and not(contains(text(), '\"'))]").text.strip()
            except:
                cronometro = "Live"

        # 3. Capturar Placares
        try:
            placar_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            placar_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            placar_casa = "0"
            placar_fora = "0"

        # Formato final sem data/hora: [Tempo] TimeCasa 0 x 0 TimeFora
        # Limpeza extra no cronômetro para não vir lixo
        cronometro = cronometro.replace('\n', '').strip()
        
        resultado = f"[{cronometro}] {nome_casa} {placar_casa} x {placar_fora} {nome_fora}"
        print(f"Resultado Final: {resultado}")

        # Salva e apaga o anterior
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_tudo()
