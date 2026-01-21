import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def buscar_placar_exato():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # Define um tempo máximo de espera de 20 segundos
    wait = WebDriverWait(driver, 20)
    
    try:
        # URL do jogo
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757778")
        
        # Aguarda até que o placar esteja visível na página
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".detail_item--score, .Gamestrip__Score")))

        # 1. BUSCA O TEMPO/STATUS DO JOGO
        try:
            tempo = driver.find_element(By.CSS_SELECTOR, ".game-status, .status-detail, .Gamestrip__Time").text.strip()
        except:
            tempo = "Status indisponível"

        # 2. BUSCA OS GOLS (PLACAR)
        # Seletores específicos da ESPN para os números do placar
        try:
            # Tenta capturar os scores individuais
            scores = driver.find_elements(By.CSS_SELECTOR, ".Gamestrip__Score")
            if len(scores) >= 2:
                gol_casa = scores[0].text.strip()
                gol_fora = scores[1].text.strip()
            else:
                # Fallback para outro seletor comum
                scores = driver.find_elements(By.CLASS_NAME, "score")
                gol_casa = scores[0].text.strip() if len(scores) > 0 else "0"
                gol_fora = scores[1].text.strip() if len(scores) > 1 else "0"
        except:
            gol_casa, gol_fora = "0", "0"

        # NOMES DOS TIMES
        TIME_A = "Newcastle"
        TIME_B = "PSV"

        resultado = f"{TIME_A} {gol_casa} X {gol_fora} {TIME_B} | {tempo}"

        # Grava o resultado
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"Sucesso: {resultado}")

    except Exception as e:
        print(f"Erro ao processar: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_exato()
