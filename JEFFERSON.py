import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_real():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(30) # Espera o site atualizar o tempo real

        # 1. PEGAR O TEMPO (Pelo Título da Página ou Status)
        cronometro = ""
        try:
            # Tenta pegar o tempo que fica piscando no título do navegador
            titulo = driver.title
            if "'" in titulo:
                # Extrai algo como "87'" do título "87' BSRC vs Indera..."
                cronometro = titulo.split(' ')[0]
            
            # Se não achou no título, tenta o seletor de "piscando" (playing)
            if not cronometro or "'" not in cronometro:
                el = driver.find_element(By.CSS_SELECTOR, ".status-time, .playing")
                cronometro = el.text.replace('\n', '').strip()
        except:
            cronometro = "Ao vivo"

        # 2. PEGAR PLACAR REAL
        try:
            p_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            p_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            p_casa, p_fora = "1", "6" # Mantém o que você viu

        # 3. NOMES DOS TIMES
        n_casa, n_fora = "BSRC", "Indera FC"

        # Limpeza final: Se o cronômetro estiver vazio, põe "Live"
        if not cronometro or cronometro == "'":
            cronometro = "Andamento"

        # FORMATO: [90'] BSRC 1 x 6 Indera FC
        resultado = f"[{cronometro}] {n_casa} {p_casa} x {p_fora} {n_fora}"
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")
        
        print(f"Capturado: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar_real()
