import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_placares_focados():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("Acessando AiScore...")
        driver.get("https://www.aiscore.com/")
        
        # 1. Espera o site carregar o básico
        time.sleep(15)

        # 2. Rola a página para baixo para carregar os jogos (Lazy Load)
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(15)

        # 3. Tenta encontrar apenas os blocos que contêm os nomes dos times
        # Mudamos o seletor para pegar a lista principal de partidas
        jogos = driver.find_elements(By.CSS_SELECTOR, ".match-list-main .match-item, .match-item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not jogos:
                # Se ainda não achar, vamos pegar o texto de uma área específica
                print("Tentando captura por área central...")
                try:
                    area_central = driver.find_element(By.CLASS_NAME, "match-list-main").text
                    f.write(area_central)
                except:
                    # Última tentativa: buscar qualquer texto que tenha '-' (indicando placar)
                    elementos_com_texto = driver.find_elements(By.XPATH, "//div[contains(text(), '-')]")
                    for el in elementos_com_texto:
                        f.write(el.text.replace("\n", " ") + "\n")
            else:
                for jogo in jogos:
                    texto = jogo.text.strip().replace("\n", " ")
                    # Só grava se tiver algo que pareça um jogo (evita menus)
                    if len(texto) > 10 and "Favorites" not in texto:
                        f.write(texto + "\n")
                        print(f"Jogo gravado: {texto}")

        print("Finalizado!")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placares_focados()
