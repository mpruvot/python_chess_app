import fastapi
from schemas.player_schema import Player
from services.player_services import *

router = fastapi.APIRouter()

@router.post('/players')
def new_player():
    return create_player()

@router.get('/players/{uuid}')
def get_player(uuid : uuid.UUID):
    pass
