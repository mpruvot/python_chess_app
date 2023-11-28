from chess_app.chess_engine import GameOfChess
from custom_errors.custom_errors import (
    GameAlreadyStartedError,
    GameNotFoundError,
    NotActiveGameError,
)
from database_services.strapi_api_service import StrapiApiService


api_service = StrapiApiService()


def start_new_game(game_uuid: str):
    """Starts a Game if two players joined the Game, init an FEN code to the Game instance

    Args:
        game_uuid (str): Uuid of the Game
    """
    
    ### Here to avoid circular import
    from management_services.game_services import retrieve_single_game
    ###

    game = retrieve_single_game(game_uuid)
    if game.fen:
        raise GameAlreadyStartedError(f"Game already started with fen : {game.fen}")
    if len(game.players) != 2:
        raise NotActiveGameError(
            f"Not enough Players in the Game: {len(game.players)} joined"
        )
    try:
        player_1 = game.players[0].name
        player_2 = game.players[1].name
        chess_engine = GameOfChess(name_player_1=player_1, name_player_2=player_2)
        fen = chess_engine.return_fen()
        game.is_active = True
        updated_game = api_service.update_fen_of_game(game=game, fen=fen)
        return updated_game

    except GameNotFoundError:
        raise GameNotFoundError(f"No game found with UUID: {game_uuid}")


def make_a_move(game_uuid: str, player_name: str, move: str) -> str:
    game = retrieve_single_game(game_uuid)
    if not game.is_active:
        raise NotActiveGameError(
            f"Not enough Players in the Game: {len(game.players)} joined"
        )

    chess_engine = GameOfChess(
        name_player_1=game.players[0].name, name_player_2=game.players[1].name
    )
    pass
