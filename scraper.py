import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_placar():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # URL exata do jogo São Paulo x Portuguesa
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/762098")
        
        # Espera o carregamento (reduzido para 15s para ser mais ágil no GitHub)
        time.sleep(15)

        # 1. BUSCAR O TEMPO REAL (Priorizando o relógio do topo)
        tempo = "Início"
        try:
            # Tenta o seletor do cronômetro principal que aparece no placar do topo
            # Esse seletor ".GameState__Time" é o mais comum para o tempo corrido
            el_tempo = driver.find_element(By.CSS_SELECTOR, ".GameStatus__Text, .GameState__Time, .ScoreCell__Time--active")
            if el_tempo.text:
                tempo = el_tempo.text.strip()
        except:
            # Se falhar, procura por qualquer texto que tenha o símbolo de minutos (') no topo da página
            try:
                header = driver.find_element(By.ID, "gamepackage-header-wrap")
                match = re.search(r"\d+'(\+\d+)?'|HT|Intervalo|Fim", header.text)
                if match:
                    tempo = match.group()
            except:
                pass

        # 2. BUSCAR GOLS
        gols = ["0", "0"]
        try:
            # Seleciona apenas os scores que estão dentro do cabeçalho principal
            scores = driver.find_elements(By.CSS_SELECTOR, ".ScoreCell__Score")
            if len(scores) >= 2:
                gols = [s.text.strip() for s in scores[:2]]
        except:
            pass

        # 3. NOMES DOS TIMES
        time_a, time_b = "São Paulo", "Portuguesa"

        # MONTAGEM FINAL
        resultado = f"{time_a} {gols[0]} X {gols[1]} {time_b} | {tempo}"
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"Capturado: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar()
