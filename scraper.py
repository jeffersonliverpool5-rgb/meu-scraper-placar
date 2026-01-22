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
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://www.aiscore.com/match-argentinos-juniors-ferrocarril-midland/34kgmio142waeko"
        driver.get(url)
        
        # Espera o carregamento (AiScore é pesado)
        time.sleep(15)

        # 1. Nomes dos Times
        try:
            time_casa = driver.find_element(By.XPATH, "//div[contains(@class, 'home-team')]//a[contains(@class, 'name')]").text.strip()
            time_fora = driver.find_element(By.XPATH, "//div[contains(@class, 'away-team')]//a[contains(@class, 'name')]").text.strip()
        except:
            time_casa, time_fora = "Argentinos Jrs", "Midland"

        # 2. Placar
        try:
            g1 = driver.find_element(By.CLASS_NAME, "home-score").text.strip()
            g2 = driver.find_element(By.CLASS_NAME, "away-score").text.strip()
        except:
            g1, g2 = "0", "0"

        # 3. TEMPO REAL (Cronômetro)
        tempo_jg = ""
        try:
            # Tenta pegar o cronômetro ativo (ex: 34')
            tempo_jg = driver.find_element(By.CSS_SELECTOR, ".score-status .status-time").text.strip()
        except:
            try:
                # Se não achar o anterior, tenta o status geral (pode ser "Half-time", "Finished")
                tempo_jg = driver.find_element(By.CSS_SELECTOR, ".score-status .status").text.strip()
            except:
                tempo_jg = "Andamento"

        # Limpeza para evitar quebras de linha
        tempo_jg = tempo_jg.replace("\n", " ").strip()
        if not tempo_jg: tempo_jg = "Vivo"

        # Montagem da Linha
        resultado = f"{time_casa} {g1} X {g2} {time_fora} | {tempo_jg}"
        resultado = " ".join(resultado.split())

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"DEBUG: {resultado}")

    except Exception as e:
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(f"Erro na captura")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_aiscore()
