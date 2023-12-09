from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from custom_errors.custom_errors import *
import uuid


class Game(BaseModel):
    game_id : Optional[int] = None
    is_active: bool = False
    white_player : Optional["Player"] = None
    black_player : Optional["Player"] = None
    turn : Optional[str] = None
    fen: Optional[str] = None

    # @field_validator('players')
    # @classmethod
    # def check_number_of_players(cls, v: list):
    #   if len(v) >= 2:
    #      raise GameIsFullError('Already two players in the game !')
    # return v

    # State -> probably need to load it from a database


class Player(BaseModel):
    """Player model"""

    name: str
    player_id : Optional[int] = None
    rank: Optional[int] = None
    friends: List["Player"] = []
    active_games: List[int] = []
    


Game.model_rebuild()
Player.model_rebuild()

# https://docs.pydantic.dev/latest/concepts/validators/
