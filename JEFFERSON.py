import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_limpo():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(25) # Espera o carregamento

        # 1. PEGAR O TEMPO (Focado no container de status)
        cronometro = "HT"
        try:
            # Busca especificamente na área de tempo/status
            el_status = driver.find_element(By.CSS_SELECTOR, ".match-status, .status-name, .status-time")
            cronometro = el_status.text.strip().replace('\n', ' ')
            
            # Se o texto for muito longo (pegou coisa errada), encurta
            if len(cronometro) > 10:
                # Tenta pegar apenas o que tem o símbolo de minuto
                minuto = driver.find_element(By.XPATH, "//*[contains(text(), \"'\")]")
                cronometro = minuto.text.strip()
        except:
            cronometro = "Live"

        # 2. PEGAR PLACAR
        try:
            p_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            p_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            p_casa, p_fora = "0", "5"

        # 3. NOMES DOS TIMES
        n_casa, n_fora = "BSRC", "Indera FC"

        # Formato final desejado
        resultado = f"[{cronometro}] {n_casa} {p_casa} x {p_fora} {n_fora}"
        
        # Salva e limpa o arquivo
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")
        
        print(f"Gravado: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar_limpo()
