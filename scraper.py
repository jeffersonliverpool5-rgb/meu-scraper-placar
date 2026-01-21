import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_placar_limpo():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Acessando página do time...")
        driver.get("https://www.aiscore.com/team-shire-endaselassie-fc/34kgmino3lh8ko9")
        
        # Tempo para carregar os dados dinâmicos
        time.sleep(30) 

        # No link do time, os jogos ficam geralmente em elementos com a classe 'match-item'
        # Vamos ser mais específicos para evitar os menus laterais
        jogos = driver.find_elements(By.CSS_SELECTOR, "div.match-item, a.match-item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not jogos:
                f.write("Jogo não encontrado ou ainda não carregou.")
            else:
                for jogo in jogos:
                    txt = jogo.text.strip().replace("\n", " ")
                    
                    # FILTRO DE LIMPEZA:
                    # Só salva se contiver o nome do time (ou parte dele) e um traço de placar
                    if "Shire" in txt and "-" in txt:
                        # Remove palavras indesejadas que costumam aparecer
                        txt_limpo = txt.replace("Live", "").replace("Schedule", "").strip()
                        f.write(txt_limpo + "\n")
                        print(f"Capturado com sucesso: {txt_limpo}")

        print("Arquivo placares.txt atualizado com o filtro!")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_limpo()
