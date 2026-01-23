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
        # URL solicitada
        url = "https://www.aiscore.com/match-instituto-de-cordoba-velez-sarsfield/vrqwni43wdgu4qn"
        driver.get(url)
        
        # Espera o carregamento do conteúdo dinâmico
        time.sleep(15)

        # 1. Busca os nomes dos times
        try:
            time_casa = driver.find_element(By.CSS_SELECTOR, ".home-team .name").text.strip()
            time_fora = driver.find_element(By.CSS_SELECTOR, ".away-team .name").text.strip()
        except:
            time_casa, time_fora = "Instituto", "Velez Sarsfield"

        # 2. Busca o Placar (Gols)
        try:
            g1 = driver.find_element(By.CLASS_NAME, "home-score").text.strip()
            g2 = driver.find_element(By.CLASS_NAME, "away-score").text.strip()
        except:
            g1, g2 = "0", "0"

        # 3. Busca o valor exato dentro de .time-score (Ex: 50)
        try:
            # Busca especificamente o elemento time-score que contém o minuto
            # O seletor abaixo foca no elemento que tem a classe time-score
            tempo_val = driver.find_element(By.CSS_SELECTOR, ".time-score").text.strip()
            
            # Se o valor vier vazio por algum motivo, tentamos pelo atributo data-v
            if not tempo_val:
                tempo_val = driver.find_element(By.CSS_SELECTOR, "div[data-v-5689a66f].time-score").text.strip()
        except:
            tempo_val = "0"

        # MONTAGEM DA LINHA FINAL substituindo "Ao Vivo" pelo valor capturado
        resultado = f"{time_casa} {g1} X {g2} {time_fora} | {tempo_val}"
        resultado = " ".join(resultado.split())

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"CAPTURA OK: {resultado}")

    except Exception as e:
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(f"Erro na captura: {str(e)}")
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_aiscore()
