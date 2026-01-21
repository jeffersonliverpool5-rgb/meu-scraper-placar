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
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # LINK DO JOGO NEWCASTLE X PSV
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757778")
        
        # Espera o carregamento dos elementos dinâmicos
        time.sleep(30) 

        TIME_A = "Newcastle"
        TIME_B = "PSV"

        # 1. BUSCA O TEMPO (MINUTO)
        tempo = "Início"
        try:
            # Tenta localizar o tempo pela nova classe da ESPN
            tempo_el = driver.find_element(By.CSS_SELECTOR, ".GameStatus__Text, .game-time, .status-detail")
            if tempo_el.text:
                tempo = tempo_el.text.strip()
        except:
            texto_bruto = driver.find_element(By.TAG_NAME, "body").text
            minutos = re.findall(r"\d+'\+\d+'|\d+'|HT|Intervalo|Fim", texto_bruto)
            if minutos: tempo = minutos[0]

        # 2. BUSCA OS GOLS (PLACAR) - AJUSTADO PARA PEGAR O 2 X 0 DA FOTO
        gols = ["0", "0"]
        try:
            # Na foto, o placar fica dentro de classes como 'score-container' ou 'ScoreCell__Score'
            # Este seletor busca as classes de score mais comuns da ESPN atual
            elementos_score = driver.find_elements(By.CSS_SELECTOR, ".ScoreCell__Score, .score-container, .DetailView__Score")
            
            placar_encontrado = [e.text.strip() for e in elementos_score if e.text.strip().isdigit()]
            
            if len(placar_encontrado) >= 2:
                gols = placar_encontrado[:2]
        except:
            pass

        # MONTAGEM FINAL
        gol_casa = gols[0]
        gol_fora = gols[1]

        resultado = f"{TIME_A} {gol_casa} X {gol_fora} {TIME_B} | {tempo}"

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            print(f"Gravado: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_exato()
