import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def buscar_placar_newcastle():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # LINK DO JOGO NEWCASTLE X PSV
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757778")
        
        # Espera o bloco principal carregar
        wait = WebDriverWait(driver, 45)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Gamestrip")))
        time.sleep(10) # Tempo para os números "sentarem" na tela

        # Pega apenas o texto do placar para não confundir com o resto da página
        bloco = driver.find_element(By.CLASS_NAME, "Gamestrip").text
        linhas = bloco.split('\n')

        # Configuração dos Times
        TIME_A = "Newcastle"
        TIME_B = "PSV"
        
        gols = []
        tempo = "Ao Vivo"

        for item in linhas:
            item = item.strip()
            # 1. Identifica o Tempo (ex: 22', HT, Fim)
            if "'" in item or "HT" in item or "Intervalo" in item or "Fim" in item:
                tempo = item
            # 2. Identifica os Gols (números isolados)
            elif item.isdigit() and len(item) <= 2:
                gols.append(item)

        # Se o placar falhar no bloco, tenta uma busca rápida no body
        if len(gols) < 2:
            scores = driver.find_elements(By.CLASS_NAME, "score")
            gols = [s.text.strip() for s in scores if s.text.strip().isdigit()]

        # Garante o formato 0 X 0 se ainda não houver gols
        gol_casa = gols[0] if len(gols) >= 1 else "0"
        gol_fora = gols[1] if len(gols) >= 2 else "0"

        resultado = f"⚪ {TIME_A} {gol_casa} X {gol_fora} {TIME_B} 🔴 | {tempo}"

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            print(f"Resultado salvo: {resultado}")

    except Exception as e:
        print(f"Erro ao capturar: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_newcastle()
