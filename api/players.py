import fastapi
from fastapi import HTTPException
from schemas.chess_schemas import Player, Game
from services.player_services import *
from typing import List, Optional

router = fastapi.APIRouter()

@router.post('/players/')
def new_player(name: str) -> Player:
    """Create a new Player"""
    try:
        created_player = create_player(name= name)
        return created_player
    except NameAlreadyExistsError as err:
        raise HTTPException(status_code=403, detail=str(err))

@router.get('/players/')
def get_players() -> List[Player]:
    """returns a list of all players"""
    try:
        return get_all_players()
    except PlayernotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))

@router.get('/player/{name}')
def return_player_by_name(name: str) -> Player:
    try:
        players = get_all_players()
        found_player = [player for player in players.get('data') if player['attributes'].get('name') == name]
        if found_player:
            return found_player
        raise PlayernotFoundError
    except PlayernotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
