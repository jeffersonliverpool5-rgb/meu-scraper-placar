from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extrair_placar_e_nomes():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    try:
        url = "https://www.aiscore.com/match-instituto-de-cordoba-velez-sarsfield/vrqwni43wdgu4qn"
        driver.get(url)
        
        # Espera o container principal carregar
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "score-content")))

        # Pega os nomes
        time_casa = driver.find_element(By.CSS_SELECTOR, ".home-team .name").text.strip()
        time_fora = driver.find_element(By.CSS_SELECTOR, ".away-team .name").text.strip()

        # Pega os gols
        gols_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
        gols_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()

        resultado = f"{time_casa} {gols_casa} X {gols_fora} {time_fora}"
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"CAPTURA: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar_e_nomes()
