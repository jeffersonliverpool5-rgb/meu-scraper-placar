import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_google_scores():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Pesquisa no Google por placares ao vivo
        print("Buscando no Google...")
        driver.get("https://www.google.com/search?q=jogos+de+futebol+ao+vivo+agora")
        time.sleep(5) 

        # O Google organiza jogos em blocos. Vamos tentar pegar esses blocos de texto.
        # Procuramos por elementos que contenham dados de partidas
        partidas = driver.find_elements(By.XPATH, "//div[@data-ved] | //div[@role='button']")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            encontrou = False
            for p in partidas:
                texto = p.text.strip()
                # Filtro simples: só salva se tiver cara de placar (ex: contém ' x ' ou números)
                if ' x ' in texto or ('-' in texto and any(char.isdigit() for char in texto)):
                    if len(texto) > 10 and len(texto) < 200:
                        f.write(texto.replace('\n', ' | ') + "\n")
                        encontrou = True
            
            if not encontrou:
                f.write("Nenhum placar ao vivo encontrado no topo do Google no momento.")

        print("Arquivo placares.txt atualizado via Google.")
        
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_google_scores()
