from ..schemas.game import Game
from ..schemas.player import Player

def create_game():
    game = Game()
    return game

game = create_game()

print(game)

    