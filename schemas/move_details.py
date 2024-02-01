from pydantic import BaseModel


class MoveDetails(BaseModel):
    player_name: str
    move: str
