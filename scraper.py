import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def limpar_e_buscar_jogos():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.aiscore.com/")
        time.sleep(40) 

        jogos = driver.find_elements(By.CLASS_NAME, "match-item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            for jogo in jogos:
                try:
                    texto = jogo.text.replace("\n", " ")
                    # Tenta extrair apenas: TIME CASA - PLACAR - TIME FORA
                    # Usando uma regra simples de busca por padrões
                    match = re.search(r'(\d+)\s+(.*?)\s+(\d+\s+-\s+\d+)\s+(.*?)\s+HT', texto)
                    
                    if match:
                        minuto = match.group(1)
                        casa = match.group(2)
                        placar = match.group(3)
                        fora = match.group(4)
                        f.write(f"[{minuto}'] {casa} {placar} {fora}\n")
                    else:
                        # Se não conseguir limpar, salva o que pegou (como já está funcionando)
                        f.write(texto + "\n")
                except:
                    continue
        print("Placares atualizados e organizados!")
    finally:
        driver.quit()

if __name__ == "__main__":
    limpar_e_buscar_jogos()
