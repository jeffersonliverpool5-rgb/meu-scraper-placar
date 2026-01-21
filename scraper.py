import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_partida_especifica():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Disfarce de navegador real
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Camuflagem para não ser detectado como bot
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        url = "https://www.aiscore.com/match-zed-fc-al-masry/ndkz6i3n5yjcxq3"
        print(f"Acessando partida: {url}")
        driver.get(url)
        
        # Espera o placar e as estatísticas carregarem
        time.sleep(30) 

        with open("placares.txt", "w", encoding="utf-8") as f:
            try:
                # 1. Tenta pegar os nomes dos times e o placar no topo
                header = driver.find_element(By.CLASS_NAME, "match-header")
                f.write("=== DADOS DO JOGO ===\n")
                f.write(header.text.replace("\n", " ") + "\n\n")
            except:
                # Se não achar o header, pega o título da página
                f.write(f"Partida: {driver.title}\n")

            try:
                # 2. Tenta pegar as estatísticas principais (posse, chutes, etc)
                estatisticas = driver.find_elements(By.CLASS_NAME, "stat-item")
                if estatisticas:
                    f.write("=== ESTATÍSTICAS ===\n")
                    for stat in estatisticas:
                        f.write(stat.text.replace("\n", " ") + "\n")
            except:
                pass

        print("Arquivo placares.txt atualizado com os dados da partida!")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_partida_especifica()
