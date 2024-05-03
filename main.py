from board import Board
from player import Player
from bot import Bot


board = Board()
player = Player()
bot = Bot()
board.print_board()

while True:
    if board.check_for_winner('O'):
        board.print_board()
        print('You lost!')
        break
    else:
        player.move(board)

    if board.check_for_winner('X'):
        board.print_board()
        print('You won!')
        break
    else:
        bot.smart_move(board)
    board.print_board()

# END

print('Game Over!')
print('push test')
