import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def pegar_dados_agora():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://www.aiscore.com/match-instituto-de-cordoba-velez-sarsfield/vrqwni43wdgu4qn"
        driver.get(url)
        
        # Espera forçada de 10 segundos para o JavaScript carregar os números
        time.sleep(10)

        # Seletores simplificados que funcionam no Live
        try:
            # Pega os nomes usando uma busca de texto parcial
            home_name = driver.find_element(By.CSS_SELECTOR, ".home-team .name").text.strip()
            away_name = driver.find_element(By.CSS_SELECTOR, ".away-team .name").text.strip()
            
            # Pega os scores (tenta as duas classes possíveis do AiScore)
            try:
                h_score = driver.find_element(By.CLASS_NAME, "home-score").text.strip()
                a_score = driver.find_element(By.CLASS_NAME, "away-score").text.strip()
            except:
                h_score = driver.find_element(By.CLASS_NAME, "score-home").text.strip()
                a_score = driver.find_element(By.CLASS_NAME, "score-away").text.strip()

            resultado = f"{home_name} {h_score} X {a_score} {away_name}"
            
            # FORÇA A GRAVAÇÃO DO ARQUIVO (Modo 'w' sobrescreve o antigo)
            with open("placares.txt", "w", encoding="utf-8") as f:
                f.write(resultado)
                f.flush() # Garante que o Windows escreva no disco agora
                os.fsync(f.fileno()) 
            
            print(f"ARQUIVO ATUALIZADO: {resultado}")

        except Exception as e:
            print(f"Erro ao localizar elementos: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        print("\n--- Iniciando nova captura ---")
        pegar_dados_agora()
        print("Aguardando 30 segundos para a próxima...")
        time.sleep(30)
