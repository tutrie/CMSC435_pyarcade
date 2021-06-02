from itertools import count

from pyarcade.minesweeper import MinesweeperGame
from pyarcade.minesweeper_builder import MinesweeperBoardBuilder
from pyarcade.session_manager import SessionManager, Session
import unittest

FOUR_CORNERS_BOARD_SOLN = {0: ['mine'] + [1] + [0] * 5 + [1] + ['mine'], 1: [1, 1] + [0] * 5 + [1, 1], 2: [0] * 9,
                           3: [0] * 9, 4: [0] * 9, 5: [0] * 9, 6: [0] * 9, 7: [1, 1] + [0] * 5 + [1, 1],
                           8: ['mine'] + [1] + [0] * 5 + [1] + ['mine']}


class MinesweeperTestInitialize(unittest.TestCase):
    session = MinesweeperGame()
    builder = MinesweeperBoardBuilder()

    def test_initialize_board(self):
        try:
            board, mines = MinesweeperTestInitialize.builder.initialize_board()
            MinesweeperGame.print_board(board)
            # If it ran the above functions without issue pass the test
            self.assertEqual(True, True)
        except IndexError:
            # force to assert false if code didn't pass initialize or print
            self.assertEqual(True, False)
        except KeyError:
            self.assertEqual(True, False)

    def test_initialize_fails_four_corners(self):
        four_corners_board = {0: ['mine'] + [0]*7 + ['mine'], 1: [0]*9, 2: [0]*9, 3: [0]*9, 4: [0]*9,
                              5: [0]*9, 6: [0]*9, 7: [0]*9, 8: ['mine'] + [0]*7 + ['mine']}
        mines = [(0, 0), (8, 8), (0, 8), (8, 0)]
        result = MinesweeperBoardBuilder.count_adjacent_mines(mines, four_corners_board)
        self.assertEqual(result, FOUR_CORNERS_BOARD_SOLN)

    def test_magic_eight(self):
        eight_adjacent_bombs = {0: ['mine', 'mine', 'mine'] + [0]*6, 1: ['mine'] + [0] + ['mine'] + [0]*6,
                                2: ['mine', 'mine', 'mine'] + [0]*6, 3: [0]*9, 4: [0]*9, 5: [0]*9, 6: [0]*9,
                                7: [0]*9, 8: [0]*9}
        mines = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
        eight_adjacent_bombs_soln = {0: ['mine', 'mine', 'mine'] + [2] + [0]*5,
                                     1: ['mine'] + [8] + ['mine'] + [3] + [0]*5,
                                     2: ['mine', 'mine', 'mine'] + [2] + [0]*5,
                                     3: [2, 3, 2, 1] + [0]*5, 4: [0]*9, 5: [0]*9, 6: [0]*9, 7: [0]*9, 8: [0]*9}
        result = MinesweeperBoardBuilder.count_adjacent_mines(mines, eight_adjacent_bombs)
        self.assertEqual(result, eight_adjacent_bombs_soln)


class MinesweeperTestBasicGame(unittest.TestCase):
    instance = MinesweeperGame()

    @classmethod
    def setUpClass(cls):
        SessionManager.active_sessions = {}
        Session._session_id = count(1)

    def setUp(self):
        self.session_manager = SessionManager()

    def test_add_session(self):
        session_ids = []
        for idx in range(4):
            session_ids.append(self.instance.create_game({}))
        self.assertEqual(len(session_ids), 4)

    def test_print_hidden_board(self):
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 \n'
        board = ""
        for idx in range(9):
            board += line
        session_1 = self.session_manager.active_sessions[1]
        board_to_print = MinesweeperGame.print_player_board(session_1.data["player_board"], session_1.data["board"])
        self.assertEqual(board, board_to_print)

    def test_flag_cell(self):
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 \n'
        board = ""
        for idx in range(8):
            board += line
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 F \n'
        board += line
        session_2 = self.session_manager.active_sessions[2]
        self.instance.flag_cell((8, 8), session_2)
        board_to_print = MinesweeperGame.print_player_board(session_2.data["player_board"], session_2.data["board"])
        self.assertEqual(board, board_to_print)

    def test_unflag_cell(self):
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 \n'
        board = ""
        for idx in range(9):
            board += line
        session_3 = self.session_manager.active_sessions[3]
        self.instance.flag_cell((8, 8), session_3)
        self.instance.flag_cell((8, 8), session_3)
        board_to_print = MinesweeperGame.print_player_board(session_3.data["player_board"], session_3.data["board"])
        self.assertEqual(board, board_to_print)

    def test_unhide_cell(self):
        self.instance.create_game({})
        session_4 = self.session_manager.active_sessions[4].data
        session_4["board"] = FOUR_CORNERS_BOARD_SOLN
        session_4 = self.session_manager.active_sessions[4]
        self.instance.unhide_cell((8, 7), session_4)
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 \n'
        board = ""
        for idx in range(8):
            board += line
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 1 🬅 \n'
        board += line
        board_to_print = MinesweeperGame.print_player_board(session_4.data["player_board"], session_4.data["board"])
        self.assertEqual(board, board_to_print)

    def test_end_game(self):
        self.instance.create_game({})
        session_4 = self.session_manager.active_sessions[4].data
        session_4["board"] = FOUR_CORNERS_BOARD_SOLN
        session_4 = self.session_manager.active_sessions[4]
        self.instance.unhide_cell((8, 8), session_4)
        session_4 = self.session_manager.get_session_by_id(4)
        self.assertEqual(session_4.is_done(), True)


class MinesweeperTestReadCreateGame(unittest.TestCase):
    instance = MinesweeperGame()

    @classmethod
    def setUpClass(cls):
        SessionManager.active_sessions = {}
        Session._session_id = count(1)

    def setUp(self):
        self.session_manager = SessionManager()

    def test_create_game(self):
        prev_number_of_sessions = len(set(self.session_manager.active_sessions))
        session_ids = []
        for idx in range(3):
            session_ids.append(self.instance.create_game({})["session_id"])
        number_of_sessions = len(set(self.session_manager.active_sessions))
        self.assertEqual(number_of_sessions, prev_number_of_sessions+3)

    def test_end_game_lose(self):
        board = ""
        line = 'x 🬅 🬅 🬅 🬅 🬅 🬅 🬅 F \n'
        board += line
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 \n'
        for idx in range(7):
            board += line
        line = 'x 🬅 🬅 🬅 🬅 🬅 0 1 x \n'
        board += line
        session_1 = self.session_manager.active_sessions[1].data
        session_1["board"] = FOUR_CORNERS_BOARD_SOLN
        session_1 = self.session_manager.active_sessions[1]
        MinesweeperTestReadCreateGame.instance.unhide_cell((8, 7), session_1)
        MinesweeperTestReadCreateGame.instance.unhide_cell((8, 6), session_1)
        MinesweeperTestReadCreateGame.instance.flag_cell((0, 8), session_1)
        MinesweeperTestReadCreateGame.instance.unhide_cell((8, 8), session_1)
        reply = MinesweeperTestReadCreateGame.instance.read_game({"session_id": 1})
        board_to_print = reply["board"]
        self.assertEqual(board, board_to_print)

    def test_read_game_not_done(self):
        board = ""
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 F \n'
        board += line
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 \n'
        for idx in range(7):
            board += line
        line = '🬅 🬅 🬅 🬅 🬅 🬅 0 1 🬅 \n'
        board += line
        session_2 = self.session_manager.active_sessions[2].data
        session_2["board"] = FOUR_CORNERS_BOARD_SOLN
        session_2 = self.session_manager.active_sessions[2]
        MinesweeperTestReadCreateGame.instance.unhide_cell((8, 7), session_2)
        MinesweeperTestReadCreateGame.instance.unhide_cell((8, 6), session_2)
        MinesweeperTestReadCreateGame.instance.flag_cell((0, 8), session_2)
        testing = self.session_manager.active_sessions[2].data["player_board"]
        reply = MinesweeperTestReadCreateGame.instance.read_game({"session_id": 2})
        board_to_print = reply["board"]
        self.assertEqual(board, board_to_print)

    def test_flags_decrement(self):
        session_3 = self.session_manager.active_sessions[3]
        MinesweeperTestReadCreateGame.instance.flag_cell((0, 8), session_3)
        reply = MinesweeperTestReadCreateGame.instance.read_game({"session_id": 3})
        num_flags = reply["flags"]
        self.assertEqual(9, num_flags)

    def test_flags_increment(self):
        session_3 = self.session_manager.active_sessions[3]
        MinesweeperTestReadCreateGame.instance.flag_cell((0, 8), session_3)
        reply = MinesweeperTestReadCreateGame.instance.read_game({"session_id": 3})
        num_flags = reply["flags"]
        self.assertEqual(10, num_flags)


class MinesweeperTestUpdateDeleteGame(unittest.TestCase):
    instance = MinesweeperGame()

    @classmethod
    def setUpClass(cls):
        SessionManager.active_sessions = {}
        Session._session_id = count(1)

    def setUp(self):
        self.session_manager = SessionManager()

    def test_create_game(self):
        session_ids = []
        for idx in range(5):
            session_ids.append(MinesweeperTestUpdateDeleteGame.instance.create_game({})["session_id"])
        self.assertEqual(len(session_ids), 5)

    def test_update(self):
        board = ""
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 F \n'
        board += line
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 \n'
        for idx in range(7):
            board += line
        line = '🬅 🬅 🬅 🬅 🬅 🬅 0 1 🬅 \n'
        board += line
        session_1 = self.session_manager.active_sessions[5].data
        session_1["board"] = FOUR_CORNERS_BOARD_SOLN
        MinesweeperTestUpdateDeleteGame.instance.update_game({"session_id": 5, "unhide_cell": (8, 7)})
        MinesweeperTestUpdateDeleteGame.instance.update_game({"session_id": 5, "unhide_cell": (8, 6)})
        reply = MinesweeperTestUpdateDeleteGame.instance.update_game({"session_id": 5, "flag_cell": (0, 8)})
        board_to_print = reply["board"]
        self.assertEqual(board_to_print, board)

    def test_delete(self):
        prev_number_of_sessions = len(set(self.session_manager.active_sessions))
        MinesweeperTestUpdateDeleteGame.instance.delete_game({"session_id": 2})
        number_of_sessions = len(set(self.session_manager.active_sessions))
        self.assertEqual(number_of_sessions, prev_number_of_sessions-1)

    def test_delete_return(self):
        session_id = MinesweeperTestUpdateDeleteGame.instance.delete_game({"session_id": 3})
        self.assertEqual(3, session_id["session_id"])
