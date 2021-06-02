from pyarcade.game_interface import GameInterface
from pyarcade.mastermind import MastermindGame
from pyarcade.minesweeper_builder import MinesweeperBoardBuilder
from pyarcade.session_manager import SessionManager
from pyarcade.checkers import Checkers
from pyarcade.minesweeper import MinesweeperGame
from pyarcade.game_ids import *


class GameProxy(GameInterface):
    game_id_map = {MASTERMIND_ID: MastermindGame, CHECKERS_ID: Checkers, MINESWEEPER_ID: MinesweeperGame}

    def __init__(self, game_instance: GameInterface):
        self.game_instance = game_instance
        self.session_manager = SessionManager.singleton()

    def create_game(self, request):
        """
                Args:
                    request: dictionary containing single key-value pair. The key is "game_id". The value
                    should be zero.

                Returns:
                    reply: dictionary containing a single key-value pair. The key is "session_id". The value is a
                    integer unique to all ongoing game sessions. If the request is invalid, a session_id of
                    zero should be returned. Otherwise, pass the request onto the game.
                """
        if request is None \
                or not self.request_correct_size(request, 1) \
                or not self.key_present(request, "game_id") \
                or not self.correct_type(request, "game_id", int()) \
                or not self.valid_game_id(request["game_id"]):
            return {"session_id": 0}

        return self.game_instance.create_game(request)

    def read_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary containing single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing game sessions.

        Returns:
            reply: dictionary containing a single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing game sessions. If the request is invalid, a session_id of
            zero should be returned. Otherwise, pass the request onto the game.
        """

        if not self.valid_session_request(request):
            return {"session_id": 0}

        return self.game_instance.read_game(request)

    def delete_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary containing single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing game sessions.

        Returns:
            reply: dictionary containing single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing game sessions. If the session_id is invalid, then a session_id of
            zero is returned. Otherwise, pass the request onto the game.
        """
        if not self.valid_session_request(request):
            return {"session_id": 0}

        return self.game_instance.delete_game(request)

    def update_game(self, request: dict) -> dict:
        raise NotImplemented

    def session_exists(self, request: dict) -> bool:
        return self.session_manager.session_exists(request["session_id"])

    def session_is_done(self, request: dict) -> bool:
        return self.session_manager.session_is_done(request["session_id"])

    def valid_session_request(self, request: dict, request_size=1) -> bool:
        return request is not None \
               and GameProxy.request_correct_size(request, request_size) \
               and GameProxy.key_present(request, "session_id") \
               and GameProxy.correct_type(request, "session_id", int()) \
               and self.session_exists(request)

    @staticmethod
    def tuple_contains_only_int_type(tup_in: tuple) -> bool:
        for val in tup_in:
            if type(val) != int:
                return False

        return True

    @staticmethod
    def input_in_valid_range(tup_in: tuple, _min=1, _max=9) -> bool:
        for val in tup_in:
            if val < _min or val > _max:
                return False

        return True

    @staticmethod
    def request_correct_size(request: dict, max_size: int) -> bool:
        return len(request) == max_size

    @staticmethod
    def correct_type(request: dict, key: str, type_we_want) -> bool:
        return type(request[key]) == type(type_we_want)

    @staticmethod
    def key_present(request: dict, key: str) -> bool:
        return key in request

    def valid_game_id(self, game_id: int) -> bool:
        return game_id in GameProxy.game_id_map \
               and type(self.game_instance) == GameProxy.game_id_map[game_id]

    @staticmethod
    def tuple_correct_size(tup_in: tuple, size: int, is_unique=False) -> bool:
        if is_unique:
            tup_in = set(tup_in)

        return len(tup_in) == size


class MastermindGameProxy(GameProxy):

    def __init__(self, game_instance: MastermindGame):
        GameProxy.__init__(self, game_instance)

    def update_game(self, request: dict) -> dict:
        """
                Args:
                    request: dictionary containing two key-value pairs. One key is "session_id". The value is a
                    integer unique to all ongoing game sessions. The second key is "guess." The value should be a tuple
                    of four integers.

                Returns:
                    reply: dictionary containing a single key-value pair. The key is "session_id". The value is a
                    integer unique to all ongoing game sessions. If the request is invalid, a session_id of
                    zero should be returned. Otherwise, pass the request onto the game.
                """

        # guess should only be allowed if it is between 0 and 9
        if not self.valid_session_request(request, request_size=2) \
                or self.session_is_done(request) \
                or not self.valid_update_request(request):
            return {"session_id": 0}

        return self.game_instance.update_game(request)

    def valid_update_request(self, request: dict) -> bool:
        return self.key_present(request, "guess") \
               and self.correct_type(request, "guess", tuple()) \
               and self.tuple_contains_only_int_type(request["guess"]) \
               and self.tuple_correct_size(request["guess"], 4, is_unique=True) \
               and self.input_in_valid_range(request["guess"])


class CheckersProxy(GameProxy):

    def __init__(self, game_instance: Checkers):
        GameProxy.__init__(self, game_instance)

    def update_game(self, request: dict) -> dict:
        """
                Args:
                    request: dictionary containing two key-value pairs. One key is "session_id". The value is a
                    integer unique to all ongoing game sessions. The second key is "guess." The value should be a tuple
                    of four integers.

                Returns:
                    reply: dictionary containing a single key-value pair. The key is "session_id". The value is a
                    integer unique to all ongoing game sessions. If the request is invalid, a session_id of
                    zero should be returned. Otherwise, pass the request onto the game.
                """

        if not self.valid_session_request(request, request_size=2) \
                or not self.valid_update_request(request):
            return {"session_id": 0}

        return self.game_instance.update_game(request)

    def valid_update_request(self, request: dict) -> bool:
        return self.key_present(request, "move") \
            and self.correct_type(request, "move", tuple()) \
            and self.tuple_correct_size(request["move"], 2) \
            and self.tuple_correct_size(request["move"][0], 2) \
            and self.tuple_correct_size(request["move"][1], 2) \
            and self.tuple_contains_only_int_type(request["move"][0]) \
            and self.tuple_contains_only_int_type(request["move"][1]) \
            and self.input_in_valid_range(request["move"][0]) \
            and self.input_in_valid_range(request["move"][1]) \
            and self.valid_checkers_move(request)

    def valid_checkers_move(self, request: dict) -> bool:
        game = self.session_manager.get_session_by_id(request["session_id"])
        origin, dest = request["move"]

        return game.is_movable_piece(origin) \
            and game.is_correct_team_turn(origin) \
            and game.is_valid_move(origin, dest)


class MinesweeperProxy(GameProxy):
    def __init__(self, game_instance: MinesweeperGame):
        GameProxy.__init__(self, game_instance)

    def update_game(self, request: dict) -> dict:
        """
                Args:
                    request: dictionary containing two key-value pairs. One key is "session_id". The value is a
                    integer unique to all ongoing game sessions. The second key is "guess." The value should be a tuple
                    of four integers.

                Returns:
                    reply: dictionary containing a single key-value pair. The key is "session_id". The value is a
                    integer unique to all ongoing game sessions. If the request is invalid, a session_id of
                    zero should be returned. Otherwise, pass the request onto the game.
                """

        if not self.valid_session_request(request, request_size=2) \
                or not self.valid_update_request(request):
            return {"session_id": 0}

        return self.game_instance.update_game(request)

    def valid_update_request(self, request: dict) -> bool:
        """
        Args:
            request: Should be a dictionary containing two key-value pairs. One key is "session_id". The value is a
            integer. The second key is "unhide_cell." or "flag_cell" The value should be a tuple of the location.
            Locations should be store as positive integers in (row, column) from 0 to 8.

        Returns: True if request contains a dictionary with the correct two key-value pairs
        """

        if self.key_present(request, "flag_cell"):
            return self.validate_flag(request)

        if self.key_present(request, "unhide_cell"):
            return self.validate_unhide(request)

        return False

    def validate_flag(self, request: dict) -> bool:
        return self.correct_type(request, "flag_cell", tuple()) \
            and self.tuple_contains_only_int_type(request["flag_cell"]) \
            and self.tuple_correct_size(request["flag_cell"], 2) \
            and self.input_in_valid_range(request["flag_cell"], _min=0, _max=MinesweeperBoardBuilder.EASY_SIZE) \
            and not self.session_is_done(request) \
            and self.session_manager.get_session_by_id(request["session_id"]).is_flagged(request["flag_cell"])

    def validate_unhide(self, request: dict) -> bool:
        return self.correct_type(request, "unhide_cell", tuple()) \
            and self.tuple_correct_size(request["unhide_cell"], 2) \
            and self.tuple_contains_only_int_type(request["unhide_cell"]) \
            and self.input_in_valid_range(request["unhide_cell"], _min=0, _max=MinesweeperBoardBuilder.EASY_SIZE) \
            and not self.session_is_done(request) \
            and self.session_manager.get_session_by_id(request["session_id"]).is_hidden(request["unhide_cell"])
