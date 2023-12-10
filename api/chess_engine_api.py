from fastapi import APIRouter, HTTPException
import chess
from custom_errors.custom_errors import (
    GameAlreadyStartedError,
    GameNotFoundError,
    GameOverError,
    InvalidTurnError,
    NotActiveGameError,
)
from schemas.game import Game
from services.chess_engine_service import make_a_move, start_new_game

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

@router.post("/game/move/{game_uuid}/{player_name}/{move}")
def make_move(game_uuid, player_name, move) -> Game:
    try:
        return make_a_move(game_uuid=game_uuid, player_name=player_name, move=move)
    except NotActiveGameError as err:
        raise HTTPException(status_code=403, detail=str(err))
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except (chess.InvalidMoveError, chess.IllegalMoveError, InvalidTurnError, GameOverError) as err:
        raise HTTPException(status_code=404, detail=str(err))
        