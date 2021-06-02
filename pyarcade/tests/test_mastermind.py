from pyarcade.mastermind import MastermindGame
import unittest
from pyarcade.session_manager import SessionManager


class MastermindTestCase(unittest.TestCase):
    def setUp(self):
        """Make all instances of MastermindGame independent"""
        SessionManager.active_sessions = {}

    """CREATE GAME"""

    def test_create_game_gives_unique_session_id(self):
        session_ids = []
        game = MastermindGame()
        for idx in range(100):
            session_ids.append(game.create_game({"game_id": 0})["session_id"])

        self.assertEqual(len(set(session_ids)), 100)

    def test_create_game_stores_session_ids(self):
        sessions_created = []
        game = MastermindGame()
        for idx in range(100):
            sessions_created.append(game.create_game({"game_id": 0})["session_id"])

        session_ids = list(SessionManager.active_sessions.keys())
        self.assertEqual(session_ids, sessions_created)

    """READ GAME"""

    def test_read_game_no_guesses(self):
        game = MastermindGame()
        session = game.create_game(({"game_id": 0}))["session_id"]
        correct_response = {"guesses": [], "session_id": session, "done": False}
        self.assertEqual(correct_response, game.read_game({"session_id": session}))

    def test_read_game_session_has_guesses(self):
        game = MastermindGame()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        SessionManager.active_sessions[session_id].guesses = [(1, 2, 3, 4), (1, 2)]
        correct_response = {"guesses": [(1, 2, 3, 4), (1, 2)], "session_id": session_id, "done": False}
        self.assertEqual(correct_response, game.read_game({"session_id": session_id}))

    def test_read_game_session_is_done(self):
        game = MastermindGame()
        session_id = game.create_game(({"game_id": 0}))["session_id"]

        SessionManager.active_sessions[session_id].guesses = [(1, 2, 3, 4), (1, 2)]
        SessionManager.active_sessions[session_id].done = True

        correct_response = {"guesses": [(1, 2, 3, 4), (1, 2)], "session_id": session_id, "done": True}
        self.assertEqual(correct_response, game.read_game({"session_id": session_id}))

    """UPDATE GAME"""

    def test_update_game_incorrect_guess(self):
        game = MastermindGame()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        SessionManager.active_sessions[session_id].sequence = [1, 2, 3, 5]
        guess = (7, 6, 8, 9)

        correct_response = {"guesses": [((7, 6, 8, 9), (0, 0))], "session_id": session_id, "done": False}
        self.assertEqual(correct_response, game.update_game({"session_id": session_id, "guess": guess}))

    def test_update_game_no_prev_guesses(self):
        game = MastermindGame()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        SessionManager.active_sessions[session_id].sequence = [1, 2, 3, 5]
        guess = (1, 3, 4, 5)

        correct_response = {"guesses": [((1, 3, 4, 5), (1, 2))], "session_id": session_id, "done": False}
        self.assertEqual(correct_response, game.update_game({"session_id": session_id, "guess": guess}))

    def test_update_game_has_prev_guesses(self):
        game = MastermindGame()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        SessionManager.active_sessions[session_id].sequence = [1, 2, 3, 5]
        SessionManager.active_sessions[session_id].guesses = [((2, 3, 6, 1), (3, 0))]
        guess = (1, 3, 4, 5)

        correct_response = {
            "guesses": [((2, 3, 6, 1), (3, 0)), ((1, 3, 4, 5), (1, 2))],
            "session_id": session_id,
            "done": False
        }

        self.assertEqual(correct_response, game.update_game({"session_id": session_id, "guess": guess}))

    def test_update_game_consecutive_guesses(self):
        game = MastermindGame()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        SessionManager.active_sessions[session_id].sequence = [1, 2, 3, 5]

        first_guess = (2, 3, 6, 1)
        second_guess = (1, 3, 4, 5)

        correct_first_response = {
            "guesses": [((2, 3, 6, 1), (3, 0))],
            "session_id": session_id,
            "done": False
        }

        correct_second_response = {
            "guesses": [((2, 3, 6, 1), (3, 0)), ((1, 3, 4, 5), (1, 2))],
            "session_id": session_id,
            "done": False
        }

        self.assertEqual(correct_first_response, game.update_game({"session_id": session_id, "guess": first_guess}))
        self.assertEqual(correct_second_response, game.update_game({"session_id": session_id, "guess": second_guess}))

    def test_update_game_correct_inputs_consecutive_guesses(self):
        game = MastermindGame()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        SessionManager.active_sessions[session_id].sequence = [1, 2, 3, 5]

        first_guess = (2, 3, 6, 1)
        second_guess = (1, 3, 4, 5)

        correct_first_response = {
            "guesses": [((2, 3, 6, 1), (3, 0))],
            "session_id": session_id,
            "done": False
        }

        correct_second_response = {
            "guesses": [((2, 3, 6, 1), (3, 0)), ((1, 3, 4, 5), (1, 2))],
            "session_id": session_id,
            "done": False
        }

        self.assertEqual(correct_first_response, game.update_game({"session_id": session_id, "guess": first_guess}))
        self.assertEqual(correct_second_response, game.update_game({"session_id": session_id, "guess": second_guess}))

    def test_update_game_correct_guess_sets_session_to_done(self):
        game = MastermindGame()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        SessionManager.active_sessions[session_id].sequence = [1, 2, 3, 5]
        guess = (1, 2, 3, 5)

        correct_response = {"guesses": [(guess, (0, 4))], "session_id": session_id, "done": True}
        self.assertEqual(correct_response, game.update_game({"session_id": session_id, "guess": guess}))

    """DELETE GAME"""

    def test_delete_game_returns_correct_id(self):
        game = MastermindGame()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        self.assertEqual(session_id, game.delete_game({"session_id": session_id})["session_id"])

    def test_delete_game_returns_correct_id_every_time(self):
        game = MastermindGame()
        session_id_list = [game.create_game(({"game_id": 0}))["session_id"] for idx in range(0, 100)]

        for session_id in session_id_list:
            self.assertEqual(session_id, game.delete_game({"session_id": session_id})["session_id"])

    def test_delete_game_removes_session_from_list(self):
        game = MastermindGame()
        session_id = game.create_game(({"game_id": 0}))["session_id"]
        game.delete_game({"session_id": session_id})
        self.assertFalse(session_id in SessionManager.active_sessions)

    def test_delete_game_removes_multiple_sessions_from_list(self):
        game = MastermindGame()
        session_id_list = [game.create_game(({"game_id": 0}))["session_id"] for idx in range(0, 100)]

        for session_id in session_id_list:
            game.delete_game({"session_id": session_id})["session_id"]
            self.assertFalse(session_id in SessionManager.active_sessions)

    """SEQUENCES"""

    def test_read_game_returns_updated_values_after_update_game(self):
        game = MastermindGame()
        session_id = game.create_game({"game_id": 0})["session_id"]
        update_reply = game.update_game({"session_id": session_id, "guess": (1, 2, 3, 4)})
        read_reply = game.read_game({"session_id": session_id})

        self.assertEqual(update_reply, read_reply)

    def test_read_game_returns_updated_values_after_game_done(self):
        game = MastermindGame()
        session_id = game.create_game({"game_id": 0})["session_id"]
        SessionManager.active_sessions[session_id].sequence = [1, 2, 3, 4]

        update_reply = game.update_game({"session_id": session_id, "guess": (1, 2, 3, 4)})
        read_reply = game.read_game({"session_id": session_id})

        self.assertEqual(update_reply, read_reply)

    def test_read_create_read_update_win_read_delete_correct_input(self):
        game = MastermindGame()

        session_id = game.create_game({"game_id": 0})["session_id"]
        SessionManager.active_sessions[session_id].sequence = [1, 2, 3, 4]

        read_reply = game.read_game({"session_id": session_id})
        self.assertEqual({"guesses": [], "session_id": session_id, "done": False}, read_reply)

        update_request = {"session_id": session_id, "guess": (1, 2, 3, 4)}
        update_reply = game.update_game(update_request)
        self.assertEqual({"guesses": [((1, 2, 3, 4), (0, 4))], "session_id": session_id, "done": True}, update_reply)

        read_reply = game.read_game({"session_id": session_id})
        self.assertEqual({"guesses": [((1, 2, 3, 4), (0, 4))], "session_id": session_id, "done": True}, read_reply)

        delete_reply = game.delete_game({"session_id": session_id})
        self.assertEqual(delete_reply, {"session_id": session_id})

        self.assertEqual(0, len(SessionManager.active_sessions))

    def test_read_create_read_update_no_win_read_delete_correct_input(self):
        game = MastermindGame()

        session_id = game.create_game({"game_id": 0})["session_id"]
        SessionManager.active_sessions[session_id].sequence = [1, 2, 3, 4]

        read_reply = game.read_game({"session_id": session_id})
        self.assertEqual({"guesses": [], "session_id": session_id, "done": False}, read_reply)

        update_request = {"session_id": session_id, "guess": (1, 2, 3, 5)}
        update_reply = game.update_game(update_request)
        self.assertEqual({"guesses": [((1, 2, 3, 5), (0, 3))], "session_id": session_id, "done": False}, update_reply)

        read_reply = game.read_game({"session_id": session_id})
        self.assertEqual({"guesses": [((1, 2, 3, 5), (0, 3))], "session_id": session_id, "done": False}, read_reply)

        delete_reply = game.delete_game({"session_id": session_id})
        self.assertEqual(delete_reply, {"session_id": session_id})

        self.assertEqual(0, len(SessionManager.active_sessions))

    """MULTIPLE GAME INSTANCES"""

    def test_multiple_games_see_created_session(self):
        game_one = MastermindGame()

        session_id = game_one.create_game({"game_id": 0})["session_id"]
        self.assertTrue(session_id in SessionManager.active_sessions)
        self.assertTrue(session_id in SessionManager.active_sessions)

    def test_multiple_games_read_same_date_for_session(self):
        game_one = MastermindGame()
        game_two = MastermindGame()

        session_id = game_one.create_game({"game_id": 0})["session_id"]
        game_two.update_game({"session_id": session_id, "guess": (1, 2, 3, 4)})
        read_one_reply = game_one.read_game({"session_id": session_id})
        read_two_reply = game_two.read_game({"session_id": session_id})

        self.assertEqual(read_one_reply, read_two_reply)

    def test_multiple_games_can_see_session_update(self):
        game_one = MastermindGame()
        game_two = MastermindGame()

        session_id = game_one.create_game({"game_id": 0})["session_id"]
        game_two.update_game({"session_id": session_id, "guess": (1, 2, 3, 4)})

        read_one_reply = game_one.read_game({"session_id": session_id})
        read_two_reply = game_two.read_game({"session_id": session_id})

        self.assertEqual(read_one_reply, read_two_reply)

    def test_multiple_games_can_see_session_deletes(self):
        game_one = MastermindGame()

        session_id = game_one.create_game({"game_id": 0})["session_id"]

        game_one.delete_game({"session_id": session_id})

        self.assertFalse(session_id in SessionManager.active_sessions)

    def test_multiple_games_read_update_delete_multiple_sessions(self):
        game_instance_one = MastermindGame()
        game_instance_two = MastermindGame()

        session_one = game_instance_one.create_game({"game_id": 0})["session_id"]
        session_two = game_instance_two.create_game({"game_id": 0})["session_id"]

        SessionManager.active_sessions[session_one].sequence = [4, 3, 2, 1]
        SessionManager.active_sessions[session_two].sequence = [1, 2, 3, 4]

        # read game session two from game one and vice versa
        game_one_read_session_two = game_instance_one.read_game({"session_id": session_two})
        game_two_read_session_one = game_instance_two.read_game({"session_id": session_one})

        # both are empty
        self.assertEqual({"guesses": [], "session_id": session_two, "done": False}, game_one_read_session_two)
        self.assertEqual({"guesses": [], "session_id": session_one, "done": False}, game_two_read_session_one)

        # game_instance_one updates session two and correctly guesses sequence
        game_one_update_two_request = {"session_id": session_two, "guess": (1, 2, 3, 4)}
        game_one_update_two_reply = game_instance_two.update_game(game_one_update_two_request)
        self.assertEqual({"guesses": [((1, 2, 3, 4), (0, 4))], "session_id": session_two, "done": True},
                         game_one_update_two_reply)

        # game_instance_two reads session two as done
        game_two_read_session_two = game_instance_two.read_game({"session_id": session_two})
        self.assertEqual({"guesses": [((1, 2, 3, 4), (0, 4))], "session_id": session_two, "done": True},
                         game_two_read_session_two)

        # game_instance_two deletes session two out of fury
        delete_reply = game_instance_two.delete_game({"session_id": session_two})
        self.assertEqual(delete_reply, {"session_id": session_two})

        # game_instance_two updates session one a guess that doesn't win
        game_two_update_one_request = {"session_id": session_one, "guess": (1, 2, 3, 4)}
        game_two_update_one_reply = game_instance_two.update_game(game_two_update_one_request)
        self.assertEqual({"guesses": [((1, 2, 3, 4), (4, 0))], "session_id": session_one, "done": False},
                         game_two_update_one_reply)

        # game_instance_one updates session one and guesses correctly again!
        game_one_update_one_request = {"session_id": session_one, "guess": (4, 3, 2, 1)}
        game_one_update_one_reply = game_instance_one.update_game(game_one_update_one_request)
        self.assertEqual({"guesses": [((1, 2, 3, 4), (4, 0)), ((4, 3, 2, 1), (0, 4))],
                          "session_id": session_one,
                          "done": True},
                         game_one_update_one_reply)

        # game_session_two deletes session one out of fury (somehow)
        delete_reply = game_instance_two.delete_game({"session_id": session_one})
        self.assertEqual(delete_reply, {"session_id": session_one})

        self.assertEqual(0, len(SessionManager.active_sessions))
