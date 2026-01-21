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
        # URL do jogo São Paulo x Portuguesa
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/762098")
        
        # Espera o carregamento dos dados dinâmicos
        time.sleep(20)

        # 1. BUSCAR O TEMPO REAL (Focado no container do placar)
        tempo = "0'"
        try:
            # Procuramos o tempo especificamente dentro do cabeçalho do jogo
            # O seletor abaixo busca o status que fica entre os scores
            status_container = driver.find_element(By.CSS_SELECTOR, ".GameStrip__FullStatus, .status-detail, .ScoreCell__Time")
            texto_tempo = status_container.text.strip()
            
            # Se encontrar algo como "3'", "45+2'", "Intervalo" ou "Fim"
            if texto_tempo:
                tempo = texto_tempo
        except:
            # Fallback: tenta buscar qualquer número com ' que não seja 45' fixo se houver erro
            elementos = driver.find_elements(By.XPATH, "//*[contains(text(), \"'\")]")
            for el in elementos:
                if len(el.text) <= 5: # Filtra para pegar apenas strings curtas como 12'
                    tempo = el.text.strip()
                    break

        # 2. BUSCAR GOLS (Focado nos números grandes)
        gols = ["0", "0"]
        try:
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
            
        print(f"Resultado Capturado: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar()
