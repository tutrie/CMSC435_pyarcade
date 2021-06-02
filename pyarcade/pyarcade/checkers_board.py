from pyarcade.checker_pieces import RedPiece, BlackPiece, OpenPiece, EmptyPiece, GamePiece


def is_open_piece(piece: EmptyPiece) -> bool:
    return type(piece) == OpenPiece


def is_empty_piece(piece: EmptyPiece) -> bool:
    return type(piece) == EmptyPiece


def is_red_piece(piece: EmptyPiece) -> bool:
    return type(piece) == RedPiece


def is_black_piece(piece: EmptyPiece) -> bool:
    return type(piece) == BlackPiece


def is_king_piece(piece: GamePiece) -> bool:
    return piece.is_king


def is_red_side_of_board(row: int) -> bool:
    return row < 4


def is_black_side_of_board(row: int) -> bool:
    return row > 5


class CheckerBoard:
    def __init__(self):
        self.board = []
        self.red_left = self.black_left = 12
        self.red_kings = self.black_kings = 0
        self.setup_board()
        self._cache_valid_moves = {}
        self.turn = "RED"

    def setup_board(self):
        self.board = [[EmptyPiece(row, col) for col in range(10)] for row in range(10)]
        self.place_game_pieces()

    def to_json(self):
        return {
            "turn": self.turn,
            "red_left": self.red_left,
            "black_left": self.black_left,
            "board": self.get_board_for_ui()
        }

    def get_board_for_ui(self) -> list:
        ui_board = []

        for row in range(0, 10):
            ui_board.append([])
            for col in range(0, 10):
                ui_board[row].append(self.get_piece_at(row, col).to_json())

        return ui_board

    def place_game_pieces(self):
        for row in range(1, 9):
            for col in range(1, 9):
                if col % 2 == ((row + 1) % 2):
                    if is_red_side_of_board(row):
                        self.board[row][col] = RedPiece(row, col)
                    elif is_black_side_of_board(row):
                        self.board[row][col] = BlackPiece(row, col)
                    else:
                        self.board[row][col] = OpenPiece(row, col)

    def get_board(self) -> list:
        return self.board

    def is_red_turn(self) -> bool:
        return self.turn == "RED"

    def is_black_turn(self) -> bool:
        return self.turn == "BLACK"

    def swap_turn(self):
        self.turn = "BLACK" if self.is_red_turn() else "RED"

    def remove_pieces(self, pieces: list):
        for piece in pieces:
            if is_red_piece(piece):
                self.red_left -= 1
            elif is_black_piece(piece):
                self.black_left -= 1

            if is_king_piece(piece):
                self.decrease_king_count(piece)

            self.set_to_open_piece(piece)

    def set_to_open_piece(self, piece: GamePiece):
        self.board[piece.row][piece.col] = OpenPiece(piece.row, piece.col)

    def get_jumped_pieces(self, origin: tuple, dest: tuple) -> list:
        return self._cache_valid_moves[origin][dest]

    def is_a_winner(self):
        return self.black_left <= 0 or self.red_left <= 0

    def get_winner(self) -> str:
        if self.black_left <= 0:
            return "RED"
        elif self.red_left <= 0:
            return "BLACK"

        return "No Winner"

    def get_piece_at(self, row: int, col: int) -> GamePiece:
        return self.board[row][col]

    def move_piece_to(self, source_loc: tuple, dest_loc: tuple):
        source_row, source_col = source_loc[0], source_loc[1]
        dest_row, dest_col = dest_loc[0], dest_loc[1]

        dest = self.get_piece_at(dest_row, dest_col)
        source = self.get_piece_at(source_row, source_col)

        self.swap_pieces(source, dest)

        dest.move_to(source_row, source_col)
        source.move_to(dest_row, dest_col)

        self.reset_valid_moves_cache(source_loc)
        self.reset_valid_moves_cache(dest_loc)

        if source.can_be_a_king():
            source.set_king()
            self.increase_king_count(source)

    def swap_pieces(self, source: GamePiece, dest: GamePiece):
        self.board[source.row][source.col], self.board[dest.row][dest.col] = \
            self.board[dest.row][dest.col], self.board[source.row][source.col]

    def reset_valid_moves_cache(self, piece: tuple):
        if self.is_cache_set_for_piece(piece):
            del self._cache_valid_moves[piece]

    def is_cache_set_for_piece(self, piece: tuple) -> bool:
        return piece in self._cache_valid_moves

    def increase_king_count(self, piece: GamePiece):
        if is_red_piece(piece):
            self.red_kings += 1
        else:
            self.black_kings += 1

    def decrease_king_count(self, piece: GamePiece):
        if is_red_piece(piece):
            self.red_kings -= 1
        else:
            self.black_kings -= 1

    def is_movable_piece(self, row: int, col: int) -> bool:
        piece = self.get_piece_at(row, col)
        return is_red_piece(piece) or is_black_piece(piece)

    def is_valid_move_for_piece(self, origin_loc: tuple, dest_loc: tuple) -> bool:
        origin = self.get_piece_at(origin_loc[0], origin_loc[1])
        dest = self.get_piece_at(dest_loc[0], dest_loc[1])

        if not self.is_cache_set_for_piece(origin_loc):
            self.get_valid_moves(origin)

        return (dest.row, dest.col) in self._cache_valid_moves[(origin.row, origin.col)]

    def get_valid_moves(self, origin: GamePiece) -> dict:
        moves = self.traverse_board(origin)
        self.set_moves_cache((origin.row, origin.col), moves)
        return moves

    def set_moves_cache(self, piece: tuple, moves: dict):
        self._cache_valid_moves[piece] = moves

    def traverse_board(self, origin: GamePiece) -> dict:
        visited = set()
        jumped = []
        moves = {}

        self.traverse_forward(moves, origin, origin, jumped, visited)

        if origin.is_king:
            self.traverse_backward(moves, origin, origin, jumped, visited)

        return moves

    def traverse_forward(self, moves: dict, piece: GamePiece, origin: GamePiece, jumped: list, visited: set):
        self.traverse_right(moves, piece, origin, jumped, visited)
        self.traverse_left(moves, piece, origin, jumped, visited)

    def traverse_backward(self, moves: dict, piece: GamePiece, origin: GamePiece, jumped: list, visited: set):
        self.traverse_back_left(moves, piece, origin, jumped, visited)
        self.traverse_back_right(moves, piece, origin, jumped, visited)

    def traverse_right(self, moves: dict, piece: GamePiece, origin: GamePiece, jumped: list, visited: set):
        next_piece = self.get_right_piece(piece, origin)
        moves.update(self.process_right(next_piece, piece, origin, jumped, visited))

    def traverse_left(self, moves: dict, piece: GamePiece, origin: GamePiece, jumped: list, visited: set):
        next_piece = self.get_left_piece(piece, origin)
        moves.update(self.process_left(next_piece, piece, origin, jumped, visited))

    def traverse_back_left(self, moves: dict, piece: GamePiece, origin: GamePiece, jumped: list, visited: set):
        next_piece = self.get_back_left_piece(piece, origin)
        moves.update(self.process_back_left(next_piece, piece, origin, jumped, visited))

    def traverse_back_right(self, moves: dict, piece: GamePiece, origin: GamePiece, jumped: list, visited: set):
        next_piece = self.get_back_right_piece(piece, origin)
        moves.update(self.process_back_right(next_piece, piece, origin, jumped, visited))

    def get_right_piece(self, piece: GamePiece, origin: GamePiece) -> GamePiece:
        row, col = piece.get_right_piece(row_step=origin.row_step, col_step=origin.col_step)
        return self.get_piece_at(row, col)

    def get_left_piece(self, piece: GamePiece, origin: GamePiece) -> GamePiece:
        row, col = piece.get_left_piece(row_step=origin.row_step, col_step=origin.col_step)
        return self.get_piece_at(row, col)

    def get_back_left_piece(self, piece: GamePiece, origin: GamePiece) -> GamePiece:
        row, col = piece.get_back_left_piece(row_step=origin.row_step, col_step=origin.col_step)
        return self.get_piece_at(row, col)

    def get_back_right_piece(self, piece: GamePiece, origin: GamePiece) -> GamePiece:
        row, col = piece.get_back_right_piece(row_step=origin.row_step, col_step=origin.col_step)
        return self.get_piece_at(row, col)

    def process_right(self, current: GamePiece, prev: GamePiece, origin: GamePiece, jumped: list, visited: set) \
            -> dict:
        if is_empty_piece(current) or current in visited or current.is_same_type(prev):
            return {}

        visited.add(current)
        moves = {}

        if is_open_piece(current):
            last = []
            if type(prev) != type(origin):
                last = [prev]

            last.extend(jumped)
            moves[(current.row, current.col)] = last

            self.traverse_forward(moves, current, origin, last, visited)

            if origin.is_king:
                self.traverse_back_left(moves, current, origin, last, visited)
        else:
            # we need to keep going right
            self.traverse_right(moves, current, origin, jumped, visited)

        return moves

    def process_left(self, current: GamePiece, prev: GamePiece, origin: GamePiece, jumped: list, visited: set) \
            -> dict:
        if is_empty_piece(current) or current in visited or current.is_same_type(prev):
            return {}

        visited.add(current)
        moves = {}

        if is_open_piece(current):
            last = []
            if type(prev) != type(origin):
                last = [prev]

            last.extend(jumped)
            moves[(current.row, current.col)] = last

            self.traverse_forward(moves, current, origin, last, visited)

            if origin.is_king:
                self.traverse_back_right(moves, current, origin, last, visited)
        else:
            # we need to keep going left
            self.traverse_left(moves, current, origin, jumped, visited)

        return moves

    def process_back_left(self, current: GamePiece, prev: GamePiece, origin: GamePiece, jumped: list, visited: set) \
            -> dict:
        if is_empty_piece(current) or current in visited or current.is_same_type(prev):
            return {}

        visited.add(current)
        moves = {}

        if is_open_piece(current):
            last = []
            if type(prev) != type(origin):
                last = [prev]

            last.extend(jumped)
            moves[(current.row, current.col)] = last

            self.traverse_left(moves, current, origin, last, visited)
            self.traverse_backward(moves, current, origin, last, visited)

        else:
            # we need to keep going left
            self.traverse_back_left(moves, current, origin, jumped, visited)

        return moves

    def process_back_right(self, current: GamePiece, prev: GamePiece, origin: GamePiece, jumped: list, visited: set) \
            -> dict:
        if is_empty_piece(current) or current in visited or current.is_same_type(prev):
            return {}

        visited.add(current)
        moves = {}

        if is_open_piece(current):
            last = []
            if type(prev) != type(origin):
                last = [prev]

            last.extend(jumped)
            moves[(current.row, current.col)] = last

            self.traverse_right(moves, current, origin, last, visited)
            self.traverse_backward(moves, current, origin, last, visited)

        else:
            # we need to keep going back right
            self.traverse_back_right(moves, current, origin, jumped, visited)

        return moves
