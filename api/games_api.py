from fastapi import APIRouter, HTTPException, status
from schemas.chess_schemas import Game, Player
from services.game_services import *

router = APIRouter()

@router.post('/games', response_model=Game)
def new_game():
    """Create a New Game"""
    return create_game()

@router.patch('/join/{game_uuid}/{player_name}', response_model=Game)
def join_game(game_uuid: str, player_name: str):
    """Allows a player to join a game"""
    try: 
        return add_player_in_game(game_uuid, player_name)
    except GameIsFullError as err:
        raise HTTPException(status_code= 403, detail=str(err))

@router.get('/games', response_model=list[Game])
def get_all_games():
    """Return a list of all the games"""
    try:
        return retrieve_all_games()
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))

@router.get('/game/{game_uuid}', response_model=Game)
def get_single_game(game_uuid: str):
    """Retrieve a game by its UUID"""
    try:
        return retrieve_single_game(game_uuid)
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
