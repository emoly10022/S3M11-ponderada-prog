import pytest
import requests
from unittest.mock import patch, MagicMock
from data_ingestion.ingest import fetch_pokemon_data, ingest_pokemon_to_supabase
from data_ingestion.exceptions import DataIngestionException

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon?offset=0&limit=151"

def test_fetch_pokemon_data_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
            {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"}
        ]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_response):
        data = fetch_pokemon_data()
        assert len(data) == 2
        assert data[0]["name"] == "bulbasaur"
        assert data[1]["name"] == "ivysaur"

def test_fetch_pokemon_data_failure():
    with patch("requests.get", side_effect=requests.RequestException("Error")):
        with pytest.raises(DataIngestionException, match="Erro ao buscar dados da PokeAPI: Error"):
            fetch_pokemon_data()

@patch("data_ingestion.ingest.fetch_pokemon_data")
@patch("data_ingestion.ingest.get_supabase_client")
def test_ingest_pokemon_to_supabase_success(mock_get_supabase_client, mock_fetch_pokemon_data):
    mock_fetch_pokemon_data.return_value = [
        {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
        {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"}
    ]

    mock_client = MagicMock()
    mock_client.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
    mock_get_supabase_client.return_value = mock_client

    ingest_pokemon_to_supabase()
    assert mock_client.table("pokemon").insert.call_count == 2

@patch("data_ingestion.ingest.fetch_pokemon_data")
@patch("data_ingestion.ingest.get_supabase_client")
def test_ingest_pokemon_to_supabase_failure(mock_get_supabase_client, mock_fetch_pokemon_data):
    mock_fetch_pokemon_data.return_value = [
        {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"}
    ]

    mock_client = MagicMock()
    mock_client.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[])
    mock_get_supabase_client.return_value = mock_client

    with pytest.raises(DataIngestionException, match="Erro ao inserir dados:"):
        ingest_pokemon_to_supabase()