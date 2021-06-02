import unittest
from pyarcade.checkers_board import CheckerBoard
from pyarcade.checker_pieces import RedPiece, BlackPiece, OpenPiece, EmptyPiece


class CheckerBoardRemovePiecesTestCase(unittest.TestCase):

    def test_remove_pieces_sets_to_open_space(self):
        board = CheckerBoard()

        remove_me = [board.get_piece_at(3, 2), board.get_piece_at(3, 4), board.get_piece_at(6, 3)]
        board.remove_pieces(remove_me)

        self.assertTrue(type(board.get_piece_at(3, 2)) == OpenPiece)
        self.assertTrue(type(board.get_piece_at(3, 4)) == OpenPiece)
        self.assertTrue(type(board.get_piece_at(6, 3)) == OpenPiece)
        self.assertEqual(board.red_left, 10)
        self.assertEqual(board.black_left, 11)

    def test_remove_pieces_sets_decrease_count(self):
        board = CheckerBoard()

        remove_me = [board.get_piece_at(3, 2), board.get_piece_at(3, 4), board.get_piece_at(6, 3)]
        board.remove_pieces(remove_me)

        self.assertEqual(board.red_left, 10)
        self.assertEqual(board.black_left, 11)


class CheckerBoardSetupBoardTestCase(unittest.TestCase):

    def test_setup_board_puts_edge_pieces_on_the_top_row(self):
        checkers = CheckerBoard()
        row = 0
        for col in range(10):
            self.assertTrue(type(checkers.board[row][col]) == EmptyPiece)

    def test_setup_board_puts_edge_pieces_on_the_bottom_row(self):
        checkers = CheckerBoard()
        row = 9
        for col in range(10):
            self.assertTrue(type(checkers.board[row][col]) == EmptyPiece)

    def test_setup_board_puts_edge_pieces_on_the_left_column(self):
        checkers = CheckerBoard()
        col = 0
        for row in range(10):
            self.assertTrue(type(checkers.board[row][col]) == EmptyPiece)

    def test_setup_board_puts_edge_pieces_on_the_right_column(self):
        checkers = CheckerBoard()
        col = 9
        for row in range(10):
            self.assertTrue(type(checkers.board[row][col]) == EmptyPiece)

    def test_setup_board_puts_twelve_red_pieces(self):
        red_count = 0
        checkers = CheckerBoard()

        for row in range(1, 9):
            for col in range(1, 9):
                red_count += 1 if type(checkers.board[row][col]) == RedPiece else 0

        self.assertTrue(red_count == 12)

    def test_setup_board_puts_twelve_black_pieces(self):
        black_count = 0
        checkers = CheckerBoard()

        for row in range(1, 9):
            for col in range(1, 9):
                black_count += 1 if type(checkers.board[row][col]) == BlackPiece else 0

        self.assertTrue(black_count == 12)

    def test_setup_board_puts_red_on_every_other_space(self):
        checkers = CheckerBoard()

        # row 1
        row = 1
        for col in range(2, 9, 2):
            self.assertEqual(type(checkers.board[row][col]), RedPiece)

        # row 2
        row = 2
        for col in range(1, 9, 2):
            self.assertEqual(type(checkers.board[row][col]), RedPiece)

        # row 3
        row = 2
        for col in range(1, 9, 2):
            self.assertEqual(type(checkers.board[row][col]), RedPiece)

    def test_setup_board_puts_black_on_every_other_space(self):
        checkers = CheckerBoard()

        # row 1
        row = 6
        for col in range(1, 9, 2):
            self.assertEqual(type(checkers.board[row][col]), BlackPiece)

        # row 2
        row = 7
        for col in range(2, 9, 2):
            self.assertEqual(type(checkers.board[row][col]), BlackPiece)

        # row 3
        row = 8
        for col in range(1, 9, 2):
            self.assertEqual(type(checkers.board[row][col]), BlackPiece)


class CheckBoardSwapPieceTestCase(unittest.TestCase):
    def test_swap_updates_board(self):
        checkers = CheckerBoard()
        source = checkers.board[3][2]
        dest = checkers.board[6][3]

        checkers.swap_pieces(source, dest)

        self.assertEqual(checkers.board[3][2], dest)
        self.assertEqual(checkers.board[6][3], source)

    def test_swap_updates_board_everytime(self):
        checkers = CheckerBoard()

        for row in range(1, 9):
            for col in range(1, 9):
                source = checkers.board[row][col]
                dest = checkers.board[col][row]
                checkers.swap_pieces(source, dest)
                self.assertEqual(checkers.board[col][row], source)
                self.assertEqual(checkers.board[row][col], dest)


class CheckerBoardMoveToTestCase(unittest.TestCase):
    def test_move_to_updates_piece_row_col(self):
        checkers = CheckerBoard()

        source = checkers.get_piece_at(3, 2)
        dest = checkers.get_piece_at(4, 1)
        checkers.move_piece_to((3, 2), (4, 1))

        self.assertEqual((4, 1), (source.row, source.col))
        self.assertEqual((3, 2), (dest.row, dest.col))

    def test_move_to_resets_cache(self):
        checkers = CheckerBoard()

        source = checkers.get_piece_at(3, 2)
        dest = checkers.get_piece_at(4, 1)

        checkers._cache_valid_moves[(3, 2)] = {(4, 1): [dest]}
        checkers.move_piece_to((3, 2), (4, 1))

        self.assertFalse(checkers.is_cache_set_for_piece((3, 2)))

    def test_red_moves_right_when_open(self):
        checkers = CheckerBoard()

        red_piece = checkers.get_piece_at(3, 2)
        checkers.move_piece_to((3, 2), (4, 1))

        self.assertEqual(checkers.get_piece_at(4, 1), red_piece)

    def test_red_moves_left_when_open(self):
        checkers = CheckerBoard()

        red_piece = checkers.get_piece_at(3, 2)
        checkers.move_piece_to((3, 2), (4, 3))

        self.assertEqual(checkers.get_piece_at(4, 3), red_piece)

    def test_black_moves_left_when_open(self):
        checkers = CheckerBoard()

        black_piece = checkers.get_piece_at(6, 3)
        checkers.move_piece_to((6, 3), (5, 2))

        self.assertEqual(checkers.get_piece_at(5, 2), black_piece)

    def test_black_moves_right_when_open(self):
        checkers = CheckerBoard()

        black_piece = checkers.get_piece_at(6, 3)
        checkers.move_piece_to((6, 3), (5, 4))

        self.assertEqual(checkers.get_piece_at(5, 4), black_piece)

    def test_red_king_moves_forward(self):
        checkers = CheckerBoard()

        red_piece = checkers.get_piece_at(3, 2)
        red_piece.is_king = True

        checkers.move_piece_to((3, 2), (4, 3))
        self.assertEqual(checkers.get_piece_at(4, 3), red_piece)

    def test_red_king_moves_backward(self):
        checkers = CheckerBoard()

        red_piece = checkers.get_piece_at(3, 2)
        red_piece.is_king = True

        checkers.move_piece_to((3, 2), (4, 3))
        checkers.move_piece_to((4, 3), (3, 2))
        self.assertEqual(checkers.get_piece_at(3, 2), red_piece)

    def test_black_king_moves_forward(self):
        checkers = CheckerBoard()

        black_piece = checkers.get_piece_at(6, 3)
        black_piece.is_king = True
        checkers.move_piece_to((6, 3), (5, 2))

        self.assertEqual(checkers.get_piece_at(5, 2), black_piece)

    def test_black_king_moves_backward(self):
        checkers = CheckerBoard()

        black_piece = checkers.get_piece_at(6, 3)
        black_piece.is_king = True
        checkers.move_piece_to((6, 3), (5, 2))
        checkers.move_piece_to((5, 2), (6, 3))

        self.assertEqual(checkers.get_piece_at(6, 3), black_piece)

    def test_move_to_kings_red_piece(self):
        checkers = CheckerBoard()

        red_piece = checkers.get_piece_at(3, 2)
        checkers.move_piece_to((3, 2), (8, 1))

        self.assertTrue(red_piece.is_king)

    def test_move_to_kings_black_piece(self):
        checkers = CheckerBoard()

        black_piece = checkers.get_piece_at(8, 1)
        checkers.move_piece_to((8, 1), (1, 2))

        self.assertTrue(black_piece.is_king)

    def test_move_to_updates_black_king_count(self):
        checkers = CheckerBoard()

        black_piece = checkers.get_piece_at(8, 1)
        checkers.move_piece_to((8, 1), (1, 2))

        self.assertEqual(checkers.black_kings, 1)

    def test_move_to_updates_red_king_count(self):
        checkers = CheckerBoard()

        red_piece = checkers.get_piece_at(3, 2)
        checkers.move_piece_to((3, 2), (8, 1))

        self.assertEqual(checkers.red_kings, 1)


class CheckerBoardTraverseBoardTestCase(unittest.TestCase):
    def test_traverse_board_for_corner_only_has_one_open(self):
        checkers = CheckerBoard()
        black_piece = checkers.get_piece_at(6, 1)
        moves = checkers.traverse_board(black_piece)

        self.assertTrue((5, 2) in moves)
        self.assertTrue(len(moves) == 1)

    def test_traverse_board_for_red_piece_only_open_spots(self):
        checkers = CheckerBoard()
        red_piece = checkers.get_piece_at(3, 2)
        moves = checkers.traverse_board(red_piece)

        self.assertTrue((4, 1) in moves)
        self.assertTrue((4, 3) in moves)

    def test_traverse_board_for_red_piece_has_single_jump(self):
        checkers = CheckerBoard()
        red_piece = checkers.get_piece_at(3, 2)
        checkers.move_piece_to((6, 3), (4, 3))
        black_piece = checkers.board[4][3]
        moves = checkers.traverse_board(red_piece)

        self.assertTrue((4, 1) in moves)
        self.assertTrue((5, 4) in moves)
        self.assertTrue(black_piece in moves[(5, 4)])

    def test_traverse_board_for_red_piece_has_multi_jumps(self):
        checkers = CheckerBoard()
        red_piece = checkers.get_piece_at(3, 2)

        # move two black pieces so it can be multi-jumped
        checkers.move_piece_to((6, 3), (4, 3))
        checkers.move_piece_to((7, 2), (6, 3))

        black_piece = checkers.board[4][3]
        black_piece_two = checkers.board[6][3]

        moves = checkers.traverse_board(red_piece)

        self.assertTrue((4, 1) in moves)
        self.assertTrue((5, 4) in moves)
        self.assertTrue((7, 2) in moves)
        self.assertEqual(len(moves[(5, 4)]), 1)
        self.assertEqual(len(moves[7, 2]), 2)
        self.assertTrue(black_piece in moves[(5, 4)])
        self.assertTrue(black_piece in moves[(7, 2)])
        self.assertTrue(black_piece_two in moves[(7, 2)])

    def test_traverse_board_for_red_king_only_forward_open(self):
        checkers = CheckerBoard()
        red_piece = checkers.get_piece_at(3, 2)
        red_piece.is_king = True
        moves = checkers.traverse_board(red_piece)

        self.assertEqual(len(moves), 2)
        self.assertTrue((4, 1) in moves)
        self.assertTrue((4, 3) in moves)

    def test_traverse_board_for_red_king_only_backward_open(self):
        checkers = CheckerBoard()
        red_piece = checkers.get_piece_at(3, 2)
        checkers.move_piece_to((3, 2), (5, 4))
        red_piece.is_king = True
        moves = checkers.traverse_board(red_piece)

        self.assertEqual(len(moves), 2)
        self.assertTrue((4, 5) in moves)
        self.assertTrue((4, 3) in moves)

    def test_traverse_board_for_red_king_piece_has_single_backward_jumps(self):
        checkers = CheckerBoard()

        checkers.move_piece_to((6, 3), (5, 4))
        black_piece = checkers.board[5][4]

        checkers.move_piece_to((3, 2), (6, 3))
        red_piece = checkers.get_piece_at(6, 3)
        red_piece.is_king = True

        moves = checkers.traverse_board(red_piece)

        self.assertTrue((4, 5) in moves)
        self.assertTrue((5, 2) in moves)
        self.assertEqual(len(moves[(4, 5)]), 1)
        self.assertEqual(len(moves[(5, 2)]), 0)
        self.assertTrue(black_piece in moves[(4, 5)])

    def test_traverse_board_for_red_king_piece_has_multi_backward_jumps(self):
        checkers = CheckerBoard()

        # move two black pieces so it can be multi-jumped
        checkers.move_piece_to((6, 3), (5, 4))
        checkers.move_piece_to((3, 4), (6, 3))
        checkers.move_piece_to((6, 5), (3, 4))

        checkers.board[2][3] = OpenPiece(2, 3)

        black_piece = checkers.board[5][4]
        black_piece_two = checkers.board[3][4]
        red_piece = checkers.get_piece_at(6, 3)

        red_piece.is_king = True

        moves = checkers.traverse_board(red_piece)

        self.assertTrue((4, 5) in moves)
        self.assertTrue((2, 3) in moves)
        self.assertEqual(len(moves[(4, 5)]), 1)
        self.assertEqual(len(moves[2, 3]), 2)
        self.assertTrue(black_piece in moves[(4, 5)])
        self.assertTrue(black_piece in moves[(2, 3)])
        self.assertTrue(black_piece_two in moves[(2, 3)])

    def test_traverse_board_for_red_king_piece_has_multi_forward_and_back_jumps(self):
        checkers = CheckerBoard()

        # move two black pieces so it can be multi-jumped
        checkers.move_piece_to((6, 3), (4, 5))
        checkers.move_piece_to((6, 5), (4, 3))

        checkers.board[3][2] = OpenPiece(3, 2)

        black_piece = checkers.board[4][5]
        black_piece_two = checkers.board[4][3]
        red_piece = checkers.get_piece_at(3, 6)

        red_piece.is_king = True

        moves = checkers.traverse_board(red_piece)

        self.assertTrue((5, 4) in moves)
        self.assertTrue((3, 2) in moves)
        self.assertEqual(len(moves[(5, 4)]), 1)
        self.assertEqual(len(moves[3, 2]), 2)
        self.assertTrue(black_piece in moves[(5, 4)])
        self.assertTrue(black_piece in moves[(3, 2)])
        self.assertTrue(black_piece_two in moves[(3, 2)])

    def test_traverse_board_for_black_piece_only_open_spots(self):
        checkers = CheckerBoard()
        black_piece = checkers.get_piece_at(6, 3)
        moves = checkers.traverse_board(black_piece)

        self.assertTrue((5, 2) in moves)
        self.assertTrue((5, 4) in moves)
        self.assertEqual(len(moves[(5, 2)]), 0)
        self.assertEqual((len(moves[(5, 4)])), 0)

    def test_traverse_board_for_black_piece_has_single_jump(self):
        checkers = CheckerBoard()
        red_piece = checkers.get_piece_at(3, 2)
        checkers.move_piece_to((6, 3), (4, 3))
        black_piece = checkers.board[4][3]
        moves = checkers.traverse_board(red_piece)

        self.assertTrue((4, 1) in moves)
        self.assertTrue((5, 4) in moves)
        self.assertTrue(black_piece in moves[(5, 4)])

    def test_traverse_board_for_black_piece_has_multi_jumps(self):
        checkers = CheckerBoard()
        black_piece = checkers.board[6][3]

        # move red piece so it can be multi-jumped
        checkers.move_piece_to((2, 3), (5, 4))

        red_piece = checkers.board[5][4]
        red_piece_two = checkers.board[3][4]

        moves = checkers.traverse_board(black_piece)

        self.assertTrue((4, 5) in moves)
        self.assertTrue((2, 3) in moves)
        self.assertTrue((5, 2) in moves)

        self.assertEqual(len(moves[(4, 5)]), 1)
        self.assertEqual(len(moves[2, 3]), 2)
        self.assertTrue(red_piece in moves[(4, 5)])
        self.assertTrue(red_piece in moves[(2, 3)])
        self.assertTrue(red_piece_two in moves[(2, 3)])

    def test_traverse_board_for_black_king_only_forward_open(self):
        checkers = CheckerBoard()

        black_piece = checkers.get_piece_at(6, 3)
        black_piece.is_king = True

        moves = checkers.traverse_board(black_piece)

        self.assertEqual(len(moves), 2)
        self.assertTrue((5, 2) in moves)
        self.assertTrue((5, 4) in moves)

    def test_traverse_board_for_black_king_only_backward_open(self):
        checkers = CheckerBoard()

        checkers.move_piece_to((6, 3), (4, 3))
        black_piece = checkers.get_piece_at(4, 3)
        black_piece.is_king = True

        moves = checkers.traverse_board(black_piece)

        self.assertEqual(len(moves), 2)
        self.assertTrue((5, 2) in moves)
        self.assertTrue((5, 4) in moves)

    def test_traverse_board_for_black_king_piece_has_single_backward_jumps(self):
        checkers = CheckerBoard()

        checkers.move_piece_to((3, 4), (4, 3))
        red_piece = checkers.get_piece_at(4, 3)

        checkers.move_piece_to((6, 3), (3, 4))
        black_piece = checkers.board[3][4]
        black_piece.is_king = True

        moves = checkers.traverse_board(black_piece)

        self.assertTrue((4, 5) in moves)
        self.assertTrue((5, 2) in moves)
        self.assertEqual(len(moves[(4, 5)]), 0)
        self.assertEqual(len(moves[(5, 2)]), 1)
        self.assertTrue(red_piece in moves[(5, 2)])

    def test_traverse_board_for_black_king_piece_has_multi_backward_jumps(self):
        checkers = CheckerBoard()

        # move two red pieces so it can be multi-jumped
        checkers.move_piece_to((3, 4), (4, 3))
        checkers.move_piece_to((6, 3), (3, 4))
        checkers.move_piece_to((3, 2), (6, 3))

        checkers.board[7][4] = OpenPiece(7, 4)

        red_piece = checkers.get_piece_at(4, 3)
        red_piece_two = checkers.get_piece_at(6, 3)
        black_piece = checkers.get_piece_at(3, 4)

        black_piece.is_king = True

        moves = checkers.traverse_board(black_piece)

        self.assertTrue((5, 2) in moves)
        self.assertTrue((7, 4) in moves)
        self.assertEqual(len(moves[(5, 2)]), 1)
        self.assertEqual(len(moves[7, 4]), 2)
        self.assertTrue(red_piece in moves[(5, 2)])
        self.assertTrue(red_piece in moves[(7, 4)])
        self.assertTrue(red_piece_two in moves[(7, 4)])

    def test_traverse_board_for_black_king_piece_has_multi_forward_and_back_jumps(self):
        checkers = CheckerBoard()

        # move two black pieces so it can be multi-jumped
        checkers.move_piece_to((3, 4), (5, 4))
        checkers.move_piece_to((3, 2), (5, 6))

        checkers.board[6][7] = OpenPiece(6, 7)

        red_piece = checkers.board[5][4]
        red_piece_two = checkers.board[5][6]
        black_piece = checkers.get_piece_at(6, 3)

        black_piece.is_king = True

        moves = checkers.traverse_board(black_piece)

        self.assertTrue((4, 5) in moves)
        self.assertTrue((6, 7) in moves)
        self.assertEqual(len(moves[(4, 5)]), 1)
        self.assertEqual(len(moves[6, 7]), 2)
        self.assertTrue(red_piece in moves[(4, 5)])
        self.assertTrue(red_piece in moves[(6, 7)])
        self.assertTrue(red_piece_two in moves[(6, 7)])


class CheckerBoardUtilitiesTestCase(unittest.TestCase):
    def test_to_json_has_correct_keys(self):
        checkers = CheckerBoard()
        json = checkers.to_json()

        self.assertTrue("turn" in json)
        self.assertTrue("red_left" in json)
        self.assertTrue("black_left" in json)
        self.assertTrue("board" in json)
        self.assertTrue(len(json) == 4)
