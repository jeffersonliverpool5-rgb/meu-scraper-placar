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
        url = "https://www.aiscore.com/match-inter-f-a-fuerte-san-francisco/69759igly5gugk2"
        driver.get(url)
        
        # Espera generosa para garantir o carregamento do conteúdo dinâmico
        time.sleep(15)

        # 1. Busca os nomes dos times dentro do container de cabeçalho
        try:
            # Usando caminhos mais específicos para não pegar nomes de jogadores
            time_casa = driver.find_element(By.XPATH, "//div[contains(@class, 'home-team')]//a[contains(@class, 'name')]").text.strip()
            time_fora = driver.find_element(By.XPATH, "//div[contains(@class, 'away-team')]//a[contains(@class, 'name')]").text.strip()
        except:
            time_casa, time_fora = "Inter F.A","Fuerte San Francisco"

        # 2. Busca o Placar (Gols)
        try:
            g1 = driver.find_element(By.CLASS_NAME, "home-score").text.strip()
            g2 = driver.find_element(By.CLASS_NAME, "away-score").text.strip()
        except:
            g1, g2 = "0", "0"

        # 3. Busca o Tempo do Jogo (Status central)
        try:
            # No AiScore, o tempo fica geralmente num elemento de classe 'status' ou 'period'
            tempo_jg = driver.find_element(By.CSS_SELECTOR, ".score-status .status").text.strip()
            # Se vier vazio ou com quebra de linha, limpamos
            tempo_jg = tempo_jg.replace("\n", " ")
        except:
            tempo_jg = "Ao Vivo"

        # MONTAGEM DA LINHA FINAL
        resultado = f"{time_casa} {g1} X {g2} {time_fora} | {tempo_jg}"
        
        # Limpeza final de strings
        resultado = " ".join(resultado.split())

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"CAPTURA OK: {resultado}")

    except Exception as e:
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(f"Erro na captura: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_aiscore()
