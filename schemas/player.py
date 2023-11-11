from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

class Player(BaseModel):
    name : str
    uuid : uuid.UUID = Field(default_factory=uuid.uuid4)
    rank : int
    friends : List['Player'] = []
    
