import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_focado_total():
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
        
        # 1. BUSCA OS TIMES PELAS CLASSES DE NOME CURTO/LONGO DA ESPN
        # Isso evita pegar "Carioca", "NFL", etc.
        try:
            # Tenta pegar os nomes que estão no bloco de placar
            times_elementos = driver.find_elements(By.XPATH, "//span[contains(@class, 'long-name')] | //span[contains(@class, 'short-name')] | //div[contains(@class, 'team-name')]")
            nomes = [t.text.strip() for t in times_elementos if t.text.strip() and len(t.text) > 1]
            
            # Pega os dois primeiros nomes únicos (Time Casa e Visitante)
            equipes = []
            for n in nomes:
                if n not in equipes and n not in ["NBA", "NFL", "Carioca", "Champions", "Paulista"]:
                    equipes.append(n)
            equipes = equipes[:2]
        except:
            equipes = ["Time A", "Time B"]

        # 2. BUSCA PLACAR E TEMPO (REDE DE ARRASTÃO NO TOPO)
        placar = ["0", "0"]
        tempo = "Aguardando..."
        
        try:
            # Foca apenas no container do placar para não pegar lixo
            container = driver.find_element(By.CLASS_NAME, "Gamestrip")
            texto_bruto = container.text.split('\n')
            
            gols_encontrados = []
            for linha in texto_bruto:
                linha = linha.strip()
                # Verifica minuto
                if "'" in linha or "HT" in linha or "Fim" in linha:
                    tempo = linha
                # Verifica números do placar
                elif re.match(r"^[0-9]$", linha):
                    gols_encontrados.append(linha)
            
            if len(gols_encontrados) >= 2:
                placar = gols_encontrados[:2]
        except:
            tempo = "Live"

        # MONTAGEM FINAL
        if len(equipes) >= 2:
            resultado = f"{equipes[0]} {placar[0]} - {placar[1]} {equipes[1]} | {tempo}"
        else:
            resultado = "Buscando dados da partida..."

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            print(f"Final: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_focado_total()
