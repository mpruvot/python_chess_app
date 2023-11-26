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
            players_data = r.json()["data"]
            return [Player(**player["attributes"]) for player in players_data]
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
        if new_player.name.capitalize() in [
            i.name.capitalize() for i in self.get_players_from_db()
        ]:
            raise NameAlreadyExistsError("A player with this name already exists !")

        try:
            new_player_json = json.loads(new_player.model_dump_json())
            payload = json.dumps({"data": new_player_json})
            r = requests.post(
                f"{self.API_URL}/players",
                headers={"Content-Type": "application/json"},
                data=payload,
            )
            r.raise_for_status()
            return Player(**r.json()["data"]["attributes"])
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError(
                f"Failed to store player in database: {err}"
            )

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
            payload = json.dumps({"data": new_game_json})
            r = requests.post(
                f"{self.API_URL}/games",
                headers={"Content-Type": "application/json"},
                data=payload,
            )
            r.raise_for_status()
            return Game(**r.json()["data"]["attributes"])
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError(
                f"Failed to store game in database: {err}"
            )

    def get_games_from_db(self) -> List[Game]:
        """
        Retrieve a list of all games stored in the database.

        Raises:
            GameNotFoundError: If no games are found in the database.
        """
        try:
            r = requests.get(f"{self.API_URL}/games")
            r.raise_for_status()
            games_data = r.json()["data"]
            if not games_data:
                raise GameNotFoundError("No games found in the database.")
            return [Game(**game["attributes"]) for game in games_data]

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
            if not games["data"]:
                raise GameNotFoundError(f"Game with UUID {game_uuid} not found.")
            return Game(**games["data"][0]["attributes"])

        except requests.exceptions.HTTPError as err:
            raise GameNotFoundError(
                f"Game with UUID {game_uuid} not found. HTTP error: {err}"
            )

    def get_strapi_game_id(self, game_uuid: str) -> int:
        """
        Retrieve the Strapi ID of a Game.
        Args:
            game_uuid (str): The UUID of the game.
        Raises:
            GameNotFoundError: If the game with the given UUID is not found.
        """
        url = f"{self.API_URL}/games?filters[game_uuid][$eq]={game_uuid}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            id = response.json()["data"][0].get("id")
            return id
        except requests.exceptions.HTTPError as err:
            raise GameNotFoundError(
                f"Game with UUID {game_uuid} not found. HTTP error: {err}"
            )

    def get_strapi_player_id(self, player_name: str):
        """
        Retrieve the Strapi ID of a Player.
        Args:
            player_name (str): The UUID of the Player.
        Raises:
            PlayerNotFoundError: If the Player with the given namm is not found.
        """
        url = f"{self.API_URL}/players?filters[name][$eq]={player_name.capitalize()}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            print (response.json())
            id = response.json()["data"][0].get("id")
            return id
        except requests.exceptions.HTTPError as err:
            raise PlayernotFoundError(f"Player with name {player_name} not found !")

    def update_game_with_new_player(self, player: Player, game: Game) -> Game:
        """
        Update a game with a new player.
        Args:
            player (Player): The player to add to the game.
            game (Game): The game to be updated.
        Raises:
            HTTPError: If there is an HTTP error during the request.
        """
        if player in game.players:
            raise PlayerAlreadyInGameError(
                f"Player {player.name} with uuid : {player.player_uuid} already join this game ! "
            )

        if len(game.players) == 2:
            raise GameIsFullError("Already two players in the game !")

        game_id = self.get_strapi_game_id(str(game.game_uuid))
        url = f"{self.API_URL}/games/{game_id}"

        game.players.append(player)
        game_data_json = json.loads(game.model_dump_json())
        payload = json.dumps({"data": game_data_json})

        try:
            response = requests.put(
                url, headers={"Content-Type": "application/json"}, data=payload
            )
            response.raise_for_status()
            updated_game_data = response.json()["data"]["attributes"]
            return Game(**updated_game_data)
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError(f"HTTP error occurred: {err}")

    def update_fen_of_game(self, game: Game, fen: str) -> Game:
        game_id = self.get_strapi_game_id(str(game.game_uuid))
        url = f"{self.API_URL}/games/{game_id}"
        
        game.fen = fen
        game_data_json = json.loads(game.model_dump_json())
        payload = json.dumps({"data": game_data_json})
        
        try:
            response = requests.put(
                url, headers={"Content-Type": "application/json"}, data=payload
            )
            response.raise_for_status()
            updated_game_data = response.json()["data"]["attributes"]
            return Game(**updated_game_data)
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError(f"HTTP error occurred: {err}")
        
    def delete_player_from_db(self, player_name: str):
        """
        Delete a player from the database by their name.
        Args:
            player_name (str): The name of the player to be deleted.
        Returns:
            The content of the response from the DELETE request if successful.
        Raises:
            PlayernotFoundError: If the player with the given name cannot be found or if there is an HTTP error during the deletion process, indicating that the player could not be deleted.
        """
        player_strpi_id = self.get_strapi_player_id(player_name)
        try:
            r = requests.delete(f"{self.API_URL}/players/{player_strpi_id}")
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as err:
            raise PlayernotFoundError(
                f"Player {player_name} not found and canno't be deleted. HTTP error: {err}"
            )
    
    def delete_game_from_db(self, game_uuid: str):
        """
        Delete a game from the database by its UUID.
        Args:
            game_uuid (str): The UUID of the game to be deleted.
        Returns:
            The content of the response from the DELETE request if successful.
        Raises:
            GameNotFoundError: If the game with the given UUID cannot be found or if there is an HTTP error during the deletion process, indicating that the game could not be deleted.
        """
        game_strapi_id = self.get_strapi_game_id(game_uuid)
        try:
            response = requests.delete(f'{self.API_URL}/games/{game_strapi_id}')
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            raise GameNotFoundError(f'Game with UUID {game_uuid} not found and cannot be deleted. HTTP error: {err}')