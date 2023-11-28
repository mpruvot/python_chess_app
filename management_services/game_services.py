from database_services.strapi_api_service import StrapiApiService
from schemas.chess_schemas import Game, Player
from custom_errors.custom_errors import *
from typing import Optional, List
from chess_services.chess_engine_services import start_new_game

from management_services.player_services import get_single_player

api_service = StrapiApiService()


def create_game() -> Game:
    """
    Create a new Game instance and store it in the database.
    Returns:
        Game: The newly created Game instance.
    """
    game = Game()
    return api_service.store_game_in_db(game)


def delete_game(game_uuid: str):
    try:
        api_service.delete_game_from_db(game_uuid)
    except GameNotFoundError as err:
        raise err


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

def _update_game_with_player(game: Game, player: Player) -> Game:
    """
    Updates a game instance with a new player and starts the game if two players have joined.
    Args:
        game (Game): The game instance to update.
        player (Player): The player to add to the game.
    Returns:
        Game: The updated game instance.
    """
    updated_game = api_service.update_game_with_new_player(player, game)
    if len(updated_game.players) == 2:
        return start_new_game(game_uuid=game.game_uuid)
    return updated_game

def add_player_in_game(game_uuid: str, player_name: str) -> Game:
    """
    Allows a Player to join an active game which is not already full
    strat a game if two players joined.
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
    return _update_game_with_player(game, player)


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
    return _update_game_with_player(game, player)

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
    available_games = [game for game in games if len(game.players) != 2]
    if not available_games:
        raise GameNotFoundError(
            "No game available at the moment, please create a game first."
        )
        
    player = get_single_player(player_name)
    selected_game = available_games[0]
    
    if player in selected_game.players:
        raise PlayerAlreadyInGameError(
            f"Player {player.name} with uuid : {player.player_uuid} already join this game ! Please try to create another Game"
        )
    return _update_game_with_player(selected_game, player)