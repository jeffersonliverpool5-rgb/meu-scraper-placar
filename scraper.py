import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_placar_real():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # LINK DO JOGO
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757771")
        time.sleep(35)
        
        # --- CONFIGURAÇÃO ---
        TIME_A = "Galatasaray"
        TIME_B = "Atlético Madrid"
        # --------------------

        # 1. PEGA O TEMPO (Minuto)
        try:
            tempo_el = driver.find_element(By.CLASS_NAME, "game-time") or \
                       driver.find_element(By.CLASS_NAME, "status-detail")
            tempo = tempo_el.text.strip()
        except:
            # Fallback se não achar a classe: busca no texto bruto
            texto_todo = driver.find_element(By.TAG_NAME, "body").text
            minuto = re.findall(r"\d+'|HT|Intervalo|Fim", texto_todo)
            tempo = minuto[0] if minuto else "Ao Vivo"

        # 2. PEGA OS GOLS (Procura especificamente pelos números do placar)
        # Na ESPN as classes de gols costumam ser 'score' ou 'score-container'
        try:
            gols_elementos = driver.find_elements(By.CLASS_NAME, "score")
            placar = [g.text.strip() for g in gols_elementos if g.text.strip().isdigit()]
        except:
            placar = []

        # 3. SE NÃO ACHOU POR CLASSE, PEGA PELO TEXTO AO REDOR DO NOME
        if len(placar) < 2:
            linhas = driver.find_element(By.TAG_NAME, "body").text.split('\n')[:60]
            placar = []
            for l in linhas:
                if l.strip().isdigit() and len(l.strip()) <= 2:
                    placar.append(l.strip())

        # 4. MONTAGEM FINAL (Garante o formato 1 X 1)
        gol_casa = placar[0] if len(placar) >= 1 else "0"
        gol_fora = placar[1] if len(placar) >= 2 else "0"
        
        resultado = f"{TIME_A} {gol_casa} X {gol_fora} {TIME_B} | {tempo}"

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            print(f"Sucesso: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_real()
