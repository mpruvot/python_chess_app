from schemas.game import Game
from schemas.player import Player
import uuid

def create_player():
    player = Player()
    return player

def join_game(game : Game, player : Player):
    pass