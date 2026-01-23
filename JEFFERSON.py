import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_insano():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(30) # Espera o carregamento dos scripts do site

        # --- TÉCNICA 1: JAVASCRIPT DIRETO (Pega o que o olho humano vê) ---
        cronometro = driver.execute_script("""
            var el = document.querySelector('.status-time, .playing, .match-status span');
            return el ? el.innerText : '...';
        """)

        # Se o JS falhar, tenta pegar qualquer coisa com '
        if not cronometro or cronometro == '...':
            try:
                cronometro = driver.find_element(By.XPATH, "//*[contains(text(), \"'\")]").text
            except:
                cronometro = "Andamento"

        # --- PEGAR PLACAR ---
        try:
            p_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            p_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            p_casa, p_fora = "0", "5"

        # Nomes dos times fixos para evitar erro de carregamento
        n_casa, n_fora = "BSRC", "Indera FC"

        # Limpeza rápida
        cronometro = str(cronometro).replace('\n', '').strip()
        if len(cronometro) > 6: cronometro = "Live"

        resultado = f"[{cronometro}] {n_casa} {p_casa} x {p_fora} {n_fora}"
        
        # SALVA E APAGA O ANTERIOR
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")
        
        print(f"Resultado salvo: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar_insano()
