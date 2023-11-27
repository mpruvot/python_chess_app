from fastapi import APIRouter, HTTPException, status
from schemas.chess_schemas import Player
from services.player_services import *
from custom_errors.custom_errors import *
from typing import List

router = APIRouter()


@router.get("/")
def home_page():
    return {"message": "Chess API"}


@router.post("/player/", response_model=Player)
def new_player(name: str) -> Player:
    """
    Endpoint to create a new player.
    Args:
        name (str): The name of the player to create.
    Returns:
        Player: The newly created player instance.
    Raises:
        HTTPException: If a player with the same name already exists.
    """
    try:
        return create_player(name=name)
    except NameAlreadyExistsError as err:
        raise HTTPException(status_code=403, detail=str(err))


@router.get("/players/", response_model=List[Player])
def get_players() -> List[Player]:
    """
    Endpoint to retrieve a list of all players.
    Returns:
        List[Player]: A list of all player instances.
    Raises:
        HTTPException: If no players are found.
    """
    try:
        return get_all_players()
    except PlayernotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/player/{name}", response_model=Player)
def return_player_by_name(name: str) -> Player:
    """
    Endpoint to retrieve a single player by name.
    Args:
        name (str): The name of the player to retrieve.
    Returns:
        Player: The player instance with the specified name.
    Raises:
        HTTPException: If no player with the specified name is found.
    """
    try:
        return get_single_player(name)
    except PlayernotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.delete("/player/{name}")
def delete_player_by_name(name: str):
    try:
        return delete_player(name)
    except PlayernotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
