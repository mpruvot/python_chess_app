import requests
import json
from schemas.chess_schemas import Player, Game
from custom_errors.custom_errors import *

class StrapiApiService:
    API_URL = "http://localhost:1337/api"

    def __init__(self) -> None:
        pass

    def get_players_from_db(self) -> json:
        """Return a list of all the players stored in database."""
        try:
            r = requests.get(f"{self.API_URL}/players")
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError:
            raise PlayernotFoundError("List of players is empty!")

    def store_player_in_db(self, new_player: Player) -> json:
        """Store an instance of player object in database."""
        player_data = new_player.model_dump()
        player_data["player_uuid"] = str(player_data["player_uuid"])
        try:
            r = requests.post(
                f"{self.API_URL}/players",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"data": player_data}),
            )
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as err:
            if r.status_code == 400:
                raise NameAlreadyExistsError("A player with this name already exists!")
            else:
                raise err

    def store_game_in_db(self, new_game: Game) -> json:
        """Store an instance of Game object in database."""
        game_data = new_game.model_dump()
        game_data["game_uuid"] = str(game_data["game_uuid"])
        try:
            r = requests.post(
                f"{self.API_URL}/games",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"data": game_data}),
            )
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as err:
            raise err

    def get_games_from_db(self) -> json:
        """Return a list of all the games stored in database."""
        try:
            r = requests.get(f"{self.API_URL}/games")
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError:
            raise GameNotFoundError("List of games is empty!")

    def get_single_game(self, game_uuid: str):
        """Retrieve a single game by UUID."""
        url = f"{self.API_URL}/games?filters[game_uuid][$eq]={game_uuid}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            games = response.json()
            if not games['data']:
                raise GameNotFoundError
            return games['data'][0]
        except requests.exceptions.HTTPError:
            raise GameNotFoundError("Game not found!")

    def get_strapi_game_id(self, game_uuid: str):
        """Retrieve the Strapi ID of a Game."""
        try:
            data = self.get_single_game(game_uuid)
            return data.get('id')
        except requests.exceptions.HTTPError:
            raise GameNotFoundError

    def put_add_player(self, player: str, game_uuid: str):
        """Update an existing game: add a new Player in List[Player]."""
        pass