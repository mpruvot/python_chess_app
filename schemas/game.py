from pydantic import BaseModel
from typing import Optional, List

from schemas.player import Player


class Game(BaseModel):
    """Chess Model"""

    game_id: Optional[int] = None
    is_active: bool = False
    white_player: Optional[Player] = None
    black_player: Optional[Player] = None
    turn: Optional[Player] = None
    fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


Game.model_rebuild()