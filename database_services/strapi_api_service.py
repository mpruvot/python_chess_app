import requests
import json
from schemas.chess_schemas import Player, Game
from custom_errors.custom_errors import *
from typing import List

class StrapiApiService:
    API_URL = "http://localhost:1337/api"

    def __init__(self) -> None:
        pass

    def get_players_from_db(self) -> List[Player]:
        """Return a list of all the players stored in database."""
        try:
            r = requests.get(f"{self.API_URL}/players")
            r.raise_for_status()
            players_data = r.json()['data']
            return [Player(**player['attributes']) for player in players_data]
        except requests.exceptions.HTTPError:
            raise PlayernotFoundError

    def store_player_in_db(self, new_player: Player) -> Player:
        """Store an instance of player object in database."""
        if new_player.name.capitalize() in [i.name.capitalize() for i in self.get_players_from_db()]:
            raise NameAlreadyExistsError('A player with this name already exists !')
        
        try:
            # Convert Player into dict, didn't use model.dump() because UUID is not Json Serializable
            new_player_json = json.loads(new_player.model_dump_json())
            
            payload = json.dumps({"data" : new_player_json})
            
            r = requests.post(
                f"{self.API_URL}/players",
                headers={"Content-Type": "application/json"},
                data = payload
            )
            r.raise_for_status()
            return Player(**r.json()['data']['attributes'])

        except requests.exceptions.HTTPError as err:
                raise str(err)
                
    def store_game_in_db(self, new_game: Game) -> Game:
        """Store an instance of Game object in database."""
        try:
            new_game_json = json.loads(new_game.model_dump_json())
            payload = json.dumps({"data" : new_game_json})
            r = requests.post(
                f"{self.API_URL}/games",
                headers={"Content-Type": "application/json"},
                data=payload
            )
            r.raise_for_status()
            return Game(**r.json()['data']['attributes'])
        except requests.exceptions.HTTPError as err:
            raise err

    def get_games_from_db(self) -> List[Game]:
        """Return a list of all the games stored in database."""
        try:
            r = requests.get(f"{self.API_URL}/games")
            r.raise_for_status()
            games_data = r.json()['data']
            return [Game(**game['attributes']) for game in games_data]
        except requests.exceptions.HTTPError:
            raise GameNotFoundError

    def get_single_game(self, game_uuid: str) -> Game:
        """Retrieve a single game by UUID and return a Game instance."""
        url = f"{self.API_URL}/games?filters[game_uuid][$eq]={game_uuid}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            games = response.json()
            if not games['data']:
                raise GameNotFoundError
            return Game(**games['data'][0]['attributes'])
        
        except requests.exceptions.HTTPError as err:
            raise GameNotFoundError from err

    def get_strapi_game_id(self, game_uuid: str):
        """Retrieve the Strapi ID of a Game."""
        try:
            data = self.get_single_game(game_uuid)
            return data.get('id')
        except requests.exceptions.HTTPError as err:
            raise GameNotFoundError + err

    def update_game_with_new_player(self, player: Player, game: Game) -> Game:
        
        game_id = self.get_strapi_game_id(str(game.game_uuid))
        url = f"{self.API_URL}/games/{game_id}"
        
        game.players.append(player)
        game_data_json = json.loads(game.model_dump_json())
        payload = json.dumps({"data" : game_data_json})
        
        try: 
            response = requests.put(
                url,
                headers={"Content-Type": "application/json"},
                data=payload
            )
            response.raise_for_status()
            updated_game_data = response.json()['data']['attributes']
            return Game(**updated_game_data)
        except requests.exceptions.HTTPError as err:
            raise err
