import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_limpo():
    url = "https://www.aiscore.com/match-ca-penarol-boston-river/ndqmliw2oxehrkv"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        # Tempo de espera para o JavaScript injetar o minuto do jogo
        time.sleep(30) 
        
        # 1. Capturar Nomes dos Times
        try:
            nome_casa = driver.find_element(By.CSS_SELECTOR, ".home-team-name, .home-name, .home-team .name").text.strip()
            nome_fora = driver.find_element(By.CSS_SELECTOR, ".away-team-name, .away-name, .away-team .name").text.strip()
        except:
            nome_casa = "BSRC"
            nome_fora = "Indera FC"

        # 2. Capturar o Tempo (Cronômetro) - Busca Exaustiva
        cronometro = ""
        try:
            elementos_tempo = driver.find_elements(By.XPATH, "//*[contains(text(), \"'\")]")
            for el in elementos_tempo:
                texto = el.text.strip()
                if "'" in texto and len(texto) <= 5: # Filtra para pegar algo como 45' ou 90+2'
                    cronometro = texto
                    break
            
            if not cronometro:
                cronometro = driver.find_element(By.CSS_SELECTOR, ".match-status, .status-info").text.strip()
        except:
            cronometro = "Ao vivo"

        # 3. Capturar Placares
        try:
            placar_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            placar_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            placar_casa = "0"
            placar_fora = "0"

        # Formatação solicitada
        resultado = f"[{cronometro}] {nome_casa} {placar_casa} x {placar_fora} {nome_fora}"
        print(f"Salvando: {resultado}")

        # Salva no arquivo 'placares.txt' limpando o anterior
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

# --- ABAIXO A MODIFICAÇÃO PARA REPETIR 100X ---
if __name__ == "__main__":
    for i in range(1, 101):  # Vai de 1 até 100
        print(f"\n>>> Iniciando atualização {i} de 100")
        extrair_placar_limpo()
        
        if i < 100:  # Se não for a última vez, espera 60 segundos
            print("Aguardando 60 segundos para a próxima atualização...")
            time.sleep(60)
            
    print("Fim das 100 atualizações.")
