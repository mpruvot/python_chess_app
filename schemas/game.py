from .player import Player
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

class Game(BaseModel):
    uuid : uuid.UUID = Field(default_factory=uuid.uuid4)
    players : List[Player] = []
    # State -> probably need to load it from a database