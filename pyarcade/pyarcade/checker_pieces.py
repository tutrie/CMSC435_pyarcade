"""GAME PIECES"""


class EmptyPiece:
    color = "GRAY"

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return "#"

    def to_json(self) -> dict:
        return {
            "row": self.row,
            "col": self.col,
            "piece": self.__repr__(),
            "color": self.color
        }


class GamePiece(EmptyPiece):
    def __init__(self, row: int, col: int, **kwargs):
        EmptyPiece.__init__(self, row, col)
        self.is_king = False
        if kwargs:
            self.row_step = kwargs["row_step"]
            self.col_step = kwargs["col_step"]
        else:
            self.row_step = 0
            self.col_step = 0

    def set_king(self):
        self.is_king = True
        self.color = "GOLD"

    def can_be_a_king(self):
        return False

    def is_king(self):
        return self.is_king

    def move_to(self, row: int, col: int):
        self.row = row
        self.col = col

    def is_same_type(self, other_piece):
        return type(self) == type(other_piece)

    def get_left_piece(self, **kwargs) -> tuple:
        if kwargs:
            return self.row + kwargs["row_step"], self.col + kwargs["col_step"]
        return self.row + self.row_step, self.col + self.col_step

    def get_right_piece(self, **kwargs) -> tuple:
        if kwargs:
            return self.row + kwargs["row_step"], self.col - kwargs["col_step"]
        return self.row + self.row_step, self.col - self.col_step

    def get_back_left_piece(self, **kwargs) -> tuple:
        if kwargs:
            return self.row - kwargs["row_step"], self.col - kwargs["col_step"]
        return self.row - self.row_step, self.col - self.col_step

    def get_back_right_piece(self, **kwargs) -> tuple:
        if kwargs:
            return self.row - kwargs["row_step"], self.col + kwargs["col_step"]
        return self.row - self.row_step, self.col + self.col_step


class RedPiece(GamePiece):
    row_step = 1
    col_step = 1
    color = "RED"

    def __init__(self, row, col):
        GamePiece.__init__(self, row, col, row_step=RedPiece.row_step, col_step=RedPiece.col_step)

    def can_be_a_king(self):
        return not self.is_king and self.row == 8

    def __repr__(self):
        return "R"


class BlackPiece(GamePiece):
    row_step = -1
    col_step = -1
    color = "BLACK"

    def __init__(self, row, col):
        GamePiece.__init__(self, row, col, row_step=BlackPiece.row_step, col_step=BlackPiece.col_step)

    def can_be_a_king(self):
        return not self.is_king and self.row == 1

    def __repr__(self):
        return "B"


class OpenPiece(GamePiece):
    def __init__(self, row, column):
        GamePiece.__init__(self, row, column)
        self.open = True

    def __repr__(self):
        return " "
