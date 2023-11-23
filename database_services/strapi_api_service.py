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
        try:
            r = requests.post(
                f"{self.API_URL}/players",
                headers={"Content-Type": "application/json"},
                data=new_player.model_dump_json()
            )
            r.raise_for_status()
            return Player(**r.json()['data']['attributes'])
        
        except requests.exceptions.HTTPError as err:
            if r.status_code == 400:
                raise NameAlreadyExistsError
            else:
                raise err
            
    def store_game_in_db(self, new_game: Game) -> Game:
        """Store an instance of Game object in database."""
        try:
            r = requests.post(
                f"{self.API_URL}/games",
                headers={"Content-Type": "application/json"},
                data=new_game.model_dump_json(),
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
        
        game.players.append(player)
        
        game_data = game.model_dump_json()
        
        game_id = self.get_strapi_game_id(str(game.game_uuid))
        url = f"{self.API_URL}/games/{game_id}"

        try: 
            response = requests.put(
                url,
                headers={"Content-Type": "application/json"},
                data=game_data
            )
            response.raise_for_status()
            updated_game_data = response.json()['data']['attributes']
            return Game(**updated_game_data)
        except requests.exceptions.HTTPError as err:
            raise err
