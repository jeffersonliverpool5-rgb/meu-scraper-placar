import time
import re
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair_na_marra():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Adiciona um número aleatório no final para burlar o cache do site
        url = "https://ge.globo.com/rs/futebol/campeonato-gaucho/jogo/21-01-2026/internacional-inter-sm.ghtml"
        driver.get(f"{url}?update={random.randint(1, 99999)}")
        
        # Espera o carregamento (reduzi para 20s para não estourar o tempo do GitHub)
        time.sleep(20)

        # 1. Captura do Placar (Usando Seletores de Classe Específicos)
        try:
            g1 = driver.find_element(By.CSS_SELECTOR, ".placar-jogo__equipe--placar-mandante").text.strip()
            g2 = driver.find_element(By.CSS_SELECTOR, ".placar-jogo__equipe--placar-visitante").text.strip()
        except:
            try:
                # Fallback caso mude a classe
                placares = driver.find_elements(By.CLASS_NAME, "placar-jogo__equipe--placar")
                g1 = placares[0].text.strip()
                g2 = placares[1].text.strip()
            except:
                g1, g2 = "0", "0"

        # 2. Busca do Tempo/Período
        tempo_final = "Ao Vivo"
        try:
            # Tenta pegar o tempo real (ex: 34' 2T)
            elemento_tempo = driver.find_element(By.CLASS_NAME, "placar-jogo__periodo")
            tempo_final = elemento_tempo.text.replace("\n", " ").strip()
        except:
            # Busca por Regex no corpo da página se o elemento falhar
            todo_texto = driver.find_element(By.TAG_NAME, "body").text
            match = re.search(r"(\d{1,2}:\d{2}(\s[12]T)?)|(\d{1,2}')", todo_texto)
            if match:
                tempo_final = match.group(0)

        # Formatação Final
        resultado = f"INT {g1} X {g2} ISM | {tempo_final}"
        resultado = resultado.replace("\n", "").strip()

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"SUCESSO: {resultado}")

    except Exception as e:
        print(f"ERRO: {e}")
        with open("placares.txt", "a", encoding="utf-8") as f:
            f.write(f"\nErro em: {time.strftime('%H:%M:%S')}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_na_marra()
