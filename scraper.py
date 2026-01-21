import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def buscar_placar_real():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757771")
        
        # ESPERA ATÉ 40 SEGUNDOS para o placar ou tempo aparecer
        wait = WebDriverWait(driver, 40)
        
        # Tenta localizar o bloco principal do placar
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Gamestrip")))
        
        # Dá um tempinho extra para os números carregarem dentro do bloco
        time.sleep(10)

        # PEGA O TEXTO DO BLOCO DO PLACAR
        bloco_placar = driver.find_element(By.CLASS_NAME, "Gamestrip").text
        linhas = bloco_placar.split('\n')

        # --- FILTRAGEM ---
        gols = []
        tempo = "Ao Vivo"
        
        for item in linhas:
            item = item.strip()
            # Procura o tempo (ex: 85', HT, Fim)
            if "'" in item or "HT" in item or "Fim" in item or "Intervalo" in item:
                tempo = item
            # Procura os gols (apenas números de 0 a 20)
            elif item.isdigit() and len(item) <= 2:
                gols.append(item)

        # Se não achou gols no bloco, tenta no body inteiro como última chance
        if len(gols) < 2:
            texto_total = driver.find_element(By.TAG_NAME, "body").text
            gols = re.findall(r"\b\d\b", texto_total)[:2]

        TIME_A = "Galatasaray"
        TIME_B = "Atlético Madrid"

        # Garante que temos dois números para o placar
        gol_casa = gols[0] if len(gols) >= 1 else "0"
        gol_fora = gols[1] if len(gols) >= 2 else "0"

        resultado = f"{TIME_A} {gol_casa} X {gol_fora} {TIME_B} | {tempo}"

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            print(f"Capturado com sucesso: {resultado}")

    except Exception as e:
        print(f"Erro no carregamento: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_real()
