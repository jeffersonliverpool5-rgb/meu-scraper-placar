import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_placares_disfarçado():
    options = Options()
    # Modo headless é necessário para o GitHub, mas vamos camuflá-lo
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # 1. User-agent de um navegador real e atualizado
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # 2. Remove as marcas de automação que os sites detectam
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 3. Script para esconder o parâmetro "navigator.webdriver" do Selenium
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        print("Acessando AiScore com camuflagem...")
        # Acessa a página principal onde os jogos ficam na frente
        driver.get("https://www.aiscore.com/")
        
        # Espera um tempo generoso para o conteúdo dinâmico carregar
        time.sleep(35) 

        # Procura pelos blocos de partidas (usando classes comuns do AiScore)
        jogos = driver.find_elements(By.CLASS_NAME, "match-item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not jogos:
                # Se não achar por classe, tenta pegar o texto que contém placares
                f.write("Nenhum jogo detectado. Tentando captura de texto bruto...\n")
                corpo = driver.find_element(By.TAG_NAME, "body").text
                f.write(corpo[:2000]) # Salva uma parte do texto da página
            else:
                for jogo in jogos:
                    try:
                        # Extrai o texto de cada jogo e limpa
                        dados_jogo = jogo.text.strip().replace('\n', ' | ')
                        if len(dados_jogo) > 10:
                            f.write(dados_jogo + "\n")
                    except:
                        continue

        print("Arquivo placares.txt atualizado!")

    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placares_disfarçado()
