import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair_aiscore():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Configuração específica para ambientes Linux/GitHub Actions
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        url = "https://www.aiscore.com/match-ca-penarol-boston-river/ndqmliw2oxehrkv"
        driver.get(url)
        
        # Espera o carregamento
        time.sleep(20)

        try:
            time_casa = driver.find_element(By.XPATH, "//div[contains(@class, 'home-team')]//a[contains(@class, 'name')]").text.strip()
            time_fora = driver.find_element(By.XPATH, "//div[contains(@class, 'away-team')]//a[contains(@class, 'name')]").text.strip()
        except:
            time_casa, time_fora = "Capital CF", "Real FC"

        try:
            g1 = driver.find_element(By.CLASS_NAME, "home-score").text.strip()
            g2 = driver.find_element(By.CLASS_NAME, "away-score").text.strip()
        except:
            g1, g2 = "0", "0"

        try:
            tempo_jg = driver.find_element(By.CSS_SELECTOR, ".score-status .status").text.strip()
            tempo_jg = tempo_jg.replace("\n", " ")
        except:
            tempo_jg = "Ao Vivo"

        resultado = f"{time_casa} {g1} X {g2} {time_fora} | {tempo_jg}"
        resultado = " ".join(resultado.split())

        # No Actions, o print é o que você consegue ver no log em tempo real
        print(f"--- PLACAR CAPTURADO: {resultado} ---")

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
    except Exception as e:
        print(f"ERRO: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Roda 100 vezes dentro da mesma Action
    for i in range(1, 101):
        print(f"\n[VOLTA {i}] Horário: {time.strftime('%H:%M:%S')}")
        extrair_aiscore()
        if i < 100:
            time.sleep(60)
