from fastapi import APIRouter, HTTPException, status
from schemas.chess_schemas import Game, Player
from services.game_services import *

router = APIRouter()


@router.post("/game", response_model=Game)
def new_game():
    """
    Endpoint to create a new game.
    Returns:
        Game: The newly created game instance.
    """
    return create_game()


@router.patch("/join/{game_uuid}/{player_name}", response_model=Game)
def join_game(game_uuid: str, player_name: str):
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
        return add_player_in_game(game_uuid, player_name)
    except GameIsFullError as err:
        raise HTTPException(status_code=403, detail=str(err))
    except PlayerAlreadyInGameError as err:
        raise HTTPException(status_code=403, detail=str(err))


@router.patch("/join/{player_name}", response_model=Game)
def join_free_game(player_name: str):
    try:
        return search_and_join_game(player_name)
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except PlayernotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except PlayerAlreadyInGameError as err:
        raise HTTPException(status_code=403, detail=str(err))


@router.get("/games", response_model=list[Game])
def get_all_games(player_name: str | None = None):
    """
    Endpoint to retrieve a list of all games.
    if a player name is specified, retrives all the games with the specified player.

    Returns:
        list[Game]: A list of all game instances. or with a specified name
    Raises:
        HTTPException: If no games are found.
    """

    try:
        games = retrieve_all_games()
        if player_name:
            player = get_single_player(player_name)
            games_with_specified_player = [
                game for game in games if player in game.players
            ]
            if games_with_specified_player:
                return games_with_specified_player
            else:
                raise GameNotFoundError(
                    f"No game Found with player : {player_name.capitalize()}"
                )
        return games
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except PlayernotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/game/{game_uuid}", response_model=Game)
def get_single_game(game_uuid: str):
    """
    Endpoint to retrieve a single game by its UUID.
    Args:
        game_uuid (str): The UUID of the game to retrieve.
    Returns:
        Game: The game instance with the specified UUID.
    Raises:
        HTTPException: If no game with the specified UUID is found.
    """
    try:
        return retrieve_single_game(game_uuid)
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.delete("/game/{game_uuid}")
def delete_game_by_id(game_uuid: str):
    try:
        return delete_game(game_uuid)
    except GameNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))



@router.post("/game/{player}")
def new_game_and_join(player: str):
    try:
        return create_and_join_game(player)
    except PlayernotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
