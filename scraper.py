import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_detalhes_partida():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://www.aiscore.com/match-zed-fc-al-masry/ndkz6i3n5yjcxq3"
        driver.get(url)
        
        # Aumentamos o tempo para garantir que o cronômetro e o score carreguem
        time.sleep(45) 

        with open("placares.txt", "w", encoding="utf-8") as f:
            try:
                # Tenta capturar o placar (geralmente em classes como 'score' ou dentro do header)
                # No AiScore, o placar ao vivo costuma ficar em elementos com a classe 'home-score' e 'away-score'
                casa = driver.find_element(By.CLASS_NAME, "home-name").text
                fora = driver.find_element(By.CLASS_NAME, "away-name").text
                
                # Busca o placar e o minuto
                score_casa = driver.find_element(By.CLASS_NAME, "home-score").text
                score_fora = driver.find_element(By.CLASS_NAME, "away-score").text
                minuto = driver.find_element(By.CLASS_NAME, "status-time").text # Classe comum para o tempo
                
                resultado = f"{minuto}' | {casa} {score_casa} - {score_fora} {fora}"
                f.write(resultado)
                print(f"Sucesso: {resultado}")
                
            except Exception:
                # Se falhar nos elementos específicos, tenta pegar o bloco central de informações
                try:
                    info_central = driver.find_element(By.CLASS_NAME, "match-header").text
                    f.write(info_central.replace("\n", " "))
                except:
                    f.write("Ainda carregando dados ou elemento não encontrado.")

    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_detalhes_partida()
