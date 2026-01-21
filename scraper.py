import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_dados_ge():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Link direto da sua foto
        driver.get("https://ge.globo.com/sp/futebol/campeonato-paulista/jogo/21-01-2026/sao-paulo-portuguesa.ghtml")
        
        # Espera carregar os scripts do placar
        time.sleep(15)

        # CAPTURA DOS GOLS (Baseado na área azul da foto)
        # O GE usa spans para os números do placar
        gols = driver.find_elements(By.CLASS_NAME, "placar-jogo__equipe--placar")
        gol_casa = gols[0].text.strip() if len(gols) > 0 else "0"
        gol_fora = gols[1].text.strip() if len(gols) > 1 else "0"

        # CAPTURA DO TEMPO (Ex: 28:23 1T)
        # Na foto, fica logo abaixo dos números 0-0
        try:
            tempo_el = driver.find_element(By.CLASS_NAME, "placar-jogo__periodo")
            tempo = tempo_el.text.replace("\n", " ").strip()
        except:
            tempo = "Tempo indisponível"

        # NOMES DOS TIMES
        try:
            nomes = driver.find_elements(By.CLASS_NAME, "placar-jogo__equipe--nome")
            time_a = nomes[0].text.strip()
            time_b = nomes[1].text.strip()
        except:
            time_a, time_b = "SAO", "POR"

        # RESULTADO FINAL PARA O GITHUB
        resultado = f"{time_a} {gol_casa} X {gol_fora} {time_b} | {tempo}"
        
        # Salva apenas a linha com os dados brutos
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"Dados extraídos: {resultado}")

    except Exception as e:
        print(f"Erro ao capturar dados: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_dados_ge()
