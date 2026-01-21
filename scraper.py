import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def rodar_scraper():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # O teu link atual
        driver.get("https://www.aiscore.com/team-cd-fas-reserves/edq09ip2z4i4qxg")
        time.sleep(45) 

        # Captura tudo o que for jogo ou item (a tua lógica que funciona)
        elementos = driver.find_elements(By.XPATH, "//div[contains(@class, 'match')] | //div[contains(@class, 'item')]")
        
        with open("placares.txt", "w", encoding="utf-8") as f:
            for el in elementos:
                txt = el.text.strip().replace("\n", " ")
                if len(txt) > 10:
                    f.write(txt + "\n")
                    
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    rodar_scraper()
