from .player_schema import Player
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from typing_extensions import Annotated
import uuid

class Game(BaseModel):
    game_uuid : uuid.UUID = Field(default_factory=uuid.uuid4)
    is_active : bool = True
    players : List[Player] = []
    # State -> probably need to load it from a database
    
    
# https://docs.pydantic.dev/latest/concepts/validators/