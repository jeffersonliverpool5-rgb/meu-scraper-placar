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
        time.sleep(30) 

        jogos = driver.find_elements(By.CLASS_NAME, "match-item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not jogos:
                f.write("Nenhum jogo encontrado no momento.")
            else:
                for jogo in jogos:
                    try:
                        casa = jogo.find_element(By.CLASS_NAME, "home-name").text
                        fora = jogo.find_element(By.CLASS_NAME, "away-name").text
                        
                        try:
                            score_bruto = jogo.find_element(By.CLASS_NAME, "score").text
                            # Correção do erro da barra invertida:
                            score_limpo = score_bruto.replace('\n', '-')
                        except:
                            score_limpo = "vs"
                        
                        resultado = f"{casa} {score_limpo} {fora}"
                        f.write(resultado + "\n")
                        print(f"Salvo: {resultado}")
                    except:
                        continue

        print("Atualização concluída!")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placares_detalhados()
