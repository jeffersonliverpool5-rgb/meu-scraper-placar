import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_aiscore_protegido():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # ISSO É O MAIS IMPORTANTE: Engana o sistema anti-bot
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Comando extra para evitar detecção
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        print("Acessando AiScore...")
        # Usamos o link direto da aba LIVE para evitar redirecionamentos
        driver.get("https://www.aiscore.com/live")
        
        # Espera longa para garantir que o JavaScript carregue os jogos
        time.sleep(20) 

        # Tenta pegar todos os blocos de jogos usando um seletor de texto
        jogos = driver.find_elements(By.CSS_SELECTOR, ".match-item, .item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not jogos:
                # Se não achou por classe, tenta pegar o texto bruto da página
                corpo_site = driver.find_element(By.TAG_NAME, "body").text
                if "Live" in corpo_site:
                    f.write("Dados Brutos Encontrados:\n")
                    f.write(corpo_site[:1000]) # Salva os primeiros 1000 caracteres
                else:
                    f.write("O site bloqueou o acesso ou não há jogos agora.")
            else:
                for jogo in jogos:
                    texto = jogo.text.replace("\n", " ")
                    if len(texto) > 5:
                        f.write(texto + "\n")
        
        print("Fim do processo.")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_aiscore_protegido()
