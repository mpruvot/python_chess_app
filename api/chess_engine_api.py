from fastapi import APIRouter, HTTPException, Body
import chess
from pydantic import BaseModel
from chess_app.chess_engine import ChessGame
from custom_errors.custom_errors import GameOverError, InvalidMoveError, InvalidTurnError

from services.strapi_service import StrapiApiService

class MoveDetails(BaseModel):
    player_name: str
    move: str

router = APIRouter()
service = StrapiApiService()

@router.patch("/games/{game_id}")
def make_a_move(game_id: int, move_details: MoveDetails = Body(...)):
    game = service.get_single_game(game_id=game_id)
    player = service.get_single_player(name=move_details.player_name.capitalize())
    chess_game = ChessGame(game=game)
    
    if player in [game.black_player, game.white_player]:
        try:
            updated_game = chess_game.move(move_details.move, player)
            return updated_game
            service.update_game(updated_game) 
            return updated_game
        except InvalidMoveError as err:
            raise HTTPException(status_code=400, detail=f"Invalid move: {err}")
        except InvalidTurnError as err:
            raise HTTPException(status_code=403, detail=str(err))
        except GameOverError as err:
            raise HTTPException(status_code=403, detail=str(err))
    else: 
        raise HTTPException(status_code=403, detail=f"{move_details.player_name} does not belong to this game, please choose a valid player")

@router.get("/games/move/{game_id}")
def legal_move(game_id: int):
    game = service.get_single_game(game_id=game_id)
    chess_game = ChessGame(game=game)  
    return chess_game.get_legal_move()
    
