import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar():
    url = "https://www.aiscore.com/match-bsrc-indera-fc/ndkz6i3lgg6hxq3"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(30) # Tempo para carregar o placar ao vivo

        # 1. CAPTURAR O TEMPO (Cronômetro)
        try:
            # Busca o elemento que contém o minuto (ex: 85')
            el_tempo = driver.find_element(By.CSS_SELECTOR, ".status-time, .playing, .match-status")
            cronometro = el_tempo.text.replace('\n', ' ').strip()
            # Se vier lixo ou texto longo, tenta pegar apenas o que tem o '
            if len(cronometro) > 10 or "'" not in cronometro:
                cronometro = driver.find_element(By.XPATH, "//*[contains(text(), \"'\")]").text.strip()
        except:
            cronometro = "Ao vivo"

        # 2. CAPTURAR PLACARES E TIMES
        try:
            p_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            p_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
            n_casa = driver.find_element(By.CSS_SELECTOR, ".home-team-name").text.strip()
            n_fora = driver.find_element(By.CSS_SELECTOR, ".away-team-name").text.strip()
        except:
            p_casa, p_fora, n_casa, n_fora = "0", "0", "BSRC", "Indera FC"

        # 3. FORMATAR RESULTADO
        # Exemplo: [88'] BSRC 0 x 6 Indera FC
        resultado = f"[{cronometro}] {n_casa} {p_casa} x {p_fora} {n_fora}"
        print(f"Resultado capturado: {resultado}")

        # 4. SALVAR E SOBRESCREVER O ARQUIVO
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")

    except Exception as e:
        print(f"Erro no script: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar()
