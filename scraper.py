import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def rodar_scraper_atualizado():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Forçar a página a não usar cache antigo
    options.add_argument("--disable-cache")
    options.add_argument("--disk-cache-size=0")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Link do jogo (Exemplo Newcastle x PSV)
        # Certifique-se de usar o link da equipe ou do jogo específico
        driver.get("https://www.aiscore.com/match-newcastle-united-psv-eindhoven/705g6f33d79skql")
        
        # Espera o site carregar o placar real (ajustado para 30s para ser mais rápido e frequente)
        time.sleep(30) 

        # Captura os blocos de jogo
        elementos = driver.find_elements(By.XPATH, "//div[contains(@class, 'match')] | //div[contains(@class, 'item')] | //div[contains(@class, 'score')]")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            for el in elementos:
                txt = el.text.strip().replace("\n", " ")
                if len(txt) > 5:
                    f.write(txt + "\n")
                    
    except Exception as e:
        print(f"Erro na captura: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    rodar_scraper_atualizado()
