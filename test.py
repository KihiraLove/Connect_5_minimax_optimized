import unittest

from Connect_5_minimax_optimized.board import Board


class TestBoard(unittest.TestCase):

    def test_init(self):
        board = Board()
        self.assertEqual(board.o_indexes, set())
        self.assertEqual(board.x_indexes, set())
        self.assertEqual(board.size, 20)

    def test_enlarge(self):
        board = Board()
        board.o_indexes.add(0)
        board.o_indexes.add(19)
        board.x_indexes.add(380)
        board.x_indexes.add(399)
        board.enlarge()
        self.assertEqual(board.o_indexes, {0, 19})
        self.assertEqual(board.x_indexes, {399, 418})

if __name__ == '__main__':
    unittest.main()