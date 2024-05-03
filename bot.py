import copy
import random


class Node:
    def __init__(self, step, player, value=float('-inf'), board=None):
        self.val = value
        self.children = []
        self.step = step
        self.player = player
        if len(step) > 0:
            board.set_position(self.step[0], self.step[1], player)
        self.board = board

    def get_board(self):
        return self.board

    def add_child(self, child):
        self.children.extend(child)

    def set_value(self, value):
        self.val = value

    def set_step(self, step):
        self.step = step

    def get_player(self):
        return self.player


class Bot:
    def __init__(self):
        self.step = [0, 0]

    def collect_possible_moves(self, board):
        possible_moves = []
        # consider open 4 'O'
        if self.movement(board, 'O', 4):
            possible_moves.append(self.step)
            return possible_moves
        # consider open 4 'X'
        if self.movement(board, 'X', 4):
            possible_moves.append(self.step)
            return possible_moves
        # consider open 3 'O'
        possible_moves.extend(self.look_for_3_emp_emp(board, 'O'))
        # consider open 3 'X'
        if len(possible_moves) == 0:
            possible_moves.extend(self.look_for_3_emp_emp(board, 'X'))
        # consider every move #TODO limit it somehow
        if len(possible_moves) == 0:
            for row in range(board.minx, board.maxx + 1):
                for col in range(board.miny, board.maxy + 1):
                    if self.movement_valid(row, col, board):
                        possible_moves.append([row, col])
        return possible_moves

    def smart_move(self, board):
        if self.movement(board, 'O', 4):
            pass
        elif self.movement(board, 'X', 4):
            pass
        else:
            head = Node((), '0', board=board)
            head.set_value(self.minimax(head, 0, True, float('-inf'), float('+inf')))
            # self.step already set
        board.set_position(self.step[0], self.step[1], "O")
        return

    def is_leaf(self, node):
        if node.get_board().check_for_winner(node.get_player()):
            return True
        return False

    #TODO update heuristic
    def heuristic(self, node):
        return random.randint(0, 10)

    def minimax(self, node, depth, isMaximizingPlayer, alpha, beta):
        # if capacity available remove the depth limit
        if self.is_leaf(node):
            if node.get_player() == 'O':
                return float('+inf')
            else:
                return float('-inf')
        elif depth == 5:
            return self.heuristic(node)

        if isMaximizingPlayer:
            bestVal = float('-inf')
            all_possible_moves = copy.deepcopy(self.collect_possible_moves(node.get_board()))
            for one_move in all_possible_moves:
                new_node = Node(one_move, 'O', board=copy.deepcopy(node.get_board()))
                node.add_child([new_node])  #TODO probably not needed
                value = self.minimax(new_node, depth + 1, False, alpha, beta)
                node.set_value(value) #TODO probably not needed
                bestVal = max(bestVal, value)
                if value >= bestVal and depth == 0:
                    self.step = one_move
                alpha = max(alpha, bestVal)
                if beta <= alpha:
                    break
            return bestVal

        else:
            bestVal = float('+inf')
            all_possible_moves = copy.deepcopy(self.collect_possible_moves(node.get_board()))
            for one_move in all_possible_moves:
                new_node = Node(one_move, 'X', board=copy.deepcopy(node.get_board()))
                node.add_child([new_node])
                value = self.minimax(new_node, depth + 1, True, alpha, beta)
                node.set_value(value)
                bestVal = min(bestVal, value)
                beta = min(beta, bestVal)
                if beta <= alpha:
                    break
            return bestVal

    def move(self, board):
        if self.movement(board, 'X', 4):
            board.set_position(self.step[0], self.step[1], "O")
            return
        elif self.look_for_3_emp_emp(board, 'X'):
            board.set_position(self.step[0], self.step[1], "O")
            return

        i = 4
        while i > 0:
            if self.movement(board, 'O', i):
                board.set_position(self.step[0], self.step[1], "O")
                return
            i -= 1

        self.movement(board, 'X', 1)
        board.set_position(self.step[0], self.step[1], "O")
        return

    def look_for_3_emp_emp(self, board, look_for):
        possible_moves = []
        for x in range(board.get_size()):
            for y in range(board.get_size()):
                if board.get_cell(x, y) == look_for:
                    # keresunk 3mat vizszintesen jobbra ami mindket oldalrol ures
                    if board.get_cell(x, y - 1) == ' ' and board.get_cell(x, y + 1) == look_for and board.get_cell(
                            x, y + 2) == look_for and board.get_cell(x, y + 3) == ' ':
                        if self.movement_valid(x, y - 1, board):
                            possible_moves.append([x, y - 1])
                        elif self.movement_valid(x, y + 3, board):
                            possible_moves.append([x, y + 3])

                    # keresunk 3mat balra le ami mindket oldalrol ures
                    if board.get_cell(x - 1, y + 1) == ' ' and board.get_cell(x + 1,
                                                                              y - 1) == look_for and board.get_cell(
                            x + 2, y - 2) == look_for and board.get_cell(x + 3, y - 3) == ' ':
                        if self.movement_valid(x - 1, y + 1, board):
                            possible_moves.append([x - 1, y + 1])
                        elif self.movement_valid(x + 3, y - 3, board):
                            possible_moves.append([x + 3, y - 3])

                    # keresunk 3mat jobbra lefele ami mindket oldalrol ures
                    if board.get_cell(x - 1, y - 1) == ' ' and board.get_cell(x + 1,
                                                                              y + 1) == look_for and board.get_cell(
                            x + 2, y + 2) == look_for and board.get_cell(x + 3, y + 3) == ' ':
                        if self.movement_valid(x - 1, y - 1, board):
                            possible_moves.append([x - 1, y - 1])
                        elif self.movement_valid(x + 3, y + 3, board):
                            possible_moves.append([x + 3, y + 3])

                    # keresunk 3mat fuggolegesen lefele ami mindket oldalrol ures
                    if board.get_cell(x - 1, y) == ' ' and board.get_cell(x + 1, y) == look_for and board.get_cell(
                            x + 2, y) == look_for and board.get_cell(x + 3, y) == ' ':
                        if self.movement_valid(x - 1, y, board):
                            possible_moves.append([x - 1, y])
                        elif self.movement_valid(x + 3, y, board):
                            possible_moves.append([x + 3, y])
        return possible_moves

    def movement(self, board, look_for, how_many):
        for x in range(board.get_size()):
            for y in range(board.get_size()):
                if board.get_cell(x, y) == look_for:
                    # count x right straight
                    if self.char_counter(board, x, y, look_for, how_many, 0, 1):
                        return True
                    # count x left down
                    if self.char_counter(board, x, y, look_for, how_many, 1, -1):
                        return True
                    # count x right down
                    if self.char_counter(board, x, y, look_for, how_many, 1, 1):
                        return True
                    # count x down
                    if self.char_counter(board, x, y, look_for, how_many, 1, 0):
                        return True

        return False

    def char_counter(self, board, x, y, look_for, how_many, x_inc, y_inc):
        prev_x = x - x_inc
        prev_y = y - y_inc

        counter = 1
        x += x_inc
        y += y_inc
        while counter != how_many:
            if 0 < x < board.get_size() and 0 < y < board.get_size() and board.get_cell(x, y) == look_for:
                counter += 1
                x += x_inc
                y += y_inc
            else:
                break
        if self.movement_valid(x, y, board) and counter == how_many:
            self.step = [x, y]
            return True
        elif self.movement_valid(prev_x, prev_y, board) and counter == how_many:
            self.step = [prev_x, prev_y]
            return True

        return False

    def movement_valid(self, x, y, board):
        if board.get_cell(x, y) != 'X' and board.get_cell(x, y) != 'O' and 0 < x < 98 and 0 < y < 98:
            return True
        return False
