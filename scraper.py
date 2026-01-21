import time
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def buscar_placar_espn():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # LINK ENVIADO: São Paulo x Portuguesa
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/762098")
        
        # Espera até 20 segundos para os elementos de score aparecerem
        wait = WebDriverWait(driver, 20)
        
        # 1. CAPTURA OS GOLS (PLACAR)
        # A ESPN usa classes como 'detailScore' ou 'ScoreCell__Score'
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".detailScore__wrapper")))
            scores = driver.find_elements(By.CSS_SELECTOR, ".detailScore__wrapper > span")
            # Filtra apenas os números
            gols = [s.text.strip() for s in scores if s.text.strip().isdigit()]
        except:
            gols = ["0", "0"]

        # 2. CAPTURA O TEMPO (MINUTO)
        tempo = "Início"
        try:
            # Captura o elemento do status/tempo (ex: 3', Intervalo, Fim)
            status_el = driver.find_element(By.CSS_SELECTOR, ".game-status, .status-detail, .GameStatus__Text")
            tempo = status_el.text.strip()
        except:
            pass

        # 3. NOMES DOS TIMES (Garantindo que estão corretos)
        times = driver.find_elements(By.CSS_SELECTOR, ".format--long, .ShortName")
        time_a = times[0].text if len(times) > 0 else "São Paulo"
        time_b = times[1].text if len(times) > 1 else "Portuguesa"

        # MONTAGEM DO RESULTADO
        gol_casa = gols[0] if len(gols) >= 1 else "0"
        gol_fora = gols[1] if len(gols) >= 2 else "0"

        resultado = f"{time_a} {gol_casa} X {gol_fora} {time_b} | {tempo}"

        # SALVA NO ARQUIVO
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
        
        print(f"Sucesso: {resultado}")

    except Exception as e:
        print(f"Erro ao processar: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_espn()
