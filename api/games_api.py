import fastapi
from fastapi import HTTPException
import uuid
from schemas.chess_schemas import Game, Player
from services.game_services import *

router = fastapi.APIRouter()

@router.post('/games')
def new_game():
    """Create a New Game"""
    return create_game()

@router.patch('/join/{game_uuid}/{player_name}')
def join_game(game_uuid: str, player_name: str):
    try: 
        add_player_in_game(game_uuid, player_name)
    except GameIsFullError as err:
        raise HTTPException(status_code=403, detail=str(err))
            

@router.get('/games')
def get_all_games():
    """Return a list of all the games"""
    try:
        return retrieve_all_games()
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))

@router.get('/game/{game_uuid}')
def get_single_game(game_uuid: str):
    """Retrieve a game by its UUID"""
    try:
        return retrieve_single_game(game_uuid)
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    
