from ast import List
import chess
from custom_errors.custom_errors import (
    InvalidTurnError,
    InvalidMoveError,
    GameOverError,
)
from schemas.game import Game
from schemas.player import Player


class ChessGame:
    def __init__(self, game: Game):
        """
        Initialize a new instance of ChessGame.

        Args:
            game (Game): The Game object containing information about the current game.
        """
        self.game = game
        self.white_player = game.white_player
        self.black_player = game.black_player
        self.current_turn = game.turn
        self.board = chess.Board()
        self.set_board(game.fen)

    def set_board(self, fen: str) -> None:
        """
        Set the game board to a given FEN.

        Args:
            fen (str): The FEN string representing the board position.

        Raises:
            InvalidMoveError: If the FEN string is invalid.
        """
        try:
            self.board.set_fen(fen)
        except ValueError as err:
            raise InvalidMoveError(f"Invalid FEN: {err}")

    def move(self, move: str, player: Player) -> Game:
        """
        Make a move in the chess game.

        Args:
            move (str): The move to be made in standard algebraic notation.
            player (Player): The player making the move.

        Returns:
            Game: A Game Object containing the updated game state.

        Raises:
            GameOverError: If the move is made after the game is over.
            InvalidTurnError: If the move is made out of turn.
            InvalidMoveError: If the move is illegal in the current position.
        """
        if self.is_game_over():
            raise GameOverError("The game is already over.")

        self._validate_player_turn(player)
        self._execute_move(move)
        self._update_turn()
        self._update_game_state()
        self.game.game_over = self.is_game_over()
        self.game.winner = self.determine_winner() if self.game.game_over else None

        return self.game

    def _validate_player_turn(self, player: Player) -> None:
        """
        Validate if it's the correct player's turn.

        Args:
            player (Player): The player to validate.

        Raises:
            InvalidTurnError: If it's not the player's turn.
        """
        if player != self.current_turn:
            raise InvalidTurnError(
                f"Not your turn, {self.current_turn.name} needs to play first"
            )

    def _execute_move(self, move: str) -> None:
        """
        Execute a move on the chess board.

        Args:
            move (str): The move to be executed.

        Raises:
            InvalidMoveError: If the move is illegal in the current position.
        """
        try:
            self.board.push_san(move)
        except chess.IllegalMoveError as err:
            raise InvalidMoveError(
                f"The move '{move}' is illegal in the current position: {err}"
            )
        except chess.InvalidMoveError as err:
            raise InvalidMoveError(f"The move '{move}' is invalid")

    def _update_turn(self) -> None:
        """
        Update the player turn after a move.
        """
        self.current_turn = (
            self.white_player
            if self.current_turn == self.black_player
            else self.black_player
        )
        self.game.turn = self.current_turn

    def _update_game_state(self) -> None:
        """
        Update the game state after a move.
        """
        self.game.fen = self.board.fen()

    def is_game_over(self) -> bool:
        """
        Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        if self.board.is_game_over():
            self.game.is_active = False
        return self.board.is_game_over()

    def get_board_fen(self) -> str:
        """
        Get the current board position in FEN.

        Returns:
            str: The current board position in FEN notation.
        """
        return self.board.fen()

    def get_player_turn(self) -> Player:
        """
        Get the current player's turn.

        Returns:
            Player: The player whose turn it is.
        """
        return self.current_turn

    def get_legal_move(self) -> list:
        moves = list(self.board.legal_moves)
        moves_uci = [move.uci() for move in moves]
        return moves_uci

    def determine_winner(self) -> [Player, str, None]:
        """
        Determine the winner of the game.

        Returns:
            Player or str: The winning player, "Draw" for a draw, or None if undecided.
        """
        if self.board.is_checkmate():
            return (
                self.white_player
                if self.current_turn == self.black_player
                else self.black_player
            )
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            return "Draw"
        else:
            return None
