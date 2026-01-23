import time
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair_e_subir():
    options = Options()
    options.add_argument("--headless") # Roda sem abrir janela
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # URL do jogo que você quer monitorar
        url = "https://www.aiscore.com/match-south-island-united-fc-vanuatu-united-fc/9gklzi16gjpim7x"
        driver.get(url)
        
        # Espera o site carregar os números
        time.sleep(15)

        # 1. Busca os nomes
        try:
            time_casa = driver.find_element(By.XPATH, "//div[contains(@class, 'home-team')]//a[contains(@class, 'name')]").text.strip()
            time_fora = driver.find_element(By.XPATH, "//div[contains(@class, 'away-team')]//a[contains(@class, 'name')]").text.strip()
        except:
            time_casa, time_fora = "Capital CF", "Real FC"

        # 2. Busca o Placar
        try:
            g1 = driver.find_element(By.CLASS_NAME, "home-score").text.strip()
            g2 = driver.find_element(By.CLASS_NAME, "away-score").text.strip()
        except:
            g1, g2 = "0", "0"

        # 3. Busca o Tempo
        try:
            tempo_jg = driver.find_element(By.CSS_SELECTOR, ".score-status .status").text.strip()
            tempo_jg = tempo_jg.replace("\n", " ")
        except:
            tempo_jg = "Ao Vivo"

        resultado = f"{time_casa} {g1} X {g2} {time_fora} | {tempo_jg}"
        
        # SALVA LOCALMENTE
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"CAPTURA OK: {resultado}")

        # --- PARTE DO GITHUB ---
        # Garante que estamos na pasta certa para o Git
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        subprocess.run(["git", "add", "placares.txt"], check=True)
        subprocess.run(["git", "commit", "-m", f"Placar atualizado: {g1}x{g2}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("ENVIADO PARA O GITHUB!")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_e_subir()
