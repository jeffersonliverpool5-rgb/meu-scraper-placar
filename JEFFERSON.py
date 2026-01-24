import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def commit_file():
    """Função para salvar o arquivo no GitHub de verdade"""
    try:
        subprocess.run(["git", "config", "--global", "user.name", "GitHub Actions"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "add", "placares.txt"], check=True)
        subprocess.run(["git", "commit", "-m", "Atualizando placar [skip ci]"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Arquivo enviado para o repositório!")
    except Exception as e:
        print(f"⚠️ Erro ao comitar (pode não haver mudanças): {e}")

def extrair_aiscore():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://www.aiscore.com/match-ca-penarol-boston-river/ndqmliw2oxehrkv"
        driver.get(url)
        time.sleep(15)

        # Captura de dados (Sua lógica original)
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

        # Salva localmente
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
        
        print(f"Capturado: {resultado}")
        
        # Envia para o GitHub
        commit_file()

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # No Actions, rodar 100 vezes pode exceder o tempo limite (6 horas).
    # Vamos rodar as 100 vezes com 1 min de intervalo.
    for i in range(1, 101):
        print(f"\n--- RODADA {i} ---")
        extrair_aiscore()
        time.sleep(60)
