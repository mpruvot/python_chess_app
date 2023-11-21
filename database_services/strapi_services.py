# https://medium.com/@kevinkoech265/a-guide-to-connecting-postgresql-and-pythons-fast-api-from-installation-to-integration-825f875f9f7d
# https://www.youtube.com/watch?v=398DuQbQJq0
# https://docs.strapi.io/dev-docs/integrations/python
# https://docs.strapi.io/dev-docs/quick-start

import requests
import json
from schemas.chess_schemas import Player, Game
from pydantic import json_schema, BaseModel
from custom_errors.custom_errors import *

API_URL = "http://localhost:1337/api/"


##### PLAYER DATABASE SERVICES #####

def get_players_from_db() -> json:
    """return a list of all the players stored in databse

    Returns:
        _type_: Json
    """
    try:
        r = requests.get(API_URL + "/players")
        r.raise_for_status()
        response = r.json()
        return response
    except requests.exceptions.HTTPError as err:
        raise PlayernotFoundError("list of plaers is empty !")
    
    
def store_player_in_db(new_player: Player) -> json:
    """Store an instance of player objet in database

    Args:
        new_player (Player): Instance of player created by a post.request 

    Returns:
        _type_: json
    """
    player_data = new_player.model_dump()
    
    # UUID to (str) because UUID object are not serializable into Json format
    player_data["player_uuid"] = str(player_data["player_uuid"])
    try:
        r = requests.post(
            "http://localhost:1337/api/players",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"data": player_data}),
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as err:
        if r.status_code == 400:  
            raise NameAlreadyExistsError("A player with this name already exists !")
        else:
            raise err


##### GAME DATABASE SERVICES #####

def store_game_in_db(new_game : Game) -> json:
    """Store an instance of Game objet in database

    Args:
        new_game (Game): Instance of Game created by a post.request 

    Returns:
        _type_: json
    """
    game_data = new_game.model_dump()
    game_data["game_uuid"] = str(game_data["game_uuid"])
    try:
        r = requests.post(
            "http://localhost:1337/api/games",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"data": game_data}),
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as err:
        raise err
    
def get_games_from_db() -> json:
    """return a list of all the games stored in database

    Returns:
        _type_: Json
    """
    try:
        r = requests.get(API_URL + "/games")
        r.raise_for_status()
        response = r.json()
        return response
    except requests.exceptions.HTTPError as err:
        raise GameNotFoundError("list of games is empty !")
    
def get_single_game(game_uuid: str):
    url = f"{API_URL}games?filters[game_uuid][$eq]={game_uuid}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        games = response.json()
        if not games['data']:
            raise GameNotFoundError
        return games['data'][0]  
    except requests.exceptions.HTTPError as err:
        raise GameNotFoundError("list of games is empty !")

def get_strapi_game_id(game_uuid: str):
    """retrieve the strapi ID of a Game"""
    try:
        data = get_single_game(game_uuid)
        return data.get('id')
    except requests.exceptions.HTTPError as err:
        raise GameNotFoundError
    
def put_add_player(player: str, game_uuid: str):
    """Update an existing game: add a new Player in List[Player]"""
    pass
