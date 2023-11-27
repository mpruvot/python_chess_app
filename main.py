from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from api import games_api, players_api, chess_engine_api


app = FastAPI()

app.include_router(players_api.router)
app.include_router(games_api.router)
app.include_router(chess_engine_api.router)


