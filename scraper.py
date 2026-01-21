import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def buscar_placares_com_gols():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Camuflagem anti-bot
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Esconde o uso de automação
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        print("Acessando AiScore...")
        driver.get("https://www.aiscore.com/")
        
        # Espera 40 segundos para garantir que os placares ao vivo carreguem
        time.sleep(40) 

        # Tenta capturar os blocos de partidas centrais
        # O seletor '.match-item' captura o bloco todo (Nomes + Placar)
        jogos = driver.find_elements(By.CSS_SELECTOR, ".match-item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not jogos:
                f.write("Não foi possível encontrar os blocos de jogos. Tentando alternativa...\n")
                # Alternativa: pega o texto de todos os elementos que parecem placar (ex: 0-0, 1-2)
                elementos_texto = driver.find_elements(By.XPATH, "//*[contains(text(), '-')]")
                for el in elementos_texto:
                    txt = el.text.strip()
                    if len(txt) > 3 and len(txt) < 100:
                        f.write(txt.replace("\n", " ") + "\n")
            else:
                for jogo in jogos:
                    try:
                        # Extrai o texto completo do bloco (isso costuma incluir Nome Casa, Placar e Nome Fora)
                        info = jogo.text.strip().split('\n')
                        
                        # Tenta organizar: [Time Casa] [Placar] [Time Fora]
                        # Geralmente o AiScore coloca o placar no meio das linhas de texto
                        linha_formatada = " | ".join(info)
                        
                        if len(linha_formatada) > 5:
                            f.write(linha_formatada + "\n")
                            print(f"Capturado: {linha_formatada}")
                    except:
                        continue

        print("Processo finalizado. Arquivo placares.txt atualizado.")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placares_com_gols()
