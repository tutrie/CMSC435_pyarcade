from itertools import count

from pyarcade.checkers import Checkers
from pyarcade.minesweeper import MinesweeperGame
from pyarcade.proxy import MastermindGameProxy, GameProxy, CheckersProxy, MinesweeperProxy
from pyarcade.mastermind import MastermindGame
from pyarcade.session_manager import SessionManager, Session
import unittest

from pyarcade.game_ids import *


class ProxyCreateGameMastermindTestCase(unittest.TestCase):
    def test_create_game_gives_unique_sequence(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        id_one = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]
        id_two = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]

        seq_one = game.session_manager.get_session_by_id(id_one).get_sequence()
        seq_two = game.session_manager.get_session_by_id(id_two).get_sequence()

        self.assertNotEqual(seq_one, seq_two)


class ProxyCreateGameTestCase(unittest.TestCase):
    def setUp(self):
        """Set MastermindGame instances to be INDEPENDENT between tests"""
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}

    def test_create_game_request_has_wrong_type_value_or_key(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        reply = proxy.create_game({"game_id": "string"})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.create_game({"game_id": 1.0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.create_game({"game_id": {}})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.create_game({"game_id": []})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.create_game({"game_id": False})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.create_game({"game_id": None})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.create_game({"game_id": (0, 0)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.create_game({1: 0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.create_game({None: 0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.create_game({1.0: 0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.create_game({("game_id", "game_id"): 0})
        self.assertEqual(reply["session_id"], 0)

        self.assertTrue(len(self.session_manager.active_sessions) == 0)

    def test_create_game_request_dict_wrong_size(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        reply = proxy.create_game({"game_id": "0", "key": 0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.create_game({})
        self.assertEqual(reply["session_id"], 0)

    def test_create_game_incorrect_inputs(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        reply = proxy.create_game({"game_id": 1})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.create_game(None)
        self.assertEqual(reply["session_id"], 0)


class ProxyReadGameTestCase(unittest.TestCase):
    def setUp(self):
        """Set MastermindGame instances to be INDEPENDENT between tests"""
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}

    def test_read_game_request_has_wrong_type_value_or_key(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        reply = proxy.read_game({"session_id": "string"})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.read_game({"session_id": 1.0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.read_game({"session_id": {}})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.read_game({"session_id": []})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.read_game({"session_id": False})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.read_game({"session_id": None})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.read_game({"session_id": (0, 0)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.read_game({1: 0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.read_game({None: 0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.read_game({1.0: 0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.read_game({("session_id", "session_id"): 0})
        self.assertEqual(reply["session_id"], 0)

    def test_read_game_request_dict_wrong_size(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        reply = proxy.read_game({"session_id": "0", "key": 0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.read_game({})
        self.assertEqual(reply["session_id"], 0)

    def test_read_game_incorrect_inputs(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        reply = proxy.read_game({"session_id": "100"})
        self.assertEqual(reply["session_id"], 0)

        session_id = proxy.create_game({"game_id": 0})["session_id"]
        reply = proxy.read_game({"session_id": session_id + 1})
        self.assertEqual(reply["session_id"], 0)

    def test_read_mastermind_game_with_created_session_id(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]

        reply = proxy.read_game({"session_id": session_id})
        self.assertNotEqual(reply["session_id"], 0)

    def test_read_checkers_game_with_created_session_id(self):
        game = Checkers()
        proxy = CheckersProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": CHECKERS_ID})["session_id"]

        reply = proxy.read_game({"session_id": session_id})
        self.assertNotEqual(reply["session_id"], 0)


class ProxyUpdateMastermindGameTestCase(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}

    def test_update_game_request_has_wrong_type_value_or_key(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)
        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]

        reply = proxy.update_game({"session_id": 1.0, "guess": (1, 2, 3, 4)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": "string", "guess": (1, 2, 3, 4)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": (1, 2), "guess": (1, 2, 3, 4)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": [], "guess": (1, 2, 3, 4)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": {}, "guess": (1, 2, 3, 4)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": None, "guess": (1, 2, 3, 4)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": False, "guess": (1, 2, 3, 4)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": None})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": "string"})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": 1.0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": 1})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": {}})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": []})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": False})
        self.assertEqual(reply["session_id"], 0)

    def test_update_game_request_dict_wrong_size(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        reply = proxy.update_game({"session_id": CHECKERS_ID, "key": 0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({})
        self.assertEqual(reply["session_id"], 0)

        request = {"guess": (1, 2, 3, 4)}
        self.assertEqual(proxy.update_game(request)["session_id"], 0)

        request = {"session_id": 0}
        self.assertEqual(proxy.update_game(request)["session_id"], 0)

    def test_update_game_incorrect_inputs(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]
        request = {"guess": (1, 2, 3, 4)}

        self.assertEqual(proxy.update_game(request)["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": (1, 2, 3, "4")})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": (1, 2, 3, 4.0)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": (1, 2, 3, [])})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": (1, 2, 3, {})})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": (1, 2, 3, None)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": (1, 2, 3, False)})
        self.assertEqual(reply["session_id"], 0)

        request = {"session_id": session_id, "other_key": (1, 2, 3, 4)}
        self.assertEqual(proxy.update_game(request)["session_id"], 0)

        request = {"other key": session_id, "guess": (1, 2, 3, 4)}
        self.assertEqual(proxy.update_game(request)["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": (1, 2, 3, -4)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": (1, 2, 3, 10)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": (1, 1, 1, 1)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": (1, 2, 3, 4, 5)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "guess": (1, 2, 3)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": 170, "guess": (1, 2, 3, 4)})
        self.assertEqual(reply["session_id"], 0)

    def test_update_game_first_guess_wins_second_guess_rejected(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game(({"game_id": MASTERMIND_ID}))["session_id"]
        self.session_manager.active_sessions[session_id].sequence = [1, 2, 3, 5]

        first_request = {"session_id": session_id, "guess": (1, 2, 3, 5)}
        second_request = {"session_id": session_id, "guess": (2, 4, 5, 9)}

        # will and set session to done and second_guess will be rejected
        proxy.update_game(first_request)
        self.assertEqual(proxy.update_game(second_request)["session_id"], 0)

    def test_update_game_rejected_when_session_is_done(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = game.create_game({"game_id": MASTERMIND_ID})["session_id"]
        self.session_manager.active_sessions[session_id].done = True

        reply = proxy.update_game({"session_id": session_id, "guess": (1, 2, 3, 4)})
        self.assertEqual(reply["session_id"], 0)

    def test_update_game_with_created_session_id(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]
        guess = (1, 2, 3, 4)
        update = proxy.update_game({"session_id": session_id, "guess": guess})

        self.assertFalse(update["session_id"] == 0)


class ProxyUpdateCheckersTestCase(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}

    def test_update_game_request_has_wrong_type_value_or_key(self):
        game = Checkers()
        proxy = CheckersProxy(game_instance=game)
        session_id = proxy.create_game({"game_id": CHECKERS_ID})["session_id"]

        reply = proxy.update_game({"session_id": 1.0, "move": ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": "string", "move": ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": (1, 2), "move": ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": [], "move": ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": {}, "move": ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": None, "move": ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": False, "move": ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": 1})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": 1.0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": "string"})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": []})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": {}})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": False})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": None})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({1: session_id, "move": ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, 1: ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({True: session_id, "move": ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, True: ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({1.0: session_id, "move": ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, 1.0: ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({("session_id", "session"): session_id, "move": ((1, 2), (3, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, ("move", "p"): ((1, 2), (2, 3))})
        self.assertEqual(reply["session_id"], 0)

    def test_update_game_request_dict_wrong_size(self):
        game = Checkers()
        proxy = CheckersProxy(game_instance=game)

        reply = proxy.update_game({"session_id": CHECKERS_ID})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": 1, "move": ((1, 2), (3, 2)), "extra": 123})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({})
        self.assertEqual(reply["session_id"], 0)

    def test_update_game_incorrect_inputs(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]
        request = {"guess": (1, 2, 3, 4)}

        self.assertEqual(proxy.update_game(request)["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": ((1, 2, 3), (1, 2))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": ((1, 2), 1)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": ((3, 4.0), (5, 6))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": ((3, 4), (5, "6"))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": ((3, 4), (5, []))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": ((3, 4), (5, {}))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": ((3, 4), (5, False))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": ((3, 4), (5, None))})
        self.assertEqual(reply["session_id"], 0)

        request = {"session_id": session_id, "other_key": ((3, 4), (5, 6))}
        self.assertEqual(proxy.update_game(request)["session_id"], 0)

        request = {"other key": session_id, "move": (1, 2, 3, 4)}
        self.assertEqual(proxy.update_game(request)["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": ((3, 4), (5, -6))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": ((3, 4), (5, 10))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": ((3, 4), (5, 6), (7, 8))})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": session_id, "move": (3, 4)})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.update_game({"session_id": 170, "move": ((3, 4), (5, 6))})
        self.assertEqual(reply["session_id"], 0)

    def test_update_game_first_guess_wins_second_guess_rejected(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game(({"game_id": MASTERMIND_ID}))["session_id"]
        self.session_manager.active_sessions[session_id].sequence = [1, 2, 3, 5]

        first_request = {"session_id": session_id, "guess": (1, 2, 3, 5)}
        second_request = {"session_id": session_id, "guess": (2, 4, 5, 9)}

        # will and set session to done and second_guess will be rejected
        proxy.update_game(first_request)
        self.assertEqual(proxy.update_game(second_request)["session_id"], 0)

    def test_update_game_rejected_when_session_is_done(self):
        game = Checkers()
        proxy = CheckersProxy(game_instance=game)

        session_id = game.create_game({"game_id": MASTERMIND_ID})["session_id"]
        self.session_manager.active_sessions[session_id].done = True

        reply = proxy.update_game({"session_id": session_id, "move": ((3, 4), (5, 6))})
        self.assertEqual(reply["session_id"], 0)

    def test_update_game_with_created_session_id(self):
        game = Checkers()
        proxy = CheckersProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": CHECKERS_ID})["session_id"]
        update = proxy.update_game({"session_id": session_id, "move": ((3, 4), (4, 5))})

        self.assertFalse(update["session_id"] == 0)


class ProxyDeleteGameTestCase(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}

    def test_delete_game_request_has_wrong_type_value_or_key(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)
        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]

        request = {"session_id": "string"}
        reply = proxy.delete_game(request)
        self.assertEqual(reply["session_id"], 0)

        request = {"session_id": 1.0}
        reply = proxy.delete_game(request)
        self.assertEqual(reply["session_id"], 0)

        request = {"session_id": []}
        reply = proxy.delete_game(request)
        self.assertEqual(reply["session_id"], 0)

        request = {"session_id": None}
        reply = proxy.delete_game(request)
        self.assertEqual(reply["session_id"], 0)

        request = {"session_id": {}}
        reply = proxy.delete_game(request)
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.delete_game({1: 0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.delete_game({None: 0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.delete_game({1.0: 0})
        self.assertEqual(reply["session_id"], 0)

        reply = proxy.delete_game({("session_id", "session_id"): 0})
        self.assertEqual(reply["session_id"], 0)

    def test_delete_game_request_dict_wrong_size(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]
        request = {"session_id": session_id, "another key": 1}

        self.assertEqual(proxy.delete_game(request)["session_id"], 0)
        self.assertEqual(proxy.delete_game({})["session_id"], 0)

    def test_delete_game_incorrect_inputs(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]
        request = {"wrong_key": session_id}

        self.assertEqual(proxy.delete_game(request)["session_id"], 0)

    def test_delete_game_with_created_session_id(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]
        request = {"session_id": session_id}

        self.assertFalse(proxy.delete_game(request)["session_id"] == 0)

    def test_delete_game_rejected_when_after_session_deleted(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]
        request = {"session_id": session_id}

        self.assertEqual(proxy.delete_game(request)["session_id"], session_id)
        self.assertEqual(proxy.delete_game(request)["session_id"], 0)


class ProxyMastermindSingleSessionGameSequenceTestCase(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}

    def test_read_game_rejected_when_after_session_deleted(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]
        request = {"session_id": session_id}
        proxy.delete_game(request)

        self.assertEqual(proxy.read_game(request)["session_id"], 0)

    def test_update_game_rejected_when_after_session_deleted(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]
        proxy.delete_game({"session_id": session_id})

        update_request = {"session_id": session_id, "guess": (1, 2, 3, 4)}
        self.assertEqual(proxy.update_game(update_request)["session_id"], 0)

    def test_can_read_game_after_session_done(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]
        self.session_manager.active_sessions[session_id].sequence = [1, 2, 3, 4]

        proxy.update_game({"session_id": session_id, "guess": (1, 2, 3, 4)})
        read_reply = proxy.read_game({"session_id": session_id})

        self.assertNotEqual(read_reply["session_id"], 0)

    def test_read_create_read_update_read_delete_read_correct_input(self):
        game = MastermindGame()
        proxy = MastermindGameProxy(game_instance=game)

        read_reply = proxy.read_game({"session_id": 0})
        self.assertEqual(read_reply["session_id"], 0)

        session_id = proxy.create_game({"game_id": MASTERMIND_ID})["session_id"]
        self.session_manager.active_sessions[session_id].sequence = [1, 2, 3, 4]

        read_reply = proxy.read_game({"session_id": session_id})
        self.assertFalse(read_reply["session_id"] == 0)

        update_request = {"session_id": session_id, "guess": (1, 2, 3, 4)}
        update_reply = proxy.update_game(update_request)
        self.assertNotEqual(update_reply["session_id"], 0)

        read_reply = proxy.read_game({"session_id": session_id})
        self.assertNotEqual(0, read_reply["session_id"])

        delete_reply = proxy.delete_game({"session_id": session_id})
        self.assertEqual(delete_reply, {"session_id": session_id})

        read_reply = proxy.read_game({"session_id": session_id})
        self.assertEqual(read_reply["session_id"], 0)


class ProxyMastermindMultipleSessionGameSequenceTestCase(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}
        Session._session_id = count(1)

    def test_multiple_games_updates_where_one_wins(self):
        game_one = MastermindGame()
        game_two = MastermindGame()
        proxy_one = MastermindGameProxy(game_instance=game_one)
        proxy_two = MastermindGameProxy(game_instance=game_two)

        session_id = proxy_one.create_game({"game_id": MASTERMIND_ID})["session_id"]
        self.session_manager.active_sessions[session_id].sequence = [1, 2, 3, 4]

        update_reply_one = proxy_one.update_game({"session_id": session_id, "guess": (1, 2, 3, 4)})
        update_reply_two = proxy_two.update_game({"session_id": session_id, "guess": (1, 2, 3, 4)})

        self.assertFalse(update_reply_one["session_id"] == 0)
        self.assertEqual(update_reply_two["session_id"], 0)

    def test_multiple_games_both_delete_same_session(self):
        game_one = MastermindGame()
        game_two = MastermindGame()
        proxy_one = MastermindGameProxy(game_instance=game_one)
        proxy_two = MastermindGameProxy(game_instance=game_two)

        session_id = proxy_one.create_game({"game_id": MASTERMIND_ID})["session_id"]

        update_reply_one = proxy_one.delete_game({"session_id": session_id})
        update_reply_two = proxy_two.delete_game({"session_id": session_id})

        self.assertFalse(update_reply_one["session_id"] == 0)
        self.assertEqual(update_reply_two["session_id"], 0)


class MinesweeperGameProxyCreateGame(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}
        Session._session_id = count(1)

    def test_create_game_fails(self):
        game = MinesweeperGame()
        proxy = MinesweeperProxy(game)
        result = proxy.create_game({"game_id": MASTERMIND_ID})
        self.assertEqual({"session_id": 0}, result)

    def test_create_game_works(self):
        game = MinesweeperGame()
        proxy = MinesweeperProxy(game)
        result = proxy.create_game({"game_id": MINESWEEPER_ID})
        self.assertEqual({"session_id": 1}, result)


class MinesweeperGameProxyReadGame(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}
        Session._session_id = count(1)

    def test_read_game_works(self):
        game = MinesweeperGame()
        proxy = MinesweeperProxy(game)
        proxy.create_game({"game_id": MINESWEEPER_ID})
        result = proxy.read_game({"session_id": 1})
        self.assertEqual(len(result.keys()), 5)

    def test_read_game_fails(self):
        game = MinesweeperGame()
        proxy = MinesweeperProxy(game)
        result = proxy.read_game({"session_id": 10})
        self.assertEqual({"session_id": 0}, result)


class MinesweeperGameProxyUpdateGame(unittest.TestCase):
    FOUR_CORNERS_BOARD_SOLN = {0: ['mine'] + [1] + [0] * 5 + [1] + ['mine'], 1: [1, 1] + [0] * 5 + [1, 1], 2: [0] * 9,
                               3: [0] * 9, 4: [0] * 9, 5: [0] * 9, 6: [0] * 9, 7: [1, 1] + [0] * 5 + [1, 1],
                               8: ['mine'] + [1] + [0] * 5 + [1] + ['mine']}

    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}
        Session._session_id = count(1)

    def test_update_game_flag_fails(self):
        game = MinesweeperGame()
        proxy = MinesweeperProxy(game)
        proxy.create_game({"game_id": MINESWEEPER_ID})
        result = proxy.update_game({"session_id": 1, "flag_cell": (-1, 1)})
        self.assertEqual({"session_id": 0}, result)

    def test_update_game_flag_fails(self):
        game = MinesweeperGame()
        proxy = MinesweeperProxy(game)
        proxy.create_game({"game_id": MINESWEEPER_ID})
        result = proxy.update_game({"session_id": 1, "flag_cell": (10, 1)})
        self.assertEqual({"session_id": 0}, result)

    def test_update_unhide_cell_fails(self):
        game = MinesweeperGame()
        proxy = MinesweeperProxy(game)
        proxy.create_game({"game_id": MINESWEEPER_ID})
        proxy.update_game({"session_id": 1, "flag_cell": (1, 1)})
        result = proxy.update_game({"session_id": 1, "unhide_cell": (1, 1)})
        self.assertEqual({"session_id": 0}, result)

    def test_update_flag_cell_fails(self):
        game = MinesweeperGame()
        proxy = MinesweeperProxy(game)
        proxy.create_game({"game_id": MINESWEEPER_ID})
        proxy.create_game({"game_id": MINESWEEPER_ID})
        session = self.session_manager.active_sessions[2].get_data()
        session["board"] = self.FOUR_CORNERS_BOARD_SOLN
        proxy.update_game({"session_id": 2, "unhide_cell": (1, 1)})
        result = proxy.update_game({"session_id": 2, "flag_cell": (1, 1)})
        self.assertEqual({"session_id": 0}, result)

    def test_update_done_game_fails(self):
        game = MinesweeperGame()
        proxy = MinesweeperProxy(game)
        proxy.create_game({"game_id": MINESWEEPER_ID})
        proxy.create_game({"game_id": MINESWEEPER_ID})
        session = self.session_manager.active_sessions[2].get_data()
        session["board"] = self.FOUR_CORNERS_BOARD_SOLN
        proxy.update_game({"session_id": 2, "unhide_cell": (0, 0)})
        result = proxy.update_game({"session_id": 2, "flag_cell": (1, 1)})
        self.assertEqual({"session_id": 0}, result)


class MinesweeperGameProxyBadInput(unittest.TestCase):
    def setUp(self):
        self.session_manager = SessionManager()
        SessionManager.active_sessions = {}

    def test_bad_input_one_fails(self):
        game = MinesweeperGame()
        proxy = MinesweeperProxy(game)
        result = proxy.create_game({"game_id": 'a'})
        self.assertEqual({"session_id": 0}, result)

    def test_bad_input_two_fails(self):
        game = MinesweeperGame()
        proxy = MinesweeperProxy(game)
        result = proxy.update_game({"session_id": 10, "guess": (1, -2, 3, 4)})
        self.assertEqual({"session_id": 0}, result)

    def test_bad_input_three_fails(self):
        game = MinesweeperGame()
        proxy = MinesweeperProxy(game)
        proxy.create_game({"game_id": '1'})
        result = proxy.update_game({"session_id": 1})
        self.assertEqual({"session_id": 0}, result)
