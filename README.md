---

### Project: Online Chess Server with FastAPI

#### 1. Data Modeling
- **Game Class:**
  - `GameUid`: Unique identifier for each game.
  - `List of Players`: Contains exactly two different players. Pydantic is used for validation.
  - `Game State`: Representation of the current state of the game, likely stored in a database.

- **Player Class:**
  - `Attributes`: Player's name, Player Id, Elo rating.
  - `Friends`: An instance of Friends representing a list of players, excluding the player themselves.
  - `Active Games`: List of ongoing games.

#### 2. Business Logic
- **Features:**
  - Creating games.
  - Joining a game.
  - Leaving a game.

#### 3. Integration with the Chess API
- Utilizing the Chess API for managing moves and game rules.
- Developing a script to initiate a chess game based on the current game state.

#### 4. Database Management
- Deciding on the technology: SQLAlchemy or another to be determined.
- Learning and implementing database management techniques.

#### 5. External APIs and Advanced Features
- Investigating connections with APIs like [Chess.com](http://chess.com/).
- Potential future features include machine learning or integration with tools like Stockfish.

### TBC