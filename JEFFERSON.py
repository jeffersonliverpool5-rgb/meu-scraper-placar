from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def extrair_dados_partida():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    # Configurações do Navegador (Modo Headless para não abrir janela)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        
        # Aguarda até que o placar esteja visível (usando seletores comuns do AiScore)
        wait = WebDriverWait(driver, 20)
        
        # Extraindo o Placar (Seletores baseados na estrutura do AiScore)
        home_score = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "home-score"))).text
        away_score = driver.find_element(By.CLASS_NAME, "away-score").text
        
        # Extraindo o Cronômetro/Status
        status_tempo = driver.find_element(By.CLASS_NAME, "match-status").text
        
        resultado = f"Status: {status_tempo} | Placar: {home_score} x {away_score}"
        print(f"Dados capturados: {resultado}")

        # Salva no arquivo placares.txt
        with open("placares.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {resultado}\n")

    except Exception as e:
        print(f"Erro ao extrair: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_dados_partida()
