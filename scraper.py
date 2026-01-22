import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair_placar():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Coloque o link do jogo que você deseja aqui
        driver.get("https://ge.globo.com/rj/futebol/campeonato-carioca/jogo/21-01-2026/flamengo-vasco.ghtml")
        time.sleep(30)

        try:
            placar_bruto = driver.find_elements(By.CLASS_NAME, "placar-jogo__equipe--placar")
            g1 = placar_bruto[0].text.strip()
            g2 = placar_bruto[1].text.strip()
        except:
            g1, g2 = "0", "0"

        # MONTAGEM: Apenas os gols. Note que NÃO tem o tempo aqui.
        resultado = f"FLA {g1} X {g2} VAS"

        # "w" limpa o arquivo e começa a linha
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"Placar gravado: {resultado}")

    except Exception as e:
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write("Erro no Placar")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_placar()
