from fastapi import APIRouter, HTTPException
import chess
from chess_app.chess_engine import ChessGame
from custom_errors.custom_errors import (
    GameAlreadyStartedError,
    GameNotFoundError,
    GameOverError,
    InvalidTurnError,
    NotActiveGameError,
)
from schemas.game import Game
from services.strapi_service import StrapiApiService


router = APIRouter()

service = StrapiApiService()

@router.post("/games/{game_id}/{player_name}/{move}")
def make_a_move(game_id: int, player_name: str, move: str):
    game = service.get_single_game(game_id=game_id)
    player = service.get_single_player(name=player_name)
    chess_game = ChessGame(game=game)
    
    if player in [game.black_player, game.white_player]:
        try:
            return service.update_game(chess_game.move(move, player))
        except chess.IllegalMoveError as err:
            raise HTTPException(status_code=403, detail=str(err))
        
        except chess.InvalidMoveError as err:
            raise HTTPException(status_code=403, detail=str(err))
        except InvalidTurnError as err:
            raise HTTPException(status_code=403, detail=str(err))
    
    else: 
        raise HTTPException(status_code=403, detail=str(f"{player_name} : does',t not belong to this game, please choose a valid player"))
    