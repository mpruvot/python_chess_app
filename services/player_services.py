from schemas.chess_schemas import Game, Player
import uuid

players_list = []

def create_player(name: str):
    player = Player(name=name)
    players_list.append(player)
    return player

def get_players():
    return [player for player in players_list]

def get_player_by_name(name: str):
    return [player for player in players_list if player.name == name]