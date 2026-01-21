import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_placares_detalhados():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Coletando placares detalhados...")
        driver.get("https://www.aiscore.com/live")
        time.sleep(25) # Tempo essencial para carregar os números dos gols

        # O AiScore organiza os dados em classes específicas para nomes e scores
        # Vamos tentar capturar os blocos de jogo completos
        jogos = driver.find_elements(By.CLASS_NAME, "match-item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not jogos:
                # Se a classe mudar, ele tenta pegar pelo seletor de texto que funcionou antes
                corpo = driver.find_element(By.TAG_NAME, "body").text
                f.write(corpo)
            else:
                for jogo in jogos:
                    try:
                        # Tenta extrair cada parte separadamente
                        casa = jogo.find_element(By.CLASS_NAME, "home-name").text
                        fora = jogo.find_element(By.CLASS_NAME, "away-name").text
                        
                        # Tenta pegar o score. Se não achar, tenta a classe geral de placar
                        try:
                            score = jogo.find_element(By.CLASS_NAME, "score").text
                        except:
                            score = "vs" # Caso o jogo ainda não tenha começado
                        
                        linha = f"{casa} {score.replace('\n', '-')} {fora}"
                        f.write(linha + "\n")
                        print(f"Salvo: {linha}")
                    except:
                        # Se falhar em um jogo, tenta pegar o texto bruto do bloco
                        f.write(jogo.text.replace("\n", " ") + "\n")

        print("Atualização concluída com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placares_detalhados()
