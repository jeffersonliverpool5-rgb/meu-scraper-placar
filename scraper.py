import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_placar_time_zed():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Disfarce de usuário real para evitar bloqueios do Cloudflare
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Remove a marca de automação 'webdriver' do navegador
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        # Link da página do time ZED FC
        url = "https://www.aiscore.com/team-zed-fc/63kv9i939ncp7ez"
        print(f"Acessando página do time...")
        driver.get(url)
        
        # Espera 45 segundos para o JavaScript carregar os placares ao vivo
        time.sleep(45) 

        with open("placares.txt", "w", encoding="utf-8") as f:
            # Estratégia: Localizar o container que contém o nome do time e pegar o texto ao redor
            try:
                # Busca blocos de jogos (match-item ou similares)
                blocos_jogos = driver.find_elements(By.XPATH, "//div[contains(@class, 'match-item')] | //a[contains(@class, 'match-item')]")
                
                encontrou_jogo = False
                for bloco in blocos_jogos:
                    texto = bloco.text.strip().replace("\n", " ")
                    # Se o jogo estiver acontecendo, ele terá o nome do time e um placar ou minuto
                    if "ZED FC" in texto:
                        f.write(f"JOGO ATUAL: {texto}\n")
                        print(f"Dados capturados: {texto}")
                        encontrou_jogo = True
                
                if not encontrou_jogo:
                    # Plano B: Se não achar bloco, pega o texto bruto próximo ao nome do time
                    conteudo = driver.find_element(By.TAG_NAME, "body").text
                    if "ZED FC" in conteudo:
                        # Pega um pedaço do texto onde o nome do time aparece
                        idx = conteudo.find("ZED FC")
                        trecho = conteudo[idx-20:idx+100].replace("\n", " ")
                        f.write(f"TRECHO ENCONTRADO: {trecho}")
                    else:
                        f.write("Time ZED FC não localizado na página.")
            
            except Exception as e:
                f.write(f"Erro ao ler elementos: {str(e)}")

        print("Arquivo placares.txt atualizado!")

    except Exception as e:
        print(f"Erro no driver: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_time_zed()
