from schemas.chess_schemas import Game, Player
from custom_errors.custom_errors import *
import uuid


#Just for test before implementing a database
games_list = []


def create_game() -> Game:
    """Create a new Game"""
    game = Game()
    games_list.append(game)
    return game

def join_game(game: Game, player: Player) -> None:
    '''Allows a player to join an active game which is not already full'''
    
    if game not in games_list:
        raise GameNotFoundError('The game you are tyrying to join does not exists')
    elif not game.is_active:
        raise NotActiveGameError('Game is not active, or finished')
    elif len(game.players) == 2:
        raise GameIsFullError('Already to players in the Game, please choose another Game, or create one')
    
    
    game.players.append(player)
    player.active_games.append(game)
    
def retrieve_game(game_uuid: uuid.UUID) -> Game:
    """Retrieve a game by its Uuid"""
    found_game = [game for game in games_list if game.game_uuid == game_uuid]
    if found_game:
        return found_game[0]
    else: 
        raise GameNotFoundError('No game found uder this ID, please provide a valid ID')