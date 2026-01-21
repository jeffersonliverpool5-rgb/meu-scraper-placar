import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_ceramica_tempo_real():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Link do Ceramica Cleopatra FC
        driver.get("https://www.aiscore.com/team-ceramica-cleopatra-fc/ndkz6i99r6teq3z")
        time.sleep(45) 

        elementos = driver.find_elements(By.CLASS_NAME, "match-item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            achou_jogo = False
            for el in elementos:
                texto = el.text.strip()
                
                # SÓ PEGA SE TIVER O NOME DO TIME
                if "Ceramica" in texto:
                    # LIMPEZA INICIAL
                    limpo = texto.replace("Egypt Premier League", "").replace("\n", " ").strip()
                    limpo = re.sub(r'\d+\s+[a-zA-Z]+\s+\d{2}:\d{2}', '', limpo) # Tira data
                    
                    # LÓGICA DO TEMPO (AQUI ESTÁ O SEGREDO):
                    # Procura por um número seguido de ' OU o texto HT
                    if re.search(r"(\d+'|HT)", limpo):
                        f.write(f"JOGO ROLANDO: {limpo}\n")
                        print(f"Capturado ao vivo: {limpo}")
                        achou_jogo = True
                        break # Pega o primeiro que estiver ao vivo e para
            
            if not achou_jogo:
                f.write("O jogo ainda nao começou ou ja terminou (sem cronometro ativo no site).\n")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_ceramica_tempo_real()
