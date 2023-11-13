from schemas.game_schema import Game
from schemas.player_schema import Player
import uuid

players_list = []

def create_player():
    player = Player()
    players_list.append(player)
    return player
