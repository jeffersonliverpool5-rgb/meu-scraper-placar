import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_limpo():
    url = "https://www.aiscore.com/match-ca-penarol-boston-river/ndqmliw2oxehrkv"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # User-agent atualizado para parecer um navegador real
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = None
    try:
        # Inicia o driver com o WebDriver Manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(url)
        
        # Espera até 20 segundos para o placar aparecer na tela (mais seguro que sleep fixo)
        wait = WebDriverWait(driver, 20)
        
        try:
            # Tenta localizar o placar da casa para confirmar que a página carregou
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".home-score")))
            
            nome_casa = driver.find_element(By.CSS_SELECTOR, ".home-team-name, .home-name, .home-team .name").text.strip()
            nome_fora = driver.find_element(By.CSS_SELECTOR, ".away-team-name, .away-name, .away-team .name").text.strip()
            placar_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            placar_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
            
            # Busca o tempo
            cronometro = "Ao vivo"
            elementos_tempo = driver.find_elements(By.XPATH, "//*[contains(text(), \"'\")]")
            for el in elementos_tempo:
                texto = el.text.strip()
                if "'" in texto and len(texto) <= 6:
                    cronometro = texto
                    break
            
            resultado = f"[{cronometro}] {nome_casa} {placar_casa} x {placar_fora} {nome_fora}"
            
            with open("placares.txt", "w", encoding="utf-8") as f:
                f.write(resultado + "\n")
            
            return resultado

        except Exception as e_intern:
            return f"Erro ao localizar elementos: {e_intern}"

    except Exception as e:
        return f"Erro de conexão/driver: {e}"
    
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    for i in range(1, 101):
        print(f"\n--- Tentativa {i} de 100 ---")
        resultado = extrair_placar_limpo()
        print(f"Status: {resultado}")
        
        if i < 100:
            print("Aguardando 60 segundos...")
            time.sleep(60)
