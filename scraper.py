import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_focado():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # LINK DO JOGO
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757771")
        time.sleep(30)
        
        # FOCO TOTAL: Pega o container do placar (Gamestrip / Competitors)
        # Esse bloco contém apenas os dois times, o placar e o tempo.
        try:
            placar_focado = driver.find_element(By.CSS_SELECTOR, ".competitors, .Gamestrip, .Gamestrip__Overview")
            texto_bruto = placar_focado.text.split('\n')
        except:
            # Caso o CSS mude, pega o topo do body mas filtra mais pesado
            texto_bruto = driver.find_element(By.TAG_NAME, "body").text.split('\n')[:40]

        # Limpeza seletiva
        lixo = ["O Melhor", "Champions", "NBA", "Paulista", "Copinha", "Vídeo", "Menu", "Resultados", "Futebol"]
        dados_bons = [linha for linha in texto_bruto if not any(palavra in linha for palavra in lixo) and len(linha.strip()) > 0]

        times = []
        gols = []
        tempo = "Aguardando..."

        for item in dados_bons:
            # 1. Minuto ou Status
            if "'" in item or "HT" in item or "Fim" in item or "Intervalo" in item:
                tempo = item
            # 2. Placar (Números sozinhos)
            elif re.match(r"^[0-9]+$", item) and len(item) <= 2:
                gols.append(item)
            # 3. Nomes dos Times (Geralmente são palavras maiores que 2 letras)
            elif len(item) > 2 and len(times) < 2:
                times.append(item)

        # MONTAGEM DA LINHA
        if len(times) >= 2 and len(gols) >= 2:
            resultado = f"{times[0]} {gols[0]} - {gols[1]} {times[1]} | {tempo}"
        elif len(times) >= 2:
            resultado = f"{times[0]} vs {times[1]} | {tempo}"
        else:
            resultado = "Dados do placar não encontrados no momento."

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            print(f"Capturado: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_focado()
