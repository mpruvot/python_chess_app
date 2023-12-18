import chess
from custom_errors.custom_errors import GameOverError, InvalidTurnError
from schemas.game import Game
from schemas.player import Player

class ChessGame:
    def __init__(self, game: Game):
        self.game = game
        self.white_player = game.white_player
        self.black_player = game.black_player
        self.current_turn = game.turn
        
        self.board = chess.Board()
        self.set_board(game.fen)

    def get_board(self):
        return self.board.fen()
    
    def get_player_turn(self):
        return self.current_turn
        
    def set_board(self, fen: str):
        """
        Initialize a ChessBoard from a Valid FEN
        Args:
            fen (str): The FEN of a chess Game
        Raises:
            ValueError: If the FEN is Not Valid
        """
        try:
            self.board.set_fen(fen)
        except ValueError as err:
            raise ValueError(f"Please Enter a Valid FEN: error: {err}")
    
    def _update_game(self, game: Game, fen: str, turn: Player):
        game.turn = turn
        game.fen = fen
        return game
        
    def _update_turn(self):
        self.current_turn = (
                self.white_player if self.current_turn == self.black_player else self.black_player
            )
        
    def end_of_game(self):
        if self.board.is_checkmate():
            return "Checkmate"
        elif self.board.is_stalemate():
            return "Stalemate"
        elif self.board.is_insufficient_material():
            return "Draw due to insufficient material"
        return "Draw"
    
    def determine_winner(self):
        if self.board.is_checkmate():
            return self.current_turn
        
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            return "Draw"
        
    def move(self, move: str, player: Player):
        if player != self.current_turn:
            raise InvalidTurnError(
                f"Not your turn, {self.current_turn.name} needs to play first"
            )
        try:
            self.board.push_san(move)
            # update Player turn
            self._update_turn()
            return self._update_game(self.game, self.board.fen(), self.current_turn)
        
        except chess.IllegalMoveError as err:
            raise chess.InvalidMoveError(
                f"The move '{move}' is illegal in the current position: {err}"
            )