from pyarcade.game_interface import GameInterface
from pyarcade.session_manager import SessionManager
from pyarcade.checkers_board import CheckerBoard


class Checkers(GameInterface):

    def __init__(self):
        self.session_manager = SessionManager.singleton()

    def create_game(self, request: dict) -> dict:
        """
            Args:
                request: dictionary containing single key-value pair. The key is "game_id". The value
                is an integer denoting which game should be created

            Returns:
                reply: dictionary containing a single key-value pair. The key is "session_id". The value is a
                integer unique to all ongoing game sessions.

            """
        return self.session_manager.init_checkers_session(CheckerBoard())

    def read_game(self, request: dict) -> dict:
        """
            Args:
                request: dictionary containing single key-value pair. The key is "session_id". The value is a
                integer unique to all ongoing game sessions.

            Returns:
                reply: dictionary containing a several key-value pairs that fully describe the game's state.
            """
        session = self.session_manager.get_session_by_id(request["session_id"])
        return session.to_json()

    def update_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary containing two key-value pairs. One key is "session_id". The value is a
            integer unique to all ongoing game sessions. The second key is "move" The value should be a tuple
            of tuples where the first item is the location of the peice to move and the second the location
            to move that piece to.

        Returns:
            reply: dictionary containing three keys.
                "board": The updated board after the pieces have been moved.
                "session_id": session_id provided with the original request.
                "done": True or False depending on whether the game is over.
        """

        session = self.session_manager.get_session_by_id(request["session_id"])
        game = session.get_game()

        origin, dest = request["move"]

        jumped_pieces = game.get_jumped_pieces(origin, dest)
        game.remove_pieces(jumped_pieces)
        game.move_piece_to(origin, dest)

        if game.is_a_winner():
            session.set_to_done()
        else:
            game.swap_turn()

        return session.to_json()

    def delete_game(self, request: dict) -> dict:
        """
            Args:
                request: dictionary containing a single key-value pair. The key is "session_id". The value is a
                integer unique to all ongoing game sessions.

            Returns:
                reply: dictionary containing a single key-value pair. The key is "session_id". The value is a
                integer unique to all ongoing game sessions.
            """
        return self.session_manager.delete_session(request["session_id"])
