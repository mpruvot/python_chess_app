import pytest
from fastapi.testclient import TestClient
from api.main import app
from services.strapi_service import StrapiApiService
from schemas.game import Game
from custom_errors.custom_errors import GameIsFullError, GameNotFoundError, PlayerAlreadyInGameError, PlayernotFoundError

client = TestClient(app)

@pytest.fixture
def mock_strapi_service(mocker):
    def _mock_service(mock_method: str, response=None, side_effect=None):
        if side_effect:
            mocker.patch.object(StrapiApiService, mock_method, side_effect=side_effect)
        else:
            mocker.patch.object(StrapiApiService, mock_method, return_value=response)
    return _mock_service

class TestGameAPI:
    def test_new_game_success(self, mock_strapi_service):
        new_game = Game()
        mock_strapi_service("post_games", response=new_game)
        response = client.post("/games/")
        assert response.status_code == 200
        assert response.json()['is_active'] == False
        assert isinstance(response.json(), dict)  

    def test_join_game_success(self, mock_strapi_service):
        updated_game = Game()
        mock_strapi_service("add_player_to_game", response=updated_game)
        response = client.patch("/games/1/PlayerName")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_join_game_full(self, mock_strapi_service):
        mock_strapi_service("add_player_to_game", side_effect=GameIsFullError("Game is full"))
        response = client.patch("/games/1/PlayerName")
        assert response.status_code == 403
        assert "Game is full" in response.text

    def test_list_games_success(self, mock_strapi_service):
        mock_games = [Game(), Game()]
        mock_strapi_service("get_games", response=mock_games)
        response = client.get("/games/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_list_games_not_found(self, mock_strapi_service):
        mock_strapi_service("get_games", side_effect=GameNotFoundError("No games found"))
        response = client.get("/games/")
        assert response.status_code == 404
        assert "No games found" in response.text

    def test_retrieve_game_success(self, mock_strapi_service):
        game = Game()
        mock_strapi_service("get_single_game", response=game)
        response = client.get("/games/1")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_retrieve_game_not_found(self, mock_strapi_service):
        mock_strapi_service("get_single_game", side_effect=GameNotFoundError("Game not found"))
        response = client.get("/games/999")
        assert response.status_code == 404
        assert "Game not found" in response.text

    def test_delete_game_success(self, mock_strapi_service):
        mock_strapi_service("delete_game", response=None)
        response = client.delete("/games/1")
        assert response.status_code == 200

    def test_delete_game_not_found(self, mock_strapi_service):
        mock_strapi_service("delete_game", side_effect=GameNotFoundError("Game not found"))
        response = client.delete("/games/999")
        assert response.status_code == 404
        assert "Game not found" in response.text
