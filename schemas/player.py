import uuid
from typing import Optional, List
from pydantic import BaseModel, Field
from game import Game


class Player(BaseModel):
    '''Player model'''
    name : str
    player_uuid : uuid.UUID = Field(default_factory=uuid.uuid4)
    rank : int
    friends : List['Player'] = []
    active_games : List[Game] = []
    
