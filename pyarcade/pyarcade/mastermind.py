from pyarcade.game_interface import GameInterface
from pyarcade.session_manager import SessionManager
from random import sample


class MastermindGame(GameInterface):
    """ A class representing a Mastermind game session.

    Note:
        For now, Mastermind must have a hidden sequence of length 4 in which all 4 integers may take on values
        between 0 and 9.
    """

    def __init__(self):
        self.session_manager = SessionManager.singleton()

    def create_game(self, request: dict) -> dict:
        """ Upon calling create_game, the Mastermind game should initialize its hidden sequence

         Args:
             request: dictionary containing single key-value pair. The key is "game_id".

         Returns:
            reply: dictionary containing the session_id in the request.
        """
        hidden_sequence = tuple(sample(range(10), 4))
        return self.session_manager.init_mastermind_session(hidden_sequence)

    def read_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary containing single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing game sessions.

        Returns:
            reply: dictionary containing three keys.
                "guesses": all previous guesses and their respective numbers of cows and bulls
                for this game_session. All guesses should be kept as a list of tuples under the key "guesses."
                A guess of (0, 1, 2, 3) that has one cow and two bulls should be APPENDED to the list as
                ((0, 1, 2, 3), (1, 2)).
                "session_id": session_id provided with the original request.
                "done": True or False depending on whether the game is over.

            So the overall reply could look like:
            {"guesses": [((0, 1, 2, 3), (1, 2), ((3, 2, 1, 0), (2, 1))], "session_id": 1, "done": False}
        """
        session = self.session_manager.get_session_by_id(request["session_id"])

        return {"guesses": session.get_guesses(), "session_id": session.get_id(), "done": session.is_done()}

    def update_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary containing two key-value pairs. One key is "session_id". The value is a
            integer unique to all ongoing game sessions. The second key is "guess." The value should be a tuple
            of four integers.

        Returns:
            reply: dictionary containing three keys.
                "guesses": all previous guesses and their respective numbers of cows and bulls
                for this game_session. All guesses should be kept as a list of tuples under the key "guesses."
                A guess of (0, 1, 2, 3) that has one cow and two bulls should be APPENDED to the list as
                ((0, 1, 2, 3), (1, 2)).
                "session_id": session_id provided with the original request.
                "done": True or False depending on whether the game is over.

            So the overall reply could look like:
            {"guesses": [((0, 1, 2, 3), (1, 2), ((3, 2, 1, 0), (2, 1))], "session_id": 1, "done": False}
        """
        game_session = self.session_manager.get_session_by_id(request["session_id"])
        sequence_to_guess = game_session.get_sequence()
        bulls = cows = 0

        for guess_idx, guess in enumerate(request["guess"]):
            if guess in sequence_to_guess:
                if sequence_to_guess[guess_idx] == guess:
                    bulls += 1
                else:
                    cows += 1

        game_session.insert_guess((request["guess"], (cows, bulls)))

        if bulls == 4:
            game_session.set_to_done()

        return {"guesses": game_session.get_guesses(),
                "session_id": game_session.get_id(),
                "done": game_session.is_done()}

    def delete_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary containing single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing game sessions.

        Returns:
            reply: dictionary containing the session_id in the request.
        """

        return self.session_manager.delete_session(request["session_id"])
