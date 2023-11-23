from schemas.chess_schemas import Game, Player
from custom_errors.custom_errors import *
from database_services.strapi_api_service import StrapiApiService
from typing import Optional, List

api_service = StrapiApiService()

def create_game() -> Game:
    """Create a new Game"""
    game = Game()
    api_service.store_game_in_db(game)
    return game

def retrieve_all_games() -> Optional[List[Game]]:
    """Retrieve a list of all the games"""
    data = api_service.get_games_from_db().get('data')
    if not data:
        raise GameNotFoundError('List is empty!')
    return [Game(**game_data['attributes']) for game_data in data]

def retrieve_single_game(game_uuid: str) -> Game:
    """Retrieve a game by its UUID"""
    try:
        game_data = api_service.get_single_game(game_uuid)
        return Game(**game_data['attributes'])
    except GameNotFoundError:
        raise GameNotFoundError(f'No game found with UUID: {game_uuid}')

def add_player_in_game(game_uuid: str, player_name: str) -> Game:
    """Allows a Player to join an active game which is not already full"""
    game = retrieve_single_game(game_uuid)
    
    if player_name in game.players:
        raise PlayerAlreadyInGameError(f'Player {player_name} is already in the game.')
    if len(game.players) >= 2:
        raise GameIsFullError('The game is already full.')

    game.players.append(player_name)
    # update database?
    return game
