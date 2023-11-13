import fastapi
from schemas.chess_schemas import Player, Game
from services.player_services import *

router = fastapi.APIRouter()

@router.post('/players/')
def new_player(name: str):
    created_player = create_player(name= name)
    return created_player

@router.get('/players/')
def get_player():
    return get_players()
