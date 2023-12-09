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
    
    @staticmethod
    def _check_full_game(game: Game) -> bool:
         return game.white_player is not None and game.black_player is not None
     
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
                raise PlayernotFoundError("No players found in the database.")
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

    def _add_game_to_player_active_games(self, player: Player, game: Game) -> Player:
        """
        Add a game to a player's list of active games in the database.

        Args:
            player (Player): The player to update.
            game_id (int): The ID of the game to add to the player's active games list.

        Returns:
            Player: The updated player object with the modified active games list.

        Raises:
            PlayerAlreadyInGameError: If the player is already in the specified game.
            requests.exceptions.HTTPError: If an HTTP error occurs during the API request.
        """
        if game.game_id in player.active_games:
            raise PlayerAlreadyInGameError(
                f"Player {player.name} already in game with ID: {game.game_id}"
            )

        player.active_games.append(game.game_id)

        player_data_json = json.loads(player.model_dump_json())
        payload = json.dumps({"data": player_data_json})

        response = requests.put(
            f"{self.API_URL}/players/{player.player_id}",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        response.raise_for_status()
        updated_player_data = response.json()["data"]
        return self._convert_json_to_player_object(updated_player_data)

    def add_player_to_game(self, player: Player, game: Game) -> Game:
        """
        Add a player to a game in the database.

        Args:
            player (Player): The player to add to the game.
            game (Game): The game to which the player is to be added.

        Returns:
            Game: The updated game object with the new player added.

        Raises:
            GameIsFullError: If the game cannot accommodate more players.
            requests.exceptions.HTTPError: If an HTTP error occurs during the API request.
        """
        # Check if the game can accommodate more players
        if self._check_full_game(game):
            raise GameIsFullError(f"Game with ID {game.game_id} is already full.")

        if not game.white_player:
            game.white_player = player
        elif not game.black_player:
            game.black_player = player
        
        if self._check_full_game(game):
            game.is_active = True
        
        self._add_game_to_player_active_games(player, game)
        

        game_data_json = json.loads(game.model_dump_json())
        payload = json.dumps({"data": game_data_json})

        response = requests.put(
            f"{self.API_URL}/games/{game.game_id}",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        response.raise_for_status()
        updated_game_data = response.json()["data"]
        return self._convert_json_to_game_object(updated_game_data)

    def update_fen_of_game(self, game: Game, fen: str) -> Game:
        pass

    ## Delete Methods

    def delete_player(self, name: str) -> None:
        """
        Delete a player by name from the database.

        Args:
            name (str): The name of the player to delete.

        Raises:
            PlayernotFoundError: If no player with the specified name is found in the database.
            requests.exceptions.HTTPError: If an HTTP error occurs during the API request.
        """
        try:
            player = self.get_single_player(name)
            if not player:
                raise PlayernotFoundError(f"No player with name {name} found")
            response = requests.delete(f"{self.API_URL}/players/{player.player_id}")
            response.raise_for_status()

        except requests.exceptions.HTTPError as err:
            raise err

    def delete_game(self, game_id: int) -> None:
        """
        Delete a game by its ID from the database.

        Args:
            game_id (int): The ID of the game to delete.

        Raises:
            GameNotFoundError: If no game with the specified ID is found in the database.
            requests.exceptions.HTTPError: If an HTTP error occurs during the API request.
        """
        try:
            response = requests.delete(f"{self.API_URL}/games/{game_id}")
            if response.status_code == 404:
                raise GameNotFoundError(f"No game with ID {game_id} found")
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err
