from board import Board


class Player:
    def move(self, board):
        player_move = self.user_input(board)
        board.set_position(player_move[0] - 1, player_move[1] - 1, "X")

    def user_input(self, board):
        while True:
            try:
                mov = input("Enter your move (x y): ").split(' ')
                x = int(mov[0])
                y = int(mov[1])
                if x < 1 or y < 1 or x > 99 or y > 99:
                    print("Invalid")
                elif self.movement_valid(x - 1, y - 1, board):
                    return [x, y]
            except Exception as e:
                print("Invalid")

    def movement_valid(self, x, y, board):
        if board.get_cell(x, y) != 'X' and board.get_cell(x, y) != 'O':
            return True
        print("Invalid")
        return False
