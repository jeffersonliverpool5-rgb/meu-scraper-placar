import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair_bruto_ge():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Acessa o link do jogo
        driver.get("https://ge.globo.com/sp/futebol/campeonato-paulista/jogo/21-01-2026/sao-paulo-portuguesa.ghtml")
        
        # Espera generosa para o site carregar tudo
        time.sleep(30)

        # CAPTURA TODO O TEXTO DA PÁGINA
        conteudo_total = driver.find_element(By.TAG_NAME, "body").text
        
        # FILTRAGEM DOS DADOS (Busca por padrões no texto bruto)
        
        # 1. Busca o Tempo (Ex: 28:23 1T)
        busca_tempo = re.search(r"(\d{1,2}:\d{2}\s[12]T|Intervalo|Fim de jogo|Encerrado)", conteudo_total)
        tempo = busca_tempo.group(0) if busca_tempo else "Tempo não detectado"

        # 2. Busca o Placar (Gols)
        # No GE, os gols aparecem isolados no topo. Vamos tentar capturar os elementos do placar primeiro
        try:
            gols = driver.find_elements(By.CLASS_NAME, "placar-jogo__equipe--placar")
            gol_casa = gols[0].text.strip()
            gol_fora = gols[1].text.strip()
        except:
            # Se falhar, tenta achar números isolados perto dos nomes dos times
            gol_casa = "0"
            gol_fora = "0"

        # MONTAGEM DA LINHA BRUTA
        resultado = f"SAO {gol_casa} X {gol_fora} POR | {tempo}"
        
        # Salva no arquivo para o GitHub
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"Extração Concluída: {resultado}")

    except Exception as e:
        print(f"Erro na extração: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_bruto_ge()
