from pydantic import BaseModel
from typing import Optional, List
import uuid

class Player(BaseModel):
    Name : str
    Uuid : str(uuid.uuid4())
    Rank : int
    Friends : List[self] = None
    