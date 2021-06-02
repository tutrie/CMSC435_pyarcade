from pyarcade.checker_pieces import OpenPiece
from pyarcade.checkers import Checkers
import unittest
import copy
from pyarcade.session_manager import SessionManager


class CheckersCreateGameTestCase(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}

    def test_create_game_gives_unique_session_id(self):
        session_ids = []
        game = Checkers()
        for idx in range(100):
            session_ids.append(game.create_game({"game_id": 0})["session_id"])

        self.assertEqual(len(set(session_ids)), 100)

    def test_create_game_stores_session_ids(self):
        sessions_created = []
        game = Checkers()
        for idx in range(100):
            sessions_created.append(game.create_game({"game_id": 0})["session_id"])

        session_ids = list(self.session_manager.active_sessions.keys())
        self.assertEqual(session_ids, sessions_created)


class CheckersReadGameTestCase(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}

    def test_read_game_no_moves(self):
        game = Checkers()
        session = game.create_game(({"game_id": 0}))["session_id"]
        reply = game.read_game({"session_id": session})

        correct_board = self.session_manager.get_session_by_id(session).to_json()["game"]["board"]

        self.assertEqual(correct_board, reply["game"]["board"])
        self.assertEqual(session, reply["session_id"])
        self.assertFalse(reply["done"])

    def test_read_game_session_after_moves(self):
        pass

    def test_read_game_session_is_done(self):
        game = Checkers()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        self.session_manager.active_sessions[session_id].done = True

        reply = game.read_game({"session_id": session_id})
        correct_board = self.session_manager.get_session_by_id(session_id).to_json()["game"]

        self.assertEqual(correct_board, reply["game"])
        self.assertEqual(session_id, reply["session_id"])
        self.assertTrue(reply["done"])


class CheckersUpdateGameTestCase(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}

    def test_update_game_moves_pieces(self):
        game = Checkers()
        session_id = game.create_game(({"game_id": 0}))["session_id"]

        board = copy.deepcopy(self.session_manager.get_session_by_id(session_id).to_json()["game"]["board"])

        board[3][2], board[4][1] = board[4][1], board[3][2]
        board[3][2]["row"] = 3
        board[3][2]["col"] = 2
        board[4][1]["row"] = 4
        board[4][1]["col"] = 1

        # before we can update, we need to set the cache..
        session = self.session_manager.get_session_by_id(session_id).get_game()
        session.get_valid_moves(session.get_piece_at(3, 2))

        updated_board = game.update_game({"session_id": session_id, "move": ((3, 2), (4, 1))})["game"]["board"]

        self.assertTrue(board[3][2] == updated_board[3][2])
        self.assertTrue(board[4][1] == updated_board[4][1])

    def test_update_game_removes_jumped_pieces(self):
        game = Checkers()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        checkers = self.session_manager.get_session_by_id(session_id).get_game()

        # need to call these so the cache gets set for jumps and setup a piece to jump
        red_piece = checkers.get_piece_at(3, 2)
        checkers.move_piece_to((6, 3), (4, 3))
        checkers.get_valid_moves(red_piece)

        game.update_game({"session_id": session_id, "move": ((3, 2), (5, 4))})
        updated_board = self.session_manager.get_session_by_id(session_id).get_game().get_board()

        self.assertEqual(type(updated_board[4][3]), OpenPiece)

    def test_update_game_winner_sets_session_to_done(self):
        game = Checkers()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        checkers = self.session_manager.get_session_by_id(session_id).get_game()

        # need to call these so the cache gets set for jumps and setup a piece to jump
        red_piece = checkers.get_piece_at(3, 2)
        checkers.move_piece_to((6, 3), (4, 3))
        checkers.get_valid_moves(red_piece)
        checkers.black_left = 1

        reply = game.update_game({"session_id": session_id, "move": ((3, 2), (5, 4))})

        self.assertTrue(reply["done"])


class CheckersDeleteGameTestCase(unittest.TestCase):
    def test_delete_game_returns_correct_id(self):
        game = Checkers()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        self.assertEqual(session_id, game.delete_game({"session_id": session_id})["session_id"])

    def test_delete_game_returns_correct_id_every_time(self):
        game = Checkers()
        session_id_list = [game.create_game(({"game_id": 0}))["session_id"] for idx in range(0, 100)]

        for session_id in session_id_list:
            self.assertEqual(session_id, game.delete_game({"session_id": session_id})["session_id"])

    def test_delete_game_removes_session_from_list(self):
        game = Checkers()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        game.delete_game({"session_id": session_id})
        self.assertFalse(session_id in SessionManager.active_sessions)

    def test_delete_game_removes_multiple_sessions_from_list(self):
        game = Checkers()
        session_id_list = [game.create_game(({"game_id": 0}))["session_id"] for idx in range(0, 100)]

        for session_id in session_id_list:
            game.delete_game({"session_id": session_id})["session_id"]
            self.assertFalse(session_id in SessionManager.active_sessions)


class CheckersOperationSequenceTestCase(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}

    def test_read_game_returns_updated_values_after_update_game(self):
        game = Checkers()
        session_id = game.create_game(({"game_id": 0}))["session_id"]

        # before we can update, we need to set the cache..
        session = self.session_manager.get_session_by_id(session_id).get_game()
        session.get_valid_moves(session.get_piece_at(3, 2))

        updated_board = game.update_game({"session_id": session_id, "move": ((3, 2), (4, 1))})["game"]["board"]
        read_board = game.read_game({"session_id": session_id})["game"]["board"]

        self.assertEqual(updated_board, read_board)

    def test_read_game_returns_updated_values_after_game_done(self):
        game = Checkers()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        checkers = self.session_manager.get_session_by_id(session_id).get_game()

        # need to call these so the cache gets set for jumps and setup a piece to jump
        red_piece = checkers.get_piece_at(3, 2)
        checkers.move_piece_to((6, 3), (4, 3))
        checkers.get_valid_moves(red_piece)
        checkers.black_left = 1

        update_reply = game.update_game({"session_id": session_id, "move": ((3, 2), (5, 4))})
        read_reply = game.read_game({"session_id": session_id})

        self.assertEqual(update_reply, read_reply)


class CheckersMultipleSessionsTestCase(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}

    def test_multiple_games_see_created_session(self):
        game_one = Checkers()
        game_two = Checkers()

        session_id = game_one.create_game({"game_id": 0})["session_id"]
        session_id_two = game_two.create_game({"game_id": 0})["session_id"]
        self.assertTrue(session_id in self.session_manager.active_sessions)
        self.assertTrue(session_id_two in self.session_manager.active_sessions)

    def test_multiple_games_can_see_session_update(self):
        game_one = Checkers()
        game_two = Checkers()
        session_id = game_one.create_game({"game_id": 0})["session_id"]

        checker_board = self.session_manager.get_session_by_id(session_id).get_game()
        checker_board.get_valid_moves(checker_board.get_piece_at(3, 2))

        game_two.update_game({"session_id": session_id, "move": ((3, 2), (4, 1))})["game"]["board"]

        read_one_reply = game_one.read_game({"session_id": session_id})
        read_two_reply = game_two.read_game({"session_id": session_id})

        self.assertEqual(read_one_reply, read_two_reply)

    def test_multiple_games_can_see_session_deletes(self):
        game_one = Checkers()

        session_id = game_one.create_game({"game_id": 0})["session_id"]

        game_one.delete_game({"session_id": session_id})

        self.assertFalse(session_id in self.session_manager.active_sessions)

    def test_multiple_games_read_update_delete_multiple_sessions(self):
        game_instance_one = Checkers()
        game_instance_two = Checkers()

        session_one = game_instance_one.create_game({"game_id": 0})["session_id"]
        session_two = game_instance_two.create_game({"game_id": 0})["session_id"]

        checkers_one = self.session_manager.get_session_by_id(session_one)
        checkers_two = self.session_manager.get_session_by_id(session_two)

        board_one = checkers_one.to_json()
        board_two = checkers_two.to_json()

        # read game session two from game one and vice versa
        game_one_read_session_two = game_instance_one.read_game({"session_id": session_two})
        game_two_read_session_one = game_instance_two.read_game({"session_id": session_one})

        # both are empty
        self.assertEqual(board_two, game_one_read_session_two)
        self.assertEqual(board_one, game_two_read_session_one)

        # game_instance_one updates session two and correctly guesses sequence
        checkers_two.get_game().get_valid_moves(checkers_two.get_game().get_piece_at(3, 2))

        game_one_update_two_request = {"session_id": session_two, "move": ((3, 2), (4, 1))}
        game_one_update_two_reply = game_instance_one.update_game(game_one_update_two_request)
        game_two_read_one_move_reply = game_instance_two.read_game({"session_id": session_two})

        self.assertEqual(game_one_update_two_reply, game_two_read_one_move_reply)

        # game_instance_two deletes session two out of fury
        delete_reply = game_instance_two.delete_game({"session_id": session_two})
        self.assertEqual(delete_reply, {"session_id": session_two})

        # game_session_two deletes session one out of fury (somehow)
        delete_reply = game_instance_two.delete_game({"session_id": session_one})
        self.assertEqual(delete_reply, {"session_id": session_one})

        self.assertEqual(0, len(SessionManager.active_sessions))
