from typing import List
from fastapi import APIRouter, HTTPException
from custom_errors.custom_errors import NameAlreadyExistsError, PlayernotFoundError
from services.strapi_service import StrapiApiService
from schemas.player import Player


router = APIRouter()

service = StrapiApiService()


@router.get("/")
def home_page():
    return {"message": "Chess API"}


@router.post("/players/{name}", response_model=Player)
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
        return service.post_players(Player(name=name.capitalize()))
    except NameAlreadyExistsError as err:
        raise HTTPException(status_code=403, detail=str(err))


@router.get("/players/", response_model=List[Player])
def list_players() -> List[Player]:
    """
    Endpoint to retrieve a list of all players.
    Returns:
        List[Player]: A list of all player instances.
    Raises:
        HTTPException: If no players are found.
    """
    try:
        return service.get_players()
    except PlayernotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/players/{name}", response_model=Player)
def retrieve_player(name: str) -> Player:
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
        return service.get_single_player(name=name.capitalize())
    except PlayernotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.delete("/players/{name}")
def delete_player(name: str):
    try:
        return service.delete_player(name=name)
    except PlayernotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
