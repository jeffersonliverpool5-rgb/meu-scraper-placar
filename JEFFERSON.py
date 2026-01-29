import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def commit_file():
    """Faz o upload automático do placares.txt para o seu GitHub"""
    try:
        subprocess.run(["git", "config", "--global", "user.name", "GitHub Actions"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "add", "placares.txt"], check=True)
        # O [skip ci] evita que o GitHub entre em loop infinito de Actions
        subprocess.run(["git", "commit", "-m", "Atualizando placar [skip ci]"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ ARQUIVO ENVIADO AO REPOSITÓRIO!")
    except Exception as e:
        print(f"⚠️ Sem alterações para subir ou erro no Git: {e}")

def extrair_aiscore():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # URL do jogo que você enviou por último
        url = "https://www.aiscore.com/match-panathinaikos-as-roma/ndqmliw585ltrkv"
        driver.get(url)
        
        # Espera para carregar o conteúdo dinâmico
        time.sleep(15)

        # 1. Busca os nomes dos times (Sua lógica original)
        try:
            time_casa = driver.find_element(By.XPATH, "//div[contains(@class, 'home-team')]//a[contains(@class, 'name')]").text.strip()
            time_fora = driver.find_element(By.XPATH, "//div[contains(@class, 'away-team')]//a[contains(@class, 'name')]").text.strip()
        except:
            time_casa, time_fora = "Panathinaikos","AS Roma"

        # 2. Busca o Placar (Gols)
        try:
            g1 = driver.find_element(By.CLASS_NAME, "home-score").text.strip()
            g2 = driver.find_element(By.CLASS_NAME, "away-score").text.strip()
        except:
            g1, g2 = "0", "0"

        # 3. Busca o Tempo do Jogo
        try:
            tempo_jg = driver.find_element(By.CSS_SELECTOR, ".score-status .status").text.strip()
            tempo_jg = tempo_jg.replace("\n", " ")
        except:
            tempo_jg = "Ao Vivo"

        # MONTAGEM DA LINHA FINAL
        resultado = f"{time_casa} {g1} X {g2} {time_fora} | {tempo_jg}"
        resultado = " ".join(resultado.split())

        # ESCREVE NO ARQUIVO
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"CAPTURA OK: {resultado}")
        
        # ENVIA PARA O GITHUB (Aparecerá na aba Code)
        commit_file()

    except Exception as e:
        print(f"ERRO: {e}")
    finally:
        driver.quit()

# REPETIR 100 VEZES COM INTERVALO DE 1 MINUTO
if __name__ == "__main__":
    for i in range(1, 151):
        print(f"\n--- ATUALIZAÇÃO {i} de 150 ---")
        extrair_aiscore()
        
        if i < 100:
            print("Aguardando 60 segundos...")
            time.sleep(30)
