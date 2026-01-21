import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_jogo_reserves_ao_vivo():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # --- CONFIGURAÇÃO PARA O NOVO LINK ---
    TIME_ALVO = "FAS" 
    LINK = "https://www.aiscore.com/team-cd-fas-reserves/edq09ip2z4i4qxg"
    # -------------------------------------

    try:
        print(f"Acessando AiScore para buscar jogo AO VIVO de: {TIME_ALVO}...")
        driver.get(LINK)
        
        # Espera os 45 segundos que você validou para carregar tudo
        time.sleep(45) 

        # O seu XPATH que nunca falha para pegar todos os blocos
        elementos = driver.find_elements(By.XPATH, "//div[contains(@class, 'match')] | //div[contains(@class, 'item')]")
        
        linha_viva = ""

        for el in elementos:
            texto = el.text.strip().replace("\n", " ")
            
            # REGRA PARA O JOGO AO VIVO:
            # 1. Tem que ter "FAS" (o nome do seu time)
            # 2. Tem que ter o símbolo de minuto (') ou "HT" (1º tempo, intervalo ou 2º tempo)
            if TIME_ALVO in texto and (re.search(r"\d+'", texto) or "HT" in texto):
                linha_viva = texto
                break # Achou o jogo que está acontecendo AGORA, para de ler

        with open("placares.txt", "w", encoding="utf-8") as f:
            if linha_viva:
                # Limpa a linha de lixo (tira o nome da liga e datas)
                limpa = linha_viva.replace("El Salvador Reserva League", "")
                limpa = re.sub(r'\d+\s+[a-zA-Z]+\s+\d{2}:\d{2}', '', limpa)
                
                # Salva apenas a linha limpa com o jogo ao vivo
                resultado_final = " ".join(limpa.split())
                f.write(resultado_final + "\n")
                print(f"CAPTURADO AO VIVO: {resultado_final}")
            else:
                # Se não tiver cronômetro rodando, o arquivo avisa
                f.write(f"Nenhum jogo do {TIME_ALVO} Reserves ao vivo agora.\n")

    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_jogo_reserves_ao_vivo()
