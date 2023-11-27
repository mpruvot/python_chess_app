from schemas.chess_schemas import Game, Player
from chess_app.chess_engine import *
from custom_errors.custom_errors import *
from database_services.strapi_api_service import StrapiApiService
from typing import Optional, List
from services.chess_engine_services import *
from services.player_services import *


api_service = StrapiApiService()


def create_game() -> Game:
    """
    Create a new Game instance and store it in the database.
    Returns:
        Game: The newly created Game instance.
    """
    game = Game()
    return api_service.store_game_in_db(game)


def retrieve_all_games() -> Optional[List[Game]]:
    """
    Retrieve a list of all the games from the database.
    Returns:
        List[Game]: A list of Game instances.
    Raises:
        GameNotFoundError: If no games are found in the database.
    """
    try:
        return api_service.get_games_from_db()
    except GameNotFoundError:
        raise GameNotFoundError("List of games is empty!")


def retrieve_single_game(game_uuid: str) -> Game:
    """
    Retrieve a game by its UUID from the database.
    Args:
        game_uuid (str): The UUID of the game to retrieve.
    Returns:
        Game: The Game instance with the specified UUID.
    Raises:
        GameNotFoundError: If no game with the specified UUID is found.
    """
    try:
        return api_service.get_single_game(game_uuid)
    except GameNotFoundError:
        raise GameNotFoundError(f"No game found with UUID: {game_uuid}")


def add_player_in_game(game_uuid: str, player_name: str) -> Game:
    """
    Allows a Player to join an active game which is not already full.
    Args:
        game_uuid (str): The UUID of the game to join.
        player_name (str): The name of the player joining the game.
    Returns:
        Game: The updated Game instance after adding the player.
    Raises:
        PlayerNotFoundError: If the player with the specified name is not found.
        GameNotFoundError: If the game with the specified UUID is not found.
        PlayerAlreadyInGameError : If the player already joined the game.
    """
    game = retrieve_single_game(game_uuid)
    player = get_single_player(player_name)
    updated_game = api_service.update_game_with_new_player(player, game)
    return updated_game


def create_and_join_game(player_name: str):
    """
    Creates a new game and adds a player to it.

    Args:
        player_name (str): The name of the player joining the new game.

    Returns:
        The updated game instance with the player added.
    """
    player = get_single_player(player_name)
    game = create_game()
    updated_game = api_service.update_game_with_new_player(player, game)
    return updated_game


def search_and_join_game(player_name: str):
    """
    Searches for an available game and adds a player to it.

    Args:
        player_name (str): The name of the player looking to join a game.

    Returns:
        The updated game instance with the player added.

    Raises:
        GameNotFoundError: If no available games are found.
        PlayerAlreadyInGameError: If the player is already in the selected game.
    """
    games = retrieve_all_games()
    available_game = [game for game in games if len(game.players) != 2]
    player = get_single_player(player_name)
    if not available_game:
        raise GameNotFoundError(
            "No game available at the moment, please create a game first."
        )
    if available_game and player in available_game[0]:
        raise PlayerAlreadyInGameError(
            f"Player {player.name} with uuid : {player.player_uuid} already join this game ! Please try to create another Game"
        )
    updated_game = api_service.update_game_with_new_player(player, available_game[0])
    return updated_game
