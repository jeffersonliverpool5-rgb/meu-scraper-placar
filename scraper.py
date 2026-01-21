import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_jogo_ao_vivo_certeiro():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # --- CONFIGURAÇÃO ---
    TIME_ALVO = "Ceramica" 
    LINK = "https://www.aiscore.com/team-ceramica-cleopatra-fc/ndkz6i99r6teq3z"
    # --------------------

    try:
        print(f"Buscando jogo AO VIVO: {TIME_ALVO}")
        driver.get(LINK)
        time.sleep(45) 

        # Usa o XPATH que você validou que pega tudo
        elementos = driver.find_elements(By.XPATH, "//div[contains(@class, 'match')] | //div[contains(@class, 'item')]")
        
        linha_viva = ""

        for el in elementos:
            texto = el.text.strip().replace("\n", " ")
            
            # FILTRO: Nome do time + (Minutagem ou HT)
            # Isso garante que pegue 1º tempo, 2º tempo e intervalo
            if TIME_ALVO in texto and (re.search(r"\d+'", texto) or "HT" in texto):
                linha_viva = texto
                break 

        with open("placares.txt", "w", encoding="utf-8") as f:
            if linha_viva:
                # Limpa a linha tirando o excesso de espaços
                resultado = " ".join(linha_viva.split())
                f.write(resultado + "\n")
                print(f"CAPTURADO: {resultado}")
            else:
                f.write(f"Aguardando o inicio do jogo ou intervalo do {TIME_ALVO}...\n")

        print("Finalizado.")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_jogo_ao_vivo_certeiro()
