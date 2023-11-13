from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from api import players, games


app = FastAPI()

app.include_router(players.router)
app.include_router(games.router)

