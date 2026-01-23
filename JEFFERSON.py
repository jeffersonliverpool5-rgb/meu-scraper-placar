import requests
import os

# Configurações
URL_API = "https://api.aiscore.com/v1/web/api/match/detail?match_id=9gklzi16gjpim7x"
ARQUIVO = "placares.txt"

def buscar_placar():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(URL_API, headers=headers, timeout=10)
        data = response.json()

        # Extração dos dados baseada na estrutura da API do AiScore
        match_data = data.get('data', {})
        home_score = match_data.get('home_score', 0)
        away_score = match_data.get('away_score', 0)
        home_name = match_data.get('home_team_name', 'Home')
        away_name = match_data.get('away_team_name', 'Away')
        status = match_data.get('status_name', 'N/A')

        resultado = f"{home_name} {home_score} x {away_score} {away_name} ({status})"
        
        # Salva no arquivo
        with open(ARQUIVO, "a", encoding="utf-8") as f:
            f.write(resultado + "\n")
        
        print(f"Sucesso: {resultado}")

    except Exception as e:
        print(f"Erro ao buscar dados: {e}")

if __name__ == "__main__":
    buscar_placar()
