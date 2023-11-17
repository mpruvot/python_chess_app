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
    players = strapi_services.get_players_from_db()
    if not players:
        raise PlayernotFoundError('List is empty !')
    return players
     