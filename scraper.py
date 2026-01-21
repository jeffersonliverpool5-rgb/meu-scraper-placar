import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_partida_ao_vivo():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Link específico da partida que você enviou
        url = "https://www.espn.com.br/futebol/partida/_/jogoId/757771"
        driver.get(url)
        
        # Espera o carregamento dos elementos de placar
        time.sleep(20) 

        # Captura o container principal do placar
        # Na ESPN, as classes costumam ser 'Gamestrip' ou 'competitors'
        corpo = driver.find_element(By.TAG_NAME, "body").text
        
        # Vamos capturar as linhas que importam: Times, Placar e Tempo
        # Tentamos pegar elementos específicos primeiro para evitar lixo
        try:
            placar_container = driver.find_element(By.CLASS_NAME, "Gamestrip").text
            resultado = placar_container.replace("\n", " ")
        except:
            # Fallback caso a classe mude: pega o topo da página
            resultado = corpo.split("\n")[0:20] # Pega as primeiras 20 linhas de texto
            resultado = " ".join(resultado)

        with open("placares.txt", "w", encoding="utf-8") as f:
            # Filtro para garantir que estamos pegando a linha do jogo
            # Procura por números de placar ou indicadores de tempo (', HT, Final)
            if re.search(r"\d+ - \d+|'|HT|Fim|vencendo", resultado):
                f.write(resultado)
            else:
                f.write("Aguardando início da partida ou dados ao vivo...")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_partida_ao_vivo()
