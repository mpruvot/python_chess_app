
from fastapi import FastAPI

from api import chess_engine_api, games_api, players_api


app = FastAPI()

app.include_router(players_api.router)
app.include_router(games_api.router)



