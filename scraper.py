import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_agenda_e_ao_vivo():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def buscar_jogos_aiscore():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Disfarce de navegador real para evitar bloqueios
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Remove a marca de "webdriver" que denuncia o bot
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        print("Acessando AiScore...")
        # Acessa a página com a lista de jogos central
        driver.get("https://www.aiscore.com/")
        
        # Espera 40 segundos para garantir que a lista central carregue totalmente
        time.sleep(40) 

        # Procura pelos blocos de jogos na área central (match-item)
        jogos = driver.find_elements(By.CLASS_NAME, "match-item")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            if not jogos:
                f.write("Nenhum jogo encontrado na área central.")
            else:
                for jogo in jogos:
                    try:
                        # Extrai o texto do bloco central (Times e Placar)
                        texto_bruto = jogo.text.strip()
                        if len(texto_bruto) > 5:
                            # Corrige o erro de sintaxe limpando o texto fora da f-string
                            linha_limpa = texto_bruto.replace("\n", " | ")
                            f.write(f"{linha_limpa}\n")
                            print(f"Capturado: {linha_limpa}")
                    except:
                        continue

        print("Arquivo placares.txt atualizado com os jogos centrais!")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_jogos_aiscore()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Camuflagem anti-bot
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        url = "https://www.aiscore.com/team-zed-fc/63kv9i939ncp7ez"
        print("Acessando página do ZED FC...")
        driver.get(url)
        
        # 1. Rola a página para baixo para carregar a lista de jogos
        time.sleep(10)
        driver.execute_script("window.scrollTo(0, 800);")
        print("Rolando página para carregar agenda...")
        time.sleep(30) # Espera o carregamento dos dados dinâmicos

        with open("placares.txt", "w", encoding="utf-8") as f:
            # 2. Busca todos os itens que parecem ser jogos (cards de partida)
            # No AiScore, os jogos na página do time costumam usar a classe 'match-item'
            jogos = driver.find_elements(By.CSS_SELECTOR, ".match-item, .match-list-item, [class*='match-item']")
            
            if not jogos:
                f.write("Agenda ou jogo ao vivo não carregou. Tentando captura de texto ampla...\n")
                # Plano B: Pega todo o texto da área de partidas
                try:
                    area_jogos = driver.find_element(By.XPATH, "//div[contains(@class, 'match-list')]").text
                    f.write(area_jogos)
                except:
                    f.write("Não foi possível encontrar a seção de partidas.")
            else:
                f.write(f"=== JOGOS E AGENDA ENCONTRADOS ({time.strftime('%H:%M:%S')}) ===\n\n")
                for jogo in jogos:
                    texto = jogo.text.strip().replace("\n", " | ")
                    # Filtra para evitar pegar menus laterais, foca em quem tem 'vs' ou números
                    if len(texto) > 10:
                        f.write(texto + "\n")
                        print(f"Capturado: {texto}")

        print("Finalizado com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_agenda_e_ao_vivo()
