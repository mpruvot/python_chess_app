import random
import chess

from custom_errors.custom_errors import GameOverError, InvalidTurnError


class GameOfChess:
    def __init__(self, name_player_1: str, name_player_2: str):
        self.board = chess.Board()
        self.player_1 = name_player_1
        self.player_2 = name_player_2
        self.player_1_color = random.choice(["Black", "White"])
        self.player_2_color = "Black" if self.player_1_color == "White" else "White"
        self.current_turn = (
            self.player_1 if self.player_1_color == "White" else self.player_2
        )

    def return_fen(self):
        return self.board.fen()

    def init_board(self, fen: str):
        """Initialize a ChessBoard from a Valid FEN
        Args:
            fen (str): The FEN of a chess Game
        Raises:
            VallueError: If the FEN is Not Valid
        Returns:
            Bool: True is FEN is Valid
        """
        try:
            self.board.set_fen(fen)
            return True
        except ValueError as err:
            raise ValueError(f"Please Enter a Valid FEN: error: {err}")

    def get_player_turn(self):
        return self.current_turn

    def print_board(self):
        print(self.board)

    def is_check(self):
        return self.board.is_check()

    def end_of_game(self):
        if self.board.is_checkmate():
            return "Checkmate"
        elif self.board.is_stalemate():
            return "Stalemate"
        elif self.board.is_insufficient_material():
            return "Draw due to insufficient material"
        return False

    def determine_winner(self):
        if self.board.is_checkmate():
            return (
                self.player_2 if self.current_turn == self.player_1 else self.player_1
            )
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            return "Draw"

    def make_move(self, move: str, player_name: str):
        if self.end_of_game():
            winner = self.determine_winner()
            raise GameOverError(f"Game Over. Winner: {winner}")

        if player_name.capitalize() != self.current_turn.capitalize():
            raise InvalidTurnError(
                f"Not your turn, {self.current_turn} needs to play first."
            )
        try:
            self.board.push_san(move)
            # update Player turn
            self.current_turn = (
                self.player_1 if self.current_turn == self.player_2 else self.player_2
            )
            return self.board.fen()

        except chess.IllegalMoveError as err:
            raise chess.InvalidMoveError(
                f"The move '{move}' is illegal in the current position."
            )


# board.push_san('e4') -> makes a move
# legal moves -> board.legal_moves
# Verifying check mate -> board.is_checkmate()
# Verifying stalemate -> board.is_stalemate()
# code -> board.is_check()
