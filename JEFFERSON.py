import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def monitorar_placar():
    options = Options()
    # Desative o headless se continuar sem atualizar para testar
    options.add_argument("--headless") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    print("Iniciando monitoramento... (Pressione Ctrl+C para parar)")

    try:
        while True:
            url = "https://www.aiscore.com/match-instituto-de-cordoba-velez-sarsfield/vrqwni43wdgu4qn"
            driver.get(url)
            
            # Espera carregar os elementos principais
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".home-score, .score-home")))

            # Pega Nomes
            t_casa = driver.find_element(By.CSS_SELECTOR, ".home-team .name").text.strip()
            t_fora = driver.find_element(By.CSS_SELECTOR, ".away-team .name").text.strip()

            # Pega Gols (Tentando dois seletores comuns do AiScore para garantir)
            try:
                g_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
                g_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
            except:
                g_casa = driver.find_element(By.CSS_SELECTOR, ".score-home").text.strip()
                g_fora = driver.find_element(By.CSS_SELECTOR, ".score-away").text.strip()

            resultado = f"{t_casa} {g_casa} X {g_fora} {t_fora}"
            
            # Salva e exibe no console com horário
            com_hora = f"[{time.strftime('%H:%M:%S')}] {resultado}"
            with open("placares.txt", "w", encoding="utf-8") as f:
                f.write(com_hora)
            
            print(com_hora)

            # Espera 30 segundos para a próxima atualização
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nMonitoramento parado pelo usuário.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    monitorar_placar()
