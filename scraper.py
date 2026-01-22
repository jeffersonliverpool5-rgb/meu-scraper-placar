import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair_aiscore():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://www.aiscore.com/match-argentinos-juniors-ferrocarril-midland/34kgmio142waeko"
        driver.get(url)
        
        # Aumentamos o tempo para garantir que o cronômetro carregue
        time.sleep(25)

        # 1. Nomes dos Times
        try:
            casa = driver.find_element(By.CSS_SELECTOR, ".home-team .name").text.strip()
            fora = driver.find_element(By.CSS_SELECTOR, ".away-team .name").text.strip()
        except:
            casa, fora = "Argentinos Jrs", "Midland"

        # 2. Placar
        try:
            g1 = driver.find_element(By.CLASS_NAME, "home-score").text.strip()
            g2 = driver.find_element(By.CLASS_NAME, "away-score").text.strip()
        except:
            g1, g2 = "0", "0"

        # 3. BUSCA DO TEMPO (Usando JavaScript para garantir a captura)
        tempo_jg = "Ao Vivo"
        try:
            # Esse seletor busca exatamente a div que fica entre os scores
            elemento_tempo = driver.find_element(By.CSS_SELECTOR, ".score-status")
            
            # O script abaixo pega todo o texto visível dentro dessa div, ignorando o placar
            texto_bruto = driver.execute_script("return arguments[0].innerText;", elemento_tempo)
            
            # O texto vem tipo "1 - 0\n45'" ou "1 - 0\nHT"
            # Vamos pegar apenas a parte que contém o minuto ou o status
            partes = texto_bruto.split('\n')
            if len(partes) > 1:
                tempo_jg = partes[1].strip() # Pega a segunda linha (onde fica o tempo)
            else:
                tempo_jg = partes[0].strip()
        except:
            tempo_jg = "Andamento"

        # Tradução rápida
        if "Half-time" in tempo_jg: tempo_jg = "Intervalo"
        if "Finished" in tempo_jg: tempo_jg = "Fim"

        resultado = f"{casa} {g1} X {g2} {fora} | {tempo_jg}"
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"DEBUG: {resultado}")

    except Exception as e:
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(f"Erro: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_aiscore()
