from schemas.chess_schemas import Game, Player
from custom_errors.custom_errors import *
from database_services.strapi_api_service import StrapiApiService
from typing import Optional, List

api_service = StrapiApiService()

def create_player(name: str) -> Player:
    """Create a new Player and store it into strapi_db"""
    player = Player(name=name)
    api_service.store_player_in_db(player)
    return player

def get_all_players() -> Optional[List[Player]]:
    try:
        data = api_service.get_players_from_db().get('data')
        if not data:
            raise PlayernotFoundError('List is empty!')
        return [Player(**player_data['attributes']) for player_data in data]
    except PlayernotFoundError:
        raise PlayernotFoundError('No players found')

def get_single_player(name: str) -> Player:
    try:
        players = get_all_players()
        single_player = [player for player in players if player.name.lower() == name.lower()]
        if single_player:
            return single_player[0]
        else:
            raise PlayernotFoundError(f'No player found with name: {name}')
    except PlayernotFoundError:
        raise PlayernotFoundError(f'Error retrieving player with name: {name}')
