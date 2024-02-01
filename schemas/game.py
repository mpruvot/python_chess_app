from typing import List, Optional

from pydantic import BaseModel

from schemas.player import Player


class Game(BaseModel):
    """Chess Model"""

    game_id: Optional[int] = None
    is_active: bool = False
    white_player: Optional[Player] = None
    black_player: Optional[Player] = None
    turn: Optional[Player] = None
    fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    game_over: bool = False
    winner: Optional[Player] = None


Game.model_rebuild()
