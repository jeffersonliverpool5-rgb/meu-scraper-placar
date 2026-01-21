import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def rodar_scraper():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # AJUSTE O TIME AQUI
    TIME_NOME = "Newcastle" 
    
    try:
        # Link do time ou jogo
        driver.get("https://www.aiscore.com/team-newcastle-united/714x6i6v9y7q29v")
        time.sleep(45) 

        # Captura todos os blocos de partidas
        elementos = driver.find_elements(By.XPATH, "//div[contains(@class, 'match')] | //div[contains(@class, 'item')]")
        
        resultado_final = "Aguardando início do jogo..."

        for el in elementos:
            txt = el.text.strip().replace("\n", " ")
            # Se a linha contém o nome do time, salvamos ela
            if TIME_NOME in txt:
                # Se encontrar o símbolo de tempo (') ou HT, prioriza essa linha
                if "'" in txt or "HT" in txt:
                    resultado_final = " ".join(txt.split())
                    break 
                else:
                    # Se não estiver ao vivo ainda, guarda a linha do próximo jogo
                    resultado_final = " ".join(txt.split())

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado_final)
            print(f"Gravado: {resultado_final}")
                    
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    rodar_scraper()
