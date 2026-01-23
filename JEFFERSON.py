import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extrair_aiscore_preciso():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # User-agent é crucial para o AiScore não bloquear a requisição
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 25) # Aumentamos o tempo de espera

    try:
        url = "https://www.aiscore.com/match-instituto-de-cordoba-velez-sarsfield/vrqwni43wdgu4qn"
        driver.get(url)
        
        # 1. Espera o carregamento do elemento que contém o status do jogo (tempo/período)
        # O AiScore usa muito a classe 'score-status' ou 'status-running'
        elemento_tempo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".score-status, .match-status")))
        tempo_jg = elemento_tempo.text.strip().replace("\n", " ")

        # 2. Captura dos nomes dos times
        # Usando seletores que evitam pegar nomes de jogadores ou substitutos
        time_casa = driver.find_element(By.CSS_SELECTOR, ".home-team .name").text.strip()
        time_fora = driver.find_element(By.CSS_SELECTOR, ".away-team .name").text.strip()

        # 3. Captura do Placar
        # No layout atual, eles usam classes como 'home-score' e 'away-score' dentro do header
        try:
            g1 = driver.find_element(By.CSS_SELECTOR, ".score-home, .home-score").text.strip()
            g2 = driver.find_element(By.CSS_SELECTOR, ".score-away, .away-score").text.strip()
        except:
            g1, g2 = "0", "0"

        resultado = f"{time_casa} {g1} X {g2} {time_fora} | {tempo_jg}"
        
        # Limpa espaços duplos
        resultado = " ".join(resultado.split())

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"SUCESSO: {resultado}")

    except Exception as e:
        print(f"Erro na extração: {e}")
        # Tira um print da tela para debug (ajuda muito a ver o que o bot está vendo)
        driver.save_screenshot("debug_erro.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_aiscore_preciso()
