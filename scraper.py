import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_placar_ge():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # LINK DO GE ENVIADO
        driver.get("https://ge.globo.com/sp/futebol/campeonato-paulista/jogo/21-01-2026/sao-paulo-portuguesa.ghtml")
        
        # O GE carrega rápido, 15s é suficiente
        time.sleep(15)

        # 1. BUSCAR GOLS
        # No GE os gols ficam em classes 'placar-jogo__equipe--placar'
        gols_elementos = driver.find_elements(By.CLASS_NAME, "placar-jogo__equipe--placar")
        gol_casa = gols_elementos[0].text.strip() if len(gols_elementos) > 0 else "0"
        gol_fora = gols_elementos[1].text.strip() if len(gols_elementos) > 1 else "0"

        # 2. BUSCAR O TEMPO REAL
        tempo = "Pré-jogo"
        try:
            # O GE usa a classe 'placar-jogo__periodo' para o tempo (ex: 3' 1T, Intervalo, Fim de jogo)
            tempo_el = driver.find_element(By.CLASS_NAME, "placar-jogo__periodo")
            if tempo_el.text:
                tempo = tempo_el.text.replace("\n", " ").strip()
        except:
            pass

        # 3. NOMES DOS TIMES
        # No GE: placar-jogo__equipe--nome
        try:
            nomes = driver.find_elements(By.CLASS_NAME, "placar-jogo__equipe--nome")
            time_a = nomes[0].text.strip()
            time_b = nomes[1].text.strip()
        except:
            time_a, time_b = "São Paulo", "Portuguesa"

        # MONTAGEM FINAL
        resultado = f"{time_a} {gol_casa} X {gol_fora} {time_b} | {tempo}"
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"GE Capturado: {resultado}")

    except Exception as e:
        print(f"Erro no GE: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_ge()
