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
        url = "https://www.aiscore.com/match-capital-cf-real-fc/ezk96i369dxu1kn"
        driver.get(url)
        
        # Tempo de espera para o conteúdo dinâmico carregar
        time.sleep(12)

        # 1. Busca os nomes dos times
        try:
            time_casa = driver.find_element(By.XPATH, "//div[contains(@class, 'home-team')]//a[contains(@class, 'name')]").text.strip()
            time_fora = driver.find_element(By.XPATH, "//div[contains(@class, 'away-team')]//a[contains(@class, 'name')]").text.strip()
        except:
            time_casa, time_fora = "Casa", "Fora"

        # 2. Busca o Placar
        try:
            g1 = driver.find_element(By.CLASS_NAME, "home-score").text.strip()
            g2 = driver.find_element(By.CLASS_NAME, "away-score").text.strip()
        except:
            g1, g2 = "0", "0"

        # 3. BUSCA O TEMPO (O QUE VOCÊ PRECISA)
        try:
            # Tenta o seletor mais comum para o relógio/status no AiScore
            tempo_jg = driver.find_element(By.CSS_SELECTOR, ".score-status .status-name, .score-status .status").text.strip()
        except:
            # Backup caso o seletor mude durante o jogo
            try:
                tempo_jg = driver.find_element(By.XPATH, "//div[contains(@class, 'score-status')]").text.strip()
            except:
                tempo_jg = "--"

        # MONTAGEM DA LINHA FINAL COM O TEMPO
        resultado = f"{time_casa} {g1} X {g2} {time_fora} | Tempo: {tempo_jg}"
        
        # Limpeza de strings
        resultado = " ".join(resultado.split())

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"CAPTURA COMPLETA: {resultado}")

    except Exception as e:
        print(f"Erro na captura: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_aiscore()
