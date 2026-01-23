from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. Configurações do Navegador
chrome_options = Options()
chrome_options.add_argument("--headless")  # Rode em segundo plano
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# Adicionando um User-Agent para evitar ser bloqueado como bot
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.aiscore.com/match-south-island-united-fc-vanuatu-united-fc/9gklzi16gjpim7x"

try:
    driver.get(url)
    
    # 2. Aguarda até 15 segundos para os elementos aparecerem
    wait = WebDriverWait(driver, 15)
    
    # Seletores atualizados baseados na estrutura do AiScore
    # Buscando pelos nomes dos times
    home_name = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'home-team')]//a[contains(@class, 'name')]"))).text
    away_name = driver.find_element(By.XPATH, "//div[contains(@class, 'away-team')]//a[contains(@class, 'name')]").text
    
    # Buscando o placar (score)
    # O AiScore geralmente coloca o placar dentro de um container centralizado
    home_score = driver.find_element(By.XPATH, "//div[contains(@class, 'score-item')][1]").text
    away_score = driver.find_element(By.XPATH, "//div[contains(@class, 'score-item')][2]").text

    # 3. Formatação da linha
    resultado = f"{home_name} {home_score} - {away_score} {away_name}\n"
    print(f"Dados capturados: {resultado}")

    # 4. Escrita no arquivo (Modo 'a' para adicionar ao final, 'w' para sobrescrever)
    with open("placares.txt", "a", encoding="utf-8") as f:
        f.write(resultado)
        f.flush() # Garante que os dados saiam do buffer para o arquivo
    
    print("Arquivo placares.txt atualizado com sucesso!")

except Exception as e:
    print(f"Erro ao capturar dados: {e}")
    # Caso queira debugar, tire o print abaixo:
    # print(driver.page_source) 

finally:
    driver.quit()
