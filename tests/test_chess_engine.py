import chess
import pytest
from custom_errors.custom_errors import InvalidTurnError, InvalidMoveError
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


def test_validate_player_turn_exception(default_game):
    with pytest.raises(InvalidTurnError):
        default_game._validate_player_turn(default_game.game.black_player)


def test_update_turn(default_game):
    default_game._update_turn()
    assert default_game.current_turn == default_game.black_player


def test_execute_move(default_game):
    fen_with_e4_as_first_move = (
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
    )
    default_game._execute_move("e4")
    assert default_game.board.fen() == fen_with_e4_as_first_move


def test_execute_move_exceptions(default_game):
    with pytest.raises(InvalidMoveError):
        default_game._execute_move("Be3")


def test_update_game_state(default_game):
    fen_with_e4_as_first_move = (
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
    )
    default_game._execute_move("e4")
    default_game._update_game_state()
    assert default_game.game.fen == fen_with_e4_as_first_move


def test_is_game_over(default_game):
    checkmate = "r1bqkbnr/1ppp1Qpp/p1n5/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 1"
    default_game.set_board(checkmate)

    assert default_game.is_game_over()


def tests_get_legal_move(default_game):
    legal_moves = [
        "g1h3",
        "g1f3",
        "b1c3",
        "b1a3",
        "h2h3",
        "g2g3",
        "f2f3",
        "e2e3",
        "d2d3",
        "c2c3",
        "b2b3",
        "a2a3",
        "h2h4",
        "g2g4",
        "f2f4",
        "e2e4",
        "d2d4",
        "c2c4",
        "b2b4",
        "a2a4",
    ]
    assert default_game.get_legal_move() == legal_moves
    
def test_move(default_game):
    fen_with_e4_as_first_move = (
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
    )
    
    default_game.move("e4", default_game.white_player)
    
    assert default_game.game.fen == fen_with_e4_as_first_move
    assert default_game.game.turn == default_game.game.black_player