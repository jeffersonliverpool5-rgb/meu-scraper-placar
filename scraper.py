
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_placar_exato():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # LINK DO JOGO
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757771")
        time.sleep(30)
        
        # 1. BUSCA O PLACAR PELAS CLASSES ESPECÍFICAS (Geralmente .score-container ou .score)
        # Vamos pegar os dois elementos de placar que ficam no topo
        try:
            scores = driver.find_elements(By.CLASS_NAME, "score")
            if len(scores) >= 2:
                gol_casa = scores[0].text.strip()
                gol_fora = scores[1].text.strip()
            else:
                # Se não achar a classe 'score', tenta a 'gamestrip-score'
                scores = driver.find_elements(By.CSS_SELECTOR, ".Gamestrip__Score")
                gol_casa = scores[0].text.strip()
                gol_fora = scores[1].text.strip()
        except:
            gol_casa, gol_fora = "0", "0"

        # 2. BUSCA O TEMPO (Garantindo que pega o minuto real)
        try:
            tempo = driver.find_element(By.CLASS_NAME, "game-time").text.strip()
        except:
            try:
                tempo = driver.find_element(By.CLASS_NAME, "status-detail").text.strip()
            except:
                tempo = "Ao Vivo"

        # --- NOMES FIXOS PARA NÃO PEGAR LIXO ---
        TIME_A = "Galatasaray"
        TIME_B = "Atlético Madrid"

        resultado = f"{TIME_A} {gol_casa} X {gol_fora} {TIME_B} | {tempo}"

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            print(f"Placar Corrigido: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_exato()
