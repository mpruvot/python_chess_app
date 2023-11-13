from schemas.game import Game
from schemas.player import Player
import uuid

players_list = []

def create_player():
    player = Player()
    players_list.append(player)
    return player
