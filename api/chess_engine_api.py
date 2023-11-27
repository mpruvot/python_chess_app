from fastapi import APIRouter, HTTPException, status
from schemas.chess_schemas import Game, Player
from services.game_services import *
from chess_app.chess_engine import *
from services.player_services import *
from services.chess_engine_services import *

router = APIRouter()

@router.post("/game/{game_uuid}/")
def start_game(game_uuid: str):
    try:
        return start_new_game(game_uuid)
    except NotActiveGameError as err:
        raise HTTPException(status_code=403, detail=str(err))
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except GameAlreadyStartedError as err:
        raise HTTPException(status_code=403, detail=str(err))

