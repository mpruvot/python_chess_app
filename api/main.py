from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from schemas.player import Player
from schemas.game import Game
from services.game_services import *
from services.player_services import *

app = FastAPI()

@app.get('/')
def root():
    return {"message": "test"}


###### Games Routes ######

@app.post('/games')
def new_game():
    return create_game()

@app.get('/games/{uuid}')
def get_game(uuid : uuid.UUID):
    pass

###### Players Routes #######

@app.post('/players')
def new_player():
    return create_player()

@app.get('/players/{uuid}')
def get_player(uuid : uuid.UUID):
    pass