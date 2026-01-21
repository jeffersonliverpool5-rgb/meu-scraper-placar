import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_jogos_robusto():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # User-agent para parecer um acesso doméstico
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Iniciando acesso ao AiScore...")
        driver.get("https://www.aiscore.com/")
        
        # Aumentamos o tempo para 50 segundos para garantir o carregamento no servidor do GitHub
        time.sleep(50) 

        # Tenta pegar os jogos pela classe principal
        jogos = driver.find_elements(By.CLASS_NAME, "match-item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if jogos:
                print(f"Sucesso: {len(jogos)} jogos encontrados.")
                for jogo in jogos:
                    f.write(jogo.text.replace("\n", " ") + "\n")
            else:
                # REDE DE SEGURANÇA: Se as classes mudarem, ele pega o texto bruto da tela
                print("Classe não encontrada. Capturando texto bruto da página...")
                texto_total = driver.find_element(By.TAG_NAME, "body").text
                # Filtra apenas a parte que contém "Live" ou resultados
                f.write("--- CAPTURA DE SEGURANÇA ---\n")
                f.write(texto_total)

        print("Arquivo placares.txt atualizado!")

    except Exception as e:
        with open("placares.txt", "w") as f:
            f.write(f"Erro no sistema: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_jogos_robusto()
