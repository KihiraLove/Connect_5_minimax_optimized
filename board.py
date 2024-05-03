class Board:
    def __init__(self):
        # fix board size
        self.size = 20
        self.one_row = []
        self.the_board = []
        for i in range(self.size):
            self.one_row.append(' ')
        for i in range(self.size):
            self.the_board.append(self.one_row.copy())
        self.minx = None
        self.maxx = None
        self.miny = None
        self.maxy = None

    def set_size(self, size, old_size):
        self.size = size
        old_board = self.the_board.copy()
        self.the_board.clear()
        self.one_row.clear()
        for i in range(self.size):
            self.one_row.append(' ')
        for i in range(self.size):
            self.the_board.append(self.one_row.copy())

        for i in range(old_size):
            for j in range(old_size):
                self.the_board[i][j] = old_board[i][j]

    def get_size(self):
        return self.size

    def get_cell(self, x, y):
        if x < 0 or y < 0:
            return None
        if x > self.size - 1 or y > self.size - 1:
            return ' '
        return self.the_board[x][y]

    def set_position(self, x, y, current_player):
        if x > self.size - 1 or y > self.size - 1:
            self.set_size(max(x + 1, y + 1), self.size)
        self.the_board[x][y] = current_player
        if self.minx is None:
            self.minx = x - 1
        elif x == 0:
            self.minx = 0
        elif x <= self.minx:
            self.minx = x - 1

        if self.maxx is None:
            self.maxx = x + 1
        elif x > self.maxx:
            self.maxx = x + 1

        if self.miny is None:
            self.miny = y - 1
        elif y == 0:
            self.miny = 0
        elif y <= self.miny:
            self.miny = y - 1

        if self.maxy is None:
            self.maxy = y + 1
        elif y > self.maxy:
            self.maxy = y + 1

    def print_board(self):
        print("    ", end="")
        for i in range(1, self.size + 1):
            if i < 10:
                print(f"{i}  ", end=' ')
            else:
                print(f"{i} ", end=' ')
        print("")
        number = 1
        for row in self.the_board:
            if number < 10:
                print(f'{number} | ', end='')
            else:
                print(f'{number}| ', end='')
            for column in row:
                print(column, end=' | ')
            print("")
            number += 1

    def check_for_winner(self, current_player):
        for x in range(self.size):
            for y in range(self.size):
                if self.get_cell(x, y) == current_player:
                    # check if someone won right straight
                    if x < self.size and y + 1 < self.size and self.get_cell(x, y + 1) == current_player:
                        counter = 2
                        x1 = x
                        y1 = y + 2
                        while x1 < self.size and y1 < self.size and self.get_cell(x1,
                                                                                                 y1) == current_player and counter < 5:
                            counter += 1
                            y1 += 1
                        if counter > 4:
                            return True
                    # check if someone won left down
                    if x + 1 < self.size and y - 1 > 0 and self.get_cell(x + 1, y - 1) == current_player:
                        counter = 2
                        x1 = x + 2
                        y1 = y - 2
                        while x1 < self.size and y1 > 0 and self.get_cell(x1,
                                                                                  y1) == current_player and counter < 5:
                            counter += 1
                            x1 += 1
                            y1 -= 1
                        if counter > 4:
                            return True
                    # check if someone won straight down
                    if x + 1 < self.size and y < self.size and self.get_cell(x + 1, y) == current_player:
                        counter = 2
                        x1 = x + 2
                        y1 = y
                        while x1 < self.size and y1 < self.size and self.get_cell(x1,
                                                                                                 y1) == current_player and counter < 5:
                            counter += 1
                            x1 += 1
                        if counter > 4:
                            return True
                    # check if someone won right down
                    if x + 1 < self.size and y + 1 < self.size and self.get_cell(x + 1,
                                                                                                y + 1) == current_player:
                        counter = 2
                        x1 = x + 2
                        y1 = y + 2
                        while x1 < self.size and y1 < self.size and self.get_cell(x1,
                                                                                                 y1) == current_player and counter < 5:
                            counter += 1
                            x1 += 1
                            y1 += 1
                            if counter > 4:
                                return True
        return False

