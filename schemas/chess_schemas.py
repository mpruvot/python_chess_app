from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from custom_errors.custom_errors import *
import uuid


class Game(BaseModel):
    game_uuid: uuid.UUID = Field(default_factory=uuid.uuid4)
    is_active: bool = False
    players: List["Player"] = []
    turn : Optional[str] = ""
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
    player_uuid: uuid.UUID = Field(default_factory=uuid.uuid4)
    rank: Optional[int] = None
    friends: List["Player"] = []
    active_games: List[Game] = []
    color: Optional[str] = None


Game.model_rebuild()
Player.model_rebuild()

# https://docs.pydantic.dev/latest/concepts/validators/
