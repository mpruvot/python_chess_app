from schemas.chess_schemas import Game, Player
from custom_errors.custom_errors import *
import uuid


#Just for test before implementing a database
games_list = []


def create_game():
    game = Game()
    games_list.append(game)
    return game

def join_game(game: Game, player: Player):
    '''Allows a player to join an active game which is not already full'''
    
    if game not in games_list or game.players >= 2:
        raise GameNotFoundError
    if not game.is_active:
        raise NotActiveGameError
    
    game.players.append(player)
    player.active_games.append(game)
    
    