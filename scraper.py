import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_jogo_perfeito():
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
        
        linhas = driver.find_element(By.TAG_NAME, "body").text.split('\n')
        
        # --- NOMES DOS TIMES ---
        TIME_A = "Galatasaray"
        TIME_B = "Atlético Madrid"
        # -----------------------

        gols = []
        tempo = ""

        # 1. Busca os dados no topo da página (onde o placar é real)
        for i, texto in enumerate(linhas[:60]):
            texto = texto.strip()
            # Pega o tempo
            if "'" in texto or "HT" in texto or "Fim" in texto or "Intervalo" in texto:
                if not tempo: tempo = texto
            # Pega números isolados (placar)
            elif re.match(r"^[0-9]$", texto):
                gols.append(texto)

        # 2. Monta a frase exatamente como você pediu
        # Se achou os gols, monta: Time 1 X 0 Time | Minuto
        if len(gols) >= 2:
            resultado_final = f"{TIME_A} {gols[0]} X {gols[1]} {TIME_B} | {tempo}"
        else:
            resultado_final = f"{TIME_A} 0 X 0 {TIME_B} | {tempo if tempo else '0'}'"

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado_final)
            print(f"Resultado: {resultado_final}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_perfeito()
