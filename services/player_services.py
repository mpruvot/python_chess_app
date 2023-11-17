from schemas.chess_schemas import Game, Player
import uuid
from typing import List, Optional
from database_services import strapi_services
from custom_errors.custom_errors import *

def create_player(name: str) -> Player:
    """Create a new Player and store it into strapi_db"""
    player = Player(name=name)
    strapi_services.store_player_in_db(player)
    return player

def get_all_players() -> Optional[List[Player]]:
    data = strapi_services.get_players_from_db().get('data')
    if not data:
        raise PlayernotFoundError('List is empty !')

    players = [Player(**player_data['attributes']) for player_data in data]
    return players

def get_single_player(name: str) -> Player:
    data = get_all_players()
    single_player = [player for player in data if player.name.lower() == name.lower()]
    
    if single_player:
        return single_player[0]
    else:
        raise PlayernotFoundError('No player found under this name')
