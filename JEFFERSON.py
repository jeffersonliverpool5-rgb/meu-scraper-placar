import requests
import subprocess
import os

# Link da API interna para evitar bloqueio de HTML
URL_API = "https://api.aiscore.com/v1/web/api/match/detail?match_id=9gklzi16gjpim7x"
ARQUIVO = "placares.txt"

def atualizar_placar():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.aiscore.com/"
    }

    try:
        # Busca os dados
        response = requests.get(URL_API, headers=headers, timeout=15)
        response.raise_for_status() # Gera erro se o site bloquear
        
        data = response.json().get('data', {})
        
        home_score = data.get('home_score', '0')
        away_score = data.get('away_score', '0')
        placar_final = f"{home_score}-{away_score}"

        # Salva no arquivo local
        with open(ARQUIVO, "w") as f:
            f.write(placar_final)
        
        print(f"Placar local atualizado: {placar_final}")

        # Envia para o GitHub
        enviar_ao_github(placar_final)

    except Exception as e:
        print(f"ERRO NO PROCESSO: {e}")

def enviar_ao_github(placar):
    try:
        # Executa comandos git
        subprocess.run(["git", "add", ARQUIVO], check=True)
        subprocess.run(["git", "commit", "-m", f"Update score {placar}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("GitHub atualizado com sucesso!")
    except Exception as e:
        print(f"ERRO AO SUBIR PARA GITHUB: {e} - Verifique se você está logado no Git.")

if __name__ == "__main__":
    atualizar_placar()
