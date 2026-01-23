from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurações do Chrome (Modo Headless para rodar no GitHub Actions/Servidor)
chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inicializa o Driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.aiscore.com/match-south-island-united-fc-vanuatu-united-fc/9gklzi16gjpim7x"

try:
    driver.get(url)
    
    # Espera até que o nome de um dos times esteja visível (máximo 10 segundos)
    wait = WebDriverWait(driver, 10)
    
    # Capturando nomes dos times
    # No AiScore, os nomes costumam estar em elementos com a classe 'home-name' e 'away-name'
    home_team = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "home-name"))).text
    away_team = driver.find_element(By.CLASS_NAME, "away-name").text
    
    # Capturando placares
    # Geralmente ficam em spans ou divs com classes como 'score' ou dentro de um container central
    home_score = driver.find_element(By.CLASS_NAME, "home-score").text
    away_score = driver.find_element(By.CLASS_NAME, "away-score").text

    print(f"Partida: {home_team} vs {away_team}")
    print(f"Placar: {home_score} - {away_score}")

    # Lógica para salvar no seu arquivo placares.txt
    with open("placares.txt", "a", encoding="utf-8") as f:
        f.write(f"{home_team} {home_score} x {away_score} {away_team}\n")

except Exception as e:
    print(f"Erro ao buscar dados: {e}")

finally:
    driver.quit()
