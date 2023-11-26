import chess    
from chess import InvalidMoveError, IllegalMoveError
import random
from custom_errors.custom_errors import *
from schemas.chess_schemas import *

class GameOfChess:
    def __init__(self, name_player_1: str, name_player_2: str):
        self.board = chess.Board()
        self.player_1 = name_player_1
        self.player_2 = name_player_2
        self.player_1_color = random.choice(['Black', 'White'])
        self.player_2_color = 'Black' if self.player_1_color == 'White' else 'White'
        self.current_turn = self.player_1 if self.player_1_color == "White" else self.player_2
        
    def get_player_turn(self):
        return self.current_turn
    
    def print_board(self):
        print(self.board)


    def make_move(self, move: str, player_name: str):
        if player_name.capitalize() != self.current_turn.capitalize():
            raise InvalidTurnError(f'Not your turn, {self.current_turn} needs to play first.')
        try:
                self.board.push_san(move)
                #update Player turn
                self.current_turn = self.player_1 if self.current_turn == self.player_2 else self.player_2
                return self.board.fen()
            
        except IllegalMoveError as err:
            raise InvalidMoveError(f"The move '{move}' is illegal in the current position.")







# board.push_san('e4') -> makes a move
# legal moves -> board.legal_moves
# Verifying check mate -> board.is_checkmate()
# Verifying stalemate -> board.is_stalemate()
# code -> board.is_check()
