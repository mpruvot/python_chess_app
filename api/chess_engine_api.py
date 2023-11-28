from fastapi import APIRouter, HTTPException
from custom_errors.custom_errors import (
    GameAlreadyStartedError,
    GameNotFoundError,
    NotActiveGameError,
)

from chess_services.chess_engine_services import start_new_game


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
