import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_jogos_centrais():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Acessando AiScore...")
        driver.get("https://www.aiscore.com/")
        
        # Tempo para carregar a lista central (ZED FC, etc)
        time.sleep(30) 

        # Busca os blocos de jogos centrais
        jogos = driver.find_elements(By.CLASS_NAME, "match-item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not jogos:
                f.write("Nenhum jogo encontrado na área central.")
            else:
                for jogo in jogos:
                    try:
                        texto = jogo.text.strip()
                        if len(texto) > 10:
                            # Organiza o texto em uma linha só
                            linha = texto.replace("\n", " | ")
                            f.write(linha + "\n")
                    except:
                        continue
        print("Sucesso! Arquivo placares.txt atualizado.")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_jogos_centrais()
