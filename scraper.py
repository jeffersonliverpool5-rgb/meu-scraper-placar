import time
import re
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
    # User-agent mais atualizado para evitar que o site entregue uma página antiga
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Forçamos o link com um parâmetro de tempo para evitar cache do navegador
        driver.get(f"https://www.espn.com.br/futebol/partida/_/jogoId/757777?refresh={int(time.time())}")
        
        # Espera o tempo necessário para o placar "subir" na tela
        time.sleep(30) 

        TIME_A = "Newcastle"
        TIME_B = "PSV"

        # 1. BUSCA O TEMPO
        tempo = "Início"
        try:
            # Tenta pegar o tempo exato que aparece entre os placares
            tempo_el = driver.find_element(By.CSS_SELECTOR, ".GameStatus__Text, .status-detail, .game-time")
            if tempo_el.text:
                tempo = tempo_el.text.strip()
        except:
            pass

        # 2. BUSCA OS GOLS (PLACAR REAL)
        # Seletor focado na estrutura da Gamestrip (a barra principal da sua foto)
        gols = ["0", "0"]
        try:
            # A ESPN coloca os gols em elementos com a classe 'ScoreCell__Score' 
            # ou dentro de 'div.score-container'. Vamos pegar todos os que forem números.
            elementos = driver.find_elements(By.CSS_SELECTOR, "div.ScoreCell__Score, span.ScoreCell__Score, .score-container")
            
            # Filtramos apenas o que é número puro
            valores = [e.text.strip() for e in elementos if e.text.strip().isdigit()]
            
            if len(valores) >= 2:
                # Pegamos os dois primeiros números encontrados na parte superior
                gols = valores[:2]
        except:
            pass

        resultado = f"{TIME_A} {gols[0]} X {gols[1]} {TIME_B} | {tempo}"

        # Grava o arquivo
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            print(f"ATUALIZADO: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_exato()
