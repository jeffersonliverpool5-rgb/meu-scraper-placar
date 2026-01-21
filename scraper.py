import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair_lance_a_lance():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Link do jogo Internacional x Inter-SM
        driver.get("https://ge.globo.com/rs/futebol/campeonato-gaucho/jogo/21-01-2026/internacional-inter-sm.ghtml")
        
        # Espera o feed de lances carregar
        time.sleep(25)

        # 1. PEGAR O PLACAR E TEMPO (Resumo)
        try:
            gols = driver.find_elements(By.CLASS_NAME, "placar-jogo__equipe--placar")
            tempo_el = driver.find_element(By.CLASS_NAME, "placar-jogo__periodo")
            placar_resumo = f"INT {gols[0].text} X {gols[1].text} ISM | {tempo_el.text.replace('\n', ' ')}"
        except:
            placar_resumo = "Placar indisponível"

        # 2. PEGAR O ÚLTIMO LANCE NARRADO
        # No GE, os lances ficam em itens de feed. Vamos pegar o texto do lance mais recente.
        try:
            # Busca o texto do primeiro lance que aparece na lista de tempo real
            ultimo_lance_el = driver.find_element(By.CSS_SELECTOR, ".feed-post-body, .live-feed__item")
            texto_lance = ultimo_lance_el.text.replace("\n", " ").strip()
        except:
            texto_lance = "Aguardando novos lances..."

        # MONTAGEM FINAL DO TEXTO BRUTO
        resultado = f"{placar_resumo}\nLANCE: {texto_lance}"
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"Dados Capturados:\n{resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_lance_a_lance()
