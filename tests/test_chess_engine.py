import pytest
from schemas.game import Game
from schemas.player import Player
from chess_app.chess_engine import ChessGame


@pytest.fixture
def default_game():
    player_1 = Player(name="Player1")
    player_2 = Player(name="Player2")
    game = Game(
        game_id=1,
        is_active=False,
        white_player=player_1,
        black_player=player_2,
        turn=player_1,
    )
    return ChessGame(game=game)


def test_default_board(default_game):
    default_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    # Test if the board is well initialized
    assert default_game.board.fen() == default_fen

def test_set_board(default_game):

    new_fen = "rnbqkbnr/pp2pppp/2p5/3p4/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1"
    default_game.set_board(new_fen)

    # Test after setting a new fen
    assert default_game.board.fen() == new_fen
