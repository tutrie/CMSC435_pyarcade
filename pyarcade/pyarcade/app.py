from flask import Flask, request

from pyarcade.minesweeper import MinesweeperGame
from pyarcade.checkers import Checkers
from pyarcade.mastermind import MastermindGame
from pyarcade.proxy import MastermindGameProxy, CheckersProxy, MinesweeperProxy
from pyarcade.session_manager import SessionManager
from pyarcade.json_decoders import *


def create_app():
    app = Flask(__name__)
    session_manager = SessionManager()

    games = {
        "mastermind": {
            "proxy": MastermindGameProxy(game_instance=MastermindGame()),
            "game_type": MastermindGame,
            "_json_decoder": json_tuple_decoder,
            "_tuple_depth": 1
        },
        "checkers": {
            "proxy": CheckersProxy(game_instance=Checkers()),
            "game_type": Checkers,
            "_json_decoder": json_tuple_decoder,
            "_tuple_depth": 2
        },
        "minesweeper": {
            "proxy": MinesweeperProxy(game_instance=MinesweeperGame()),
            "game_type": MinesweeperGame,
            "_json_decoder": json_tuple_decoder,
            "_tuple_depth": 1
        }
    }

    main_menu = {"mastermind": "/game/mastermind", "checkers": "/game/checkers", "minesweeper": "/game/minesweeper"}

    @app.route("/")
    def home():
        return {"menu": main_menu}

    @app.route("/create/<string:game_name>", methods=["POST"])
    def create_game_session(game_name):
        if game_name not in games:
            return main_menu, 404

        reply = games[game_name]["proxy"].create_game(request.json)
        reply["menu"] = build_menu(game_name)

        return reply

    @app.route("/game/<string:game_name>", methods=["GET"])
    def read_game_sessions(game_name):
        if game_name not in games:
            return main_menu, 404

        active_sessions = session_manager.get_sessions_by_type(games[game_name]["game_type"])
        return {"menu": build_menu(game_name), "active_sessions": active_sessions}

    @app.route("/play/<string:game_name>", methods=["GET"])
    def play_game_session(game_name):
        if game_name not in games:
            return main_menu, 404

        reply = games[game_name]["proxy"].read_game(request.json)
        reply["menu"] = build_menu(game_name)

        return reply

    @app.route("/update/<string:game_name>", methods=["POST"])
    def update_game_session(game_name):
        if game_name not in games:
            return main_menu, 404

        game = games[game_name]
        update = game["_json_decoder"](request.json, game["_tuple_depth"])

        reply = games[game_name]["proxy"].update_game(update)
        reply["menu"] = build_menu(game_name)

        return reply

    @app.route("/delete/<string:game_name>", methods=["POST"])
    def delete_game_session(game_name):
        if game_name not in games:
            return main_menu, 404

        reply = games[game_name]["proxy"].delete_game(request.json)
        reply["menu"] = build_menu(game_name)

        return reply

    def build_menu(game_name: str) -> dict:
        return {"home": "/", "create": f"/create/{game_name}", "play": f"/play/{game_name}",
                "delete": f"/delete/{game_name}",
                "update": f"/update/{game_name}"}

    return app
