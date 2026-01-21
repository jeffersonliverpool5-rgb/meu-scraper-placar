import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_organizado():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # COLOQUE O LINK DO JOGO AQUI
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757771")
        time.sleep(30)
        
        # Pega o topo da página onde estão os dados principais
        texto = driver.find_element(By.TAG_NAME, "body").text.split('\n')[:50]
        
        times = []
        placar = []
        tempo = ""

        for linha in texto:
            linha = linha.strip()
            # 1. Identifica o tempo (Ex: 45', HT, Fim)
            if "'" in linha or "HT" in linha or "Fim" in linha or "FIM" in linha:
                tempo = linha
            # 2. Identifica o placar (Números isolados de 0 a 9)
            elif re.match(r"^[0-9]$", linha):
                placar.append(linha)
            # 3. Identifica os nomes dos times (Ignora lixo como 'PTS', 'Estatísticas', etc)
            elif len(linha) > 2 and not any(x in linha for x in ["PTS", "Estatísticas", "ATA", "ATH", "Vídeo"]):
                if len(times) < 2: # Pega apenas os dois primeiros nomes que sobrarem
                    times.append(linha)

        # MONTA A LINHA ÚNICA
        if len(times) >= 2 and len(placar) >= 2:
            linha_final = f"{times[0]} {placar[0]} - {placar[1]} {times[1]} | {tempo}"
        elif len(times) >= 2:
            linha_final = f"{times[0]} vs {times[1]} | {tempo}"
        else:
            linha_final = "Aguardando dados da partida..."

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(linha_final)
            print(f"Linha Organizada: {linha_final}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_organizado()
