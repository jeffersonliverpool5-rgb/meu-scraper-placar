import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair_relogio():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://ge.globo.com/rj/futebol/campeonato-carioca/jogo/21-01-2026/flamengo-vasco.ghtml")
        time.sleep(35) # Espera o relógio carregar bem

        todo_texto = driver.find_element(By.TAG_NAME, "body").text
        match = re.search(r"(\d{1,2}:\d{2}(\s[12]T)?)|(\d{1,2}')", todo_texto)
        
        tempo_final = match.group(0) if match else "Ao Vivo"

        # O SEGREDO: "a" abre para anexar. O " | " separa o tempo do placar.
        with open("placares.txt", "a", encoding="utf-8") as f:
            f.write(f" | {tempo_final}")
            
        print(f"Tempo adicionado: {tempo_final}")

    except Exception as e:
        with open("placares.txt", "a", encoding="utf-8") as f:
            f.write(" | --:--")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_relogio()
