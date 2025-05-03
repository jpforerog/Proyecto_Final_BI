import requests

API_BASE = "http://localhost:8000"

def get_players():
    try:
        response = requests.get(f"{API_BASE}/jugadores/")
        return response.json().get("jugadores_ids", [])
    except Exception as e:
        
        return response.json({"Error al obtener jugadores",str(e)})

def get_performance(player_id: str):
    try:
        response = requests.get(f"{API_BASE}/partidos/rendimiento/{player_id}")
        return response.json() if response.ok else None
    except Exception as e:
        
        return response.json({"Error al obtener rendimiento",str(e)})