from fastapi import APIRouter, HTTPException, status
from schemas.chess_schemas import Player
from services.player_services import create_player, get_all_players, get_single_player
from custom_errors.custom_errors import *
from typing import List

router = APIRouter()

@router.post('/player/', response_model=Player)
def new_player(name: str) -> Player:
    """Create a new Player"""
    try : 
        return create_player(name=name)
    except NameAlreadyExistsError as err:
        raise HTTPException(status_code=403, detail=str(err))

        
@router.get('/players/', response_model=List[Player])
def get_players() -> List[Player]:
    """Returns a list of all players"""
    try:
        return get_all_players()
    except PlayernotFoundError as err:
        raise HTTPException(status_code= 404, detail=str(err))

@router.get('/player/{name}', response_model=Player)
def return_player_by_name(name: str) -> Player:
    """Retrieve a player by name"""
    try:
        return get_single_player(name)
    except PlayernotFoundError as err:
        raise HTTPException(status_code= 404, detail=str(err))
