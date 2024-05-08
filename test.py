import unittest

from Connect_5_minimax_optimized.board import Board


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_init(self):
        self.assertEqual(self.board.o_indexes, set())
        self.assertEqual(self.board.x_indexes, set())
        self.assertEqual(self.board.size, 20)

    def test_enlarge(self):
        self.board.o_indexes.add(0)
        self.board.o_indexes.add(19)
        self.board.x_indexes.add(380)
        self.board.x_indexes.add(399)
        self.board.enlarge()
        self.assertEqual(self.board.o_indexes, {0, 19})
        self.assertEqual(self.board.x_indexes, {399, 418})
        self.assertEqual(self.board.size, 21)

    def test_shift_indexes(self):
        indexes = {0, 19, 380, 399}
        shifted_indexes = {0, 19, 399, 418}
        self.assertEqual(self.board.shift_indexes(indexes), shifted_indexes)

    def test_calculate_index_from_position(self):
        x = [1, 1, 20, 20]
        y = [1, 20, 1, 20]
        indexes = [0, 19, 380, 399]
        for i in range(len(x)):
            self.assertEqual(self.board.calculate_index_from_position(x[i], y[i]), indexes[i])

    def test_calculate_position_from_index(self):
        x = [1, 1, 20, 20]
        y = [1, 20, 1, 20]
        indexes = [0, 19, 380, 399]
        for i in range(len(x)):
            self.assertEqual(self.board.calculate_position_from_index(indexes[i]), (x[i], y[i]))

    def test_add_index(self):
        player_x = True
        player_o = False
        indexes = {0, 19, 380, 399}
        for index in indexes:
            self.board.add_index(index, player_x)
            self.board.add_index(index, player_o)
        self.assertEqual(self.board.x_indexes, indexes)
        self.assertEqual(self.board.o_indexes, indexes)

    def test_set_position(self):
        x = [1, 1, 20, 20]
        y = [1, 20, 1, 20]
        x_over_size = 21
        y_over_size = 21
        player_x = True
        player_o = False
        indexes = {0, 19, 380, 399}
        shifted_indexes = {0, 19, 399, 418, 440}
        for i in range(len(x)):
            self.assertFalse(self.board.set_position(x[i], y[i], player_x))
            self.assertFalse(self.board.set_position(x[i], y[i], player_o))

        self.assertEqual(self.board.x_indexes, indexes)
        self.assertEqual(self.board.o_indexes, indexes)

        self.assertTrue(self.board.set_position(x_over_size, y_over_size, player_x))
        self.assertEqual(self.board.x_indexes, shifted_indexes)

    def test_is_position_valid_empty(self):
        player_x = True
        x = [1, 1, 20, 20]
        y = [1, 20, 1, 20]
        for i in range(len(x)):
            self.assertTrue(self.board.is_position_valid(x[i], y[i]))

    def test_is_position_valid_occupied(self):
        player_x = True
        x = [1, 1, 20, 20]
        y = [1, 20, 1, 20]
        for i in range(len(x)):
            self.board.set_position(x[i], y[i], player_x)

        for i in range(len(x)):
            self.assertFalse(self.board.is_position_valid(x[i], y[i]))

    def test_is_position_valid_out_of_bounds(self):
        player_x = True
        x = [0, 0, 22, 22]
        y = [0, 22, 0, 22]
        for i in range(len(x)):
            self.board.set_position(x[i], y[i], player_x)

        for i in range(len(x)):
            self.assertFalse(self.board.is_position_valid(x[i], y[i]))

    def test_is_index_occupied(self):
        x_indexes = {0, 19, 380, 399}
        o_indexes = {1, 18, 381, 398}
        for i in x_indexes.union(o_indexes):
            self.assertFalse(self.board.is_index_occupied(i))
        for i in x_indexes:
            self.board.x_indexes.add(i)
        for i in o_indexes:
            self.board.o_indexes.add(i)
        for i in x_indexes.union(o_indexes):
            self.assertTrue(self.board.is_index_occupied(i))