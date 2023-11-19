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

@router.post('/join/{game}')
#To be defined

@router.get('/games')
def get_all_games():
    """Return a list of all the games"""
    try:
        return retrieve_all_games()
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))

@router.get('/game/{game_uuid}')
def get_single_game(game_uuid: uuid.UUID):
    """Retrieve a game by its UUID"""
    try:
        return retrieve_single_game(game_uuid)
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    
