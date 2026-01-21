import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_jogo_especifico():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # LINK DO JOGO PRINCIPAL
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757771")
        time.sleep(35)
        
        # PEGA O TEXTO BRUTO
        linhas = driver.find_element(By.TAG_NAME, "body").text.split('\n')
        
        # --- CONFIGURAÇÃO DO JOGO ALVO ---
        TIME_A = "Galatasaray"
        TIME_B = "Atlético" # Ou "Atl Madrid"
        # ---------------------------------

        resultado_final = ""
        
        # Procura o índice onde o nome do time aparece
        for i, texto in enumerate(linhas):
            if TIME_A in texto or TIME_B in texto:
                # Quando acha o time, pega um bloco de 6 linhas ao redor
                # Geralmente o placar e o tempo estão logo acima ou abaixo
                bloco = linhas[i:i+8] 
                
                # Procura o minuto dentro desse bloco específico
                tempo = "Aguardando..."
                gols = []
                for item in bloco:
                    if "'" in item or "HT" in item or "Fim" in item:
                        tempo = item
                    elif re.match(r"^[0-9]$", item):
                        gols.append(item)
                
                # Se achamos pelo menos os times e o tempo, montamos a linha
                if len(gols) >= 2:
                    resultado_final = f"{TIME_A} {gols[0]} - {gols[1]} {TIME_B} | {tempo}"
                else:
                    # Caso o placar esteja em outro formato, pegamos o texto do bloco
                    resultado_final = f"{TIME_A} vs {TIME_B} | {tempo}"
                break # Para de procurar após achar o jogo certo

        if not resultado_final:
            resultado_final = "Jogo alvo não localizado na página."

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado_final)
            print(f"Gravado: {resultado_final}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_jogo_especifico()
