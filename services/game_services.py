from schemas.chess_schemas import Game, Player
from custom_errors.custom_errors import *
from database_services.strapi_api_service import StrapiApiService
from typing import Optional, List

api_service = StrapiApiService()

def create_game() -> Game:
    """Create a new Game"""
    game = Game()
    return api_service.store_game_in_db(game)

def retrieve_all_games() -> Optional[List[Game]]:
    """Retrieve a list of all the games"""
    try:
        return api_service.get_games_from_db()
    except GameNotFoundError:
        raise GameNotFoundError('List is empty!')

def retrieve_single_game(game_uuid: str) -> Game:
    """Retrieve a game by its UUID"""
    try:
        return api_service.get_single_game(game_uuid)
    except GameNotFoundError:
        raise GameNotFoundError(f'No game found with UUID: {game_uuid}')

def add_player_in_game(game: Game, player: Player) -> Game:
    """Allows a Player to join an active game which is not already full"""
    if player in game.players:
        raise PlayerAlreadyInGameError(f'Player {player.name} is already in the game.')
    
    updated_game = api_service.update_game_with_new_player(player, game)
    return updated_game
