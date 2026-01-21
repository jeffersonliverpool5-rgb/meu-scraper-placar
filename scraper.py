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
        
        # Tempo de espera para garantir que o JavaScript carregue os números
        time.sleep(25)

        # 1. BUSCAR O TEMPO REAL (Ex: 3', HT, Fim)
        tempo = "0'"
        # Lista de possíveis classes que a ESPN usa para o relógio
        seletores_tempo = [".game-time", ".status-detail", ".GameStatus__Text", ".ScoreCell__Time"]
        
        for seletor in seletores_tempo:
            try:
                el = driver.find_element(By.CSS_SELECTOR, seletor)
                if el.text:
                    tempo = el.text.strip()
                    break
            except:
                continue

        # 2. BUSCAR GOLS
        gols = ["0", "0"]
        try:
            # Pega os números grandes do placar
            scores = driver.find_elements(By.CSS_SELECTOR, ".ScoreCell__Score, .detailScore__wrapper > span")
            temp_gols = [s.text.strip() for s in scores if s.text.strip().isdigit()]
            if len(temp_gols) >= 2:
                gols = temp_gols[:2]
        except:
            pass

        # 3. NOMES DOS TIMES
        try:
            # Tenta pegar os nomes dos times para confirmar
            time_a = driver.find_elements(By.CSS_SELECTOR, ".format--long")[0].text
            time_b = driver.find_elements(By.CSS_SELECTOR, ".format--long")[1].text
        except:
            time_a, time_b = "São Paulo", "Portuguesa"

        # MONTAGEM FINAL
        resultado = f"{time_a} {gols[0]} X {gols[1]} {time_b} | {tempo}"
        
        # Salva o resultado no arquivo
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"Atualizado: {resultado}")

    except Exception as e:
        print(f"Erro no scraping: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar()
