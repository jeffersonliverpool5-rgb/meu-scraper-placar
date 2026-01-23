Vimport requests
import subprocess
import os

# Configurações
URL_API = "https://api.aiscore.com/v1/web/api/match/detail?match_id=9gklzi16gjpim7x"
ARQUIVO = "placares.txt"

def atualizar_github():
    try:
        # 1. Scraping
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL_API, headers=headers, timeout=10)
        data = response.json().get('data', {})
        
        home = data.get('home_score', 0)
        away = data.get('away_score', 0)
        placar_formatado = f"HOME: {home} - AWAY: {away}"

        # 2. Escrever no arquivo (sobrescreve para manter apenas o atual ou 'a' para lista)
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            f.write(placar_formatado)

        # 3. Comandos Git para subir ao GitHub
        subprocess.run(["git", "add", ARQUIVO])
        subprocess.run(["git", "commit", "-m", f"Atualização Placar: {placar_formatado}"])
        subprocess.run(["git", "push"])
        
        print(f"Sucesso: {placar_formatado} enviado ao GitHub.")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    atualizar_github()
