import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_organizado_certeiro():
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
        
        # 1. PEGA OS NOMES DOS CLUBES PELAS CLASSES DA ESPN
        # A ESPN usa 'short-name' ou 'long-name' para os times no placar
        times_elementos = driver.find_elements(By.CLASS_NAME, "Table__Team") or \
                          driver.find_elements(By.CLASS_NAME, "long-name") or \
                          driver.find_elements(By.CLASS_NAME, "short-name")
        
        times = [t.text.strip() for t in times_elementos if t.text.strip() and len(t.text) > 2]
        # Limpa nomes repetidos e pega os dois primeiros
        times = list(dict.fromkeys(times))[:2]

        # 2. PEGA O PLACAR E O TEMPO PELO TEXTO BRUTO (REDE DE ARRASTÃO)
        texto = driver.find_element(By.TAG_NAME, "body").text.split('\n')[:60]
        placar = []
        tempo = ""

        for linha in texto:
            linha = linha.strip()
            # Identifica o tempo (Ex: 45', HT, Intervalo, Fim)
            if "'" in linha or "HT" in linha or "Intervalo" in linha or "Fim" in linha or "FIM" in linha:
                if not tempo: # Pega o primeiro que aparecer
                    tempo = linha
            # Identifica o placar (Números isolados de 0 a 9)
            elif re.match(r"^[0-9]$", linha):
                if len(placar) < 2:
                    placar.append(linha)

        # MONTA A LINHA FINAL
        if len(times) >= 2 and len(placar) >= 2:
            linha_final = f"{times[0]} {placar[0]} - {placar[1]} {times[1]} | {tempo}"
        elif len(times) >= 2:
            linha_final = f"{times[0]} vs {times[1]} | {tempo}"
        else:
            # Fallback caso os nomes falhem: pega as primeiras linhas úteis
            linha_final = " ".join(texto[:5])

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(linha_final)
            print(f"Resultado: {linha_final}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_organizado_certeiro()
