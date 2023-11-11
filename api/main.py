from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def root():
    return {"message": "test"}