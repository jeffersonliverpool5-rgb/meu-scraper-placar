import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_aiscore():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.aiscore.com/live")
        time.sleep(10) # Tempo para carregar os jogos

        # Seletor simplificado: busca os itens da lista de jogos
        jogos = driver.find_elements(By.CSS_SELECTOR, ".match-list .match-item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            for jogo in jogos:
                try:
                    casa = jogo.find_element(By.CSS_SELECTOR, ".home-team .name").text
                    fora = jogo.find_element(By.CSS_SELECTOR, ".away-team .name").text
                    score = jogo.find_element(By.CSS_SELECTOR, ".score").text
                    
                    f.write(f"{casa} {score} {fora}\n")
                except:
                    continue
        print("Scraping finalizado com sucesso.")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_aiscore()
