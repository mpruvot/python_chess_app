from schemas.chess_schemas import Game, Player
import uuid
from typing import List, Optional
from custom_errors.custom_errors import *

players_list = []

def create_player(name: str) -> Player:
    """Create a new PLayer"""
    for player in players_list:
        if player.name == name:
            raise NameAlreadyExistsError('user already exists, please choose another name')
    player = Player(name=name)
    players_list.append(player)
    return player

def get_all_players() -> List[Player]:
    return players_list

def get_player_by_name(name: str) -> Optional[Player]:
    player = [player for player in players_list if player.name == name]
    if player:
        return player[0]
    else:
        raise PlayernotFoundError('No player found under this Name')