import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair_narracao_bruta():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Link do jogo do Internacional no GE
        driver.get("https://ge.globo.com/rs/futebol/campeonato-gaucho/jogo/21-01-2026/internacional-inter-sm.ghtml")
        
        # Espera o carregamento do conteúdo dinâmico (35 segundos)
        time.sleep(35)

        # 1. CAPTURA O PLACAR E TEMPO NO TOPO
        try:
            p_casa = driver.find_element(By.CLASS_NAME, "placar-jogo__equipe--placar").text
            p_fora = driver.find_elements(By.CLASS_NAME, "placar-jogo__equipe--placar")[1].text
            tempo = driver.find_element(By.CLASS_NAME, "placar-jogo__periodo").text.replace("\n", " ")
        except:
            p_casa, p_fora, tempo = "0", "0", "Ao Vivo"

        # 2. CAPTURA O LANCE MAIS RECENTE (Narração)
        # O GE usa classes como 'feed-post-body' ou 'tipo-lance'
        try:
            # Pega o texto do lance mais recente no topo do feed
            lances = driver.find_elements(By.CSS_SELECTOR, ".feed-post-body, .live-feed__item, .content-publication")
            ultimo_lance = lances[0].text.replace("\n", " ").strip() if lances else "Sem comentários recentes."
        except:
            ultimo_lance = "Não foi possível carregar a narração."

        # FORMATAÇÃO DO RESULTADO BRUTO
        resumo = f"INTERNACIONAL {p_casa} X {p_fora} INTER-SM | {tempo}"
        comentario = f"LANCE: {ultimo_lance}"
        
        final = f"{resumo}\n{comentario}"

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(final)
            
        print(f"Dados salvos:\n{final}")

    except Exception as e:
        print(f"Erro no Scraper: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_narracao_bruta()
