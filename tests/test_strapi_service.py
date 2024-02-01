import pytest
from unittest.mock import patch

import requests
from custom_errors.custom_errors import PlayernotFoundError
from services.strapi_service import StrapiApiService


@patch("services.strapi_service.requests.get")
def test_get_single_player(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "data": [
            {
                "id": 1,
                "attributes": {
                    "createdAt": "2023-12-18T12:49:19.951Z",
                    "updatedAt": "2023-12-18T19:51:51.509Z",
                    "publishedAt": "2023-12-18T12:49:19.944Z",
                    "name": "Marius",
                    "rank": None,
                    "friends": [],
                    "active_games": [3, 4],
                },
            }
        ],
        "meta": {"pagination": {"page": 1, "pageSize": 25, "pageCount": 1, "total": 1}},
    }
    service = StrapiApiService()
    player = service.get_single_player("Marius")
    mock_get.assert_called_once_with("http://localhost:1337/api/players?filters[name][$eq]=Marius")
    
    assert player.name == "Marius"
    assert player.player_id == 1
    assert player.active_games == [3, 4]
    
@patch("services.strapi_service.requests.get")
def test_get_single_player_no_player_found(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": []}  # Aucun joueur trouvé

    service = StrapiApiService()

    with pytest.raises(PlayernotFoundError):
        service.get_single_player("Random")


@patch("services.strapi_service.requests.get")
def test_get_single_player_http_error(mock_get):
    mock_get.side_effect = requests.exceptions.HTTPError("Error HTTP")

    service = StrapiApiService()

    with pytest.raises(requests.exceptions.HTTPError):
        service.get_single_player("Random")