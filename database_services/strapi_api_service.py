import requests
import json
from schemas.chess_schemas import Player, Game
from custom_errors.custom_errors import *
from typing import List

class StrapiApiService:
    API_URL = "http://localhost:1337/api"

    def __init__(self) -> None:
        """Initialize the Strapi API service."""
        pass

    def get_players_from_db(self) -> List[Player]:
        """
        Retrieve a list of all players stored in the database.
        
        Raises:
            PlayernotFoundError: If no players are found in the database.
        """
        try:
            r = requests.get(f"{self.API_URL}/players")
            r.raise_for_status()
            players_data = r.json()['data']
            return [Player(**player['attributes']) for player in players_data]
        except requests.exceptions.HTTPError:
            raise PlayernotFoundError("No players found in the database.")

    def store_player_in_db(self, new_player: Player) -> Player:
        """
        Store a new player instance in the database.

        Args:
            new_player (Player): The player instance to store.

        Raises:
            NameAlreadyExistsError: If a player with the same name already exists.
            HTTPError: If an HTTP error occurs during the request.
        """
        if new_player.name.capitalize() in [i.name.capitalize() for i in self.get_players_from_db()]:
            raise NameAlreadyExistsError('A player with this name already exists !')
        
        try:
            new_player_json = json.loads(new_player.model_dump_json())
            payload = json.dumps({"data" : new_player_json})
            r = requests.post(f"{self.API_URL}/players", headers={"Content-Type": "application/json"}, data=payload)
            r.raise_for_status()
            return Player(**r.json()['data']['attributes'])
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError(f"Failed to store player in database: {err}")

    def store_game_in_db(self, new_game: Game) -> Game:
        """
        Store a new game instance in the database.

        Args:
            new_game (Game): The game instance to store.

        Raises:
            HTTPError: If an HTTP error occurs during the request.
        """
        try:
            new_game_json = json.loads(new_game.model_dump_json())
            payload = json.dumps({"data" : new_game_json})
            r = requests.post(f"{self.API_URL}/games", headers={"Content-Type": "application/json"}, data=payload)
            r.raise_for_status()
            return Game(**r.json()['data']['attributes'])
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError(f"Failed to store game in database: {err}")

    def get_games_from_db(self) -> List[Game]:
        """
        Retrieve a list of all games stored in the database.

        Raises:
            GameNotFoundError: If no games are found in the database.
        """
        try:
            r = requests.get(f"{self.API_URL}/games")
            r.raise_for_status()
            games_data = r.json()['data']
            return [Game(**game['attributes']) for game in games_data]
        except requests.exceptions.HTTPError:
            raise GameNotFoundError("No games found in the database.")

    def get_single_game(self, game_uuid: str) -> Game:
            """
            Retrieve a single game by UUID and return a Game instance.
            Args:
                game_uuid (str): The UUID of the game to retrieve.
            Raises:
                GameNotFoundError: If the game with the given UUID is not found.
            """
            url = f"{self.API_URL}/games?filters[game_uuid][$eq]={game_uuid}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                games = response.json()
                if not games['data']:
                    raise GameNotFoundError(f"Game with UUID {game_uuid} not found.")
                return Game(**games['data'][0]['attributes'])
            
            except requests.exceptions.HTTPError as err:
                raise GameNotFoundError(f"Game with UUID {game_uuid} not found. HTTP error: {err}")

    def get_strapi_game_id(self, game_uuid: str):
        """
        Retrieve the Strapi ID of a Game.
        Args:
            game_uuid (str): The UUID of the game.
        Raises:
            GameNotFoundError: If the game with the given UUID is not found.
        """
        try:
            data = self.get_single_game(game_uuid)
            return data.get('id')
        except requests.exceptions.HTTPError as err:
            raise GameNotFoundError(f"Game with UUID {game_uuid} not found. HTTP error: {err}")

    def update_game_with_new_player(self, player: Player, game: Game) -> Game:
        """
        Update a game with a new player.
        Args:
            player (Player): The player to add to the game.
            game (Game): The game to be updated.
        Raises:
            HTTPError: If there is an HTTP error during the request.
        """
        game_id = self.get_strapi_game_id(str(game.game_uuid))
        url = f"{self.API_URL}/games/{game_id}"
        
        game.players.append(player)
        game_data_json = json.loads(game.model_dump_json())
        payload = json.dumps({"data" : game_data_json})
        
        try: 
            response = requests.put(
                url,
                headers={"Content-Type": "application/json"},
                data=payload
            )
            response.raise_for_status()
            updated_game_data = response.json()['data']['attributes']
            return Game(**updated_game_data)
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError(f"HTTP error occurred: {err}")
