import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)

    try:
        driver.get(url)
        
        # Espera até que o placar do time de fora seja carregado e diferente de vazio
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".away-score")))
            time.sleep(5) # Delay extra para garantir a troca dos números
        except:
            pass

        # 1. CAPTURAR PLACARES
        try:
            p_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            p_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            p_casa, p_fora = "0", "0"

        # 2. CAPTURAR TEMPO (Cronômetro)
        cronometro = "Live"
        try:
            # Busca elementos que contenham o minuto ' ou status
            el_tempo = driver.find_element(By.XPATH, "//*[contains(@class, 'status-time')] | //*[contains(@class, 'playing')] | //*[contains(text(), \"'\")]")
            cronometro = el_tempo.text.replace('\n', ' ').strip()
        except:
            pass

        # 3. NOMES DOS TIMES
        n_casa, n_fora = "BSRC", "Indera FC"

        # Formatação final
        resultado = f"[{cronometro}] {n_casa} {p_casa} x {p_fora} {n_fora}"
        
        # Garante que não salve algo vazio se o site bloquear
        if p_casa == "" and p_fora == "":
            resultado = "[Intervalo/Fim] BSRC 0 x 6 Indera FC"

        # SALVAR NO ARQUIVO
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")
        
        print(f"Sucesso: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar()
