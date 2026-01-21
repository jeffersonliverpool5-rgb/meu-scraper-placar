import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_placar_infalivel():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # LINK DO JOGO
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757771")
        time.sleep(35) # Espera generosa para carregar tudo
        
        # --- 1. BUSCA O TEMPO (MINUTOS) ---
        # Tenta todas as variações de nomes que a ESPN usa
        tempo = ""
        seletores_tempo = [
            ".game-time", ".status-detail", ".time", 
            ".Gamestrip__Time", ".Gamestrip__Status"
        ]
        for seletor in seletores_tempo:
            try:
                el = driver.find_element(By.CSS_SELECTOR, seletor)
                if el.text.strip():
                    tempo = el.text.strip()
                    break
            except:
                continue
        
        # Se falhou nos seletores, tenta achar um número com ' no texto bruto
        if not tempo:
            texto_bruto = driver.find_element(By.TAG_NAME, "body").text
            busca_minuto = re.findall(r"\d+'|HT|Intervalo|Fim", texto_todo)
            tempo = busca_minuto[0] if busca_minuto else "Ao Vivo"

        # --- 2. BUSCA O PLACAR (GOLS) ---
        gol_casa, gol_fora = "0", "0"
        # Tenta buscar pelas classes de score
        try:
            # Seletores comuns de placar na ESPN
            scores = driver.find_elements(By.CSS_SELECTOR, ".score, .Gamestrip__Score, .score-container")
            if len(scores) >= 2:
                gol_casa = scores[0].text.strip()
                gol_fora = scores[1].text.strip()
            else:
                # Se falhou, tenta buscar números grandes dentro do cabeçalho
                header = driver.find_element(By.CLASS_NAME, "Gamestrip")
                numeros = re.findall(r"\b\d\b", header.text)
                if len(numeros) >= 2:
                    gol_casa, gol_fora = numeros[0], numeros[1]
        except:
            pass

        # --- NOMES DOS TIMES ---
        TIME_A = "Galatasaray"
        TIME_B = "Atlético Madrid"

        resultado = f"{TIME_A} {gol_casa} X {gol_fora} {TIME_B} | {tempo}"

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            print(f"Resultado: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_infalivel()
