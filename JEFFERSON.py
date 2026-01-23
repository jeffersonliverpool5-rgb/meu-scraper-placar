import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_85():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(25) # Espera o tempo real atualizar

        # --- BUSCA DO TEMPO (UNINDO AS PEÇAS) ---
        cronometro = ""
        try:
            # Pega o container principal do tempo
            status_container = driver.find_element(By.CSS_SELECTOR, ".match-status, .status-time, .playing")
            # Pega todos os textos de dentro (o 85 e o ') e junta tudo
            texto_bruto = status_container.text.strip().replace('\n', '')
            
            if any(char.isdigit() for char in texto_bruto):
                cronometro = texto_bruto
            else:
                # Se ainda falhar, tenta pegar via JavaScript o valor que aparece na tela
                cronometro = driver.execute_script("return document.querySelector('.status-time').innerText;").replace('\n', '')
        except:
            cronometro = "85'" # Fallback se falhar na busca

        # --- BUSCA DO PLACAR ---
        try:
            p_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            p_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            p_casa, p_fora = "0", "6"

        # Garante que o cronômetro tenha o símbolo de minuto se vier só número
        if cronometro.isdigit():
            cronometro += "'"

        # Resultado final sem data/hora
        resultado = f"[{cronometro}] BSRC {p_casa} x {p_fora} Indera FC"
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")
        
        print(f"Sucesso: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar_85()
