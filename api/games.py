import fastapi
import uuid
from schemas.game import game
from services.game_services import *

router = fastapi.APIRouter()

@router.post('/games')
def new_game():
    return create_game()

@router.post('/join/{game}')

@router.get('/games/{uuid}')
def get_game(uuid : uuid.UUID):
    pass
