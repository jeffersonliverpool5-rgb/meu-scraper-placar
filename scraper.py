import time
import re
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
        driver.get("https://ge.globo.com/sp/futebol/campeonato-paulista/jogo/21-01-2026/sao-paulo-portuguesa.ghtml")
        
        # Espera o carregamento total (aumentado para 40s)
        time.sleep(40)

        # 1. Pega os nomes e placar pelos seletores mais básicos do GE
        try:
            placar_bruto = driver.find_elements(By.CLASS_NAME, "placar-jogo__equipe--placar")
            g1 = placar_bruto[0].text.strip()
            g2 = placar_bruto[1].text.strip()
        except:
            g1, g2 = "0", "0"

        # 2. BUSCA DO TEMPO (A "MERDA" QUE VAMOS TIRAR)
        # Se não achar o tempo específico, ele vai varrer a página atrás de algo como "28:23" ou "30'"
        tempo_final = "Andamento"
        
        # Pega todo o texto da página
        todo_texto = driver.find_element(By.TAG_NAME, "body").text
        
        # Procura o padrão de tempo (ex: 28:23 1T ou apenas 28:23)
        match = re.search(r"(\d{1,2}:\d{2}(\s[12]T)?)|(\d{1,2}')", todo_texto)
        
        if match:
            tempo_final = match.group(0)
        else:
            # Se ainda assim não achar, tenta pegar o texto do elemento de período do GE
            try:
                tempo_final = driver.find_element(By.CLASS_NAME, "placar-jogo__periodo").text.replace("\n", " ")
            except:
                tempo_final = "Ao Vivo"

        # MONTAGEM DA LINHA ÚNICA
        resultado = f"INT {g1} X {g2} ISM | {tempo_final}"
        
        # Limpa qualquer quebra de linha indesejada
        resultado = resultado.replace("\n", "").strip()

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"DEBUG TEXTO COMPLETO: {resultado}")

    except Exception as e:
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(f"INT 0 X 0 ISM | Erro na Captura")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_na_marra()
