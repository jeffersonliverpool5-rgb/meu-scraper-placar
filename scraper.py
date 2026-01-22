import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair_aiscore():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://www.aiscore.com/match-argentinos-juniors-ferrocarril-midland/34kgmio142waeko"
        driver.get(url)
        
        # Espera o carregamento dos elementos dinâmicos
        time.sleep(20)

        # 1. Nomes dos Times (Seletores estáveis)
        try:
            time_casa = driver.find_element(By.CSS_SELECTOR, ".home-team .name").text.strip()
            time_fora = driver.find_element(By.CSS_SELECTOR, ".away-team .name").text.strip()
        except:
            time_casa, time_fora = "Argentinos Jrs", "Midland"

        # 2. Placar
        try:
            g1 = driver.find_element(By.CLASS_NAME, "home-score").text.strip()
            g2 = driver.find_element(By.CLASS_NAME, "away-score").text.strip()
        except:
            g1, g2 = "0", "0"

        # 3. BUSCA DO TEMPO (Ajustada)
        tempo_jg = "Ao Vivo"
        try:
            # Tenta pegar o container que envolve o tempo e o status
            bloco_tempo = driver.find_element(By.CLASS_NAME, "score-status").text
            
            # Limpa o texto (remove quebras de linha e espaços extras)
            linhas = [lin.strip() for lin in bloco_tempo.split('\n') if lin.strip()]
            
            # Geralmente o tempo é a linha que tem o minuto (ex: 40') ou "HT" ou "Half-time"
            # Vamos tentar pegar o que for mais relevante
            if len(linhas) > 0:
                # Se a primeira linha for o placar (ex: 1 - 0), tentamos a segunda
                if "-" in linhas[0] and len(linhas) > 1:
                    tempo_jg = linhas[1]
                else:
                    tempo_jg = linhas[0]
        except:
            tempo_jg = "Andamento"

        # Se o tempo vier como "Half-time", vamos abreviar para ficar bonito
        status_map = {
            "Half-time": "Intervalo",
            "Finished": "Fim",
            "Ended": "Fim",
            "Waiting": "Aguardando"
        }
        tempo_jg = status_map.get(tempo_jg, tempo_jg)

        # Montagem Final
        resultado = f"{time_casa} {g1} X {g2} {time_fora} | {tempo_jg}"
        resultado = " ".join(resultado.split()) # Remove espaços duplos

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"CAPTURA FINAL: {resultado}")

    except Exception as e:
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(f"Erro na captura")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_aiscore()
