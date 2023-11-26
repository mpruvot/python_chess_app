from schemas.chess_schemas import Game, Player
from chess_app.chess_engine import *
from custom_errors.custom_errors import *
from database_services.strapi_api_service import StrapiApiService
from typing import Optional, List
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

def init_game(game_uuid: str):
    """Starts a Game if two players joined the Game, init an FEN code to the Game instance

    Args:
        game_uuid (str): Uuid of the Game
    """
    game = retrieve_single_game(game_uuid)
    if game.fen:
        raise GameAlreadyStartedError(f'Game already started with fen : {game.fen}')
    if len(game.players) != 2:
        raise NotActiveGameError(f'Not enough Players in the Game: {len(game.players)} joined')
    try:
        player_1 = game.players[0].name
        player_2 = game.players[1].name
        chess_engine = GameOfChess(name_player_1=player_1, name_player_2=player_2)
        fen = chess_engine.return_fen()
        game.is_active = True
        updated_game = api_service.update_fen_of_game(game=game, fen=fen)
        return updated_game
    
    except GameNotFoundError:
        raise GameNotFoundError(f"No game found with UUID: {game_uuid}")