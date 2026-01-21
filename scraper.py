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
        # LINK DO JOGO NEWCASTLE X PSV (ID 757778)
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757778")
        
        # Espera forçada para o site carregar totalmente os números
        time.sleep(45) 

        # NOMES DOS TIMES
        TIME_A = "Newcastle"
        TIME_B = "PSV"

        # 1. BUSCA O TEMPO (MINUTO)
        tempo = "Início"
        try:
            # Tenta achar o elemento do minuto
            tempo_el = driver.find_element(By.CSS_SELECTOR, ".game-time, .status-detail, .Gamestrip__Time")
            if tempo_el.text:
                tempo = tempo_el.text.strip()
        except:
            # Se falhar, procura algo com ' no texto
            texto_bruto = driver.find_element(By.TAG_NAME, "body").text
            minutos = re.findall(r"\d+'|HT|Intervalo|Fim", texto_bruto)
            if minutos: tempo = minutos[0]

        # 2. BUSCA OS GOLS (PLACAR)
        # Vamos pegar especificamente os números que estão dentro do cabeçalho do jogo
        gols = ["0", "0"]
        try:
            # Pega os elementos com a classe 'score'
            scores = driver.find_elements(By.CLASS_NAME, "score")
            if len(scores) >= 2:
                gols = [s.text.strip() for s in scores if s.text.strip().isdigit()]
            
            # Se ainda não veio o placar, tenta pelo Gamestrip
            if len(gols) < 2:
                header = driver.find_element(By.CLASS_NAME, "Gamestrip")
                gols_header = re.findall(r"\b\d+\b", header.text)
                if len(gols_header) >= 2:
                    gols = gols_header[:2]
        except:
            pass

        # MONTAGEM FINAL
        # Se os gols vierem vazios por erro de carga, mantemos o 0 X 0 mas com os nomes certos
        gol_casa = gols[0] if len(gols) >= 1 else "0"
        gol_fora = gols[1] if len(gols) >= 2 else "0"

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
