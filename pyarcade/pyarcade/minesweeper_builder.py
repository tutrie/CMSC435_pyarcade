from random import sample


class MinesweeperBoardBuilder:
    EASY_SIZE = 9
    EASY_MINES = 10

    def __init__(self):
        pass

    @staticmethod
    def on_board(row: int, column: int, board: dict) -> bool:
        """
        Args:
            board: The game board to check
            row: Location on board
            column: Location on board

        Returns: True or False if the location is on the board
        """
        try:
            access = board[row][column]
            if column < 0:
                return False
        except IndexError:
            return False
        except KeyError:
            return False
        return True

    @staticmethod
    def count_adjacent_mines(mines: list, board: dict) -> dict:
        """
        Args:
            mines: Locations of mines on the board
            board: Board with mines placed

        Returns: A game board with cells whose values reflect the number of bombs adjacent to them.
        """
        for row, column in mines:
            if MinesweeperBoardBuilder.on_board(row+1, column+1, board) and board[row+1][column+1] != 'mine':
                board[row+1][column+1] += 1
            if MinesweeperBoardBuilder.on_board(row+1, column, board) and board[row+1][column] != 'mine':
                board[row+1][column] += 1
            if MinesweeperBoardBuilder.on_board(row+1, column-1, board) and board[row+1][column-1] != 'mine':
                board[row+1][column-1] += 1
            if MinesweeperBoardBuilder.on_board(row, column-1, board) and board[row][column-1] != 'mine':
                board[row][column-1] += 1
            if MinesweeperBoardBuilder.on_board(row-1, column-1, board) and board[row-1][column-1] != 'mine':
                board[row-1][column-1] += 1
            if MinesweeperBoardBuilder.on_board(row-1, column, board) and board[row-1][column] != 'mine':
                board[row-1][column] += 1
            if MinesweeperBoardBuilder.on_board(row-1, column+1, board) and board[row-1][column+1] != 'mine':
                board[row-1][column+1] += 1
            if MinesweeperBoardBuilder.on_board(row, column+1, board) and board[row][column+1] != 'mine':
                board[row][column+1] += 1
        return board

    @staticmethod
    def initialize_board() -> tuple:
        """
        Returns: A dictionary representing a minesweeperGame board. The keys are rows and the values are lists that
        represent the columns. The column is a list of numbers indicating how many mines are adjacent to that location.
        """

        board = {0: [0]*9, 1: [0]*9, 2: [0]*9, 3: [0]*9, 4: [0]*9, 5: [0]*9, 6: [0]*9, 7: [0]*9, 8: [0]*9}
        mines = []
        for row_loc in range(9):
            for col_loc in range(9):
                # Creates a list of board locations
                mines.append((row_loc, col_loc))
        # Randomly picks locations to assign mines
        mines = sample(mines, MinesweeperBoardBuilder.EASY_MINES)
        for row, column in mines:
            board[row][column] = 'mine'
        board = MinesweeperBoardBuilder.count_adjacent_mines(mines, board)
        return board, mines
