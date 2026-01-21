import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_aiscore_ajustado():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Acessando aba Live do AiScore...")
        driver.get("https://www.aiscore.com/live")
        
        # Espera o site carregar totalmente os placares
        time.sleep(25) 

        # No AiScore, os jogos ficam dentro de elementos com a classe 'match-list'
        # Vamos tentar pegar os itens da lista de forma mais precisa
        jogos = driver.find_elements(By.XPATH, "//div[contains(@class, 'match-item')]")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not jogos:
                # Se não achou os itens, tenta pegar todas as linhas de texto que tenham números (placares)
                elementos = driver.find_elements(By.XPATH, "//*[contains(text(), '-')]")
                for el in elementos:
                    txt = el.text.strip()
                    if len(txt) > 5 and len(txt) < 100:
                        f.write(txt.replace("\n", " ") + "\n")
            else:
                for jogo in jogos:
                    texto = jogo.text.replace("\n", " ").strip()
                    # Filtro: só salva se tiver cara de jogo (evita menus de idiomas)
                    if len(texto) > 10 and not "Football Live Score" in texto:
                        f.write(texto + "\n")
                        print(f"Jogo encontrado: {texto}")
        
        print("Arquivo placares.txt atualizado!")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_aiscore_ajustado()
