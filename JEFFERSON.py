import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extrair_aiscore():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # User-agent mais atualizado para evitar bloqueios
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20) # Espera explícita de até 20 segundos
    
    try:
        url = "https://www.aiscore.com/match-capital-cf-real-fc/ezk96i369dxu1kn"
        driver.get(url)
        
        # 1. Capturar Nomes dos Times (Aguardando o elemento carregar)
        home_team_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'home-team')]//a[contains(@class, 'name')]")))
        time_casa = home_team_element.text.strip()
        time_fora = driver.find_element(By.XPATH, "//div[contains(@class, 'away-team')]//a[contains(@class, 'name')]").text.strip()

        # 2. Capturar Placar (Usando seletores que englobam o placar ao vivo e final)
        try:
            # Tenta buscar pelo container de score que o AiScore usa no topo
            g1 = driver.find_element(By.XPATH, "//div[contains(@class, 'score-item')][1]").text.strip()
            g2 = driver.find_element(By.XPATH, "//div[contains(@class, 'score-item')][2]").text.strip()
        except:
            # Fallback para as classes que você estava usando
            try:
                g1 = driver.find_element(By.CLASS_NAME, "home-score").text.strip()
                g2 = driver.find_element(By.CLASS_NAME, "away-score").text.strip()
            except:
                g1, g2 = "0", "0"

        # 3. Capturar Tempo/Status
        try:
            # O status costuma ficar em um span dentro do header
            tempo_jg = driver.find_element(By.XPATH, "//div[contains(@class, 'score-status')]//span[contains(@class, 'status')]").text.strip()
        except:
            tempo_jg = "Status Indisponível"

        # Formatação
        resultado = f"{time_casa} {g1} X {g2} {time_fora} | {tempo_jg}"
        resultado = " ".join(resultado.split())

        # Escrita garantida
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            f.flush()
            
        print(f"ATUALIZADO: {resultado}")

    except Exception as e:
        erro_msg = f"Erro na captura: {str(e)}"
        print(erro_msg)
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(erro_msg)
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_aiscore()
