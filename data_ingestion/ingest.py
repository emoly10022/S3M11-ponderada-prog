import requests
from .supabase_client import get_supabase_client
from .exceptions import DataIngestionException

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon?offset=0&limit=1304"

def fetch_pokemon_data():
    try:
        response = requests.get(POKEAPI_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        raise DataIngestionException(f"Erro ao buscar dados da PokeAPI: {str(e)}")

def ingest_pokemon_to_supabase():
    client = get_supabase_client()
    pokemons = fetch_pokemon_data()

    for pokemon in pokemons:
        data = {
            "name": pokemon["name"],
            "url": pokemon["url"]
        }
        response = client.table("pokemon").insert(data).execute()

        if response.get("status_code", 200) >= 400:
            raise DataIngestionException(f"Erro ao inserir dados: {response}")

    print(f"{len(pokemons)} Pokémons inseridos na tabela 'pokemon' com sucesso!")