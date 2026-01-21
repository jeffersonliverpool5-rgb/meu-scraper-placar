import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_placar_zed_fc():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://www.aiscore.com/match-zed-fc-al-masry/ndkz6i3n5yjcxq3"
        print("Acessando página da partida...")
        driver.get(url)
        
        # Espera o carregamento completo (ajuste para 50s se necessário)
        time.sleep(45) 

        with open("placares.txt", "w", encoding="utf-8") as f:
            # Captura o texto de elementos que costumam conter o placar e tempo
            # Tentamos IDs e Classes comuns de containers de score
            seletores = [
                "//div[contains(@class, 'match-header')]",
                "//div[contains(@class, 'score-container')]",
                "//div[contains(@class, 'match-detail-header')]",
                "//div[@id='match-header']"
            ]
            
            encontrou = False
            for seletor in seletores:
                try:
                    elemento = driver.find_element(By.XPATH, seletor)
                    texto = elemento.text.strip().replace("\n", " ")
                    if len(texto) > 10:
                        f.write(texto)
                        print(f"Dados capturados: {texto}")
                        encontrou = True
                        break
                except:
                    continue
            
            if not encontrou:
                # Se tudo falhar, ele salva o texto bruto do corpo da página
                print("Tentando captura bruta...")
                corpo = driver.find_element(By.TAG_NAME, "body").text
                # Filtra apenas a parte que cita os times para não vir lixo
                if "ZED FC" in corpo:
                    f.write(corpo.split("ZED FC")[1][:200].replace("\n", " "))
                else:
                    f.write("Erro: Não foi possível localizar o placar na tela.")

    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_placar_zed_fc()
