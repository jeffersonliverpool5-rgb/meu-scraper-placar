import time
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
    
    try:
        # LINK DO JOGO NEWCASTLE X PSV
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757777")
        
        # Espera técnica para o JavaScript da ESPN renderizar os números reais
        time.sleep(25) 

        TIME_A = "Newcastle"
        TIME_B = "PSV"

        # 1. BUSCA O TEMPO (MINUTO) - Foca na classe que aparece na sua foto
        tempo = "Início"
        try:
            tempo_el = driver.find_element(By.CSS_SELECTOR, ".GameStatus__Text, .status-detail")
            if tempo_el.text:
                tempo = tempo_el.text.strip()
        except:
            pass

        # 2. BUSCA OS GOLS (PLACAR REAL)
        # Na ESPN, os gols ficam em classes 'ScoreCell__Score' ou dentro de 'score-container'
        gols = ["0", "0"]
        try:
            # Busca especificamente pelos números do placar que aparecem na barra principal
            elementos_gols = driver.find_elements(By.CSS_SELECTOR, ".ScoreCell__Score")
            
            if len(elementos_gols) >= 2:
                # Extrai apenas os números (evita pegar nomes ou siglas)
                placar_real = [el.text.strip() for el in elementos_gols if el.text.strip().isdigit()]
                if len(placar_real) >= 2:
                    gols = placar_real[:2]
        except:
            # Backup caso a classe mude: procura por qualquer dígito isolado no cabeçalho
            pass

        gol_casa = gols[0]
        gol_fora = gols[1]

        resultado = f"{TIME_A} {gol_casa} X {gol_fora} {TIME_B} | {tempo}"

        # Grava o resultado real capturado
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            print(f"Sucesso: {resultado}")

    except Exception as e:
        print(f"Erro ao capturar: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_exato()
