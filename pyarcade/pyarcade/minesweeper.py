from pyarcade.game_interface import GameInterface
from pyarcade.minesweeper_builder import MinesweeperBoardBuilder
from pyarcade.session_manager import SessionManager, MinesweeperSession
from copy import deepcopy


class MinesweeperGame(GameInterface):
    """ A class representing MinesweeperGame game sessions. For now each instance of MinesweeperGame
    game will hold multiple sessions where there is only one player against the computer. Any instance has access to
    these sessions.

    Note:
        For now, MinesweeperGame will have a 9x9 board with only 10 mines.
    """

    def __init__(self):
        self.session_manager = SessionManager.singleton()

    @staticmethod
    def print_board(board: dict) -> str:
        """
        Note: This function is useful for debugging

        Args:
            board: The game board

        Returns: The game board with all cells revealed.
        """
        reply = ""
        for key in board.keys():
            line = ""
            for cell in board[key]:
                if cell == 'mine':
                    line += 'x '
                else:
                    line += str(cell) + ' '
            line += '\n'
            reply += line
        return reply

    @staticmethod
    def print_player_board(player_board: dict, board: dict) -> str:
        reply = ""
        for key in board.keys():
            line = ""
            for cell in range(len(board[key])):
                if isinstance(player_board[key][cell], str):
                    line += 'F '
                elif player_board[key][cell]:
                    line += '🬅 '
                else:
                    line += str(board[key][cell]) + ' '
            line += '\n'
            reply += line
        return reply

    @staticmethod
    def print_board_done(player_board: dict, board: dict) -> str:
        reply = ""
        for key in board.keys():
            line = ""
            for cell in range(len(board[key])):
                if isinstance(player_board[key][cell], str):
                    line += 'F '
                elif isinstance(board[key][cell], str):
                    line += 'x '
                elif player_board[key][cell]:
                    line += '🬅 '
                else:
                    line += str(board[key][cell]) + ' '
            line += '\n'
            reply += line
        return reply

    @staticmethod
    def end_game(session: MinesweeperSession):
        """
        Args:
            session: The session to be modified

        Returns: Nothing. Updates game state in place.
        Note: This contains some dead code from testing.
        """
        session.set_to_done()
        print("You lose\n")
        MinesweeperGame.print_board(session.data["board"])

    @staticmethod
    def unhide_cell(location: tuple, session: MinesweeperSession):
        """
        Args:
            location: Location on the board of where to flag
            session: The session that is being modified

        Returns: Nothing. It modifies in place. If player unhides a mine then update game state to done.
        """
        # Location stores in (row,column)
        if session.data["board"][location[0]][location[1]] == 'mine':
            MinesweeperGame.end_game(session)
        else:
            session.data["player_board"][location[0]][location[1]] = False
            session.data["cells_hidden"] += -1

    @staticmethod
    def flag_cell(location: tuple, session: MinesweeperSession):
        """
        Args:
            location: Location on the board of where to flag
            session: The session that is being modified

        Returns: Nothing. It modifies inplace.
        """
        # Will not get bad input, so only cells that are hidden can be flagged
        if session.data["player_board"][location[0]][location[1]] == 'flag':
            session.data["player_board"][location[0]][location[1]] = True
            print(session.data["flags"])
            session.data["flags"] += 1
            print(session.data["flags"])
        else:
            session.data["player_board"][location[0]][location[1]] = 'flag'
            session.data["flags"] += (-1)

    def create_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary containing single key-value pair. The key is "game_id". The value
            is an integer denoting which game should be created

        Returns:
            reply: dictionary containing a single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing game sessions.
        """

        board, mines = MinesweeperBoardBuilder.initialize_board()
        # Player board stores the state of whether or not cells are hidden or flagged.
        player_board = {}
        for length in range(MinesweeperBoardBuilder.EASY_SIZE):
            player_board[length] = [True] * MinesweeperBoardBuilder.EASY_SIZE
        new_game_session = {"player_board": player_board, "board": board,
                            "mines": mines, "cells_hidden": MinesweeperBoardBuilder.EASY_SIZE ** 2,
                            "flags": MinesweeperBoardBuilder.EASY_MINES}

        return self.session_manager.init_minesweeper_session(new_game_session)

    def read_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary containing single key-value pair. The key is "session_id". The value is a
            integer unique to all ongoing game sessions.

        Returns:
            reply: dictionary containing a several key-value pairs that fully describe the game's state. They will be
            board which contains a string of the board, number of mines in this mode and the number flags the player has
            left to place as well as if the game is done or not. If the game was a loss, board contains x where the
            bombs were and correct flags. If it was a win, then board string is board with flags where the mines were.
        """
        session = self.session_manager.get_session_by_id(request["session_id"])
        data = session.data
        reply = deepcopy(data)
        reply.pop("cells_hidden")
        if session.is_done():
            reply["board"] = MinesweeperGame.print_board_done(reply["player_board"], reply["board"])
        else:
            reply["board"] = MinesweeperGame.print_player_board(reply["player_board"], reply["board"])
        reply.pop("player_board")
        reply["mines"] = MinesweeperBoardBuilder.EASY_MINES
        reply["session_id"] = request["session_id"]
        reply["done"] = session.is_done()

        return reply

    def update_game(self, request: dict) -> dict:
        """
        Args:
            request: dictionary describing the "move" to be made in the game

        Returns:
            reply: dictionary describing the game's new state.
        """
        session = self.session_manager.get_session_by_id(request["session_id"])
        if "unhide_cell" in request:
            location = request["unhide_cell"]
            MinesweeperGame.unhide_cell(location, session)
            request.pop("unhide_cell")
        if "flag_cell" in request:
            location = request["flag_cell"]
            MinesweeperGame.flag_cell(location, session)
            request.pop("flag_cell")

        return self.read_game(request)

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
