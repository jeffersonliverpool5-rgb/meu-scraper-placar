import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_placares_simples():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Livescore.bz é um site bem básico, fácil de ler
        print("Acessando site de placares...")
        driver.get("https://www.livescore.com/pt/") 
        time.sleep(10) # Tempo para os placares carregarem

        # No livescore.bz, os jogos ficam em linhas de tabela (tr)
        jogos = driver.find_elements(By.CLASS_NAME, "row")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not jogos:
                # Tenta um seletor alternativo se o primeiro falhar
                jogos = driver.find_elements(By.TAG_NAME, "tr")
            
            for jogo in jogos:
                texto = jogo.text.strip().replace("\n", " ")
                # Filtra apenas linhas que parecem ter placares (ex: contêm ':')
                if ":" in texto and len(texto) > 10:
                    f.write(texto + "\n")
                    print(f"Encontrado: {texto}")
                    
        print("Arquivo placares.txt atualizado com sucesso.")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placares_simples()
