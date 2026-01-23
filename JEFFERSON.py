import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_blindado():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Valores padrão caso tudo falhe
    cronometro = "Andamento"
    n_casa, n_fora = "BSRC", "Indera FC"
    p_casa, p_fora = "0", "0"

    try:
        driver.get(url)
        time.sleep(30) # Espera o site carregar

        # --- CAPTURAR NOMES ---
        try:
            n_casa = driver.find_element(By.CSS_SELECTOR, ".home-team-name, .home-name").text.strip()
            n_fora = driver.find_element(By.CSS_SELECTOR, ".away-team-name, .away-name").text.strip()
        except: pass

        # --- CAPTURAR PLACAR ---
        try:
            p_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            p_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except: pass

        # --- CAPTURAR TEMPO (O MAIS DIFÍCIL) ---
        try:
            # Tenta 3 seletores diferentes para o tempo
            seletores_tempo = [
                "//span[contains(@class, 'status-time')]",
                "//div[contains(@class, 'match-status')]//span[contains(text(), \"'\")]",
                "//span[contains(@class, 'playing')]"
            ]
            for sel in seletores_tempo:
                try:
                    el = driver.find_element(By.XPATH, sel)
                    if el.text.strip():
                        cronometro = el.text.strip()
                        break
                except: continue
        except: pass

        # Montagem do resultado
        resultado = f"[{cronometro}] {n_casa} {p_casa} x {p_fora} {n_fora}"
        
        # Salva no arquivo
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")
        
        print(f"Sucesso: {resultado}")

    except Exception as e:
        print(f"Erro Crítico: {e}")
        # Se der erro, salva pelo menos o que tinha de padrão
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(f"[Erro] BSRC {p_casa} x {p_fora} Indera FC\n")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_blindado()
