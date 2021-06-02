from pyarcade.checkers_board import CheckerBoard, is_red_piece, is_black_piece
from itertools import count
import json


class Session:
    _session_id = count(1)

    def __init__(self):
        self.id = next(Session._session_id)
        self.done = False

    def get_id(self) -> int:
        return self.id

    def is_done(self) -> bool:
        return self.done

    def set_to_done(self):
        self.done = True

    @staticmethod
    def serialize(obj):
        if not isinstance(obj, Session):
            return obj.to_json()

        return obj.__dict__

    def to_json(self):
        return json.dumps(self, default=Session.serialize)

    def __repr__(self):
        return self.get_id()


class MastermindSession(Session):
    def __init__(self, sequence: tuple):
        Session.__init__(self)
        self.guesses = []
        self.sequence = sequence

    def get_guesses(self) -> list:
        return self.guesses

    def get_sequence(self) -> tuple:
        return self.sequence

    def insert_guess(self, guess: tuple):
        self.guesses.append(guess)


def html_board(board: str) -> list:
    """
        Args:
            board: takes a str representation of the minesweeper board
        Returns:
            A list that can be interpreted by flask to display properly in html
        Notes:
            This is only used for Minesweeper
    """
    board_list = board.split('\n')
    board_list.pop()
    for row, token in enumerate(board_list):
        board_list[row] = str(row + 1) + "|" + token
    return board_list


class MinesweeperSession(Session):
    def __init__(self, data: dict):
        Session.__init__(self)
        self.data = data

    def is_flagged(self, cell: tuple) -> bool:
        state = self.data["player_board"][cell[0]][cell[1]]
        if state == "flag":
            return True
        return state

    def is_hidden(self, cell: tuple) -> bool:
        state = self.data["player_board"][cell[0]][cell[1]]
        if state == "flag" or False:
            return False
        return True

    def get_data(self) -> dict:
        return self.data


class CheckerSession(Session):
    def __init__(self, game: CheckerBoard):
        Session.__init__(self)
        self.game = game

    def get_game(self) -> CheckerBoard:
        return self.game

    def is_movable_piece(self, piece: tuple) -> bool:
        return self.game.is_movable_piece(piece[0], piece[1])

    def is_valid_move(self, origin: tuple, dest: tuple) -> bool:
        return self.game.is_valid_move_for_piece(origin, dest)

    def is_correct_team_turn(self, loc: tuple) -> bool:
        piece = self.game.get_piece_at(loc[0], loc[1])

        if self.game.is_red_turn():
            return is_red_piece(piece)

        return is_black_piece(piece)

    def __repr__(self):
        return self.get_id()

    def to_json(self):
        return {
            'session_id': self.get_id(),
            'done': self.done,
            'game': self.game.to_json()
        }


class Singleton:
    _instance = None

    @classmethod
    def singleton(cls) -> 'Singleton':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class SessionManager(Singleton):
    """
    Session Manager
    """
    active_sessions = {}

    def __init__(self):
        super(SessionManager, self).__init__()

    def is_checkers_session(self, session_id: int) -> bool:
        return type(self.active_sessions[session_id]) == CheckerSession

    def is_mastermind_session(self, session_id: int) -> bool:
        return type(self.active_sessions[session_id]) == MastermindSession

    def get_session_by_id(self, session_id: int):
        return self.active_sessions[session_id]

    def delete_session(self, session_id: int):
        del self.active_sessions[session_id]
        return {"session_id": session_id}

    def session_exists(self, session_id: int) -> bool:
        return session_id in self.active_sessions

    def session_is_done(self, session_id: int) -> bool:
        return self.get_session_by_id(session_id).is_done()

    def insert_active_session(self, session: Session) -> dict:
        self.active_sessions[session.get_id()] = session
        return {"session_id": session.get_id()}

    def init_mastermind_session(self, sequence: tuple) -> dict:
        return self.insert_active_session(MastermindSession(sequence))

    def init_checkers_session(self, board: CheckerBoard) -> dict:
        return self.insert_active_session(CheckerSession(board))

    def init_minesweeper_session(self, data: dict) -> dict:
        return self.insert_active_session(MinesweeperSession(data))

    def get_sessions_by_type(self, session_type):
        return {session.__repr__(): session.to_json() for session in self.active_sessions.values() if
                type(session) == session_type}
