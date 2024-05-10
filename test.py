import unittest

from Connect_5_minimax_optimized.board import Board
from Connect_5_minimax_optimized.bot import Bot


class TestBot(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.bot = Bot(self.board)

    def test_init(self):
        self.assertEqual(self.bot.board, self.board)
        self.assertEqual(self.bot.x_index_chains, [])
        self.assertEqual(self.bot.o_index_chains, [])

    def test_recalculate_chains(self):
        indexes = {0, 19, 380, 399}
        shifted_indexes = {0, 19, 399, 418}
        self.bot.x_index_chains.append(indexes)
        self.bot.recalculate_chain(True)
        self.assertEqual(shifted_indexes, self.bot.x_index_chains[0])

    def test_add_last_move(self):
        indexes1 = {59, 79}
        indexes2 = {19}
        move = (2, 20)
        solution = {19, 39, 59, 79}
        self.board.x_indexes.update(indexes1.union(indexes2))
        self.bot.x_index_chains.append(indexes1)
        self.bot.x_index_chains.append(indexes2)
        self.bot.add_last_move(move, True)
        print(self.bot.x_index_chains)
        self.assertEqual(solution, self.bot.x_index_chains[0])


    def test_vet_closed_chains(self):
        pass


    def test_add_index_to_chain(self):
        pass

    def test_check_for_overlap_dir1(self):
        #check for angle
        self.bot.o_index_chains.append({84, 85, 86})
        self.bot.o_index_chains.append({82, 83, 84})
        self.bot.check_for_overlap([(0, 1), (1, 1)], False)
        self.assertEqual([{82, 83, 84, 85, 86}], self.bot.o_index_chains)

    def test_check_for_overlap_dir19(self):
        self.bot.o_index_chains.append({84, 103, 122})
        self.bot.o_index_chains.append({122, 141, 160})
        self.bot.check_for_overlap([(0, 19), (1, 19)], False)
        self.assertEqual([{84, 103, 122, 141, 160}], self.bot.o_index_chains)

    def test_check_for_overlap_dir20(self):
        self.bot.o_index_chains.append({84, 104, 124})
        self.bot.o_index_chains.append({124, 144, 164})
        self.bot.check_for_overlap([(0, 20), (1, 20)], False)
        self.assertEqual([{84, 104, 124, 144, 164}], self.bot.o_index_chains)

    def test_check_for_overlap_dir21(self):
        self.bot.o_index_chains.append({84, 105, 126})
        self.bot.o_index_chains.append({126, 147, 168})
        self.bot.check_for_overlap([(0, 21), (1, 21)], False)
        self.assertEqual([{84, 105, 126, 147, 168}], self.bot.o_index_chains)

    def test_delete_indexes_from_chain_o_dir1(self):
        self.bot.o_index_chains.append({84, 85, 86})
        self.bot.x_index_chains.append({87, 88})
        self.bot.x_index_chains.append({82, 83})
        self.bot.check_for_open_chains([0], False)
        self.assertEqual([], self.bot.o_index_chains)
        self.assertEqual([{82, 83}, {87, 88}], self.bot.x_index_chains)

    def test_delete_indexes_from_chain_o_dir19(self):
        self.bot.o_index_chains.append({84, 103, 122})
        self.bot.x_index_chains.append({65})
        self.bot.x_index_chains.append({141})
        self.bot.check_for_open_chains([0], False)
        self.assertEqual([], self.bot.o_index_chains)
        self.assertEqual([{65}, {141}], self.bot.x_index_chains)

    def test_delete_indexes_from_chain_o_dir20(self):
        self.bot.o_index_chains.append({84, 104, 124})
        self.bot.x_index_chains.append({64})
        self.bot.x_index_chains.append({144})
        self.bot.check_for_open_chains([0], False)
        self.assertEqual([], self.bot.o_index_chains)
        self.assertEqual([{64}, {144}], self.bot.x_index_chains)

    def test_delete_indexes_from_chain_o_dir21(self):
        self.bot.o_index_chains.append({84, 105, 126})
        self.bot.x_index_chains.append({63})
        self.bot.x_index_chains.append({147})
        self.bot.check_for_open_chains([0], False)
        self.assertEqual([], self.bot.o_index_chains)
        self.assertEqual([{63}, {147}], self.bot.x_index_chains)

    def test_smart_move(self):
        pass


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

    def test_is_index_in_indexes_for_player(self):
        x_index = 0
        o_index = 1
        player_x = True
        player_o = False

        self.assertFalse(self.board.is_index_in_indexes_for_player(x_index, player_x))
        self.assertFalse(self.board.is_index_in_indexes_for_player(o_index, player_o))

        self.board.x_indexes.add(x_index)
        self.board.o_indexes.add(o_index)
        self.assertTrue(self.board.is_index_in_indexes_for_player(x_index, player_x))
        self.assertTrue(self.board.is_index_in_indexes_for_player(o_index, player_o))

    def test_get_neighbours(self):
        neighbours = {1, 20, 21, 379, 398, 378, 18, 38, 39, 360, 361, 381}
        indexes = {0, 19, 380, 399}
        player_x = True
        player_o = False
        for neighbour in neighbours:
            self.board.x_indexes.add(neighbour)
            self.board.o_indexes.add(neighbour)
        self.assertEqual({1, 20, 21}, self.board.get_neighbours(0, player_x))
        self.assertEqual({18, 38, 39}, self.board.get_neighbours(19, player_x))
        self.assertEqual({360, 361, 381}, self.board.get_neighbours(380, player_x))
        self.assertEqual({379, 398, 378}, self.board.get_neighbours(399, player_x))
        self.assertEqual({1, 20, 21}, self.board.get_neighbours(0, player_o))
        self.assertEqual({18, 38, 39}, self.board.get_neighbours(19, player_o))
        self.assertEqual({360, 361, 381}, self.board.get_neighbours(380, player_o))
        self.assertEqual({379, 398, 378}, self.board.get_neighbours(399, player_o))

    def test_move(self):
        x = [1, 21]
        y = [1, 21]
        player_x = True
        self.assertFalse(self.board.move(x[0], y[0], player_x)[1])
        with self.assertRaises(IndexError):
            self.board.move(x[0], y[0], player_x)
        self.assertTrue(self.board.move(x[1], y[1], player_x)[1])

    def test_check_for_win_horizontal(self):
        player_x = True
        chain = {1, 2, 3, 4}
        x = [1, 1, 1]
        y = [1, 3, 5]
        index = 0
        for i in chain:
            self.board.x_indexes.add(i)

        self.assertFalse(self.board.check_for_win(1, 2, player_x))
        self.board.x_indexes.add(index)
        for i in range(len(x)):
            self.assertTrue(self.board.check_for_win(x[i], y[i], player_x))

    def test_check_for_win_vertical(self):
        player_x = True
        chain = {20, 40, 60, 80}
        x = [1, 3, 5]
        y = [1, 1, 1]
        index = 0
        for i in chain:
            self.board.x_indexes.add(i)

        self.assertFalse(self.board.check_for_win(2, 1, player_x))
        self.board.x_indexes.add(index)
        for i in range(len(x)):
            self.assertTrue(self.board.check_for_win(x[i], y[i], player_x))

    def test_check_for_win_diagonal_up_down(self):
        player_x = True
        chain = {21, 42, 63, 84}
        x = [1, 3, 5]
        y = [1, 3, 5]
        index = 0
        for i in chain:
            self.board.x_indexes.add(i)

        self.assertFalse(self.board.check_for_win(2, 2, player_x))
        self.board.x_indexes.add(index)
        for i in range(len(x)):
            self.assertTrue(self.board.check_for_win(x[i], y[i], player_x))

    def test_check_for_win_diagonal_down_up(self):
        player_x = True
        chain = {61, 42, 23, 4}
        x = [5, 3, 1]
        y = [1, 3, 5]
        index = 80
        for i in chain:
            self.board.x_indexes.add(i)

        self.assertFalse(self.board.check_for_win(4, 2, player_x))
        self.board.x_indexes.add(index)
        for i in range(len(x)):
            self.assertTrue(self.board.check_for_win(x[i], y[i], player_x))

    def test_print_board(self):
        self.board.print_board()
