import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_final():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        # Espera forçada para o WebSocket atualizar o tempo
        time.sleep(35) 
        
        # 1. Nomes dos Times
        try:
            nome_casa = driver.find_element(By.CSS_SELECTOR, ".home-team-name, .home-name").text.strip()
            nome_fora = driver.find_element(By.CSS_SELECTOR, ".away-team-name, .away-name").text.strip()
        except:
            nome_casa = "BSRC"
            nome_fora = "Indera FC"

        # 2. O CRONÔMETRO (Busca por seletores dinâmicos do AiScore)
        cronometro = ""
        try:
            # Tenta encontrar o elemento que tem o minuto (ex: 75')
            # O seletor .status-time .playing é o mais comum para o tempo real
            el_tempo = driver.find_element(By.CSS_SELECTOR, ".status-time, .playing, .match-status span")
            cronometro = el_tempo.text.strip()
            
            # Se vier vazio ou sem o ', tenta buscar o texto do pai
            if not cronometro or "'" not in cronometro:
                cronometro = driver.find_element(By.CLASS_NAME, "match-status").text.strip()
        except:
            cronometro = "Ao vivo"

        # 3. Placares
        try:
            placar_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            placar_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            placar_casa = "0"
            placar_fora = "0"

        # Limpeza: Se o cronômetro capturar o placar por erro, definimos como 'Live'
        if ":" in cronometro: cronometro = "Live"
        
        # Formato: [70'] BSRC 0 x 4 Indera FC
        resultado = f"[{cronometro}] {nome_casa} {placar_casa} x {placar_fora} {nome_fora}"
        
        # Salva no arquivo 'placares.txt' limpando o anterior
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")
            
        print(f"Sucesso: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar_final()import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_final():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        # Espera forçada para o WebSocket atualizar o tempo
        time.sleep(35) 
        
        # 1. Nomes dos Times
        try:
            nome_casa = driver.find_element(By.CSS_SELECTOR, ".home-team-name, .home-name").text.strip()
            nome_fora = driver.find_element(By.CSS_SELECTOR, ".away-team-name, .away-name").text.strip()
        except:
            nome_casa = "BSRC"
            nome_fora = "Indera FC"

        # 2. O CRONÔMETRO (Busca por seletores dinâmicos do AiScore)
        cronometro = ""
        try:
            # Tenta encontrar o elemento que tem o minuto (ex: 75')
            # O seletor .status-time .playing é o mais comum para o tempo real
            el_tempo = driver.find_element(By.CSS_SELECTOR, ".status-time, .playing, .match-status span")
            cronometro = el_tempo.text.strip()
            
            # Se vier vazio ou sem o ', tenta buscar o texto do pai
            if not cronometro or "'" not in cronometro:
                cronometro = driver.find_element(By.CLASS_NAME, "match-status").text.strip()
        except:
            cronometro = "Ao vivo"

        # 3. Placares
        try:
            placar_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            placar_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            placar_casa = "0"
            placar_fora = "0"

        # Limpeza: Se o cronômetro capturar o placar por erro, definimos como 'Live'
        if ":" in cronometro: cronometro = "Live"
        
        # Formato: [70'] BSRC 0 x 4 Indera FC
        resultado = f"[{cronometro}] {nome_casa} {placar_casa} x {placar_fora} {nome_fora}"
        
        # Salva no arquivo 'placares.txt' limpando o anterior
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")
            
        print(f"Sucesso: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar_final()
