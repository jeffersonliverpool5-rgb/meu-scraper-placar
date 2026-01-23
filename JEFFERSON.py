import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_definitivo():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        # Espera o site "estabilizar" os dados do placar ao vivo
        time.sleep(30) 
        
        # 1. Capturar Nomes dos Times
        try:
            nome_casa = driver.find_element(By.CSS_SELECTOR, ".home-team-name, .home-name").text.strip()
            nome_fora = driver.find_element(By.CSS_SELECTOR, ".away-team-name, .away-name").text.strip()
        except:
            nome_casa = "BSRC"
            nome_fora = "Indera FC"

        # 2. Capturar o Tempo (BUSCA AGRESSIVA)
        cronometro = "Ao vivo"
        try:
            # Pega TODO o texto da página para encontrar o minuto onde quer que ele esteja
            corpo_pagina = driver.find_element(By.TAG_NAME, "body").text
            # Procura por padrões como 45', 90+2', 15'
            match = re.search(r"(\d+\+?\d?')", corpo_pagina)
            if match:
                cronometro = match.group(1)
            else:
                # Segunda tentativa: buscar em elementos de status específicos
                cronometro = driver.find_element(By.CSS_SELECTOR, ".match-status, .status-info, .status-time").text.strip()
        except:
            pass

        # 3. Capturar Placares
        try:
            placar_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            placar_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            placar_casa = "0"
            placar_fora = "0"

        # Formata a string final
        # Garante que o cronômetro tenha o ' se for apenas número
        if cronometro.isdigit():
            cronometro += "'"
            
        resultado = f"[{cronometro}] {nome_casa} {placar_casa} x {placar_fora} {nome_fora}"
        print(f"Resultado: {resultado}")

        # Salva no arquivo 'placares.txt' limpando o anterior
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")

    except Exception as e:
        print(f"Erro no processo: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar_definitivo()
