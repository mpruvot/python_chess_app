from schemas.chess_schemas import Game, Player
from custom_errors.custom_errors import *
from database_services import strapi_services
from typing import Optional, List
import uuid

def create_game() -> Game:
    """Create a new Game"""
    game = Game()
    strapi_services.store_game_in_db(game)
    return game

def retrieve_all_games() -> Optional[List[Game]]:
    """retrieve a List of all the games"""
    data = strapi_services.get_games_from_db().get('data')
    if not data:
        raise GameNotFoundError('List is empty !')
    games = [Game(**game_data['attributes']) for game_data in data]
    return games

def retrieve_single_game(game_uuid: str) -> Game:
    """Retrieve a game by its UUID"""
    games_data = retrieve_all_games()
    single_game = [game for game in games_data if str(game.game_uuid) == game_uuid]
    
    if single_game:
        return single_game[0]
    else:
        raise GameNotFoundError('No game found under this uuid')

    
    
def add_player_in_game(game_uuid: str, player_name: str) -> Game:
    '''Allows a Player to join an active game which is not already full'''
    game = retrieve_single_game(game_uuid)
    
    if player_name in game.players:
        raise GameIsFullError
    if len(game.players) == 2:
        raise GameIsFullError
    
    game.players.append(player_name)
    return Game
        
    
