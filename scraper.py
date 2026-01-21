import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def buscar_dados_ge():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 25) # Espera até 25 segundos
    
    try:
        driver.get("https://ge.globo.com/sp/futebol/campeonato-paulista/jogo/21-01-2026/sao-paulo-portuguesa.ghtml")
        
        # Espera o elemento do tempo (a classe da área azul) estar visível
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "placar-jogo__periodo")))

        # 1. PEGAR OS GOLS
        gols = driver.find_elements(By.CLASS_NAME, "placar-jogo__equipe--placar")
        gol_casa = gols[0].text.strip() if len(gols) > 0 else "0"
        gol_fora = gols[1].text.strip() if len(gols) > 1 else "0"

        # 2. PEGAR O TEMPO (28:23 1T)
        # Usamos uma busca mais ampla caso a classe mude
        try:
            tempo_el = driver.find_element(By.CSS_SELECTOR, ".placar-jogo__periodo, .tempo-jogo")
            tempo = tempo_el.text.replace("\n", " ").strip()
        except:
            tempo = "Em andamento"

        # 3. PEGAR NOMES
        nomes = driver.find_elements(By.CLASS_NAME, "placar-jogo__equipe--nome")
        time_a = nomes[0].text.strip() if len(nomes) > 0 else "SAO"
        time_b = nomes[1].text.strip() if len(nomes) > 1 else "POR"

        resultado = f"{time_a} {gol_casa} X {gol_fora} {time_b} | {tempo}"
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"Sucesso: {resultado}")

    except Exception as e:
        print(f"Erro ao capturar: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_dados_ge()
