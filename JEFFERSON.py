import requests
import subprocess
import os
from datetime import datetime

# Configurações
MATCH_ID = "9gklzi16gjpim7x"
URL_API = f"https://api.aiscore.com/v1/web/api/match/detail?match_id={MATCH_ID}"
ARQUIVO = "placares.txt"

def rodar_scraper():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Origin": "https://www.aiscore.com",
        "Referer": "https://www.aiscore.com/"
    }

    try:
        # 1. Busca o placar
        print(f"Tentando acessar API para o jogo {MATCH_ID}...")
        response = requests.get(URL_API, headers=headers, timeout=20)
        response.raise_for_status()
        
        data = response.json().get('data', {})
        
        # Extrai scores (Home e Away)
        home_score = data.get('home_score', '0')
        away_score = data.get('away_score', '0')
        
        # Formata a string do placar
        agora = datetime.now().strftime("%H:%M:%S")
        placar_final = f"{home_score}-{away_score}"
        conteudo_arquivo = f"HOME SCORE: {home_score} AWAY SCORE: {away_score} (Atualizado: {agora})"

        # 2. Escreve no arquivo placares.txt
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            f.write(conteudo_arquivo)
        
        print(f"Arquivo local atualizado: {placar_final}")

        # 3. Comandos Git para atualizar o GitHub
        # Importante: O script precisa estar dentro da pasta do repositório
        subprocess.run(["git", "add", ARQUIVO], check=True)
        # O commit leva a hora para garantir que o GitHub aceite a mudança
        msg_commit = f"Placar {placar_final} as {agora}"
        subprocess.run(["git", "commit", "-m", msg_commit], check=True)
        subprocess.run(["git", "push"], check=True)
        
        print(">>> SUCESSO: Placar enviado para o GitHub!")

    except Exception as e:
        print(f">>> ERRO: {e}")

if __name__ == "__main__":
    rodar_scraper()
