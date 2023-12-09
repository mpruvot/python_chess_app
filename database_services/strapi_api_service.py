import json
from typing import List, Dict, Any
import requests
from custom_errors.custom_errors import (
    GameIsFullError,
    GameNotFoundError,
    NameAlreadyExistsError,
    PlayerAlreadyInGameError,
    PlayernotFoundError,
)
from schemas.chess_schemas import Game, Player


class StrapiApiService:
    API_URL = "http://localhost:1337/api"
    FILTER_PLAYER_BY_NAME = "/players?filters[name][$eq]="

    def __init__(self) -> None:
        """Initialize the Strapi API service."""
        pass

    def _convert_json_to_player_object(self, response_data: Dict[str, Any]) -> Player:
        """Converts player JSON data to a Player object."""
        player_attributes = response_data["attributes"]
        player_id = response_data["id"]
        player = Player(**player_attributes)
        player.player_id = player_id
        return player

    def _convert_json_to_game_object(self, response_data: Dict[str, Any]) -> Game:
        """Converts game JSON data to a Game object."""
        game_attributes = response_data["attributes"]
        game_id = response_data["id"]
        game = Game(**game_attributes)
        game.game_id = game_id
        return game

    ## Get Methods

    def get_players(self) -> List[Player]:
        """
        Retrieve a list of all players stored in the database.

        Raises:
            PlayernotFoundError: If no players are found in the database.
        """
        try:
            response = requests.get(f"{self.API_URL}/players")
            response.raise_for_status()
            players_json = response.json()["data"]
            if not players_json:
                raise GameNotFoundError("No games found in the database.")
            return [
                self._convert_json_to_player_object(player) for player in players_json
            ]
        except requests.exceptions.HTTPError:
            raise PlayernotFoundError("No players found in the database.")

    def get_single_player(self, name: str) -> Player:
        """
        Retrieve a single player by name from the database.

        Args:
            name (str): The name of the player to retrieve.

        Returns:
            Player: An object representing the player's data if found.

        Raises:
            PlayernotFoundError: If no player with the specified name is found in the database.
            requests.exceptions.HTTPError: If an HTTP error occurs during the API request.
        """
        try:
            response = requests.get(f"{self.API_URL}{self.FILTER_PLAYER_BY_NAME}{name}")
            response.raise_for_status()
            player_json = response.json()["data"]
            if not player_json:
                raise PlayernotFoundError("No player with this name")
            return self._convert_json_to_player_object(player_json[0])
        except requests.exceptions.HTTPError as err:
            raise err

    def get_games(self) -> List[Game]:
        """Retrieve a list of all games stored in the database."""
        try:
            response = requests.get(f"{self.API_URL}/games")
            response.raise_for_status()
            games_json = response.json()["data"]
            if not games_json:
                raise GameNotFoundError("No games found in the database.")
            return [self._convert_json_to_game_object(game) for game in games_json]
        except requests.exceptions.HTTPError as err:
            raise err

    def get_single_game(self, game_id: int) -> Game:
        """
        Retrieve a single game by its ID from the database.

        Args:
            game_id (int): The ID of the game to retrieve.

        Returns:
            Game: An object representing the game's data if found.

        Raises:
            GameNotFoundError: If no game with the specified ID is found in the database.
            requests.exceptions.HTTPError: If an HTTP error occurs during the API request.
        """
        try:
            response = requests.get(f"{self.API_URL}/games/{game_id}")
            if response.status_code == 404:
                raise GameNotFoundError(f"No game with ID {game_id} found")
            response.raise_for_status()
            game_json = response.json()["data"]
            return self._convert_json_to_game_object(game_json)
        except requests.exceptions.HTTPError as err:
            raise err

    ## Post Methods
    
    def post_players(self, new_player: Player) -> Player:
        """
        Store a new player instance in the database.

        Args:
            new_player (Player): The player instance to store.

        Returns:
            Player: The stored player object with updated data from the database.

        Raises:
            NameAlreadyExistsError: If a player with the same name already exists.
            HTTPError: If an HTTP error occurs during the request.
        """
        try:
            new_player_json = json.loads(new_player.model_dump_json())
            payload = json.dumps({"data": new_player_json})
            response = requests.post(
                f"{self.API_URL}/players",
                headers={"Content-Type": "application/json"},
                data=payload,
            )
            response.raise_for_status()
            player_json = response.json()["data"]
            return self._convert_json_to_player_object(player_json)
        except requests.exceptions.HTTPError as err:
            raise NameAlreadyExistsError(
                f"A player with this Name already exists : {err}"
            )

    def post_games(self, new_game: Game) -> Game:
        """Store a new game instance in the database."""
        try:
            new_game_json = json.loads(new_game.model_dump_json())
            payload = json.dumps({"data": new_game_json})
            response = requests.post(
                f"{self.API_URL}/games",
                headers={"Content-Type": "application/json"},
                data=payload,
            )
            response.raise_for_status()
            return self._convert_json_to_game_object(response.json()["data"])
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError(
                f"Failed to store game in database: {err}"
            )

    ## Put Methods

    def update_player_active_games(self, player: Player, game: Game = None) -> Player:
        if game in player.active_games:
            raise PlayerAlreadyInGameError(
                f"Player {player.name} with uuid : {player.player_uuid} already join this game ! "
            )
        player_id = self.get_strapi_player_id(player_name=player.name)
        url = f"{self.API_URL}/players/{player_id}"
        if game:
            player.active_games.append(game.game_uuid)

        player_data_json = json.loads(player.model_dump_json())
        payload = json.dumps({"data": player_data_json})

        try:
            response = requests.put(
                url, headers={"Content-Type": "application/json"}, data=payload
            )
            response.raise_for_status()
            updated_player_data = response.json()["data"]["attributes"]
            return Player(**updated_player_data)
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError(f"HTTP error occurred: {err}")

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
        updated_player = self.update_player_active_games(player, game)

        game.players.append(updated_player)
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
        """
        Updates the FEN of a game instance.
        Args:
            game (Game): The game to be updated.
            fen (str): The FEN string to update the game with.
        Returns:
            Game: The updated game instance.
        Raises:
            HTTPError: If there is an HTTP error during the request.
        """
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
            response = requests.delete(f"{self.API_URL}/games/{game_strapi_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            raise GameNotFoundError(
                f"Game with UUID {game_uuid} not found and cannot be deleted. HTTP error: {err}"
            )
