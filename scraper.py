import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extrair_aiscore():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://www.aiscore.com/match-argentinos-juniors-ferrocarril-midland/34kgmio142waeko"
        driver.get(url)
        
        # Espera até que o placar esteja visível (máximo 30s)
        wait = WebDriverWait(driver, 30)
        
        # Captura Nomes dos Times
        # O AiScore costuma usar a classe 'name' dentro do bloco de equipe
        times = driver.find_elements(By.CLASS_NAME, "name")
        time_casa = times[0].text.strip() if len(times) > 0 else "Casa"
        time_fora = times[1].text.strip() if len(times) > 1 else "Fora"

        # Captura Placar
        try:
            # Busca pelo container de score que geralmente tem a classe 'score'
            g1 = driver.find_element(By.CLASS_NAME, "home-score").text.strip()
            g2 = driver.find_element(By.CLASS_NAME, "away-score").text.strip()
        except:
            g1, g2 = "0", "0"

        # Captura Tempo do Jogo
        try:
            # Procura pela classe de status ou tempo (comum no AiScore: 'status' ou 'time')
            tempo_jogo = driver.find_element(By.CLASS_NAME, "status").text.strip()
        except:
            tempo_jogo = "Andamento"

        # Montagem da Linha Única
        resultado = f"{time_casa} {g1} X {g2} {time_fora} | {tempo_jogo}"
        resultado = resultado.replace("\n", "").strip()

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"SUCESSO: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(f"Erro na captura dos dados")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_aiscore()
