from typing import List, Optional
from custom_errors.custom_errors import GameNotFoundError, NameAlreadyExistsError, PlayernotFoundError
from database_services.strapi_api_service import StrapiApiService
from schemas.chess_schemas import Player


api_service = StrapiApiService()


def create_player(name: str) -> Player:
    """
    Create a new Player with the given name and store it in the database.
    Args:
        name (str): The name of the player to create.
    Returns:
        Player: The newly created Player instance.
    Raises:
        NameAlreadyExistsError: If a player with the same name already exists in the database.
    """
    player = Player(name=name)
    return api_service.post_players(player)
    

def delete_player(player_name: str):
    return api_service.delete_player(player_name)


def get_all_players() -> Optional[List[Player]]:
    """
    Retrieve all players from the database.
    Returns:
        List[Player]: A list of Player instances.
    Raises:
        PlayernotFoundError: If no players are found in the database.
    """
    try:
        return api_service.get_players_from_db()
    except PlayernotFoundError:
        raise PlayernotFoundError("No players found in the database.")


def get_single_player(name: str) -> Player:
    """
    Retrieve a single player by name from the database.
    Args:
        name (str): The name of the player to retrieve.
    Returns:
        Player: The Player instance with the specified name.
    Raises:
        PlayernotFoundError: If no player with the specified name is found.
    """
    try:
        players = get_all_players()
        single_player = [
            player for player in players if player.name.lower() == name.lower()
        ]
        if single_player:
            return single_player[0]
        else:
            raise PlayernotFoundError(f"No player found with name: {name}")
    except PlayernotFoundError:
        raise PlayernotFoundError(f"Error retrieving player with name: {name}")


