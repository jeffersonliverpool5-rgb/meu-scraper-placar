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
        # Link do time (ajuste para o time que quiser)
        driver.get("https://www.aiscore.com/team-newcastle-united/714x6i6v9y7q29v")
        time.sleep(45) 

        # Captura tudo (a sua técnica que funciona)
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
