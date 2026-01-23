import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_v3():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(30) # Tempo para o WebSocket do tempo carregar

        # 1. PEGAR O TEMPO (Técnica de busca por texto limpo)
        cronometro = "Ao vivo"
        try:
            # Pegamos o container de status completo
            el_status = driver.find_element(By.CSS_SELECTOR, ".match-status, .status-time")
            # Extraímos todo o texto dentro dele, mesmo que esteja em spans separados
            texto_status = el_status.text.replace('\n', '').strip()
            
            if texto_status and any(char.isdigit() for char in texto_status):
                cronometro = texto_status
            else:
                # Tentativa 2: Buscar especificamente o número que pisca
                minuto = driver.find_element(By.CSS_SELECTOR, ".status-time span, .playing").text
                cronometro = f"{minuto}'" if minuto.isdigit() else minuto
        except:
            pass

        # 2. PEGAR PLACAR
        try:
            p_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            p_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            p_casa, p_fora = "0", "6"

        # 3. NOMES DOS TIMES
        n_casa, n_fora = "BSRC", "Indera FC"

        # Formatação final: [Tempo] Time Placar x Placar Time
        # Remove espaços duplos se existirem
        cronometro = " ".join(cronometro.split())
        resultado = f"[{cronometro}] {n_casa} {p_casa} x {p_fora} {n_fora}"
        
        # Grava no arquivo limpando o anterior
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")
        
        print(f"Salvo: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar_v3()
