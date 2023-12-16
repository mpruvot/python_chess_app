import pytest
from fastapi.testclient import TestClient
from api.main import app
from services.strapi_service import StrapiApiService
from schemas.player import Player
from custom_errors.custom_errors import NameAlreadyExistsError, PlayernotFoundError

client = TestClient(app)

@pytest.fixture
def mock_strapi_service(mocker):
    def _mock_service(mock_method: str, response=None, side_effect=None):
        if side_effect:
            mocker.patch.object(StrapiApiService, mock_method, side_effect=side_effect)
        else:
            mocker.patch.object(StrapiApiService, mock_method, return_value=response)
    return _mock_service

class TestPlayersAPI:
    def test_home_page(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Chess API"}
    
    def test_list_players(self, mock_strapi_service):
        mock_players = [Player(name="Player1"), Player(name="Player2")]
        mock_strapi_service("get_players", response=mock_players)
        response = client.get("/players/")
        assert response.status_code == 200
        assert len(response.json()) == 2
    
    def test_error_retrieving_players_from_list_players(self, mock_strapi_service):
        mock_strapi_service("get_players", side_effect=PlayernotFoundError('No players found.'))
        response = client.get("/players/")
        assert response.status_code == 404
        assert "No players found." in response.text
        
    def test_create_new_player_success(self, mock_strapi_service):
        new_player = Player(name="NewPlayer")
        mock_strapi_service("post_players", response=new_player)
        response = client.post("/players/NewPlayer")
        assert response.status_code == 200
        assert response.json()["name"] == "NewPlayer"

    def test_create_new_player_name_exists(self, mock_strapi_service):
        mock_strapi_service("post_players", side_effect=NameAlreadyExistsError("Player already exists"))
        response = client.post("/players/ExistingPlayer")
        assert response.status_code == 403
        assert "Player already exists" in response.text
    
    def test_retrieve_player_success(self, mock_strapi_service):
        existing_player = Player(name="ExistingPlayer")
        mock_strapi_service("get_single_player", response=existing_player)
        response = client.get("/players/ExistingPlayer")
        assert response.status_code == 200
        assert response.json()["name"] == "ExistingPlayer"

    def test_retrieve_player_not_found(self, mock_strapi_service):
        mock_strapi_service("get_single_player", side_effect=PlayernotFoundError("Player not found"))
        response = client.get("/players/NonExistentPlayer")
        assert response.status_code == 404
        assert "Player not found" in response.text
        
    def test_delete_player_success(self, mock_strapi_service):
        mock_strapi_service("delete_player", response=None)  
        response = client.delete("/players/ExistingPlayer")
        assert response.status_code == 200

    def test_delete_player_not_found(self, mock_strapi_service):
        mock_strapi_service("delete_player", side_effect=PlayernotFoundError("Player not found"))
        response = client.delete("/players/NonExistentPlayer")
        assert response.status_code == 404
        assert "Player not found" in response.text