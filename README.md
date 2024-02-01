# Python Chess App API

## Overview
The Python Chess App API is a FastAPI-based application designed for playing chess. 
It offers a range of endpoints for managing chess games and players, providing functionalities such as creating new games, joining existing games, making moves, and more.

## Endpoints

### Chess Engine API (`api/chess_engine_api.py`)
- `PATCH /games/{game_id}`: Make a move in a game. Requires the game ID and move details.
- `GET /games/move/{game_id}`: Get legal moves for a game. Requires the game ID.

### Games API (`api/games_api.py`)
- `POST /games/`: Create a new game.
- `PATCH /games/{game_id}/{player_name}`: Join a game. Requires the game ID and player name.
- `GET /games/`: List all games.
- `GET /games/{game_id}`: Retrieve a specific game by ID.
- `DELETE /games/{game_id}`: Delete a game by ID.

### Players API (`api/players_api.py`)
- `POST /players/{name}`: Create a new player. Requires the player's name.
- `GET /players/`: List all players.
- `GET /players/{name}`: Retrieve a specific player by name.
- `DELETE /players/{name}`: Delete a player by name.

## Core Components

- **Chess Engine (`chess_app/chess_engine.py`):** Handles the logic of the chess game, including move validation and game state updates.
- **Data Models:**
  - `Game` (`schemas/game.py`): Defines the structure of a chess game.
  - `Player` (`schemas/player.py`): Defines the structure of a player.
- **Custom Errors (`custom_errors/custom_errors.py`):** Defines custom exceptions for error handling in the application.
- **Strapi Service (`services/strapi_service.py`):** Manages interactions with the Strapi backend.

## Testing
- Unit tests for game and player APIs are available in `tests/test_game_api.py` and `tests/test_players_api.py`.



## Dependencies
- The application's dependencies are listed in `requirements.txt`. Install them using `pip install -r requirements.txt`.

---

# Installation
### Fast api Project
- create a virtual env:
  ```python3 -m venv venv```
  
- install all the dependancies:
    ```pip install -r requirements.txt```
  
- run uvicorn, in root: ```uvicorn api.main:app --reload```

### Strapi
- ```cd chess_db```
- ```npm install```
- ```npm run develop```

- in .env.exemple, replace the keys with your own and rename to .env
  


