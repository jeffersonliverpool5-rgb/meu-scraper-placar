import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_apenas_jogo_ao_vivo():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Link do time Shire Endaselassie FC
        driver.get("https://www.aiscore.com/team-shire-endaselassie-fc/34kgmino3lh8ko9")
        time.sleep(45) 

        # Procura os elementos de jogo
        elementos = driver.find_elements(By.CLASS_NAME, "match-item")
        
        jogo_ao_vivo = ""

        for el in elementos:
            texto = el.text.strip()
            
            # REGRA PARA JOGO AO VIVO:
            # 1. Tem que ter o nome do time
            # 2. Tem que ter um indicador de tempo real (minutos como 70', 85' ou HT para intervalo)
            # 3. Ignora se tiver datas (Jan, Feb) para não pegar jogos passados
            if "Shire" in texto:
                # Procura por números seguidos de ' (ex: 85') ou o termo HT
                if re.search(r"\d+'|HT", texto):
                    # Limpeza: remove nomes de ligas e lixo lateral
                    limpo = texto.replace("Ethiopia Premier League", "").replace("\n", " ").strip()
                    # Remove a data se ela vier grudada
                    limpo = re.sub(r'\d+\s+[a-zA-Z]+\s+\d{2}:\d{2}', '', limpo)
                    jogo_ao_vivo = " ".join(limpo.split())
                    break # Para na primeira ocorrência (o jogo atual)

        with open("placares.txt", "w", encoding="utf-8") as f:
            if jogo_ao_vivo:
                f.write(f"AO VIVO AGORA: {jogo_ao_vivo}\n")
                print(f"Capturado: {jogo_ao_vivo}")
            else:
                f.write("Não há nenhum jogo do Shire Endaselassie FC a acontecer agora.\n")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_apenas_jogo_ao_vivo()
