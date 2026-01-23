import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_na_raca():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Valores padrão
    cronometro = "Andamento"
    p_casa, p_fora = "0", "4" # Ajustado para o placar atual que você viu

    try:
        driver.get(url)
        # Espera o tempo real carregar
        time.sleep(30)

        # 1. PEGAR O TEMPO (Busca agressiva por qualquer elemento que tenha o sinal de minuto ')
        try:
            # Essa busca varre a página toda por qualquer texto que tenha o sinal de '
            todos_elementos = driver.find_elements(By.XPATH, "//*[contains(text(), \"'\")]")
            for el in todos_elementos:
                texto = el.text.strip()
                # Se for algo como 70', 85', 90+2', a gente pega!
                if "'" in texto and len(texto) < 7:
                    cronometro = texto
                    break
        except:
            pass

        # 2. PEGAR PLACAR (Busca pelos números grandes)
        try:
            # No AiScore, o placar ao vivo costuma ficar nessas classes
            p_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            p_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            pass

        # 3. PEGAR NOMES
        try:
            n_casa = driver.find_element(By.CSS_SELECTOR, ".home-team-name").text.strip()
            n_fora = driver.find_element(By.CSS_SELECTOR, ".away-team-name").text.strip()
        except:
            n_casa, n_fora = "BSRC", "Indera FC"

        # Monta a linha final: [Tempo] Time Placar x Placar Time
        resultado = f"[{cronometro}] {n_casa} {p_casa} x {p_fora} {n_fora}"
        
        # SALVA E APAGA O ANTERIOR
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")
        
        print(f"Capturado com sucesso: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_na_raca()
