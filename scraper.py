import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def buscar_posicional():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # LINK DO JOGO
        driver.get("https://www.espn.com.br/futebol/partida/_/jogoId/757771")
        time.sleep(35) # Tempo extra para garantir carga total
        
        # PEGA O TEXTO BRUTO DE TUDO
        linhas = driver.find_element(By.TAG_NAME, "body").text.split('\n')
        
        # FILTRO: Vamos ignorar menus iniciais comuns (até 20 linhas de lixo podem existir)
        # Mas o placar real na ESPN costuma estar entre a linha 5 e 30.
        dados_uteis = []
        for l in linhas[:40]:
            limpa = l.strip()
            # Ignora palavras de menu conhecidas
            if any(x in limpa for x in ["Resultados", "Calendário", "Equipes", "NBA", "NFL", "Champions", "Carioca", "Paulista", "Vídeo"]):
                continue
            if len(limpa) > 0:
                dados_uteis.append(limpa)

        # Na ESPN, a estrutura quase sempre é:
        # Linha X: Time Casa
        # Linha X+1: Placar Casa
        # Linha X+2: Time Visitante
        # Linha X+3: Placar Visitante
        # Linha X+4: Tempo
        
        # Vamos buscar o índice do tempo (ex: 58') para nos guiar
        idx_tempo = -1
        for i, texto in enumerate(dados_uteis):
            if "'" in texto or "HT" in texto or "Fim" in texto or "Intervalo" in texto:
                idx_tempo = i
                break
        
        if idx_tempo != -1:
            # Se achamos o tempo, os times e placares estão logo acima dele
            # Pegamos um bloco de 5 linhas ao redor do tempo
            inicio = max(0, idx_tempo - 4)
            bloco = dados_uteis[inicio:idx_tempo + 1]
            resultado = " ".join(bloco)
        else:
            # Se não achou o minuto, pega as primeiras 10 linhas limpas
            resultado = " | ".join(dados_uteis[:6])

        with open("placares.txt", "w", encoding="utf-8") as f:
            f.write(resultado)
            print(f"Gravado: {resultado}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    buscar_posicional()
