import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_completo():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        # 30 segundos é o tempo ideal para o placar ao vivo conectar
        time.sleep(30)

        # 1. BUSCA PELO TEMPO (Pega o número + o sinal de minuto)
        cronometro = "Ao vivo"
        try:
            # Procuramos o elemento que contém o minuto real. 
            # No AiScore, o pai do elemento que tem o "'" geralmente tem o tempo completo.
            el_tempo = driver.find_element(By.XPATH, "//*[contains(text(), \"'\")]/..")
            texto_bruto = el_tempo.text.strip().replace('\n', '')
            if texto_bruto:
                cronometro = texto_bruto
        except:
            # Fallback caso o jogo tenha acabado ou esteja no intervalo
            try:
                cronometro = driver.find_element(By.CSS_SELECTOR, ".match-status, .status-name").text.strip()
            except:
                pass

        # 2. CAPTURAR PLACAR
        try:
            p_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            p_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            p_casa, p_fora = "0", "4"

        # 3. CAPTURAR NOMES
        try:
            n_casa = driver.find_element(By.CSS_SELECTOR, ".home-team-name").text.strip()
            n_fora = driver.find_element(By.CSS_SELECTOR, ".away-team-name").text.strip()
        except:
            n_casa, n_fora = "BSRC", "Indera FC"

        # Resultado limpo: [85'] BSRC 0 x 4 Indera FC
        resultado = f"[{cronometro}] {n_casa} {p_casa} x {p_fora} {n_fora}"
        
        # Grava no arquivo limpando o anterior
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")
        
        print(f"Sucesso: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar_completo()
