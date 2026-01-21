import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_espn_viva():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Acessando partida na ESPN...")
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757770")
        
        # Espera o site carregar
        time.sleep(30)
        
        # Rola a página um pouco para garantir que o placar carregue
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(5)

        # CAPTURA TUDO (Sua rede de arrastão favorita)
        texto_completo = driver.find_element(By.TAG_NAME, "body").text
        
        # Salva o texto bruto para o GitHub limpar depois
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(texto_completo)
            
        print("Texto capturado com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_espn_viva()
