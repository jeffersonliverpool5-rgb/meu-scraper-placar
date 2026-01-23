import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extrair_placar_limpo():
    url = "https://www.aiscore.com/match-ca-penarol-boston-river/ndqmliw2oxehrkv"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Recomenda-se iniciar o driver dentro da função ou gerenciar o fechamento corretamente
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        # Espera o conteúdo carregar
        time.sleep(15) 
        
        # 1. Capturar Nomes dos Times
        try:
            nome_casa = driver.find_element(By.CSS_SELECTOR, ".home-team-name, .home-name, .home-team .name").text.strip()
            nome_fora = driver.find_element(By.CSS_SELECTOR, ".away-team-name, .away-name, .away-team .name").text.strip()
        except:
            nome_casa = "CA Penarol
"
            nome_fora = "Boston River"

        # 2. Capturar o Tempo
        cronometro = ""
        try:
            elementos_tempo = driver.find_elements(By.XPATH, "//*[contains(text(), \"'\")]")
            for el in elementos_tempo:
                texto = el.text.strip()
                if "'" in texto and len(texto) <= 5:
                    cronometro = texto
                    break
            if not cronometro:
                cronometro = driver.find_element(By.CSS_SELECTOR, ".match-status, .status-info").text.strip()
        except:
            cronometro = "Ao vivo"

        # 3. Capturar Placares
        try:
            placar_casa = driver.find_element(By.CSS_SELECTOR, ".home-score").text.strip()
            placar_fora = driver.find_element(By.CSS_SELECTOR, ".away-score").text.strip()
        except:
            placar_casa = "0"
            placar_fora = "0"

        resultado = f"[{cronometro}] {nome_casa} {placar_casa} x {placar_fora} {nome_fora}"
        
        # Salva no arquivo limpando o anterior
        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado + "\n")
            
        return resultado

    except Exception as e:
        return f"Erro na captura: {e}"
    finally:
        driver.quit()

if __name__ == "__main__":
    execucoes_totais = 100
    intervalo_segundos = 60  # 1 minuto

    for i in range(1, execucoes_totais + 1):
        print(f"Execução {i}/{execucoes_totais} - {time.strftime('%H:%M:%S')}")
        status = extrair_placar_limpo()
        print(f"Resultado: {status}")
        
        if i < execucoes_totais:
            print(f"Aguardando {intervalo_segundos} segundos para a próxima atualização...")
            time.sleep(intervalo_segundos)

    print("Ciclo de 100 atualizações finalizado.")
