import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def buscar_aiscore():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Abrindo AiScore Live...")
        driver.get("https://www.aiscore.com")
        
        # Espera até 20 segundos para a página carregar os jogos
        wait = WebDriverWait(driver, 20)
        
        # Tenta localizar os itens de jogo de uma forma mais robusta
        time.sleep(10) 
        
        # Busca todos os blocos de jogos
        jogos = driver.find_elements(By.XPATH, "//div[contains(@class, 'match-item')]")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not jogos:
                f.write("Nenhum jogo ao vivo detectado no momento.")
                print("Nenhum jogo encontrado.")
            else:
                for jogo in jogos:
                    try:
                        # Pega o texto inteiro do bloco do jogo e limpa
                        dados = jogo.text.replace('\n', ' ')
                        f.write(dados + "\n")
                        print(f"Capturado: {dados}")
                    except:
                        continue
        print("Processo concluído.")
        
    except Exception as e:
        with open("placares.txt", "w") as f:
            f.write(f"Erro no scraping: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_aiscore()
