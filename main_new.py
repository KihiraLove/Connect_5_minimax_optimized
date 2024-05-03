import os

from board_new import Board
from bot_new import Bot

board = Board()
bot = Bot(board)
win = False
isPlayerX = True
enlarged = False
last_move = ()
while not win:
    os.system('cls' if os.name == 'nt' else 'clear')
    board.print_board()
    try:
        if isPlayerX:
            move = input("Enter your move (x y): ").split(' ')
            x = int(move[0])
            y = int(move[1])
            last_move = (x, y)
            win, enlarged = board.move(x, y, isPlayerX)
        else:
            win = bot.smart_move(last_move, enlarged)

        isPlayerX = not isPlayerX
    except IndexError:
        print("Invalid move")


