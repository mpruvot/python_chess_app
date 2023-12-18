class GameNotFoundError(Exception):
    """Game not found !"""

    pass


class NotActiveGameError(Exception):
    """Game is not an active Game"""

    pass


class GameIsFullError(Exception):
    """Game is already ull !"""

    pass


class PlayernotFoundError(Exception):
    """No player found under this name !"""

    pass


class NameAlreadyExistsError(Exception):
    """A player with this name already exists"""

    pass


class PlayerAlreadyInGameError(Exception):
    """This Player is already in the Game !"""

    pass


class InvalidTurnError(Exception):
    """It's not your turn to play !"""

    pass


class GameOverError(Exception):
    pass


class GameAlreadyStartedError(Exception):
    pass

class InvalidFENError(Exception):
    pass


class InvalidMoveError(Exception):
    pass
# https://www.programiz.com/python-programming/user-defined-exception
