from pydantic import BaseModel
from typing import Optional, List
from custom_errors.custom_errors import *


class Game(BaseModel):
    """Chess Model"""
    game_id: Optional[int] = None
    is_active: bool = False
    white_player: Optional["Player"] = None
    black_player: Optional["Player"] = None
    turn: Optional[str] = None
    fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Player(BaseModel):
    """Player Model"""

    name: str
    player_id: Optional[int] = None
    rank: Optional[int] = None
    friends: List["Player"] = []
    active_games: List[int] = []


Game.model_rebuild()
Player.model_rebuild()

# https://docs.pydantic.dev/latest/concepts/validators/
