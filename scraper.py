import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_jogos_definitivo_limpo():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Acessando AiScore...")
        # Coloque aqui o link que você estiver usando no momento
        driver.get("https://www.aiscore.com/team-iraklis-1908-fc-u19/ndqmli055ncgkve")
        
        time.sleep(45) 

        # O XPATH que você confirmou que funciona sempre
        elementos = driver.find_elements(By.XPATH, "//div[contains(@class, 'match')] | //div[contains(@class, 'item')]")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not elementos:
                # Se não achar nada, ele avisa (segurança)
                f.write("Nenhum elemento encontrado na página.")
            else:
                for el in elementos:
                    txt = el.text.strip().replace("\n", " ")
                    
                    # >>> FILTRO DE JOGO AO VIVO <<<
                    # 1. Tem que ter o símbolo de minuto (') OU o texto HT (intervalo)
                    # 2. Tem que ter um placar (número - número)
                    if re.search(r"\d+'|HT", txt) and re.search(r"\d+\s*-\s*\d+", txt):
                        
                        # LIMPEZA DE LIXO (Tira nome de ligas e datas se sobrarem)
                        txt = txt.replace("Egypt Premier League", "").replace("Ethiopia Premier League", "")
                        txt = re.sub(r'\d+\s+[a-zA-Z]+\s+\d{2}:\d{2}', '', txt) # Tira datas
                        
                        # Remove espaços extras e salva
                        linha_final = " ".join(txt.split())
                        f.write(linha_final + "\n")
                        print(f"Jogo ao vivo capturado: {linha_final}")

        print("Processo finalizado!")

    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_jogos_definitivo_limpo()
