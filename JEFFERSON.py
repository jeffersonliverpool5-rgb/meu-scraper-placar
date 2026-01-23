import requests
import subprocess
import os
from datetime import datetime

# Link direto da API do jogo informado
URL_API = "https://api.aiscore.com/v1/web/api/match/detail?match_id=9gklzi16gjpim7x"
ARQUIVO = "placares.txt"

def atualizar():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # 1. Pega os dados da API
        response = requests.get(URL_API, headers=headers, timeout=15)
        data = response.json().get('data', {})
        
        home = data.get('home_score', 0)
        away = data.get('away_score', 0)
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # O segredo: colocar o horário garante que o arquivo sempre mude
        conteudo = f"HOME {home} x {away} AWAY | Ultima atualizacao: {agora}"

        # 2. Escreve no arquivo (sobrescrevendo o anterior)
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            f.write(conteudo)
        
        print(f"Placar capturado: {home}x{away}")

        # 3. Comandos Git - Forçando o Push
        # 'cd' para a pasta do script antes de rodar os comandos
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        subprocess.run(["git", "add", ARQUIVO], check=True)
        # Commit com a hora para não dar erro de "nada para commitar"
        subprocess.run(["git", "commit", "-m", f"Placar {home}x{away} em {agora}"], check=True)
        subprocess.run(["git", "push"], check=True)
        
        print(">>> ATUALIZADO NO GITHUB COM SUCESSO!")

    except Exception as e:
        print(f">>> ERRO: {e}")

if __name__ == "__main__":
    atualizar()
