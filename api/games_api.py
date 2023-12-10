from fastapi import APIRouter, HTTPException
from custom_errors.custom_errors import (
    GameIsFullError,
    GameNotFoundError,
    PlayerAlreadyInGameError,
)
from database_services.strapi_api_service import StrapiApiService

from schemas.chess_schemas import Game


router = APIRouter()
service = StrapiApiService()


@router.post("/games/", response_model=Game)
def new_game():
    """
    Endpoint to create a new game.
    Returns:
        Game: The newly created game instance.
    """
    return service.post_games(Game())


@router.patch("/games/{game_id}/{player_name}", response_model=Game)
def join_game(game_id: int, player_name: str):
    """
    Endpoint to allow a player to join a game.
    Args:
        game_uuid (str): The UUID of the game to join.
        player_name (str): The name of the player joining the game.
    Returns:
        Game: The updated game instance after adding the player.
    Raises:
        HTTPException: If the game is full or if the game is not found.
    """
    try:
        return service.add_player_to_game(player_name, game_id)
    except GameIsFullError as err:
        raise HTTPException(status_code=403, detail=str(err))
    except PlayerAlreadyInGameError as err:
        raise HTTPException(status_code=403, detail=str(err))


@router.get("/games/", response_model=list[Game])
def list_games():
    """
    Endpoint to retrieve a list of all games.
    if a player name is specified, retrives all the games with the specified player.

    Returns:
        list[Game]: A list of all game instances. or with a specified name
    Raises:
        HTTPException: If no games are found.
    """

    try:
        return service.get_games()
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/games/{game_id}", response_model=Game)
def retrieve_game(game_id: int):
    """
    Endpoint to retrieve a single game by its UUID.
    Args:
        game_uuid (int): The UUID of the game to retrieve.
    Returns:
        Game: The game instance with the specified UUID.
    Raises:
        HTTPException: If no game with the specified UUID is found.
    """
    try:
        return service.get_single_game(game_id)
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.delete("/games/{game_id}")
def delete_game(game_id: int):
    try:
        return service.delete_game(game_id)
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
