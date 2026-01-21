import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_jogos_limpos():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Acessando AiScore...")
        # Usando o link do time que você quer monitorar
        driver.get("https://www.aiscore.com/team-ceramica-cleopatra-fc/ndkz6i99r6teq3z")
        
        time.sleep(45) 

        # Usa o XPATH que você confirmou que funciona
        elementos = driver.find_elements(By.XPATH, "//div[contains(@class, 'match')] | //div[contains(@class, 'item')]")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not elementos:
                # Se falhar, pega o texto bruto como segurança
                texto_pagina = driver.find_element(By.TAG_NAME, "body").text
                f.write("--- MODO SEGURANÇA (TEXTO BRUTO) ---\n")
                f.write(texto_pagina)
            else:
                for el in elementos:
                    txt = el.text.strip().replace("\n", " ")
                    
                    # FILTRO DE LIMPEZA (O QUE FICA NO ARQUIVO):
                    # 1. Tem que ter o traço do placar ou "vs"
                    # 2. Tem que ter o nome do time
                    if "-" in txt or "vs" in txt:
                        if "Ceramica" in txt:
                            # Tira nomes de ligas comuns e datas (número + mês + hora)
                            txt_limpo = txt.replace("Egypt Premier League", "")
                            txt_limpo = txt_limpo.replace("Ethiopia Premier League", "")
                            
                            # Remove as datas (Ex: 21 Jan 14:00) usando Regex
                            txt_limpo = re.sub(r'\d+\s+[a-zA-Z]+\s+\d{2}:\d{2}', '', txt_limpo)
                            
                            # Remove espaços duplos que sobraram
                            txt_limpo = " ".join(txt_limpo.split())
                            
                            if len(txt_limpo) > 10:
                                f.write(txt_limpo + "\n")

        print("Processo finalizado com sucesso!")

    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_jogos_limpos()
