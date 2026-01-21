import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_apenas_o_jogo():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Link específico do seu time
        driver.get("https://www.aiscore.com/team-shire-endaselassie-fc/34kgmino3lh8ko9")
        
        # Tempo de espera para o placar ao vivo carregar
        time.sleep(45) 

        # Pega todos os elementos que podem conter o texto do jogo
        elementos = driver.find_elements(By.XPATH, "//*[contains(text(), 'Shire')]")
        
        jogos_encontrados = []

        for el in elementos:
            txt = el.text.strip().replace("\n", " ")
            
            # FILTRO MESTRE: 
            # 1. Tem que ter "Shire"
            # 2. Tem que ter um número, um traço e outro número (placar: 0 - 0)
            if "Shire" in txt and re.search(r'\d+\s*-\s*\d+', txt):
                # Limpa palavras de menu que costumam vir grudadas
                txt_limpo = txt.replace("Live", "").replace("Schedule", "").replace("Finished", "").strip()
                if txt_limpo not in jogos_encontrados:
                    jogos_encontrados.append(txt_limpo)

        with open("placares.txt", "w", encoding="utf-8") as f:
            if jogos_encontrados:
                for j in jogos_encontrados:
                    f.write(j + "\n")
                    print(f"Jogo salvo: {j}")
            else:
                f.write("Nenhum placar ao vivo encontrado para este time no momento.")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_apenas_o_jogo()
