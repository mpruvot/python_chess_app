from typing import List, Optional

from pydantic import BaseModel


class Player(BaseModel):
    """Player Model"""

    name: str
    player_id: Optional[int] = None
    rank: Optional[int] = None
    friends: List["Player"] = []
    active_games: List[int] = []


Player.model_rebuild()
