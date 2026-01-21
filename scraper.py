import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_e_limpar_agenda():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Acessa o link do time onde estão esses dados
        driver.get("https://www.aiscore.com/team-shire-endaselassie-fc/34kgmino3lh8ko9")
        time.sleep(45) 

        # Pega os blocos que contêm as informações das partidas
        # O seletor 'match-item' ou 'schedule-item' costuma conter essas linhas
        elementos = driver.find_elements(By.XPATH, "//*[contains(text(), 'Shire')]")
        
        resultados_finais = []

        for el in elementos:
            # Pega o texto e remove quebras de linha extras
            texto = el.text.strip()
            
            # REGRA DE LIMPEZA:
            # 1. Procura por padrões de placar como "1 - 3", "0 - 1" ou apenas "-"
            # 2. Ignora textos longos de "Premier League" e datas
            if "Shire" in texto and ("-" in texto or "vs" in texto):
                # Remove informações que você não quer (datas e nome da liga)
                # Vamos usar Expressão Regular para pegar apenas o essencial
                # Tenta capturar: Time Casa + Placar + Time Fora
                partes = texto.split('\n')
                
                # Se o texto vier bagunçado em uma linha só, tentamos organizar
                linha_limpa = texto.replace("Ethiopia Premier League", "").strip()
                # Remove datas (ex: 4 Jan 10:00)
                linha_limpa = re.sub(r'\d+\s+[a-zA-Z]+\s+\d{2}:\d{2}', '', linha_limpa)
                
                if len(linha_limpa) > 5:
                    # Evita duplicados na lista
                    if linha_limpa not in resultados_finais:
                        resultados_finais.append(linha_limpa)

        with open("placares.txt", "w", encoding="utf-8") as f:
            if resultados_finais:
                for res in resultados_finais:
                    # Limpeza final de espaços duplos
                    final = " ".join(res.split())
                    f.write(final + "\n")
                    print(f"Adicionado: {final}")
            else:
                f.write("Nenhum dado de jogo formatado foi encontrado.")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_e_limpar_agenda()
