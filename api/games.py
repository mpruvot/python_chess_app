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

@router.get('/games/{uuid}')
def get_game(uuid : uuid.UUID):
    """Return a specific game when you provide its UUID"""
    try: 
        return retrieve_game(uuid)
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
