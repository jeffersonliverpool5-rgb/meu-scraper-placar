import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair_aiscore():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://www.aiscore.com/match-instituto-de-cordoba-velez-sarsfield/vrqwni43wdgu4qn"
        driver.get(url)
        
        # Espera o carregamento dos dados reais
        time.sleep(15)

        # 1. Busca os nomes dos times
        time_casa = driver.find_element(By.CSS_SELECTOR, ".home-team .name").text.strip()
        time_fora = driver.find_element(By.CSS_SELECTOR, ".away-team .name").text.strip()

        # 2. Busca o Placar e o Tempo dentro do container 'match-score'
        # Usamos execução de script para garantir que pegamos o valor exato entre as tags ><
        dados_placar = driver.execute_script("""
            let container = document.querySelector('.match-score');
            if (!container) return {g1: "0", g2: "0", tempo: "0"};
            
            // Busca os elementos de score e tempo dentro do container match-score
            let hScore = container.querySelector('.home-score')?.innerText || "0";
            let aScore = container.querySelector('.away-score')?.innerText || "0";
            let tempo = container.querySelector('.time-score')?.innerText || "0";
            
            return {g1: hScore, g2: aScore, tempo: tempo};
        """)

        g1 = dados_placar['g1']
        g2 = dados_placar['g2']
        tempo_val = dados_placar['tempo']

        # MONTAGEM DA LINHA FINAL
        resultado = f"{time_casa} {g1} X {g2} {time_fora} | {tempo_val}"
        resultado = " ".join(resultado.split())

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            
        print(f"CAPTURA OK: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair_aiscore()
